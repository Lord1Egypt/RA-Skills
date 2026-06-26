"""图像工具单元测试"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.image_enhancer import ImageEnhancer


class TestImageEnhancer(unittest.TestCase):
    def setUp(self):
        self.enhancer = ImageEnhancer()
    
    def test_init(self):
        self.assertIsNotNone(self.enhancer)


if __name__ == '__main__':
    print("🧪 运行 Image AI Kit 单元测试...\n")
    unittest.main(verbosity=2)
