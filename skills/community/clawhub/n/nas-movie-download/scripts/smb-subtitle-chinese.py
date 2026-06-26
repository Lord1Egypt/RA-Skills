#!/usr/bin/env python3
"""
SMB 字幕自动下载与上传工具 (中文字幕源)
支持字幕源:
- 字幕库 (Zimuku)
- SubHD
- 射手网 (通过伪射手 API)
"""

from smb.SMBConnection import SMBConnection
import os
import sys
import re
import time
import json
import hashlib
import tempfile
import requests
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

# SMB 配置
SMB_CONFIG = {
    "username": "13917908083",
    "password": "Roger0808",
    "server_name": "Z4ProPlus-X6L8",
    "server_ip": "192.168.1.246",
    "share_name": "super8083",
    "remote_path": "qb/downloads"
}

# 字幕源配置
SUBTITLE_SOURCES = {
    "zimuku": {
        "name": "字幕库",
        "enabled": True,
        "search_url": "https://so.zimuku.org/search",
    },
    "subhd": {
        "name": "SubHD",
        "enabled": True,
        "base_url": "https://subhd.tv",
    }
}

class ChineseSubtitleDownloader:
    """中文字幕下载器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # 禁用 SSL 验证（中文字幕网站证书经常有问题）
        self.session.verify = False
        # 禁用 SSL 警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def search_zimuku(self, query):
        """搜索字幕库"""
        try:
            search_url = f"https://so.zimuku.org/search?q={quote(query)}"
            print(f"   🔍 搜索字幕库: {query}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            # 解析搜索结果 (使用正则简单提取)
            import re
            results = []
            
            # 查找字幕链接
            pattern = r'href="(/detail/\d+\.html)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, response.text)
            
            for match in matches[:5]:  # 只取前5个结果
                link, title = match
                results.append({
                    'source': 'zimuku',
                    'title': title.strip(),
                    'url': f"https://so.zimuku.org{link}",
                    'link': link
                })
            
            return results
            
        except Exception as e:
            print(f"   ⚠️  字幕库搜索失败: {e}")
            return []
    
    def download_zimuku_subtitle(self, detail_url):
        """从字幕库下载字幕"""
        try:
            response = self.session.get(detail_url, timeout=10)
            if response.status_code != 200:
                return None
            
            # 查找下载链接
            import re
            pattern = r'href="(/download/[^"]+)"'
            match = re.search(pattern, response.text)
            
            if match:
                download_url = f"https://so.zimuku.org{match.group(1)}"
                print(f"   📥 下载字幕: {download_url[:60]}...")
                
                dl_response = self.session.get(download_url, timeout=30)
                if dl_response.status_code == 200:
                    return dl_response.content
            
            return None
            
        except Exception as e:
            print(f"   ⚠️  下载失败: {e}")
            return None
    
    def search_subhd(self, query):
        """搜索 SubHD"""
        try:
            # SubHD 搜索需要特殊处理
            search_url = f"https://subhd.tv/search/{quote(query)}"
            print(f"   🔍 搜索 SubHD: {query}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            results = []
            import re
            # 查找字幕链接
            pattern = r'href="(/a/\d+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, response.text)
            
            for match in matches[:5]:
                link, title = match
                results.append({
                    'source': 'subhd',
                    'title': title.strip(),
                    'url': f"https://subhd.tv{link}",
                    'link': link
                })
            
            return results
            
        except Exception as e:
            print(f"   ⚠️  SubHD 搜索失败: {e}")
            return []

class SMBSubtitleManager:
    def __init__(self):
        self.conn = None
        self.video_files = []
        self.temp_dir = tempfile.mkdtemp(prefix="smb_subtitles_")
        self.stats = {"total": 0, "skipped": 0, "downloaded": 0, "failed": 0}
        self.subtitle_downloader = ChineseSubtitleDownloader()
        
    def connect(self):
        self.conn = SMBConnection(
            SMB_CONFIG["username"], SMB_CONFIG["password"],
            "openclaw-client", SMB_CONFIG["server_name"], use_ntlm_v2=True
        )
        print("🔌 连接 SMB...", end=" ")
        connected = self.conn.connect(SMB_CONFIG["server_ip"], 445, timeout=10)
        if connected:
            print("✅")
            return True
        else:
            print("❌")
            return False
    
    def parse_video_info(self, filename):
        """解析视频文件名"""
        # TV Show: ShowName.S01E02.xxx
        tv_match = re.search(r'([^.]+)\.S(\d+)E(\d+)', filename, re.IGNORECASE)
        # Movie: Movie.Name.2023.xxx
        movie_match = re.search(r'^(.+?)\s*(\d{4})', filename)
        
        # 常见美剧中文译名映射
        chinese_names = {
            'young sheldon': ['小谢尔顿', '少年谢尔顿'],
            'sheldon': ['小谢尔顿', '少年谢尔顿'],
            'breaking bad': ['绝命毒师'],
            'game of thrones': ['权力的游戏'],
            'friends': ['老友记', '六人行'],
            'the big bang theory': ['生活大爆炸'],
            'stranger things': ['怪奇物语'],
        }
        
        if tv_match:
            show_name = tv_match.group(1).replace('.', ' ')
            season = int(tv_match.group(2))
            episode = int(tv_match.group(3))
            
            # 生成搜索查询
            queries = [f"{show_name} S{season:02d}E{episode:02d}"]
            
            # 添加中文译名搜索
            show_lower = show_name.lower()
            for eng_name, cn_names in chinese_names.items():
                if eng_name in show_lower:
                    for cn_name in cn_names:
                        queries.append(f"{cn_name} S{season:02d}E{episode:02d}")
                        queries.append(f"{cn_name} 第{season}季 第{episode}集")
            
            return {
                'type': 'tv',
                'title': show_name,
                'season': season,
                'episode': episode,
                'query': queries[0],
                'queries': queries
            }
        elif movie_match:
            movie_name = movie_match.group(1).replace('.', ' ').strip()
            year = movie_match.group(2)
            return {
                'type': 'movie',
                'title': movie_name,
                'year': year,
                'query': f"{movie_name} {year}",
                'queries': [f"{movie_name} {year}"]
            }
        else:
            title = os.path.splitext(filename)[0].replace('.', ' ')
            return {'type': 'unknown', 'title': title, 'query': title, 'queries': [title]}
    
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
                        video_info = self.parse_video_info(f.filename)
                        video_info.update({
                            'filename': f.filename,
                            'remote_path': full_remote_path,
                            'relative_dir': subdir,
                            'size': f.file_size
                        })
                        self.video_files.append(video_info)
        except Exception as e:
            print(f"⚠️ 扫描失败 {path}: {e}")
    
    def check_existing_subtitles(self, video_info):
        base_name = os.path.splitext(video_info['filename'])[0]
        for ext in ['.srt', '.ass', '.vtt', '.ssa']:
            for suffix in ['.zh', '.zh-cn', '.en', '.chs', '']:
                sub_name = f"{base_name}{suffix}{ext}" if suffix else f"{base_name}{ext}"
                sub_path = f"{video_info['relative_dir']}/{sub_name}".strip("/")
                full_path = f"{SMB_CONFIG['remote_path']}/{sub_path}".strip("/")
                try:
                    self.conn.getAttributes(SMB_CONFIG["share_name"], full_path)
                    return True
                except:
                    pass
        return False
    
    def download_subtitles(self, video_info):
        """下载字幕"""
        queries = video_info.get('queries', [video_info['query']])
        
        for query in queries:
            print(f"   🔍 搜索: {query}")
            
            # 尝试字幕库
            results = self.subtitle_downloader.search_zimuku(query)
            
            if results:
                print(f"   ✅ 字幕库找到 {len(results)} 个结果")
                # 下载第一个结果
                subtitle_data = self.subtitle_downloader.download_zimuku_subtitle(results[0]['url'])
                if subtitle_data:
                    return self.process_downloaded_subtitle(subtitle_data, video_info)
            
            # 如果字幕库失败，尝试 SubHD
            results = self.subtitle_downloader.search_subhd(query)
            if results:
                print(f"   ✅ SubHD 找到 {len(results)} 个结果")
                # SubHD 下载逻辑...
                pass
            
            time.sleep(0.5)  # 避免请求过快
        
        return []
    
    def process_downloaded_subtitle(self, data, video_info):
        """处理下载的字幕数据"""
        import zipfile
        import io
        
        downloaded_files = []
        
        try:
            # 尝试解压 ZIP
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                for name in zf.namelist():
                    if name.endswith(('.srt', '.ass', '.ssa', '.vtt')):
                        # 提取字幕文件
                        local_path = os.path.join(self.temp_dir, os.path.basename(name))
                        with open(local_path, 'wb') as f:
                            f.write(zf.read(name))
                        downloaded_files.append(local_path)
        except zipfile.BadZipFile:
            # 如果不是 ZIP，直接保存
            local_path = os.path.join(self.temp_dir, "subtitle.srt")
            with open(local_path, 'wb') as f:
                f.write(data)
            downloaded_files.append(local_path)
        
        return downloaded_files
    
    def upload_subtitle(self, local_sub_path, video_info):
        """上传字幕到 SMB"""
        sub_filename = os.path.basename(local_sub_path)
        # 重命名为与视频匹配的名称
        video_base = os.path.splitext(video_info['filename'])[0]
        sub_ext = os.path.splitext(sub_filename)[1]
        final_name = f"{video_base}.zh{sub_ext}"
        
        remote_path = f"{SMB_CONFIG['remote_path']}/{video_info['relative_dir']}/{final_name}".strip("/")
        
        try:
            with open(local_sub_path, 'rb') as f:
                self.conn.storeFile(SMB_CONFIG["share_name"], remote_path, f)
            return final_name
        except Exception as e:
            print(f"   ⚠️ 上传失败: {e}")
            return None
    
    def process_video(self, video_info):
        self.stats["total"] += 1
        print(f"\\n🎬 [{self.stats['total']}/{len(self.video_files)}] {video_info['filename']}")
        print(f"   📺 识别: {video_info['query']}")
        
        if self.check_existing_subtitles(video_info):
            print("   ⏭️ 已有字幕，跳过")
            self.stats["skipped"] += 1
            return True
        
        subtitle_files = self.download_subtitles(video_info)
        
        if not subtitle_files:
            print("   ❌ 未找到字幕")
            self.stats["failed"] += 1
            return False
        
        print(f"   ✅ 下载了 {len(subtitle_files)} 个字幕文件")
        
        uploaded = 0
        for sub_file in subtitle_files:
            result = self.upload_subtitle(sub_file, video_info)
            if result:
                print(f"   📤 上传: {result}")
                uploaded += 1
            os.remove(sub_file)
        
        if uploaded > 0:
            print("   ✅ 完成")
            self.stats["downloaded"] += 1
            return True
        else:
            print("   ❌ 上传失败")
            self.stats["failed"] += 1
            return False
    
    def process_batch(self, start_idx=0, batch_size=10):
        end_idx = min(start_idx + batch_size, len(self.video_files))
        batch = self.video_files[start_idx:end_idx]
        
        print(f"\\n📦 处理第 {start_idx+1}-{end_idx} 个视频\\n")
        
        for video in batch:
            self.process_video(video)
            time.sleep(1)  # 避免请求过快
        
        return end_idx < len(self.video_files)
    
    def run(self, start_idx=0, batch_size=10):
        print("="*60)
        print("🎥 SMB 字幕下载工具 (中文字幕源)")
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
        
        # 显示内容
        series_groups = {}
        for v in self.video_files:
            title = v.get('title', 'Unknown')
            if title not in series_groups:
                series_groups[title] = []
            series_groups[title].append(v)
        
        print("📋 发现的内容:")
        for title, videos in series_groups.items():
            if videos[0].get('type') == 'tv':
                seasons = set(v.get('season') for v in videos if v.get('season'))
                print(f"   📺 {title} - {len(videos)} 集")
            else:
                print(f"   🎬 {title}")
        print()
        
        # 处理批次
        has_more = self.process_batch(start_idx, batch_size)
        
        print(f"\\n{'='*60}")
        print("📊 统计:")
        print(f"   已处理: {self.stats['total']}")
        print(f"   跳过: {self.stats['skipped']}")
        print(f"   成功: {self.stats['downloaded']}")
        print(f"   失败: {self.stats['failed']}")
        if has_more:
            print(f"\\n📦 还有 {len(self.video_files) - self.stats['total']} 个视频")
            print(f"   继续: python3 {sys.argv[0]} {self.stats['total']}")
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
