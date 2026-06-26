#!/usr/bin/env python3
"""
终极字幕搜索 - 使用所有可用 provider 和高级选项
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import argparse
import tempfile
import subprocess
import shutil
import re

SMB_CONFIG = {
    "username": '13917908083',
    "password": 'Roger0808',
    "server_name": 'Z4ProPlus-X6L8',
    "server_ip": '192.168.1.246',
    "share_name": 'sata11-139XXXX8083',
    "remote_path": 'movie'
}

ALL_LANGUAGES = ['zh', 'zho', 'chi', 'zh-cn', 'zh-tw', 'chs', 'cht', 'en', 'eng']
VIDEO_EXTS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']

def connect_smb():
    conn = SMBConnection(
        SMB_CONFIG["username"], SMB_CONFIG["password"],
        "openclaw-client", SMB_CONFIG["server_name"], use_ntlm_v2=True
    )
    if conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10):
        return conn
    return None

def has_subtitle(conn, folder_path, video_base):
    for ext in ['.srt', '.ass', '.vtt', '.ssa']:
        for lang in ['.zh', '.en', '.chs', '.cht', '.zho', '.eng', '']:
            sub_name = f"{video_base}{lang}{ext}" if lang else f"{video_base}{ext}"
            try:
                conn.getAttributes(SMB_CONFIG["share_name"], f"{folder_path}/{sub_name}")
                return True
            except:
                pass
    return False

def download_with_aggressive_search(conn, folder_path, video_filename):
    """使用所有可用 provider 和高级选项"""
    base_name = os.path.splitext(video_filename)[0]
    
    if has_subtitle(conn, folder_path, base_name):
        return True, "skipped"
    
    print(f"      🔍 [终极搜索] {video_filename[:50]}")
    
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    all_downloaded = []
    
    try:
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 所有 provider 列表
        providers = [
            'opensubtitles', 'opensubtitlescom', 'opensubtitlesvip',
            'podnapisi', 'addic7ed', 'tvsubtitles', 
            'bsplayer', 'gestdown', 'napiprojekt', 'subtitulamos'
        ]
        
        # 尝试不同的语言变体
        lang_variants = [
            ['zh'], ['zho'], ['chi'], ['zh-cn'], ['zh-tw'],
            ['chs'], ['cht'], ['en'], ['eng']
        ]
        
        for provider in providers:
            for langs in lang_variants:
                for lang in langs:
                    cmd = [
                        'subliminal', 'download', '--force',
                        '-p', provider,
                        '-l', lang,
                        '--refiner', 'hash',
                        '--refiner', 'metadata',
                        local_video
                    ]
                    
                    try:
                        result = subprocess.run(cmd, capture_output=True, timeout=45)
                        if result.returncode == 0:
                            # 检查下载结果
                            for root, dirs, files in os.walk(temp_dir):
                                for f in files:
                                    if f.endswith(('.srt', '.ass', '.vtt', '.ssa')):
                                        full_path = os.path.join(root, f)
                                        if full_path not in all_downloaded:
                                            all_downloaded.append(full_path)
                                            print(f"      ✅ 找到字幕: {f[:40]} (via {provider}/{lang})")
                    except subprocess.TimeoutExpired:
                        pass
                    except Exception as e:
                        pass
        
        if not all_downloaded:
            print(f"      ❌ 终极搜索无结果")
            return False, "not_found"
        
        # 上传字幕
        uploaded = 0
        for i, sub_file in enumerate(all_downloaded):
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

def process_folder(conn, folder_name, dry_run=False):
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
            sub_stats = process_folder(conn, f"{folder_name}/{f.filename}", dry_run)
            for k in stats:
                stats[k] += sub_stats[k]
        else:
            ext = os.path.splitext(f.filename)[1].lower()
            if ext not in VIDEO_EXTS:
                continue
            
            stats["total"] += 1
            
            if dry_run:
                base_name = os.path.splitext(f.filename)[0]
                if has_subtitle(conn, folder_path, base_name):
                    stats["skipped"] += 1
                else:
                    print(f"   ❌ {f.filename[:50]}")
            else:
                success, status = download_with_aggressive_search(conn, folder_path, f.filename)
                if status == "skipped":
                    stats["skipped"] += 1
                elif status == "downloaded":
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='终极字幕搜索')
    parser.add_argument('-f', '--folder', help='指定单个文件夹')
    parser.add_argument('--dry-run', action='store_true', help='只检查不下载')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📝 终极字幕搜索 (Ultimate Edition)")
    print("=" * 60)
    print("策略: 所有 provider + 所有语言变体 + hash/metadata 精炼")
    print("")
    
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\n")
    
    try:
        if args.folder:
            stats = process_folder(conn, args.folder, args.dry_run)
        else:
            root_path = SMB_CONFIG['remote_path']
            files = conn.listPath(SMB_CONFIG["share_name"], root_path)
            
            folders = [f.filename for f in files 
                      if f.filename not in ['.', '..'] and f.isDirectory]
            
            print(f"发现 {len(folders)} 个文件夹\n")
            
            stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
            
            for folder in sorted(folders):
                folder_stats = process_folder(conn, folder, args.dry_run)
                for k in stats:
                    stats[k] += folder_stats[k]
        
        print(f"\n" + "=" * 60)
        print("📊 统计")
        print("=" * 60)
        print(f"视频总数: {stats['total']}")
        print(f"已有字幕: {stats['skipped']}")
        if not args.dry_run:
            print(f"下载成功: {stats['downloaded']}")
            print(f"下载失败: {stats['failed']}")
        print("=" * 60)
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
