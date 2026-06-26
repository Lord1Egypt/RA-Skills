#!/usr/bin/env python3
# /// script
# dependencies = [
#   "google-genai>=1.0.0",
# ]
# ///
"""
Reverse-engineer a visual style from a reference image using Gemini Vision.
Outputs a structured Chinese prompt prefix suitable for image generation.

Usage:
  uv run reverse_style.py --image /path/to/ref.jpg
  uv run reverse_style.py --image /path/to/ref.jpg --output style.txt
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

ANALYSIS_PROMPT = """请作为一名顶级的 AI 绘画提示词专家，为我分析这张图片的视觉风格。

**任务目标：** 提取并反推这张图片的艺术风格，生成一份通用的 Prompt。这份 Prompt 必须剥离原图中的具体角色、文字或特定情节，仅保留其美学灵魂。

**分析维度（请务必涵盖以下 15 个方面）：**
1. **基础维度：** 画面风格、画面成分组成、构图方式、分镜类型、光影特质、色调与色彩科学、媒介与材质纹理、情绪与氛围、渲染/拍摄参数。
2. **进阶维度：** 时代感与文化语境、空间逻辑与透视关系、信息密度与留白、动态状态（瞬时感）、后期处理与数字痕迹、符号化特征。

**输出要求：**
1. 请直接输出一段完整的、高水准的**中文提示词**。
2. 在提示词的开头或核心位置，使用 `[在此处替换为您想要生成的主体内容]` 作为占位符。
3. 确保该 Prompt 具有高度通用性，用户只需更换占位符内容，即可在保持原图质感的同时生成全新的画面。
4. 无需输出分析过程，请直接给出最终的 Prompt 文本。"""


def resolve_api_key(cli_key: str | None) -> str:
    key = cli_key or os.getenv("GEMINI_API_KEY") or os.getenv("NANO_BANANA_API_KEY")
    if not key:
        raise ValueError("Missing API key. Set GEMINI_API_KEY or NANO_BANANA_API_KEY.")
    return key


def load_image_bytes(path: str) -> tuple[bytes, str]:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")
    suffix = p.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                ".webp": "image/webp", ".gif": "image/gif"}
    mime = mime_map.get(suffix, "image/jpeg")
    return p.read_bytes(), mime


def reverse_style(image_path: str, api_key: str, model: str = "gemini-2.5-flash") -> str:
    client = genai.Client(api_key=api_key)
    img_bytes, mime_type = load_image_bytes(image_path)

    response = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_bytes(data=img_bytes, mime_type=mime_type),
            types.Part.from_text(text=ANALYSIS_PROMPT),
        ],
    )
    return response.text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Reverse-engineer image style via Gemini Vision.")
    parser.add_argument("-i", "--image", required=True, help="Path to reference image")
    parser.add_argument("-o", "--output", default=None, help="Save result to file (optional)")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash", help="Gemini text model")
    parser.add_argument("-k", "--api-key", default=None, help="API key override")
    args = parser.parse_args()

    api_key = resolve_api_key(args.api_key)
    print(f"🔍 Analyzing style from: {args.image}", file=sys.stderr)

    result = reverse_style(args.image, api_key, args.model)

    if args.output:
        Path(args.output).expanduser().write_text(result, encoding="utf-8")
        print(f"✅ Style saved to: {args.output}", file=sys.stderr)

    print(result)


if __name__ == "__main__":
    main()
