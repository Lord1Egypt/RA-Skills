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
错误处理和降级策略模块

设计目标：
1. 识别不同类型的故障
2. 设计合理的降级策略
3. 在降级后自动恢复
4. 避免降级时的状态不一致

降级策略矩阵：
| 故障类型 | 降级策略 | 恢复条件 | 数据一致性 |
|---------|---------|---------|-----------|
| Redis 不可用 | 文件存储 | Redis 可用 | 最终一致 |
| 磁盘不可用 | 内存缓存 | 磁盘可用 | 可能丢失 |
| 内存不足 | 清理缓存 | 内存充足 | 保留热点 |
| 网络超时 | 本地缓存 | 网络恢复 | 延迟同步 |

工具调用集成：
本模块支持 Agent 工具调用的降级策略，详见：
references/agent_tools_use_rules.md

- 支持工具调用错误分类
- 支持结构化反思流程
- 支持工具调用特定的降级路径
"""

import asyncio
import json
import os
import time
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from pydantic import BaseModel, Field

# ============================================================================
# 故障类型枚举
# ============================================================================


class FaultType(str, Enum):
    """故障类型"""

    REDIS_UNAVAILABLE = "redis_unavailable"
    DISK_UNAVAILABLE = "disk_unavailable"
    MEMORY_INSUFFICIENT = "memory_insufficient"
    NETWORK_TIMEOUT = "network_timeout"
    SERVICE_UNAVAILABLE = "service_unavailable"
    UNKNOWN = "unknown"


class FallbackLevel(str, Enum):
    """降级级别"""

    NORMAL = "normal"  # 正常运行
    DEGRADED = "degraded"  # 功能降级
    MINIMAL = "minimal"  # 最小功能
    UNAVAILABLE = "unavailable"  # 不可用


# ============================================================================
# 故障事件
# ============================================================================


@dataclass
class FaultEvent:
    """故障事件"""

    fault_type: FaultType
    timestamp: datetime = field(default_factory=datetime.now)
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False


# ============================================================================
# 降级策略配置
# ============================================================================


class FallbackConfig(BaseModel):
    """降级策略配置"""

    # Redis 降级配置
    redis_fallback_to_file: bool = True
    redis_retry_interval: float = 5.0  # 重试间隔（秒）
    redis_max_retries: int = 3

    # 磁盘降级配置
    disk_fallback_to_memory: bool = True
    disk_retry_interval: float = 10.0
    disk_max_retries: int = 2

    # 内存降级配置
    memory_cleanup_threshold: float = 0.8  # 内存使用率阈值
    memory_cache_max_size: int = 1000  # 最大缓存条目数

    # 网络降级配置
    network_timeout: float = 5.0
    network_retry_interval: float = 2.0
    network_max_retries: int = 5

    # 通用配置
    enable_auto_recovery: bool = True
    recovery_check_interval: float = 10.0  # 恢复检查间隔


# ============================================================================
# 降级管理器
# ============================================================================


class FallbackManager:
    """
    降级管理器

    职责：
    1. 监控系统状态
    2. 检测故障
    3. 执行降级策略
    4. 自动恢复
    """

    def __init__(self, config: Optional[FallbackConfig] = None):
        """
        初始化降级管理器

        Args:
            config: 降级策略配置
        """
        self.config = config or FallbackConfig()
        self.current_level: FallbackLevel = FallbackLevel.NORMAL
        self.fault_events: List[FaultEvent] = []
        self.recovery_tasks: Dict[FaultType, asyncio.Task] = {}

        # 降级回调函数
        self.fallback_callbacks: Dict[FaultType, List[Callable]] = {}

        # 恢复回调函数
        self.recovery_callbacks: Dict[FaultType, List[Callable]] = {}

    # ========================================================================
    # 故障检测与处理
    # ========================================================================

    async def detect_fault(self, fault_type: FaultType, message: str = "", **metadata) -> bool:
        """
        检测故障

        Args:
            fault_type: 故障类型
            message: 故障消息
            **metadata: 额外元数据

        Returns:
            是否需要降级
        """
        # 记录故障事件
        event = FaultEvent(
            fault_type=fault_type,
            message=message,
            metadata=metadata,
        )
        self.fault_events.append(event)

        print(f"[FallbackManager] 检测到故障: {fault_type.value} - {message}")

        # 执行降级策略
        need_fallback = await self._execute_fallback(fault_type)

        if need_fallback:
            # 触发降级回调
            await self._trigger_fallback_callbacks(fault_type)

            # 启动自动恢复任务
            if self.config.enable_auto_recovery:
                await self._start_recovery_task(fault_type)

        return need_fallback

    async def _execute_fallback(self, fault_type: FaultType) -> bool:
        """
        执行降级策略

        Args:
            fault_type: 故障类型

        Returns:
            是否需要降级
        """
        if fault_type == FaultType.REDIS_UNAVAILABLE:
            if self.config.redis_fallback_to_file:
                print("[FallbackManager] Redis 降级到文件存储")
                self.current_level = FallbackLevel.DEGRADED
                return True

        elif fault_type == FaultType.DISK_UNAVAILABLE:
            if self.config.disk_fallback_to_memory:
                print("[FallbackManager] 磁盘降级到内存缓存")
                self.current_level = FallbackLevel.MINIMAL
                return True

        elif fault_type == FaultType.MEMORY_INSUFFICIENT:
            print("[FallbackManager] 内存不足，清理缓存")
            await self._cleanup_memory()
            return True

        elif fault_type == FaultType.NETWORK_TIMEOUT:
            print("[FallbackManager] 网络超时，使用本地缓存")
            self.current_level = FallbackLevel.DEGRADED
            return True

        return False

    async def _cleanup_memory(self):
        """清理内存缓存"""
        # TODO: 实现内存清理逻辑
        print("[FallbackManager] 执行内存清理...")
        await asyncio.sleep(0.1)

    # ========================================================================
    # 自动恢复
    # ========================================================================

    async def _start_recovery_task(self, fault_type: FaultType):
        """
        启动自动恢复任务

        Args:
            fault_type: 故障类型
        """
        if fault_type in self.recovery_tasks:
            # 任务已在运行
            return

        task = asyncio.create_task(self._auto_recovery(fault_type))
        self.recovery_tasks[fault_type] = task

    async def _auto_recovery(self, fault_type: FaultType):
        """
        自动恢复

        Args:
            fault_type: 故障类型
        """
        print(f"[FallbackManager] 启动自动恢复任务: {fault_type.value}")

        while True:
            await asyncio.sleep(self.config.recovery_check_interval)

            # 检查是否恢复
            recovered = await self._check_recovery(fault_type)

            if recovered:
                print(f"[FallbackManager] 故障已恢复: {fault_type.value}")

                # 标记故障已解决
                for event in self.fault_events:
                    if event.fault_type == fault_type and not event.resolved:
                        event.resolved = True

                # 触发恢复回调
                await self._trigger_recovery_callbacks(fault_type)

                # 清理恢复任务
                if fault_type in self.recovery_tasks:
                    del self.recovery_tasks[fault_type]

                break

    async def _check_recovery(self, fault_type: FaultType) -> bool:
        """
        检查是否恢复

        Args:
            fault_type: 故障类型

        Returns:
            是否恢复
        """
        # TODO: 实现具体的恢复检查逻辑
        if fault_type == FaultType.REDIS_UNAVAILABLE:
            # 检查 Redis 是否可用
            return await self._check_redis_available()

        elif fault_type == FaultType.DISK_UNAVAILABLE:
            # 检查磁盘是否可用
            return await self._check_disk_available()

        elif fault_type == FaultType.NETWORK_TIMEOUT:
            # 检查网络是否恢复
            return await self._check_network_available()

        return False

    async def _check_redis_available(self) -> bool:
        """检查 Redis 是否可用"""
        # TODO: 实现实际的 Redis 检查
        return False

    async def _check_disk_available(self) -> bool:
        """检查磁盘是否可用"""
        # TODO: 实现实际的磁盘检查
        try:
            temp_file = Path("/tmp/fallback_test.tmp")
            temp_file.write_text("test")
            temp_file.unlink()
            return True
        except Exception:
            return False

    async def _check_network_available(self) -> bool:
        """检查网络是否可用"""
        # TODO: 实现实际的网络检查
        return False

    # ========================================================================
    # 回调管理
    # ========================================================================

    def register_fallback_callback(self, fault_type: FaultType, callback: Callable):
        """
        注册降级回调

        Args:
            fault_type: 故障类型
            callback: 回调函数
        """
        if fault_type not in self.fallback_callbacks:
            self.fallback_callbacks[fault_type] = []
        self.fallback_callbacks[fault_type].append(callback)

    def register_recovery_callback(self, fault_type: FaultType, callback: Callable):
        """
        注册恢复回调

        Args:
            fault_type: 故障类型
            callback: 回调函数
        """
        if fault_type not in self.recovery_callbacks:
            self.recovery_callbacks[fault_type] = []
        self.recovery_callbacks[fault_type].append(callback)

    async def _trigger_fallback_callbacks(self, fault_type: FaultType):
        """触发降级回调"""
        callbacks = self.fallback_callbacks.get(fault_type, [])
        for callback in callbacks:
            try:
                await callback(fault_type)
            except Exception as e:
                print(f"[FallbackManager] 降级回调执行失败: {e}")

    async def _trigger_recovery_callbacks(self, fault_type: FaultType):
        """触发恢复回调"""
        callbacks = self.recovery_callbacks.get(fault_type, [])
        for callback in callbacks:
            try:
                await callback(fault_type)
            except Exception as e:
                print(f"[FallbackManager] 恢复回调执行失败: {e}")

    # ========================================================================
    # 状态查询
    # ========================================================================

    def get_current_level(self) -> FallbackLevel:
        """获取当前降级级别"""
        return self.current_level

    def get_fault_events(
        self,
        fault_type: Optional[FaultType] = None,
        resolved: Optional[bool] = None,
        limit: int = 100,
    ) -> List[FaultEvent]:
        """
        获取故障事件

        Args:
            fault_type: 故障类型（可选）
            resolved: 是否已解决（可选）
            limit: 返回数量限制

        Returns:
            故障事件列表
        """
        events = self.fault_events[-limit:]

        if fault_type is not None:
            events = [e for e in events if e.fault_type == fault_type]

        if resolved is not None:
            events = [e for e in events if e.resolved == resolved]

        return events

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息
        """
        total_faults = len(self.fault_events)
        resolved_faults = len([e for e in self.fault_events if e.resolved])

        # 按类型统计
        fault_counts = {}
        for event in self.fault_events:
            fault_type = event.fault_type.value
            fault_counts[fault_type] = fault_counts.get(fault_type, 0) + 1

        return {
            "current_level": self.current_level.value,
            "total_faults": total_faults,
            "resolved_faults": resolved_faults,
            "unresolved_faults": total_faults - resolved_faults,
            "fault_counts": fault_counts,
        }


# ============================================================================
# 降级上下文管理器
# ============================================================================


class FallbackContext:
    """
    降级上下文管理器

    用于在特定操作中处理降级逻辑
    """

    def __init__(self, fallback_manager: FallbackManager, fault_type: FaultType):
        """
        初始化降级上下文

        Args:
            fallback_manager: 降级管理器
            fault_type: 故障类型
        """
        self.fallback_manager = fallback_manager
        self.fault_type = fault_type

    async def __aenter__(self):
        """进入上下文"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if exc_type is not None:
            # 发生异常，检测故障
            await self.fallback_manager.detect_fault(
                self.fault_type,
                message=str(exc_val),
            )
        return False


# ============================================================================
# 工厂函数
# ============================================================================


_fallback_manager_instance: Optional[FallbackManager] = None


def get_fallback_manager(config: Optional[FallbackConfig] = None) -> FallbackManager:
    """
    获取降级管理器实例（单例）

    Args:
        config: 降级策略配置

    Returns:
        降级管理器实例
    """
    global _fallback_manager_instance

    if _fallback_manager_instance is None:
        _fallback_manager_instance = FallbackManager(config)

    return _fallback_manager_instance
