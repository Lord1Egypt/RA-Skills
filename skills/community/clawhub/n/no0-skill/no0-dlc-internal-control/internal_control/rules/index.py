"""
规则索引器
为快速匹配构建索引（Hash Map + 前缀索引 + 扩展名索引）
"""

import fnmatch
import re
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict
from pathlib import Path

from .models import Rule, MatchResult
from ..platform.path_utils import normalize_path


class RuleIndex:
    """
    规则索引器 - 加速匹配查询
    
    策略：
    1. 精确匹配规则 → Hash Map (O(1))
    2. 前缀匹配规则 → 前缀索引 (O(prefix_length))
    3. 后缀/扩展名规则 → 反向索引
    4. 通用 glob 规则 → 列表遍历（兜底）
    """
    
    def __init__(self):
        # 精确匹配: 完整路径 -> 规则
        self.exact_rules: Dict[str, Rule] = {}
        
        # 前缀匹配: 前缀 -> 规则列表
        self.prefix_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 文件名匹配: 文件名模式 -> 规则列表
        self.filename_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 扩展名匹配: 扩展名 -> 规则列表
        self.extension_rules: Dict[str, List[Rule]] = defaultdict(list)
        
        # 通用 glob 规则
        self.glob_rules: List[Rule] = []
        
        # 排除规则单独存放
        self.exclusion_rules: List[Rule] = []
        
        # 所有规则（用于统计）
        self.all_rules: List[Rule] = []
    
    def build(self, rules: List[Rule]) -> None:
        """从规则列表构建索引"""
        # 重置
        self.__init__()
        self.all_rules = rules
        
        for rule in rules:
            # 排除项单独处理
            if rule.action == 'exclude':
                self.exclusion_rules.append(rule)
                continue
            
            # 按 pattern_type 分类
            if rule.pattern_type == 'exact':
                # 标准化路径作为键
                normalized_pattern = normalize_path(rule.pattern)
                self.exact_rules[normalized_pattern] = rule
                
            elif rule.pattern_type in ('startswith', 'glob'):
                # 提取可索引的前缀
                prefix = self._extract_prefix(rule.pattern)
                if prefix and len(prefix) > 3:  # 只有有意义的前缀才索引
                    self.prefix_rules[prefix].append(rule)
                else:
                    self.glob_rules.append(rule)
                    
            elif rule.pattern_type == 'filename':
                pattern = rule.pattern[9:] if rule.pattern.startswith('filename:') else rule.pattern
                self.filename_rules[pattern].append(rule)
                
            elif rule.pattern_type == 'extension':
                ext = rule.pattern[4:] if rule.pattern.startswith('ext:') else rule.pattern
                if not ext.startswith('.'):
                    ext = '.' + ext
                self.extension_rules[ext].append(rule)
                
            else:
                # 其他类型放入通用列表
                self.glob_rules.append(rule)
    
    def _extract_prefix(self, pattern: str) -> Optional[str]:
        """从 glob 模式中提取可索引的前缀"""
        # 找到第一个特殊字符前的部分
        special_chars = set('*?[]{}')
        prefix = ''
        for char in pattern:
            if char in special_chars:
                break
            prefix += char
        return prefix if len(prefix) > 3 else None
    
    def query(self, file_path: str) -> List[Tuple[Rule, float]]:
        """
        查询匹配的规则
        
        Returns:
            List[(Rule, match_score)]
        """
        matches = []
        normalized_path = normalize_path(file_path)
        
        # 1. 精确匹配 (O(1))
        if normalized_path in self.exact_rules:
            matches.append((self.exact_rules[normalized_path], 1.0))
        
        # 2. 前缀匹配
        for prefix, rules in self.prefix_rules.items():
            if normalized_path.startswith(prefix):
                for rule in rules:
                    score = self._calculate_match_score(normalized_path, rule)
                    if score > 0:
                        matches.append((rule, score))
        
        # 3. 文件名匹配
        filename = Path(normalized_path).name
        for pattern, rules in self.filename_rules.items():
            if fnmatch.fnmatch(filename, pattern):
                for rule in rules:
                    matches.append((rule, 0.7))
        
        # 4. 扩展名匹配
        ext = Path(normalized_path).suffix
        if ext in self.extension_rules:
            for rule in self.extension_rules[ext]:
                matches.append((rule, 0.5))
        
        # 5. 通用 glob 规则
        for rule in self.glob_rules:
            score = self._calculate_match_score(normalized_path, rule)
            if score > 0:
                matches.append((rule, score))
        
        return matches
    
    def is_excluded(self, file_path: str) -> bool:
        """检查路径是否被排除"""
        normalized_path = normalize_path(file_path)
        
        for rule in self.exclusion_rules:
            if rule._compiled_pattern and rule._compiled_pattern(normalized_path):
                return True
        return False
    
    def get_exclusion_reason(self, file_path: str) -> Optional[str]:
        """获取排除原因（用于调试/日志）"""
        normalized_path = normalize_path(file_path)
        
        for rule in self.exclusion_rules:
            if rule._compiled_pattern and rule._compiled_pattern(normalized_path):
                return rule.reason
        return None
    
    def _calculate_match_score(self, path: str, rule: Rule) -> float:
        """计算匹配分数 (0.0 - 1.0)"""
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
            # 计算模式深度
            depth = self._calculate_pattern_depth(rule.pattern)
            return min(0.95, 0.5 + depth * 0.1)
        elif rule.pattern_type == 'filename':
            return 0.7
        elif rule.pattern_type == 'extension':
            return 0.5
        elif rule.pattern_type == 'startswith':
            return 0.8
        elif rule.pattern_type == 'endswith':
            return 0.6
        
        return 0.6
    
    def _calculate_pattern_depth(self, pattern: str) -> int:
        """计算模式深度（作为具体程度指标）"""
        # 移除 glob 特殊字符后计算路径深度
        clean_pattern = pattern.replace('*', '').replace('?', '').replace('**', '')
        return clean_pattern.count('/')
    
    def get_stats(self) -> Dict[str, int]:
        """获取索引统计信息"""
        return {
            'exact_rules': len(self.exact_rules),
            'prefix_rules': len(self.prefix_rules),
            'filename_rules': len(self.filename_rules),
            'extension_rules': len(self.extension_rules),
            'glob_rules': len(self.glob_rules),
            'exclusion_rules': len(self.exclusion_rules),
            'total_rules': len(self.all_rules)
        }