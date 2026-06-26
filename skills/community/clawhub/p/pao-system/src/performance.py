"""
PAO系统性能优化模块

提供：
- 数据库查询优化
- 网络通信压缩
- 内存使用优化
- 缓存管理
"""

import time
import asyncio
import psutil
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from functools import wraps
import hashlib
import json

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """性能指标"""
    operation: str
    duration_ms: float
    memory_before_mb: float
    memory_after_mb: float
    timestamp: float


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self):
        self.metrics: list[PerformanceMetrics] = []
        self.process = psutil.Process()

    def record(self, operation: str, duration_ms: float,
               memory_before_mb: float, memory_after_mb: float):
        """记录性能指标"""
        metric = PerformanceMetrics(
            operation=operation,
            duration_ms=duration_ms,
            memory_before_mb=memory_before_mb,
            memory_after_mb=memory_after_mb,
            timestamp=time.time()
        )
        self.metrics.append(metric)

    def get_metrics(self, operation: Optional[str] = None) -> list[PerformanceMetrics]:
        """获取性能指标"""
        if operation:
            return [m for m in self.metrics if m.operation == operation]
        return self.metrics

    def get_average_duration(self, operation: str) -> float:
        """获取平均执行时间"""
        metrics = self.get_metrics(operation)
        if not metrics:
            return 0.0
        return sum(m.duration_ms for m in metrics) / len(metrics)

    def clear(self):
        """清空指标"""
        self.metrics.clear()


class CacheManager:
    """缓存管理器"""

    def __init__(self, max_size_mb: int = 100, ttl_seconds: int = 300):
        self.max_size_mb = max_size_mb
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                self._hits += 1
                return value
            else:
                del self._cache[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any):
        """设置缓存"""
        self._cache[key] = (value, time.time())

    def invalidate(self, key: str):
        """使缓存失效"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0
        return {
            "size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate
        }


def timed(metric_name: str = "operation"):
    """性能计时装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            mem_before = psutil.Process().memory_info().rss / 1024 / 1024
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = (time.perf_counter() - start) * 1000
                mem_after = psutil.Process().memory_info().rss / 1024 / 1024
                logger.debug(f"{metric_name}: {duration:.2f}ms, mem: {mem_before:.1f}->{mem_after:.1f}MB")
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            mem_before = psutil.Process().memory_info().rss / 1024 / 1024
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = (time.perf_counter() - start) * 1000
                mem_after = psutil.Process().memory_info().rss / 1024 / 1024
                logger.debug(f"{metric_name}: {duration:.2f}ms, mem: {mem_before:.1f}->{mem_after:.1f}MB")
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator


class DataCompressor:
    """数据压缩器"""

    @staticmethod
    def compress(data: str) -> bytes:
        """压缩数据（使用简单编码）"""
        if not data:
            return b""
        # 简单压缩：移除多余空白
        compressed = " ".join(data.split())
        return compressed.encode('utf-8')

    @staticmethod
    def decompress(data: bytes) -> str:
        """解压数据"""
        if not data:
            return ""
        return data.decode('utf-8')

    @staticmethod
    def should_compress(data: str, threshold: int = 1024) -> bool:
        """判断是否应该压缩"""
        return len(data) > threshold


class QueryOptimizer:
    """查询优化器"""

    def __init__(self):
        self._query_cache = CacheManager(max_size_mb=50, ttl_seconds=60)

    def get_cached_query(self, query_key: str) -> Optional[Any]:
        """获取缓存的查询结果"""
        return self._query_cache.get(query_key)

    def cache_query_result(self, query_key: str, result: Any):
        """缓存查询结果"""
        self._query_cache.set(query_key, result)

    @staticmethod
    def generate_query_key(query: str, params: Dict[str, Any]) -> str:
        """生成查询缓存键"""
        key_data = json.dumps({"query": query, "params": params}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()


class MemoryOptimizer:
    """内存优化器"""

    def __init__(self):
        self.process = psutil.Process()
        self._peak_memory_mb = 0

    def get_current_memory_mb(self) -> float:
        """获取当前内存使用（MB）"""
        return self.process.memory_info().rss / 1024 / 1024

    def get_memory_percent(self) -> float:
        """获取内存使用百分比"""
        return self.process.memory_percent()

    def track_peak(self):
        """追踪峰值内存"""
        current = self.get_current_memory_mb()
        if current > self._peak_memory_mb:
            self._peak_memory_mb = current

    def get_peak_memory_mb(self) -> float:
        """获取峰值内存"""
        return self._peak_memory_mb

    def suggest_gc(self, threshold_mb: int = 500) -> bool:
        """建议是否进行垃圾回收"""
        current = self.get_current_memory_mb()
        if current > threshold_mb:
            import gc
            gc.collect()
            return True
        return False


# 全局性能监控实例
performance_monitor = PerformanceMonitor()
query_optimizer = QueryOptimizer()
memory_optimizer = MemoryOptimizer()
