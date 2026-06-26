"""
双轨并行架构 - 融合层模块

本模块包含桶-链融合、交叉验证、摘要生成等功能。
"""

from .bucket_chain_linker import BucketChainLinker, BucketChainLink
from .cross_validator import CrossValidator, ValidationResult
from .multi_dimension_summary import (
    MultiDimensionSummaryGenerator,
    MultiDimensionSummary
)
from .bucket_chain_fusion import BucketChainFusion


__all__ = [
    # 关联
    "BucketChainLinker",
    "BucketChainLink",
    
    # 验证
    "CrossValidator",
    "ValidationResult",
    
    # 摘要
    "MultiDimensionSummaryGenerator",
    "MultiDimensionSummary",
    
    # 融合
    "BucketChainFusion",
]
