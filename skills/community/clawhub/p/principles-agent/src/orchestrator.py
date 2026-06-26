"""
总控 Orchestrator
协调整个第一性原理 Agent 生成执行流程
"""
from typing import List, Callable, Dict, Optional
import json

from types_def import (
    Goal,
    FundamentalTruth,
    SubTask,
    RefinementDecision,
    RefinementType,
    ExecutionPlan,
    TaskResult,
    FinalResult
)
from truth_deriver import TruthDeriver
from task_breaker import TaskBreaker
from refiner import Refiner
from dependency_sorter import DependencySorter
from validator import Validator
from executor import OpenClawExecutor
from integrator import Integrator


class PrinciplesOrchestrator:
    """
    基于第一性原理的总控 Orchestrator
    """

    def __init__(
        self,
        llm_call: Callable[[str], str],
        max_iterations: int = 5,
        session_key: str = None
    ):
        """
        初始化
        :param llm_call: LLM 调用函数，输入 prompt，返回文本
        :param max_iterations: 最大迭代精炼次数
        :param session_key: OpenClaw 会话 key
        """
        self.llm_call = llm_call
        self.max_iterations = max_iterations
        self.truth_deriver = TruthDeriver()
        self.task_breaker = TaskBreaker()
        self.refiner = Refiner()
        self.dependency_sorter = DependencySorter()
        self.validator = Validator()
        self.executor = OpenClawExecutor(session_key)
        self.integrator = Integrator()

    def clarify_goal(self, original_prompt: str) -> Goal:
        """澄清目标，提取约束和成功标准"""
        prompt = f"""请帮我澄清这个目标，提取出清晰的目标描述、约束条件和可量化的成功标准。

原始请求: {original_prompt}

请以 JSON 格式返回：
{{
  "clarified_objective": "清晰简明的目标描述",
  "constraints": ["约束条件1", "约束条件2"],
  "success_criteria": ["成功标准1", "成功标准2"]
}}
"""
        response = self.llm_call(prompt)
        cleaned = self._extract_json(response)
        data = json.loads(cleaned)

        return Goal(
            original_prompt=original_prompt,
            clarified_objective=data.get("clarified_objective", original_prompt),
            constraints=data.get("constraints", []),
            success_criteria=data.get("success_criteria", [])
        )

    def run(self, original_prompt: str) -> FinalResult:
        """
        执行完整的 Principles 流程
        1. 澄清目标
        2. 推导基础事实（迭代精炼）
        3. 拆解原子任务（迭代精炼）
        4. 依赖排序
        5. 按批次执行并验证
        6. 整合结果
        7. 全局验证
        """

        # Step 1: 澄清目标
        goal = self.clarify_goal(original_prompt)
        iteration_count = 0
        truths: List[FundamentalTruth] = []
        subtasks: List[SubTask] = []
        relationships = ""

        # Step 2-4: 迭代精炼直到满足要求
        truths, subtasks, iteration_count = self._iterate_refine(goal)

        # Step 5: 依赖拓扑排序
        plan = self.dependency_sorter.sort(subtasks)
        if plan.has_circular_dependency:
            raise ValueError(f"依赖排序失败: {plan.circular_dependency_details}")

        # Step 6: 按批次执行并验证
        task_results: List[TaskResult] = []
        previous_results: Dict[str, TaskResult] = {}

        for batch in plan.parallel_batches:
            # 执行批次
            batch_results = self.executor.execute_parallel_batch(
                batch, goal, previous_results, self.llm_call
            )

            # 验证每个结果
            for task, result in zip(batch, batch_results):
                if result.success:
                    # 验证输出
                    passed, failed, reason = self.validator.validate_task(task, result.output)
                    result.validation_passed = passed
                    if not passed:
                        # 这里可以重试，简化处理先记录
                        result.error_message = f"验证失败: {reason}; 不通过标准: {failed}"

                task_results.append(result)
                previous_results[task.id] = result

        # Step 7: 整合结果
        integration = self.integrator.integrate(
            goal, truths, subtasks, task_results, iteration_count
        )

        # Step 8: 全局验证
        global_passed, global_reason = self.validator.validate_global(
            goal, task_results, integration["synthesized_output"]
        )

        return FinalResult(
            goal=goal,
            truths=truths,
            tasks=subtasks,
            task_results=task_results,
            synthesized_output=integration.get("synthesized_output", ""),
            global_validation_passed=global_passed,
            iteration_count=iteration_count,
            report=integration.get("report", "")
        )

    def _iterate_refine(
        self,
        goal: Goal
    ) -> tuple[List[FundamentalTruth], List[SubTask], int]:
        """迭代精炼循环"""
        iteration_count = 0
        truths: List[FundamentalTruth] = []
        subtasks: List[SubTask] = []
        relationships = ""

        # 第一步：推导基础事实
        prompt = self.truth_deriver._build_prompt(goal)
        response = self.llm_call(prompt)
        truths, relationships = self.truth_deriver._parse_response(response)

        while iteration_count < self.max_iterations:
            iteration_count += 1

            # 拆解任务
            prompt = self.task_breaker._build_prompt(goal, truths)
            response = self.llm_call(prompt)
            subtasks = self.task_breaker._parse_response(response)

            # 决策是否需要精炼
            prompt = self.refiner._build_prompt(goal, truths, subtasks)
            response = self.llm_call(prompt)
            decision = self.refiner._parse_response(response)

            if decision.decision == RefinementType.FINALIZE:
                break
            elif decision.decision == RefinementType.REFINE_TRUTHS:
                # 重新推导事实
                prompt = self.truth_deriver._build_prompt_with_feedback(
                    goal, decision.feedback
                )
                response = self.llm_call(prompt)
                truths, relationships = self.truth_deriver._parse_response(response)
            elif decision.decision == RefinementType.REFINE_SUBTASKS:
                # 保持事实不变，重新拆解任务
                continue

        return truths, subtasks, iteration_count

    def _extract_json(self, text: str) -> str:
        """从文本提取JSON，处理 markdown 代码块"""
        import re
        
        # 移除 markdown 代码块标记
        text = re.sub(r'```(?:json)?\n', '', text)
        text = re.sub(r'\n```', '', text)
        
        # 找到第一个 { 和最后一个 }
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= 0:
            return text[start:end+1]
        
        # 如果找不到完整对象，尝试找数组
        start = text.find("[")
        end = text.rfind("]")
        if start >= 0 and end >= 0:
            return text[start:end+1]
            
        return text

    def generate_report(self, result: FinalResult) -> str:
        """生成可读的执行报告"""
        report = []
        report.append("# Principles 执行报告\n")
        report.append(f"## 原始目标\n{result.goal.original_prompt}\n")
        report.append(f"## 澄清目标\n{result.goal.clarified_objective}\n")

        if result.goal.constraints:
            report.append("## 约束条件\n")
            for c in result.goal.constraints:
                report.append(f"- {c}")
            report.append("")

        report.append(f"## 基础事实 ({len(result.truths)} 项)\n")
        for t in result.truths:
            report.append(f"- **{t.id}**: {t.content}")
        report.append("")

        report.append(f"## 原子任务 ({len(result.tasks)} 项)\n")
        for t in result.tasks:
            status = "✅" if all(
                r.task_id == t.id and r.success and r.validation_passed
                for r in result.task_results
            ) else "❌"
            deps = f" (依赖: {', '.join(t.dependencies)})" if t.dependencies else ""
            report.append(f"{status} **{t.id}**: {t.title}{deps}")
        report.append("")

        report.append(f"## 迭代次数: {result.iteration_count}\n")
        report.append(f"## 全局验证: {'✅ 通过' if result.global_validation_passed else '❌ 不通过'}\n")

        if result.report:
            report.append("---\n")
            report.append(result.report)

        report.append("\n---\n## 最终输出\n")
        report.append(str(result.synthesized_output))

        return "\n".join(report)
