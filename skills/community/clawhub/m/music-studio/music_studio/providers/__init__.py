"""Provider 注册与工厂"""

from music_studio.providers.base import MusicAPIBase
from music_studio.providers import minimax

_PROVIDERS = {
    "minimax": minimax.MiniMaxProvider,
}


def get_api_client(api_key: str, provider: str = "minimax") -> MusicAPIBase:
    """根据 provider 名称返回对应 API 实例"""
    cls = _PROVIDERS.get(provider)
    if cls is None:
        raise ValueError(f"未知的 provider: {provider}，支持的: {list(_PROVIDERS.keys())}")
    return cls(api_key)