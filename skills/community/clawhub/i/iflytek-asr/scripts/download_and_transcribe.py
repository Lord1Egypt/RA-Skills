#!/usr/bin/env python3
"""
下载 YouTube 视频音频并转为文字

用法:
    python3 download_and_transcribe.py <youtube_url> [output_dir]
"""

import sys
import subprocess
from pathlib import Path

# 导入下载和转写模块
import download_audio
import speech_to_text


def download_and_transcribe(youtube_url, output_dir=None):
    """
    下载 YouTube 音频并转为文字
    
    Args:
        youtube_url: YouTube 视频 URL
        output_dir: 输出目录（默认为当前目录）
    """
    # 1. 下载音频
    print("\n" + "=" * 60)
    print("步骤 1/2: 下载音频")
    print("=" * 60)
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()
    
    audio_file = download_audio.download_audio(youtube_url, str(output_path))
    
    if not audio_file:
        print("❌ 音频下载失败")
        sys.exit(1)
    
    # 2. 转为文字
    print("\n" + "=" * 60)
    print("步骤 2/2: 语音转文字")
    print("=" * 60)
    
    try:
        text = speech_to_text.speech_to_text(audio_file)
        print(f"\n✅ 处理完成!")
        print(f"   音频文件: {audio_file}")
        print(f"   文字文件: {Path(audio_file).with_suffix('.txt')}")
        return audio_file, text
    except Exception as e:
        print(f"❌ 语音转文字失败: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 download_and_transcribe.py <youtube_url> [output_dir]")
        print()
        print("示例:")
        print("  python3 download_and_transcribe.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("  python3 download_and_transcribe.py https://www.youtube.com/watch?v=VIDEO_ID ~/Downloads/xufei")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    download_and_transcribe(youtube_url, output_dir)


if __name__ == '__main__':
    main()
