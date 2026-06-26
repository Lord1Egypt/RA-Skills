"""
Multi-LLM Adapter Library

Universal adapter for multiple LLM providers
"""

from .client import LLMClient, Message, LLMResponse, ProviderConfig
from .client import OpenAIProvider, AnthropicProvider, OllamaProvider

__version__ = "1.0.0"
__all__ = [
    'LLMClient', 'Message', 'LLMResponse', 'ProviderConfig',
    'OpenAIProvider', 'AnthropicProvider', 'OllamaProvider'
]
