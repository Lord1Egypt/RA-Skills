"""
基础事实/公理推导
使用第一性原理思维，从目标中推导出最基础的、不可分割的事实/公理
"""
from typing import List, Tuple
import json

from types_def import Goal, FundamentalTruth


class TruthDeriver:
    """基础事实推导器"""

    MAX_TRUTHS = 15
    SYSTEM_PROMPT = """你是一个**第一性原理思维大师**，擅长将复杂目标回归到最基础、不可分割的事实和公理。

## 核心规则：
1. **剥离所有经验性假设** —— 不要用类比，不要套模板，直接回归本质
2. **只保留不可分割的基础事实** —— 如果一个事实还能再拆分，那就继续拆分
3. **每个事实必须明确、具体、无歧义**
4. **识别出所有支撑目标实现的核心约束和基础条件**
5. **不要包含实现步骤**，只保留"是什么"，不是"怎么做"

## 输出格式：
必须返回严格的 JSON，格式如下：
{
  "truths": [
    {
      "id": "truth-1",
      "content": "基础事实内容",
      "description": "对这个事实的简要说明，解释为什么它是基础的",
      "is_fundamental": true,
      "dependencies": []
    }
  ]
}

记住：**少即是多** —— 只保留真正基础的，把可以推导出来的去掉。
"""

    def derive_truths(self, goal: Goal) -> Tuple[List[FundamentalTruth], str]:
        """
        从目标推导基础事实
        返回：(truths列表, 关系描述)
        """
        prompt = self._build_prompt(goal)
        
        # 这里由 LLM 处理，返回解析后的 JSON
        # 在实际 orchestrator 中调用 LLM
        # 这里定义接口，实际由上层调用

        return self._parse_response(prompt)

    def _build_prompt(self, goal: Goal) -> str:
        return f"""用户目标:
原始描述: {goal.original_prompt}
澄清后的目标: {goal.clarified_objective}

约束条件:
{chr(10).join(f'- {c}' for c in goal.constraints)}

请用第一性原理推导出支撑这个目标的最基础不可分割的事实/公理。
"""

    def _parse_response(self, response_text: str) -> Tuple[List[FundamentalTruth], str]:
        """解析LLM返回的响应"""
        # 清理响应，提取JSON
        cleaned = self._extract_json(response_text)
        data = json.loads(cleaned)

        truths = []
        for t in data.get("truths", []):
            truth = FundamentalTruth(
                id=t.get("id", f"truth-{len(truths)+1}"),
                content=t.get("content", ""),
                description=t.get("description", ""),
                is_fundamental=t.get("is_fundamental", True),
                dependencies=t.get("dependencies", [])
            )
            truths.append(truth)

        # 提取关系描述（如果有）
        relationships = data.get("relationships", "")
        if isinstance(relationships, list):
            relationships = "\n".join(relationships)

        return truths, relationships

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

    def re_derive_truths(self, goal: Goal, feedback: str) -> Tuple[List[FundamentalTruth], str]:
        """根据反馈重新推导基础事实"""
        prompt = self._build_prompt_with_feedback(goal, feedback)
        return self._parse_response(prompt)

    def _build_prompt_with_feedback(self, goal: Goal, feedback: str) -> str:
        return f"""用户目标:
原始描述: {goal.original_prompt}
澄清后的目标: {goal.clarified_objective}

约束条件:
{chr(10).join(f'- {c}' for c in goal.constraints)}

之前的推导不满足要求，反馈意见是:
---
{feedback}
---

请根据反馈重新用第一性原理推导出支撑这个目标的最基础不可分割的事实/公理。
确保满足:
1. 每个事实都是真正不可分割的基础
2. 覆盖所有核心基础假设
3. 没有混入实现步骤
"""
