#!/usr/bin/env python3
"""
Music Downloader Script
=========================
Usage: python3 download_music.py "<search term or URL>" "<category>"

首次使用请先修改下方的 MUSIC_DIR 配置为你的音乐目录路径
"""

import os
import sys
import subprocess

# ============ 配置区域 =============
# 修改此行为你的音乐目录路径（示例：~/Music 或 /path/to/your/music）
MUSIC_DIR = os.path.expanduser("~/Music")

# Chrome cookie 提取方式: chrome / safari / firefox
# 如果不使用 cookie，可设为 None
BROWSER = "chrome"
# ==================================


def ensure_dir(category):
    """确保分类目录存在"""
    category_path = os.path.join(MUSIC_DIR, category)
    os.makedirs(category_path, exist_ok=True)
    return category_path


def get_cookie_arg():
    """获取 cookie 参数"""
    if BROWSER:
        return f"--cookies-from-browser {BROWSER}"
    return ""


def download(search_term, category):
    """使用 yt-dlp 下载音乐"""
    output_dir = ensure_dir(category)
    
    # 判断是 URL 还是搜索词
    if search_term.startswith(('http://', 'https://')):
        url = search_term
        print(f"检测到 URL: {url}")
    else:
        url = f"ytsearch10:{search_term}"
        print(f"正在搜索: {search_term}")
    
    # 输出模板：歌名-作者-来源.mp3
    output_template = os.path.join(output_dir, "%(title)s-%(uploader)s-%(extractor)s.%(ext)s")
    
    # 构建 yt-dlp 命令
    cookie_arg = get_cookie_arg().split() if get_cookie_arg() else []
    
    cmd = [
        "yt-dlp",
    ] + cookie_arg + [
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--output", output_template,
        "--no-playlist",
        url
    ]
    
    print(f"下载目录: {output_dir}")
    print(f"命令: {' '.join(cmd)}")
    print("开始下载...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 下载成功!")
            for line in result.stdout.split('\n'):
                if 'Destination' in line or 'Merging' in line:
                    print(line)
        else:
            print("❌ 下载失败!")
            print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
        return result.returncode
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("=" * 40)
        print("Music Manager 下载器")
        print("=" * 40)
        print("用法: python3 download_music.py '<搜索词或URL>' '<分类文件夹>'")
        print()
        print("示例:")
        print("  python3 download_music.py '周杰伦 稻香' '中文'")
        print("  python3 download_music.py 'https://youtube.com/...' '英文'")
        print("  python3 download_music.py 'https://bilibili.com/...' '游戏'")
        print()
        print("首次使用请先编辑脚本修改 MUSIC_DIR 路径")
        print("=" * 40)
        sys.exit(1)
    
    search_term = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else "未分类"
    
    sys.exit(download(search_term, category))
