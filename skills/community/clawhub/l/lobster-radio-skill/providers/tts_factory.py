"""
TTS工厂模式

用于创建不同的TTS提供商实例。
"""

from typing import Dict, Type, Optional
from .tts_base import TTSProvider, TTSError


class TTSFactory:
    """
    TTS工厂类
    
    用于创建和管理不同的TTS提供商实例。
    """
    
    _providers: Dict[str, Type[TTSProvider]] = {}
    _instances: Dict[str, TTSProvider] = {}
    
    @classmethod
    def register(cls, provider_class: Type[TTSProvider]) -> None:
        """
        注册TTS提供商
        
        Args:
            provider_class: TTS提供商类
        """
        provider_name = provider_class.__name__.lower().replace('provider', '')
        cls._providers[provider_name] = provider_class
    
    @classmethod
    def create(cls, provider_name: str, **kwargs) -> TTSProvider:
        """
        创建TTS提供商实例
        
        Args:
            provider_name: 提供商名称
            **kwargs: 提供商初始化参数
            
        Returns:
            TTSProvider: TTS提供商实例
            
        Raises:
            TTSError: 提供商未注册
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            raise TTSError(
                f"TTS provider '{provider_name}' not registered. "
                f"Available providers: {list(cls._providers.keys())}"
            )
        
        if provider_name not in cls._instances:
            provider_class = cls._providers[provider_name]
            cls._instances[provider_name] = provider_class(**kwargs)
        
        return cls._instances[provider_name]
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        获取所有已注册的提供商名称
        
        Returns:
            list: 提供商名称列表
        """
        return list(cls._providers.keys())
    
    @classmethod
    def clear_instances(cls) -> None:
        """清除所有实例"""
        cls._instances.clear()


def register_provider(provider_class: Type[TTSProvider]) -> Type[TTSProvider]:
    """
    装饰器：自动注册TTS提供商
    
    Args:
        provider_class: TTS提供商类
        
    Returns:
        Type[TTSProvider]: 注册后的提供商类
    """
    TTSFactory.register(provider_class)
    return provider_class
