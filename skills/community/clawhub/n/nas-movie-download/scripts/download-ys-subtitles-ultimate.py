#!/usr/bin/env python3
"""
Young Sheldon 终极字幕搜索 - 多阶段搜索策略
阶段1: subliminal 全源搜索
阶段2: 其他字幕工具
阶段3: 生成手动搜索报告
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import tempfile
import subprocess
import shutil
import json

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

def extract_video_info(filename):
    """从文件名提取信息用于搜索"""
    import re
    # 尝试匹配 SxxEyy 格式
    match = re.search(r'[Ss](\d+)[Ee](\d+)', filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return {'season': season, 'episode': episode, 'show': 'Young Sheldon'}
    return None

def search_subtitle_stage1(conn, folder_path, video_filename):
    """阶段1: subliminal 全源搜索"""
    base_name = os.path.splitext(video_filename)[0]
    
    print(f"\n   🔍 阶段1 - subliminal: {video_filename[:55]}")
    
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    downloaded = []
    
    try:
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        providers = [
            'opensubtitles', 'opensubtitlescom', 'opensubtitlesvip',
            'podnapisi', 'addic7ed', 'tvsubtitles', 
            'bsplayer', 'gestdown', 'napiprojekt', 'subtitulamos'
        ]
        
        for provider in providers:
            for lang in ALL_LANGUAGES:
                cmd = [
                    'subliminal', 'download', '--force',
                    '-p', provider, '-l', lang,
                    '--refiner', 'hash', '--refiner', 'metadata',
                    local_video
                ]
                
                try:
                    subprocess.run(cmd, capture_output=True, timeout=45)
                except:
                    pass
                
                for root, dirs, files in os.walk(temp_dir):
                    for f in files:
                        if f.endswith(('.srt', '.ass', '.vtt')):
                            full_path = os.path.join(root, f)
                            if full_path not in downloaded:
                                downloaded.append(full_path)
                                print(f"      ✅ 找到: {f[:40]} ({provider})")
        
        if downloaded:
            return upload_subtitles(conn, folder_path, base_name, downloaded)
        
        return False, "stage1_failed"
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def search_subtitle_stage2(conn, folder_path, video_filename):
    """阶段2: 尝试其他方式"""
    base_name = os.path.splitext(video_filename)[0]
    
    print(f"\n   🔍 阶段2 - 扩展搜索: {video_filename[:55]}")
    
    # 尝试用 periscope 或其他工具（如果安装了）
    temp_dir = tempfile.mkdtemp()
    local_video = os.path.join(temp_dir, video_filename)
    
    downloaded = []
    
    try:
        with open(local_video, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        # 尝试用不同的语言代码再次搜索
        extra_langs = ['cn', 'tw', 'hk', 'cn-zh', 'zh-hans', 'zh-hant']
        for lang in extra_langs:
            cmd = ['subliminal', 'download', '--force', '-l', lang, local_video]
            try:
                subprocess.run(cmd, capture_output=True, timeout=30)
            except:
                pass
            
            for root, dirs, files in os.walk(temp_dir):
                for f in files:
                    if f.endswith(('.srt', '.ass', '.vtt')):
                        full_path = os.path.join(root, f)
                        if full_path not in downloaded:
                            downloaded.append(full_path)
                            print(f"      ✅ 找到: {f[:40]} (lang: {lang})")
        
        if downloaded:
            return upload_subtitles(conn, folder_path, base_name, downloaded)
        
        return False, "stage2_failed"
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def upload_subtitles(conn, folder_path, base_name, sub_files):
    """上传字幕到 SMB"""
    uploaded = 0
    for i, sub_file in enumerate(sub_files):
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

def get_missing_videos(conn, folder_path):
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

def process_season(conn, folder_name, still_missing):
    """处理单个季"""
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
        # 阶段1
        success, status = search_subtitle_stage1(conn, folder_path, video)
        if success:
            downloaded += 1
            continue
        
        # 阶段2
        success, status = search_subtitle_stage2(conn, folder_path, video)
        if success:
            downloaded += 1
        else:
            failed += 1
            still_missing.append({
                'folder': folder_name,
                'video': video,
                'info': extract_video_info(video)
            })
    
    return {"total": len(missing), "downloaded": downloaded, "failed": failed}

def main():
    print("=" * 70)
    print("📝 Young Sheldon 终极字幕搜索 (多阶段)")
    print("=" * 70)
    print("阶段1: subliminal 全源搜索")
    print("阶段2: 扩展语言代码搜索")
    print("阶段3: 生成手动搜索报告")
    print("=" * 70)
    print("")
    
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功\n")
    
    folders = [
        ("Young.Sheldon.S03.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]", "S03"),
        ("Young.Sheldon.S04.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]", "S04"),
        ("Young.Sheldon.S05.COMPLETE.720p.AMZN.WEBRip.x264-GalaxyTV[TGx]", "S05"),
        ("Young Sheldon (2017) Season 6 S06 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)", "S06"),
        ("Young Sheldon (2017) Season 7 S07 (1080p BluRay x265 HEVC 10bit AAC 5.1 Vyndros)", "S07"),
    ]
    
    total_stats = {"total": 0, "downloaded": 0, "failed": 0}
    still_missing = []
    
    try:
        for folder, season_name in folders:
            stats = process_season(conn, folder, still_missing)
            for k in total_stats:
                total_stats[k] += stats[k]
        
        print(f"\n{'='*70}")
        print("📊 最终统计")
        print('='*70)
        print(f"缺字幕视频: {total_stats['total']}")
        print(f"下载成功: {total_stats['downloaded']}")
        print(f"下载失败: {total_stats['failed']}")
        print('='*70)
        
        # 输出仍需手动搜索的列表
        if still_missing:
            print(f"\n\n{'='*70}")
            print("📝 仍需手动搜索的字幕 (建议去字幕库/SubHD搜索)")
            print('='*70)
            for item in still_missing:
                info = item['info']
                if info:
                    print(f"  - {item['folder']}: {item['video'][:50]}")
                    print(f"    搜索关键词: Young Sheldon S{info['season']:02d}E{info['episode']:02d}")
                else:
                    print(f"  - {item['folder']}: {item['video'][:50]}")
            print('='*70)
    
    finally:
        conn.close()
        print("\n🔌 断开连接")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
