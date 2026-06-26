#!/usr/bin/env python3
"""
字幕搜索终极方案 - 基于文件名信息构建搜索
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import re
import subprocess
import tempfile
import shutil

SMB_CONFIG = {
    "username": '13917908083',
    "password": 'Roger0808',
    "server_name": 'Z4ProPlus-X6L8',
    "server_ip": '192.168.1.246',
    "share_name": 'sata11-139XXXX8083',
    "remote_path": 'movie'
}

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

def extract_show_info(filename):
    """从文件名提取剧集信息"""
    # 匹配 SxxEyy 格式
    match = re.search(r'[Ss](\d+)[Ee](\d+)', filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        # 提取剧集名称
        if 'Young.Sheldon' in filename or 'Young Sheldon' in filename:
            return {'show': 'Young Sheldon', 'season': season, 'episode': episode}
        elif 'Community' in filename:
            return {'show': 'Community', 'season': season, 'episode': episode}
    return None

def search_with_clean_name(conn, folder_path, video_filename):
    """使用清理后的文件名搜索"""
    base_name = os.path.splitext(video_filename)[0]
    
    if has_subtitle(conn, folder_path, base_name):
        return True, "skipped"
    
    info = extract_show_info(video_filename)
    if not info:
        return False, "no_info"
    
    print(f"\n   🔍 搜索: {info['show']} S{info['season']:02d}E{info['episode']:02d}")
    
    # 创建临时目录，使用标准命名
    temp_dir = tempfile.mkdtemp()
    
    # 构建标准文件名
    clean_name = f"{info['show'].replace(' ', '.')}.S{info['season']:02d}E{info['episode']:02d}.mkv"
    local_video = os.path.join(temp_dir, clean_name)
    
    downloaded = []
    
    try:
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 尝试更多搜索组合
        search_configs = [
            # 基本搜索
            {'providers': ['opensubtitles', 'opensubtitlescom'], 'langs': ['zh', 'zho', 'chi']},
            # 英文搜索然后翻译
            {'providers': ['opensubtitles', 'addic7ed', 'tvsubtitles'], 'langs': ['en', 'eng']},
            # 全部 provider
            {'providers': ['podnapisi', 'bsplayer', 'gestdown', 'napiprojekt', 'subtitulamos'], 
             'langs': ['zh', 'en', 'zho', 'chi']},
        ]
        
        for config in search_configs:
            for provider in config['providers']:
                for lang in config['langs']:
                    cmd = [
                        'subliminal', 'download', '--force',
                        '-p', provider, '-l', lang,
                        local_video
                    ]
                    
                    try:
                        subprocess.run(cmd, capture_output=True, timeout=30)
                    except:
                        pass
                    
                    # 检查下载结果
                    for root, dirs, files in os.walk(temp_dir):
                        for f in files:
                            if f.endswith(('.srt', '.ass', '.vtt')):
                                full_path = os.path.join(root, f)
                                if full_path not in downloaded:
                                    downloaded.append(full_path)
                                    print(f"      ✅ 找到: {f[:40]} ({provider}/{lang})")
        
        if not downloaded:
            return False, "not_found"
        
        # 使用原始文件名上传字幕
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

def get_missing_videos(conn, folder_path):
    """获取缺字幕的视频列表"""
    missing = []
    try:
        files = conn.listPath(SMB_CONFIG["share_name"], folder_path)
        for f in files:
            if f.filename in ['.', '..']:
                continue
            if any(f.filename.endswith(ext) for ext in ['.mkv', '.mp4', '.avi']):
                base_name = os.path.splitext(f.filename)[0]
                if not has_subtitle(conn, folder_path, base_name):
                    missing.append(f.filename)
    except Exception as e:
        print(f"   错误: {e}")
    return missing

def process_folder(conn, folder_name):
    """处理单个文件夹"""
    folder_path = f"{SMB_CONFIG['remote_path']}/{folder_name}"
    
    print(f"\n{'='*60}")
    print(f"📁 {folder_name}")
    print('='*60)
    
    missing = get_missing_videos(conn, folder_path)
    
    if not missing:
        print("✅ 全部有字幕")
        return {"total": 0, "downloaded": 0, "failed": 0}
    
    print(f"缺字幕: {len(missing)} 个视频\n")
    
    downloaded = 0
    failed = 0
    
    for video in sorted(missing):
        success, status = search_with_clean_name(conn, folder_path, video)
        if status == "skipped":
            pass
        elif status == "downloaded":
            downloaded += 1
        else:
            failed += 1
    
    return {"total": len(missing), "downloaded": downloaded, "failed": failed}

def main():
    print("=" * 70)
    print("📝 字幕搜索 - 标准命名方案")
    print("=" * 70)
    print("")
    
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\n")
    
    # 优先处理 Young Sheldon S05-S07，然后 Community S05-S06
    folders = [
        "Young.Sheldon.S05.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]",
        "Young Sheldon (2017) Season 6 S06 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)",
        "Young Sheldon (2017) Season 7 S07 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)",
        "Community.S01-S06.COMPLETE.SERIES.REPACK.1080p.Bluray.x265-HiQVE/Community.S05.REPACK.1080p.Bluray.x265-HiQVE",
        "Community.S01-S06.COMPLETE.SERIES.REPACK.1080p.Bluray.x265-HiQVE/Community.S06.REPACK.1080p.Bluray.x265-HiQVE",
    ]
    
    total_stats = {"total": 0, "downloaded": 0, "failed": 0}
    
    try:
        for folder in folders:
            stats = process_folder(conn, folder)
            for k in total_stats:
                total_stats[k] += stats[k]
        
        print(f"\n{'='*70}")
        print("📊 统计")
        print('='*70)
        print(f"缺字幕视频: {total_stats['total']}")
        print(f"下载成功: {total_stats['downloaded']}")
        print(f"下载失败: {total_stats['failed']}")
        print('='*70)
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
