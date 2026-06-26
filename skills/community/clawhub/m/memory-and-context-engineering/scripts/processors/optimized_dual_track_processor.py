"""
双轨并行架构 - 优化双轨处理器模块

本模块实现性能优化的双轨并行处理器。
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class ProcessingResult:
    """
    处理结果

    Attributes:
        topic_clusters: 话题簇列表
        extracted_chains: 提取的链字典
        bucket_chain_links: 桶-链关联列表
        validation_results: 验证结果列表
        extraction_action: 提取动作
        processing_time: 处理时间（秒）
        performance_metrics: 性能指标
    """

    def __init__(
        self,
        topic_clusters: List[Any] = None,
        extracted_chains: Dict = None,
        bucket_chain_links: List[Any] = None,
        validation_results: List[Any] = None,
        extraction_action: Any = None,
        processing_time: float = 0.0,
        performance_metrics: Dict = None
    ):
        self.topic_clusters = topic_clusters or []
        self.extracted_chains = extracted_chains or {}
        self.bucket_chain_links = bucket_chain_links or []
        self.validation_results = validation_results or []
        self.extraction_action = extraction_action
        self.processing_time = processing_time
        self.performance_metrics = performance_metrics or {}


class OptimizedDualTrackProcessor:
    """
    优化的双轨处理器

    使用异步并行处理、缓存等优化技术提升性能。
    """

    def __init__(self, enable_parallel: bool = True, enable_cache: bool = True, cache_ttl: int = 60):
        self.enable_parallel = enable_parallel
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl

        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=2)

        # 缓存
        self.processing_cache: Dict[str, Any] = {}

        # 性能监控
        self.performance_stats: Dict[str, List[float]] = {
            "bucket_track_time": [],
            "chain_track_time": [],
            "fusion_time": [],
            "total_time": []
        }

    async def process_input_async(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """
        异步处理输入

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            处理结果
        """
        start_time = time.time()

        # 检查缓存
        cache_key = self._generate_cache_key(text, context)
        if self.enable_cache and cache_key in self.processing_cache:
            cached_result = self.processing_cache[cache_key]
            # 检查是否过期
            if (datetime.now().timestamp() - cached_result["timestamp"]) < self.cache_ttl:
                cached_result["result"].processing_time = time.time() - start_time
                cached_result["result"].performance_metrics["cache_hit"] = True
                return cached_result["result"]

        # 并行处理
        if self.enable_parallel:
            result = await self._parallel_process(text, context)
        else:
            result = await self._sequential_process(text, context)

        result.processing_time = time.time() - start_time

        # 缓存结果
        if self.enable_cache:
            self.processing_cache[cache_key] = {
                "result": result,
                "timestamp": datetime.now().timestamp()
            }

        return result

    async def _parallel_process(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """
        并行处理

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            处理结果
        """
        # 模拟轨道A和轨道B的并行处理
        loop = asyncio.get_event_loop()

        # 轨道A: 语义桶提炼
        bucket_future = loop.run_in_executor(
            self.executor,
            self._process_bucket_track,
            text,
            context
        )

        # 轨道B: 链提取
        chain_future = loop.run_in_executor(
            self.executor,
            self._process_chain_track,
            text,
            context
        )

        # 等待两个轨道完成
        bucket_result, chain_result = await asyncio.gather(
            bucket_future,
            chain_future
        )

        # 融合处理
        fusion_result = await loop.run_in_executor(
            self.executor,
            self._process_fusion,
            bucket_result,
            chain_result,
            context
        )

        return fusion_result

    async def _sequential_process(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """
        串行处理（降级模式）

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            处理结果
        """
        # 顺序处理
        bucket_result = self._process_bucket_track(text, context)
        chain_result = self._process_chain_track(text, context)
        fusion_result = self._process_fusion(bucket_result, chain_result, context)

        return fusion_result

    def _process_bucket_track(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        处理轨道A（语义桶提炼）

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            处理结果
        """
        start_time = time.time()

        # 模拟语义桶提炼
        time.sleep(0.1)

        processing_time = time.time() - start_time
        self.performance_stats["bucket_track_time"].append(processing_time)

        return {
            "type": "bucket",
            "result": [],
            "processing_time": processing_time
        }

    def _process_chain_track(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        处理轨道B（链提取）

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            处理结果
        """
        start_time = time.time()

        # 模拟链提取
        time.sleep(0.15)

        processing_time = time.time() - start_time
        self.performance_stats["chain_track_time"].append(processing_time)

        return {
            "type": "chain",
            "result": {},
            "processing_time": processing_time
        }

    def _process_fusion(
        self,
        bucket_result: Dict[str, Any],
        chain_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """
        融合处理

        Args:
            bucket_result: 桶轨道结果
            chain_result: 链轨道结果
            context: 上下文信息

        Returns:
            融合结果
        """
        start_time = time.time()

        # 模拟融合处理
        time.sleep(0.05)

        processing_time = time.time() - start_time
        self.performance_stats["fusion_time"].append(processing_time)

        return ProcessingResult(
            topic_clusters=bucket_result.get("result", []),
            extracted_chains=chain_result.get("result", {}),
            processing_time=processing_time,
            performance_metrics={
                "bucket_time": bucket_result.get("processing_time", 0),
                "chain_time": chain_result.get("processing_time", 0),
                "fusion_time": processing_time,
                "parallel": self.enable_parallel,
                "cache_enabled": self.enable_cache
            }
        )

    def _generate_cache_key(
        self,
        text: str,
        context: Dict[str, Any]
    ) -> str:
        """
        生成缓存键

        Args:
            text: 输入文本
            context: 上下文信息

        Returns:
            缓存键
        """
        import hashlib
        key_string = f"{text}_{context}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def set_parallel_enabled(self, enabled: bool) -> None:
        """
        设置并行处理开关

        Args:
            enabled: 是否启用
        """
        self.enable_parallel = enabled

    def set_cache_enabled(self, enabled: bool) -> None:
        """
        设置缓存开关

        Args:
            enabled: 是否启用
        """
        self.enable_cache = enabled

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计

        Returns:
            性能统计信息
        """
        stats = {}
        for key, values in self.performance_stats.items():
            if values:
                stats[key] = {
                    "count": len(values),
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values)
                }
            else:
                stats[key] = {
                    "count": 0,
                    "avg": 0.0,
                    "min": 0.0,
                    "max": 0.0
                }

        stats["cache_size"] = len(self.processing_cache)
        stats["parallel_enabled"] = self.enable_parallel
        stats["cache_enabled"] = self.enable_cache

        return stats

    def clear_cache(self) -> None:
        """清空缓存"""
        self.processing_cache.clear()
