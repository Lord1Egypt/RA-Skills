#!/usr/bin/env python3
"""
PaddleOCR-VL MCP Server — GPU-accelerated document parsing via ephemeral Docker.
Auto-detects NVIDIA GPU architecture and selects the correct official image.

Supported architectures:
  - Blackwell (SM120 / compute capability >= 12.0) → paddleocr-vl:latest-nvidia-gpu-sm120
  - Other NVIDIA GPU                              → paddleocr-vl:latest-nvidia-gpu

First-run: if the image is not pulled yet, the check_environment tool prints the
exact docker pull + run commands from the official PaddleOCR docs.

SkillHub: https://skillhub.cloud.tencent.com/
Official docs: https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ---------------------------------------------------------------------------
# Image registry
# ---------------------------------------------------------------------------

BLACKWELL_IMAGE = (
    "ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/"
    "paddleocr-vl:latest-nvidia-gpu-sm120"
)
STANDARD_IMAGE = (
    "ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/"
    "paddleocr-vl:latest-nvidia-gpu"
)

# ---------------------------------------------------------------------------
# GPU detection (cached at module level)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEMO_DIR = _SKILL_DIR / "demo"


def _detect_gpu_arch() -> dict:
    """Return {arch, image, compute_cap} by querying nvidia-smi."""
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,compute_cap", "--format=csv,noheader"],
            text=True, timeout=10,
        ).strip()
    except Exception:
        return {"arch": "unknown", "image": STANDARD_IMAGE, "compute_cap": "unknown"}

    caps = []
    for line in out.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 2:
            try:
                caps.append(float(parts[1]))
            except ValueError:
                continue

    if not caps:
        return {"arch": "unknown", "image": STANDARD_IMAGE, "compute_cap": "unknown"}

    max_cap = max(caps)
    is_blackwell = max_cap >= 12.0
    return {
        "arch": "blackwell" if is_blackwell else "standard",
        "image": BLACKWELL_IMAGE if is_blackwell else STANDARD_IMAGE,
        "compute_cap": max_cap,
    }


_GPU = _detect_gpu_arch()


def _docker_image_present(image: str) -> bool:
    """Check whether the Docker image exists locally."""
    try:
        subprocess.check_output(
            ["docker", "image", "inspect", image],
            text=True, stderr=subprocess.DEVNULL, timeout=10,
        )
        return True
    except subprocess.CalledProcessError:
        return False


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

server = Server("paddle-ocr-vl")


# ---------------------------------------------------------------------------
# Inline Python that runs *inside* the container
# ---------------------------------------------------------------------------

_INLINE_PREAMBLE = (
    "import os\n"
    "os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK'] = 'True'\n"
    "from paddlex import create_pipeline\n"
)

_INLINE_BODY = """
pipeline = create_pipeline(pipeline='PaddleOCR-VL')
output = pipeline.predict(input='{container_img_path}')
result_list = []
for res in output:
    if hasattr(res, 'str'):
        result_list.append(res.str())
    else:
        result_list.append(str(res))
