"""Provider 插件抽象层"""

from abc import ABC, abstractmethod
from typing import Optional


class MusicAPIBase(ABC):
    """音乐 API 基类，所有 Provider 必须实现"""

    @abstractmethod
    def lyrics_generation(
        self,
        prompt: str = "",
        *,
        mode: str = "write_full_song",
        lyrics: Optional[str] = None,
        title: Optional[str] = None,
    ) -> dict:
        """作词"""
        ...

    @abstractmethod
    def music_cover_preprocess(
        self,
        model: str,
        *,
        audio_url: Optional[str] = None,
        audio_base64: Optional[str] = None,
    ) -> dict:
        """翻唱前处理，返回 cover_feature_id / formatted_lyrics / structure_result / audio_duration"""
        ...

    @abstractmethod
    def music_generation(
        self,
        model: str,
        prompt: str,
        *,
        lyrics: Optional[str] = None,
        is_instrumental: bool = False,
        lyrics_optimizer: bool = False,
        output_format: str = "url",
        sample_rate: int = 44100,
        bitrate: int = 256000,
        reference_audio_url: Optional[str] = None,
        reference_audio_base64: Optional[str] = None,
        cover_feature_id: Optional[str] = None,
    ) -> dict:
        """音乐生成（文本→音乐 或 翻唱）"""
        ...

    @abstractmethod
    def raise_on_error(self, resp: dict) -> None:
        """检查响应状态码，非 0 则抛异常"""
        ...
