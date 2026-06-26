"""
LLM Memory Integration - 接口定义层
"""

from .search import ISearchEngine
from .memory import IMemoryStore
from .vector import IVectorBackend

__all__ = [
    "ISearchEngine",
    "IMemoryStore",
    "IVectorBackend"
]
