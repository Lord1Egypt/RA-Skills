#!/usr/bin/env python3
"""
huo15-img-test — 提示词直出图片 v2.2

把 enhance_prompt.py 生成的提示词，直接调用本地或云端 API 出图。

支持的后端：
  - comfyui     本地 ComfyUI（HTTP API，默认 http://127.0.0.1:8188）
  - sd-webui    AUTOMATIC1111 / Forge（默认 http://127.0.0.1:7860/sdapi/v1/txt2img）
  - dalle       OpenAI DALL-E 3（OPENAI_API_KEY）
  - openai      同 dalle
  - none        只生成调用脚本，不真实执行（dry-run，方便贴到 ComfyUI 桌面端）

依赖：仅 Python 标准库（urllib），不引入 requests/PIL，避免企业扫描器命中第三方包。

调用：
  render_prompt.py "赛博朋克猫" -p 赛博朋克 -m SD --backend sd-webui
  render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
  render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl-base.json
  render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j > recipe.json   # dry-run

环境变量：
  OPENAI_API_KEY        DALL-E 调用必需
  COMFYUI_URL           覆盖 ComfyUI 端点（默认 http://127.0.0.1:8188）
  SDWEBUI_URL           覆盖 SD WebUI 端点（默认 http://127.0.0.1:7860）
"""

import sys
import os
import json
import time
import base64
import argparse
import uuid
from typing import Dict, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt,
    parse_mix_preset,
    resolve_preset,
    parse_requirement,
    STYLE_PRESETS,
    ASPECT_TO_SDXL,
)

VERSION = "2.3.0"


# ─────────────────────────────────────────────────────────
# HTTP 工具
# ─────────────────────────────────────────────────────────
def http_post_json(url: str, body: Dict, headers: Optional[Dict] = None, timeout: int = 600) -> Dict:
    data = json.dumps(body).encode("utf-8")
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    req = Request(url, data=data, headers=h, method="POST")
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_json(url: str, headers: Optional[Dict] = None, timeout: int = 60) -> Dict:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_bytes(url: str, headers: Optional[Dict] = None, timeout: int = 600) -> bytes:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as r:
        return r.read()


# ─────────────────────────────────────────────────────────
# DALL-E 3
# ─────────────────────────────────────────────────────────
DALLE_SIZES = {"1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792"}


def render_dalle(positive: str, size: str, output_dir: str, n: int = 1) -> Dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 OPENAI_API_KEY 环境变量")
    body = {
        "model": "dall-e-3",
        "prompt": positive[:4000],
        "n": n,
        "size": size,
        "quality": "hd",
        "response_format": "b64_json",
    }
    resp = http_post_json(
        "https://api.openai.com/v1/images/generations",
        body,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=300,
    )
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, item in enumerate(resp.get("data", [])):
        path = os.path.join(output_dir, f"dalle-{int(time.time())}-{i}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
        saved.append(path)
    return {"backend": "dalle", "saved": saved, "raw_response_keys": list(resp.keys())}


# ─────────────────────────────────────────────────────────
# AUTOMATIC1111 / Forge SD WebUI
# ─────────────────────────────────────────────────────────
def aspect_to_size(aspect: str) -> tuple:
    sdxl = ASPECT_TO_SDXL.get(aspect, "1024x1024")
    w, h = sdxl.split("x")
    return int(w), int(h)


def render_sdwebui(positive: str, negative: str, aspect: str, seed: int, steps: int, cfg: float,
                   sampler: str, output_dir: str, base_url: Optional[str] = None) -> Dict:
    base = base_url or os.environ.get("SDWEBUI_URL", "http://127.0.0.1:7860")
    w, h = aspect_to_size(aspect)
    body = {
        "prompt": positive,
        "negative_prompt": negative,
        "width": w,
        "height": h,
        "seed": seed,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": sampler,
        "send_images": True,
    }
    resp = http_post_json(urljoin(base, "/sdapi/v1/txt2img"), body, timeout=900)
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, b64 in enumerate(resp.get("images", [])):
        path = os.path.join(output_dir, f"sdwebui-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64.split(",", 1)[-1]))
        saved.append(path)
    return {"backend": "sd-webui", "saved": saved, "info": resp.get("info", "")[:200]}


# ─────────────────────────────────────────────────────────
# ComfyUI
# ─────────────────────────────────────────────────────────
DEFAULT_COMFY_WORKFLOW = {
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 0, "steps": 25, "cfg": 7.0, "sampler_name": "dpmpp_2m",
            "scheduler": "karras", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0],
        },
    },
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "POSITIVE_PLACEHOLDER", "clip": ["4", 1]}},
    "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "NEGATIVE_PLACEHOLDER", "clip": ["4", 1]}},
    "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
    "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": "huo15"}},
}


