#!/usr/bin/env python3
"""
视频下载工具 - 基于 yt-dlp
支持 YouTube、Bilibili、抖音等数千个网站
"""

import os
import sys
import subprocess
import argparse
import re
from urllib.parse import urlparse

# 默认下载目录
DEFAULT_DOWNLOAD_DIR = os.path.expanduser("~/Downloads/Videos")

def check_yt_dlp():
    """检查 yt-dlp 是否已安装"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False

def install_yt_dlp():
    """安装 yt-dlp"""
    print("📦 正在安装 yt-dlp...")
    try:
        # 尝试使用 pip 安装
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-U', 'yt-dlp'], 
                      check=True, capture_output=True)
        print("✅ yt-dlp 安装成功")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        print("\n请手动安装:")
        print("  pip install -U yt-dlp")
        print("或访问: https://github.com/yt-dlp/yt-dlp#installation")
        return False

def get_platform(url):
    """识别视频平台"""
    domain = urlparse(url).netloc.lower()
    
    platforms = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube',
        'bilibili.com': 'Bilibili',
        'b23.tv': 'Bilibili',
        'douyin.com': '抖音',
        'tiktok.com': 'TikTok',
        'ixigua.com': '西瓜视频',
        'weibo.com': '微博',
        'x.com': 'X (Twitter)',
        'twitter.com': 'X (Twitter)',
        'instagram.com': 'Instagram',
        'facebook.com': 'Facebook',
        'reddit.com': 'Reddit',
    }
    
    for key, name in platforms.items():
        if key in domain:
            return name
    
    return "未知平台"

def download_video(url, output_dir=None, quality='best', audio_only=False, 
                   subtitle=False, playlist=False):
    """
    下载视频
    
    Args:
        url: 视频链接
        output_dir: 下载目录
        quality: 视频质量 (best, worst, bestvideo, bestaudio 等)
        audio_only: 仅下载音频
        subtitle: 下载字幕
        playlist: 下载整个播放列表
    """
    
    # 检查 yt-dlp
    if not check_yt_dlp():
        print("⚠️  yt-dlp 未安装")
        if not install_yt_dlp():
            return False
    
    # 设置下载目录
    if output_dir is None:
        output_dir = DEFAULT_DOWNLOAD_DIR
    
    # 创建下载目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 识别平台
    platform = get_platform(url)
    print(f"📺 平台: {platform}")
    print(f"🔗 链接: {url}")
    print(f"📁 下载目录: {output_dir}")
    print("-" * 60)
    
    # 构建命令
    cmd = ['yt-dlp', '--no-warnings']
    
    # 输出模板
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    cmd.extend(['-o', output_template])
    
    # 格式选择
    if audio_only:
        cmd.extend(['-f', 'bestaudio', '--extract-audio', '--audio-format', 'mp3'])
        print("🎵 模式: 仅音频 (MP3)")
    else:
        if quality == 'best':
            cmd.extend(['-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'])
        elif quality == 'worst':
            cmd.extend(['-f', 'worst'])
        else:
            cmd.extend(['-f', quality])
        print(f"🎬 模式: 视频 ({quality})")
    
    # 字幕
    if subtitle:
        cmd.extend(['--write-subs', '--sub-langs', 'zh-CN,zh-TW,en'])
        print("📝 字幕: 下载")
    
    # 播放列表
    if not playlist:
        cmd.append('--no-playlist')
    else:
        print("📂 播放列表: 下载全部")
    
    # 其他选项
    cmd.extend(['--progress', '--newline'])
    
    # 添加 URL
    cmd.append(url)
    
    # 执行下载
    print("\n⬇️  开始下载...\n")
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ 下载成功！")
            print(f"📁 保存位置: {output_dir}")
            print("=" * 60)
            return True
        else:
            print("\n❌ 下载失败")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  下载已取消")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False

def batch_download(urls_file, **kwargs):
    """批量下载"""
    if not os.path.exists(urls_file):
        print(f"❌ 文件不存在: {urls_file}")
        return False
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 批量下载: {len(urls)} 个视频\n")
    
    success_count = 0
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] ")
        if download_video(url, **kwargs):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ 成功: {success_count}/{len(urls)}")
    print(f"{'=' * 60}")
    
    return success_count == len(urls)

def main():
    parser = argparse.ArgumentParser(
        description='视频下载工具 - 支持 YouTube、Bilibili、抖音等',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 下载单个视频（最佳质量）
  python3 video_downloader.py "https://www.youtube.com/watch?v=xxxxx"
  
  # 仅下载音频
  python3 video_downloader.py "URL" --audio-only
  
  # 指定下载目录
  python3 video_downloader.py "URL" -o ~/Desktop/Videos
  
  # 批量下载
  python3 video_downloader.py -f urls.txt
  
  # 下载带字幕
  python3 video_downloader.py "URL" --subtitle
        """
    )
    
    parser.add_argument('url', nargs='?', help='视频链接')
    parser.add_argument('-f', '--file', help='批量下载（URL列表文件）')
    parser.add_argument('-o', '--output', help='下载目录', default=DEFAULT_DOWNLOAD_DIR)
    parser.add_argument('-q', '--quality', help='视频质量', default='best',
                       choices=['best', 'worst', 'bestvideo', 'bestaudio'])
    parser.add_argument('-a', '--audio-only', action='store_true', help='仅下载音频')
    parser.add_argument('-s', '--subtitle', action='store_true', help='下载字幕')
    parser.add_argument('-p', '--playlist', action='store_true', help='下载播放列表')
    parser.add_argument('--install', action='store_true', help='安装 yt-dlp')
    
    args = parser.parse_args()
    
    # 安装模式
    if args.install:
        install_yt_dlp()
        return
    
    # 检查参数
    if not args.url and not args.file:
        parser.print_help()
        return
    
    print("=" * 60)
    print("🎬 视频下载工具 (Powered by yt-dlp)")
    print("=" * 60)
    
    # 批量下载
    if args.file:
        batch_download(
            args.file,
            output_dir=args.output,
            quality=args.quality,
            audio_only=args.audio_only,
            subtitle=args.subtitle,
            playlist=args.playlist
        )
    else:
        # 单个下载
        download_video(
            args.url,
            output_dir=args.output,
            quality=args.quality,
            audio_only=args.audio_only,
            subtitle=args.subtitle,
            playlist=args.playlist
        )

if __name__ == "__main__":
    main()
