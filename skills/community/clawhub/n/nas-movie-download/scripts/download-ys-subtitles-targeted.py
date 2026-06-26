#!/usr/bin/env python3
"""
针对性字幕搜索 - 只搜索缺字幕的视频
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import tempfile
import subprocess
import shutil

SMB_CONFIG = {
    "username": '13917908083',
    "password": 'Roger0808',
    "server_name": 'Z4ProPlus-X6L8',
    "server_ip": '192.168.1.246',
    "share_name": 'sata11-139XXXX8083',
    "remote_path": 'movie'
}

ALL_LANGUAGES = ['zh', 'zho', 'chi', 'zh-cn', 'zh-tw', 'chs', 'cht', 'en', 'eng']
VIDEO_EXTS = ['.mkv', '.mp4', '.avi', '.mov']

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

def get_missing_subtitles(conn, folder_path):
    """获取缺字幕的视频列表"""
    missing = []
    try:
        files = conn.listPath(SMB_CONFIG["share_name"], folder_path)
        for f in files:
            if f.filename in ['.', '..']:
                continue
            if any(f.filename.endswith(ext) for ext in VIDEO_EXTS):
                base_name = os.path.splitext(f.filename)[0]
                if not has_subtitle(conn, folder_path, base_name):
                    missing.append(f.filename)
    except Exception as e:
        print(f"   错误: {e}")
    return missing

def download_with_all_providers(conn, folder_path, video_filename):
    """使用所有 provider 搜索字幕"""
    base_name = os.path.splitext(video_filename)[0]
    
    print(f"      🔍 搜索: {video_filename[:60]}")
    
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    all_downloaded = []
    
    try:
        # 创建占位文件
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 所有 provider
        providers = [
            'opensubtitles', 'opensubtitlescom', 'opensubtitlesvip',
            'podnapisi', 'addic7ed', 'tvsubtitles', 
            'bsplayer', 'gestdown', 'napiprojekt', 'subtitulamos'
        ]
        
        for provider in providers:
            for lang in ALL_LANGUAGES:
                cmd = [
                    'subliminal', 'download', '--force',
                    '-p', provider,
                    '-l', lang,
                    '--refiner', 'hash',
                    '--refiner', 'metadata',
                    local_video
                ]
                
                try:
                    subprocess.run(cmd, capture_output=True, timeout=60)
                except:
                    pass
                
                # 检查是否下载了字幕
                for root, dirs, files in os.walk(temp_dir):
                    for f in files:
                        if f.endswith(('.srt', '.ass', '.vtt')):
                            full_path = os.path.join(root, f)
                            if full_path not in all_downloaded:
                                all_downloaded.append(full_path)
                                print(f"      ✅ 找到: {f[:40]} ({provider})")
        
        if not all_downloaded:
            print(f"      ❌ 未找到")
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

def process_season(conn, folder_name):
    """处理单个季"""
    folder_path = f"{SMB_CONFIG['remote_path']}/{folder_name}"
    
    print(f"\n📁 {folder_name}")
    
    # 获取缺字幕的视频列表
    missing = get_missing_subtitles(conn, folder_path)
    
    if not missing:
        print("   ✅ 全部有字幕")
        return {"total": 0, "downloaded": 0, "failed": 0}
    
    print(f"   缺字幕: {len(missing)} 个视频")
    
    downloaded = 0
    failed = 0
    
    for video in sorted(missing):
        success, status = download_with_all_providers(conn, folder_path, video)
        if status == "downloaded":
            downloaded += 1
        else:
            failed += 1
    
    return {"total": len(missing), "downloaded": downloaded, "failed": failed}

def main():
    print("=" * 60)
    print("📝 Young Sheldon S03-S07 针对性字幕搜索")
    print("=" * 60)
    print("")
    
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\n")
    
    folders = [
        "Young.Sheldon.S03.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
        "Young.Sheldon.S04.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
        "Young.Sheldon.S05.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
        "Young Sheldon (2017) Season 6 S06 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)",
        "Young Sheldon (2017) Season 7 S07 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)"
    ]
    
    total_stats = {"total": 0, "downloaded": 0, "failed": 0}
    
    try:
        for folder in folders:
            stats = process_season(conn, folder)
            for k in total_stats:
                total_stats[k] += stats[k]
        
        print(f"\n" + "=" * 60)
        print("📊 统计")
        print("=" * 60)
        print(f"缺字幕视频: {total_stats['total']}")
        print(f"下载成功: {total_stats['downloaded']}")
        print(f"下载失败: {total_stats['failed']}")
        print("=" * 60)
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
