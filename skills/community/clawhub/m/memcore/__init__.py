"""
MemCore Enhanced - 增强版五层记忆系统
=====================================

基于原版 MemCore，新增四大功能：
- Episodic Memory (情景记忆)
- Semantic Compression (语义压缩)
- Memory Triggers (记忆触发器)
- Forgetting Curve (遗忘曲线)

额外增强：
- Persistent Storage (SQLite持久化)
- Vector Knowledge (向量检索)
- Conflict Resolution (冲突解决)
- Confidence Tracking (置信度跟踪)

作者: laojun509 (增强版协助: Hermes Agent)
版本: 0.2.0
许可证: MIT-0
"""

__version__ = "0.2.0"
__author__ = "laojun509"

# 导出核心类
from .memcore_enhanced import MemCoreEnhanced
from .enhanced_memcore import (
    EpisodicMemoryEntry,
    MemoryTrigger,
    SemanticCompressor,
    ForgettingCurveManager,
    MemoryPriority
)
from .confidence_tracker import MemorySource, ConfidenceMetrics
from .conflict_resolver import ConflictStrategy, MemoryConflict

# 使用示例
def quickstart():
    """快速开始示例"""
    print("""
    from memcore_enhanced import MemCoreEnhanced, MemoryPriority
    
    mc = MemCoreEnhanced()
    
    # 记录情景
    mc.record_episode(
        context_summary="用户询问优化建议",
        conclusion="建议添加四个模块",
        related_topics=["MemCore"],
        priority=MemoryPriority.HIGH
    )
    
    # 触发记忆
    result = mc.process_input("我想继续弄MemCore")
    print(result['suggested_context'])
    """)

__all__ = [
    'MemCoreEnhanced',
    'EpisodicMemoryEntry',
    'MemoryTrigger',
    'SemanticCompressor',
    'ForgettingCurveManager',
    'MemoryPriority',
    'MemorySource',
    'ConfidenceMetrics',
    'ConflictStrategy',
    'MemoryConflict',
    'quickstart'
]
