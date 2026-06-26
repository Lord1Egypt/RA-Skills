"""
协调器

负责协调多个机器人执行任务计划。
"""

from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
import time
import logging

from .task_planner import Task, TaskPlan, TaskType
from ..adapters.base import RobotAdapter, ActionResult, ActionStatus


logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """执行模式"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"      # 并行执行
    AUTO = "auto"              # 自动决定


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    task_name: str
    success: bool
    message: str = ""
    data: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    error: Optional[Exception] = None
    subtask_results: List['ExecutionResult'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "execution_time": self.execution_time,
            "error": str(self.error) if self.error else None,
            "subtask_results": [r.to_dict() for r in self.subtask_results]
        }


class Coordinator:
    """
    协调器

    负责协调多个机器人执行任务计划。
    """

    def __init__(self, max_workers: int = 4):
        """
        初始化协调器

        Args:
            max_workers: 最大并行工作线程数
        """
        self.robots: Dict[str, RobotAdapter] = {}
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.event_callbacks: Dict[str, List[Callable]] = {}

    def register_robot(self, robot: RobotAdapter):
        """注册机器人"""
        self.robots[robot.name] = robot
        logger.info(f"注册机器人: {robot.name}")

    def unregister_robot(self, robot_name: str):
        """注销机器人"""
        if robot_name in self.robots:
            del self.robots[robot_name]
            logger.info(f"注销机器人: {robot_name}")

    def get_robot(self, robot_name: str) -> Optional[RobotAdapter]:
        """获取机器人"""
        return self.robots.get(robot_name)

    def on_event(self, event_name: str, callback: Callable):
        """注册事件回调"""
        if event_name not in self.event_callbacks:
            self.event_callbacks[event_name] = []
        self.event_callbacks[event_name].append(callback)

    def _emit_event(self, event_name: str, data: Any):
        """触发事件"""
        if event_name in self.event_callbacks:
            for callback in self.event_callbacks[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"事件回调错误: {e}")

    def execute_plan(self, plan: TaskPlan) -> List[ExecutionResult]:
        """
        执行任务计划

        Args:
            plan: 任务计划

        Returns:
            List[ExecutionResult]: 执行结果列表
        """
        logger.info(f"开始执行任务计划: {plan.name}")
        self._emit_event("plan_started", {"plan_id": plan.id, "plan_name": plan.name})

        start_time = time.time()
        results = []

        try:
            # 获取执行顺序（拓扑排序）
            execution_order = plan.get_execution_order()

            # 按批次执行
            for batch_idx, batch in enumerate(execution_order):
                logger.info(f"执行批次 {batch_idx + 1}/{len(execution_order)}, 任务数: {len(batch)}")

                # 批次内的任务可以并行执行
                batch_results = self._execute_batch(batch)
                results.extend(batch_results)

                # 检查是否有失败的任务
                failed_tasks = [r for r in batch_results if not r.success]
                if failed_tasks:
                    logger.warning(f"批次 {batch_idx + 1} 中有 {len(failed_tasks)} 个任务失败")
                    # 可以选择继续或中止
                    # 这里选择继续执行

            execution_time = time.time() - start_time
            logger.info(f"任务计划执行完成，耗时: {execution_time:.2f}秒")

            self._emit_event("plan_completed", {
                "plan_id": plan.id,
                "execution_time": execution_time,
                "total_tasks": len(results),
                "successful_tasks": sum(1 for r in results if r.success)
            })

        except Exception as e:
            logger.error(f"任务计划执行失败: {e}")
            self._emit_event("plan_failed", {"plan_id": plan.id, "error": str(e)})
            raise

        return results

    def _execute_batch(self, tasks: List[Task]) -> List[ExecutionResult]:
        """
        执行一批任务（并行）

        Args:
            tasks: 任务列表

        Returns:
            List[ExecutionResult]: 执行结果列表
        """
        if len(tasks) == 1:
            # 单个任务，直接执行
            return [self._execute_task(tasks[0])]

        # 多个任务，并行执行
        futures: Dict[Future, Task] = {}
        for task in tasks:
            future = self.executor.submit(self._execute_task, task)
            futures[future] = task

        results = []
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"任务执行异常: {task.name}, 错误: {e}")
                results.append(ExecutionResult(
                    task_id=task.id,
                    task_name=task.name,
                    success=False,
                    message=f"执行异常: {str(e)}",
                    error=e
                ))

        return results

    def _execute_task(self, task: Task) -> ExecutionResult:
        """
        执行单个任务

        Args:
            task: 任务

        Returns:
            ExecutionResult: 执行结果
        """
        logger.info(f"开始执行任务: {task.name} (ID: {task.id})")
        self._emit_event("task_started", {"task_id": task.id, "task_name": task.name})

        start_time = time.time()

        try:
            if task.task_type == TaskType.ATOMIC:
                # 原子任务
                result = self._execute_atomic_task(task)
            elif task.task_type == TaskType.PARALLEL:
                # 并行任务
                result = self._execute_parallel_task(task)
            elif task.task_type == TaskType.SEQUENTIAL:
                # 顺序任务
                result = self._execute_sequential_task(task)
            else:
                result = ExecutionResult(
                    task_id=task.id,
                    task_name=task.name,
                    success=False,
                    message=f"不支持的任务类型: {task.task_type}"
                )

            result.execution_time = time.time() - start_time

            if result.success:
                logger.info(f"任务完成: {task.name}, 耗时: {result.execution_time:.2f}秒")
                self._emit_event("task_completed", {
                    "task_id": task.id,
                    "execution_time": result.execution_time
                })
            else:
                logger.warning(f"任务失败: {task.name}, 原因: {result.message}")
                self._emit_event("task_failed", {
                    "task_id": task.id,
                    "error": result.message
                })

            return result

        except Exception as e:
            logger.error(f"任务执行异常: {task.name}, 错误: {e}")
            self._emit_event("task_error", {"task_id": task.id, "error": str(e)})
            return ExecutionResult(
                task_id=task.id,
                task_name=task.name,
                success=False,
                message=f"执行异常: {str(e)}",
                error=e,
                execution_time=time.time() - start_time
            )

    def _execute_atomic_task(self, task: Task) -> ExecutionResult:
        """执行原子任务"""
        if not task.robot or not task.action:
            return ExecutionResult(
                task_id=task.id,
                task_name=task.name,
                success=False,
                message="原子任务缺少 robot 或 action"
            )

        robot = self.get_robot(task.robot)
        if not robot:
            return ExecutionResult(
                task_id=task.id,
                task_name=task.name,
                success=False,
                message=f"机器人 {task.robot} 未注册"
            )

        # 执行动作
        action_result = robot.execute_action(task.action, task.params)

        return ExecutionResult(
            task_id=task.id,
            task_name=task.name,
            success=action_result.success,
            message=action_result.message,
            data=action_result.data,
            error=action_result.error
        )

    def _execute_parallel_task(self, task: Task) -> ExecutionResult:
        """执行并行任务"""
        subtask_results = self._execute_batch(task.subtasks)

        success = all(r.success for r in subtask_results)
        return ExecutionResult(
            task_id=task.id,
            task_name=task.name,
            success=success,
            message=f"并行任务完成，成功: {sum(1 for r in subtask_results if r.success)}/{len(subtask_results)}",
            subtask_results=subtask_results
        )

    def _execute_sequential_task(self, task: Task) -> ExecutionResult:
        """执行顺序任务"""
        subtask_results = []

        for subtask in task.subtasks:
            result = self._execute_task(subtask)
            subtask_results.append(result)

            # 如果失败，可以选择中止或继续
            if not result.success:
                logger.warning(f"顺序任务中的子任务失败: {subtask.name}")
                # 这里选择中止
                break

        success = all(r.success for r in subtask_results)
        return ExecutionResult(
            task_id=task.id,
            task_name=task.name,
            success=success,
            message=f"顺序任务完成，成功: {sum(1 for r in subtask_results if r.success)}/{len(task.subtasks)}",
            subtask_results=subtask_results
        )

    def shutdown(self):
        """关闭协调器"""
        logger.info("关闭协调器")
        self.executor.shutdown(wait=True)
