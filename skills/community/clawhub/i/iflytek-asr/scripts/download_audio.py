#!/usr/bin/env python3
"""
Download audio from YouTube videos.

Usage:
    python3 download_audio.py <youtube_url> [output_path]
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


def download_audio(youtube_url, output_path=None):
    """
    Download audio from YouTube video using yt-dlp.
    
    Args:
        youtube_url: YouTube video URL or video ID
        output_path: Optional output directory (defaults to current directory)
    
    Returns:
        Path to downloaded audio file
    """
    # Find yt-dlp executable
    ytdlp_paths = [
        'yt-dlp',  # Try PATH first
        str(Path.home() / 'Library' / 'Python' / '3.9' / 'bin' / 'yt-dlp'),  # User install
        '/usr/local/bin/yt-dlp',  # Homebrew
        '/opt/homebrew/bin/yt-dlp',  # Apple Silicon Homebrew
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
    
    # Extract video ID for filename
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
    
    # Download audio using yt-dlp with enhanced options
    cmd = [
        ytdlp_cmd,
        '-x',  # Extract audio
        '--audio-format', 'mp3',  # Convert to MP3
        '--audio-quality', '0',  # Best quality
        '-o', output_template,
        '--no-check-certificates',  # 跳过证书检查
        '--extractor-args', 'youtube:player_client=android',  # 使用 Android 客户端
        '--user-agent', 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36',  # Android UA
        youtube_url
    ]
    
    try:
        print(f"Downloading audio from: {youtube_url}")
        print(f"Output directory: {output_dir}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Find the downloaded file
        audio_file = output_dir / f"{video_id}.mp3"
        if audio_file.exists():
            print(f"\n✅ Audio downloaded successfully: {audio_file}")
            return str(audio_file)
        else:
            print(f"Error: Downloaded file not found at {audio_file}", file=sys.stderr)
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 download_audio.py <youtube_url> [output_path]")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    download_audio(youtube_url, output_path)


if __name__ == '__main__':
    main()
