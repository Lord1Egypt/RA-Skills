"""
Media Processor - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from video_processor import VideoProcessor, VideoInfo
from audio_processor import AudioProcessor


class TestVideoProcessor(unittest.TestCase):
    """测试视频处理器"""
    
    def setUp(self):
        self.processor = VideoProcessor()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.processor)
        self.assertEqual(self.processor.ffmpeg_path, 'ffmpeg')
    
    def test_video_info_dataclass(self):
        """测试视频信息数据类"""
        info = VideoInfo(
            duration=120.5,
            width=1920,
            height=1080,
            fps=30.0,
            bitrate=5000000,
            codec='h264',
            audio_codec='aac',
            format='mp4'
        )
        self.assertEqual(info.width, 1920)
        self.assertEqual(info.height, 1080)


class TestAudioProcessor(unittest.TestCase):
    """测试音频处理器"""
    
    def test_init(self):
        """测试初始化"""
        processor = AudioProcessor()
        self.assertIsNone(processor.audio)
    
    def test_info_empty(self):
        """测试空音频信息"""
        processor = AudioProcessor()
        info = processor.get_info()
        self.assertEqual(info, {})


class TestTranscriber(unittest.TestCase):
    """测试语音识别"""
    
    def test_model_sizes(self):
        """测试模型大小常量"""
        from transcriber import Transcriber
        self.assertIn('tiny', Transcriber.MODEL_SIZES)
        self.assertIn('base', Transcriber.MODEL_SIZES)
        self.assertIn('large', Transcriber.MODEL_SIZES)


if __name__ == '__main__':
    unittest.main(verbosity=2)
