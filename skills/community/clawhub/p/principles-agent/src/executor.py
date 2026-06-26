"""
子任务执行器
对接 OpenClaw sessions_spawn 执行子任务
"""
from typing import List, Dict, Any
import asyncio
import json

from types_def import SubTask, TaskResult, Goal


class OpenClawExecutor:
    """OpenClaw 子任务执行器"""

    def __init__(self, session_key: str = None):
        self.session_key = session_key

    def build_task_prompt(
        self,
        task: SubTask,
        goal: Goal,
        previous_results: Dict[str, TaskResult]
    ) -> str:
        """构建子任务执行提示词"""

        # 收集依赖任务的输出
        previous_outputs = ""
        for dep_id in task.dependencies:
            if dep_id in previous_results:
                result = previous_results[dep_id]
                previous_outputs += f"\n--- 来自 {dep_id} 的输出 ---\n"
                output_str = str(result.output)
                if len(output_str) > 2000:
                    output_str = output_str[:2000] + "\n... (已截断)"
                previous_outputs += output_str + "\n"

        template = f"""你现在需要执行一个原子子任务，这是基于第一性原理拆解得到的整体项目的一部分。

## 整体目标
{goal.clarified_objective}

## 当前子任务
**{task.title}**

{task.description}

## 验收标准
{chr(10).join(f'- {c}' for c in task.acceptance_criteria)}

## 来自前置依赖任务的输出
{previous_outputs if previous_outputs else '（无前置依赖）'}

---
请完成这个子任务，并确保输出满足所有验收标准。
"""
        return template

    def execute_task_sync(
        self,
        task: SubTask,
        goal: Goal,
        previous_results: Dict[str, TaskResult],
        llm_call
    ) -> TaskResult:
        """同步执行一个任务（调用LLM）"""
        import time
        start_time = time.time()

        prompt = self.build_task_prompt(task, goal, previous_results)

        try:
            # 调用传入的 LLM 函数
            output = llm_call(prompt)

            execution_time = int((time.time() - start_time) * 1000)

            return TaskResult(
                task_id=task.id,
                success=True,
                output=output,
                validation_passed=False,  # 需要后续验证
                execution_time_ms=execution_time
            )

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            return TaskResult(
                task_id=task.id,
                success=False,
                output=None,
                validation_passed=False,
                error_message=str(e),
                execution_time_ms=execution_time
            )

    def execute_parallel_batch(
        self,
        batch: List[SubTask],
        goal: Goal,
        previous_results: Dict[str, TaskResult],
        llm_call
    ) -> List[TaskResult]:
        """并行执行一批无依赖的任务"""
        results = []
        for task in batch:
            result = self.execute_task_sync(task, goal, previous_results, llm_call)
            results.append(result)
            previous_results[task.id] = result
        return results
