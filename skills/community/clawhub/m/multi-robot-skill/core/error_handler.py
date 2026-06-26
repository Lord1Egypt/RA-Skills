"""
错误处理器

负责处理任务执行过程中的错误和异常。
"""

from dataclasses import dataclass
from typing import Optional, Callable, Any
from enum import Enum
import logging
import time

from .task_planner import Task
from ..adapters.base import ActionResult, ActionStatus


logger = logging.getLogger(__name__)


class ErrorStrategy(Enum):
    """错误处理策略"""
    RETRY = "retry"          # 重试
    SKIP = "skip"            # 跳过
    ABORT = "abort"          # 中止
    ROLLBACK = "rollback"    # 回滚
    CONTINUE = "continue"    # 继续


@dataclass
class ErrorConfig:
    """错误处理配置"""
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 60.0
    default_strategy: ErrorStrategy = ErrorStrategy.RETRY
    on_error_callback: Optional[Callable] = None


class ErrorHandler:
    """
    错误处理器

    负责处理任务执行过程中的错误和异常。
    """

    def __init__(self, config: Optional[ErrorConfig] = None):
        self.config = config or ErrorConfig()
        self.error_history = []

    def handle_error(
        self,
        task: Task,
        error: Exception,
        strategy: Optional[ErrorStrategy] = None
    ) -> tuple[bool, Optional[str]]:
        """
        处理错误

        Args:
            task: 出错的任务
            error: 错误对象
            strategy: 错误处理策略（如果为None，使用默认策略）

        Returns:
            (bool, Optional[str]): (是否应该重试, 错误消息)
        """
        strategy = strategy or self.config.default_strategy

        # 记录错误
        error_record = {
            "task_id": task.id,
            "task_name": task.name,
            "error": str(error),
            "strategy": strategy.value,
            "timestamp": time.time()
        }
        self.error_history.append(error_record)

        logger.error(f"任务错误: {task.name}, 错误: {error}, 策略: {strategy.value}")

        # 调用回调
        if self.config.on_error_callback:
            try:
                self.config.on_error_callback(error_record)
            except Exception as e:
                logger.error(f"错误回调失败: {e}")

        # 根据策略处理
        if strategy == ErrorStrategy.RETRY:
            return self._handle_retry(task, error)
        elif strategy == ErrorStrategy.SKIP:
            return False, f"跳过任务: {task.name}"
        elif strategy == ErrorStrategy.ABORT:
            return False, f"中止执行: {task.name}"
        elif strategy == ErrorStrategy.ROLLBACK:
            return self._handle_rollback(task, error)
        elif strategy == ErrorStrategy.CONTINUE:
            return False, f"继续执行（忽略错误）: {task.name}"
        else:
            return False, f"未知策略: {strategy}"

    def _handle_retry(self, task: Task, error: Exception) -> tuple[bool, Optional[str]]:
        """处理重试"""
        if task.retry_count < task.max_retries:
            task.retry_count += 1
            logger.info(f"重试任务: {task.name}, 第 {task.retry_count}/{task.max_retries} 次")

            # 等待一段时间再重试
            time.sleep(self.config.retry_delay)

            return True, None
        else:
            return False, f"任务 {task.name} 重试次数已达上限"

    def _handle_rollback(self, task: Task, error: Exception) -> tuple[bool, Optional[str]]:
        """处理回滚"""
        logger.warning(f"回滚任务: {task.name}")
        # TODO: 实现回滚逻辑
        # 这需要记录每个任务的状态变化，以便回滚
        return False, f"任务 {task.name} 已回滚"

    def should_retry(self, task: Task, result: ActionResult) -> bool:
        """
        判断是否应该重试

        Args:
            task: 任务
            result: 执行结果

        Returns:
            bool: 是否应该重试
        """
        if result.status == ActionStatus.SUCCESS:
            return False

        if result.status == ActionStatus.TIMEOUT:
            # 超时总是重试
            return task.retry_count < task.max_retries

        if result.status == ActionStatus.FAILED:
            # 失败根据配置决定
            return task.retry_count < task.max_retries

        return False

    def get_error_history(self) -> list:
        """获取错误历史"""
        return self.error_history.copy()

    def clear_error_history(self):
        """清空错误历史"""
        self.error_history.clear()
