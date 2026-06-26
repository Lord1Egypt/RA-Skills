#!/usr/bin/env python3
"""
MiMo API (clawm-alpha) 多模态调用工具 / Multimodal Tool (中文/English)

用法 / Usage:
  python mimo_api.py image   <图片URL或本地路径/image URL or local path> <问题/question> [--max-tokens N] [--timeout N]
  python mimo_api.py images  <图片1/img1> <图片2/img2> ... --question <问题/question> [--max-tokens N] [--timeout N]
  python mimo_api.py video   <视频URL或本地路径/video URL or local path> <问题/question> [--fps N] [--resolution default|max] [--max-tokens N] [--timeout N]
  python mimo_api.py audio   <音频URL或本地路径/audio URL or local path> <问题/question> [--max-tokens N] [--timeout N]
  python mimo_api.py mixed   --video <视频/video> --audio <音频/audio> <问题/question> [--fps N] [--max-tokens N] [--timeout N]

通用参数 / General parameters:
  --api-key KEY  MiMo API 密钥 / API key (also via env var MIMO_API_KEY)
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time

import requests

API_URL = os.environ.get("MIMO_API_ENDPOINT", "https://api.xiaomimimo.com/v1/chat/completions")
MODEL = os.environ.get("MIMO_OMNI_MODEL", "clawm-alpha")


_API_KEY = None


def _resolve_api_key():
    """解析 API 密钥 / Resolve API key: explicit → env var → openclaw.json"""
    if _API_KEY:
        return _API_KEY
    if os.environ.get("MIMO_API_KEY"):
        return os.environ["MIMO_API_KEY"]
    openclaw = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.isfile(openclaw):
        try:
            with open(openclaw) as f:
                return json.load(f)["models"]["providers"]["xiaomi"]["apiKey"]
        except (KeyError, TypeError, json.JSONDecodeError):
            pass
    print("错误: 未找到 MiMo API 密鑰。请设置环境变量 MIMO_API_KEY，或在 ~/.openclaw/openclaw.json 中配置 models.providers.xiaomi.apiKey", file=sys.stderr)
    sys.exit(1)


def get_headers():
    return {"Content-Type": "application/json", "api-key": _resolve_api_key()}


def to_data_uri(path):
    """本地文件 → data URI / Local file → data URI"""
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        ext = path.rsplit(".", 1)[-1].lower()
        mime = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "gif": "image/gif", "webp": "image/webp", "mp4": "video/mp4",
            "webm": "video/webm", "mov": "video/quicktime",
            "wav": "audio/wav", "mp3": "audio/mpeg", "flac": "audio/flac",
        }.get(ext, f"application/octet-stream")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def resolve_source(source):
    """URL 直接返回，本地路径转 data URI / URL → pass through, local path → data URI"""
    if source.startswith("http://") or source.startswith("https://"):
        return source
    if source.startswith("data:"):
        return source
    return to_data_uri(source)


def call_api(content, max_tokens=65536, timeout=300):
    """调用 MiMo API 并返回结果 / Call MiMo API and return result"""
    t0 = time.time()
    resp = requests.post(API_URL, headers=get_headers(), json={
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_completion_tokens": max_tokens,
    }, timeout=timeout)
    elapsed = time.time() - t0
    result = resp.json()

    if "choices" in result:
        text = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        print(f"[{elapsed:.1f}s | prompt={usage.get('prompt_tokens', '?')}, "
              f"completion={usage.get('completion_tokens', '?')}]", file=sys.stderr)
        return text
    else:
        print(f"API 错误: {json.dumps(result, ensure_ascii=False)[:500]}", file=sys.stderr)
        sys.exit(1)


# ========== 子命令 / Sub-commands ==========

def cmd_image(args):
    """单张图片分析 / Single image analysis"""
    url = resolve_source(args.source)
    content = [
        {"type": "image_url", "image_url": {"url": url}},
        {"type": "text", "text": args.question},
    ]
    print(call_api(content, args.max_tokens, args.timeout))


def cmd_images(args):
    """多张图片分析 / Multi-image analysis"""
    content = []
    for src in args.sources:
        url = resolve_source(src)
        content.append({"type": "image_url", "image_url": {"url": url}})
    content.append({"type": "text", "text": args.question})
    print(call_api(content, args.max_tokens, args.timeout))


def cmd_video(args):
    """视频分析 / Video analysis"""
    url = resolve_source(args.source)
    video_item = {
        "type": "video_url",
        "video_url": {"url": url},
        "fps": args.fps,
        "media_resolution": args.resolution,
    }
    content = [video_item, {"type": "text", "text": args.question}]
    print(call_api(content, args.max_tokens, args.timeout))


def cmd_audio(args):
    """音频分析 / Audio analysis"""
    source = args.source
    if source.startswith("http"):
        data = source
    elif source.startswith("data:"):
        data = source
    else:
        data = to_data_uri(source)
    content = [
        {"type": "input_audio", "input_audio": {"data": data}},
        {"type": "text", "text": args.question},
    ]
    print(call_api(content, args.max_tokens, args.timeout))


def cmd_mixed(args):
    """视频+音频联合分析 / Mixed video+audio analysis"""
    video_url = resolve_source(args.video)
    audio_src = args.audio
    if audio_src.startswith("http") or audio_src.startswith("data:"):
        audio_data = audio_src
    else:
        audio_data = to_data_uri(audio_src)
    content = [
        {"type": "video_url", "video_url": {"url": video_url}, "fps": args.fps},
        {"type": "input_audio", "input_audio": {"data": audio_data}},
        {"type": "text", "text": args.question},
    ]
    print(call_api(content, args.max_tokens, args.timeout))


def main():
    global _API_KEY
    parser = argparse.ArgumentParser(description="MiMo API 多模态调用工具 / Multimodal Tool")

    sub = parser.add_subparsers(dest="command", required=True)

    # image
    p = sub.add_parser("image", help="单张图片分析 / Single image analysis")
    p.add_argument("source", help="图片 URL 或本地路径 / image URL or local path")
    p.add_argument("question", help="问题 / question")
    p.add_argument("--max-tokens", type=int, default=65536)
    p.add_argument("--timeout", type=int, default=300, help="请求超时秒数 / request timeout in seconds")
    p.set_defaults(func=cmd_image)

    # images
    p = sub.add_parser("images", help="多张图片分析 / Multi-image analysis")
    p.add_argument("sources", nargs="+", help="图片 URL 或本地路径（多个）/ image URLs or local paths")
    p.add_argument("--question", required=True, help="问题 / question")
    p.add_argument("--max-tokens", type=int, default=65536)
    p.add_argument("--timeout", type=int, default=300, help="请求超时秒数 / request timeout in seconds")
    p.set_defaults(func=cmd_images)

    # video
    p = sub.add_parser("video", help="视频分析 / Video analysis")
    p.add_argument("source", help="视频 URL 或本地路径 / video URL or local path")
    p.add_argument("question", help="问题 / question")
    p.add_argument("--fps", type=float, default=1)
    p.add_argument("--resolution", choices=["default", "max"], default="default")
    p.add_argument("--max-tokens", type=int, default=65536)
    p.add_argument("--timeout", type=int, default=300, help="请求超时秒数 / request timeout in seconds")
    p.set_defaults(func=cmd_video)

    # audio
    p = sub.add_parser("audio", help="音频分析 / Audio analysis")
    p.add_argument("source", help="音频 URL 或本地路径 / audio URL or local path")
    p.add_argument("question", help="问题 / question")
    p.add_argument("--max-tokens", type=int, default=65536)
    p.add_argument("--timeout", type=int, default=300, help="请求超时秒数 / request timeout in seconds")
    p.set_defaults(func=cmd_audio)

    # mixed
    p = sub.add_parser("mixed", help="视频+音频联合分析 / Mixed video+audio analysis")
    p.add_argument("--video", required=True, help="视频 URL 或本地路径 / video URL or local path")
    p.add_argument("--audio", required=True, help="音频 URL 或本地路径 / audio URL or local path")
    p.add_argument("question", help="问题 / question")
    p.add_argument("--fps", type=float, default=1)
    p.add_argument("--max-tokens", type=int, default=262144)
    p.add_argument("--timeout", type=int, default=600, help="请求超时秒数 / request timeout in seconds")
    p.set_defaults(func=cmd_mixed)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
