#!/usr/bin/env python3
"""
原图下载器 - 无损模式
版本：1.0.0

安全声明：
- 100% 保留原图，不做任何修改
- 不裁剪、不压缩、不格式转换
- 仅支持单款人工触发
"""

import os
import time
import random
import logging
import requests
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class ImageDownloader:
    """原图下载器 - 无损模式"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        })
        
        self.timeout = int(os.getenv('DOWNLOAD_TIMEOUT', '30'))
        self.retry_times = int(os.getenv('DOWNLOAD_RETRY_TIMES', '3'))
        self.chunk_size = int(os.getenv('DOWNLOAD_CHUNK_SIZE', '8192'))
        self.min_delay = int(os.getenv('MIN_DELAY_SECONDS', '3'))
        self.max_delay = int(os.getenv('MAX_DELAY_SECONDS', '10'))
        
        logger.info("原图下载器已初始化（无损模式）")
    
    def _random_delay(self):
        """随机延迟（模拟人工操作）"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
    
    def download_images(self, image_urls: List[str], output_dir: Path) -> List[Dict]:
        """
        下载原图（无损模式）
        
        Args:
            image_urls: 图片 URL 列表
            output_dir: 输出目录
            
        Returns:
            下载结果列表
        """
        results = []
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, url in enumerate(image_urls, 1):
            logger.info(f"下载图片 {i}/{len(image_urls)}: {url}")
            print(f"   正在下载 {i}/{len(image_urls)}...", end=' ')
            
            # 随机延迟
            self._random_delay()
            
            # 下载图片
            result = self._download_single_image(url, output_dir, i)
            results.append(result)
            
            if result['success']:
                print(f"✅ {result['filename']} ({result['size']}KB)")
            else:
                print(f"❌ 失败：{result['error']}")
        
        return results
    
    def _download_single_image(self, url: str, output_dir: Path, index: int) -> Dict:
        """
        下载单张图片（无损模式）
        
        Returns:
            下载结果字典
        """
        try:
            # 发送请求
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            # 获取原始文件名和格式
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            file_ext = self._get_file_extension(content_type)
            
            # 生成文件名（三位序号 + _original + 扩展名）
            filename = f"{index:03d}_original{file_ext}"
            filepath = output_dir / filename
            
            # 保存文件（原样保存，不做任何处理）
            total_size = 0
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
            
            # 验证文件大小
            if total_size == 0:
                return {
                    'success': False,
                    'filename': filename,
                    'error': '文件大小为 0',
                    'size': 0,
                    'url': url
                }
            
            return {
                'success': True,
                'filename': filename,
                'filepath': str(filepath),
                'size': total_size,
                'size_kb': round(total_size / 1024, 2),
                'url': url,
                'index': index
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'filename': f"{index:03d}_original.jpg",
                'error': str(e),
                'size': 0,
                'url': url,
                'index': index
            }
    
    def _get_file_extension(self, content_type: str) -> str:
        """根据 Content-Type 获取文件扩展名"""
        mime_to_ext = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/bmp': '.bmp',
            'image/svg+xml': '.svg',
        }
        return mime_to_ext.get(content_type, '.jpg')
