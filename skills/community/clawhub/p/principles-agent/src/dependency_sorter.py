"""
依赖拓扑排序
对原子子任务进行拓扑排序，识别可并行批次，检测循环依赖
"""
from typing import List, Dict, Set
from collections import deque

from types_def import SubTask, ExecutionPlan


class DependencySorter:
    """依赖排序器"""

    def sort(self, tasks: List[SubTask]) -> ExecutionPlan:
        """
        拓扑排序，返回有序任务列表和可并行批次
        """
        # 构建依赖图
        task_map: Dict[str, SubTask] = {t.id: t for t in tasks}
        adj: Dict[str, List[str]] = {t.id: [] for t in tasks}
        in_degree: Dict[str, int] = {t.id: 0 for t in tasks}

        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    adj[dep_id].append(task.id)
                    in_degree[task.id] += 1

        # Kahn's algorithm for topological sort
        queue = deque([t_id for t_id, degree in in_degree.items() if degree == 0])
        sorted_ids: List[str] = []
        parallel_batches: List[List[str]] = []

        while queue:
            # 当前批次就是所有入度为0的节点，可以并行执行
            current_batch = list(queue)
            parallel_batches.append(current_batch)
            for _ in range(len(queue)):
                u = queue.popleft()
                sorted_ids.append(u)
                for v in adj[u]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)

        # 检查循环依赖
        if len(sorted_ids) != len(tasks):
            remaining = set(t.id for t in tasks) - set(sorted_ids)
            details = f"检测到循环依赖，涉及节点: {', '.join(remaining)}"
            return ExecutionPlan(
                ordered_tasks=[],
                parallel_batches=[],
                has_circular_dependency=True,
                circular_dependency_details=details
            )

        # 转换回SubTask列表
        ordered_tasks = [task_map[t_id] for t_id in sorted_ids]
        parallel_task_batches = [
            [task_map[t_id] for t_id in batch]
            for batch in parallel_batches
        ]

        return ExecutionPlan(
            ordered_tasks=ordered_tasks,
            parallel_batches=parallel_task_batches,
            has_circular_dependency=False
        )

    def get_execution_order(self, plan: ExecutionPlan) -> List[List[SubTask]]:
        """获取分批执行顺序，每批可以并行执行"""
        return plan.parallel_batches
