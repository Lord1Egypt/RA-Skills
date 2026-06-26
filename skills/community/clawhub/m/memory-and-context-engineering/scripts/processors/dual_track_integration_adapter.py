"""
双轨并行架构 - 集成适配器模块

本模块提供双轨架构与现有系统的集成接口。
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .optimized_dual_track_processor import OptimizedDualTrackProcessor, ProcessingResult
from .chain_cache_manager import ChainCacheManager
from .monitoring_system import MonitoringSystem


class DualTrackIntegrationAdapter:
    """
    双轨集成适配器

    提供与现有ContextOrchestrator等系统的集成接口。
    """

    def __init__(
        self,
        processor: OptimizedDualTrackProcessor = None,
        cache_manager: ChainCacheManager = None,
        monitoring_system: MonitoringSystem = None,
        enable_health_check: bool = True
    ):
        """
        初始化适配器

        Args:
            processor: 双轨处理器
            cache_manager: 缓存管理器
            monitoring_system: 监控系统
            enable_health_check: 是否启用健康检查
        """
        # 初始化组件
        self.processor = processor or OptimizedDualTrackProcessor()
        self.cache_manager = cache_manager or ChainCacheManager()
        self.monitoring_system = monitoring_system or MonitoringSystem()
        self.enable_health_check = enable_health_check

        # 降级模式标志
        self.degraded_mode = False

        # 最后一次健康检查时间
        self.last_health_check = None

    def process_message(
        self,
        message: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        处理消息

        Args:
            message: 消息内容
            context: 上下文信息

        Returns:
            处理结果字典
        """
        context = context or {}
        start_time = datetime.now()

        try:
            # 健康检查（如果启用）
            if self.enable_health_check:
                health = self._check_health()
                if health["status"] != "healthy":
                    self.degraded_mode = True
                    self.monitoring_system.health_check(
                        "processor",
                        "degraded",
                        "Running in degraded mode",
                        health
                    )
                else:
                    self.degraded_mode = False

            # 根据模式处理
            if self.degraded_mode:
                # 降级模式：关闭并行处理
                original_parallel = self.processor.enable_parallel
                self.processor.enable_parallel = False
                result = self._run_async_processing(message, context)
                self.processor.enable_parallel = original_parallel
            else:
                # 正常模式
                result = self._run_async_processing(message, context)

            # 更新监控
            processing_time = (datetime.now() - start_time).total_seconds()
            self.monitoring_system.record_processing_time(
                processing_time,
                "degraded" if self.degraded_mode else "normal"
            )

            # 记录缓存命中率
            cache_stats = self.cache_manager.get_stats()
            self.monitoring_system.record_cache_hit_rate(cache_stats.get("hit_rate", 0.0))

            return {
                "status": "success",
                "result": result,
                "degraded_mode": self.degraded_mode,
                "processing_time": processing_time
            }

        except Exception as e:
            # 记录错误
            self.monitoring_system.health_check(
                "processor",
                "unhealthy",
                f"Processing error: {str(e)}",
                {"error": str(e)}
            )

            return {
                "status": "error",
                "error": str(e),
                "degraded_mode": self.degraded_mode,
                "processing_time": (datetime.now() - start_time).total_seconds()
            }

    def _run_async_processing(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> ProcessingResult:
        """
        运行异步处理

        Args:
            message: 消息内容
            context: 上下文信息

        Returns:
            处理结果
        """
        # 创建事件循环并运行异步处理
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.processor.process_input_async(message, context)
            )
            return result
        finally:
            loop.close()

    def _check_health(self) -> Dict[str, Any]:
        """
        健康检查

        Returns:
            健康状态
        """
        self.last_health_check = datetime.now()

        health_issues = []

        # 检查处理器状态
        if not self.processor.executor:
            health_issues.append("Processor executor not available")

        # 检查缓存状态
        cache_stats = self.cache_manager.get_stats()
        if cache_stats.get("hit_rate", 0) < 0.5 and cache_stats.get("total_requests", 0) > 10:
            health_issues.append("Cache hit rate too low")

        # 确定健康状态
        if health_issues:
            return {
                "status": "unhealthy",
                "issues": health_issues
            }
        else:
            return {
                "status": "healthy",
                "message": "All systems operational"
            }

    def get_status(self) -> Dict[str, Any]:
        """
        获取适配器状态

        Returns:
            状态信息
        """
        return {
            "degraded_mode": self.degraded_mode,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None,
            "processor_stats": self.processor.get_performance_stats(),
            "cache_stats": self.cache_manager.get_stats(),
            "monitoring_stats": self.monitoring_system.get_overall_health()
        }

    def reset_degraded_mode(self) -> None:
        """重置降级模式"""
        self.degraded_mode = False
        self.monitoring_system.health_check(
            "processor",
            "healthy",
            "Degraded mode reset"
        )

    async def process_message_async(
        self,
        message: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        异步处理消息

        Args:
            message: 消息内容
            context: 上下文信息

        Returns:
            处理结果字典
        """
        context = context or {}
        start_time = datetime.now()

        try:
            # 健康检查（如果启用）
            if self.enable_health_check:
                health = self._check_health()
                if health["status"] != "healthy":
                    self.degraded_mode = True
                    self.monitoring_system.health_check(
                        "processor",
                        "degraded",
                        "Running in degraded mode",
                        health
                    )
                else:
                    self.degraded_mode = False

            # 根据模式处理
            if self.degraded_mode:
                # 降级模式
                original_parallel = self.processor.enable_parallel
                self.processor.enable_parallel = False
                result = await self.processor.process_input_async(message, context)
                self.processor.enable_parallel = original_parallel
            else:
                result = await self.processor.process_input_async(message, context)

            # 更新监控
            processing_time = (datetime.now() - start_time).total_seconds()
            self.monitoring_system.record_processing_time(
                processing_time,
                "degraded" if self.degraded_mode else "normal"
            )

            return {
                "status": "success",
                "result": result,
                "degraded_mode": self.degraded_mode,
                "processing_time": processing_time
            }

        except Exception as e:
            self.monitoring_system.health_check(
                "processor",
                "unhealthy",
                f"Processing error: {str(e)}",
                {"error": str(e)}
            )

            return {
                "status": "error",
                "error": str(e),
                "degraded_mode": self.degraded_mode,
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
