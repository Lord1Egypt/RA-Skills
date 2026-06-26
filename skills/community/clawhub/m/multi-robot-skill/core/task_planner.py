"""
任务规划器

负责将高层任务分解为可执行的子任务，并分析任务依赖关系。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from enum import Enum
import uuid


class TaskType(Enum):
    """任务类型"""
    ATOMIC = "atomic"        # 原子任务（单个动作）
    SEQUENTIAL = "sequential"  # 顺序任务
    PARALLEL = "parallel"    # 并行任务
    CONDITIONAL = "conditional"  # 条件任务


@dataclass
class Task:
    """任务定义"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    robot: Optional[str] = None  # 机器人名称
    action: Optional[str] = None  # 动作名称
    params: Dict[str, Any] = field(default_factory=dict)
    task_type: TaskType = TaskType.ATOMIC
    subtasks: List['Task'] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)  # 依赖的任务ID
    description: str = ""
    timeout: float = 60.0
    retry_count: int = 0
    max_retries: int = 3

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "robot": self.robot,
            "action": self.action,
            "params": self.params,
            "task_type": self.task_type.value,
            "subtasks": [t.to_dict() for t in self.subtasks],
            "depends_on": self.depends_on,
            "description": self.description,
            "timeout": self.timeout,
        }


@dataclass
class TaskPlan:
    """任务计划"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks.append(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_execution_order(self) -> List[List[Task]]:
        """
        获取任务执行顺序（拓扑排序）

        Returns:
            List[List[Task]]: 每个子列表中的任务可以并行执行
        """
        # 构建依赖图
        task_map = {task.id: task for task in self.tasks}
        in_degree = {task.id: len(task.depends_on) for task in self.tasks}

        # 找出所有没有依赖的任务
        ready_tasks = [task for task in self.tasks if not task.depends_on]

        execution_order = []

        while ready_tasks:
            # 当前批次可以并行执行
            execution_order.append(ready_tasks[:])

            # 处理完成的任务
            completed_ids = {task.id for task in ready_tasks}
            ready_tasks = []

            # 找出下一批可以执行的任务
            for task in self.tasks:
                if task.id in completed_ids:
                    continue

                # 检查依赖是否都已完成
                if all(dep_id in completed_ids or dep_id in [t.id for batch in execution_order for t in batch]
                       for dep_id in task.depends_on):
                    # 检查是否所有依赖都在已完成的批次中
                    all_deps_completed = True
                    for dep_id in task.depends_on:
                        found = False
                        for batch in execution_order:
                            if any(t.id == dep_id for t in batch):
                                found = True
                                break
                        if not found:
                            all_deps_completed = False
                            break

                    if all_deps_completed and task.id not in [t.id for t in ready_tasks]:
                        ready_tasks.append(task)

        return execution_order

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tasks": [t.to_dict() for t in self.tasks],
            "metadata": self.metadata,
        }


class TaskPlanner:
    """
    任务规划器

    负责将高层任务描述转换为可执行的任务计划。
    """

    def __init__(self):
        self.plans: Dict[str, TaskPlan] = {}

    def create_plan(self, name: str, description: str = "") -> TaskPlan:
        """创建新的任务计划"""
        plan = TaskPlan(name=name, description=description)
        self.plans[plan.id] = plan
        return plan

    def create_atomic_task(
        self,
        robot: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        name: str = "",
        description: str = "",
        depends_on: Optional[List[str]] = None,
        timeout: float = 60.0
    ) -> Task:
        """
        创建原子任务

        Args:
            robot: 机器人名称
            action: 动作名称
            params: 动作参数
            name: 任务名称
            description: 任务描述
            depends_on: 依赖的任务ID列表
            timeout: 超时时间（秒）

        Returns:
            Task: 创建的任务
        """
        return Task(
            name=name or f"{robot}.{action}",
            robot=robot,
            action=action,
            params=params or {},
            task_type=TaskType.ATOMIC,
            depends_on=depends_on or [],
            description=description,
            timeout=timeout
        )

    def create_parallel_task(
        self,
        subtasks: List[Task],
        name: str = "",
        description: str = "",
        depends_on: Optional[List[str]] = None
    ) -> Task:
        """
        创建并行任务

        Args:
            subtasks: 子任务列表（将并行执行）
            name: 任务名称
            description: 任务描述
            depends_on: 依赖的任务ID列表

        Returns:
            Task: 创建的任务
        """
        return Task(
            name=name or "parallel_task",
            task_type=TaskType.PARALLEL,
            subtasks=subtasks,
            depends_on=depends_on or [],
            description=description
        )

    def create_sequential_task(
        self,
        subtasks: List[Task],
        name: str = "",
        description: str = "",
        depends_on: Optional[List[str]] = None
    ) -> Task:
        """
        创建顺序任务

        Args:
            subtasks: 子任务列表（将顺序执行）
            name: 任务名称
            description: 任务描述
            depends_on: 依赖的任务ID列表

        Returns:
            Task: 创建的任务
        """
        return Task(
            name=name or "sequential_task",
            task_type=TaskType.SEQUENTIAL,
            subtasks=subtasks,
            depends_on=depends_on or [],
            description=description
        )

    def validate_plan(self, plan: TaskPlan) -> tuple[bool, Optional[str]]:
        """
        验证任务计划

        检查：
        1. 依赖关系是否有效（没有循环依赖）
        2. 所有依赖的任务是否存在
        3. 机器人和动作是否有效

        Returns:
            (bool, Optional[str]): (是否有效, 错误信息)
        """
        task_ids = {task.id for task in plan.tasks}

        # 检查依赖是否存在
        for task in plan.tasks:
            for dep_id in task.depends_on:
                if dep_id not in task_ids:
                    return False, f"任务 {task.name} 依赖的任务 {dep_id} 不存在"

        # 检查循环依赖
        if self._has_circular_dependency(plan):
            return False, "存在循环依赖"

        return True, None

    def _has_circular_dependency(self, plan: TaskPlan) -> bool:
        """检查是否有循环依赖"""
        task_map = {task.id: task for task in plan.tasks}
        visited = set()
        rec_stack = set()

        def dfs(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)

            task = task_map.get(task_id)
            if task:
                for dep_id in task.depends_on:
                    if dep_id not in visited:
                        if dfs(dep_id):
                            return True
                    elif dep_id in rec_stack:
                        return True

            rec_stack.remove(task_id)
            return False

        for task in plan.tasks:
            if task.id not in visited:
                if dfs(task.id):
                    return True

        return False

    def get_plan(self, plan_id: str) -> Optional[TaskPlan]:
        """获取任务计划"""
        return self.plans.get(plan_id)
