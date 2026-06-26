import os
import json
import re
import time
import subprocess
from datetime import datetime
from urllib.parse import urlparse

class VideoDownloader:
    """通用视频下载器 - 支持多平台"""
    
    def __init__(self, save_path):
        self.save_path = save_path
        self.yt_dlp_available = self._check_yt_dlp()
        self.drission_available = self._check_drission()
        
    def _check_yt_dlp(self):
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _check_drission(self):
        try:
            from DrissionPage import ChromiumPage
            return True
        except:
            return False
    
    def _sanitize_filename(self, filename):
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)
        if len(filename) > 80:
            filename = filename[:80]
        return filename
    
    def detect_platform(self, url):
        """检测视频平台"""
        domain = urlparse(url).netloc.lower()
        
        if 'douyin.com' in domain:
            return 'douyin'
        elif 'bilibili.com' in domain or 'b23.tv' in domain:
            return 'bilibili'
        elif 'youtube.com' in domain or 'youtu.be' in domain:
            return 'youtube'
        elif 'tiktok.com' in domain:
            return 'tiktok'
        elif 'ixigua.com' in domain:
            return 'ixigua'
        elif 'kuaishou.com' in domain:
            return 'kuaishou'
        else:
            return 'generic'
    
    def download_with_ytdlp(self, url, index=1, platform='generic'):
        """使用 yt-dlp 下载视频"""
        if not self.yt_dlp_available:
            print("Error: yt-dlp not installed")
            return None
        
        print(f"[{index}] Using yt-dlp to download: {url}")
        
        try:
            # 获取视频信息
            cmd = ['yt-dlp', '--dump-json', '--no-download', '--quiet', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0 or not result.stdout:
                print(f"    Cannot get video info, trying direct download...")
                title = f"video_{index}"
                uploader = "unknown"
            else:
                info = json.loads(result.stdout.strip().split('\n')[0])
                title = info.get('title', f'video_{index}')
                uploader = info.get('uploader', 'unknown')
            
            safe_title = self._sanitize_filename(title)
            output_template = os.path.join(self.save_path, f"{index:03d}_{safe_title}.%(ext)s")
            
            print(f"    Title: {title[:40]}...")
            print(f"    Author: {uploader}")
            
            # 下载视频
            download_cmd = [
                'yt-dlp',
                '-o', output_template,
                '--merge-output-format', 'mp4',
                '--no-warnings',
                '--quiet',
                url
            ]
            
            download_result = subprocess.run(download_cmd, capture_output=True, timeout=180)
            
            if download_result.returncode == 0:
                downloaded_files = [f for f in os.listdir(self.save_path) 
                                  if f.startswith(f"{index:03d}_{safe_title}") and f.endswith('.mp4')]
                
                if downloaded_files:
                    video_filename = downloaded_files[0]
                    file_size = os.path.getsize(os.path.join(self.save_path, video_filename))
                    
                    metadata = {
                        'index': index,
                        'title': title,
                        'author': uploader,
                        'platform': platform,
                        'url': url,
                        'video_filename': video_filename,
                        'file_size_mb': round(file_size / 1024 / 1024, 2),
                        'download_time': datetime.now().isoformat(),
                    }
                    
                    # 保存元数据
                    meta_path = os.path.join(self.save_path, video_filename.replace('.mp4', '.json'))
                    with open(meta_path, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, ensure_ascii=False, indent=2)
                    
                    print(f"    Downloaded: {video_filename} ({metadata['file_size_mb']} MB)\n")
                    return metadata
            
            print(f"    yt-dlp download failed\n")
            return None
            
        except Exception as e:
            print(f"    Error: {e}\n")
            return None
    
    def download_with_drission(self, url, index=1):
        """使用 DrissionPage 下载视频（用于反爬严格的网站）"""
        if not self.drission_available:
            print("Error: DrissionPage not installed")
            return None
        
        from DrissionPage import ChromiumPage, ChromiumOptions
        
        print(f"[{index}] Using DrissionPage to download: {url}")
        
        page = None
        try:
            # 启动浏览器
            co = ChromiumOptions()
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-dev-shm-usage')
            co.set_argument('--disable-gpu')
            
            page = ChromiumPage(co)
            
            # 访问页面
            page.get(url)
            time.sleep(5)
            
            # 获取页面标题
            title = page.title or f'video_{index}'
            
            # 查找视频元素
            print("  Looking for video element...")
            
            # 执行 JS 获取视频 URL
            js_result = page.run_js('''
                const videos = document.querySelectorAll('video');
                const result = [];
                for (let v of videos) {
                    result.push({
                        src: v.src,
                        currentSrc: v.currentSrc,
                    });
                }
                return result;
            ''')
            
            video_url = None
            for v in js_result:
                if v.get('src'):
                    video_url = v['src']
                    break
                if v.get('currentSrc'):
                    video_url = v['currentSrc']
                    break
            
            if not video_url:
                print("  No video URL found, falling back to yt-dlp...")
                page.quit()
                return self.download_with_ytdlp(url, index)
            
            print(f"  Video URL: {video_url[:60]}...")
            
            # 使用 browser session 下载
            safe_title = self._sanitize_filename(title)
            filename = f"{index:03d}_{safe_title}.mp4"
            filepath = os.path.join(self.save_path, filename)
            
            print(f"  Downloading: {filename}")
            
            response = page.session.get(video_url)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = os.path.getsize(filepath)
                
                metadata = {
                    'index': index,
                    'title': title,
                    'author': 'unknown',
                    'platform': 'web',
                    'url': url,
                    'video_filename': filename,
                    'file_size_mb': round(file_size / 1024 / 1024, 2),
                    'download_time': datetime.now().isoformat(),
                }
                
                meta_path = os.path.join(self.save_path, filename.replace('.mp4', '.json'))
                with open(meta_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                print(f"  Downloaded: {filename} ({metadata['file_size_mb']} MB)\n")
                
                page.quit()
                return metadata
            else:
                print(f"  Download failed: HTTP {response.status_code}")
                page.quit()
                return None
                
        except Exception as e:
            print(f"  Error: {e}")
            if page:
                page.quit()
            return None
    
    def download_video(self, url, index=1, use_browser=False):
        """智能下载视频"""
        platform = self.detect_platform(url)
        print(f"Detected platform: {platform}")
        
        # 根据平台选择下载方式
        if platform == 'douyin' or use_browser:
            # 抖音或强制使用浏览器
            return self.download_with_drission(url, index)
        else:
            # 其他平台使用 yt-dlp
            return self.download_with_ytdlp(url, index, platform)
    
    def search_and_download(self, keyword, platform='douyin', count=5):
        """搜索并下载（目前仅支持抖音）"""
        if platform != 'douyin':
            print(f"Search not supported for {platform}, please provide URLs directly")
            return None, []
        
        if not self.drission_available:
            print("Error: DrissionPage not installed, cannot search")
            return None, []
        
        from DrissionPage import ChromiumPage, ChromiumOptions
        
        print(f"Searching {platform} for: {keyword}")
        
        videos = []
        page = None
        
        try:
            co = ChromiumOptions()
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-dev-shm-usage')
            co.set_argument('--disable-gpu')
            
            page = ChromiumPage(co)
            
            search_url = f"https://www.douyin.com/search/{keyword}?type=video"
            page.get(search_url)
            time.sleep(8)
            
            links = page.eles('tag:a')
            
            for link in links:
                try:
                    href = link.attr('href')
                    if href and '/video/' in href:
                        match = re.search(r'/video/(\d+)', href)
                        if match:
                            aweme_id = match.group(1)
                            
                            if any(v.get('aweme_id') == aweme_id for v in videos):
                                continue
                            
                            videos.append({
                                'aweme_id': aweme_id,
                                'title': f'video_{aweme_id}',
                                'share_url': href if href.startswith('http') else f"https://www.douyin.com{href}",
                            })
                            
                            print(f"  Found: {aweme_id}")
                            
                            if len(videos) >= count:
                                break
                except:
                    continue
            
            page.quit()
            
        except Exception as e:
            print(f"Search error: {e}")
            if page:
                page.quit()
        
        if not videos:
            print("No videos found")
            return None, []
        
        print(f"Total found: {len(videos)} videos\n")
        
        # 创建保存目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{platform}_{keyword}_{timestamp}"
        save_dir = os.path.join(self.save_path, folder_name)
        os.makedirs(save_dir, exist_ok=True)
        
        self.save_path = save_dir
        print(f"Save location: {save_dir}\n")
        
        # 下载视频
        results = []
        for i, video in enumerate(videos, 1):
            result = self.download_with_drission(video['share_url'], i)
            if result:
                results.append(result)
            time.sleep(3)
        
        # 保存汇总
        if results:
            summary = {
                'keyword': keyword,
                'platform': platform,
                'download_time': datetime.now().isoformat(),
                'total_count': len(results),
                'save_directory': save_dir,
                'videos': results,
            }
            with open(os.path.join(save_dir, '_summary.json'), 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print(f"{'='*60}")
            print(f"Complete! {len(results)}/{len(videos)} videos")
            print(f"Location: {save_dir}")
            print(f"{'='*60}")
        
        return save_dir, results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Video Downloader')
    parser.add_argument('url_or_keyword', nargs='?', help='Video URL or search keyword')
    parser.add_argument('--url', '-u', action='append', help='Video URL(s)')
    parser.add_argument('--platform', '-p', default='douyin', help='Platform for search (default: douyin)')
    parser.add_argument('--search', '-s', action='store_true', help='Search mode')
    parser.add_argument('--count', '-n', type=int, default=5, help='Number of videos to download')
    parser.add_argument('--output', '-o', default='D:\\video_downloads', help='Output directory')
    parser.add_argument('--browser', '-b', action='store_true', help='Force use browser mode')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output, exist_ok=True)
    
    downloader = VideoDownloader(args.output)
    
    print(f"{'='*60}")
    print(f"Universal Video Downloader")
    print(f"{'='*60}\n")
    
    # 搜索模式
    if args.search and args.url_or_keyword:
        print(f"Mode: Search")
        print(f"Platform: {args.platform}")
        print(f"Keyword: {args.url_or_keyword}")
        print(f"Count: {args.count}\n")
        
        save_dir, results = downloader.search_and_download(args.url_or_keyword, args.platform, args.count)
        
        if results:
            print(f"\nSaved to: {save_dir}")
        else:
            print("\nNo videos downloaded")
    
    # URL 下载模式
    elif args.url:
        urls = args.url
        
        print(f"Mode: URL Download")
        print(f"URLs: {len(urls)}\n")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"batch_{timestamp}"
        save_dir = os.path.join(args.output, folder_name)
        os.makedirs(save_dir, exist_ok=True)
        
        downloader.save_path = save_dir
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")
            result = downloader.download_video(url, i, args.browser)
            if result:
                results.append(result)
            time.sleep(2)
        
        if results:
            summary = {
                'download_time': datetime.now().isoformat(),
                'total_count': len(results),
                'save_directory': save_dir,
                'videos': results,
            }
            with open(os.path.join(save_dir, '_summary.json'), 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print(f"\n{'='*60}")
            print(f"Complete! {len(results)}/{len(urls)} videos")
            print(f"Location: {save_dir}")
            print(f"{'='*60}")
    
    # 单 URL 模式
    elif args.url_or_keyword:
        url = args.url_or_keyword
        
        # 检测是否是 URL
        if url.startswith('http'):
            print(f"Mode: Single URL")
            print(f"URL: {url}\n")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"single_{timestamp}"
            save_dir = os.path.join(args.output, folder_name)
            os.makedirs(save_dir, exist_ok=True)
            
            downloader.save_path = save_dir
            
            result = downloader.download_video(url, 1, args.browser)
            
            if result:
                print(f"\nSaved to: {save_dir}")
            else:
                print("\nDownload failed")
        else:
            print(f"'{url}' is not a valid URL")
            print("Use --search to search for videos")
    
    else:
        print("Please provide a URL or keyword")
        print("\nExamples:")
        print('  Download single video:')
        print('    python video_downloader.py "https://www.douyin.com/video/xxx"')
        print('    python video_downloader.py "https://www.bilibili.com/video/xxx"')
        print('    python video_downloader.py "https://www.youtube.com/watch?v=xxx"')
        print()
        print('  Download multiple videos:')
        print('    python video_downloader.py -u "url1" -u "url2" -u "url3"')
        print()
        print('  Search and download:')
        print('    python video_downloader.py 美女 --search --count 5')
        print()
        print('  Force browser mode (for anti-crawl sites):')
        print('    python video_downloader.py "https://example.com/video" --browser')


if __name__ == '__main__':
    main()
