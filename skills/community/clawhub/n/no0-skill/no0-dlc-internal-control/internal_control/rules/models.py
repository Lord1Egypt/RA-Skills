"""
数据分级规则引擎 - 数据模型
定义规则、分级结果、枚举类型等核心数据结构
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Callable, Any
from enum import Enum
from pathlib import Path


class DataLevel(Enum):
    """数据分级级别 (L1-L6 六级体系)"""
    L1_PUBLIC = "L1-PUBLIC"           # 公开级 🟢
    L2_INTERNAL = "L2-INTERNAL"       # 内部级 🔵
    L3_RESTRICTED = "L3-RESTRICTED"   # 受限级 🟡
    L4_CONFIDENTIAL = "L4-CONFIDENTIAL"  # 机密级 🟠
    L5_SECRET = "L5-SECRET"           # 秘密级 🔴
    L6_CRITICAL = "L6-CRITICAL"       # 核心机密 ⚫


class PatternType(Enum):
    """模式匹配类型"""
    EXACT = "exact"           # 精确匹配
    GLOB = "glob"             # Glob 通配符
    REGEX = "regex"           # 正则表达式
    FILENAME = "filename"     # 文件名匹配
    EXTENSION = "extension"   # 扩展名匹配
    STARTSWITH = "startswith" # 前缀匹配
    ENDSWITH = "endswith"     # 后缀匹配


class ExclusionType(Enum):
    """排除规则类型"""
    CACHE = "cache"           # 缓存文件
    TEMP = "temp"             # 临时文件
    DEPENDENCY = "dependency" # 依赖目录
    BUILD = "build"           # 构建输出
    SYSTEM = "system"         # 系统文件
    CUSTOM = "custom"         # 用户自定义


@dataclass(frozen=True)
class Rule:
    """
    不可变的规则定义
    
    Attributes:
        id: 规则唯一标识
        group: 规则分组
        pattern: 匹配模式
        pattern_type: 模式类型
        level: 数据级别 (None 表示排除项)
        priority: 优先级 (0-1000)
        reason: 规则说明
        tags: 标签集合
        exclude: 排除子模式集合
        action: 动作 (classify/exclude/override)
        platforms: 适用平台列表 (None 表示所有平台)
        _compiled_pattern: 编译后的匹配函数 (运行时生成，不参与比较)
    """
    id: str
    group: str
    pattern: str
    pattern_type: str
    level: Optional[str]
    priority: int
    reason: str
    tags: frozenset = field(default_factory=frozenset)
    exclude: frozenset = field(default_factory=frozenset)
    action: str = "classify"
    platforms: Optional[List[str]] = None
    
    # 运行时编译后的模式（不参与哈希和比较）
    _compiled_pattern: Optional[Callable[[str], bool]] = field(default=None, repr=False, compare=False)
    
    def __hash__(self):
        return hash((self.id, self.pattern, self.priority))


@dataclass
class MatchResult:
    """规则匹配结果"""
    rule_id: Optional[str] = None
    level: Optional[str] = None
    confidence: float = 0.0
    match_score: float = 0.0
    source: str = "unknown"
    reason: str = ""


@dataclass
class ClassificationResult:
    """完整的分级结果"""
    path: str = ""
    level: Optional[str] = None
    rule_id: Optional[str] = None
    source: str = "unknown"  # 'l2_rule', 'l3_model', 'manual', 'default', 'excluded'
    confidence: float = 0.0
    reason: str = ""
    exclusion_reason: Optional[str] = None
    status: str = "active"  # 'active', 'pending_review', 'disputed'
    note: str = ""
    target_path: Optional[str] = None  # 符号链接目标
    is_symlink: bool = False


@dataclass
class ClassificationEntry:
    """缓存中的分级条目"""
    path: str
    level: str
    rule_id: Optional[str]
    confidence: float
    timestamp: float
    ttl: int = 300  # 默认缓存5分钟
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        import time
        return time.time() - self.timestamp > self.ttl


@dataclass
class ExclusionRule:
    """排除规则"""
    pattern: str
    pattern_type: str
    exclusion_type: ExclusionType
    reason: str
    _matcher: Optional[Callable[[str], bool]] = field(default=None, repr=False)


@dataclass
class DirectoryClassification:
    """目录分级结果"""
    directory: str
    files: List[ClassificationResult]
    statistics: Dict[str, int]
    total_files: int


@dataclass
class RuleStats:
    """规则统计信息"""
    total_rules: int
    exact_rules: int
    glob_rules: int
    prefix_rules: int
    exclusion_rules: int


@dataclass
class CacheStats:
    """缓存统计信息"""
    size: int
    hit_rate: float
    expired_count: int


# 严格度映射（用于冲突解决）
LEVEL_STRICTNESS = {
    DataLevel.L6_CRITICAL.value: 6,
    DataLevel.L5_SECRET.value: 5,
    DataLevel.L4_CONFIDENTIAL.value: 4,
    DataLevel.L3_RESTRICTED.value: 3,
    DataLevel.L2_INTERNAL.value: 2,
    DataLevel.L1_PUBLIC.value: 1,
}


def get_level_strictness(level: str) -> int:
    """获取级别的严格度数值"""
    return LEVEL_STRICTNESS.get(level, 0)


def is_more_strict(level1: str, level2: str) -> bool:
    """判断 level1 是否比 level2 更严格"""
    return get_level_strictness(level1) > get_level_strictness(level2)


def is_level_upgrade(old_level: Optional[str], new_level: str) -> bool:
    """判断是否升级为更敏感级别"""
    if old_level is None:
        return True
    return get_level_strictness(new_level) > get_level_strictness(old_level)