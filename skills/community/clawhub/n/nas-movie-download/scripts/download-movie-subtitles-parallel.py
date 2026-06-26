#!/usr/bin/env python3
"""
并行批量下载 movie 目录中的字幕
同时处理多个视频，大大加快速度
"""
from smb.SMBConnection import SMBConnection
import os
import sys
import argparse
import tempfile
import subprocess
import shutil
import concurrent.futures
import threading

# SMB 配置 - 机械硬盘
SMB_CONFIG = {
    "username": '13917908083',
    "password": 'Roger0808',
    "server_name": 'Z4ProPlus-X6L8',
    "server_ip": '192.168.1.246',
    "share_name": 'sata11-139XXXX8083',
    "remote_path": 'movie'
}

DEFAULT_LANGUAGES = ['zh', 'zh-cn', 'zh-tw', 'chs', 'cht']
VIDEO_EXTS = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
MAX_WORKERS = 5  # 并行线程数

# 线程锁，用于保护 SMB 连接
smb_lock = threading.Lock()

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

def download_subtitle_for_video(video_info, languages=None):
    """为单个视频下载字幕（在线程中运行）"""
    if languages is None:
        languages = DEFAULT_LANGUAGES
    
    folder_path, video_filename = video_info
    base_name = os.path.splitext(video_filename)[0]
    
    # 每个线程使用独立的 SMB 连接
    conn = connect_smb()
    if not conn:
        return False, video_filename, "SMB连接失败"
    
    try:
        # 再次检查是否已有字幕（可能其他线程已下载）
        if has_subtitle(conn, folder_path, base_name):
            return True, video_filename, "已有字幕"
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        local_video = os.path.join(temp_dir, video_filename)
        
        try:
            # 创建占位文件
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
                sub_file = os.path.join(temp_dir, f"{base_name}{ext}")
                if os.path.exists(sub_file) and sub_file not in downloaded:
                    downloaded.append(sub_file)
            
            if not downloaded:
                return False, video_filename, "未找到字幕"
            
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
                uploaded += 1
            
            return True, video_filename, f"下载了 {uploaded} 个字幕"
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    except subprocess.TimeoutExpired:
        return False, video_filename, "超时"
    except Exception as e:
        return False, video_filename, f"错误: {e}"
    finally:
        conn.close()

def collect_videos(conn, folder_name="", max_depth=3, current_depth=0):
    """收集所有需要下载字幕的视频"""
    if current_depth > max_depth:
        return []
    
    folder_path = f"{SMB_CONFIG['remote_path']}/{folder_name}".strip("/")
    videos = []
    
    try:
        files = conn.listPath(SMB_CONFIG["share_name"], folder_path)
    except Exception as e:
        return []
    
    for f in files:
        if f.filename in ['.', '..', '.DS_Store']:
            continue
        
        relative_path = f"{folder_name}/{f.filename}".strip("/") if folder_name else f.filename
        
        if f.isDirectory:
            # 递归收集子目录
            sub_videos = collect_videos(conn, relative_path, max_depth, current_depth + 1)
            videos.extend(sub_videos)
        else:
            # 检查是否是视频文件
            ext = os.path.splitext(f.filename)[1].lower()
            if ext in VIDEO_EXTS:
                base_name = os.path.splitext(f.filename)[0]
                if not has_subtitle(conn, folder_path, base_name):
                    videos.append((folder_path, f.filename))
    
    return videos

def main():
    parser = argparse.ArgumentParser(description='并行下载 movie 目录字幕')
    parser.add_argument('-w', '--workers', type=int, default=MAX_WORKERS, 
                        help=f'并行线程数 (默认: {MAX_WORKERS})')
    parser.add_argument('-l', '--lang', default='zh,en', help='字幕语言')
    parser.add_argument('--dry-run', action='store_true', help='只检查不下载')
    
    args = parser.parse_args()
    
    languages = args.lang.split(',')
    
    print("="*60)
    print("🚀 并行字幕批量下载")
    print("="*60)
    print(f"目标: {SMB_CONFIG['share_name']}/{SMB_CONFIG['remote_path']}")
    print(f"语言: {languages}")
    print(f"并行数: {args.workers}")
    print("")
    
    # 连接 SMB 收集视频列表
    conn = connect_smb()
    if not conn:
        print("❌ SMB 连接失败")
        return 1
    
    print("✅ SMB 连接成功")
    print("📁 扫描视频文件...")
    
    videos = collect_videos(conn, "")
    conn.close()
    
    print(f"\n找到 {len(videos)} 个需要字幕的视频\n")
    
    if not videos:
        print("✅ 所有视频已有字幕！")
        return 0
    
    if args.dry_run:
        print("🔍 干运行模式 - 需要字幕的视频:")
        for folder, name in videos[:20]:
            print(f"   - {name}")
        if len(videos) > 20:
            print(f"   ... 还有 {len(videos) - 20} 个")
        return 0
    
    # 并行下载字幕
    success_count = 0
    fail_count = 0
    skipped_count = 0
    
    print(f"🎬 开始并行下载 ({args.workers} 线程)...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        # 提交所有任务
        future_to_video = {
            executor.submit(download_subtitle_for_video, video, languages): video 
            for video in videos
        }
        
        # 处理结果
        for i, future in enumerate(concurrent.futures.as_completed(future_to_video), 1):
            video = future_to_video[future]
            try:
                success, filename, msg = future.result()
                print(f"[{i}/{len(videos)}] {filename}")
                if success:
                    if msg == "已有字幕":
                        print(f"   ⏭️  {msg}")
                        skipped_count += 1
                    else:
                        print(f"   ✅ {msg}")
                        success_count += 1
                else:
                    print(f"   ❌ {msg}")
                    fail_count += 1
            except Exception as e:
                print(f"   ❌ 异常: {e}")
                fail_count += 1
    
    print(f"\n{'='*60}")
    print("📊 统计")
    print("="*60)
    print(f"视频总数: {len(videos)}")
    print(f"下载成功: {success_count}")
    print(f"已有字幕: {skipped_count}")
    print(f"下载失败: {fail_count}")
    print("="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
