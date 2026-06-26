"""
音视频处理器单元测试
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.video_processor import VideoProcessor


class TestVideoProcessor(unittest.TestCase):
    """测试 VideoProcessor 类"""
    
    def setUp(self):
        """测试前准备"""
        self.processor = VideoProcessor()
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.processor.ffmpeg_path, 'ffmpeg')
    
    def test_get_info_nonexistent(self):
        """测试获取不存在文件的信息"""
        info = self.processor.get_info('nonexistent.mp4')
        self.assertIn('error', info)


if __name__ == '__main__':
    print("🧪 运行 Media Processor 单元测试...\n")
    unittest.main(verbosity=2)
