# neuro_mempalace/__init__.py
"""
Neuro-α × MemPalace 融合模块

整合 MemPalace（中转站）与 Neuro-α（情感引擎）

模块组成：
- memory_unit: 记忆单元数据模型
- memory_injector: 记忆注入器
- memory_retriever: 记忆检索器
- learning_engine: 后台学习引擎

使用示例：
    from neuro_mempalace import MemoryInjector, MemoryRetriever
    
    # 注入记忆
    injector = MemoryInjector()
    injector.inject_dalin("今天天气真好", feeling="开心", intensity=0.8)
    
    # 检索记忆
    retriever = MemoryRetriever()
    results = retriever.search("天气", who="AlfredLi")
"""

from .memory_unit import MemoryUnit, LearningReport, create_memory_unit
from .memory_injector import MemoryInjector, get_injector, quick_inject
from .memory_retriever import MemoryRetriever, get_retriever, quick_search
from .learning_engine import (
    ContinuousLearningEngine,
    LearningTrigger,
    LearningEntry,
    PreferencePattern,
    InteractionInsight,
    get_learning_engine,
    learn_continuous,
    learn_from_feedback
)
from .self_narrative_generator import SelfNarrativeGenerator, get_generator, quick_review, DailyNarrative


__all__ = [
    # 记忆单元
    "MemoryUnit",
    "LearningReport", 
    "create_memory_unit",
    
    # 注入器
    "MemoryInjector",
    "get_injector",
    "quick_inject",
    
    # 检索器
    "MemoryRetriever",
    "get_retriever",
    "quick_search",
    
    # 学习引擎（持续学习）
    "ContinuousLearningEngine",
    "LearningTrigger",
    "LearningEntry",
    "PreferencePattern",
    "InteractionInsight",
    "get_learning_engine",
    "learn_continuous",
    "learn_from_feedback",
    
    # 自我叙事
    "SelfNarrativeGenerator",
    "get_generator",
    "quick_review",
    "DailyNarrative",
]

__version__ = "2.0.0"
__author__ = "Luis & AlfredLi"
