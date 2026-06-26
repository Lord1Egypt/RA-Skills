#!/usr/bin/env python3
"""
使用 pysmb 库浏览 SMB 共享并下载字幕
"""

from smb.SMBConnection import SMBConnection
import os
import sys

# SMB 配置
USERNAME = "13917908083"
PASSWORD = "Roger0808"
SERVER_NAME = "Z4ProPlus-X6L8"  # NetBIOS 名称
SERVER_IP = "192.168.1.246"  # 尝试 IP 地址
SHARE_NAME = "super8083"
REMOTE_PATH = "qb/downloads"

def connect_smb():
    """连接 SMB 服务器"""
    conn = SMBConnection(
        USERNAME,
        PASSWORD,
        "openclaw-client",  # 客户端名称
        SERVER_NAME,         # 服务器名称
        use_ntlm_v2=True
    )
    
    print(f"尝试连接到 {SERVER_IP}...")
    
    # 尝试连接
    try:
        connected = conn.connect(SERVER_IP, 445, timeout=10)
        if connected:
            print("✓ SMB 连接成功!")
            return conn
        else:
            print("✗ 连接失败")
            return None
    except Exception as e:
        print(f"✗ 连接错误: {e}")
        return None

def list_files(conn, path=""):
    """列出 SMB 共享中的文件"""
    try:
        full_path = f"{REMOTE_PATH}/{path}".strip("/")
        print(f"\\n浏览目录: {full_path}")
        
        files = conn.listPath(SHARE_NAME, full_path)
        
        video_files = []
        dirs = []
        
        print(f"{'='*60}")
        print(f"{'名称':<40} {'类型':<10} {'大小':<10}")
        print(f"{'='*60}")
        
        for f in files:
            if f.filename in ['.', '..']:
                continue
                
            is_dir = f.isDirectory
            size = f.file_size if not is_dir else "-"
            type_str = "📁 目录" if is_dir else "📄 文件"
            
            # 检查是否是视频文件
            video_exts = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
            is_video = any(f.filename.lower().endswith(ext) for ext in video_exts)
            
            if is_video:
                type_str = "🎬 视频"
                video_files.append((f.filename, full_path, f.file_size))
            elif is_dir:
                dirs.append(f.filename)
            
            size_str = f"{size:,} bytes" if isinstance(size, int) else size
            print(f"{f.filename[:38]:<40} {type_str:<10} {size_str:<10}")
        
        print(f"{'='*60}")
        print(f"\\n找到 {len(video_files)} 个视频文件, {len(dirs)} 个目录")
        
        return video_files, dirs
        
    except Exception as e:
        print(f"✗ 列出文件失败: {e}")
        return [], []

def download_subtitles_for_videos(video_files):
    """为视频文件下载字幕"""
    if not video_files:
        print("\\n没有找到视频文件")
        return
    
    print(f"\\n\\n{'='*60}")
    print("准备为以下视频下载字幕:")
    print(f"{'='*60}")
    
    for filename, path, size in video_files:
        print(f"  🎬 {filename}")
        # 这里可以调用字幕下载脚本
        # 暂时只列出文件名
    
    print(f"\\n找到 {len(video_files)} 个视频文件")
    return video_files

def main():
    print("="*60)
    print("SMB 视频浏览器 - 用于字幕下载")
    print("="*60)
    print(f"\\n服务器: {SERVER_NAME}")
    print(f"共享: {SHARE_NAME}")
    print(f"路径: {REMOTE_PATH}")
    print(f"用户: {USERNAME}")
    print()
    
    # 连接 SMB
    conn = connect_smb()
    if not conn:
        print("\\n尝试使用 IP 地址连接...")
        # 可以尝试获取 IP 地址
        return 1
    
    # 列出文件
    video_files, dirs = list_files(conn)
    
    # 递归浏览子目录
    all_videos = list(video_files)
    
    for d in dirs:
        sub_path = f"{d}"
        sub_videos, _ = list_files(conn, sub_path)
        all_videos.extend(sub_videos)
    
    # 准备字幕下载
    if all_videos:
        download_subtitles_for_videos(all_videos)
    
    conn.close()
    print("\\n✓ SMB 连接已关闭")
    return 0

if __name__ == "__main__":
    sys.exit(main())
