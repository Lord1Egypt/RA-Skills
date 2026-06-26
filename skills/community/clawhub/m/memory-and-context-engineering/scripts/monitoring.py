# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
基础监控模块

设计目标：
1. 追踪系统运行状态和性能指标
2. 避免监控本身影响性能
3. 设置合理的告警阈值
4. 存储和查询监控数据

监控指标清单：
核心指标：
- 感知记忆存储延迟
- 短期记忆存储延迟
- 长期记忆检索延迟
- 上下文重构延迟
- 洞察生成延迟

业务指标：
- 记忆存储成功率
- 记忆检索命中率
- Token 预算使用率
- 洞察生成数量

资源指标：
- Redis 连接数
- 文件系统使用率
- 内存使用量
- CPU 使用率
"""

import asyncio
import json
import os
import psutil
import time
from collections import deque
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from pydantic import BaseModel, Field


# ============================================================================
# 监控指标类型
# ============================================================================


class MetricType(str, Enum):
    """指标类型"""

    # 延迟指标
    LATENCY = "latency"

    # 计数指标
    COUNT = "count"

    # 吞吐量指标
    THROUGHPUT = "throughput"

    # 成功率指标
    SUCCESS_RATE = "success_rate"

    # 资源使用率
    RESOURCE_USAGE = "resource_usage"


class MetricCategory(str, Enum):
    """指标分类"""

    # 核心指标
    CORE = "core"

    # 业务指标
    BUSINESS = "business"

    # 资源指标
    RESOURCE = "resource"


# ============================================================================
# 监控指标数据
# ============================================================================


@dataclass
class MetricData:
    """指标数据"""

    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)
    metric_type: MetricType = MetricType.COUNT
    category: MetricCategory = MetricCategory.CORE


@dataclass
class LatencyMetric:
    """延迟指标"""

    name: str
    value: float  # 延迟值（毫秒）
    timestamp: datetime = field(default_factory=datetime.now)
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStatistics:
    """指标统计"""

    name: str
    count: int
    min: float
    max: float
    avg: float
    p50: float
    p95: float
    p99: float
    timestamp: datetime = field(default_factory=datetime.now)


# ============================================================================
# 监控配置
# ============================================================================


class MonitoringConfig(BaseModel):
    """监控配置"""

    # 数据保留配置
    max_data_points: int = 10000  # 最大数据点数
    retention_seconds: int = 3600  # 数据保留时间（秒）

    # 统计配置
    statistics_window: int = 100  # 统计窗口大小
    statistics_interval: float = 10.0  # 统计计算间隔（秒）

    # 告警配置
    enable_alerts: bool = True
    alert_threshold_latency_p95: float = 100.0  # P95 延迟告警阈值（毫秒）
    alert_threshold_error_rate: float = 0.05  # 错误率告警阈值

    # 性能配置
    enable_monitoring: bool = True  # 是否启用监控
    sampling_rate: float = 1.0  # 采样率（0.0-1.0）


# ============================================================================
# 监控器
# ============================================================================


class Monitor:
    """
    监控器

    职责：
    1. 收集指标数据
    2. 计算统计数据
    3. 检查告警阈值
    4. 提供指标查询接口
    """

    def __init__(self, config: Optional[MonitoringConfig] = None):
        """
        初始化监控器

        Args:
            config: 监控配置
        """
        self.config = config or MonitoringConfig()

        # 指标数据存储
        self.metrics_data: Dict[str, deque] = {}

        # 统计数据缓存
        self.statistics_cache: Dict[str, MetricStatistics] = {}

        # 告警回调函数
        self.alert_callbacks: List[Callable] = []

        # 资源监控任务
        self.resource_monitor_task: Optional[asyncio.Task] = None
        self.statistics_task: Optional[asyncio.Task] = None

        # 启动后台任务
        if self.config.enable_monitoring:
            self._start_background_tasks()

    # ========================================================================
    # 指标收集
    # ========================================================================

    def record_latency(
        self,
        name: str,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        记录延迟指标

        Args:
            name: 指标名称
            value: 延迟值（毫秒）
            labels: 标签
        """
        if not self.config.enable_monitoring:
            return

        # 采样
        if not self._should_sample():
            return

        metric = LatencyMetric(
            name=name,
            value=value,
            labels=labels or {},
        )

        self._add_metric(name, metric)
        self._check_latency_alert(name, value)

    def record_count(
        self,
        name: str,
        value: float = 1.0,
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        记录计数指标

        Args:
            name: 指标名称
            value: 计数值
            labels: 标签
        """
        if not self.config.enable_monitoring:
            return

        if not self._should_sample():
            return

        metric = MetricData(
            name=name,
            value=value,
            labels=labels or {},
            metric_type=MetricType.COUNT,
        )

        self._add_metric(name, metric)

    def record_success_rate(
        self,
        name: str,
        success: bool,
        labels: Optional[Dict[str, str]] = None,
    ):
        """
        记录成功率指标

        Args:
            name: 指标名称
            success: 是否成功
            labels: 标签
        """
        if not self.config.enable_monitoring:
            return

        if not self._should_sample():
            return

        value = 1.0 if success else 0.0

        metric = MetricData(
            name=name,
            value=value,
            labels=labels or {},
            metric_type=MetricType.SUCCESS_RATE,
        )

        self._add_metric(name, metric)

    # ========================================================================
    # 内部方法
    # ========================================================================

    def _add_metric(self, name: str, metric: Any):
        """
        添加指标数据

        Args:
            name: 指标名称
            metric: 指标数据
        """
        if name not in self.metrics_data:
            self.metrics_data[name] = deque(maxlen=self.config.max_data_points)

        self.metrics_data[name].append(metric)

        # 清理过期数据
        self._cleanup_expired_data()

    def _cleanup_expired_data(self):
        """清理过期数据"""
        now = datetime.now()
        cutoff_time = datetime.fromtimestamp(now.timestamp() - self.config.retention_seconds)

        for name, metrics in self.metrics_data.items():
            while metrics and metrics[0].timestamp < cutoff_time:
                metrics.popleft()

    def _should_sample(self) -> bool:
        """
        是否应该采样

        Returns:
            是否采样
        """
        import random
        return random.random() < self.config.sampling_rate

    # ========================================================================
    # 统计计算
    # ========================================================================

    def get_statistics(self, name: str) -> Optional[MetricStatistics]:
        """
        获取指标统计

        Args:
            name: 指标名称

        Returns:
            统计数据
        """
        if name not in self.metrics_data:
            return None

        metrics = list(self.metrics_data[name])
        if not metrics:
            return None

        values = [m.value for m in metrics]
        values.sort()

        return MetricStatistics(
            name=name,
            count=len(values),
            min=min(values),
            max=max(values),
            avg=sum(values) / len(values),
            p50=values[int(len(values) * 0.5)],
            p95=values[int(len(values) * 0.95)],
            p99=values[int(len(values) * 0.99)],
        )

    def get_all_statistics(self) -> Dict[str, MetricStatistics]:
        """
        获取所有指标统计

        Returns:
            所有统计数据
        """
        stats = {}
        for name in self.metrics_data:
            stat = self.get_statistics(name)
            if stat:
                stats[name] = stat
        return stats

    # ========================================================================
    # 告警检查
    # ========================================================================

    def _check_latency_alert(self, name: str, value: float):
        """
        检查延迟告警

        Args:
            name: 指标名称
            value: 延迟值
        """
        if not self.config.enable_alerts:
            return

        stat = self.get_statistics(name)
        if stat and stat.p95 > self.config.alert_threshold_latency_p95:
            self._trigger_alert(
                alert_type="latency",
                message=f"延迟告警: {name} P95={stat.p95:.2f}ms (阈值: {self.config.alert_threshold_latency_p95}ms)",
                metric_name=name,
            )

    def _trigger_alert(self, alert_type: str, message: str, **kwargs):
        """
        触发告警

        Args:
            alert_type: 告警类型
            message: 告警消息
            **kwargs: 额外参数
        """
        alert_data = {
            "alert_type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            **kwargs,
        }

        print(f"[Monitor] 告警: {message}")

        # 触发告警回调
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                print(f"[Monitor] 告警回调执行失败: {e}")

    def register_alert_callback(self, callback: Callable):
        """
        注册告警回调

        Args:
            callback: 回调函数
        """
        self.alert_callbacks.append(callback)

    # ========================================================================
    # 资源监控
    # ========================================================================

    async def _monitor_resources(self):
        """监控资源使用情况"""
        while True:
            try:
                # CPU 使用率
                cpu_percent = psutil.cpu_percent(interval=1)
                self.record_count("system.cpu.usage", cpu_percent)

                # 内存使用率
                memory = psutil.virtual_memory()
                self.record_count("system.memory.usage", memory.percent)
                self.record_count("system.memory.available", memory.available)

                # 磁盘使用率
                disk = psutil.disk_usage("/")
                self.record_count("system.disk.usage", disk.percent)
                self.record_count("system.disk.available", disk.available)

            except Exception as e:
                print(f"[Monitor] 资源监控失败: {e}")

            await asyncio.sleep(10)  # 每10秒采集一次

    # ========================================================================
    # 后台任务管理
    # ========================================================================

    def _start_background_tasks(self):
        """启动后台任务"""
        # 启动资源监控任务
        self.resource_monitor_task = asyncio.create_task(self._monitor_resources())

    def stop(self):
        """停止监控"""
        # 取消后台任务
        if self.resource_monitor_task:
            self.resource_monitor_task.cancel()

    # ========================================================================
    # 数据查询
    # ========================================================================

    def get_metrics(
        self,
        name: str,
        limit: int = 100,
    ) -> List[Any]:
        """
        获取指标数据

        Args:
            name: 指标名称
            limit: 返回数量限制

        Returns:
            指标数据列表
        """
        if name not in self.metrics_data:
            return []

        return list(self.metrics_data[name])[-limit:]


# ============================================================================
# 性能追踪上下文管理器
# ============================================================================


class LatencyTracker:
    """
    延迟追踪器

    用于追踪操作的延迟
    """

    def __init__(self, monitor: Monitor, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """
        初始化延迟追踪器

        Args:
            monitor: 监控器
            metric_name: 指标名称
            labels: 标签
        """
        self.monitor = monitor
        self.metric_name = metric_name
        self.labels = labels or {}
        self.start_time: Optional[float] = None
        self.stages: Dict[str, float] = {}

    async def __aenter__(self):
        """进入上下文"""
        self.start_time = time.time()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if self.start_time is not None:
            latency_ms = (time.time() - self.start_time) * 1000
            self.monitor.record_latency(
                self.metric_name,
                latency_ms,
                labels=self.labels,
            )
        return False

    def start_stage(self, stage_name: str):
        """
        开始阶段

        Args:
            stage_name: 阶段名称
        """
        self.stages[stage_name] = time.time()

    def end_stage(self, stage_name: str):
        """
        结束阶段

        Args:
            stage_name: 阶段名称
        """
        if stage_name in self.stages:
            latency_ms = (time.time() - self.stages[stage_name]) * 1000
            self.monitor.record_latency(
                f"{self.metric_name}.{stage_name}",
                latency_ms,
                labels=self.labels,
            )
            del self.stages[stage_name]


# ============================================================================
# 工厂函数
# ============================================================================


_monitor_instance: Optional[Monitor] = None


def get_monitor(config: Optional[MonitoringConfig] = None) -> Monitor:
    """
    获取监控器实例（单例）

    Args:
        config: 监控配置

    Returns:
        监控器实例
    """
    global _monitor_instance

    if _monitor_instance is None:
        _monitor_instance = Monitor(config)

    return _monitor_instance


def track_latency(metric_name: str, labels: Optional[Dict[str, str]] = None) -> LatencyTracker:
    """
    创建延迟追踪器

    Args:
        metric_name: 指标名称
        labels: 标签

    Returns:
        延迟追踪器
    """
    monitor = get_monitor()
    return LatencyTracker(monitor, metric_name, labels)
