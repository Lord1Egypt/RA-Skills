#!/usr/bin/env python3
"""MiMo V2.5 TTS — 音频样本复刻音色 / Voice Clone TTS (中文/English)

模型 / Model: mimo-v2.5-tts-voiceclone
支持 / Supports: 音频样本克隆音色 Voice cloning from audio sample、导演模式 Director mode

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
        description="MiMo V2.5 TTS 音频样本复刻音色 / Voice Clone TTS"
    )
    parser.add_argument("--text", required=True,
                        help="要合成的文本 / Text to synthesize")
    parser.add_argument("--voice-file", required=True,
                        help="音色样本音频路径（mp3/wav）/ Voice sample path")
    parser.add_argument("--context", default="",
                        help="自然语言风格控制 / Natural language style control (director mode)")
    parser.add_argument("--output", default="tmp/mimo-v2.5-tts/voiceclone.wav",
                        help="输出 wav 路径 / Output wav path")
    return parser.parse_args()


def build_client() -> OpenAI:
    api_key = os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("❌ MIMO_API_KEY 未设置 / is not set", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url="https://api.xiaomimimo.com/v1")


def encode_voice_file(file_path: str) -> str:
    """将音频样本编码为 base64 DataURL / Encode voice sample as base64 DataURL"""
    path = Path(file_path)
    if not path.exists():
        print(f"❌ 音频文件不存在 / File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    suffix = path.suffix.lower()
    mime_map = {".mp3": "audio/mpeg", ".wav": "audio/wav"}
    mime_type = mime_map.get(suffix)
    if not mime_type:
        print(f"❌ 不支持的格式 / Unsupported format: {suffix}（仅支持 mp3/wav）", file=sys.stderr)
        sys.exit(1)

    data = path.read_bytes()
    if len(data) > 10 * 1024 * 1024:
        print("❌ 音频文件过大（最大 10 MB）/ File too large (max 10 MB)", file=sys.stderr)
        sys.exit(1)

    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def main() -> None:
    args = parse_args()
    client = build_client()

    messages = []
    if args.context:
        messages.append({"role": "user", "content": args.context})
    messages.append({"role": "assistant", "content": args.text})

    completion = client.chat.completions.create(
        model="mimo-v2.5-tts-voiceclone",
        messages=messages,
        audio={"format": "wav", "voice": encode_voice_file(args.voice_file)},
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
