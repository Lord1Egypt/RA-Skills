#!/usr/bin/env python3
"""
文件完整性校验模块
版本：1.0.0
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image

logger = logging.getLogger(__name__)


class IntegrityChecker:
    """文件完整性校验器"""
    
    def __init__(self):
        self.enabled = os.getenv('INTEGRITY_CHECK_ENABLED', 'true').lower() == 'true'
        self.check_file_size = os.getenv('CHECK_FILE_SIZE', 'true').lower() == 'true'
        self.check_image_openable = os.getenv('CHECK_IMAGE_OPENABLE', 'true').lower() == 'true'
        self.auto_redownload = os.getenv('AUTO_REDOWNLOAD', 'true').lower() == 'true'
        
        logger.info("文件完整性校验器已初始化")
    
    def check_all_images(self, image_dir: Path, expected_count: int) -> Dict:
        """
        校验所有图片的完整性
        
        Args:
            image_dir: 图片目录
            expected_count: 预期图片数量
            
        Returns:
            校验结果字典
        """
        result = {
            'expected_count': expected_count,
            'actual_count': 0,
            'damaged_count': 0,
            'missing_count': 0,
            'files': [],
            'damaged_files': [],
            'missing_files': [],
            'passed': False
        }
        
        if not self.enabled:
            logger.info("完整性校验已禁用")
            result['passed'] = True
            return result
        
        # 获取所有图片文件
        image_files = list(image_dir.glob('*.jpg')) + \
                     list(image_dir.glob('*.png')) + \
                     list(image_dir.glob('*.webp'))
        
        result['actual_count'] = len(image_files)
        
        # 检查数量
        if len(image_files) < expected_count:
            result['missing_count'] = expected_count - len(image_files)
            logger.warning(f"缺少 {result['missing_count']} 张图片")
        
        # 逐个检查文件
        for image_file in sorted(image_files):
            file_result = self._check_single_file(image_file)
            result['files'].append(file_result)
            
            if not file_result['valid']:
                result['damaged_count'] += 1
                result['damaged_files'].append(file_result)
                logger.warning(f"文件损坏：{image_file.name}")
        
        # 判断是否通过
        result['passed'] = (result['actual_count'] >= expected_count and 
                           result['damaged_count'] == 0)
        
        print(f"   应下载：{result['expected_count']} 张")
        print(f"   实下载：{result['actual_count']} 张")
        print(f"   损坏：{result['damaged_count']} 张")
        
        return result
    
    def _check_single_file(self, image_file: Path) -> Dict:
        """
        校验单个文件的完整性
        
        Returns:
            校验结果字典
        """
        result = {
            'filename': image_file.name,
            'filepath': str(image_file),
            'valid': True,
            'errors': []
        }
        
        # 检查文件大小
        if self.check_file_size:
            file_size = image_file.stat().st_size
            result['file_size'] = file_size
            result['file_size_kb'] = round(file_size / 1024, 2)
            
            if file_size == 0:
                result['valid'] = False
                result['errors'].append('文件大小为 0')
        
        # 检查图片是否可打开
        if self.check_image_openable:
            try:
                with Image.open(image_file) as img:
                    img.verify()
                result['width'] = img.size[0]
                result['height'] = img.size[1]
                result['format'] = img.format
            except Exception as e:
                result['valid'] = False
                result['errors'].append(f'无法打开：{str(e)}')
        
        return result
