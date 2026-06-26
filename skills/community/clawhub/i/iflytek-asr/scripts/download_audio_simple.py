#!/usr/bin/env python3
"""
使用简化方法下载 YouTube 音频（不需要 ffmpeg）

用法:
    python3 download_audio_simple.py <youtube_url> [output_dir]
"""

import sys
import os
import subprocess
import re
from pathlib import Path


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def download_audio_simple(youtube_url, output_path=None):
    """
    使用简化方法下载音频（仅下载最佳音频流，不转换格式）
    
    Args:
        youtube_url: YouTube video URL or video ID
        output_path: Optional output directory
    
    Returns:
        Path to downloaded audio file
    """
    # Find yt-dlp executable
    ytdlp_paths = [
        'yt-dlp',
        str(Path.home() / 'Library' / 'Python' / '3.9' / 'bin' / 'yt-dlp'),
        '/usr/local/bin/yt-dlp',
        '/opt/homebrew/bin/yt-dlp',
    ]
    
    ytdlp_cmd = None
    for path in ytdlp_paths:
        try:
            subprocess.run([path, '--version'], 
                          capture_output=True, 
                          check=True)
            ytdlp_cmd = path
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if ytdlp_cmd is None:
        print("Error: yt-dlp is not installed.", file=sys.stderr)
        print("Install with: pip3 install yt-dlp", file=sys.stderr)
        sys.exit(1)
    
    # Extract video ID
    try:
        video_id = extract_video_id(youtube_url)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Set output path
    if output_path:
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()
    
    output_template = str(output_dir / f"{video_id}.%(ext)s")
    
    # 方法 1: 尝试直接下载音频流（webm/m4a），不需要 ffmpeg
    print(f"📥 下载音频: {youtube_url}")
    print(f"📂 输出目录: {output_dir}")
    print("🔧 方法: 直接下载音频流（不转换格式）")
    
    cmd = [
        ytdlp_cmd,
        '-f', 'bestaudio/best',  # 下载最佳音频流，或最佳视频流
        '--extract-audio',  # 提取音频
        '-o', output_template,
        '--no-check-certificates',
        '--extractor-args', 'youtube:player_client=android,web',
        '--user-agent', 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',
        '--no-warnings',
        youtube_url
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # 查找下载的文件（可能是 .webm 或 .m4a）
        for ext in ['.webm', '.m4a', '.opus', '.mp4']:
            audio_file = output_dir / f"{video_id}{ext}"
            if audio_file.exists():
                print(f"\n✅ 音频下载成功: {audio_file}")
                print(f"💡 提示: 文件格式为 {ext}，可直接用于语音转文字")
                return str(audio_file)
        
        print(f"Error: 未找到下载的文件", file=sys.stderr)
        sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"Error: 下载失败", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 download_audio_simple.py <youtube_url> [output_dir]")
        print()
        print("示例:")
        print("  python3 download_audio_simple.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("  python3 download_audio_simple.py https://www.youtube.com/watch?v=VIDEO_ID ~/Downloads/xufei")
        print()
        print("说明:")
        print("  - 直接下载音频流（webm/m4a 格式）")
        print("  - 不需要 ffmpeg")
        print("  - 下载的文件可直接用于语音转文字")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    download_audio_simple(youtube_url, output_path)


if __name__ == '__main__':
    main()
