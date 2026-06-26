"""
规则加载器
从 YAML/JSON 加载规则，验证格式，支持热更新
"""

import yaml
import hashlib
import time
import logging
import fnmatch
import re
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import replace

from .models import Rule, PatternType
from ..platform.path_utils import normalize_path, expand_user, get_config_dir

logger = logging.getLogger(__name__)


class RuleLoader:
    """
    规则加载器
    
    特性：
    1. 多源加载（系统默认 + 用户扩展）
    2. 格式验证
    3. 热更新支持
    4. 错误隔离（单条规则错误不中断整体加载）
    5. 跨平台规则过滤
    """
    
    # 默认规则文件路径
    DEFAULT_SYSTEM_RULES = [
        "~/.openclaw/rules/default_rules.yaml",
        "~/.openclaw/rules/system_rules.yaml",
    ]
    DEFAULT_USER_RULES = "~/.openclaw/rules/user_rules.yaml"
    
    def __init__(self, 
                 system_rules_paths: Optional[List[str]] = None,
                 user_rules_path: Optional[str] = None):
        """
        初始化规则加载器
        
        Args:
            system_rules_paths: 系统规则文件路径列表
            user_rules_path: 用户规则文件路径
        """
        self.system_rules_paths = [
            Path(p).expanduser() for p in (system_rules_paths or self.DEFAULT_SYSTEM_RULES)
        ]
        self.user_rules_path = Path(user_rules_path or self.DEFAULT_USER_RULES).expanduser()
        
        self._rules_cache: Optional[List[Rule]] = None
        self._last_hash: Optional[str] = None
        self._load_timestamp: float = 0
    
    def load_all(self, force_reload: bool = False) -> List[Rule]:
        """
        加载所有规则
        
        Args:
            force_reload: 强制重新加载，无视缓存
            
        Returns:
            按优先级排序的规则列表
        """
        if not force_reload and self._rules_cache is not None:
            # 检查文件是否修改
            current_hash = self._calculate_files_hash()
            if current_hash == self._last_hash:
                return self._rules_cache
        
        rules = []
        errors = []
        
        # 1. 加载系统规则
        for path in self.system_rules_paths:
            if path.exists():
                try:
                    system_rules = self._load_from_file(path)
                    rules.extend(system_rules)
                    logger.info(f"加载系统规则: {path} ({len(system_rules)} 条)")
                except Exception as e:
                    errors.append(f"系统规则加载失败 [{path}]: {e}")
        
        # 2. 加载用户规则
        if self.user_rules_path.exists():
            try:
                user_rules = self._load_from_file(self.user_rules_path)
                rules.extend(user_rules)
                logger.info(f"加载用户规则: {self.user_rules_path} ({len(user_rules)} 条)")
            except Exception as e:
                errors.append(f"用户规则加载失败 [{self.user_rules_path}]: {e}")
        
        # 3. 验证规则
        valid_rules = []
        for rule in rules:
            try:
                self._validate_rule(rule)
                valid_rules.append(rule)
            except ValueError as e:
                errors.append(f"规则 '{rule.id}' 验证失败: {e}")
        
        # 4. 检查 ID 冲突
        seen_ids = set()
        unique_rules = []
        for rule in valid_rules:
            if rule.id in seen_ids:
                errors.append(f"规则 ID 重复: {rule.id}，已跳过")
            else:
                seen_ids.add(rule.id)
                unique_rules.append(rule)
        
        # 5. 过滤当前平台的规则
        platform_rules = self._filter_platform_rules(unique_rules)
        
        # 6. 按优先级排序（高优先级在前）
        platform_rules.sort(key=lambda r: r.priority, reverse=True)
        
        # 7. 编译模式
        compiled_rules = [self._compile_pattern(r) for r in platform_rules]
        
        # 更新缓存
        self._rules_cache = compiled_rules
        self._last_hash = self._calculate_files_hash()
        self._load_timestamp = time.time()
        
        # 记录错误但不中断
        if errors:
            logger.warning(f"规则加载完成，存在 {len(errors)} 个错误:")
            for error in errors:
                logger.warning(f"  - {error}")
        
        logger.info(f"规则加载完成: {len(compiled_rules)} 条有效规则")
        return compiled_rules
    
    def _load_from_file(self, path: Path) -> List[Rule]:
        """从 YAML 文件加载规则"""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'rules' not in data:
            return []
        
        rules = []
        for rule_data in data['rules']:
            try:
                rule = self._parse_rule(rule_data)
                if rule:
                    rules.append(rule)
            except (KeyError, TypeError, ValueError) as e:
                logger.error(f"规则解析错误 [{path}]: {e}, data: {rule_data}")
                continue
        
        return rules
    
    def _parse_rule(self, data: Dict[str, Any]) -> Optional[Rule]:
        """解析单条规则数据"""
        # 处理 level 字段
        level = data.get('level')
        action = data.get('action', 'classify')
        
        # 如果是排除项，level 为 None
        if level == 'EXCLUDE' or action == 'exclude':
            level = None
            action = 'exclude'
        
        return Rule(
            id=data['id'],
            group=data.get('group', 'default'),
            pattern=data['pattern'],
            pattern_type=data['pattern_type'],
            level=level,
            priority=data.get('priority', 50),
            reason=data.get('reason', ''),
            tags=frozenset(data.get('tags', [])),
            exclude=frozenset(data.get('exclude', [])),
            action=action,
            platforms=data.get('platforms')
        )
    
    def _validate_rule(self, rule: Rule) -> None:
        """验证单条规则"""
        # 检查必需字段
        if not rule.id:
            raise ValueError("规则 ID 不能为空")
        
        if not rule.pattern:
            raise ValueError("规则 pattern 不能为空")
        
        # 检查 pattern_type
        valid_types = {t.value for t in PatternType}
        if rule.pattern_type not in valid_types:
            raise ValueError(f"无效的 pattern_type: {rule.pattern_type}，有效值: {valid_types}")
        
        # 检查 level（排除项可以为 None）
        if rule.action == 'classify' and not rule.level:
            raise ValueError("非排除规则必须指定 level")
        
        # 检查 priority 范围
        if not 0 <= rule.priority <= 1000:
            raise ValueError(f"priority 必须在 0-1000 之间: {rule.priority}")
    
    def _filter_platform_rules(self, rules: List[Rule]) -> List[Rule]:
        """过滤出当前平台适用的规则"""
        import sys
        current_platform = sys.platform
        
        filtered = []
        for rule in rules:
            # 获取规则支持的平台（默认所有平台）
            rule_platforms = rule.platforms
            
            if rule_platforms is None:
                # 无平台限制，所有平台适用
                filtered.append(rule)
            elif current_platform in rule_platforms:
                # 当前平台在支持列表中
                filtered.append(rule)
            # 否则跳过此规则
        
        return filtered
    
    def _compile_pattern(self, rule: Rule) -> Rule:
        """编译模式以提高匹配性能"""
        pattern = rule.pattern
        compiled = None
        
        # 展开 ~ 为实际 home 目录
        if pattern.startswith('~/'):
            pattern = expand_user(pattern)
        
        if rule.pattern_type == PatternType.EXACT.value:
            compiled = lambda p, target=pattern: p == target
            
        elif rule.pattern_type == PatternType.GLOB.value:
            # 编译 glob 为正则
            try:
                regex_pattern = fnmatch.translate(pattern)
                compiled_re = re.compile(regex_pattern)
                compiled = lambda p, cre=compiled_re: cre.match(p) is not None
            except re.error as e:
                logger.warning(f"规则 {rule.id} 的 glob 模式编译失败: {e}")
                compiled = lambda p: False
            
        elif rule.pattern_type == PatternType.REGEX.value:
            try:
                compiled_re = re.compile(pattern)
                compiled = lambda p, cre=compiled_re: cre.match(p) is not None
            except re.error as e:
                logger.warning(f"规则 {rule.id} 的正则表达式编译失败: {e}")
                compiled = lambda p: False
            
        elif rule.pattern_type == PatternType.FILENAME.value:
            filename_pattern = pattern[9:] if pattern.startswith('filename:') else pattern
            compiled = lambda p, fp=filename_pattern: fnmatch.fnmatch(Path(p).name, fp)
            
        elif rule.pattern_type == PatternType.EXTENSION.value:
            ext = pattern[4:] if pattern.startswith('ext:') else pattern
            if not ext.startswith('.'):
                ext = '.' + ext
            compiled = lambda p, e=ext: Path(p).suffix == e
            
        elif rule.pattern_type == PatternType.STARTSWITH.value:
            compiled = lambda p, target=pattern: p.startswith(target)
            
        elif rule.pattern_type == PatternType.ENDSWITH.value:
            compiled = lambda p, target=pattern: p.endswith(target)
        
        # 创建新规则，加入编译后的模式
        return replace(rule, _compiled_pattern=compiled)
    
    def _calculate_files_hash(self) -> str:
        """计算规则文件的哈希，用于检测变更"""
        hasher = hashlib.md5()
        
        for path in self.system_rules_paths + [self.user_rules_path]:
            if path.exists():
                try:
                    with open(path, 'rb') as f:
                        hasher.update(f.read())
                except Exception:
                    pass
        
        return hasher.hexdigest()
    
    def invalidate_cache(self) -> None:
        """使缓存失效，下次加载时重新读取"""
        self._rules_cache = None
        logger.info("规则缓存已失效，将在下次加载时重新读取")


class RuleLoaderFactory:
    """规则加载器工厂"""
    
    _instance: Optional[RuleLoader] = None
    
    @classmethod
    def get_loader(cls, 
                   system_rules_paths: Optional[List[str]] = None,
                   user_rules_path: Optional[str] = None) -> RuleLoader:
        """获取规则加载器实例（单例模式）"""
        if cls._instance is None:
            cls._instance = RuleLoader(system_rules_paths, user_rules_path)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """重置单例（主要用于测试）"""
        cls._instance = None