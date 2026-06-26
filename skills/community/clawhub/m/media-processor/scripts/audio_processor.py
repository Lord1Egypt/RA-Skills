"""
Audio Processor - 音频处理器 (基于 pydub)
"""

from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from typing import Optional, Union, Tuple
import os


class AudioProcessor:
    """音频处理器"""
    
    def __init__(self, audio_path: Optional[str] = None):
        self.audio_path = audio_path
        self.audio = None
        
        if audio_path and os.path.exists(audio_path):
            self.load(audio_path)
    
    def load(self, audio_path: str) -> 'AudioProcessor':
        """加载音频"""
        self.audio_path = audio_path
        self.audio = AudioSegment.from_file(audio_path)
        return self
    
    def trim(self, start: float, end: float) -> 'AudioProcessor':
        """剪辑音频 (秒)"""
        start_ms = int(start * 1000)
        end_ms = int(end * 1000)
        self.audio = self.audio[start_ms:end_ms]
        return self
    
    def change_volume(self, gain_db: float) -> 'AudioProcessor':
        """调整音量 (dB)"""
        self.audio = self.audio + gain_db
        return self
    
    def normalize(self) -> 'AudioProcessor':
        """标准化音量"""
        self.audio = normalize(self.audio)
        return self
    
    def remove_noise(self, reduction_amount: float = 0.5) -> 'AudioProcessor':
        """降噪处理"""
        # 简单的低通滤波降噪
        from pydub.effects import low_pass_filter
        self.audio = low_pass_filter(self.audio, 3000)
        return self
    
    def change_speed(self, speed: float = 1.0) -> 'AudioProcessor':
        """改变播放速度"""
        if speed != 1.0:
            self.audio = self.audio._spawn(
                self.audio.raw_data,
                overrides={
                    'frame_rate': int(self.audio.frame_rate * speed)
                }
            ).set_frame_rate(self.audio.frame_rate)
        return self
    
    def change_pitch(self, semitones: int) -> 'AudioProcessor':
        """改变音调 (半音)"""
        # 这里简化处理，实际可能需要更复杂的算法
        new_sample_rate = int(self.audio.frame_rate * (2 ** (semitones / 12.0)))
        self.audio = self.audio._spawn(
            self.audio.raw_data,
            overrides={'frame_rate': new_sample_rate}
        )
        return self
    
    def fade_in(self, duration: float) -> 'AudioProcessor':
        """淡入效果 (秒)"""
        self.audio = self.audio.fade_in(int(duration * 1000))
        return self
    
    def fade_out(self, duration: float) -> 'AudioProcessor':
        """淡出效果 (秒)"""
        self.audio = self.audio.fade_out(int(duration * 1000))
        return self
    
    def reverse(self) -> 'AudioProcessor':
        """倒放"""
        self.audio = self.audio.reverse()
        return self
    
    def export(self, output_path: str, format: Optional[str] = None,
              bitrate: str = '192k') -> str:
        """
        导出音频
        
        Args:
            output_path: 输出路径
            format: 格式 (mp3, wav, ogg, flac)
            bitrate: 码率
        """
        if format is None:
            format = os.path.splitext(output_path)[1][1:]
        
        self.audio.export(
            output_path,
            format=format,
            bitrate=bitrate
        )
        
        print(f"音频已导出: {output_path}")
        return output_path
    
    def get_duration(self) -> float:
        """获取时长 (秒)"""
        return len(self.audio) / 1000.0 if self.audio else 0
    
    def get_info(self) -> dict:
        """获取音频信息"""
        if not self.audio:
            return {}
        
        return {
            'duration': self.get_duration(),
            'channels': self.audio.channels,
            'sample_rate': self.audio.frame_rate,
            'sample_width': self.audio.sample_width,
            'bitrate': len(self.audio.raw_data) * 8 / self.get_duration()
        }


def merge_audio(audio_paths: list, output_path: str,
                crossfade: int = 0) -> str:
    """合并多个音频文件"""
    combined = AudioSegment.from_file(audio_paths[0])
    
    for path in audio_paths[1:]:
        audio = AudioSegment.from_file(path)
        if crossfade > 0:
            combined = combined.append(audio, crossfade=crossfade)
        else:
            combined += audio
    
    combined.export(output_path)
    print(f"合并完成: {output_path}")
    return output_path


def split_audio(audio_path: str, segments: list, output_dir: str) -> list:
    """
    分割音频
    
    Args:
        segments: [(start_sec, end_sec), ...]
    """
    audio = AudioSegment.from_file(audio_path)
    output_files = []
    
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    for i, (start, end) in enumerate(segments):
        segment = audio[start * 1000:end * 1000]
        output_path = os.path.join(output_dir, f"{base_name}_{i:03d}.mp3")
        segment.export(output_path)
        output_files.append(output_path)
    
    return output_files


if __name__ == '__main__':
    print("AudioProcessor 初始化成功")
