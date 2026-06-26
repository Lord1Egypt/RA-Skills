"""
迭代精炼决策
判断当前的基础事实和子任务是否满足要求，决定是否需要进一步精炼
"""
import json
from typing import List

from types_def import Goal, FundamentalTruth, SubTask, RefinementDecision, RefinementType


class Refiner:
    """迭代精炼决策者"""

    SYSTEM_PROMPT = """你是一个**质量检查员**，负责检查第一性原理拆解得到的基础事实和原子子任务是否满足要求，并决定下一步行动。

## 检查标准：

### 对基础事实的检查：
1. ✅ **真正基础** —— 每个事实都是不可分割的，不是推导出来的
2. ✅ **完整覆盖** —— 覆盖了实现目标所需的所有核心假设
3. ✅ **没有混入步骤** —— 只包含"是什么"，不包含实现步骤

### 对子任务的检查：
1. ✅ **原子性** —— 每个子任务都不可再分
2. ✅ **可行性** —— 每个子任务都在 LLM Agent 能力范围内
3. ✅ **可验证性** —— 每个子任务都有明确的验收标准
4. ✅ **单一职责** —— 一个子任务只做一件事
5. ✅ **无重叠** —— 功能不重叠
6. ✅ **依赖正确** —— 依赖关系正确，没有循环依赖

## 决策选项：
1. **finalize** —— 全部满足要求，可以进入下一步执行
2. **refine_subtasks** —— 子任务不满足要求，需要重新拆解（基础事实没问题）
3. **refine_truths** —— 基础事实不满足要求，需要重新推导

## 输出格式：
必须返回严格的 JSON，格式如下：
{
  "decision": "finalize" | "refine_subtasks" | "refine_truths",
  "reason": "为什么做出这个决策，具体哪里不满足",
  "feedback": "给下一轮拆解/推导的具体反馈建议"
}
"""

    def __init__(self):
        pass

    def decide(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        subtasks: List[SubTask]
    ) -> RefinementDecision:
        """检查当前结果，决定是否需要精炼"""
        prompt = self._build_prompt(goal, truths, subtasks)
        return self._parse_response(prompt)

    def _build_prompt(
        self,
        goal: Goal,
        truths: List[FundamentalTruth],
        subtasks: List[SubTask]
    ) -> str:
        truths_text = "\n".join(
            f"- {t.id}: {t.content}" for t in truths
        )

        subtasks_text = "\n".join(
            f"- {t.id}: {t.title} | 原子: {t.is_atomic} | 可行: {t.is_feasible} | 依赖: {', '.join(t.dependencies)}"
            for t in subtasks
        )

        return f"""目标: {goal.clarified_objective}

当前推导得到的基础事实：
{truths_text}

当前拆解得到的子任务：
{subtasks_text}

请检查是否满足所有标准，然后给出你的决策。
"""

    def _parse_response(self, response_text: str) -> RefinementDecision:
        """解析LLM响应"""
        cleaned = self._extract_json(response_text)
        data = json.loads(cleaned)

        decision_str = data.get("decision", "refine_subtasks")
        decision_map = {
            "finalize": RefinementType.FINALIZE,
            "refine_subtasks": RefinementType.REFINE_SUBTASKS,
            "refine_truths": RefinementType.REFINE_TRUTHS,
        }
        decision_type = decision_map.get(decision_str, RefinementType.REFINE_SUBTASKS)

        return RefinementDecision(
            decision=decision_type,
            reason=data.get("reason", ""),
            feedback=data.get("feedback", "")
        )

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
