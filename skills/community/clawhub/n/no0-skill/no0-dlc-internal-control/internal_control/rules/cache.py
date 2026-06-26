"""
分级结果缓存
LRU 内存缓存，提升查询性能
"""

import threading
import time
import logging
from typing import Dict, Optional

from .models import ClassificationEntry, ClassificationResult, CacheStats

logger = logging.getLogger(__name__)


class ClassificationCache:
    """
    分级结果内存缓存（线程安全）
    
    特性：
    1. LRU 淘汰策略
    2. TTL 过期机制
    3. 线程安全
    4. 命中率统计
    """
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 300):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认过期时间（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        
        # 路径 -> (entry, access_time, access_count)
        self._cache: Dict[str, tuple] = {}
        self._lock = threading.RLock()
        
        # 统计
        self._hits = 0
        self._misses = 0
        self._evictions = 0
    
    def get(self, path: str) -> Optional[ClassificationEntry]:
        """
        获取缓存条目
        
        Args:
            path: 文件路径
            
        Returns:
            缓存条目，如果不存在或已过期则返回 None
        """
        with self._lock:
            cached = self._cache.get(path)
            
            if cached is None:
                self._misses += 1
                return None
            
            entry, access_time, access_count = cached
            
            # 检查是否过期
            if entry.is_expired():
                del self._cache[path]
                self._misses += 1
                return None
            
            # 更新访问时间和计数
            self._cache[path] = (entry, time.time(), access_count + 1)
            self._hits += 1
            
            return entry
    
    def set(self, path: str, entry: ClassificationEntry) -> None:
        """
        设置缓存条目
        
        Args:
            path: 文件路径
            entry: 分级条目
        """
        with self._lock:
            # LRU 清理：缓存超过限制时，移除最久未访问的
            if len(self._cache) >= self.max_size and path not in self._cache:
                self._evict_lru()
            
            self._cache[path] = (entry, time.time(), 1)
    
    def invalidate_path(self, path: str) -> bool:
        """
        使特定路径缓存失效
        
        Args:
            path: 文件路径
            
        Returns:
            是否成功移除
        """
        with self._lock:
            if path in self._cache:
                del self._cache[path]
                return True
            return False
    
    def invalidate_prefix(self, prefix: str) -> int:
        """
        使某前缀下所有缓存失效
        
        Args:
            prefix: 路径前缀
            
        Returns:
            移除的条目数
        """
        with self._lock:
            to_remove = [p for p in self._cache if p.startswith(prefix)]
            for p in to_remove:
                del self._cache[p]
            return len(to_remove)
    
    def clear(self) -> None:
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
    
    def _evict_lru(self) -> None:
        """移除最久未访问的条目（LRU）"""
        if not self._cache:
            return
        
        # 找到最久未访问的
        oldest_path = min(self._cache.keys(), key=lambda p: self._cache[p][1])
        del self._cache[oldest_path]
        self._evictions += 1
    
    def get_stats(self) -> CacheStats:
        """获取缓存统计"""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
            
            # 统计过期条目
            expired_count = 0
            current_time = time.time()
            for entry, _, _ in self._cache.values():
                if current_time - entry.timestamp > entry.ttl:
                    expired_count += 1
            
            return CacheStats(
                size=len(self._cache),
                hit_rate=hit_rate,
                expired_count=expired_count
            )
    
    def clean_expired(self) -> int:
        """
        清理过期条目
        
        Returns:
            清理的条目数
        """
        with self._lock:
            current_time = time.time()
            to_remove = [
                p for p, (entry, _, _) in self._cache.items()
                if current_time - entry.timestamp > entry.ttl
            ]
            for p in to_remove:
                del self._cache[p]
            return len(to_remove)