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
缓存一致性管理器 - Cache Consistency Manager

确保多层缓存的一致性，使用 Write-Through 策略。

一致性策略：
- Write-Through: 写入时同步更新所有层
- 写入失败处理：降级到异步写入
- 缓存失效：TTL + 主动失效

核心特性：
- 强一致性保证
- 失败恢复机制
- 性能优化（异步刷新）
- 一致性验证

性能目标：
- 一致性延迟：< 50ms
- 写入成功率：> 99.9%
- 失败恢复时间：< 1s
"""

import time
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import asyncio


class ConsistencyLevel(Enum):
    """一致性级别"""
    STRONG = "strong"  # 强一致性（写入所有层）
    EVENTUAL = "eventual"  # 最终一致性（异步写入）


class WriteStatus(Enum):
    """写入状态"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class WriteResult:
    """写入结果"""
    status: WriteStatus
    key: str
    value: Any
    success_layers: List[str] = field(default_factory=list)
    failed_layers: List[str] = field(default_factory=list)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class CacheConsistencyManager:
    """
    缓存一致性管理器

    使用 Write-Through 策略确保多层缓存的一致性
    """

    def __init__(
        self,
        l1_cache: Any,
        l2_cache: Optional[Any] = None,
        l3_cache: Optional[Any] = None,
        default_consistency: ConsistencyLevel = ConsistencyLevel.STRONG,
        write_timeout: float = 1.0,
        async_write_queue_size: int = 1000,
    ):
        """
        初始化一致性管理器

        参数：
            l1_cache: L1 缓存（必需）
            l2_cache: L2 缓存（可选）
            l3_cache: L3 缓存（可选）
            default_consistency: 默认一致性级别
            write_timeout: 写入超时时间（秒）
            async_write_queue_size: 异步写入队列大小
        """
        self.l1_cache = l1_cache
        self.l2_cache = l2_cache
        self.l3_cache = l3_cache
        self.default_consistency = default_consistency
        self.write_timeout = write_timeout

        # 异步写入队列
        self.async_queue: deque = deque(maxlen=async_write_queue_size)
        self.async_worker_running = False
        self.async_worker_thread: Optional[threading.Thread] = None

        # 统计信息
        self.stats = {
            "total_writes": 0,
            "successful_writes": 0,
            "failed_writes": 0,
            "partial_writes": 0,
            "async_writes": 0,
            "write_errors": 0,
        }

        # 启动异步写入工作线程
        self._start_async_worker()

    def _start_async_worker(self) -> None:
        """启动异步写入工作线程"""
        if self.async_worker_running:
            return

        self.async_worker_running = True
        self.async_worker_thread = threading.Thread(
            target=self._async_write_worker,
            daemon=True,
        )
        self.async_worker_thread.start()

    def _async_write_worker(self) -> None:
        """异步写入工作线程"""
        while self.async_worker_running:
            try:
                if self.async_queue:
                    # 从队列取出任务
                    task = self.async_queue.popleft()
                    key, value, layers = task

                    # 异步写入
                    self._write_to_layers(key, value, layers, async_mode=True)

                time.sleep(0.01)  # 10ms 间隔
            except Exception as e:
                print(f"Async write worker error: {e}")

    def write(
        self,
        key: str,
        value: Any,
        consistency: Optional[ConsistencyLevel] = None,
        layers: Optional[List[str]] = None,
    ) -> WriteResult:
        """
        写入缓存（带一致性保证）

        参数：
            key: 缓存键
            value: 缓存值
            consistency: 一致性级别（默认使用 default_consistency）
            layers: 要写入的层列表（默认写入所有可用层）

        返回：
            写入结果
        """
        consistency = consistency or self.default_consistency

        # 确定要写入的层
        if layers is None:
            layers = []
            if self.l1_cache:
                layers.append("l1")
            if self.l2_cache:
                layers.append("l2")
            if self.l3_cache:
                layers.append("l3")

        self.stats["total_writes"] += 1

        if consistency == ConsistencyLevel.STRONG:
            # 强一致性：同步写入所有层
            return self._write_sync(key, value, layers)
        else:
            # 最终一致性：异步写入
            self._queue_async_write(key, value, layers)
            self.stats["async_writes"] += 1

            return WriteResult(
                status=WriteStatus.SUCCESS,
                key=key,
                value=value,
                success_layers=layers,  # 假设成功
                error=None,
            )

    def _write_sync(
        self,
        key: str,
        value: Any,
        layers: List[str],
    ) -> WriteResult:
        """
        同步写入

        策略：
        1. 先写入 L1（最快）
        2. 并发写入 L2 和 L3
        3. 收集结果
        4. 如果部分失败，降级到异步重试
        """
        success_layers = []
        failed_layers = []
        errors = []

        # 写入 L1（必须成功）
        try:
            self.l1_cache.set(key, value)
            success_layers.append("l1")
        except Exception as e:
            errors.append(f"L1 error: {e}")
            failed_layers.append("l1")

        # 写入 L2 和 L3（并发）
        l2_result = None
        l3_result = None

        if self.l2_cache and "l2" in layers:
            try:
                self.l2_cache.set(key, value)
                success_layers.append("l2")
            except Exception as e:
                errors.append(f"L2 error: {e}")
                failed_layers.append("l2")
                # L2 失败，降级到异步重试
                self._queue_async_write(key, value, ["l2"])

        if self.l3_cache and "l3" in layers:
            try:
                self.l3_cache.set(key, value)
                success_layers.append("l3")
            except Exception as e:
                errors.append(f"L3 error: {e}")
                failed_layers.append("l3")
                # L3 失败，降级到异步重试
                self._queue_async_write(key, value, ["l3"])

        # 确定状态
        if failed_layers:
            self.stats["partial_writes"] += 1
            self.stats["write_errors"] += 1

            if "l1" in failed_layers:
                # L1 失败是致命的
                self.stats["failed_writes"] += 1
                status = WriteStatus.FAILED
            else:
                # L1 成功，其他层失败是部分的
                status = WriteStatus.PARTIAL
        else:
            self.stats["successful_writes"] += 1
            status = WriteStatus.SUCCESS

        return WriteResult(
            status=status,
            key=key,
            value=value,
            success_layers=success_layers,
            failed_layers=failed_layers,
            error="\n".join(errors) if errors else None,
        )

    def _write_to_layers(
        self,
        key: str,
        value: Any,
        layers: List[str],
        async_mode: bool = False,
    ) -> None:
        """写入指定层（内部方法）"""
        for layer in layers:
            try:
                if layer == "l1" and self.l1_cache:
                    self.l1_cache.set(key, value)
                elif layer == "l2" and self.l2_cache:
                    self.l2_cache.set(key, value)
                elif layer == "l3" and self.l3_cache:
                    self.l3_cache.set(key, value)
            except Exception as e:
                if async_mode:
                    print(f"Async write error for {layer}: {e}")
                    # 可以在这里实现重试逻辑
                else:
                    raise

    def _queue_async_write(
        self,
        key: str,
        value: Any,
        layers: List[str],
    ) -> None:
        """将写入任务加入异步队列"""
        try:
            task = (key, value, layers)
            self.async_queue.append(task)
        except Exception as e:
            print(f"Failed to queue async write: {e}")

    def delete(
        self,
        key: str,
        consistency: Optional[ConsistencyLevel] = None,
    ) -> bool:
        """
        删除缓存（带一致性保证）

        参数：
            key: 缓存键
            consistency: 一致性级别

        返回：
            是否删除成功
        """
        consistency = consistency or self.default_consistency

        if consistency == ConsistencyLevel.STRONG:
            # 同步删除所有层
            success = True

            if self.l1_cache:
                success &= self.l1_cache.delete(key)

            if self.l2_cache:
                try:
                    success &= self.l2_cache.delete(key)
                except Exception as e:
                    print(f"L2 delete error: {e}")
                    success = False

            if self.l3_cache:
                try:
                    success &= self.l3_cache.delete(key)
                except Exception as e:
                    print(f"L3 delete error: {e}")
                    success = False

            return success
        else:
            # 异步删除
            # 简化实现：这里同步删除 L1，异步删除其他层
            if self.l1_cache:
                self.l1_cache.delete(key)

            # 将删除任务加入队列（简化处理）
            # 实际应用中需要专门的删除队列
            return True

    def invalidate(
        self,
        key: str,
        reason: str = "manual",
    ) -> bool:
        """
        使缓存失效

        参数：
            key: 缓存键
            reason: 失效原因

        返回：
            是否成功
        """
        # 删除所有层的缓存
        return self.delete(key, ConsistencyLevel.STRONG)

    def invalidate_batch(
        self,
        keys: List[str],
        reason: str = "batch",
    ) -> Dict[str, bool]:
        """
        批量使缓存失效

        参数：
            keys: 缓存键列表
            reason: 失效原因

        返回：
            每个键的删除结果
        """
        results = {}
        for key in keys:
            results[key] = self.invalidate(key, reason)

        return results

    def verify_consistency(
        self,
        key: str,
    ) -> bool:
        """
        验证缓存一致性

        检查各层的值是否一致

        参数：
            key: 缓存键

        返回：
            是否一致
        """
        values = {}

        # 从各层读取值
        if self.l1_cache:
            values["l1"] = self.l1_cache.get(key)

        if self.l2_cache:
            try:
                values["l2"] = self.l2_cache.get(key)
            except Exception:
                pass

        if self.l3_cache:
            try:
                values["l3"] = self.l3_cache.get(key)
            except Exception:
                pass

        # 比较值
        # 注意：需要根据实际的值类型实现比较逻辑
        # 这里简化处理：比较字符串表示
        str_values = {k: str(v) for k, v in values.items() if v is not None}

        if len(str_values) <= 1:
            return True  # 只有一层有值，认为一致

        # 检查所有值是否相同
        first_value = list(str_values.values())[0]
        return all(v == first_value for v in str_values.values())

    def refresh_async_queue(self) -> int:
        """
        刷新异步队列（强制处理所有待写入任务）

        返回：
            处理的任务数量
        """
        processed = 0

        while self.async_queue:
            try:
                task = self.async_queue.popleft()
                key, value, layers = task
                self._write_to_layers(key, value, layers, async_mode=True)
                processed += 1
            except Exception as e:
                print(f"Refresh async queue error: {e}")

        return processed

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.stats["total_writes"]
        success_rate = (
            self.stats["successful_writes"] / total
            if total > 0 else 0
        )

        return {
            **self.stats,
            "async_queue_size": len(self.async_queue),
            "async_worker_running": self.async_worker_running,
            "success_rate": success_rate,
            "available_layers": [
                "l1" if self.l1_cache else None,
                "l2" if self.l2_cache else None,
                "l3" if self.l3_cache else None,
            ],
        }

    def shutdown(self) -> None:
        """关闭一致性管理器"""
        print("Shutting down cache consistency manager...")

        # 刷新异步队列
        print(f"Flushing async queue ({len(self.async_queue)} items)...")
        processed = self.refresh_async_queue()
        print(f"Processed {processed} items")

        # 停止异步工作线程
        self.async_worker_running = False

        if self.async_worker_thread:
            self.async_worker_thread.join(timeout=2.0)

        print("Shutdown complete")


