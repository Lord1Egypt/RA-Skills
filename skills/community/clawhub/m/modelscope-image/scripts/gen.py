#!/usr/bin/env python3
"""
魔搭社区图片生成脚本
支持通过 ModelScope API 调用各种文生图模型生成图片

模型列表存储在 references/models.md 中，方便维护和扩展。
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html import escape as html_escape
from pathlib import Path


def _get_models_file_path() -> Path:
    """获取模型列表文件路径"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    # models.md 在 references/ 目录下
    return script_dir.parent / "references" / "models.md"


def get_available_models() -> dict[str, dict]:
    """获取可用的文生图模型列表

    从 references/models.md 读取模型配置。
    如果文件不存在，返回内置的默认模型列表。
    """
    models_file = _get_models_file_path()

    if not models_file.exists():
        # 内置默认模型列表（作为备用）
        return {
            "kolors": {
                "id": "Kwai-Kolors/Kolors",
                "name": "快手可图",
                "description": "快手可图，支持中英文，高质量生成（默认）",
                "language": ["zh", "en"],
                "recommended": True,
            },
            "sd-x1": {
                "id": "AI-ModelScope/stable-diffusion-xl-base-1.0",
                "name": "Stable Diffusion XL 1.0",
                "description": "SDXL 基础模型，高质量艺术创作",
                "language": ["en"],
                "recommended": True,
            },
            "sd-turbo": {
                "id": "AI-ModelScope/sdxl-turbo",
                "name": "SDXL Turbo",
                "description": "SDXL Turbo，快速生成",
                "language": ["en"],
                "recommended": True,
            },
            "flux-schnell": {
                "id": "black-forest-labs/FLUX.1-schnell",
                "name": "FLUX.1 schnell",
                "description": "FLUX.1 schnell，高质量快速生成",
                "language": ["en"],
                "recommended": True,
            },
            "qwen-image": {
                "id": "Qwen/Qwen-Image",
                "name": "Qwen-Image（小橙鱼）",
                "description": "通义千问图像模型，下载量 2.3M",
                "language": ["zh", "en"],
                "recommended": True,
            },
        }

    # 解析 models.md 文件
    models = {}
    current_section = None

    with open(models_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # 跳过空行和标题行
            if not line or line.startswith("#") or line.startswith(">"):
                continue

            # 匹配表格行：| `alias` | model-id | name | description | language |
            if line.startswith("|") and "`" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5:
                    alias_raw = parts[1]
                    model_id = parts[2]
                    name = parts[3]
                    desc = parts[4]
                    lang_raw = parts[5] if len(parts) > 5 else "en"

                    # 提取 alias（去掉反引号）
                    alias_match = re.search(r"`([^`]+)`", alias_raw)
                    if not alias_match:
                        continue
                    alias = alias_match.group(1)

                    # 解析语言列表
                    languages = [l.strip() for l in lang_raw.split(",")]

                    # 判断是否为推荐模型
                    recommended = (
                        "推荐模型（核心）" in current_section or
                        "通用高质量模型" in current_section
                    ) if current_section else alias in [
                        "kolors", "qwen-image", "qwen-image-2512",
                        "z-image-turbo", "z-image", "sd-x1", "sd-turbo",
                        "flux-schnell", "flux-dev", "majicflus"
                    ]

                    models[alias] = {
                        "id": model_id,
                        "name": name,
                        "description": desc,
                        "language": languages,
                        "recommended": recommended,
                    }

            # 检测章节标题
            elif line.startswith("## "):
                current_section = line[3:].strip()

    return models


def slugify(text: str) -> str:
    """将文本转换为文件名友好的格式"""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:50] or "image"


def default_out_dir() -> Path:
    """生成默认输出目录"""
    now = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    preferred = Path.home() / "Projects" / "tmp"
    base = preferred if preferred.is_dir() else Path("./tmp")
    base.mkdir(parents=True, exist_ok=True)
    return base / f"modelscope-image-gen-{now}"


def list_available_models() -> None:
    """打印可用的文生图模型列表"""
    print("魔搭社区支持 API 推理的文生图模型")
    print("=" * 80)
    print(f"模型列表来源: {_get_models_file_path()}")
    print("=" * 80)

    models = get_available_models()

    # 显示推荐模型
    print("\n【推荐模型】")
    for alias, info in models.items():
        if info.get("recommended", False):
            lang = ", ".join(info.get("language", []))
            print(f"\n  {alias:15s}")
            print(f"  {'─' * 60}")
            print(f"  ID:    {info['id']}")
            print(f"  名称:  {info['name']}")
            print(f"  说明:  {info['description']}")
            print(f"  语言:  {lang}")

    # 显示其他模型（完整信息）
    print("\n\n【其他模型】")
    for alias, info in models.items():
        if not info.get("recommended", False):
            lang = ", ".join(info.get("language", []))
            print(f"\n  {alias:15s}")
            print(f"  {'─' * 60}")
            print(f"  ID:    {info['id']}")
            print(f"  名称:  {info['name']}")
            print(f"  说明:  {info['description']}")
            print(f"  语言:  {lang}")

    print("\n" + "=" * 80)
    print(f"\n总计 {len(models)} 个模型")
    print("\n提示:")
    print("  - 使用简称（如 kolors）或完整模型 ID 调用")
    print("  - 只有标记为 inference_type 的模型才能通过 API 调用")
    print("  - 在线查看更多模型: https://modelscope.cn/models?filter=inference_type&tasks=text-to-image-synthesis")
    print()


