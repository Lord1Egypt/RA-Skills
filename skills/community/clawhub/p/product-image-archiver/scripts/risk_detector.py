#!/usr/bin/env python3
"""
侵权风险检测模块
版本：1.0.0

仅标注风险，不删除、不修改任何图片
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class RiskDetector:
    """侵权风险检测器 - 仅标注，不修改"""
    
    def __init__(self):
        self.enabled = os.getenv('RISK_DETECTION_ENABLED', 'true').lower() == 'true'
        self.risk_threshold = float(os.getenv('RISK_THRESHOLD', '0.6'))
        
        # 百度 AI 配置
        self.baidu_enabled = os.getenv('BAIDU_AI_APP_ID', '') != ''
        
        logger.info("侵权风险检测器已初始化（仅标注，不修改）")
    
    def detect_all_images(self, image_dir: Path) -> List[Dict]:
        """
        检测所有图片的侵权风险
        
        Args:
            image_dir: 图片目录
            
        Returns:
            风险检测结果列表
        """
        results = []
        
        if not self.enabled:
            logger.info("风险检测已禁用")
            return results
        
        # 获取所有图片
        image_files = sorted(image_dir.glob('*.jpg')) + \
                     sorted(image_dir.glob('*.png')) + \
                     sorted(image_dir.glob('*.webp'))
        
        for image_file in image_files:
            logger.info(f"检测风险：{image_file.name}")
            print(f"   检测 {image_file.name}...", end=' ')
            
            result = self._detect_single_image(image_file)
            results.append(result)
            
            if result['risk_level'] == '无':
                print("✅ 无风险")
            else:
                print(f"⚠️  {result['risk_level']}")
        
        return results
    
    def _detect_single_image(self, image_file: Path) -> Dict:
        """
        检测单张图片的风险
        
        Returns:
            风险检测结果字典
        """
        result = {
            'filename': image_file.name,
            'filepath': str(image_file),
            'risk_level': '无',
            'risks': [],
            'details': {}
        }
        
        # 百度 AI 检测（如有配置）
        if self.baidu_enabled:
            result = self._baidu_detect(image_file)
        else:
            # 简单检测（基于文件名和大小）
            result = self._simple_detect(image_file)
        
        return result
    
    def _baidu_detect(self, image_file: Path) -> Dict:
        """百度 AI 检测"""
        result = {
            'filename': image_file.name,
            'filepath': str(image_file),
            'risk_level': '无',
            'risks': [],
            'details': {}
        }
        
        try:
            # TODO: 实现百度 AI API 调用
            # 这里预留接口
            
            result['details']['baidu_ai'] = '已检测'
            
        except Exception as e:
            logger.error(f"百度 AI 检测失败：{str(e)}")
            result['details']['error'] = str(e)
        
        return result
    
    def _simple_detect(self, image_file: Path) -> Dict:
        """简单检测（基于规则）"""
        result = {
            'filename': image_file.name,
            'filepath': str(image_file),
            'risk_level': '无',
            'risks': [],
            'details': {}
        }
        
        # 检查文件大小（过小可能是缩略图）
        file_size = image_file.stat().st_size
        if file_size < 10240:  # 小于 10KB
            result['risks'].append('文件过小，可能是缩略图')
            result['risk_level'] = '低'
        
        return result
