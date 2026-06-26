"""
双轨并行架构 - 监控系统模块

本模块实现双轨架构的监控和日志功能。
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class Metric:
    """
    指标

    Attributes:
        name: 指标名称
        value: 指标值
        timestamp: 时间戳
        labels: 标签
    """

    def __init__(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] | None = None
    ):
        self.name = name
        self.value = value
        self.timestamp = datetime.now()
        self.labels = labels or {}


class HealthCheck:
    """
    健康检查结果

    Attributes:
        component: 组件名称
        status: 状态
        message: 消息
        timestamp: 时间戳
        details: 详情
    """

    def __init__(
        self,
        component: str,
        status: str,
        message: str,
        details: Dict | None = None
    ):
        self.component = component
        self.status = status  # healthy, degraded, unhealthy
        self.message = message
        self.timestamp = datetime.now()
        self.details = details or {}


class MonitoringSystem:
    """
    监控系统

    收集和报告双轨架构的监控指标。
    """

    def __init__(self, max_metrics: int = 1000, monitoring_enabled: bool = True):
        self.max_metrics = max_metrics
        self.monitoring_enabled = monitoring_enabled

        # 指标存储
        self.metrics: List[Metric] = []

        # 健康检查结果
        self.health_checks: Dict[str, HealthCheck] = {}

        # 性能指标
        self.performance_metrics = {
            "processing_time": [],
            "cache_hit_rate": [],
            "chain_extraction_time": [],
            "bucket_extraction_time": []
        }

    def record_metric(
        self,
        name: str,
        value: float,
        labels: Dict[str, str] | None = None
    ) -> None:
        """
        记录指标

        Args:
            name: 指标名称
            value: 指标值
            labels: 标签
        """
        if not self.monitoring_enabled:
            return

        metric = Metric(
            name=name,
            value=value,
            labels=labels or {}
        )

        self.metrics.append(metric)

        # 保持最大数量
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]

    def record_processing_time(
        self,
        time: float,
        mode: str = "parallel"
    ) -> None:
        """
        记录处理时间

        Args:
            time: 处理时间（秒）
            mode: 处理模式
        """
        self.performance_metrics["processing_time"].append(time)
        self.record_metric(
            "processing_time",
            time,
            {"mode": mode}
        )

    def record_cache_hit_rate(self, hit_rate: float) -> None:
        """
        记录缓存命中率

        Args:
            hit_rate: 命中率（0-1）
        """
        self.performance_metrics["cache_hit_rate"].append(hit_rate)
        self.record_metric("cache_hit_rate", hit_rate)

    def record_chain_extraction_time(
        self,
        chain_type: str,
        time: float
    ) -> None:
        """
        记录链提取时间

        Args:
            chain_type: 链类型
            time: 提取时间（秒）
        """
        self.performance_metrics["chain_extraction_time"].append(time)
        self.record_metric(
            "chain_extraction_time",
            time,
            {"chain_type": chain_type}
        )

    def health_check(
        self,
        component: str,
        status: str,
        message: str,
        details: Dict | None = None
    ) -> None:
        """
        记录健康检查结果

        Args:
            component: 组件名称
            status: 状态 (healthy, degraded, unhealthy)
            message: 消息
            details: 详情
        """
        health = HealthCheck(
            component=component,
            status=status,
            message=message,
            details=details or {}
        )
        self.health_checks[component] = health

    def get_overall_health(self) -> Dict[str, Any]:
        """
        获取整体健康状态

        Returns:
            整体健康状态
        """
        if not self.health_checks:
            return {
                "status": "unknown",
                "message": "No health checks performed yet"
            }

        # 统计各状态数量
        status_counts = {"healthy": 0, "degraded": 0, "unhealthy": 0}
        for health in self.health_checks.values():
            status_counts[health.status] = status_counts.get(health.status, 0) + 1

        # 确定整体状态
        if status_counts["unhealthy"] > 0:
            overall_status = "unhealthy"
            message = "Some components are unhealthy"
        elif status_counts["degraded"] > 0:
            overall_status = "degraded"
            message = "Some components are degraded"
        else:
            overall_status = "healthy"
            message = "All components are healthy"

        return {
            "status": overall_status,
            "message": message,
            "components": {
                name: {
                    "status": health.status,
                    "message": health.message
                }
                for name, health in self.health_checks.items()
            }
        }

    def export_metrics_json(self) -> str:
        """
        导出指标为JSON格式

        Returns:
            JSON字符串
        """
        export_data = {
            "metrics": [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "timestamp": metric.timestamp.isoformat(),
                    "labels": metric.labels
                }
                for metric in self.metrics
            ],
            "health_checks": {
                name: {
                    "component": health.component,
                    "status": health.status,
                    "message": health.message,
                    "timestamp": health.timestamp.isoformat(),
                    "details": health.details
                }
                for name, health in self.health_checks.items()
            },
            "performance_metrics": {
                name: {
                    "count": len(values),
                    "avg": sum(values) / len(values) if values else 0.0,
                    "min": min(values) if values else 0.0,
                    "max": max(values) if values else 0.0
                }
                for name, values in self.performance_metrics.items()
            }
        }

        return json.dumps(export_data, indent=2, ensure_ascii=False)

    def clear(self) -> None:
        """清空所有监控数据"""
        self.metrics.clear()
        self.health_checks.clear()
        for key in self.performance_metrics:
            self.performance_metrics[key].clear()
