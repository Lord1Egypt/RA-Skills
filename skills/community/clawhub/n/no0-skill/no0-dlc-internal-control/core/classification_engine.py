"""
内控 Skills - 数据分级规则引擎

提供文件路径的数据分级计算能力 (L2确定性规则层)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple, Callable, Any
from pathlib import Path
from enum import Enum
import yaml
import hashlib
import time
import fnmatch
import re
import os
import sys
from collections import defaultdict
import asyncio
from datetime import datetime

# ========== 数据模型 ==========

class DataLevel(Enum):
    """数据分级级别"""
    PUBLIC = "PUBLIC"       # 公开
    INTERNAL = "INTERNAL"   # 内部
    PRIVATE_R = "PRIVATE-R" # 私密-读取受限
    PRIVATE_W = "PRIVATE-W" # 私密-写入受限
    PRIVATE_B = "PRIVATE-B" # 私密-敏感业务
    PRIVATE_C = "PRIVATE-C" # 私密-最高机密


@dataclass(frozen=True)
class Rule:
    """不可变的规则定义"""
    id: str
    group: str
    pattern: str
    pattern_type: str  # exact, glob, regex, filename, extension, startswith, endswith
    level: Optional[str]  # None 表示排除项
    priority: int
    reason: str
    tags: frozenset = field(default_factory=frozenset)
    exclude: frozenset = field(default_factory=frozenset)  # 排除子模式
    action: str = "classify"  # classify, exclude, override
    platforms: Optional[List[str]] = None  # 支持的平台列表，None表示所有平台
    
    # 运行时编译后的模式（不参与哈希）
    _compiled_pattern: Any = field(default=None, repr=False, compare=False)
    
    def __hash__(self):
        return hash((self.id, self.pattern, self.priority))


@dataclass
class MatchResult:
    """匹配结果"""
    level: Optional[str]
    rule_id: Optional[str] = None
    source: str = "unknown"
    confidence: float = 0.0
    reason: str = ""


@dataclass
class ClassificationResult:
    """分级结果"""
    path: str
    level: Optional[str]
    source: str
    rule_id: Optional[str] = None
    confidence: float = 0.0
    reason: str = ""
    exclusion_reason: Optional[str] = None
    note: str = ""


# ========== 平台工具 ==========

class PlatformDetector:
    """平台检测器"""
    
    @staticmethod
    def current() -> str:
        """获取当前平台标识"""
        if sys.platform == 'win32':
            return 'win32'
        elif sys.platform == 'darwin':
            return 'darwin'
        else:
            return 'linux'
    
    @staticmethod
    def is_windows() -> bool:
        return sys.platform == 'win32'
    
    @staticmethod
    def is_macos() -> bool:
        return sys.platform == 'darwin'
    
    @staticmethod
    def is_linux() -> bool:
        return sys.platform.startswith('linux')


class PlatformPaths:
    """跨平台路径处理工具"""
    
    @staticmethod
    def normalize_path(path: Union[str, Path]) -> str:
        """标准化路径（跨平台统一格式）"""
        if isinstance(path, str):
            if path.startswith('~'):
                path = os.path.expanduser(path)
            path = Path(path)
        
        absolute = path.resolve()
        normalized = str(absolute).replace('\\', '/')
        return normalized
    
    @staticmethod
    def get_config_dir() -> Path:
        """获取配置目录"""
        if PlatformDetector.is_windows():
            app_data = os.environ.get('APPDATA')
            if app_data:
                return Path(app_data) / 'OpenClaw'
            return Path.home() / 'AppData' / 'Roaming' / 'OpenClaw'
        elif PlatformDetector.is_macos():
            return Path.home() / 'Library' / 'Application Support' / 'OpenClaw'
        else:
            xdg_config = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config:
                return Path(xdg_config) / 'openclaw'
            return Path.home() / '.config' / 'openclaw'
    
    @staticmethod
    def get_data_dir() -> Path:
        """获取数据目录"""
        if PlatformDetector.is_windows():
            local_app_data = os.environ.get('LOCALAPPDATA')
            if local_app_data:
                return Path(local_app_data) / 'OpenClaw'
            return Path.home() / 'AppData' / 'Local' / 'OpenClaw'
        elif PlatformDetector.is_macos():
            return Path.home() / 'Library' / 'Application Support' / 'OpenClaw'
        else:
            xdg_data = os.environ.get('XDG_DATA_HOME')
            if xdg_data:
                return Path(xdg_data) / 'openclaw'
            return Path.home() / '.local' / 'share' / 'openclaw'
    
    @staticmethod
    def path_matches(pattern: str, target: str) -> bool:
        """跨平台路径匹配"""
        if PlatformDetector.is_windows():
            return fnmatch.fnmatch(target.lower(), pattern.lower())
        else:
            return fnmatch.fnmatch(target, pattern)


# ========== 排除项管理 ==========

class ExclusionType(Enum):
    """排除类型"""
    CACHE = "cache"
    TEMP = "temp"
    DEPENDENCY = "dependency"
    BUILD = "build"
    SYSTEM = "system"
    CUSTOM = "custom"


@dataclass
class ExclusionRule:
    """排除规则"""
    pattern: str
    pattern_type: str
    exclusion_type: ExclusionType
    reason: str
    _matcher: Optional[Callable] = None


class ExclusionManager:
    """排除项管理器"""
    
    # 默认排除规则
    DEFAULT_EXCLUSIONS = [
        # 缓存
        ExclusionRule("**/.cache/**", "glob", ExclusionType.CACHE, "通用缓存目录"),
        ExclusionRule("**/__pycache__/**", "glob", ExclusionType.CACHE, "Python缓存"),
        ExclusionRule("**/.pytest_cache/**", "glob", ExclusionType.CACHE, "Pytest缓存"),
        ExclusionRule("**/node_modules/**", "glob", ExclusionType.DEPENDENCY, "Node依赖"),
        
        # Git 内部
        ExclusionRule("**/.git/objects/**", "glob", ExclusionType.CACHE, "Git对象"),
        ExclusionRule("**/.git/hooks/**", "glob", ExclusionType.SYSTEM, "Git hooks"),
        
        # 系统文件
        ExclusionRule("**/.DS_Store", "glob", ExclusionType.SYSTEM, "macOS系统文件"),
        ExclusionRule("**/Thumbs.db", "glob", ExclusionType.SYSTEM, "Windows缩略图"),
        
        # 临时文件
        ExclusionRule("**/*.tmp", "glob", ExclusionType.TEMP, "临时文件"),
        ExclusionRule("**/*.temp", "glob", ExclusionType.TEMP, "临时文件"),
        ExclusionRule("**/~$*", "glob", ExclusionType.TEMP, "Office临时文件"),
        
        # 构建输出
        ExclusionRule("**/build/**", "glob", ExclusionType.BUILD, "构建目录"),
        ExclusionRule("**/dist/**", "glob", ExclusionType.BUILD, "分发目录"),
        ExclusionRule("**/*.egg-info/**", "glob", ExclusionType.BUILD, "Python包信息"),
        ExclusionRule("**/.tox/**", "glob", ExclusionType.BUILD, "Tox测试环境"),
        
        # 日志
        ExclusionRule("**/*.log", "glob", ExclusionType.CACHE, "日志文件（过大）"),
    ]
    
    # Windows 特定排除规则
    WINDOWS_EXCLUSIONS = [
        ExclusionRule("**/Thumbs.db", "glob", ExclusionType.SYSTEM, "Windows 缩略图数据库"),
        ExclusionRule("**/desktop.ini", "glob", ExclusionType.SYSTEM, "Windows 文件夹配置"),
        ExclusionRule("**/NTUSER.DAT*", "glob", ExclusionType.SYSTEM, "Windows 用户注册表"),
        ExclusionRule("**/pagefile.sys", "glob", ExclusionType.SYSTEM, "Windows 页面文件"),
        ExclusionRule("**/hiberfil.sys", "glob", ExclusionType.SYSTEM, "Windows 休眠文件"),
        ExclusionRule("**/$RECYCLE.BIN/**", "glob", ExclusionType.SYSTEM, "Windows 回收站"),
        ExclusionRule("~/AppData/Local/Temp/**", "glob", ExclusionType.TEMP, "Windows 临时目录"),
        ExclusionRule("**/Windows/Installer/**", "glob", ExclusionType.CACHE, "Windows 安装缓存"),
        ExclusionRule("**/Windows/SoftwareDistribution/**", "glob", ExclusionType.CACHE, "Windows 更新缓存"),
    ]
    
    def __init__(self):
        self.rules: List[ExclusionRule] = list(self.DEFAULT_EXCLUSIONS)
        
        if PlatformDetector.is_windows():
            self.rules.extend(self.WINDOWS_EXCLUSIONS)
        
        self._custom_rules: List[ExclusionRule] = []
        self._build_index()
    
    def _build_index(self):
        """构建排除匹配索引"""
        for rule in self.rules:
            if rule.pattern_type == 'glob':
                regex = fnmatch.translate(rule.pattern)
                rule._matcher = re.compile(regex).match
            elif rule.pattern_type == 'exact':
                rule._matcher = lambda p, target=rule.pattern: p == target
            elif rule.pattern_type == 'regex':
                compiled = re.compile(rule.pattern)
                rule._matcher = compiled.match
    
    def is_excluded(self, file_path: str) -> Optional[ExclusionRule]:
        """检查路径是否被排除"""
        normalized = PlatformPaths.normalize_path(file_path)
        for rule in self.rules:
            if rule._matcher and rule._matcher(normalized):
                return rule
        return None
    
    def add_custom_exclusion(self, pattern: str, reason: str) -> None:
        """添加用户自定义排除规则"""
        rule = ExclusionRule(
            pattern=pattern,
            pattern_type='glob',
            exclusion_type=ExclusionType.CUSTOM,
            reason=reason
        )
        self._custom_rules.append(rule)
        self.rules.append(rule)
        self._build_index()
    
    def get_exclusion_reason(self, file_path: str) -> Optional[str]:
        """获取排除原因"""
        rule = self.is_excluded(file_path)
        return rule.reason if rule else None


# ========== 规则加载器 ==========

class RuleLoader:
    """规则加载器 - 从YAML加载规则，支持热更新"""
    
    def __init__(self, 
                 system_rules_path: str = None,
                 user_rules_path: str = None):
        # 默认路径
        config_dir = PlatformPaths.get_config_dir()
        self.system_rules_path = Path(system_rules_path) if system_rules_path else config_dir / "rules" / "system_rules.yaml"
        self.user_rules_path = Path(user_rules_path) if user_rules_path else config_dir / "rules" / "user_rules.yaml"
        
        self._rules_cache: Optional[List[Rule]] = None
        self._last_hash: Optional[str] = None
        self._load_timestamp: float = 0
    
    def load_all(self, force_reload: bool = False) -> List[Rule]:
        """加载所有规则"""
        if not force_reload and self._rules_cache is not None:
            current_hash = self._calculate_files_hash()
            if current_hash == self._last_hash:
                return self._rules_cache
        
        rules = []
        errors = []
        
        # 加载系统规则
        if self.system_rules_path.exists():
            try:
                system_rules = self._load_from_file(self.system_rules_path)
                rules.extend(system_rules)
            except Exception as e:
                errors.append(f"系统规则加载失败: {e}")
        
        # 加载用户规则
        if self.user_rules_path.exists():
            try:
                user_rules = self._load_from_file(self.user_rules_path)
                rules.extend(user_rules)
            except Exception as e:
                errors.append(f"用户规则加载失败: {e}")
        
        # 验证和编译规则
        valid_rules = []
        for rule in rules:
            try:
                self._validate_rule(rule)
                compiled_rule = self._compile_pattern(rule)
                valid_rules.append(compiled_rule)
            except ValueError as e:
                errors.append(f"规则 '{rule.id}' 验证失败: {e}")
        
        # 平台过滤
        current_platform = PlatformDetector.current()
        filtered_rules = [
            r for r in valid_rules 
            if r.platforms is None or current_platform in r.platforms
        ]
        
        # 按优先级排序
        filtered_rules.sort(key=lambda r: r.priority, reverse=True)
        
        # 更新缓存
        self._rules_cache = filtered_rules
        self._last_hash = self._calculate_files_hash()
        self._load_timestamp = time.time()
        
        if errors:
            print(f"规则加载完成，存在 {len(errors)} 个错误")
        
        return filtered_rules
    
    def _load_from_file(self, path: Path) -> List[Rule]:
        """从YAML文件加载规则"""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'rules' not in data:
            return []
        
        rules = []
        for rule_data in data['rules']:
            try:
                rule = Rule(
                    id=rule_data['id'],
                    group=rule_data.get('group', 'default'),
                    pattern=rule_data['pattern'],
                    pattern_type=rule_data['pattern_type'],
                    level=rule_data.get('level'),
                    priority=rule_data.get('priority', 50),
                    reason=rule_data.get('reason', ''),
                    tags=frozenset(rule_data.get('tags', [])),
                    exclude=frozenset(rule_data.get('exclude', [])),
                    action=rule_data.get('action', 'classify'),
                    platforms=rule_data.get('platforms')
                )
                rules.append(rule)
            except (KeyError, TypeError) as e:
                print(f"规则解析错误: {e}, data: {rule_data}")
                continue
        
        return rules
    
    def _validate_rule(self, rule: Rule) -> None:
        """验证单条规则"""
        if not rule.id:
            raise ValueError("规则 ID 不能为空")
        
        if not rule.pattern:
            raise ValueError("规则 pattern 不能为空")
        
        valid_types = {'exact', 'glob', 'regex', 'filename', 'extension', 'startswith', 'endswith'}
        if rule.pattern_type not in valid_types:
            raise ValueError(f"无效的 pattern_type: {rule.pattern_type}")
        
        if rule.action == 'classify' and not rule.level:
            raise ValueError("非排除规则必须指定 level")
        
        if not 0 <= rule.priority <= 1000:
            raise ValueError(f"priority 必须在 0-1000 之间: {rule.priority}")
    
    def _compile_pattern(self, rule: Rule) -> Rule:
        """编译模式以提高匹配性能"""
        compiled = None
        pattern = rule.pattern
        
        # 展开 ~ 为实际 home 目录
        if pattern.startswith('~/'):
            pattern = str(Path.home()) + pattern[1:]
        
        if rule.pattern_type == 'exact':
            compiled = lambda p, target=pattern: p == target
            
        elif rule.pattern_type == 'glob':
            regex_pattern = fnmatch.translate(pattern)
            compiled_re = re.compile(regex_pattern)
            compiled = lambda p, regex=compiled_re: regex.match(p) is not None
            
        elif rule.pattern_type == 'regex':
            compiled_re = re.compile(pattern)
            compiled = lambda p, regex=compiled_re: regex.match(p) is not None
            
        elif rule.pattern_type == 'filename':
            filename_pattern = pattern[9:] if pattern.startswith('filename:') else pattern
            compiled = lambda p, pat=filename_pattern: fnmatch.fnmatch(Path(p).name, pat)
            
        elif rule.pattern_type == 'extension':
            ext = pattern[4:] if pattern.startswith('ext:') else pattern
            if not ext.startswith('.'):
                ext = '.' + ext
            compiled = lambda p, ext=ext: Path(p).suffix == ext
            
        elif rule.pattern_type == 'startswith':
            compiled = lambda p, prefix=pattern: p.startswith(prefix)
            
        elif rule.pattern_type == 'endswith':
            compiled = lambda p, suffix=pattern: p.endswith(suffix)
        
        # 创建新规则，使用展开后的pattern，加入编译后的模式
        return Rule(
            id=rule.id,
            group=rule.group,
            pattern=pattern,  # 使用展开后的路径
            pattern_type=rule.pattern_type,
            level=rule.level,
            priority=rule.priority,
            reason=rule.reason,
            tags=rule.tags,
            exclude=rule.exclude,
            action=rule.action,
            platforms=rule.platforms,
            _compiled_pattern=compiled
        )
    
    def _calculate_files_hash(self) -> str:
        """计算规则文件的哈希"""
        hasher = hashlib.md5()
        
        for path in [self.system_rules_path, self.user_rules_path]:
            if path.exists():
                with open(path, 'rb') as f:
                    hasher.update(f.read())
        
        return hasher.hexdigest()


# ========== 规则索引 ==========

class RuleIndex:
    """规则索引器 - 加速匹配查询"""
    
    def __init__(self):
        # 精确匹配
        self.exact_rules: Dict[str, Rule] = {}
        
        # 前缀匹配
        self.prefix_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 文件名匹配
        self.filename_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 扩展名匹配
        self.extension_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 通用 glob 规则
        self.glob_rules: List[Rule] = []
        
        # 排除规则单独存放
        self.exclusion_rules: List[Rule] = []
        
        # 所有规则
        self.rules: List[Rule] = []
    
    def build(self, rules: List[Rule]) -> None:
        """从规则列表构建索引"""
        self.__init__()
        self.rules = rules
        
        for rule in rules:
            if rule.action == 'exclude':
                self.exclusion_rules.append(rule)
                continue
            
            if rule.pattern_type == 'exact':
                self.exact_rules[rule.pattern] = rule
                
            elif rule.pattern_type in ('startswith', 'glob'):
                prefix = self._extract_prefix(rule.pattern)
                if prefix and len(prefix) > 3:
                    self.prefix_rules[prefix].append(rule)
                else:
                    self.glob_rules.append(rule)
                    
            elif rule.pattern_type == 'filename':
                pattern = rule.pattern[9:] if rule.pattern.startswith('filename:') else rule.pattern
                self.filename_rules[pattern].append(rule)
                
            elif rule.pattern_type == 'extension':
                ext = rule.pattern[4:] if rule.pattern.startswith('ext:') else rule.pattern
                self.extension_rules[ext].append(rule)
                
            else:
                self.glob_rules.append(rule)
    
    def _extract_prefix(self, pattern: str) -> Optional[str]:
        """从 glob 模式中提取可索引的前缀"""
        special_chars = set('*?[]{}')
        prefix = ''
        for char in pattern:
            if char in special_chars:
                break
            prefix += char
        return prefix if len(prefix) > 3 else None
    
    def query(self, file_path: str) -> List[Tuple[Rule, float]]:
        """查询匹配的规则"""
        matches = []
        
        # 精确匹配
        if file_path in self.exact_rules:
            matches.append((self.exact_rules[file_path], 1.0))
        
        # 前缀匹配
        for prefix, rules in self.prefix_rules.items():
            if file_path.startswith(prefix):
                for rule in rules:
                    score = self._calculate_match_score(file_path, rule)
                    if score > 0:
                        matches.append((rule, score))
        
        # 文件名匹配
        filename = Path(file_path).name
        for pattern, rules in self.filename_rules.items():
            if fnmatch.fnmatch(filename, pattern):
                for rule in rules:
                    matches.append((rule, 0.7))
        
        # 扩展名匹配
        ext = Path(file_path).suffix
        if ext in self.extension_rules:
            for rule in self.extension_rules[ext]:
                matches.append((rule, 0.5))
        
        # 通用 glob 规则
        for rule in self.glob_rules:
            score = self._calculate_match_score(file_path, rule)
            if score > 0:
                matches.append((rule, score))
        
        return matches
    
    def _calculate_match_score(self, path: str, rule: Rule) -> float:
        """计算匹配分数"""
        if rule._compiled_pattern is None:
            return 0.0
        
        if not rule._compiled_pattern(path):
            return 0.0
        
        # 检查排除项
        for exclude_pattern in rule.exclude:
            if fnmatch.fnmatch(path, exclude_pattern):
                return 0.0
        
        # 基于匹配类型计算分数
        if rule.pattern_type == 'exact':
            return 1.0
        elif rule.pattern_type == 'glob':
            depth = self._calculate_pattern_depth(rule.pattern)
            return min(0.95, 0.5 + depth * 0.1)
        elif rule.pattern_type == 'filename':
            return 0.7
        elif rule.pattern_type == 'extension':
            return 0.5
        
        return 0.6
    
    def _calculate_pattern_depth(self, pattern: str) -> int:
        """计算模式深度"""
        clean_pattern = pattern.replace('*', '').replace('?', '').replace('**', '')
        return clean_pattern.count('/')


# ========== 匹配器 ==========

class OptimizedMatcher:
    """优化的规则匹配器"""
    
    def __init__(self, index: RuleIndex):
        self.index = index
        self._normalize_cache: Dict[str, str] = {}
        self._cache_size_limit = 10000
    
    def match(self, file_path: str) -> MatchResult:
        """单路径匹配"""
        # 标准化路径
        normalized = self._normalize_path(file_path)
        
        # 查询索引
        matches = self.index.query(normalized)
        
        if not matches:
            return MatchResult(
                level=None,
                source='no_match',
                confidence=0.0
            )
        
        # 冲突解决
        best_rule, confidence = self._resolve_conflicts(matches)
        
        return MatchResult(
            level=best_rule.level,
            rule_id=best_rule.id,
            source='l2_rule',
            confidence=confidence,
            reason=best_rule.reason
        )
    
    def _normalize_path(self, path: str) -> str:
        """标准化路径（带缓存）"""
        if path in self._normalize_cache:
            return self._normalize_cache[path]
        
        result = PlatformPaths.normalize_path(path)
        
        # 更新缓存
        if len(self._normalize_cache) >= self._cache_size_limit:
            keys = list(self._normalize_cache.keys())[:self._cache_size_limit//2]
            for k in keys:
                del self._normalize_cache[k]
        
        self._normalize_cache[path] = result
        return result
    
    def _resolve_conflicts(self, matches: List[Tuple[Rule, float]]) -> Tuple[Rule, float]:
        """冲突解决"""
        if not matches:
            raise ValueError("No matches to resolve")
        
        if len(matches) == 1:
            return matches[0]
        
        # 按优先级降序
        matches.sort(key=lambda x: (x[0].priority, x[1]), reverse=True)
        
        best_priority = matches[0][0].priority
        best_score = matches[0][1]
        
        # 收集同优先级同分数的规则
        tied = [(r, s) for r, s in matches 
                if r.priority == best_priority and s == best_score]
        
        if len(tied) == 1:
            return tied[0]
        
        # 选择更严格的级别
        strictness = {
            'PRIVATE-C': 5, 'PRIVATE-B': 4, 'PRIVATE-W': 3,
            'PRIVATE-R': 2, 'INTERNAL': 1, 'PUBLIC': 0
        }
        
        return max(tied, key=lambda x: strictness.get(x[0].level, 0))


# ========== 核心引擎 ==========

class ClassificationEngine:
    """分级规则引擎（对外统一接口）"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.exclusion_manager = ExclusionManager()
        self.rule_loader = RuleLoader()
        self.rule_index = RuleIndex()
        self.matcher = None
        
        # 初始化
        self._refresh_rules()
    
    def _refresh_rules(self):
        """刷新规则"""
        rules = self.rule_loader.load_all()
        self.rule_index.build(rules)
        self.matcher = OptimizedMatcher(self.rule_index)
    
    def classify(self, file_path: str) -> ClassificationResult:
        """分级单一路径"""
        # 阶段 1: 排除检查
        exclusion = self.exclusion_manager.is_excluded(file_path)
        if exclusion:
            return ClassificationResult(
                path=file_path,
                level=None,
                source='excluded',
                exclusion_reason=exclusion.reason,
                confidence=1.0
            )
        
        # 阶段 2: L2 规则匹配
        l2_result = self.matcher.match(file_path)
        
        return ClassificationResult(
            path=file_path,
            level=l2_result.level,
            source=l2_result.source,
            rule_id=l2_result.rule_id,
            confidence=l2_result.confidence,
            reason=l2_result.reason
        )
    
    def classify_batch(self, paths: List[str]) -> List[ClassificationResult]:
        """批量分级"""
        return [self.classify(p) for p in paths]
    
    def get_rule_stats(self) -> Dict:
        """获取规则统计"""
        return {
            'total_rules': len(self.rule_index.rules),
            'exact_rules': len(self.rule_index.exact_rules),
            'glob_rules': len(self.rule_index.glob_rules),
            'prefix_rules': len(self.rule_index.prefix_rules),
            'exclusion_rules': len(self.exclusion_manager.rules)
        }
    
    def reload_rules(self) -> None:
        """重新加载规则"""
        self._refresh_rules()


# 类型提示导入
from typing import Union