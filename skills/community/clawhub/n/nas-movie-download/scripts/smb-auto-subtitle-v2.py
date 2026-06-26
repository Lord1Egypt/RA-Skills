#!/usr/bin/env python3
"""
SMB 字幕自动下载与上传工具 (文件名搜索模式)
工作流程：
1. 扫描 SMB 共享获取视频文件名
2. 在本地创建同名占位文件
3. 使用 subliminal 按文件名搜索字幕
4. 下载字幕到本地
5. 通过 SMB 上传字幕到对应位置
6. 清理临时文件
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import subprocess
import tempfile
import re
import time
from pathlib import Path
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

# 字幕语言设置
DEFAULT_LANGUAGES = ["zh", "en"]

class SMBSubtitleManager:
    def __init__(self):
        self.conn = None
        self.video_files = []
        self.temp_dir = tempfile.mkdtemp(prefix="smb_subtitles_")
        self.stats = {
            "total": 0,
            "skipped": 0,
            "downloaded": 0,
            "failed": 0
        }
        
    def connect(self):
        """连接 SMB 服务器"""
        self.conn = SMBConnection(
            SMB_CONFIG["username"],
            SMB_CONFIG["password"],
            "openclaw-client",
            SMB_CONFIG["server_name"],
            use_ntlm_v2=True
        )
        
        print(f"🔌 正在连接 SMB 服务器 {SMB_CONFIG['server_ip']}...")
        
        connected = self.conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10)
        
        if connected:
            print("✅ SMB 连接成功!\\n")
            return True
        else:
            print("❌ SMB 连接失败")
            return False
    
    def parse_video_info(self, filename):
        """解析视频文件名提取剧集信息"""
        # TV Show 模式: ShowName.S01E02.xxx
        tv_match = re.search(r'([^.]+)\.S(\d+)E(\d+)', filename, re.IGNORECASE)
        
        # 电影模式: Movie.Name.2023.xxx
        movie_match = re.search(r'^(.+?)\s*(\d{4})', filename)
        
        if tv_match:
            show_name = tv_match.group(1).replace('.', ' ')
            season = int(tv_match.group(2))
            episode = int(tv_match.group(3))
            return {
                'type': 'tv',
                'title': show_name,
                'season': season,
                'episode': episode,
                'query': f"{show_name} S{season:02d}E{episode:02d}"
            }
        elif movie_match:
            movie_name = movie_match.group(1).replace('.', ' ').strip()
            year = movie_match.group(2)
            return {
                'type': 'movie',
                'title': movie_name,
                'year': year,
                'query': f"{movie_name} {year}"
            }
        else:
            title = os.path.splitext(filename)[0].replace('.', ' ')
            return {
                'type': 'unknown',
                'title': title,
                'query': title
            }
    
    def scan_videos(self, subdir=""):
        """递归扫描视频文件"""
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
                        video_info = self.parse_video_info(f.filename)
                        video_info.update({
                            'filename': f.filename,
                            'remote_path': full_remote_path,
                            'relative_dir': subdir,
                            'size': f.file_size
                        })
                        self.video_files.append(video_info)
                        
        except Exception as e:
            print(f"⚠️  扫描目录失败 {path}: {e}")
    
    def check_existing_subtitles(self, video_info):
        """检查是否已存在字幕文件"""
        base_name = os.path.splitext(video_info['filename'])[0]
        subtitle_extensions = ['.srt', '.ass', '.vtt', '.sub']
        existing = []
        
        for ext in subtitle_extensions:
            for lang in ['zh', 'en', 'zh-cn']:
                sub_name = f"{base_name}.{lang}{ext}"
                sub_path = f"{video_info['relative_dir']}/{sub_name}".strip("/")
                full_path = f"{SMB_CONFIG['remote_path']}/{sub_path}".strip("/")
                
                try:
                    self.conn.getAttributes(SMB_CONFIG["share_name"], full_path)
                    existing.append(sub_name)
                except:
                    pass
            
            # 检查没有语言代码的字幕
            sub_name = f"{base_name}{ext}"
            sub_path = f"{video_info['relative_dir']}/{sub_name}".strip("/")
            full_path = f"{SMB_CONFIG['remote_path']}/{sub_path}".strip("/")
            
            try:
                self.conn.getAttributes(SMB_CONFIG["share_name"], full_path)
                existing.append(sub_name)
            except:
                pass
        
        return existing
    
    def create_local_placeholder(self, video_info):
        """在本地创建同名占位文件"""
        # 创建对应的目录结构
        local_dir = os.path.join(self.temp_dir, video_info['relative_dir'])
        os.makedirs(local_dir, exist_ok=True)
        
        local_path = os.path.join(local_dir, video_info['filename'])
        
        # 创建一个小的占位文件（subiminal 需要实际文件存在）
        # 创建 1KB 的空文件
        with open(local_path, 'wb') as f:
            f.write(b'\x00' * 1024)
        
        return local_path
    
    def download_subtitles_with_subliminal(self, video_path):
        """使用 subliminal 按文件名搜索并下载字幕"""
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        
        # 构建 subliminal 命令
        # --force: 强制下载，即使已有字幕
        # --verbose: 显示详细信息
        lang_args = []
        for lang in DEFAULT_LANGUAGES:
            lang_args.extend(['-l', lang])
        
        cmd = ['subliminal', 'download', '--force'] + lang_args + [video_path]
        
        print(f"   🔍 搜索字幕: subliminal download {' '.join(lang_args)} {video_name}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # 检查字幕是否下载成功
            base_name = os.path.splitext(video_name)[0]
            downloaded = []
            
            # 检查各种可能的字幕文件名格式
            for ext in ['.srt', '.ass', '.vtt']:
                # 格式: video.zh.srt
                for lang in ['zh', 'en', 'zho', 'eng']:
                    sub_file = os.path.join(video_dir, f"{base_name}.{lang}{ext}")
                    if os.path.exists(sub_file):
                        downloaded.append(sub_file)
                
                # 格式: video.srt (没有语言代码)
                sub_file_simple = os.path.join(video_dir, f"{base_name}{ext}")
                if os.path.exists(sub_file_simple) and sub_file_simple not in downloaded:
                    downloaded.append(sub_file_simple)
            
            if downloaded:
                print(f"   ✅ 找到 {len(downloaded)} 个字幕")
            else:
                print(f"   ❌ 未找到字幕")
                if result.stderr:
                    print(f"   ℹ️  subliminal: {result.stderr[:200]}")
            
            return downloaded
            
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  subliminal 超时")
            return []
        except Exception as e:
            print(f"   ⚠️  subliminal 错误: {e}")
            return []
    
    def upload_subtitle_to_smb(self, local_sub_path, video_info):
        """上传字幕到 SMB"""
        sub_filename = os.path.basename(local_sub_path)
        
        remote_path = f"{SMB_CONFIG['remote_path']}/{video_info['relative_dir']}/{sub_filename}".strip("/")
        
        try:
            with open(local_sub_path, 'rb') as f:
                self.conn.storeFile(SMB_CONFIG["share_name"], remote_path, f)
            return sub_filename
            
        except Exception as e:
            print(f"   ⚠️  上传失败: {e}")
            return None
    
    def process_video(self, video_info):
        """处理单个视频文件"""
        self.stats["total"] += 1
        current = self.stats["total"]
        total = len(self.video_files)
        
        print(f"\\n🎬 [{current}/{total}] {video_info['filename']}")
        print(f"   📺 识别: {video_info['query']}")
        
        # 检查现有字幕
        existing = self.check_existing_subtitles(video_info)
        if existing:
            print(f"   ⏭️  已存在字幕，跳过")
            self.stats["skipped"] += 1
            return True
        
        # 创建本地占位文件
        print(f"   📝 创建占位文件...")
        local_video = self.create_local_placeholder(video_info)
        
        # 使用 subliminal 下载字幕
        subtitle_files = self.download_subtitles_with_subliminal(local_video)
        
        if not subtitle_files:
            print(f"   ❌ 未找到字幕")
            self.stats["failed"] += 1
            # 清理
            os.remove(local_video)
            return False
        
        # 上传字幕到 SMB
        uploaded = []
        for sub_file in subtitle_files:
            result = self.upload_subtitle_to_smb(sub_file, video_info)
            if result:
                uploaded.append(result)
                print(f"   📤 上传: {result}")
        
        # 清理本地文件
        os.remove(local_video)
        for sub_file in subtitle_files:
            if os.path.exists(sub_file):
                os.remove(sub_file)
        
        if uploaded:
            print(f"   ✅ 成功上传 {len(uploaded)} 个字幕")
            self.stats["downloaded"] += 1
            return True
        else:
            print(f"   ❌ 字幕上传失败")
            self.stats["failed"] += 1
            return False
    
    def process_all(self):
        """处理所有视频文件"""
        print("="*60)
        print("🎥 SMB 字幕自动下载工具 (文件名搜索模式)")
        print("="*60)
        print(f"\\n📡 服务器: {SMB_CONFIG['server_ip']}")
        print(f"📁 共享: {SMB_CONFIG['share_name']}")
        print(f"📂 路径: {SMB_CONFIG['remote_path']}")
        print(f"🌐 字幕语言: {', '.join(DEFAULT_LANGUAGES)}")
        print(f"📁 临时目录: {self.temp_dir}")
        print()
        
        # 连接 SMB
        if not self.connect():
            return False
        
        # 扫描视频文件
        print("🔍 正在扫描视频文件...")
        self.scan_videos()
        
        print(f"\\n📊 找到 {len(self.video_files)} 个视频文件\\n")
        
        if not self.video_files:
            print("❌ 没有找到视频文件")
            self.conn.close()
            return False
        
        # 按剧集分组显示
        series_groups = {}
        for v in self.video_files:
            title = v.get('title', 'Unknown')
            if title not in series_groups:
                series_groups[title] = []
            series_groups[title].append(v)
        
        print("📋 发现的内容:")
        for title, videos in series_groups.items():
            if videos[0].get('type') == 'tv' and videos[0].get('season'):
                seasons = set(v.get('season') for v in videos if v.get('season'))
                print(f"   📺 {title} - {len(videos)} 集 (季: {', '.join(map(str, sorted(seasons)))})")
            else:
                print(f"   🎬 {title} - {len(videos)} 个文件")
        print()
        
        # 确认是否继续
        print(f"将为 {len(self.video_files)} 个视频下载字幕")
        print("开始处理...\\n")
        
        # 处理每个视频
        for video in self.video_files:
            self.process_video(video)
            # 添加小延迟避免请求过快
            time.sleep(0.5)
        
        # 显示统计
        print(f"\\n{'='*60}")
        print("📊 处理完成!")
        print(f"   总计: {self.stats['total']} 个视频")
        print(f"   ⏭️  跳过 (已有字幕): {self.stats['skipped']}")
        print(f"   ✅ 下载成功: {self.stats['downloaded']}")
        print(f"   ❌ 失败: {self.stats['failed']}")
        print(f"{'='*60}")
        
        # 清理临时目录
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
        self.conn.close()
        print("\\n🔌 SMB 连接已关闭")
        return True

def main():
    manager = SMBSubtitleManager()
    success = manager.process_all()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
