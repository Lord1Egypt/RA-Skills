#!/usr/bin/env python3
"""
SMB 字幕自动下载与上传工具 (简化版 - 分批处理)
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import subprocess
import tempfile
import re
import time
from io import BytesIO

# SMB 配置
SMB_CONFIG = {
    "username": "13917908083",
    "password": "Roger0808",
    "server_name": "Z4ProPlus-X6L8",
    "server_ip": "192.168.1.246",
    "share_name": "super8083",
    "remote_path": "qb/downloads"
}

DEFAULT_LANGUAGES = ["zh", "en"]

class SMBSubtitleManager:
    def __init__(self):
        self.conn = None
        self.video_files = []
        self.temp_dir = tempfile.mkdtemp(prefix="smb_subtitles_")
        self.stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
        
    def connect(self):
        self.conn = SMBConnection(
            SMB_CONFIG["username"], SMB_CONFIG["password"],
            "openclaw-client", SMB_CONFIG["server_name"], use_ntlm_v2=True
        )
        sys.stdout.write("🔌 连接 SMB...")
        sys.stdout.flush()
        connected = self.conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10)
        if connected:
            print(" ✅")
            return True
        else:
            print(" ❌")
            return False
    
    def scan_videos(self, subdir=""):
        path = f"{SMB_CONFIG['remote_path']}/{subdir}".strip("/")
        try:
            files = self.conn.listPath(SMB_CONFIG["share_name"], path)
            for f in files:
                if f.filename in ['.', '..', '.DS_Store']:
                    continue
                relative_path = f"{subdir}/{f.filename}".strip("/") if subdir else f.filename
                full_remote_path = f"{path}/{f.filename}".strip("/")
                
                if f.isDirectory:
                    self.scan_videos(relative_path)
                else:
                    video_exts = ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
                    if any(f.filename.lower().endswith(ext) for ext in video_exts):
                        self.video_files.append({
                            'filename': f.filename,
                            'remote_path': full_remote_path,
                            'relative_dir': subdir,
                            'size': f.file_size
                        })
        except Exception as e:
            print(f"⚠️ 扫描失败 {path}: {e}")
    
    def check_existing_subtitles(self, video_info):
        base_name = os.path.splitext(video_info['filename'])[0]
        for ext in ['.srt', '.ass', '.vtt']:
            for lang in ['zh', 'en', 'zh-cn', '']:
                sub_name = f"{base_name}.{lang}{ext}" if lang else f"{base_name}{ext}"
                sub_path = f"{video_info['relative_dir']}/{sub_name}".strip("/")
                full_path = f"{SMB_CONFIG['remote_path']}/{sub_path}".strip("/")
                try:
                    self.conn.getAttributes(SMB_CONFIG["share_name"], full_path)
                    return True
                except:
                    pass
        return False
    
    def create_placeholder(self, video_info):
        local_dir = os.path.join(self.temp_dir, video_info['relative_dir'])
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, video_info['filename'])
        with open(local_path, 'wb') as f:
            f.write(b'\x00' * 1024)
        return local_path
    
    def download_subtitles(self, video_path):
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        base_name = os.path.splitext(video_name)[0]
        
        cmd = ['subliminal', 'download', '--force', '-l', 'zh', '-l', 'en', video_path]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            downloaded = []
            for ext in ['.srt', '.ass', '.vtt']:
                for lang in ['zh', 'en', 'zho', 'eng']:
                    sub_file = os.path.join(video_dir, f"{base_name}.{lang}{ext}")
                    if os.path.exists(sub_file):
                        downloaded.append(sub_file)
                sub_file_simple = os.path.join(video_dir, f"{base_name}{ext}")
                if os.path.exists(sub_file_simple) and sub_file_simple not in downloaded:
                    downloaded.append(sub_file_simple)
            return downloaded
        except:
            return []
    
    def upload_subtitle(self, local_sub_path, video_info):
        sub_filename = os.path.basename(local_sub_path)
        remote_path = f"{SMB_CONFIG['remote_path']}/{video_info['relative_dir']}/{sub_filename}".strip("/")
        try:
            with open(local_sub_path, 'rb') as f:
                self.conn.storeFile(SMB_CONFIG["share_name"], remote_path, f)
            return True
        except:
            return False
    
    def process_video(self, video_info):
        self.stats["total"] += 1
        print(f"\\n🎬 [{self.stats['total']}] {video_info['filename']}")
        
        if self.check_existing_subtitles(video_info):
            print("   ⏭️  已有字幕，跳过")
            self.stats["skipped"] += 1
            return True
        
        print("   📝 创建占位文件...")
        local_video = self.create_placeholder(video_info)
        
        print("   🔍 搜索字幕...")
        subtitle_files = self.download_subtitles(local_video)
        
        if not subtitle_files:
            print("   ❌ 未找到字幕")
            self.stats["failed"] += 1
            os.remove(local_video)
            return False
        
        print(f"   ✅ 找到 {len(subtitle_files)} 个字幕")
        
        uploaded = 0
        for sub_file in subtitle_files:
            if self.upload_subtitle(sub_file, video_info):
                print(f"   📤 上传: {os.path.basename(sub_file)}")
                uploaded += 1
            os.remove(sub_file)
        
        os.remove(local_video)
        
        if uploaded > 0:
            print(f"   ✅ 完成")
            self.stats["downloaded"] += 1
            return True
        else:
            print("   ❌ 上传失败")
            self.stats["failed"] += 1
            return False
    
    def process_batch(self, start_idx=0, batch_size=10):
        """处理一批视频"""
        end_idx = min(start_idx + batch_size, len(self.video_files))
        batch = self.video_files[start_idx:end_idx]
        
        print(f"\\n📦 处理第 {start_idx+1}-{end_idx} 个视频 (共 {len(self.video_files)} 个)")
        
        for video in batch:
            self.process_video(video)
            time.sleep(0.5)
        
        return end_idx < len(self.video_files)
    
    def run(self, start_idx=0, batch_size=10):
        print("="*60)
        print("🎥 SMB 字幕下载工具")
        print("="*60)
        
        if not self.connect():
            return False
        
        print("🔍 扫描视频文件...")
        self.scan_videos()
        print(f"✅ 找到 {len(self.video_files)} 个视频\\n")
        
        if not self.video_files:
            print("❌ 没有找到视频")
            self.conn.close()
            return False
        
        # 处理指定批次
        has_more = self.process_batch(start_idx, batch_size)
        
        # 显示统计
        print(f"\\n{'='*60}")
        print("📊 当前统计:")
        print(f"   已处理: {self.stats['total']}")
        print(f"   跳过: {self.stats['skipped']}")
        print(f"   成功: {self.stats['downloaded']}")
        print(f"   失败: {self.stats['failed']}")
        if has_more:
            print(f"\\n📦 还有 {len(self.video_files) - self.stats['total']} 个视频待处理")
            print(f"   下次运行: python3 {sys.argv[0]} {self.stats['total']}")
        print(f"{'='*60}")
        
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        self.conn.close()
        print("\\n🔌 SMB 连接已关闭")
        return True

def main():
    start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    manager = SMBSubtitleManager()
    return 0 if manager.run(start_idx, batch_size) else 1

if __name__ == "__main__":
    sys.exit(main())
