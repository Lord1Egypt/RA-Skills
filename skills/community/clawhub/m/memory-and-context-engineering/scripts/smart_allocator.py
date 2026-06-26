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
智能 Token 分配器 - Smart Token Allocator

实现动态 Token 预算分配，根据任务阶段和实际使用情况自适应调整。

分配策略：
- 规划阶段：30% Token（上下文理解）
- 设计阶段：25% Token（方案设计）
- 实现阶段：30% Token（编码实现）
- 验证阶段：15% Token（测试验证）

核心特性：
- 动态调整：基于实际使用比例反馈控制
- 预留缓冲：保留 10% 应急预算
- 超预算降级：逐级降级策略
- 阶段感知：根据任务阶段智能分配

性能目标：
- Token 使用率降低：30-50%
- 分配准确度：> 85%
- 响应时间：< 5ms
"""

import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class TaskStage(Enum):
    """任务阶段"""
    PLANNING = "planning"  # 规划阶段
    DESIGN = "design"  # 设计阶段
    IMPLEMENTATION = "implementation"  # 实现阶段
    VALIDATION = "validation"  # 验证阶段
    COMPLETED = "completed"  # 已完成


@dataclass
class StageAllocation:
    """阶段分配"""
    stage: TaskStage
    allocated_tokens: int  # 分配的 Token 数量
    used_tokens: int  # 已使用的 Token 数量
    target_ratio: float  # 目标占比
    actual_ratio: float  # 实际占比
    is_locked: bool = False  # 是否锁定（不参与调整）


@dataclass
class AllocationResult:
    """分配结果"""
    stage_allocations: Dict[TaskStage, StageAllocation]
    remaining_buffer: int  # 剩余缓冲
    total_used: int  # 总使用量
    total_allocated: int  # 总分配量


class SmartTokenAllocator:
    """
    智能 Token 分配器

    基于任务阶段动态分配 Token 预算
    """

    def __init__(
        self,
        total_budget: int = 10000,
        buffer_ratio: float = 0.1,  # 10% 缓冲
        learning_rate: float = 0.1,  # 学习率
        auto_adjust: bool = True,  # 是否自动调整
    ):
        """
        初始化分配器

        参数：
            total_budget: 总 Token 预算
            buffer_ratio: 缓冲比例
            learning_rate: 学习率（用于动态调整）
            auto_adjust: 是否自动调整
        """
        self.total_budget = total_budget
        self.buffer_ratio = buffer_ratio
        self.learning_rate = learning_rate
        self.auto_adjust = auto_adjust

        # 可用预算（扣除缓冲）
        self.available_budget = int(total_budget * (1 - buffer_ratio))
        self.buffer_budget = total_budget - self.available_budget

        # 初始分配比例
        self.default_ratios = {
            TaskStage.PLANNING: 0.30,
            TaskStage.DESIGN: 0.25,
            TaskStage.IMPLEMENTATION: 0.30,
            TaskStage.VALIDATION: 0.15,
        }

        # 当前分配
        self.stage_allocations: Dict[TaskStage, StageAllocation] = {}
        self._initialize_allocations()

        # 使用历史（用于学习）
        self.usage_history: deque = deque(maxlen=100)

        # 统计信息
        self.stats = {
            "total_allocations": 0,
            "total_adjustments": 0,
            "buffer_usages": 0,
            "overflows": 0,
        }

    def _initialize_allocations(self) -> None:
        """初始化各阶段分配"""
        for stage, ratio in self.default_ratios.items():
            allocated = int(self.available_budget * ratio)
            self.stage_allocations[stage] = StageAllocation(
                stage=stage,
                allocated_tokens=allocated,
                used_tokens=0,
                target_ratio=ratio,
                actual_ratio=ratio,
            )

    def allocate(
        self,
        stage: TaskStage,
        tokens: int,
        force: bool = False,
    ) -> bool:
        """
        分配 Token

        参数：
            stage: 任务阶段
            tokens: 需要的 Token 数量
            force: 是否强制分配（使用缓冲）

        返回：
            是否分配成功
        """
        if stage not in self.stage_allocations:
            return False

        allocation = self.stage_allocations[stage]

        # 检查是否超出分配
        remaining = allocation.allocated_tokens - allocation.used_tokens
        if tokens <= remaining:
            # 直接分配
            allocation.used_tokens += tokens
            self._update_actual_ratios()
            self.stats["total_allocations"] += 1
            return True

        # 超出分配，尝试从其他阶段借用
        shortage = tokens - remaining
        borrowed = self._borrow_tokens(stage, shortage, force)

        if borrowed > 0:
            allocation.used_tokens += tokens
            self._update_actual_ratios()
            self.stats["total_allocations"] += 1
            return True
        else:
            # 无法分配
            self.stats["overflows"] += 1
            return False

    def _borrow_tokens(
        self,
        current_stage: TaskStage,
        shortage: int,
        force: bool = False,
    ) -> int:
        """
        从其他阶段借用 Token

        策略：
        1. 优先从未锁定且有剩余的阶段借用
        2. 如果不足，使用缓冲
        3. 如果还不够，强制分配（如果 force=True）
        """
        borrowed = 0

        # 从其他阶段借用
        for stage, allocation in self.stage_allocations.items():
            if stage == current_stage:
                continue

            if allocation.is_locked:
                continue

            remaining = allocation.allocated_tokens - allocation.used_tokens
            if remaining > 0:
                # 借用剩余 Token
                borrow_amount = min(remaining, shortage - borrowed)
                allocation.used_tokens += borrow_amount
                borrowed += borrow_amount

                if borrowed >= shortage:
                    break

        # 如果还不够，使用缓冲
        if borrowed < shortage:
            buffer_shortage = shortage - borrowed
            buffer_remaining = self._get_buffer_remaining()

            if buffer_remaining >= buffer_shortage:
                borrowed += buffer_shortage
                self.stats["buffer_usages"] += 1
            elif force:
                # 强制使用所有缓冲
                borrowed += buffer_remaining
                self.stats["buffer_usages"] += 1

        return borrowed

    def _get_buffer_remaining(self) -> int:
        """获取剩余缓冲"""
        total_used = sum(a.used_tokens for a in self.stage_allocations.values())
        total_allocated = sum(a.allocated_tokens for a in self.stage_allocations.values())
        buffer_used = total_used - total_allocated
        buffer_remaining = self.buffer_budget - buffer_used
        return max(0, buffer_remaining)

    def _update_actual_ratios(self) -> None:
        """更新实际占比"""
        total_used = sum(a.used_tokens for a in self.stage_allocations.values())

        for stage, allocation in self.stage_allocations.items():
            if total_used > 0:
                allocation.actual_ratio = allocation.used_tokens / total_used
            else:
                allocation.actual_ratio = 0.0

    def adjust_allocations(
        self,
        performance_data: Optional[Dict[TaskStage, float]] = None,
    ) -> None:
        """
        调整分配（基于实际使用情况）

        参数：
            performance_data: 各阶段的性能数据（可选）
        """
        if not self.auto_adjust:
            return

        # 计算当前使用情况
        total_used = sum(a.used_tokens for a in self.stage_allocations.values())
        if total_used == 0:
            return

        # 计算偏差
        adjustments: Dict[TaskStage, float] = {}

        for stage, allocation in self.stage_allocations.items():
            target = allocation.target_ratio
            actual = allocation.actual_ratio

            # 计算偏差
            deviation = actual - target

            # 调整方向相反（如果实际使用多，减少分配）
            adjustments[stage] = -deviation * self.learning_rate

        # 应用调整（确保总和为0）
        adjustment_sum = sum(adjustments.values())
        if abs(adjustment_sum) > 0.01:
            # 归一化
            for stage in adjustments:
                adjustments[stage] -= adjustment_sum / len(adjustments)

        # 更新目标比例
        for stage, adjustment in adjustments.items():
            old_ratio = self.stage_allocations[stage].target_ratio
            new_ratio = max(0.05, min(0.50, old_ratio + adjustment))
            self.stage_allocations[stage].target_ratio = new_ratio

        # 重新分配
        self._reallocate()

        self.stats["total_adjustments"] += 1

    def _reallocate(self) -> None:
        """重新分配 Token"""
        # 计算新的分配量
        for stage, allocation in self.stage_allocations.items():
            new_allocated = int(self.available_budget * allocation.target_ratio)
            allocation.allocated_tokens = new_allocated

    def get_allocation(self, stage: TaskStage) -> StageAllocation:
        """获取阶段的分配信息"""
        if stage not in self.stage_allocations:
            raise ValueError(f"Unknown stage: {stage}")

        return self.stage_allocations[stage]

    def get_result(self) -> AllocationResult:
        """获取分配结果"""
        total_used = sum(a.used_tokens for a in self.stage_allocations.values())
        total_allocated = sum(a.allocated_tokens for a in self.stage_allocations.values())

        return AllocationResult(
            stage_allocations=self.stage_allocations.copy(),
            remaining_buffer=self._get_buffer_remaining(),
            total_used=total_used,
            total_allocated=total_allocated,
        )

    def reset(self) -> None:
        """重置分配器"""
        self._initialize_allocations()
        self.usage_history.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        result = self.get_result()

        return {
            **self.stats,
            "total_budget": self.total_budget,
            "available_budget": self.available_budget,
            "buffer_budget": self.buffer_budget,
            "buffer_remaining": result.remaining_buffer,
            "total_used": result.total_used,
            "usage_ratio": result.total_used / self.total_budget if self.total_budget > 0 else 0,
            "stage_breakdown": {
                stage.value: {
                    "allocated": a.allocated_tokens,
                    "used": a.used_tokens,
                    "target_ratio": a.target_ratio,
                    "actual_ratio": a.actual_ratio,
                }
                for stage, a in self.stage_allocations.items()
            },
        }

    def record_stage_completion(self, stage: TaskStage) -> None:
        """记录阶段完成"""
        # 记录使用情况到历史
        usage_info = {
            "stage": stage,
            "used_tokens": self.stage_allocations[stage].used_tokens,
            "allocated_tokens": self.stage_allocations[stage].allocated_tokens,
            "timestamp": datetime.now(),
        }
        self.usage_history.append(usage_info)

        # 自动调整
        if self.auto_adjust:
            self.adjust_allocations()

        # 锁定已完成的阶段（不再调整）
        self.stage_allocations[stage].is_locked = True


class AdaptiveTokenManager:
    """
    自适应 Token 管理器

    结合渐进式压缩和智能分配
    """

    def __init__(
        self,
        total_budget: int = 10000,
        allocator: Optional[SmartTokenAllocator] = None,
    ):
        """
        初始化管理器

        参数：
            total_budget: 总预算
            allocator: 分配器（默认创建新的）
        """
        self.total_budget = total_budget
        self.allocator = allocator or SmartTokenAllocator(total_budget)

        # 内容存储
        self.content_store: Dict[str, Any] = {}

    def add_content(
        self,
        stage: TaskStage,
        key: str,
        content: Any,
        token_count: int,
    ) -> bool:
        """
        添加内容

        参数：
            stage: 任务阶段
            key: 内容键
            content: 内容
            token_count: Token 数量

        返回：
            是否添加成功
        """
        # 分配 Token
        success = self.allocator.allocate(stage, token_count)

        if success:
            self.content_store[key] = {
                "content": content,
                "stage": stage,
                "token_count": token_count,
                "timestamp": datetime.now(),
            }

        return success

    def get_content(self, key: str) -> Optional[Any]:
        """获取内容"""
        if key in self.content_store:
            return self.content_store[key]["content"]
        return None

    def get_stage_content(self, stage: TaskStage) -> List[Any]:
        """获取指定阶段的所有内容"""
        return [
            item["content"]
            for item in self.content_store.values()
            if item["stage"] == stage
        ]

    def complete_stage(self, stage: TaskStage) -> None:
        """完成阶段"""
        self.allocator.record_stage_completion(stage)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "allocator": self.allocator.get_stats(),
            "content_count": len(self.content_store),
        }


# 使用示例
if __name__ == "__main__":
    print("=== 智能 Token 分配器示例 ===")

    # 创建分配器
    allocator = SmartTokenAllocator(
        total_budget=10000,
        buffer_ratio=0.1,
        auto_adjust=True,
    )

    # 查看初始分配
    print("\n初始分配:")
    result = allocator.get_result()
    for stage, allocation in result.stage_allocations.items():
        print(f"  {stage.value}: 分配={allocation.allocated_tokens}, 目标比例={allocation.target_ratio:.2%}")

    # 模拟各阶段使用
    print("\n模拟使用...")

    # 规划阶段：实际使用了 3500 Token（超过分配的 3000）
    print("\n规划阶段使用:")
    success = allocator.allocate(TaskStage.PLANNING, 3500)
    print(f"  分配 3500 Token: {'成功' if success else '失败'}")
    allocation = allocator.get_allocation(TaskStage.PLANNING)
    print(f"  已使用: {allocation.used_tokens}/{allocation.allocated_tokens}")

    # 设计阶段：使用了 2000 Token（低于分配的 2500）
    print("\n设计阶段使用:")
    success = allocator.allocate(TaskStage.DESIGN, 2000)
    print(f"  分配 2000 Token: {'成功' if success else '失败'}")
    allocation = allocator.get_allocation(TaskStage.DESIGN)
    print(f"  已使用: {allocation.used_tokens}/{allocation.allocated_tokens}")

    # 实现阶段：使用了 3000 Token（等于分配的 3000）
    print("\n实现阶段使用:")
    success = allocator.allocate(TaskStage.IMPLEMENTATION, 3000)
    print(f"  分配 3000 Token: {'成功' if success else '失败'}")
    allocation = allocator.get_allocation(TaskStage.IMPLEMENTATION)
    print(f"  已使用: {allocation.used_tokens}/{allocation.allocated_tokens}")

    # 查看当前状态
    print("\n当前状态:")
    result = allocator.get_result()
    print(f"  总使用: {result.total_used}")
    print(f"  剩余缓冲: {result.remaining_buffer}")
    print(f"  使用率: {result.total_used/allocator.total_budget:.2%}")

    for stage, allocation in result.stage_allocations.items():
        print(f"  {stage.value}: 使用={allocation.used_tokens}, 实际比例={allocation.actual_ratio:.2%}")

    # 完成规划阶段
    print("\n完成规划阶段，触发自动调整...")
    allocator.record_stage_completion(TaskStage.PLANNING)

    # 查看调整后的分配
    print("\n调整后的分配:")
    result = allocator.get_result()
    for stage, allocation in result.stage_allocations.items():
        print(f"  {stage.value}: 分配={allocation.allocated_tokens}, 目标比例={allocation.target_ratio:.2%}")

    # 统计信息
    print("\n统计信息:")
    stats = allocator.get_stats()
    print(f"  总分配次数: {stats['total_allocations']}")
    print(f"  调整次数: {stats['total_adjustments']}")
    print(f"  缓冲使用次数: {stats['buffer_usages']}")
    print(f"  超预算次数: {stats['overflows']}")

    # 自适应管理器示例
    print("\n=== 自适应 Token 管理器示例 ===")
    manager = AdaptiveTokenManager(total_budget=5000)

    # 添加内容
    manager.add_content(TaskStage.PLANNING, "plan1", "规划文档1", 1200)
    manager.add_content(TaskStage.PLANNING, "plan2", "规划文档2", 800)
    manager.add_content(TaskStage.DESIGN, "design1", "设计文档1", 1500)

    print(f"规划阶段内容: {len(manager.get_stage_content(TaskStage.PLANNING))}")
    print(f"设计阶段内容: {len(manager.get_stage_content(TaskStage.DESIGN))}")

    # 完成阶段
    manager.complete_stage(TaskStage.PLANNING)

    print(f"\n管理器统计:")
    stats = manager.get_stats()
    print(f"  总内容数: {stats['content_count']}")
    print(f"  分配器统计: {stats['allocator']}")
