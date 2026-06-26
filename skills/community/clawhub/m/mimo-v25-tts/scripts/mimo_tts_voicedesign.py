#!/usr/bin/env python3
"""MiMo V2.5 TTS — 文本描述定制音色 / Voice Design TTS (中文/English)

模型 / Model: mimo-v2.5-tts-voicedesign
支持 / Supports: 文本生成音色 Voice design via text description、导演模式 Director mode

依赖 / Requires:
    pip install openai
    export MIMO_API_KEY=...
"""

import argparse
import base64
import os
import sys
from pathlib import Path
from openai import OpenAI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MiMo V2.5 TTS 文本描述定制音色 / Voice Design TTS"
    )
    parser.add_argument("--text", required=True,
                        help="要合成的文本 / Text to synthesize")
    parser.add_argument("--context", required=True,
                        help="音色描述+风格控制 / Voice description + style control (director mode)")
    parser.add_argument("--output", default="tmp/mimo-v2.5-tts/voicedesign.wav",
                        help="输出 wav 路径 / Output wav path")
    return parser.parse_args()


def build_client() -> OpenAI:
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("❌ MIMO_API_KEY 未设置 / is not set", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url="https://api.xiaomimimo.com/v1")


def main() -> None:
    args = parse_args()
    client = build_client()

    messages = [
        {"role": "user", "content": args.context},
        {"role": "assistant", "content": args.text},
    ]

    completion = client.chat.completions.create(
        model="mimo-v2.5-tts-voicedesign",
        messages=messages,
        audio={"format": "wav"},
    )

    message = completion.choices[0].message
    if message.audio is None or not getattr(message.audio, "data", None):
        print("❌ 未返回音频数据 / No audio data returned", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(base64.b64decode(message.audio.data))
    print(output_path)


if __name__ == "__main__":
    main()
