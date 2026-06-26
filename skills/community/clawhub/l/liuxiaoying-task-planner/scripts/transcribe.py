#!/usr/bin/env python3
"""
语音转文字模块（使用 OpenAI Whisper API）
用法: python transcribe.py <音频文件路径>
环境变量: OPENAI_API_KEY 必须设置
"""

import os
import sys
from pathlib import Path

def transcribe_audio(file_path: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        print("错误: 请先安装 openai 库: pip install openai", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )
    return transcript

def main():
    if len(sys.argv) != 2:
        print("用法: python transcribe.py <音频文件路径>", file=sys.stderr)
        sys.exit(1)
    
    audio_path = Path(sys.argv[1])
    if not audio_path.exists():
        print(f"错误: 文件不存在: {audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        text = transcribe_audio(str(audio_path))
        print(text)
    except Exception as e:
        print(f"转写失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
