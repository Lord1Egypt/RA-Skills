"""
原子任务拆解
将目标基于基础事实拆解为最小可执行、可验证的原子子任务
"""
from typing import List
import json

from types_def import Goal, FundamentalTruth, SubTask


class TaskBreaker:
    """原子任务拆解器"""

    SYSTEM_PROMPT = """你是一个**任务拆解专家**，擅长基于第一性原理的基础事实，将复杂目标拆解为最小的、可执行、可验证的原子子任务。

## 核心规则：
1. **原子性** —— 每个子任务必须不可再分，如果还能拆分，就继续拆分
2. **可验证性** —— 每个子任务必须有明确的验收标准，能判断是否完成
3. **可行性** —— 每个子任务必须在单个 LLM Agent 的能力范围内（文本处理、分析、生成等）
4. **单一职责** —— 一个子任务只做一件事
5. **无重叠** —— 子任务之间功能不重叠
6. **依赖清晰** —— 明确标注每个子任务依赖哪些其他子任务的输出

## 验收标准要求：
每个子任务必须定义至少一条清晰可量化的验收标准，例如：
- "输出必须符合指定 JSON 格式"
- "覆盖所有 5 个核心要点"
- "通过语法检查，无编译错误"
- "包含完整的 API 文档"

## 输出格式：
必须返回严格的 JSON，格式如下：
{
  "subtasks": [
    {
      "id": "task-1",
      "title": "子任务标题",
      "description": "子任务详细描述",
      "acceptance_criteria": [
        "验收标准 1",
        "验收标准 2"
      ],
      "dependencies": ["依赖的任务ID，如 task-0"],
      "is_feasible": true,
      "is_atomic": true
    }
  ]
}

记住：**极致拆分** —— 哪怕一个任务只需要一句话，只要它是独立的，就应该拆出来。
"""

    def __init__(self):
        pass

    def decompose(self, goal: Goal, truths: List[FundamentalTruth]) -> List[SubTask]:
        """基于基础事实拆解目标为原子子任务"""
        prompt = self._build_prompt(goal, truths)
        # 实际 LLM 调用在上层 orchestrator
        return self._parse_response(prompt)

    def decompose_with_feedback(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        feedback: str
    ) -> List[SubTask]:
        """根据反馈重新拆解任务"""
        prompt = self._build_prompt_with_feedback(goal, truths, feedback)
        return self._parse_response(prompt)

    def _build_prompt(self, goal: Goal, truths: List[FundamentalTruth]) -> str:
        truths_text = "\n".join(
            f"{t.id}: {t.content} - {t.description}"
            for t in truths
        )

        return f"""目标:
澄清后的目标: {goal.clarified_objective}
原始描述: {goal.original_prompt}

约束条件:
{chr(10).join(f'- {c}' for c in goal.constraints)}

基础事实/公理:
{truths_text}

请基于上述基础事实，将目标拆解为最小的、可执行、可验证的原子子任务。
"""

    def _build_prompt_with_feedback(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        feedback: str
    ) -> str:
        truths_text = "\n".join(
            f"{t.id}: {t.content} - {t.description}"
            for t in truths
        )

        return f"""目标:
澄清后的目标: {goal.clarified_objective}
原始描述: {goal.original_prompt}

约束条件:
{chr(10).join(f'- {c}' for c in goal.constraints)}

基础事实/公理:
{truths_text}

之前的拆解不满足要求，反馈意见是:
---
{feedback}
---

请根据反馈重新拆解，确保:
1. 每个子任务都是真正原子的，不可再分
2. 每个子任务都有明确可验证的验收标准
3. 所有子任务都在 LLM 能力范围内
4. 依赖关系清晰正确
"""

    def _parse_response(self, response_text: str) -> List[SubTask]:
        """解析LLM响应"""
        cleaned = self._extract_json(response_text)
        data = json.loads(cleaned)

        subtasks = []
        for t in data.get("subtasks", []):
            task = SubTask(
                id=t.get("id", f"task-{len(subtasks)+1}"),
                title=t.get("title", ""),
                description=t.get("description", ""),
                acceptance_criteria=t.get("acceptance_criteria", []),
                dependencies=t.get("dependencies", []),
                is_feasible=t.get("is_feasible", True),
                is_atomic=t.get("is_atomic", True)
            )
            subtasks.append(task)

        return subtasks

    def _extract_json(self, text: str) -> str:
        """从文本提取JSON，处理 markdown 代码块"""
        import re
        
        # 移除 markdown 代码块标记
        text = re.sub(r'```(?:json)?\n', '', text)
        text = re.sub(r'\n```', '', text)
        
        start = text.find("[")
        if start < 0:
            start = text.find("{")
        end = text.rfind("]") if text.rfind("]") >= 0 else text.rfind("}")
        if start >= 0 and end >= 0:
            return text[start:end+1]
        return text
