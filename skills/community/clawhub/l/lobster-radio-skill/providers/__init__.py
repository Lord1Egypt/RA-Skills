"""
TTS Providers module

提供多种TTS提供商的实现。
"""

from .tts_base import TTSProvider, Voice, Emotion, Gender
from .tts_factory import TTSFactory, register_provider

__all__ = [
    'TTSProvider',
    'Voice',
    'Emotion',
    'Gender',
    'TTSFactory',
    'register_provider'
]

# 自动导入并注册所有provider
try:
    from . import qwen3_tts
except ImportError:
    pass

try:
    from . import ollama_tts
except ImportError:
    pass