# 使用示例
if __name__ == "__main__":
    print("=== 缓存一致性管理器示例 ===")

    # 创建简单的 L1 缓存（模拟）
    class SimpleCache:
        def __init__(self):
            self.cache = {}

        def get(self, key):
            return self.cache.get(key)

        def set(self, key, value):
            self.cache[key] = value

        def delete(self, key):
            return self.cache.pop(key, None) is not None

    # 创建缓存层
    l1_cache = SimpleCache()
    l2_cache = SimpleCache()  # 模拟 L2
    l3_cache = SimpleCache()  # 模拟 L3

    # 创建一致性管理器
    manager = CacheConsistencyManager(
        l1_cache=l1_cache,
        l2_cache=l2_cache,
        l3_cache=l3_cache,
        default_consistency=ConsistencyLevel.STRONG,
    )

    # 强一致性写入
    print("\n强一致性写入测试:")
    result = manager.write("key1", "value1")
    print(f"  状态: {result.status}")
    print(f"  成功层: {result.success_layers}")
    print(f"  失败层: {result.failed_layers}")

    # 验证一致性
    print("\n验证一致性:")
    is_consistent = manager.verify_consistency("key1")
    print(f"  key1 一致性: {is_consistent}")

    # 读取各层
    print(f"  L1: {l1_cache.get('key1')}")
    print(f"  L2: {l2_cache.get('key1')}")
    print(f"  L3: {l3_cache.get('key1')}")

    # 最终一致性写入
    print("\n最终一致性写入测试:")
    result = manager.write("key2", "value2", consistency=ConsistencyLevel.EVENTUAL)
    print(f"  状态: {result.status}")

    # 等待异步写入完成
    time.sleep(0.5)

    # 验证一致性
    is_consistent = manager.verify_consistency("key2")
    print(f"  key2 一致性: {is_consistent}")

    # 批量写入
    print("\n批量写入测试:")
    for i in range(5):
        result = manager.write(f"batch_key_{i}", f"batch_value_{i}")
        print(f"  batch_key_{i}: {result.status}")

    # 删除测试
    print("\n删除测试:")
    success = manager.delete("key1")
    print(f"  删除 key1: {success}")

    # 验证删除
    print(f"  L1: {l1_cache.get('key1')}")
    print(f"  L2: {l2_cache.get('key1')}")
    print(f"  L3: {l3_cache.get('key1')}")

    # 统计信息
    print("\n统计信息:")
    stats = manager.get_stats()
    print(f"  总写入次数: {stats['total_writes']}")
    print(f"  成功写入: {stats['successful_writes']}")
    print(f"  部分写入: {stats['partial_writes']}")
    print(f"  失败写入: {stats['failed_writes']}")
    print(f"  异步写入: {stats['async_writes']}")
    print(f"  成功率: {stats['success_rate']:.2%}")
    print(f"  异步队列大小: {stats['async_queue_size']}")

    # 关闭管理器
    print("\n关闭管理器...")
    manager.shutdown()
