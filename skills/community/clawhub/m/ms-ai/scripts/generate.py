#!/usr/bin/env python3
"""
ModelScope 生图脚本 — 支持文生图 & 图生图，Key + 模型双重轮换
用法:
  文生图: python3 generate.py --prompt "描述文字" --output result.jpg
  图生图: python3 generate.py --prompt "修改描述" --image input.jpg --output result.jpg --model edit
  指定宽高比: python3 generate.py --prompt "PPT封面" --aspect 16:9 --output slide.png
  竖屏视频: python3 generate.py --prompt "短视频" --aspect 9:16 --output video.png
  指定尺寸: python3 generate.py --prompt "风景画" --width 1920 --height 1080 --output landscape.jpg
"""

import argparse
import base64
import json
import os
import sys
import time

import requests
from PIL import Image
from io import BytesIO

from common import load_api_keys, make_headers, try_with_key_rotation

# ============ 配置 ============
BASE_URL = "https://api-inference.modelscope.cn/"
POLL_INTERVAL = 5
MAX_WAIT = 300

# 宽高比预设 — 常见场景一键选择
ASPECT_PRESETS = {
    # 比例         宽     高     适用场景
    "16:9":    (1920, 1080),  # PPT、视频横屏、演示文稿、文章封面
    "9:16":    (1080, 1920),  # 短视频竖屏、手机海报、Stories
    "1:1":     (1024, 1024),  # 社交媒体、头像、方图
    "4:3":     (1536, 1152),  # 传统演示、iPad 横屏
    "3:4":     (1152, 1536),  # 竖版海报、A4 文档
    "21:9":    (2560, 1080),  # 超宽屏、电影画幅
    "3:2":     (1800, 1200),  # 摄影标准、印刷
    "2:3":     (1200, 1800),  # 竖版印刷、书籍封面
}

# 场景→预设速查（agent 可直接传场景名）
SCENE_PRESETS = {
    "ppt":         "16:9",
    "slide":       "16:9",
    "video-h":     "16:9",   # 横屏视频
    "video-v":     "9:16",   # 竖屏视频
    "douyin":      "9:16",   # 抖音
    "reels":       "9:16",
    "poster":      "2:3",    # 竖版海报
    "cover":       "16:9",   # 文章/视频封面
    "weixin":      "16:9",   # 微信公众号封面
    "social":      "1:1",    # 社交媒体
    "avatar":      "1:1",
    "print-a4":    "3:4",    # A4 竖版
    "cinema":      "21:9",   # 电影画幅
    "photo":       "3:2",    # 摄影
}

# 文生图模型（按优先级排列）
MODELS_TEXT_TO_IMAGE = [
    "FireRedTeam/FireRed-Image-Edit-1.1",
    "Qwen/Qwen-Image-2512",
    "Qwen/Qwen-Image-Edit-2511",
    "Tongyi-MAI/Z-Image-Turbo",
]

# 图生图模型（按优先级排列）
MODELS_IMAGE_TO_IMAGE = [
    "FireRedTeam/FireRed-Image-Edit-1.1",
    "Qwen/Qwen-Image-Edit-2511",
]

# 别名映射
ALIASES = {
    "turbo":     "Tongyi-MAI/Z-Image-Turbo",
    "z-image":   "Tongyi-MAI/Z-Image-Turbo",
    "qwen":      "Qwen/Qwen-Image-2512",
    "edit":      "Qwen/Qwen-Image-Edit-2511",
    "qwen-edit": "Qwen/Qwen-Image-Edit-2511",
    "firered":   "FireRedTeam/FireRed-Image-Edit-1.1",
}


def encode_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "gif": "image/gif"}.get(ext.lstrip("."), "image/jpeg")
    return f"data:{mime};base64,{data}"


def resolve_image_urls(images) -> list:
    urls = []
    for img in images:
        if img.startswith(("http://", "https://", "data:")):
            urls.append(img)
        elif os.path.isfile(img):
            urls.append(encode_image_base64(img))
        else:
            print(f"❌ 图片不存在: {img}", file=sys.stderr)
            sys.exit(1)
    return urls


