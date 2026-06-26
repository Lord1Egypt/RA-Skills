"""
结果整合
整合所有子任务结果，生成最终输出
"""
from typing import List, Any
import json

from types_def import Goal, FundamentalTruth, SubTask, TaskResult, FinalResult


class Integrator:
    """结果整合器"""

    SYSTEM_PROMPT = """你是一个**结果整合专家**，负责将所有原子子任务的结果整合为一个连贯、完整的最终输出。

## 整合规则：
1. **完整保留所有有效结果** —— 不要遗漏任何子任务的产出
2. **保持逻辑连贯** —— 按照依赖关系和执行顺序组织结果
3. **消除重复** —— 合并重复内容，保持简洁
4. **满足原始目标** —— 最终输出必须完全满足原始目标的要求
5. **结构清晰** —— 使用适当的标题、分段、列表组织内容

## 输出要求：
请生成一个完整的最终结果，包括：
1. 对原始目标的简要回顾
2. 核心基础事实总结
3. 整合后的主体内容
4. 结论和下一步建议

## 输出格式：
{
  "synthesized_output": "整合后的完整最终结果（markdown格式）",
  "report": "完整的执行过程报告，包括迭代次数、精炼过程、任务完成情况"
}
"""

    def __init__(self):
        pass

    def integrate(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        tasks: List[SubTask],
        task_results: List[TaskResult],
        iteration_count: int
    ) -> Any:
        """整合所有结果"""
        prompt = self._build_prompt(goal, truths, tasks, task_results, iteration_count)
        return self._parse_response(prompt)

    def _build_prompt(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        tasks: List[SubTask],
        task_results: List[TaskResult],
        iteration_count: int
    ) -> str:
        truths_text = "\n".join(
            f"- {t.id}: {t.content}" for t in truths
        )

        results_text = ""
        for task, result in zip(tasks, task_results):
            results_text += f"\n### {task.id}: {task.title}\n"
            results_text += f"状态: {'✅ 通过' if result.success and result.validation_passed else '❌ 失败'}\n"
            output_str = str(result.output)
            if len(output_str) > 1000:
                output_str = output_str[:1000] + "\n... (已截断)"
            results_text += f"输出:\n{output_str}\n"

        return f"""原始目标:
{goal.clarified_objective}

约束条件:
{chr(10).join(f'- {c}' for c in goal.constraints)}

成功标准:
{chr(10).join(f'- {c}' for c in goal.success_criteria)}

基础事实:
{truths_text}

各任务结果:
{results_text}

迭代次数: {iteration_count}

请整合所有结果，生成最终输出。
"""

    def _parse_response(self, response_text: str) -> dict:
        cleaned = self._extract_json(response_text)
        data = json.loads(cleaned)
        return {
            "synthesized_output": data.get("synthesized_output", ""),
            "report": data.get("report", "")
        }

    def _extract_json(self, text: str) -> str:
        """从文本提取JSON，处理 markdown 代码块"""
        import re
        
        # 移除 markdown 代码块标记
        text = re.sub(r'```(?:json)?\n', '', text)
        text = re.sub(r'\n```', '', text)
        
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end >= 0:
            return text[start:end+1]
        return text
