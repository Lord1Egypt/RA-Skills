#!/usr/bin/env python3
"""
本地视觉模型图片描述桥接脚本
通过 Ollama 调用本地视觉模型（qwen3.5:4b）读取图片并返回文字描述。

用法:
    python describe_image.py <图片路径> [--model qwen3.5:4b] [--prompt "自定义提示词"]

输出: 纯文本图片描述，直接打印到 stdout
"""

import sys
import os
import json
import base64
import argparse
import urllib.request
import urllib.error


OLLAMA_API = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "qwen3.5:4b"  # 轻量化视觉模型
DEFAULT_PROMPT = "请详细描述这张图片的内容。包括：主体对象、场景、文字、颜色、布局、氛围等所有你能看到的细节。"


def encode_image(image_path: str) -> str:
    """读取图片并编码为 base64"""
    if not os.path.isfile(image_path):
        print(f"[ERROR] 图片文件不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"[ERROR] 读取图片失败: {e}", file=sys.stderr)
        sys.exit(1)


def get_mime_type(image_path: str) -> str:
    """根据扩展名返回 MIME 类型"""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    return mime_map.get(ext, "image/png")


def call_ollama_vision(image_path: str, model: str, prompt: str) -> str:
    """调用 Ollama 视觉模型"""
    b64 = encode_image(image_path)

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [b64],
            }
        ],
    }

    try:
        req = urllib.request.Request(
            OLLAMA_API,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            msg = result.get("message", {})
            content = msg.get("content", "").strip()
            # qwen3.5 thinking 模式: content 可能为空，从 thinking 字段取
            if not content:
                content = msg.get("thinking", "").strip()
            return content
    except urllib.error.URLError as e:
        print(f"[ERROR] 连接 Ollama 失败 (请确认 Ollama 正在运行): {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 调用视觉模型失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="用本地视觉模型描述图片")
    parser.add_argument("image", help="图片文件路径")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama 模型名 (默认: {DEFAULT_MODEL})")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="自定义提示词")
    args = parser.parse_args()

    print(f"[INFO] 正在用 {args.model} 分析图片: {args.image}", file=sys.stderr)
    description = call_ollama_vision(args.image, args.model, args.prompt)
    print(description)


if __name__ == "__main__":
    main()
