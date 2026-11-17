"""
ecosystem — 生态平台抽象层（v1.0.0）

平台无关的研究内核 + 每生态薄适配器（触发/采集/凭据/状态/输出五件事）。

用法：
    from ecosystem.registry import resolve, list_adapters
    adapter = resolve('ima')
    out = await adapter.run(ResearchInput(subject='量化交易'))
"""

from .base import ResearchInput, ResearchOutput, Config, EcosystemAdapter
from .registry import REGISTRY, get_adapter, resolve, list_adapters

__all__ = [
    'ResearchInput', 'ResearchOutput', 'Config', 'EcosystemAdapter',
    'REGISTRY', 'get_adapter', 'resolve', 'list_adapters',
]
