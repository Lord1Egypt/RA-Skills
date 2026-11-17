"""
双轨并行架构 - 链模块

本模块包含所有链类型、链缓冲区以及链提取器的实现。
"""

from .base_chain import (
    BaseExtractedChain,
    ChainType
)

from .causal_chain import (
    ExtractedCausalChain,
    ProblemNode,
    CauseNode,
    CausalRelation,
    SolutionNode
)

from .logic_chain import ExtractedLogicChain

from .operation_chain import ExtractedOperationChain

from .narrative_chain import ExtractedNarrativeChain

from .time_chain import ExtractedTimeChain

from .chain_buffer import ChainBuffer

from .chain_extractor import ChainExtractor

from .extractors import (
    BaseExtractor,
    CausalExtractor,
    LogicExtractor,
    OperationExtractor,
    NarrativeExtractor,
    TimeExtractor,
    ExtractionResult,
)


__all__ = [
    # 基类
    "BaseExtractedChain",
    "ChainType",

    # 链类型
    "ExtractedCausalChain",
    "ProblemNode",
    "CauseNode",
    "CausalRelation",
    "SolutionNode",
    "ExtractedLogicChain",
    "ExtractedOperationChain",
    "ExtractedNarrativeChain",
    "ExtractedTimeChain",

    # 缓冲区
    "ChainBuffer",

    # 提取器
    "ChainExtractor",
    "BaseExtractor",
    "CausalExtractor",
    "LogicExtractor",
    "OperationExtractor",
    "NarrativeExtractor",
    "TimeExtractor",
    "ExtractionResult",
]