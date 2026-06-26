#!/usr/bin/env python3
"""
增强版字幕搜索 - 使用所有可用字幕源
Usage:
    python3 download-movie-subtitles-advanced.py              # 全源搜索
    python3 download-movie-subtitles-advanced.py -f "Folder"  # 指定文件夹
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
    "share_name": 'sata11-139XXXX8083',
    "remote_path": 'movie'
}

# 更多语言代码
ALL_LANGUAGES = ['zh', 'zh-cn', 'zh-tw', 'zho', 'chi', 'chs', 'cht', 'en', 'eng']
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
        for lang in ['.zh', '.en', '.chs', '.cht', '.zho', '.eng', '']:
            sub_name = f"{video_base}{lang}{ext}" if lang else f"{video_base}{ext}"
            try:
                conn.getAttributes(SMB_CONFIG["share_name"], f"{folder_path}/{sub_name}")
                return True
            except:
                pass
    return False

def download_with_all_providers(conn, folder_path, video_filename):
    """使用所有可用 provider 搜索字幕"""
    base_name = os.path.splitext(video_filename)[0]
    
    if has_subtitle(conn, folder_path, base_name):
        print(f"      ⏭️  已有字幕: {video_filename}")
        return True, "skipped"
    
    print(f"      🔍 [全源搜索] {video_filename}")
    
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    all_downloaded = []
    
    try:
        # 创建占位文件
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 所有 provider
        providers = ['opensubtitles', 'opensubtitlescom', 'podnapisi', 
                     'addic7ed', 'tvsubtitles', 'bsplayer', 'gestdown', 
                     'napiprojekt', 'subtitulamos']
        
        for provider in providers:
            for lang in ALL_LANGUAGES:
                cmd = [
                    'subliminal', 'download', '--force',
                    '-p', provider,
                    '-l', lang,
                    local_video
                ]
                
                try:
                    subprocess.run(cmd, capture_output=True, timeout=30)
                except:
                    pass
                
                # 检查是否下载了字幕
                for ext in ['.srt', '.ass', '.vtt', '.ssa']:
                    for suffix in ['.zh', '.zho', '.chi', '.en', '.eng', '.chs', '.cht', '']:
                        sub_file = os.path.join(temp_dir, f"{base_name}{suffix}{ext}")
                        if os.path.exists(sub_file) and sub_file not in all_downloaded:
                            all_downloaded.append(sub_file)
                            print(f"      ✅ 找到: {os.path.basename(sub_file)} (via {provider})")
        
        if not all_downloaded:
            print(f"      ❌ 全源搜索无结果")
            return False, "not_found"
        
        # 上传字幕到 SMB
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
    """处理单个文件夹"""
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
                    print(f"   ✅ {f.filename}")
                    stats["skipped"] += 1
                else:
                    print(f"   ❌ {f.filename}")
            else:
                success, status = download_with_all_providers(conn, folder_path, f.filename)
                if status == "skipped":
                    stats["skipped"] += 1
                elif status == "downloaded":
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='全源字幕搜索')
    parser.add_argument('-f', '--folder', help='指定单个文件夹')
    parser.add_argument('--dry-run', action='store_true', help='只检查不下载')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("📝 全源字幕搜索 (Advanced)")
    print("=" * 50)
    print(f"目标: {SMB_CONFIG['share_name']}/{SMB_CONFIG['remote_path']}")
    print(f"字幕源: opensubtitles, podnapisi, addic7ed, tvsubtitles...")
    print(f"语言: {', '.join(ALL_LANGUAGES)}")
    if args.dry_run:
        print("模式: 干运行 (仅检查)")
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
            
            print(f"发现 {len(folders)} 个电影文件夹\n")
            
            stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
            
            for folder in sorted(folders):
                folder_stats = process_folder(conn, folder, args.dry_run)
                for k in stats:
                    stats[k] += folder_stats[k]
        
        print(f"\n" + "=" * 50)
        print("📊 统计")
        print("=" * 50)
        print(f"视频总数: {stats['total']}")
        print(f"已有字幕: {stats['skipped']}")
        if not args.dry_run:
            print(f"下载成功: {stats['downloaded']}")
            print(f"下载失败: {stats['failed']}")
        print("=" * 50)
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
