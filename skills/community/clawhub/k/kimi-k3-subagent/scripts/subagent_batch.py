"""SubagentBatch - 两阶段批量调度引擎

借鉴 Kimi Code SubagentBatch 架构:
- 正常阶段: 启动5个, 之后每700ms启动1个
- 限流阶段: 指数退避 + 容量收缩/恢复
- 区分 started/not_started 状态
- 超时只失败当前任务, 不影响批次
"""

import asyncio
import time
import logging
import math
from typing import Any, Callable, Optional

from .subagent_types import (
    SubagentResult,
    SubagentState,
    QueuedSubagentTask,
    TaskState,
    SubagentSuspendedEvent,
    TokenUsage,
)

logger = logging.getLogger("subagent_batch")

# 正常阶段参数
INITIAL_LAUNCH_LIMIT = 5
INITIAL_LAUNCH_INTERVAL_MS = 700

# 限流阶段参数
RATE_LIMIT_RETRY_BASE_MS = 3000
RATE_LIMIT_RETRY_FACTOR = 2
RATE_LIMIT_CAPACITY_SHRINK_INTERVAL_MS = 2000
RATE_LIMIT_CAPACITY_RECOVERY_INTERVAL_MS = 3 * 60 * 1000  # 3分钟

# 环境变量
AGENT_SWARM_MAX_CONCURRENCY_ENV = "KIMI_CODE_AGENT_SWARM_MAX_CONCURRENCY"