def render_comfyui(positive: str, negative: str, aspect: str, seed: int, steps: int, cfg: float,
                   workflow_path: Optional[str], output_dir: str,
                   base_url: Optional[str] = None) -> Dict:
    base = base_url or os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")

    if workflow_path and os.path.isfile(workflow_path):
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)
    else:
        workflow = json.loads(json.dumps(DEFAULT_COMFY_WORKFLOW))

    w, h = aspect_to_size(aspect)
    for node in workflow.values():
        ct = node.get("class_type", "")
        ins = node.get("inputs", {})
        if ct == "CLIPTextEncode":
            if ins.get("text") == "POSITIVE_PLACEHOLDER" or "positive" in str(ins.get("text", "")).lower():
                ins["text"] = positive
            elif ins.get("text") == "NEGATIVE_PLACEHOLDER" or "negative" in str(ins.get("text", "")).lower():
                ins["text"] = negative
        elif ct == "EmptyLatentImage":
            ins["width"], ins["height"] = w, h
        elif ct == "KSampler":
            ins["seed"], ins["steps"], ins["cfg"] = seed, steps, cfg

    pos_set = neg_set = False
    for node in workflow.values():
        if node.get("class_type") == "CLIPTextEncode":
            if not pos_set:
                node["inputs"]["text"] = positive
                pos_set = True
            elif not neg_set:
                node["inputs"]["text"] = negative
                neg_set = True

    client_id = str(uuid.uuid4())
    queue_resp = http_post_json(urljoin(base, "/prompt"), {"prompt": workflow, "client_id": client_id}, timeout=30)
    prompt_id = queue_resp.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI 队列失败: {queue_resp}")

    deadline = time.time() + 600
    history = {}
    while time.time() < deadline:
        try:
            history = http_get_json(urljoin(base, f"/history/{prompt_id}"), timeout=10)
            if history.get(prompt_id):
                break
        except (HTTPError, URLError):
            pass
        time.sleep(2)

    if not history.get(prompt_id):
        raise RuntimeError("ComfyUI 任务超时")

    saved = []
    os.makedirs(output_dir, exist_ok=True)
    outputs = history[prompt_id].get("outputs", {})
    for node_id, output in outputs.items():
        for img in output.get("images", []):
            url = urljoin(base, f"/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img.get('type','output')}")
            path = os.path.join(output_dir, f"comfy-{seed}-{img['filename']}")
            with open(path, "wb") as f:
                f.write(http_get_bytes(url))
            saved.append(path)

    return {"backend": "comfyui", "saved": saved, "prompt_id": prompt_id}


# ─────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test render_prompt v{VERSION} — 提示词直出图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  render_prompt.py "赛博朋克猫" -p 赛博朋克 --backend sd-webui
  render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl.json
  render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
  render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j   # dry-run，只输出 recipe
