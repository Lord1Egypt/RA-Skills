"""
验证器
验证子任务输出是否满足验收标准
"""
from typing import List, Tuple
import json

from types_def import SubTask, TaskResult


class Validator:
    """任务验证器"""

    SYSTEM_PROMPT = """你是一个**严格的质量检查员**，负责验证子任务输出是否满足所有验收标准。

## 验证规则：
1. **逐条检查验收标准** —— 每个标准都要检查，不能漏掉
2. **严格不妥协** —— 只要有一个重要标准不满足，就不通过
3. **给出明确结论** —— 是通过还是不通过，不模棱两可
4. **说明具体原因** —— 如果不通过，明确指出哪里不满足

## 输出格式：
必须返回严格的 JSON，格式如下：
{
  "validation_passed": true/false,
  "failed_criteria": [
    "不满足的验收标准1",
    "不满足的验收标准2"
  ],
  "reason": "对验证结果的详细说明"
}
"""

    def validate_task(self, task: SubTask, output: any) -> Tuple[bool, List[str], str]:
        """
        验证任务输出是否满足所有验收标准
        返回：(是否通过, 不通过的标准列表, 原因说明)
        """
        prompt = self._build_prompt(task, output)
        # 实际 LLM 调用在上层
        return self._parse_response(prompt)

    def _build_prompt(self, task: SubTask, output: any) -> str:
        criteria = "\n".join(
            f"- {i+1}. {c}" for i, c in enumerate(task.acceptance_criteria)
        )

        output_str = str(output)
        if len(output_str) > 5000:
            output_str = output_str[:5000] + "\n... (输出过长，已截断)"

        return f"""子任务信息：
ID: {task.id}
标题: {task.title}
描述: {task.description}

验收标准：
{criteria}

任务输出：
---
{output_str}
---

请验证输出是否满足所有验收标准。
"""

    def _parse_response(self, response_text: str) -> Tuple[bool, List[str], str]:
        cleaned = self._extract_json(response_text)
        data = json.loads(cleaned)

        passed = data.get("validation_passed", False)
        failed = data.get("failed_criteria", [])
        reason = data.get("reason", "")

        return passed, failed, reason

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

    def validate_global(
        self,
        original_goal,
        all_results: List[TaskResult],
        synthesized_output: any
    ) -> Tuple[bool, str]:
        """全局验证最终结果是否满足原始目标"""
        passed_all = all(r.validation_passed for r in all_results)
        if not passed_all:
            failed_tasks = [r.task_id for r in all_results if not r.validation_passed]
            return False, f"部分子任务验证未通过: {', '.join(failed_tasks)}"

        return True, "所有验证通过"
