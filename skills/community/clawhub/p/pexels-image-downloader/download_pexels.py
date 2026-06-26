#!/usr/bin/env python3
"""
Pexels图片下载工具 - 主脚本
使用Pexels API搜索和下载高质量免费图片
"""

import argparse
import os
import sys
import json
import time
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

try:
    import requests
    from PIL import Image
    import io
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print("请运行: pip install requests pillow")
    sys.exit(1)


class PexelsDownloader:
    """Pexels图片下载器"""
    
    # 平台尺寸配置
    PLATFORM_SIZES = {
        'xiaohongshu': (1242, 1660),      # 小红书
        'wechat': (900, 500),             # 微信公众号
        'weibo': (1000, 562),             # 微博
        'instagram_square': (1080, 1080), # Instagram方形
        'instagram_portrait': (1080, 1350), # Instagram竖版
        'twitter': (1200, 675),           # Twitter
        'facebook': (1200, 630),          # Facebook
        'default': (1920, 1080)           # 默认16:9
    }
    
    def __init__(self, api_key=None, output_dir='./downloads', platform='xiaohongshu'):
        """
        初始化下载器
        
        Args:
            api_key: Pexels API密钥
            output_dir: 输出目录
            platform: 目标平台，用于自动确定尺寸
        """
        self.api_key = api_key or os.getenv('PEXELS_API_KEY')
        if not self.api_key:
            raise ValueError("请提供Pexels API密钥或设置PEXELS_API_KEY环境变量")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.platform = platform
        self.headers = {'Authorization': self.api_key}
        
        print(f"🔧 初始化Pexels下载器")
        print(f"   平台: {platform}")
        print(f"   输出目录: {output_dir}")
    
    def search_photos(self, query, per_page=10, page=1, orientation='portrait', size='large'):
        """
        搜索图片
        
        Args:
            query: 搜索关键词
            per_page: 每页结果数
            page: 页码
            orientation: 方向 (portrait, landscape, square)
            size: 尺寸 (large, medium, small)
            
        Returns:
            list: 图片信息列表
        """
        print(f"🔍 搜索: '{query}' (第{page}页)")
        
        params = {
            'query': query,
            'per_page': per_page,
            'page': page,
            'orientation': orientation,
            'size': size
        }
        
        try:
            response = requests.get(
                'https://api.pexels.com/v1/search',
                headers=self.headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total_results', 0)
                photos = data.get('photos', [])
                
                print(f"✅ 找到 {total} 张图片，返回 {len(photos)} 张")
                return photos
                
            elif response.status_code == 401:
                print(f"❌ API密钥无效")
                return []
            elif response.status_code == 429:
                print(f"⚠️  请求过多，等待后重试...")
                time.sleep(2)
                return self.search_photos(query, per_page, page, orientation, size)
            else:
                print(f"❌ 搜索失败: HTTP {response.status_code}")
                return []
                
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
            return []
        except Exception as e:
            print(f"❌ 搜索出错: {e}")
            return []
    
    def download_photo(self, photo_info, target_size=None):
        """
        下载单张图片
        
        Args:
            photo_info: 图片信息字典
            target_size: 目标尺寸 (width, height)，为None则使用平台默认
            
        Returns:
            str: 下载的图片路径，失败返回None
        """
        try:
            photo_id = photo_info.get('id', 'unknown')
            photographer = photo_info.get('photographer', 'Unknown')
            photo_url = photo_info.get('src', {}).get('large')
            
            if not photo_url:
                print(f"❌ 图片 {photo_id} 无下载链接")
                return None
            
            print(f"📥 下载图片 {photo_id} - {photographer}")
            
            # 下载图片
            img_response = requests.get(photo_url, timeout=15)
            if img_response.status_code != 200:
                print(f"❌ 下载失败: HTTP {img_response.status_code}")
                return None
            
            # 打开图片
            img = Image.open(io.BytesIO(img_response.content))
            original_size = img.size
            
            # 确定目标尺寸
            if target_size is None:
                target_size = self.PLATFORM_SIZES.get(self.platform, self.PLATFORM_SIZES['default'])
            
            # 调整尺寸
            if img.size != target_size:
                img = img.resize(target_size, Image.Resampling.LANCZOS)
                print(f"   调整尺寸: {original_size} → {target_size}")
            
            # 生成文件名
            filename = f"pexels_{photo_id}_{self.platform}.jpg"
            filepath = self.output_dir / filename
            
            # 保存图片
            img.save(filepath, quality=95, optimize=True)
            file_size = filepath.stat().st_size
            
            # 保存元数据
            self._save_metadata(photo_info, filepath, target_size)
            
            print(f"✅ 保存: {filename} ({file_size/1024:.1f} KB)")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None
    
    def _save_metadata(self, photo_info, filepath, target_size):
        """保存图片元数据"""
        metadata_path = filepath.with_suffix('.json')
        
        metadata = {
            'id': photo_info.get('id'),
            'photographer': photo_info.get('photographer'),
            'photographer_url': photo_info.get('photographer_url'),
            'original_url': photo_info.get('url'),
            'src': photo_info.get('src', {}),
            'download_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'target_size': target_size,
            'platform': self.platform,
            'license': 'Pexels Free License',
            'terms': 'Free to use for personal and commercial projects. Attribution is appreciated but not required.'
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def batch_download(self, queries, count_per_query=3, **kwargs):
        """
        批量下载
        
        Args:
            queries: 关键词列表
            count_per_query: 每个关键词下载数量
            
        Returns:
            list: 所有下载的图片路径
        """
        all_downloads = []
        
        for query in queries:
            print(f"\n{'='*50}")
            print(f"处理关键词: {query}")
            print(f"{'='*50}")
            
            photos = self.search_photos(query, per_page=count_per_query, **kwargs)
            
            for i, photo in enumerate(photos):
                if i >= count_per_query:
                    break
                    
                downloaded = self.download_photo(photo)
                if downloaded:
                    all_downloads.append(downloaded)
                
                # 避免请求过快
                time.sleep(1)
        
        return all_downloads


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Pexels图片下载工具')
    parser.add_argument('--query', '-q', required=True, help='搜索关键词')
    parser.add_argument('--count', '-c', type=int, default=3, help='下载数量')
    parser.add_argument('--output-dir', '-o', default='./downloads', help='输出目录')
    parser.add_argument('--platform', '-p', default='xiaohongshu', 
                       choices=['xiaohongshu', 'wechat', 'weibo', 'instagram_square', 
                               'instagram_portrait', 'twitter', 'facebook', 'default'],
                       help='目标平台')
    parser.add_argument('--orientation', default='portrait',
                       choices=['portrait', 'landscape', 'square'],
                       help='图片方向')
    parser.add_argument('--size', default='large',
                       choices=['large', 'medium', 'small'],
                       help='图片尺寸')
    
    args = parser.parse_args()
    
    # 检查API密钥
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("❌ 请设置PEXELS_API_KEY环境变量")
        print("💡 示例: export PEXELS_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    print("="*60)
    print("Pexels图片下载工具")
    print("="*60)
    
    try:
        # 创建下载器
        downloader = PexelsDownloader(
            api_key=api_key,
            output_dir=args.output_dir,
            platform=args.platform
        )
        
        # 搜索并下载
        photos = downloader.search_photos(
            query=args.query,
            per_page=args.count,
            orientation=args.orientation,
            size=args.size
        )
        
        if not photos:
            print("❌ 未找到图片")
            sys.exit(1)
        
        # 下载图片
        downloaded_files = []
        for i, photo in enumerate(photos):
            if i >= args.count:
                break
                
            filepath = downloader.download_photo(photo)
            if filepath:
                downloaded_files.append(filepath)
            
            time.sleep(1)  # 避免请求过快
        
        # 输出结果
        print("\n" + "="*60)
        print("下载完成!")
        print(f"✅ 成功下载: {len(downloaded_files)}/{args.count} 张图片")
        print(f"📁 保存到: {args.output_dir}")
        
        for filepath in downloaded_files:
            print(f"  • {Path(filepath).name}")
        
        print("="*60)
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()