""",
    )
    parser.add_argument("subject", help="主体描述")
    parser.add_argument("-p", "--preset", help="风格预设（支持 A+B 混合）")
    parser.add_argument("--mix", type=float, default=0.6, help="混合权重（默认 0.6）")
    parser.add_argument("-a", "--aspect", default="", help="画幅")
    parser.add_argument("-t", "--tier", choices=["basic", "pro", "master"], default="pro")
    parser.add_argument("--avoid", default="", help="额外负面词")
    parser.add_argument("--seed", type=int, help="种子")
    parser.add_argument(
        "--backend", choices=["comfyui", "sd-webui", "dalle", "openai", "none"], default="none",
        help="后端：comfyui / sd-webui / dalle / none(dry-run)",
    )
    parser.add_argument("-m", "--model", default="SDXL", help="提示词模型适配（不影响后端选择）")
    parser.add_argument("--output", default="./renders", help="输出目录（默认 ./renders）")
    parser.add_argument("--workflow", default="", help="ComfyUI workflow JSON 路径（可选）")
    parser.add_argument("--steps", type=int, default=25, help="采样步数")
    parser.add_argument("--cfg", type=float, default=7.0, help="CFG scale")
    parser.add_argument("--sampler", default="DPM++ 2M Karras", help="采样器")
    parser.add_argument("--size", default="", help="DALL-E 尺寸 1024x1024 / 1792x1024 / 1024x1792")
    parser.add_argument("--n", type=int, default=1, help="生成张数（DALL-E）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    raw_preset = args.preset or "写实摄影"
    primary_raw, secondary_raw = parse_mix_preset(raw_preset)
    if secondary_raw:
        primary_resolved = resolve_preset(primary_raw)
        secondary_resolved = resolve_preset(secondary_raw)
        if not primary_resolved or not secondary_resolved:
            print(f"❌ 未知预设：{primary_raw} 或 {secondary_raw}", file=sys.stderr)
            sys.exit(1)
        preset, mix_secondary = primary_resolved, secondary_resolved
    else:
        preset, mix_secondary = primary_raw, None

    auto = parse_requirement(args.subject)
    aspect = args.aspect or auto["aspect_suggestion"] or STYLE_PRESETS.get(resolve_preset(preset) or "写实摄影", {}).get("aspect", "1:1")

    recipe = build_prompt(
        args.subject, preset, args.model, aspect,
        extra_negatives=args.avoid, seed=args.seed, quality_tier=args.tier,
        mix_secondary=mix_secondary, mix_ratio=args.mix,
    )
    seed = recipe["seed_suggestion"]

    if args.backend == "none":
        out = {"version": VERSION, "backend": "none", "recipe": recipe, "note": "dry-run，未实际调用模型"}
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"🧪 dry-run（未出图）")
            print(f"  positive: {recipe['positive'][:200]}...")
            print(f"  seed:     {seed}")
            print(f"  → 用 -j 输出完整 recipe，再 pipe 给 ComfyUI / DALL-E / SD WebUI")
        return

    try:
        if args.backend == "sd-webui":
            result = render_sdwebui(
                recipe["positive"], recipe["negative"], aspect, seed,
                args.steps, args.cfg, args.sampler, args.output,
            )
        elif args.backend == "comfyui":
            result = render_comfyui(
                recipe["positive"], recipe["negative"], aspect, seed,
                args.steps, args.cfg, args.workflow or None, args.output,
            )
        elif args.backend in ("dalle", "openai"):
            size = args.size or DALLE_SIZES.get(aspect, "1024x1024")
            result = render_dalle(recipe["positive"], size, args.output, n=args.n)
        else:
            raise RuntimeError(f"未知 backend: {args.backend}")
    except Exception as e:
        print(f"❌ 渲染失败: {e}", file=sys.stderr)
        sys.exit(2)

    out = {"version": VERSION, "recipe": recipe, "render": result}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 已出图（backend={result['backend']}）")
        for p in result.get("saved", []):
            print(f"   📷 {p}")
        print(f"   🎲 seed = {seed}")


if __name__ == "__main__":
    main()
