"""
Image AI Kit - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from image_processor import ImageProcessor
from ocr_engine import OCREngine
from smart_crop import SmartCrop


class TestImageProcessor(unittest.TestCase):
    """测试图像处理器"""
    
    def test_init(self):
        """测试初始化"""
        processor = ImageProcessor()
        self.assertIsNone(processor.image)
    
    def test_info_empty(self):
        """测试空图像信息"""
        processor = ImageProcessor()
        info = processor.get_info()
        self.assertEqual(info, {})
    
    def test_mode_string(self):
        """测试空模式"""
        processor = ImageProcessor()
        self.assertEqual(processor.get_mode(), '')


class TestOCREngine(unittest.TestCase):
    """测试OCR引擎"""
    
    def test_init(self):
        """测试初始化"""
        ocr = OCREngine(lang='chi_sim+eng')
        self.assertEqual(ocr.lang, 'chi_sim+eng')
    
    def test_available_languages(self):
        """测试获取语言列表"""
        langs = OCREngine.get_available_languages()
        self.assertIsInstance(langs, list)


class TestSmartCrop(unittest.TestCase):
    """测试智能裁剪"""
    
    def test_init(self):
        """测试初始化"""
        cropper = SmartCrop()
        self.assertIsNotNone(cropper)


if __name__ == '__main__':
    unittest.main(verbosity=2)
