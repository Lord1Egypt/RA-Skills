"""
数据分级规则引擎 (L2)

为 OpenClaw 提供自动化的数据安全分级能力

主要功能：
- 路径模式匹配（glob/exact/extension/filename）
- 优先级冲突解决
- 排除项管理
- 内存缓存加速
- 跨平台支持（Windows/macOS/Linux）

使用示例：
    from internal_control.rules import ClassificationEngine
    
    engine = ClassificationEngine()
    result = engine.classify_sync("~/.ssh/id_rsa")
    print(result.level)  # L5-SECRET
"""

from .models import (
    Rule,
    MatchResult,
    ClassificationResult,
    ClassificationEntry,
    DirectoryClassification,
    ExclusionRule,
    ExclusionType,
    DataLevel,
    RuleStats,
    CacheStats,
    get_level_strictness,
    is_more_strict,
    is_level_upgrade,
)

from .loader import RuleLoader, RuleLoaderFactory
from .index import RuleIndex
from .matcher import RuleMatcher
from .exclusions import ExclusionManager
from .cache import ClassificationCache
from .engine import ClassificationEngine

__version__ = "0.0.5"
__all__ = [
    # 核心类
    'ClassificationEngine',
    'RuleLoader',
    'RuleLoaderFactory',
    'RuleIndex',
    'RuleMatcher',
    'ExclusionManager',
    'ClassificationCache',
    
    # 数据模型
    'Rule',
    'MatchResult',
    'ClassificationResult',
    'ClassificationEntry',
    'DirectoryClassification',
    'ExclusionRule',
    'ExclusionType',
    'DataLevel',
    'RuleStats',
    'CacheStats',
    
    # 工具函数
    'get_level_strictness',
    'is_more_strict',
    'is_level_upgrade',
]