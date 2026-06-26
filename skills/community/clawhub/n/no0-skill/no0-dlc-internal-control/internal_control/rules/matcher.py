"""
规则匹配器
执行实际的路径匹配，解决规则冲突
"""

import logging
from typing import List, Tuple, Optional
from pathlib import Path

from .models import Rule, MatchResult, get_level_strictness
from .index import RuleIndex
from ..platform.path_utils import normalize_path

logger = logging.getLogger(__name__)


class RuleMatcher:
    """
    规则匹配器
    
    职责：
    1. 执行路径匹配
    2. 解决规则冲突
    3. 计算匹配置信度
    """
    
    def __init__(self, index: RuleIndex):
        self.index = index
        # 路径标准化缓存
        self._normalize_cache: dict = {}
        self._cache_size_limit = 10000
    
    def match(self, file_path: str) -> MatchResult:
        """
        单路径匹配
        
        Args:
            file_path: 文件路径
            
        Returns:
            匹配结果
        """
        # 标准化路径
        normalized = self._normalize_path(file_path)
        
        # 查询索引
        matches = self.index.query(normalized)
        
        if not matches:
            return MatchResult(
                level=None,
                confidence=0.0,
                source='no_match'
            )
        
        # 冲突解决
        best_rule, confidence = self._resolve_conflicts(matches)
        
        return MatchResult(
            rule_id=best_rule.id,
            level=best_rule.level,
            confidence=confidence,
            match_score=confidence,
            source='l2_rule',
            reason=best_rule.reason
        )
    
    def match_batch(self, paths: List[str], max_workers: int = 4) -> List[MatchResult]:
        """
        批量路径匹配
        
        使用多线程加速处理大量文件
        
        Args:
            paths: 路径列表
            max_workers: 最大并发数
            
        Returns:
            匹配结果列表
        """
        from concurrent.futures import ThreadPoolExecutor
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.match, p): p for p in paths}
            
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"匹配失败: {futures[future]} - {e}")
                    results.append(MatchResult(
                        level=None,
                        confidence=0.0,
                        source='error'
                    ))
        
        return results
    
    def _normalize_path(self, path: str) -> str:
        """
        标准化路径（带缓存）
        
        Args:
            path: 原始路径
            
        Returns:
            标准化后的路径
        """
        # 检查缓存
        if path in self._normalize_cache:
            return self._normalize_cache[path]
        
        # 标准化
        result = normalize_path(path)
        
        # 更新缓存（LRU 清理）
        if len(self._normalize_cache) >= self._cache_size_limit:
            # 简单清理：移除一半
            keys = list(self._normalize_cache.keys())[:self._cache_size_limit//2]
            for k in keys:
                del self._normalize_cache[k]
        
        self._normalize_cache[path] = result
        return result
    
    def _resolve_conflicts(self, matches: List[Tuple[Rule, float]]) -> Tuple[Rule, float]:
        """
        冲突解决
        
        冲突场景：
        1. 多个规则匹配同一文件
        2. 匹配结果指向不同级别
        
        解决策略：
        1. 优先使用高优先级规则
        2. 同优先级时，使用匹配分数更高的规则
        3. 仍相同，取级别更严格的
        
        Args:
            matches: 匹配列表 [(Rule, match_score)]
            
        Returns:
            (最佳规则, 置信度)
        """
        if not matches:
            raise ValueError("No matches to resolve")
        
        if len(matches) == 1:
            return matches[0]
        
        # 按 (priority, match_score) 降序排序
        matches.sort(key=lambda x: (x[0].priority, x[1]), reverse=True)
        
        best_priority = matches[0][0].priority
        best_score = matches[0][1]
        
        # 收集所有同优先级同分数的规则
        tied = [(r, s) for r, s in matches 
                if r.priority == best_priority and s == best_score]
        
        if len(tied) == 1:
            return tied[0]
        
        # 仍冲突，选择更严格的级别
        # 使用级别的严格度进行比较
        return max(tied, key=lambda x: get_level_strictness(x[0].level or ''))
    
    def get_stats(self) -> dict:
        """获取匹配器统计"""
        return {
            'cache_size': len(self._normalize_cache),
            'cache_limit': self._cache_size_limit
        }