def resolve_model(model_name: str) -> str:
    """解析模型名称，返回完整的模型 ID"""
    models = get_available_models()

    # 如果是简称，转换为完整 ID
    if model_name in models:
        return models[model_name]["id"]

    # 否则假设是完整的模型 ID
    return model_name


def poll_task_result(api_key: str, task_id: str, max_retries: int = 60) -> dict:
    """轮询异步任务状态直到完成
    
    Args:
        api_key: API Key
        task_id: 任务 ID
        max_retries: 最大轮询次数（每次等待 5 秒）
    
    Returns:
        包含图片数据的响应
    """
    import time
    
    url = f"https://api-inference.modelscope.cn/v1/tasks/{task_id}"
    
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-ModelScope-Task-Type": "image_generation",
            },
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                
                task_status = result.get("task_status", "")
                
                if task_status == "SUCCEED":
                    # 任务成功，返回结果
                    return result
                elif task_status == "FAILED":
                    raise RuntimeError(f"任务失败: {result}")
                elif task_status in ["PENDING", "RUNNING", "PROCESSING"]:
                    # 任务进行中，等待后重试
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                    else:
                        raise RuntimeError("任务超时")
                else:
                    raise RuntimeError(f"未知任务状态: {task_status}")
                    
        except urllib.error.HTTPError as e:
            payload = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"查询任务状态失败 ({e.code}): {payload}") from e
    
    raise RuntimeError("任务轮询超时")


