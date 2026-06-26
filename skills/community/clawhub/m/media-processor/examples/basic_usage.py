"""
Media Processor - 基本使用示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from video_processor import VideoProcessor
from video_editor import VideoEditor
from audio_processor import AudioProcessor
from transcriber import Transcriber


def demo_video_info():
    """演示视频信息获取"""
    print("=" * 50)
    print("视频信息获取示例")
    print("=" * 50)
    
    processor = VideoProcessor()
    print("\n视频处理器已初始化")
    print(f"FFmpeg 路径: {processor.ffmpeg_path}")
    
    print("\n功能列表:")
    print("  - get_info(): 获取视频信息")
    print("  - convert(): 格式转换")
    print("  - extract_audio(): 提取音频")
    print("  - compress(): 压缩视频")


def demo_audio_processor():
    """演示音频处理"""
    print("\n" + "=" * 50)
    print("音频处理示例")
    print("=" * 50)
    
    print("\n音频处理器功能:")
    print("  - trim(): 剪辑音频")
    print("  - change_volume(): 调整音量")
    print("  - normalize(): 标准化音量")
    print("  - fade_in/out(): 淡入淡出")
    print("  - export(): 导出音频")
    
    print("\n示例代码:")
    print("""
    from scripts.audio_processor import AudioProcessor
    
    # 加载音频
    audio = AudioProcessor('input.mp3')
    
    # 剪辑 (10-30秒)
    audio.trim(10, 30)
    
    # 调整音量 (+3dB)
    audio.change_volume(3)
    
    # 导出
    audio.export('output.wav', format='wav')
    """)


def demo_transcriber():
    """演示语音识别"""
    print("\n" + "=" * 50)
    print("语音识别示例")
    print("=" * 50)
    
    print("\n可用模型:")
    print("  - tiny: 最快速度，最低精度")
    print("  - base: 快速，基础精度")
    print("  - small: 平衡选择")
    print("  - medium: 更好精度")
    print("  - large: 最佳精度")
    
    print("\n示例代码:")
    print("""
    from scripts.transcriber import Transcriber
    
    # 初始化 (使用 base 模型)
    transcriber = Transcriber(model='base')
    
    # 转录音频
    text = transcriber.transcribe('audio.mp3')
    print(text)
    
    # 保存字幕
    transcriber.save_srt('subtitles.srt')
    """)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Media Processor - 音视频处理器示例 ")
    print("=" * 60)
    
    demo_video_info()
    demo_audio_processor()
    demo_transcriber()
    
    print("\n" + "=" * 60)
    print("所有示例已完成！")
    print("=" * 60)