print('---SKILL_OUTPUT_START---')
print('\\n'.join(result_list))
print('---SKILL_OUTPUT_END---')
"""


def _build_inline_script(container_img_path: str) -> str:
    return _INLINE_PREAMBLE + _INLINE_BODY.format(container_img_path=container_img_path)


def _run_container(image: str, host_image_path: str, timeout: int = 300) -> dict:
    """Run OCR inside an ephemeral Docker container."""
    apath = Path(host_image_path).resolve()
    if not apath.exists():
        return {"status": "error", "message": f"file not found: {host_image_path}"}

    host_dir = str(apath.parent)
    container_img = f"/data/{apath.name}"
    script = _build_inline_script(container_img)

    cmd = [
        "docker", "run", "--rm", "--gpus", "all", "--network", "host",
        "--user", "root",
        "-v", f"{host_dir}:/data",
        image,
        "python3", "-c", script,
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": f"timeout after {timeout}s"}

    if "---SKILL_OUTPUT_START---" in output:
        body = output.split("---SKILL_OUTPUT_START---")[1].split("---SKILL_OUTPUT_END---")[0].strip()
        return {"status": "success", "result": body}
    elif "---SKILL_ERROR---" in output:
        err = output.split("---SKILL_ERROR---:")[1].strip()
        return {"status": "error", "message": f"pipeline error: {err}"}
    else:
        return {"status": "error", "message": "unexpected output", "raw": output[-2000:]}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="run_ocr",
            description=(
                "对图片运行 PaddleOCR-VL 进行 OCR 识别。"
                "支持中英文文档、表格、图表、印章等。"
                "自动检测 GPU 架构并使用对应的 NVIDIA Docker 镜像。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "图片的绝对路径。",
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="check_environment",
            description=(
                "检查 PaddleOCR-VL 运行环境是否就绪。"
                "包括 Docker 可用性、GPU 驱动、镜像是否已拉取等。"
                "首次使用前请先运行此工具获取配置指引。"
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="run_demo",
            description=(
                "运行内置 Demo 图片的 OCR 识别，用于验证环境配置是否正确。"
                "包含两张测试图片：中文报纸版面 + 古汉语竖排文献。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "demo_name": {
                        "type": "string",
                        "description": "Demo 名称: 'newspaper'（中文报纸）或 'classical'（古汉语竖排）或 'all'（全部）。",
                        "enum": ["newspaper", "classical", "all"],
                    },
                },
                "required": ["demo_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "run_ocr":
        return await _handle_run_ocr(arguments)
    elif name == "check_environment":
        return await _handle_check_environment()
    elif name == "run_demo":
        return await _handle_run_demo(arguments)
    else:
        return [TextContent(type="text", text=f"unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def _handle_run_ocr(args: dict) -> list[TextContent]:
    image_path = args.get("image_path", "")
    if not image_path:
        return [TextContent(type="text", text="错误: 请提供 image_path 参数")]

    image = _GPU["image"]
    if not _docker_image_present(image):
        return [TextContent(type="text", text=_setup_guide(image))]

    result = await asyncio.to_thread(_run_container, image, image_path)
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def _handle_check_environment() -> list[TextContent]:
    lines = ["## PaddleOCR-VL 环境检查\n"]

    # 1. Docker
    try:
        ver = subprocess.check_output(["docker", "--version"], text=True, timeout=5).strip()
        lines.append(f"- Docker: 已安装 ({ver})")
    except Exception:
        lines.append("- Docker: **未安装** — 请先安装 Docker 和 nvidia-container-toolkit")
        return [TextContent(type="text", text="\n".join(lines))]

    # 2. GPU
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,compute_cap,driver_version", "--format=csv,noheader"],
            text=True, timeout=10,
        ).strip()
        lines.append(f"- GPU:\n```\n{out}\n```")
    except Exception:
        lines.append("- GPU: **无法检测** — 请确认 NVIDIA 驱动已安装")

    # 3. Architecture
    lines.append(f"- 检测到的架构: **{_GPU['arch']}** (compute cap {_GPU['compute_cap']})")
    lines.append(f"- 对应镜像: `{_GPU['image']}`")

    # 4. Image
    image = _GPU["image"]
    if _docker_image_present(image):
        lines.append("- Docker 镜像: 已拉取")
    else:
        lines.append("- Docker 镜像: **未拉取**")
        lines.append("")
        lines.append(_setup_guide(image))
        return [TextContent(type="text", text="\n".join(lines))]

    # 5. Demo images
    demos = list(_DEMO_DIR.glob("*.png"))
    if demos:
        lines.append(f"- Demo 图片: {len(demos)} 张就绪 ({', '.join(d.name for d in demos)})")
    else:
        lines.append("- Demo 图片: 未找到")

    lines.append("\n环境就绪，可以调用 run_ocr 或 run_demo 开始识别。")
    return [TextContent(type="text", text="\n".join(lines))]


async def _handle_run_demo(args: dict) -> list[TextContent]:
    image = _GPU["image"]
    if not _docker_image_present(image):
        return [TextContent(type="text", text=_setup_guide(image))]

    demo_map = {
        "newspaper": ("newspaper.png", "中文报纸版面"),
        "classical": ("classical_text.png", "古汉语竖排文献"),
    }
    name = args.get("demo_name", "all")

    if name == "all":
        results = {}
        for key, (fname, desc) in demo_map.items():
            fpath = _DEMO_DIR / fname
            if fpath.exists():
                results[key] = await asyncio.to_thread(_run_container, image, str(fpath))
            else:
                results[key] = {"status": "error", "message": f"demo image missing: {fname}"}
        return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False, indent=2))]

    if name not in demo_map:
        return [TextContent(type="text", text=f"unknown demo: {name}. options: {list(demo_map.keys())}, all")]

    fname, desc = demo_map[name]
    fpath = _DEMO_DIR / fname
    if not fpath.exists():
        return [TextContent(type="text", text=f"demo image missing: {fname}")]

    result = await asyncio.to_thread(_run_container, image, str(fpath))
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


# ---------------------------------------------------------------------------
# Setup guide (printed when image is missing)
# ---------------------------------------------------------------------------

def _setup_guide(image: str) -> str:
    """Return first-run setup instructions in Chinese."""
    return f"""## 首次配置 PaddleOCR-VL

检测到 GPU 架构: **{_GPU['arch']}** (compute capability {_GPU['compute_cap']})

### 第 1 步: 拉取 Docker 镜像

```bash
docker pull {image}
```

### 第 2 步: 验证容器可以启动

```bash
docker run --rm --gpus all --network host --user root {image} \\
    python3 -c "from paddlex import create_pipeline; print('OK')"
```

### 第 3 步: 验证 Demo 图片识别

镜像拉取完成后，调用 run_demo 工具:
- `run_demo` (demo_name='newspaper') — 中文报纸版面
- `run_demo` (demo_name='classical') — 古汉语竖排文献

### 架构说明

- **Blackwell GPU** → `paddleocr-vl:latest-nvidia-gpu-sm120` (SM120)
- **其他 NVIDIA GPU** → `paddleocr-vl:latest-nvidia-gpu`

官方文档: https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html
"""


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

async def main():
    # Print startup banner to stderr (visible in Claude Desktop logs)
    print(f"[paddle-ocr-vl] GPU arch: {_GPU['arch']} | image: {_GPU['image']}", file=sys.stderr)
    if not _docker_image_present(_GPU["image"]):
        print(f"[paddle-ocr-vl] WARNING: Docker image not found. Run check_environment for setup guide.", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
