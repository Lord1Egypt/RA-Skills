#!/usr/bin/env python3
"""
Jev 模拟代码评审 - 原子问题实现
用 LLM 模拟 TypeSafe Jev 的三种原语：Noul / Score / Choice
"""

import json
import re
from typing import Dict, Any, Optional


class JevPrimitive:
    """模拟 Jev 原语基类"""
    
    def __init__(self, client_func=None):
        """
        client_func: 调用 LLM 的函数，签名 (prompt: str) -> str
        默认使用 kimi CLI，可替换为任何 LLM API
        """
        self.client_func = client_func or self._default_client
    
    def _default_client(self, prompt: str) -> str:
        """默认客户端：使用 kimi CLI"""
        import subprocess
        try:
            result = subprocess.run(
                ["kimi", "chat", "--print", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """从 LLM 输出中提取 JSON"""
        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            pass
        
        # 尝试提取 ```json ... ``` 块
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass
        
        # 尝试提取 {...}
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        
        return {"error": "Failed to parse JSON", "raw": text[:500]}
    
    def noul(self, state: str, instructions: str, criteria: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Noul 原语：是/否判断，返回概率 0-1
        
        Args:
            state: 要评估的上下文（代码/diff/描述）
            instructions: 是/否问题
            criteria: 可选，{"true": "...", "false": "..."} 描述 yes/no 的含义
        
        Returns:
            {"answer": 0.85, "type": "noul"}
        """
        criteria_str = ""
        if criteria:
            criteria_str = f"\n\n判断标准：\n- 是（接近1）：{criteria.get('true', '满足条件')}\n- 否（接近0）：{criteria.get('false', '不满足条件')}"
        
        prompt = f"""你是 Jev，一个决策模型。你的任务是回答一个是/否问题，并给出概率。

上下文（代码/变更）：
```
{state[:4000]}
```

问题：{instructions}{criteria_str}

请以 JSON 格式回答，只返回 JSON，不要有其他文字：
```json
{{"answer": 0.0-1.0 之间的概率值}}
```

其中：
- answer 接近 1 表示"是"的概率高
- answer 接近 0 表示"否"的概率高
- answer 在 0.5 附近表示不确定"""
        
        response = self.client_func(prompt)
        result = self._parse_json(response)
        
        # 确保 answer 是 0-1 的数字
        answer = result.get("answer", 0.5)
        try:
            answer = float(answer)
            answer = max(0.0, min(1.0, answer))
        except:
            answer = 0.5
        
        return {
            "type": "noul",
            "question": instructions,
            "answer": answer,
            "raw_response": response[:200]
        }
    
    def score(self, state: str, instructions: str, scale: tuple = (1, 5), 
              criteria: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Score 原语：在有序量表上打分
        
        Args:
            state: 要评估的上下文
            instructions: 打分问题
            scale: (最小值, 最大值)，默认 (1, 5)
            criteria: 可选，各分数级别的描述
        
        Returns:
            {"answer": 4, "confidence": 0.72, "type": "score"}
        """
        min_s, max_s = scale
        scale_str = f"{min_s} 到 {max_s} 分"
        
        criteria_str = ""
        if criteria:
            criteria_lines = [f"- {k}分：{v}" for k, v in sorted(criteria.items())]
            criteria_str = "\n\n评分标准：\n" + "\n".join(criteria_lines)
        
        prompt = f"""你是 Jev，一个决策模型。你的任务是在一个量表上打分，并给出置信度。

上下文（代码/变更）：
```
{state[:4000]}
```

问题：{instructions}

打分范围：{scale_str}{criteria_str}

请以 JSON 格式回答，只返回 JSON，不要有其他文字：
```json
{{"answer": {min_s}-{max_s} 之间的整数, "confidence": 0.0-1.0 之间的置信度}}
```

其中：
- answer 是整数分数
- confidence 是你对这个分数的置信度（0-1）"""
        
        response = self.client_func(prompt)
        result = self._parse_json(response)
        
        # 确保 answer 和 confidence 合法
        answer = result.get("answer", (min_s + max_s) // 2)
        confidence = result.get("confidence", 0.5)
        try:
            answer = int(answer)
            answer = max(min_s, min(max_s, answer))
        except:
            answer = (min_s + max_s) // 2
        try:
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except:
            confidence = 0.5
        
        return {
            "type": "score",
            "question": instructions,
            "answer": answer,
            "scale": scale,
            "confidence": confidence,
            "raw_response": response[:200]
        }
    
    def choice(self, state: str, instructions: str, options: list) -> Dict[str, Any]:
        """
        Choice 原语：从选项中选择一个
        
        Args:
            state: 要评估的上下文
            instructions: 选择问题
            options: 选项列表，如 ["A", "B", "C"] 或 ["方案1", "方案2"]
        
        Returns:
            {"answer": "B", "probabilities": {"A": 0.1, "B": 0.7, "C": 0.2}, "type": "choice"}
        """
        options_str = "\n".join([f"- {opt}" for opt in options])
        
        prompt = f"""你是 Jev，一个决策模型。你的任务是从给定选项中选择一个，并给出各选项的概率。

上下文（代码/变更）：
```
{state[:4000]}
```

问题：{instructions}

选项：
{options_str}

请以 JSON 格式回答，只返回 JSON，不要有其他文字：
```json
{{"answer": "选中的选项", "probabilities": {{"选项1": 0.1, "选项2": 0.7, ...}}}}
```

其中：
- answer 是你选择的选项
- probabilities 是所有选项的概率分布，总和为 1"""
        
        response = self.client_func(prompt)
        result = self._parse_json(response)
        
        answer = result.get("answer", options[0] if options else None)
        probabilities = result.get("probabilities", {})
        
        # 归一化概率
        if probabilities:
            total = sum(probabilities.values())
            if total > 0:
                probabilities = {k: v/total for k, v in probabilities.items()}
        
        return {
            "type": "choice",
            "question": instructions,
            "answer": answer,
            "options": options,
            "probabilities": probabilities,
            "raw_response": response[:200]
        }


# 便捷函数
def noul(state: str, instructions: str, criteria: Optional[Dict] = None, 
         client_func=None) -> Dict[str, Any]:
    """快速调用 Noul 原语"""
    jev = JevPrimitive(client_func)
    return jev.noul(state, instructions, criteria)


def score(state: str, instructions: str, scale: tuple = (1, 5),
          criteria: Optional[Dict] = None, client_func=None) -> Dict[str, Any]:
    """快速调用 Score 原语"""
    jev = JevPrimitive(client_func)
    return jev.score(state, instructions, scale, criteria)


def choice(state: str, instructions: str, options: list,
           client_func=None) -> Dict[str, Any]:
    """快速调用 Choice 原语"""
    jev = JevPrimitive(client_func)
    return jev.choice(state, instructions, options)
