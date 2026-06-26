#!/usr/bin/env python3
"""
为 movie 目录中的电影批量下载字幕
Usage:
    python3 download-movie-subtitles.py --dry-run    # 检查哪些需要字幕
    python3 download-movie-subtitles.py              # 下载所有缺失字幕
    python3 download-movie-subtitles.py -f "Game.of.Thrones"  # 下载指定文件夹
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import argparse
import tempfile
import subprocess
import shutil

# SMB 配置 - 机械硬盘
SMB_CONFIG = {
    "username": '13917908083',
    "password": 'Roger0808',
    "server_name": 'Z4ProPlus-X6L8',
    "server_ip": '192.168.1.246',
    "share_name": 'sata11-139XXXX8083',  # 机械硬盘
    "remote_path": 'movie'               # movie 目录
}

DEFAULT_LANGUAGES = ['zh', 'zh-cn', 'zh-tw', 'chs', 'cht']
VIDEO_EXTS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']

def connect_smb():
    """连接 SMB 服务器"""
    conn = SMBConnection(
        SMB_CONFIG["username"], SMB_CONFIG["password"],
        "openclaw-client", SMB_CONFIG["server_name"], use_ntlm_v2=True
    )
    if conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10):
        return conn
    return None

def has_subtitle(conn, folder_path, video_base):
    """检查视频是否已有字幕"""
    for ext in ['.srt', '.ass', '.vtt', '.ssa']:
        for lang in ['.zh', '.en', '.chs', '.eng', '']:
            sub_name = f"{video_base}{lang}{ext}" if lang else f"{video_base}{ext}"
            try:
                conn.getAttributes(SMB_CONFIG["share_name"], f"{folder_path}/{sub_name}")
                return True
            except:
                pass
    return False

def download_subtitle_for_video(conn, folder_path, video_filename, languages=None):
    """为单个视频下载字幕"""
    if languages is None:
        languages = DEFAULT_LANGUAGES
    
    base_name = os.path.splitext(video_filename)[0]
    
    # 检查是否已有字幕
    if has_subtitle(conn, folder_path, base_name):
        print(f"      ⏭️  已有字幕: {video_filename}")
        return True, "skipped"
    
    print(f"      🔍 搜索字幕: {video_filename}")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    try:
        # 创建占位文件（只需要文件名用于 subliminal 搜索）
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 构建 subliminal 命令
        cmd = ['subliminal', 'download', '--force']
        for lang in languages:
            cmd.extend(['-l', lang])
        cmd.append(local_video)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # 检查下载的字幕
        downloaded = []
        for ext in ['.srt', '.ass', '.vtt']:
            for lang in ['.zh', '.en', '.zho', '.eng', '.chs', '.cht']:
                sub_file = os.path.join(temp_dir, f"{base_name}{lang}{ext}")
                if os.path.exists(sub_file) and sub_file not in downloaded:
                    downloaded.append(sub_file)
            # 也可能没有语言代码
            sub_file = os.path.join(temp_dir, f"{base_name}{ext}")
            if os.path.exists(sub_file) and sub_file not in downloaded:
                downloaded.append(sub_file)
        
        if not downloaded:
            print(f"      ❌ 未找到字幕")
            return False, "not_found"
        
        # 上传字幕到 SMB
        uploaded = 0
        for i, sub_file in enumerate(downloaded):
            sub_ext = os.path.splitext(sub_file)[1]
            if i == 0:
                final_name = f"{base_name}.zh{sub_ext}"
            else:
                final_name = f"{base_name}.en{sub_ext}"
            
            remote_sub_path = f"{folder_path}/{final_name}"
            
            with open(sub_file, 'rb') as f:
                conn.storeFile(SMB_CONFIG["share_name"], remote_sub_path, f)
            
            print(f"      ✅ 上传: {final_name}")
            uploaded += 1
        
        return uploaded > 0, "downloaded"
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def process_folder(conn, folder_name, languages=None, dry_run=False):
    """处理单个文件夹"""
    if languages is None:
        languages = DEFAULT_LANGUAGES
    
    folder_path = f"{SMB_CONFIG['remote_path']}/{folder_name}"
    
    print(f"\n📁 {folder_name}")
    
    try:
        files = conn.listPath(SMB_CONFIG["share_name"], folder_path)
    except Exception as e:
        print(f"   ❌ 无法读取: {e}")
        return {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
    
    stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
    
    for f in files:
        if f.filename in ['.', '..', '.DS_Store']:
            continue
        
        if f.isDirectory:
            # 递归处理子目录（如 Season 1, Season 2）
            sub_stats = process_folder(conn, f"{folder_name}/{f.filename}", languages, dry_run)
            for k in stats:
                stats[k] += sub_stats[k]
        else:
            # 检查是否是视频文件
            ext = os.path.splitext(f.filename)[1].lower()
            if ext not in VIDEO_EXTS:
                continue
            
            stats["total"] += 1
            
            if dry_run:
                # 只检查
                base_name = os.path.splitext(f.filename)[0]
                if has_subtitle(conn, folder_path, base_name):
                    print(f"   ✅ {f.filename}")
                    stats["skipped"] += 1
                else:
                    print(f"   ❌ {f.filename}")
            else:
                # 下载字幕
                success, status = download_subtitle_for_video(conn, folder_path, f.filename, languages)
                if status == "skipped":
                    stats["skipped"] += 1
                elif status == "downloaded":
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='为 movie 目录下载字幕')
    parser.add_argument('-f', '--folder', help='指定单个文件夹')
    parser.add_argument('-l', '--lang', default='zh,en', help='字幕语言')
    parser.add_argument('--dry-run', action='store_true', help='只检查不下载')
    
    args = parser.parse_args()
    
    languages = args.lang.split(',')
    
    print("========================================")
    print("📝 电影字幕批量下载")
    print("========================================")
    print(f"目标: {SMB_CONFIG['share_name']}/{SMB_CONFIG['remote_path']}")
    print(f"语言: {languages}")
    if args.dry_run:
        print("模式: 干运行 (仅检查)")
    print("")
    
    # 连接 SMB
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\n")
    
    try:
        if args.folder:
            # 处理单个文件夹
            stats = process_folder(conn, args.folder, languages, args.dry_run)
        else:
            # 处理所有文件夹
            root_path = SMB_CONFIG['remote_path']
            files = conn.listPath(SMB_CONFIG["share_name"], root_path)
            
            folders = []
            for f in files:
                if f.filename in ['.', '..']:
                    continue
                if f.isDirectory:
                    folders.append(f.filename)
            
            print(f"发现 {len(folders)} 个电影文件夹\n")
            
            stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
            
            for folder in sorted(folders):
                folder_stats = process_folder(conn, folder, languages, args.dry_run)
                for k in stats:
                    stats[k] += folder_stats[k]
        
        print(f"\n========================================")
        print("📊 统计")
        print("========================================")
        print(f"视频总数: {stats['total']}")
        print(f"已有字幕: {stats['skipped']}")
        if not args.dry_run:
            print(f"下载成功: {stats['downloaded']}")
            print(f"下载失败: {stats['failed']}")
        print("========================================")
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
