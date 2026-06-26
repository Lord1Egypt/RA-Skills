"""
TTS Provider抽象基类

定义统一的TTS接口，所有TTS提供商都需要实现这个接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class Gender(Enum):
    """音色性别"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class Emotion(Enum):
    """情感类型"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ANGRY = "angry"
    CALM = "calm"


@dataclass
class Voice:
    """音色信息"""
    id: str
    name: str
    gender: Gender
    language: str
    description: Optional[str] = None
    preview_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender.value,
            'language': self.language,
            'description': self.description,
            'preview_url': self.preview_url
        }


@dataclass
class TTSConfig:
    """TTS配置"""
    voice_id: str
    emotion: Emotion = Emotion.NEUTRAL
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'voice_id': self.voice_id,
            'emotion': self.emotion.value,
            'speed': self.speed,
            'pitch': self.pitch,
            'volume': self.volume
        }


@dataclass
class AudioData:
    """音频数据"""
    data: bytes
    format: str = "wav"
    sample_rate: int = 16000
    channels: int = 1
    duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'format': self.format,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'duration': self.duration,
            'size': len(self.data)
        }


class TTSProvider(ABC):
    """
    TTS Provider抽象基类
    
    所有TTS提供商都需要实现这个接口。
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """提供商名称"""
        pass
    
    @property
    @abstractmethod
    def supported_languages(self) -> List[str]:
        """支持的语言列表"""
        pass
    
    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice_id: str,
        emotion: Emotion = Emotion.NEUTRAL,
        speed: float = 1.0,
        pitch: float = 1.0
    ) -> AudioData:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            voice_id: 音色ID
            emotion: 情感类型
            speed: 语速（0.5-2.0）
            pitch: 音调（0.5-2.0）
            
        Returns:
            AudioData: 音频数据
            
        Raises:
            TTSError: TTS合成失败
        """
        pass
    
    @abstractmethod
    async def get_voices(self, language: Optional[str] = None) -> List[Voice]:
        """
        获取可用音色列表
        
        Args:
            language: 语言代码（如'zh-CN'），None表示所有语言
            
        Returns:
            List[Voice]: 音色列表
        """
        pass
    
    @abstractmethod
    async def check_availability(self) -> bool:
        """
        检查TTS服务是否可用
        
        Returns:
            bool: 服务是否可用
        """
        pass
    
    async def preview_voice(self, voice_id: str) -> Optional[AudioData]:
        """
        预览音色（可选实现）
        
        Args:
            voice_id: 音色ID
            
        Returns:
            Optional[AudioData]: 预览音频数据，None表示不支持预览
        """
        return None
    
    def validate_text(self, text: str) -> bool:
        """
        验证文本是否有效
        
        Args:
            text: 要验证的文本
            
        Returns:
            bool: 文本是否有效
        """
        if not text or not isinstance(text, str):
            return False
        
        if len(text.strip()) == 0:
            return False
        
        if len(text) > 10000:
            return False
        
        return True
    
    def validate_speed(self, speed: float) -> bool:
        """
        验证语速是否有效
        
        Args:
            speed: 语速值
            
        Returns:
            bool: 语速是否有效
        """
        return 0.5 <= speed <= 2.0
    
    def validate_pitch(self, pitch: float) -> bool:
        """
        验证音调是否有效
        
        Args:
            pitch: 音调值
            
        Returns:
            bool: 音调是否有效
        """
        return 0.5 <= pitch <= 2.0


class TTSError(Exception):
    """TTS错误基类"""
    pass


class TTSNotAvailableError(TTSError):
    """TTS服务不可用错误"""
    pass


class TTSVoiceNotFoundError(TTSError):
    """音色未找到错误"""
    pass


class TTSSynthesisError(TTSError):
    """语音合成错误"""
    pass
