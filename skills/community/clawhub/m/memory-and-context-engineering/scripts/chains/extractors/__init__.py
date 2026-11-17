"""
双轨并行架构 - 链提取器模块

本模块包含所有链类型的提取器实现。
"""

from .base_extractor import BaseExtractor, ExtractionResult
from .causal_extractor import CausalExtractor
from .logic_extractor import LogicExtractor
from .operation_extractor import OperationExtractor
from .narrative_extractor import NarrativeExtractor
from .time_extractor import TimeExtractor

__all__ = [
    "BaseExtractor",
    "ExtractionResult",
    "CausalExtractor",
    "LogicExtractor",
    "OperationExtractor",
    "NarrativeExtractor",
    "TimeExtractor",
]