def submit_task(api_key: str, prompt: str, model: str, width: int = 1024, height: int = 1024,
                loras=None, image_urls=None) -> str:
    headers = make_headers(api_key)
    payload = {"model": model, "prompt": prompt}
    if image_urls:
        payload["image_url"] = image_urls if len(image_urls) > 1 else image_urls[0]
    if loras:
        payload["loras"] = loras[0] if len(loras) == 1 else loras

    resp = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers={**headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "task_id" not in data:
        raise Exception(f"提交失败: {json.dumps(data, ensure_ascii=False)}")
    return data["task_id"]


def poll_task(api_key: str, task_id: str) -> dict:
    headers = make_headers(api_key)
    elapsed = 0
    while elapsed < MAX_WAIT:
        resp = requests.get(
            f"{BASE_URL}v1/tasks/{task_id}",
            headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("task_status", "")
        if status == "SUCCEED":
            return data
        elif status == "FAILED":
            raise Exception(f"生成失败: {data.get('error_message', '未知错误')}")
        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
    raise Exception(f"超时（超过 {MAX_WAIT} 秒）")


def download_image(url: str, output_path: str) -> str:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    img = Image.open(BytesIO(resp.content))
    img.save(output_path)
    return output_path


def _generate_one(api_key: str, model: str, prompt: str, output_path: str,
                  width: int, height: int, image_urls, loras) -> dict:
    """尝试用指定 key + model 生成，返回统一格式"""
    try:
        task_id = submit_task(api_key, prompt, model, width, height, loras, image_urls)
        print(f"    📋 任务 ID: {task_id}", file=sys.stderr)
        print(f"    ⏳ 等待生成中...", file=sys.stderr)
        result = poll_task(api_key, task_id)
        output_url = result["output_images"][0]
        saved_path = download_image(output_url, output_path)
        return {
            "status": "success",
            "mode": "image_edit" if image_urls else "text_to_image",
            "file": saved_path,
            "task_id": task_id,
            "prompt": prompt,
            "model": model,
        }
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            return {"status": "rate_limit"}
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="ModelScope 生图 — 支持文生图 & 图生图，Key + 模型双重轮换",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt", required=True, help="描述文字")
    parser.add_argument("--output", default="output.jpg", help="输出文件路径")
    parser.add_argument("--model", default=None, help="指定模型（别名或完整ID）")
    parser.add_argument("--image", action="append", dest="images", default=None, help="输入图片路径（图生图）")
    parser.add_argument("--aspect", default=None,
                        help="宽高比预设，如 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 3:2, 2:3；"
                             "也支持场景名: ppt, video-h, video-v, douyin, poster, cover, social 等")
    parser.add_argument("--width", type=int, default=None, help="图片宽度（默认1920，可用 --aspect 覆盖）")
    parser.add_argument("--height", type=int, default=None, help="图片高度（默认1080，可用 --aspect 覆盖）")
    parser.add_argument("--lora", action="append", dest="loras", help="LoRA 模型 ID")
    args = parser.parse_args()

    # 解析尺寸：--aspect > --width/--height > 默认 1920x1080
    if args.aspect:
        # 先查场景名映射
        aspect_key = SCENE_PRESETS.get(args.aspect.lower(), args.aspect.lower())
        if aspect_key in ASPECT_PRESETS:
            args.width, args.height = ASPECT_PRESETS[aspect_key]
            print(f"📐 预设: {args.aspect} → {args.width}x{args.height}", file=sys.stderr)
        else:
            valid = ", ".join(list(ASPECT_PRESETS.keys()) + list(SCENE_PRESETS.keys()))
            print(f"❌ 未知预设: {args.aspect}\n   可用: {valid}", file=sys.stderr)
            sys.exit(1)
    else:
        # 没指定 --aspect 时，用 --width/--height，未指定则默认 1920x1080
        if args.width is None:
            args.width = 1920
        if args.height is None:
            args.height = 1080

    keys = load_api_keys()
    is_edit = args.images is not None
    image_urls = resolve_image_urls(args.images) if is_edit else None
    default_list = MODELS_IMAGE_TO_IMAGE if is_edit else MODELS_TEXT_TO_IMAGE

    if args.model:
        specified = ALIASES.get(args.model, args.model)
        model_list = [specified] + [m for m in default_list if m != specified]
        print(f"📌 指定模型: {specified}（失败时自动轮换）", file=sys.stderr)
    else:
        model_list = default_list

    mode = "🖼️ 图生图" if is_edit else "🎨 文生图"
    print(f"\n{mode}: {args.prompt}", file=sys.stderr)
    print(f"📐 尺寸: {args.width}x{args.height}", file=sys.stderr)
    print(f"🔑 API Keys: {len(keys)} 个", file=sys.stderr)
    print(f"🤖 模型: {len(model_list)} 个", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    try:
        result = try_with_key_rotation(
            _generate_one, model_list, keys,
            args.prompt, args.output, args.width, args.height, image_urls, args.loras,
        )
        print(f"\n{'='*50}", file=sys.stderr)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
