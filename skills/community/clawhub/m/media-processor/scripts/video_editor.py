"""
Video Editor - 视频编辑器 (基于 MoviePy)
"""

from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
from typing import Optional, Tuple, Union
import os


class VideoEditor:
    """视频编辑器"""
    
    def __init__(self, video_path: Optional[str] = None):
        self.video_path = video_path
        self.clip = None
        self.text_clips = []
        self.audio_clips = []
        
        if video_path and os.path.exists(video_path):
            self.load(video_path)
    
    def load(self, video_path: str):
        """加载视频"""
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        return self
    
    def trim(self, start: Union[str, float], end: Union[str, float]) -> 'VideoEditor':
        """剪辑视频片段"""
        # 转换时间字符串为秒
        def to_seconds(time_val):
            if isinstance(time_val, str):
                parts = time_val.split(':')
                if len(parts) == 3:
                    h, m, s = map(float, parts)
                    return h * 3600 + m * 60 + s
                elif len(parts) == 2:
                    m, s = map(float, parts)
                    return m * 60 + s
            return float(time_val)
        
        start_sec = to_seconds(start)
        end_sec = to_seconds(end)
        
        self.clip = self.clip.subclip(start_sec, end_sec)
        return self
    
    def resize(self, width: Optional[int] = None,
              height: Optional[int] = None) -> 'VideoEditor':
        """调整视频大小"""
        if width and height:
            self.clip = self.clip.resize(newsize=(width, height))
        elif width:
            self.clip = self.clip.resize(width=width)
        elif height:
            self.clip = self.clip.resize(height=height)
        return self
    
    def add_text(self, text: str, position: Union[str, Tuple] = 'center',
                fontsize: int = 50, color: str = 'white',
                duration: Optional[float] = None,
                start_time: float = 0,
                font: str = 'Arial') -> 'VideoEditor':
        """添加文字"""
        txt_clip = TextClip(text, fontsize=fontsize, color=color, font=font)
        
        if isinstance(position, str):
            if position == 'center':
                txt_clip = txt_clip.set_position('center')
            elif position == 'top':
                txt_clip = txt_clip.set_position(('center', 'top'))
            elif position == 'bottom':
                txt_clip = txt_clip.set_position(('center', 'bottom'))
        else:
            txt_clip = txt_clip.set_position(position)
        
        txt_clip = txt_clip.set_start(start_time)
        if duration:
            txt_clip = txt_clip.set_duration(duration)
        else:
            txt_clip = txt_clip.set_duration(self.clip.duration)
        
        self.text_clips.append(txt_clip)
        return self
    
    def add_watermark(self, image_path: str,
                     position: Union[str, Tuple] = 'bottom-right',
                     opacity: float = 0.5) -> 'VideoEditor':
        """添加水印"""
        watermark = ImageClip(image_path).set_opacity(opacity)
        
        if position == 'bottom-right':
            watermark = watermark.set_position(('right', 'bottom'))
        elif position == 'bottom-left':
            watermark = watermark.set_position(('left', 'bottom'))
        elif position == 'top-right':
            watermark = watermark.set_position(('right', 'top'))
        elif position == 'top-left':
            watermark = watermark.set_position(('left', 'top'))
        else:
            watermark = watermark.set_position(position)
        
        watermark = watermark.set_duration(self.clip.duration)
        self.text_clips.append(watermark)
        return self
    
    def add_fade(self, fade_in: Optional[float] = None,
                fade_out: Optional[float] = None) -> 'VideoEditor':
        """添加淡入淡出效果"""
        if fade_in:
            self.clip = fadein(self.clip, fade_in)
        if fade_out:
            self.clip = fadeout(self.clip, fade_out)
        return self
    
    def add_audio(self, audio_path: str, loop: bool = False) -> 'VideoEditor':
        """添加背景音乐"""
        audio = AudioFileClip(audio_path)
        
        if loop and audio.duration < self.clip.duration:
            audio = audio.fx(vfx.audio_loop, duration=self.clip.duration)
        else:
            audio = audio.subclip(0, min(audio.duration, self.clip.duration))
        
        self.audio_clips.append(audio)
        return self
    
    def adjust_speed(self, speed: float = 1.0) -> 'VideoEditor':
        """调整播放速度"""
        self.clip = self.clip.fx(vfx.speedx, speed)
        return self
    
    def rotate(self, angle: float) -> 'VideoEditor':
        """旋转视频"""
        self.clip = self.clip.rotate(angle)
        return self
    
    def save(self, output_path: str, codec: str = 'libx264',
            audio_codec: str = 'aac', fps: int = 30) -> str:
        """保存视频"""
        # 合并所有图层
        final_clip = self.clip
        
        for clip in self.text_clips:
            final_clip = CompositeVideoClip([final_clip, clip])
        
        # 合并音频
        if self.audio_clips:
            audio = CompositeAudioClip([self.clip.audio] + self.audio_clips)
            final_clip = final_clip.set_audio(audio)
        
        final_clip.write_videofile(
            output_path,
            codec=codec,
            audio_codec=audio_codec,
            fps=fps,
            threads=4
        )
        
        print(f"视频已保存: {output_path}")
        return output_path
    
    def get_duration(self) -> float:
        """获取视频时长"""
        return self.clip.duration if self.clip else 0
    
    def get_resolution(self) -> Tuple[int, int]:
        """获取视频分辨率"""
        if self.clip:
            return (self.clip.w, self.clip.h)
        return (0, 0)


if __name__ == '__main__':
    print("VideoEditor 初始化成功")
