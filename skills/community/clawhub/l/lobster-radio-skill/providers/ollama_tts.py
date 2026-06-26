"""
Ollama Qwen3-TTS Provider

使用Ollama本地运行的Qwen3-TTS模型进行语音合成。
"""

import aiohttp
import asyncio
import json
from typing import List, Optional
from .tts_base import (
    TTSProvider, Voice, AudioData, Emotion, Gender,
    TTSError, TTSNotAvailableError, TTSSynthesisError
)
from .tts_factory import register_provider


@register_provider
class OllamaTTSProvider(TTSProvider):
    """
    Ollama Qwen3-TTS Provider
    
    使用本地Ollama服务运行Qwen3-TTS模型进行语音合成。
    """
    
    def __init__(
        self,
        model: str = "qwen3-tts:0.6b-int4",
        base_url: str = "http://localhost:11434",
        timeout: int = 60
    ):
        """
        初始化Ollama TTS Provider
        
        Args:
            model: 模型名称
            base_url: Ollama服务地址
            timeout: 请求超时时间（秒）
        """
        self.model = model
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._voices_cache: Optional[List[Voice]] = None
    
    @property
    def name(self) -> str:
        """提供商名称"""
        return "Ollama Qwen3-TTS"
    
    @property
    def supported_languages(self) -> List[str]:
        """支持的语言列表"""
        return ["zh-CN", "en-US", "ja-JP", "ko-KR", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "ru-RU"]
    
    async def synthesize(
        self,
        text: str,
        voice_id: str,
        emotion: Emotion = Emotion.NEUTRAL,
        speed: float = 1.0,
        pitch: float = 1.0
    ) -> AudioData:
        """
        使用Ollama生成语音
        
        Args:
            text: 要合成的文本
            voice_id: 音色ID
            emotion: 情感类型
            speed: 语速（0.5-2.0）
            pitch: 音调（0.5-2.0）
            
        Returns:
            AudioData: 音频数据
            
        Raises:
            TTSSynthesisError: 语音合成失败
        """
        if not self.validate_text(text):
            raise TTSSynthesisError(f"Invalid text: {text[:50]}...")
        
        if not self.validate_speed(speed):
            raise TTSSynthesisError(f"Invalid speed: {speed}")
        
        if not self.validate_pitch(pitch):
            raise TTSSynthesisError(f"Invalid pitch: {pitch}")
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                payload = {
                    "model": self.model,
                    "prompt": text,
                    "voice": voice_id,
                    "emotion": emotion.value,
                    "speed": speed,
                    "pitch": pitch,
                    "stream": False
                }
                
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise TTSSynthesisError(
                            f"Ollama API error: {response.status} - {error_text}"
                        )
                    
                    result = await response.json()
                    
                    if 'error' in result:
                        raise TTSSynthesisError(f"Ollama error: {result['error']}")
                    
                    audio_data = result.get('audio_data')
                    if not audio_data:
                        raise TTSSynthesisError("No audio data in response")
                    
                    if isinstance(audio_data, str):
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                    else:
                        audio_bytes = audio_data
                    
                    return AudioData(
                        data=audio_bytes,
                        format="wav",
                        sample_rate=16000,
                        channels=1,
                        duration=len(audio_bytes) / 32000
                    )
                    
        except aiohttp.ClientError as e:
            raise TTSSynthesisError(f"HTTP request failed: {str(e)}")
        except asyncio.TimeoutError:
            raise TTSSynthesisError(f"Request timeout after {self.timeout}s")
        except Exception as e:
            raise TTSSynthesisError(f"Unexpected error: {str(e)}")
    
    async def get_voices(self, language: Optional[str] = None) -> List[Voice]:
        """
        获取可用音色列表
        
        Args:
            language: 语言代码（如'zh-CN'），None表示所有语言
            
        Returns:
            List[Voice]: 音色列表
        """
        if self._voices_cache is None:
            self._voices_cache = [
                Voice(
                    id="xiaoxiao",
                    name="晓晓",
                    gender=Gender.FEMALE,
                    language="zh-CN",
                    description="女声，温柔，适合新闻播报"
                ),
                Voice(
                    id="yunjian",
                    name="云健",
                    gender=Gender.MALE,
                    language="zh-CN",
                    description="男声，沉稳，适合财经资讯"
                ),
                Voice(
                    id="xiaochen",
                    name="晓辰",
                    gender=Gender.FEMALE,
                    language="zh-CN",
                    description="女声，活泼，适合娱乐新闻"
                ),
                Voice(
                    id="xiaoyu",
                    name="晓宇",
                    gender=Gender.MALE,
                    language="zh-CN",
                    description="男声，年轻，适合科技资讯"
                ),
                Voice(
                    id="xiaoya",
                    name="晓雅",
                    gender=Gender.FEMALE,
                    language="zh-CN",
                    description="女声，知性，适合教育内容"
                )
            ]
        
        if language:
            return [v for v in self._voices_cache if v.language == language]
        
        return self._voices_cache
    
    async def check_availability(self) -> bool:
        """
        检查Ollama服务是否可用
        
        Returns:
            bool: 服务是否可用
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status != 200:
                        return False
                    
                    data = await response.json()
                    models = data.get('models', [])
                    
                    for model in models:
                        if self.model in model.get('name', ''):
                            return True
                    
                    return False
                    
        except Exception:
            return False
    
    async def ensure_model_available(self) -> bool:
        """
        确保模型已下载
        
        Returns:
            bool: 模型是否可用
        """
        if await self.check_availability():
            return True
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:
                async with session.post(
                    f"{self.base_url}/api/pull",
                    json={"name": self.model}
                ) as response:
                    if response.status != 200:
                        return False
                    
                    async for line in response.content:
                        data = json.loads(line)
                        if data.get('status') == 'success':
                            return True
                    
                    return False
                    
        except Exception:
            return False
    
    async def preview_voice(self, voice_id: str) -> Optional[AudioData]:
        """
        预览音色
        
        Args:
            voice_id: 音色ID
            
        Returns:
            Optional[AudioData]: 预览音频数据
        """
        preview_text = "这是一个音色预览示例，欢迎使用龙虾电台。"
        
        try:
            return await self.synthesize(
                text=preview_text,
                voice_id=voice_id,
                emotion=Emotion.NEUTRAL,
                speed=1.0,
                pitch=1.0
            )
        except Exception:
            return None
