"""
双轨并行架构 - 触发器模块

本模块包含协同提取触发器等功能。
"""

from .coordinated_extraction_trigger import (
    CoordinatedExtractionTrigger,
    ExtractionAction
)


__all__ = [
    "CoordinatedExtractionTrigger",
    "ExtractionAction",
]
