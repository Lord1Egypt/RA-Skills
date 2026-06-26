#!/usr/bin/env python3
"""
Jable.tv Video Downloader Lite - Simple downloader without web server or Telegram
"""

import sys
import os
import re
import subprocess
import urllib.request
import shutil
import platform
import signal
from pathlib import Path
from urllib.parse import quote

def get_default_videos_dir():
    home = Path.home()
    system = platform.system()
    if system == "Linux":
        try:
            res = subprocess.run(['xdg-user-dir', 'VIDEOS'], capture_output=True, text=True, check=True)
            path = Path(res.stdout.strip())
            if path.exists(): return str(path)
        except: pass
    candidates = ["Videos", "Movies", "影片", "動画"]
    for name in candidates:
        p = home / name
        if p.exists(): return str(p)
    return str(home)

def normalize_url(input_str):
    input_str = input_str.strip()
    if input_str.startswith('http://') or input_str.startswith('https://'):
        return input_str.rstrip('/') + '/'
    return f"https://jable.tv/videos/{input_str}/"

def get_real_hls_url(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Referer': 'https://jable.tv/'}
    try:
        req = urllib.request.Request(page_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        title_match = re.search(r'<h4[^>]*>([^<]+)</h4>', html)
        title = re.sub(r'[\\/:*?"<>|]', '_', title_match.group(1).strip()) if title_match else "video"
        hls_match = re.search(r"hlsUrl\s*=\s*'([^']+)'", html)
        if not hls_match: hls_match = re.search(r'source\s*:\s*"([^"]+\.m3u8)"', html)
        if hls_match: return title, hls_match.group(1)
    except Exception as e:
        print(f"Error getting video: {e}")
    return None, None

def extract_actress_name(title):
    name_match = re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]+$', title.strip())
    return name_match.group(0).strip() if name_match else "Unknown"

def organize_by_actress(output_path, actress_name):
    output_dir = os.path.dirname(output_path)
    actress_dir = os.path.join(output_dir, actress_name)
    if not os.path.exists(actress_dir): os.makedirs(actress_dir)
    new_path = os.path.join(actress_dir, os.path.basename(output_path))
    if output_path != new_path: shutil.move(output_path, new_path)
    return new_path

def search_actress_videos(actress_name):
    print(f"🔍 Searching: {actress_name}")
    search_url = f"https://jable.tv/search/{quote(actress_name)}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    videos = []
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
        for m in re.findall(r'<h6 class="title"><a href="(https://jable\.tv/videos/[^"]+/)">([^<]+)</a></h6>', html):
            videos.append({'url': m[0], 'title': m[1].strip()})
    except Exception as e: print(f"Error: {e}")
    return videos

def check_already_downloaded(video_title, videos_dir):
    if not os.path.exists(videos_dir): return False
    code = re.search(r'([A-Z]+-\d+)', video_title, re.I)
    if code:
        for root, dirs, files in os.walk(videos_dir):
            if any(code.group(1).upper() in f.upper() for f in files): return True
    return False

def cleanup_temp_files(output_path):
    """Clean up temporary files generated during download"""
    if not output_path: return
    base_dir = os.path.dirname(output_path)
    filename = os.path.basename(output_path)
    if os.path.exists(base_dir):
        for f in os.listdir(base_dir):
            if (f.startswith(filename + '.part') or 
                f.startswith('.' + filename + '.part') or
                f == filename + '.ytdl' or
                f == '.' + filename + '.ytdl'):
                try:
                    os.remove(os.path.join(base_dir, f))
                    print(f"🧹 Cleaned temp file: {f}")
                except: pass

def download_single_video(url, output_dir, max_retries=2):
    title, m3u8_url = get_real_hls_url(url)
    if not m3u8_url: 
        print(f"❌ Failed to get video URL: {url}")
        return False
    
    actress = extract_actress_name(title)
    output_path = os.path.join(output_dir, f"{title}.mp4")
    
    for attempt in range(max_retries):
        cmd = ['yt-dlp', '--force-ipv4', '--concurrent-fragments', '16', '--referer', 'https://jable.tv/', '-o', output_path, m3u8_url]
        
        print(f"⬇️ Downloading: {title} (attempt {attempt + 1}/{max_retries})")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        for line in process.stdout:
            if '[download]' in line:
                p = re.search(r'([\d.]+)%', line)
                if p:
                    print(f"   Progress: {p.group(1)}%")
        
        process.wait()
        if process.returncode == 0 and os.path.exists(output_path):
            organize_by_actress(output_path, actress)
            cleanup_temp_files(output_path)
            print(f"✅ Completed: {title}")
            return True
        
        print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
        cleanup_temp_files(output_path)
    
    cleanup_temp_files(output_path)
    print(f"❌ Failed: {title}")
    return False

def signal_handler(signum, frame):
    print("\n⚠️ Interrupted, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) >= 2 and sys.argv[1] == '--search':
        actress_name = sys.argv[2] if len(sys.argv) >= 3 else None
        count = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        output_dir = sys.argv[4] if len(sys.argv) >= 5 else get_default_videos_dir()
        
        os.makedirs(output_dir, exist_ok=True)
        
        videos = search_actress_videos(actress_name)
        if not videos: print(f"❌ Cannot find '{actress_name}'"); sys.exit(1)
        
        new_videos = [v for v in videos if not check_already_downloaded(v['title'], output_dir)][:count]
        print(f"📥 Will download {len(new_videos)} videos to {output_dir}")
        
        success_count = 0
        for v in new_videos:
            if download_single_video(v['url'], output_dir):
                success_count += 1
        
        print(f"🎉 Done! {success_count}/{len(new_videos)} videos downloaded successfully")
        
    elif len(sys.argv) >= 2:
        video_id = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else get_default_videos_dir()
        
        os.makedirs(output_dir, exist_ok=True)
        
        url = normalize_url(video_id)
        print(f"🔍 Getting video info: {url}")
        
        if download_single_video(url, output_dir):
            print("🎉 Download completed!")
        else:
            print("❌ Download failed")
            sys.exit(1)
    else:
        print("Usage: jable_downloader.py <video_id> [directory]")
        print("       jable_downloader.py --search <actress> <count> [directory]")
        sys.exit(1)
