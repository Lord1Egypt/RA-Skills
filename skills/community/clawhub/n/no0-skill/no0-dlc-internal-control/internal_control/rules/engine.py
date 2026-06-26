"""
分级引擎主类
对外统一接口，整合所有组件
"""

import os
import asyncio
import logging
from typing import Optional, List, Dict
from pathlib import Path
from collections import defaultdict

from .models import (
    Rule, ClassificationResult, ClassificationEntry, 
    DirectoryClassification, RuleStats, DataLevel
)
from .loader import RuleLoader
from .index import RuleIndex
from .matcher import RuleMatcher
from .exclusions import ExclusionManager
from .cache import ClassificationCache
from ..platform.path_utils import normalize_path

logger = logging.getLogger(__name__)


class ClassificationEngine:
    """
    分级规则引擎（对外统一接口）
    
    整合：
    - 规则加载器 (RuleLoader)
    - 规则索引 (RuleIndex)
    - 规则匹配器 (RuleMatcher)
    - 排除项管理器 (ExclusionManager)
    - 结果缓存 (ClassificationCache)
    """
    
    def __init__(self, 
                 max_cache_size: int = 10000,
                 cache_ttl: int = 300):
        """
        初始化分级引擎
        
        Args:
            max_cache_size: 最大缓存条目数
            cache_ttl: 缓存过期时间（秒）
        """
        self.cache = ClassificationCache(max_cache_size, cache_ttl)
        self.exclusion_manager = ExclusionManager()
        self.rule_loader = RuleLoader()
        self.rule_index = RuleIndex()
        self.matcher: Optional[RuleMatcher] = None
        
        # 初始化规则
        self._refresh_rules()
    
    def _refresh_rules(self) -> None:
        """刷新规则"""
        rules = self.rule_loader.load_all()
        self.rule_index.build(rules)
        self.matcher = RuleMatcher(self.rule_index)
        logger.info(f"规则引擎已刷新: {len(rules)} 条规则")
    
    # ========== 查询接口 ==========
    
    async def classify(self, path: str) -> ClassificationResult:
        """
        分级单一路径（主入口）
        
        流程：
        1. 排除检查
        2. 缓存检查
        3. 规则匹配
        4. 结果缓存
        
        Args:
            path: 文件路径
            
        Returns:
            分级结果
        """
        normalized_path = normalize_path(path)
        
        # 1. 排除检查
        if self.exclusion_manager.is_excluded(normalized_path):
            reason = self.exclusion_manager.get_exclusion_reason(normalized_path)
            return ClassificationResult(
                path=normalized_path,
                level=None,
                source='excluded',
                exclusion_reason=reason,
                confidence=1.0
            )
        
        # 2. 检查缓存
        cached = self.cache.get(normalized_path)
        if cached:
            return ClassificationResult(
                path=normalized_path,
                level=cached.level,
                rule_id=cached.rule_id,
                source='cache',
                confidence=cached.confidence
            )
        
        # 3. 规则匹配
        match_result = self.matcher.match(normalized_path)
        
        # 4. 构建结果
        if match_result.level:
            result = ClassificationResult(
                path=normalized_path,
                level=match_result.level,
                rule_id=match_result.rule_id,
                source='l2_rule',
                confidence=match_result.confidence,
                reason=match_result.reason
            )
            
            # 5. 更新缓存
            entry = ClassificationEntry(
                path=normalized_path,
                level=match_result.level,
                rule_id=match_result.rule_id,
                confidence=match_result.confidence,
                timestamp=__import__('time').time()
            )
            self.cache.set(normalized_path, entry)
        else:
            # 无匹配，使用默认分级
            result = ClassificationResult(
                path=normalized_path,
                level=DataLevel.L3_RESTRICTED.value,  # 默认受限级
                source='default',
                confidence=0.3,
                reason='无匹配规则，使用默认分级',
                note='建议手动确认分级'
            )
        
        return result
    
    def classify_sync(self, path: str) -> ClassificationResult:
        """同步版本的 classify"""
        # 排除检查
        normalized_path = normalize_path(path)
        
        if self.exclusion_manager.is_excluded(normalized_path):
            reason = self.exclusion_manager.get_exclusion_reason(normalized_path)
            return ClassificationResult(
                path=normalized_path,
                level=None,
                source='excluded',
                exclusion_reason=reason,
                confidence=1.0
            )
        
        # 缓存检查
        cached = self.cache.get(normalized_path)
        if cached:
            return ClassificationResult(
                path=normalized_path,
                level=cached.level,
                rule_id=cached.rule_id,
                source='cache',
                confidence=cached.confidence
            )
        
        # 规则匹配
        match_result = self.matcher.match(normalized_path)
        
        if match_result.level:
            result = ClassificationResult(
                path=normalized_path,
                level=match_result.level,
                rule_id=match_result.rule_id,
                source='l2_rule',
                confidence=match_result.confidence,
                reason=match_result.reason
            )
            
            # 更新缓存
            entry = ClassificationEntry(
                path=normalized_path,
                level=match_result.level,
                rule_id=match_result.rule_id,
                confidence=match_result.confidence,
                timestamp=__import__('time').time()
            )
            self.cache.set(normalized_path, entry)
        else:
            result = ClassificationResult(
                path=normalized_path,
                level=DataLevel.L3_RESTRICTED.value,
                source='default',
                confidence=0.3,
                reason='无匹配规则，使用默认分级',
                note='建议手动确认分级'
            )
        
        return result
    
    async def classify_directory(self,
                                  directory: str,
                                  recursive: bool = True,
                                  max_depth: int = 10) -> DirectoryClassification:
        """
        批量分级目录
        
        Args:
            directory: 目录路径
            recursive: 是否递归
            max_depth: 最大递归深度
            
        Returns:
            目录分级结果
        """
        import time
        
        normalized_dir = normalize_path(directory)
        
        files = []
        start_time = time.time()
        
        if recursive:
            for root, dirs, filenames in os.walk(normalized_dir):
                # 检查排除项
                dirs[:] = [d for d in dirs if not self.exclusion_manager.is_excluded(
                    os.path.join(root, d)
                )]
                
                # 检查深度
                depth = root.count(os.sep) - normalized_dir.count(os.sep)
                if depth >= max_depth:
                    del dirs[:]
                    continue
                
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            # 非递归，只处理当前目录
            for item in os.listdir(normalized_dir):
                item_path = os.path.join(normalized_dir, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
        
        # 批量分级
        results = []
        for file_path in files:
            result = await self.classify(file_path)
            results.append(result)
        
        # 统计
        stats = defaultdict(int)
        for r in results:
            if r.level:
                stats[r.level] += 1
            else:
                stats['excluded'] += 1
        
        elapsed = time.time() - start_time
        logger.info(f"目录分级完成: {normalized_dir}, {len(files)} 个文件, 耗时 {elapsed:.2f}s")
        
        return DirectoryClassification(
            directory=normalized_dir,
            files=results,
            statistics=dict(stats),
            total_files=len(files)
        )
    
    def classify_directory_sync(self,
                                directory: str,
                                recursive: bool = True,
                                max_depth: int = 10) -> DirectoryClassification:
        """同步版本的 classify_directory"""
        import time
        
        normalized_dir = normalize_path(directory)
        
        files = []
        start_time = time.time()
        
        if recursive:
            for root, dirs, filenames in os.walk(normalized_dir):
                dirs[:] = [d for d in dirs if not self.exclusion_manager.is_excluded(
                    os.path.join(root, d)
                )]
                
                depth = root.count(os.sep) - normalized_dir.count(os.sep)
                if depth >= max_depth:
                    del dirs[:]
                    continue
                
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            for item in os.listdir(normalized_dir):
                item_path = os.path.join(normalized_dir, item)
                if os.path.isfile(item_path):
                    files.append(item_path)
        
        results = []
        for file_path in files:
            result = self.classify_sync(file_path)
            results.append(result)
        
        stats = defaultdict(int)
        for r in results:
            if r.level:
                stats[r.level] += 1
            else:
                stats['excluded'] += 1
        
        elapsed = time.time() - start_time
        logger.info(f"目录分级完成: {normalized_dir}, {len(files)} 个文件, 耗时 {elapsed:.2f}s")
        
        return DirectoryClassification(
            directory=normalized_dir,
            files=results,
            statistics=dict(stats),
            total_files=len(files)
        )
    
    # ========== 管理接口 ==========
    
    def reload_rules(self) -> None:
        """重新加载规则文件"""
        self._refresh_rules()
        self.cache.clear()
        logger.info("规则已重新加载，缓存已清空")
    
    def add_exclusion(self, pattern: str, reason: str) -> None:
        """添加排除规则"""
        self.exclusion_manager.add_custom_exclusion(pattern, reason)
        logger.info(f"添加排除规则: {pattern} - {reason}")
    
    def remove_exclusion(self, pattern: str) -> bool:
        """移除排除规则"""
        result = self.exclusion_manager.remove_custom_exclusion(pattern)
        if result:
            logger.info(f"移除排除规则: {pattern}")
        return result
    
    # ========== 监控接口 ==========
    
    def get_cache_stats(self) -> dict:
        """获取缓存统计"""
        stats = self.cache.get_stats()
        return {
            'size': stats.size,
            'hit_rate': f"{stats.hit_rate:.1%}",
            'expired_count': stats.expired_count
        }
    
    def get_rule_stats(self) -> RuleStats:
        """获取规则统计"""
        index_stats = self.rule_index.get_stats()
        return RuleStats(
            total_rules=index_stats['total_rules'],
            exact_rules=index_stats['exact_rules'],
            glob_rules=index_stats['glob_rules'] + index_stats['prefix_rules'],
            prefix_rules=index_stats['prefix_rules'],
            exclusion_rules=index_stats['exclusion_rules']
        )
    
    def get_exclusion_stats(self) -> dict:
        """获取排除规则统计"""
        return self.exclusion_manager.get_stats()