def request_images(
    api_key: str,
    prompt: str,
    model: str,
    size: str = "1024x1024",
    n: int = 1,
) -> dict:
    """调用魔搭社区 API 生成图片

    API 文档：https://modelscope.cn/docs/model-service/API-Inference/intro
    兼容 OpenAI API 格式，使用异步模式
    """
    # API 端点（根据官方文档）
    url = "https://api-inference.modelscope.cn/v1/images/generations"

    args = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size,
    }

    body = json.dumps(args, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-ModelScope-Async-Mode": "true",
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            response = json.loads(resp.read().decode("utf-8"))
            
            # 检查是否为异步任务
            task_id = response.get("task_id")
            if task_id:
                # 异步模式，轮询获取结果
                print(f"  任务已提交，ID: {task_id}，等待完成...")
                return poll_task_result(api_key, task_id)
            else:
                # 同步模式，直接返回
                return response
                
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ModelScope API 调用失败 ({e.code}): {payload}") from e


def write_gallery(out_dir: Path, items: list[dict]) -> None:
    """生成 HTML 图片库"""
    thumbs = "\n".join(
        [
            f"""
<figure>
  <a href="{html_escape(it['file'], quote=True)}"><img src="{html_escape(it['file'], quote=True)}" loading="lazy" /></a>
  <figcaption>{html_escape(it['prompt'])}</figcaption>
</figure>
""".strip()
            for it in items
        ]
    )

    html = f"""<!doctype html>
<meta charset="utf-8" />
<title>modelscope-image-gen</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 24px; font: 14px/1.4 ui-sans-serif, system-ui; background: #0b0f14; color: #e8edf2; }}
  h1 {{ font-size: 18px; margin: 0 0 16px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }}
  figure {{ margin: 0; padding: 12px; border: 1px solid #1e2a36; border-radius: 14px; background: #0f1620; }}
  img {{ width: 100%; height: auto; border-radius: 10px; display: block; }}
  figcaption {{ margin-top: 10px; color: #b7c2cc; font-size: 12px; line-height: 1.4; }}
  code {{ color: #9cd1ff; }}
</style>
<h1>ModelScope 图片生成</h1>
<p>输出目录: <code>{html_escape(out_dir.as_posix())}</code></p>
<div class="grid">
{thumbs}
</div>
"""
    (out_dir / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="通过魔搭社区 API 生成图片。提示词应由 AI 根据用户需求生成，参考 references/prompt_guide.md",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 第一步：查看可用的模型列表
  python3 gen.py --list-models
  
  # 第二步：选择模型并使用 AI 生成的提示词
  python3 gen.py --prompt "一只优雅的橘猫，蓬松的毛发，灵动的眼神，躺在沙发上，温馨的家居环境，电影级摄影风格，自然阳光" --model kolors
  
  # 使用完整的模型 ID
  python3 gen.py --prompt "sunset over mountains, golden hour light, photorealistic" --model AI-ModelScope/stable-diffusion-xl-base-1.0
  
  # 批量生成多张图片
  python3 gen.py --prompt "cyberpunk city" --count 8 --model sd-x1

注意事项:
  - 提示词应由 AI 根据用户需求场景生成，遵循"主体-细节-背景-风格-光影"结构
  - 只有支持 inference_type 的模型才能通过 API 调用
  - 使用 --list-models 查看所有支持的模型
  - 提示词生成技巧请参考: references/prompt_guide.md
        """
    )

    ap.add_argument("--prompt", required=False, help="图片提示词（必需）。应由 AI 根据用户需求生成，遵循'主体-细节-背景-风格-光影'结构")
    ap.add_argument("--count", type=int, default=4, help="生成图片数量（默认: 4）")
    ap.add_argument(
        "--model",
        default="kolors",
        help="模型名称或 ID。简称: kolors, sd-x1, sd-turbo, flux-schnell；或完整模型 ID"
    )
    ap.add_argument("--size", default="1024x1024", help="图片尺寸，如 1024x1024（默认）")
    ap.add_argument("--out-dir", default="", help="输出目录（默认: ./tmp/modelscope-image-gen-<时间戳>）")
    ap.add_argument("--api-key", default="", help="ModelScope API Key（也可通过 MODELSCOPE_API_KEY 环境变量设置）")
    ap.add_argument("--list-models", action="store_true", help="列出所有可用的文生图模型")

    args = ap.parse_args()

    # 如果是列出模型，直接执行并返回
    if args.list_models:
        list_available_models()
        return 0

    # 生成图片必须提供提示词
    if not args.prompt:
        print("错误: 缺少 --prompt 参数", file=sys.stderr)
        print("提示词应由 AI 根据用户需求场景生成。", file=sys.stderr)
        print("生成技巧请参考: references/prompt_guide.md", file=sys.stderr)
        print("\n示例:", file=sys.stderr)
        print("  python3 gen.py --prompt '一只优雅的猫咪，蓬松的毛发，电影级风格' --model kolors", file=sys.stderr)
        return 2

    # 获取 API Key
    api_key = args.api_key or os.environ.get("MODELSCOPE_API_KEY", "").strip()
    if not api_key:
        print("错误: 缺少 MODELSCOPE_API_KEY", file=sys.stderr)
        print("请设置环境变量: export MODELSCOPE_API_KEY='your-api-key'", file=sys.stderr)
        print("或在命令行中指定: --api-key 'your-api-key'", file=sys.stderr)
        return 2

    # 解析模型
    model_id = resolve_model(args.model)
    print(f"使用模型: {model_id}")
    print(f"提示词: {args.prompt}")

    # 准备输出目录
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 准备提示词列表（用于批量生成）
    prompts = [args.prompt] * args.count

    items: list[dict] = []
    for idx, prompt in enumerate(prompts, start=1):
        print(f"[{idx}/{len(prompts)}] 生成: {prompt}")

        try:
            res = request_images(
                api_key,
                prompt,
                model_id,
                args.size,
                n=1,
            )
        except RuntimeError as e:
            print(f"错误: {e}", file=sys.stderr)
            continue

        # 解析响应
        # 异步模式返回格式：{"output_images": ["url1", "url2", ...]}
        output_images = res.get("output_images", [])
        
        # 兼容同步模式格式：{"data": [{"url": "...", "b64_json": "..."}]}
        if not output_images:
            data = res.get("data", [{}])
            if not data:
                print(f"警告: 响应中没有图片数据", file=sys.stderr)
                continue
            image_data = data[0]
            image_b64 = image_data.get("b64_json")
            image_url = image_data.get("url")
        else:
            # 异步模式，从 output_images 获取 URL
            image_url = output_images[0]
            image_b64 = None

        if not image_b64 and not image_url:
            print(f"警告: 响应格式异常: {json.dumps(res)[:200]}", file=sys.stderr)
            continue

        # 保存图片
        filename = f"{idx:03d}-{slugify(prompt)}.png"
        filepath = out_dir / filename

        if image_b64:
            filepath.write_bytes(base64.b64decode(image_b64))
        else:
            try:
                urllib.request.urlretrieve(image_url, filepath)
            except urllib.error.URLError as e:
                print(f"下载图片失败 {image_url}: {e}", file=sys.stderr)
                continue

        items.append({"prompt": prompt, "file": filename})
        print(f"  -> 已保存: {filename}")

    if items:
        # 保存提示词映射
        (out_dir / "prompts.json").write_text(
            json.dumps(items, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        # 生成图片库
        write_gallery(out_dir, items)
        print(f"\n✅ 完成！查看结果: {(out_dir / 'index.html').as_posix()}")
    else:
        print("\n❌ 没有成功生成任何图片", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
