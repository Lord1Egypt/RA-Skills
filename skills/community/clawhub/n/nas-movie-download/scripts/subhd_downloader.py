#!/usr/bin/env python3
"""
SubHD 字幕下载模块
作为 OpenSubtitles 的替补方案
"""
import requests
import re
import os
import tempfile
from urllib.parse import quote, urljoin
from io import BytesIO

SUBHD_BASE_URL = "https://subhd.tv"

class SubHDDownloader:
    """SubHD 字幕下载器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def search(self, query):
        """搜索字幕"""
        try:
            search_url = f"{SUBHD_BASE_URL}/search/{quote(query)}"
            print(f"    🔍 SubHD 搜索: {query}")
            
            response = self.session.get(search_url, timeout=30)
            response.raise_for_status()
            
            # 解析搜索结果
            html = response.text
            
            # 提取字幕链接 /sub/xxxx
            sub_links = re.findall(r'href="(/sub/\d+)"', html)
            
            results = []
            for link in set(sub_links[:10]):  # 最多10个结果
                sub_url = urljoin(SUBHD_BASE_URL, link)
                sub_info = self._parse_subtitle_page(sub_url)
                if sub_info:
                    results.append(sub_info)
            
            return results
            
        except Exception as e:
            print(f"    ❌ SubHD 搜索失败: {e}")
            return []
    
    def _parse_subtitle_page(self, sub_url):
        """解析字幕详情页"""
        try:
            response = self.session.get(sub_url, timeout=30)
            html = response.text
            
            # 提取标题
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            title = title_match.group(1).strip() if title_match else "Unknown"
            title = re.sub(r'<[^>]+>', '', title)  # 去除HTML标签
            
            # 提取下载链接
            download_match = re.search(r'href="(/sub/\d+/download)"', html)
            if download_match:
                download_url = urljoin(SUBHD_BASE_URL, download_match.group(1))
                return {
                    'title': title,
                    'url': sub_url,
                    'download_url': download_url
                }
            
            return None
            
        except Exception as e:
            print(f"    ⚠️ 解析字幕页失败: {e}")
            return None
    
    def download(self, download_url, output_path):
        """下载字幕文件"""
        try:
            print(f"    📥 下载字幕: {download_url}")
            
            response = self.session.get(download_url, timeout=60)
            response.raise_for_status()
            
            # SubHD 返回的是压缩包（zip/rar）或字幕文件
            content_type = response.headers.get('Content-Type', '')
            
            # 保存到临时文件
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"    ✅ 下载完成: {len(response.content)} bytes")
            return True
            
        except Exception as e:
            print(f"    ❌ 下载失败: {e}")
            return False
    
    def download_subtitle_for_video(self, video_filename, languages=['zh']):
        """
        为视频文件下载字幕
        返回: (success: bool, subtitle_path: str or None)
        """
        # 解析视频信息
        match = re.search(r'(.*?)\.S(\d+)E(\d+)', video_filename, re.IGNORECASE)
        if not match:
            print(f"    ⚠️ 无法解析视频文件名: {video_filename}")
            return False, None
        
        show_name = match.group(1).replace('.', ' ')
        season = match.group(2)
        episode = match.group(3)
        
        # 构建搜索查询
        query = f"{show_name} S{season}E{episode}"
        
        # 搜索字幕
        results = self.search(query)
        
        if not results:
            print(f"    ❌ SubHD 未找到字幕")
            return False, None
        
        print(f"    📋 找到 {len(results)} 个字幕")
        
        # 下载第一个结果
        for result in results[:3]:  # 尝试前3个
            print(f"    📝 尝试: {result['title'][:50]}")
            
            # 创建临时文件
            temp_file = tempfile.mktemp(suffix='.zip')
            
            if self.download(result['download_url'], temp_file):
                # 这里可以添加解压逻辑
                # 暂时返回成功，实际使用时需要解压并提取 .srt 文件
                return True, temp_file
        
        return False, None


def download_from_subhd_fallback(video_filename, languages=['zh']):
    """
    便捷的备用下载函数
    当 OpenSubtitles 失败时调用
    """
    downloader = SubHDDownloader()
    return downloader.download_subtitle_for_video(video_filename, languages)


if __name__ == '__main__':
    # 测试
    print("🧪 测试 SubHD 下载器")
    print("="*60)
    
    test_files = [
        "Young.Sheldon.S06E01.1080p.BluRay.x265.HEVC.mkv",
        "Young.Sheldon.S07E01.1080p.BluRay.x265.HEVC.mkv",
    ]
    
    for test_file in test_files:
        print(f"\n🎬 {test_file}")
        success, path = download_from_subhd_fallback(test_file)
        if success:
            print(f"   ✅ 下载成功: {path}")
        else:
            print(f"   ❌ 下载失败")
    
    print("\n" + "="*60)