class SubagentBatch:
    """两阶段批量调度器"""

    def __init__(
        self,
        launcher,
        tasks: list[QueuedSubagentTask],
        max_concurrency: Optional[int] = None,
    ):
        self.launcher = launcher
        self.states = [TaskState(index=i, task=t) for i, t in enumerate(tasks)]
        self.pending = list(self.states)
        self.results: list[Optional[SubagentResult]] = [None] * len(tasks)
        self.active = set()
        self.controller = asyncio.Event()
        self.max_concurrency = max_concurrency

        # 调度状态
        self.normal_launch_count = 0
        self.rate_limit_mode = False
        self.started_success_count = 0
        self.rate_limit_capacity = 1
        self.last_rate_limit_at: Optional[float] = None
        self.last_capacity_shrink_at: Optional[float] = None
        self.last_capacity_recovery_at: Optional[float] = None
        self.global_retry_interval_ms = RATE_LIMIT_RETRY_BASE_MS
        self.next_rate_limit_launch_at = 0.0

    async def run(self) -> list[SubagentResult]:
        """执行批量调度"""
        if not self.states:
            return []

        self._schedule()
        # 等待所有任务完成
        while not self._is_complete():
            await asyncio.sleep(0.1)

        return [r for r in self.results if r is not None]

    def _schedule(self):
        """主调度循环"""
        if self._is_complete():
            return

        if self.rate_limit_mode:
            self._schedule_rate_limit_launch()
        else:
            self._schedule_normal_launch()

    def _schedule_normal_launch(self):
        """正常阶段调度"""
        # 立即启动5个
        while (
            self.normal_launch_count < INITIAL_LAUNCH_LIMIT
            and self.pending
            and not self.rate_limit_mode
            and not self._at_concurrency_limit()
        ):
            state = self.pending.pop(0)
            self._start_attempt(state)
            self.normal_launch_count += 1

        # 每700ms启动1个
        if self.pending and not self.rate_limit_mode and not self._at_concurrency_limit():
            asyncio.get_event_loop().call_later(
                INITIAL_LAUNCH_INTERVAL_MS / 1000,
                lambda: self._normal_launch_tick()
            )

    def _normal_launch_tick(self):
        """正常阶段定时启动"""
        if self._is_complete() or self.rate_limit_mode or not self.pending:
            return
        if self._at_concurrency_limit():
            return
        state = self.pending.pop(0)
        self._start_attempt(state)
        self.normal_launch_count += 1
        self._schedule()

    def _schedule_rate_limit_launch(self):
        """限流阶段调度"""
        if not self.pending:
            return

        now = time.time() * 1000
        self._recover_rate_limit_capacity(now)

        if len(self.active) >= self.rate_limit_capacity:
            # 容量满了, 等恢复
            next_wake = self._next_capacity_recovery_at()
            if next_wake > now:
                asyncio.get_event_loop().call_later(
                    (next_wake - now) / 1000,
                    lambda: self._schedule()
                )
            return

        # 找第一个可重试的任务
        next_allowed = max(self.next_rate_limit_launch_at, self._next_pending_ready_at())
        if next_allowed > now:
            asyncio.get_event_loop().call_later(
                (next_allowed - now) / 1000,
                lambda: self._schedule()
            )
            return

        # 找第一个到期可启动的任务
        pending_idx = None
        for i, state in enumerate(self.pending):
            if state.retry_ready_at <= now:
                pending_idx = i
                break

        if pending_idx is not None:
            state = self.pending.pop(pending_idx)
            self._start_attempt(state)
            self.next_rate_limit_launch_at = now + self.global_retry_interval_ms

    def _start_attempt(self, state: TaskState):
        """启动一个任务尝试"""
        if self.controller.is_set():
            return

        attempt = {
            "state": state,
            "controller": asyncio.Event(),
            "ready": False,
            "timed_out": False,
        }
        self.active.add(id(attempt))
        # 异步执行
        asyncio.create_task(self._run_attempt(attempt, state))

    async def _run_attempt(self, attempt: dict, state: TaskState):
        """执行单个任务"""
        task = state.task
        try:
            # 启动
            handle = await self.launcher.spawn(
                profile_name=task.profile_name,
                prompt=task.prompt,
                description=task.description,
                model_choice=task.model_choice,
                run_in_background=task.run_in_background,
            )
            state.agent_id = handle.agent_id
            state.started = True
            attempt["ready"] = True

            if not self.rate_limit_mode:
                self.started_success_count += 1

            # 等待完成
            result = await handle.completion
            self._handle_attempt_complete(attempt, state, result)

        except Exception as e:
            self._handle_attempt_error(attempt, state, e)

    def _handle_attempt_complete(self, attempt: dict, state: TaskState, result: SubagentResult):
        """处理任务完成"""
        if not self._release_attempt(attempt):
            return

        self.results[state.index] = result
        self._schedule()

    def _handle_attempt_error(self, attempt: dict, state: TaskState, error: Exception):
        """处理任务错误"""
        if not self._release_attempt(attempt):
            return

        error_str = str(error)
        is_rate_limit = "rate_limit" in error_str.lower()

        if is_rate_limit and not self._is_only_unfinished_task(state):
            # 限流: 重试
            self._requeue_rate_limited(attempt, state)
        else:
            # 其他错误: 标记失败
            self.results[state.index] = SubagentResult(
                task=state.task,
                agent_id=state.agent_id,
                status="failed",
                error=error_str,
            )

        self._schedule()

    def _requeue_rate_limited(self, attempt: dict, state: TaskState):
        """限流重试"""
        now = time.time() * 1000
        self.last_rate_limit_at = now
        state.retry_count += 1

        # 指数退避
        retry_delay = RATE_LIMIT_RETRY_BASE_MS * (RATE_LIMIT_RETRY_FACTOR ** (state.retry_count - 1))
        state.retry_ready_at = now + retry_delay
        self.pending.insert(0, state)  # 插回队列头部

        # 进入限流模式
        self._enter_rate_limit_mode(now)

        if not attempt.get("ready", False):
            self.global_retry_interval_ms = max(
                self.global_retry_interval_ms * 2, retry_delay
            )
            self.next_rate_limit_launch_at = max(
                self.next_rate_limit_launch_at, now + self.global_retry_interval_ms
            )
        else:
            self.next_rate_limit_launch_at = max(
                self.next_rate_limit_launch_at, now + RATE_LIMIT_RETRY_BASE_MS
            )

    def _enter_rate_limit_mode(self, now: float):
        """进入限流模式"""
        if not self.rate_limit_mode:
            self.rate_limit_mode = True
            self.rate_limit_capacity = max(1, self.started_success_count)
            self.next_rate_limit_launch_at = max(
                self.next_rate_limit_launch_at, now + RATE_LIMIT_RETRY_BASE_MS
            )
            self._shrink_capacity(now, force=True)
        else:
            self._shrink_capacity(now, force=False)

    def _shrink_capacity(self, now: float, force: bool):
        """收缩容量"""
        if (
            not force
            and self.last_capacity_shrink_at is not None
            and now - self.last_capacity_shrink_at < RATE_LIMIT_CAPACITY_SHRINK_INTERVAL_MS
        ):
            return
        self.rate_limit_capacity = max(1, self.rate_limit_capacity - 1)
        self.last_capacity_shrink_at = now

    def _recover_rate_limit_capacity(self, now: float):
        """恢复容量"""
        next_recovery = self._next_capacity_recovery_at()
        if next_recovery > now:
            return
        self.rate_limit_capacity += 1
        self.last_capacity_recovery_at = now
        self.next_rate_limit_launch_at = min(self.next_rate_limit_launch_at, now)

    def _next_capacity_recovery_at(self) -> float:
        """下次容量恢复时间"""
        if not self.pending or self.last_rate_limit_at is None:
            return float("inf")
        latest_change = max(
            self.last_rate_limit_at,
            self.last_capacity_recovery_at or 0,
        )
        return latest_change + RATE_LIMIT_CAPACITY_RECOVERY_INTERVAL_MS

    def _next_pending_ready_at(self) -> float:
        """下一个待处理任务的就绪时间"""
        return min(
            (state.retry_ready_at for state in self.pending),
            default=float("inf"),
        )

    def _at_concurrency_limit(self) -> bool:
        """是否达到并发上限"""
        if self.max_concurrency is None:
            return False
        return len(self.active) >= self.max_concurrency

    def _is_complete(self) -> bool:
        """是否全部完成"""
        return all(r is not None for r in self.results)

    def _is_only_unfinished_task(self, state: TaskState) -> bool:
        """是否是唯一未完成任务"""
        return all(
            r is not None or i == state.index
            for i, r in enumerate(self.results)
        )

    def _release_attempt(self, attempt: dict) -> bool:
        """释放任务尝试"""
        try:
            self.active.remove(id(attempt))
            return True
        except KeyError:
            return False
