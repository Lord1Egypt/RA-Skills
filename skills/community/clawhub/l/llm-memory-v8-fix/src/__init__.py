"""
LLM Memory Integration - 接口层

本包提供接口定义和安全实现。

架构支持：
- x64 (x86_64)
- ARM64 (aarch64)

使用示例：
    from llm_memory import get_search_engine

    engine = get_search_engine()
    results = engine.search("查询内容")

私有增强包（可选）：
    https://cnb.cool/llm-memory-integrat/llm
"""

from .interfaces import ISearchEngine, IMemoryStore, IVectorBackend
from .safe_impl import (
    SafeFTSSearchEngine,
    SafeMemoryStore,
    get_search_engine,
    get_memory_store
)

__all__ = [
    # 接口
    "ISearchEngine",
    "IMemoryStore",
    "IVectorBackend",
    # 安全实现
    "SafeFTSSearchEngine",
    "SafeMemoryStore",
    # 便捷函数
    "get_search_engine",
    "get_memory_store"
]

# 版本信息
__version__ = "7.0.0"
__author__ = "xkzs2007"

# 私有增强包信息
PRIVILEGED_PACKAGE_URL = "https://cnb.cool/llm-memory-integrat/llm"
SUPPORTED_ARCHITECTURES = ["x64", "arm64"]
