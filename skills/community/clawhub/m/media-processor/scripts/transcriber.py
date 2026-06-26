"""
Transcriber - 语音识别转录 (基于 Whisper)
"""

import whisper
import srt
from datetime import timedelta
from typing import Optional, List, Dict
import os


class Transcriber:
    """语音识别转录器"""
    
    MODEL_SIZES = ['tiny', 'base', 'small', 'medium', 'large']
    
    def __init__(self, model: str = 'base', device: Optional[str] = None):
        """
        初始化转录器
        
        Args:
            model: 模型大小 (tiny, base, small, medium, large)
            device: 计算设备 (cuda/cpu)
        """
        self.model_name = model
        self.device = device
        self.model = whisper.load_model(model, device=device)
        self.last_result = None
    
    def transcribe(self, audio_path: str, language: Optional[str] = None,
                  task: str = 'transcribe') -> str:
        """
        转录音频
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码 (zh, en, ja, etc.)
            task: 任务类型 (transcribe/translate)
        
        Returns:
            转录文本
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        result = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            verbose=False
        )
        
        self.last_result = result
        return result['text']
    
    def transcribe_with_timestamps(self, audio_path: str,
                                   language: Optional[str] = None) -> List[Dict]:
        """转录并返回时间戳"""
        result = self.model.transcribe(
            audio_path,
            language=language,
            verbose=False
        )
        
        self.last_result = result
        
        segments = []
        for segment in result['segments']:
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return segments
    
    def save_srt(self, output_path: str, segments: Optional[List] = None):
        """保存为SRT字幕文件"""
        if segments is None:
            if self.last_result is None:
                raise ValueError("没有可保存的转录结果")
            segments = self.last_result['segments']
        
        subtitles = []
        for i, segment in enumerate(segments, 1):
            start = timedelta(seconds=segment['start'])
            end = timedelta(seconds=segment['end'])
            
            subtitle = srt.Subtitle(
                index=i,
                start=start,
                end=end,
                content=segment['text'].strip()
            )
            subtitles.append(subtitle)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt.compose(subtitles))
        
        print(f"字幕已保存: {output_path}")
    
    def save_txt(self, output_path: str, text: Optional[str] = None):
        """保存为纯文本"""
        if text is None:
            if self.last_result is None:
                raise ValueError("没有可保存的转录结果")
            text = self.last_result['text']
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"文本已保存: {output_path}")
    
    def detect_language(self, audio_path: str) -> str:
        """检测语言"""
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        
        detected_lang = max(probs, key=probs.get)
        return detected_lang


if __name__ == '__main__':
    print("Transcriber 初始化成功")
    print(f"可用模型: {', '.join(Transcriber.MODEL_SIZES)}")
