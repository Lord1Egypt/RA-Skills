"""
LLM Memory Integration - 接口定义
纯接口包，无实现代码
"""

from .memory import MemoryInterface
from .search import SearchInterface
from .vector import VectorInterface

__all__ = ["MemoryInterface", "SearchInterface", "VectorInterface"]
