"""
right_brain/logic_parser.py
============================

Neuro-Agent 右脑区 - 逻辑解析器 (Real Version)
负责：拆解复杂任务，制定执行方案

Phase 2 升级：从 Mock（简单拆分）→ Real（LLM 深度推理）
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from core.llm_client import LLMClient


@dataclass
class TaskStep:
    """任务步骤"""
    step_number: int
    description: str
    action: str
    estimated_time: str  # 预估时间
    dependencies: List[int]  # 依赖的步骤
    tools_needed: List[str]  # 需要的工具


@dataclass
class LogicOutput:
    """逻辑解析输出"""
    task_complexity: float  # 复杂度 0-1
    estimated_total_time: str
    steps: List[TaskStep]
    prerequisites: List[str]  # 前置条件
    potential_issues: List[str]  # 潜在问题
    success_criteria: List[str]  # 成功标准
    
    # Real 版本新增
    llm_reasoning: Optional[str] = None
    alternative_approaches: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class LogicParser:
    """
    逻辑解析器 (Real Version)
    
    Phase 2 升级：
    - LLM 深度分析任务结构
    - 识别依赖关系、潜在问题
    - 提供多种方案选择
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
    
    def parse(
        self,
        task_description: str,
        user_context: Optional[Dict] = None,
        constraints: Optional[List[str]] = None
    ) -> LogicOutput:
        """
        解析任务，制定方案
        
        Args:
            task_description: 任务描述
            user_context: 用户上下文（技能水平、时间限制等）
            constraints: 约束条件
        
        Returns:
            LogicOutput: 解析结果
        """
        llm_result = self._parse_with_llm(task_description, user_context, constraints)
        
        if llm_result:
            return llm_result
        
        return self._fallback_parse(task_description)
    
    def _parse_with_llm(
        self,
        task_description: str,
        user_context: Optional[Dict],
        constraints: Optional[List[str]]
    ) -> Optional[LogicOutput]:
        """使用 LLM 深度解析任务"""
        
        system_prompt = """你是 Neuro-Agent 的右脑区——逻辑解析器。
你的任务是把用户的请求拆解成可执行的步骤，像资深项目经理一样思考。

【分析维度】
1. 任务复杂度：简单/中等/复杂
2. 执行步骤：具体、可操作的步骤
3. 依赖关系：哪些步骤必须先做
4. 所需工具：完成这个任务需要什么
5. 潜在问题：可能遇到什么坑
6. 成功标准：怎么算完成了

输出 JSON 格式：
{
  "complexity": 0.0-1.0,
  "estimated_time": "预估总时间",
  "steps": [
    {
      "number": 1,
      "description": "步骤描述",
      "action": "具体动作",
      "time": "预估时间",
      "dependencies": [依赖的步骤编号],
      "tools": ["需要的工具"]
    }
  ],
  "prerequisites": ["前置条件"],
  "potential_issues": ["潜在问题"],
  "success_criteria": ["成功标准"],
  "alternative_approaches": ["替代方案"],
  "reasoning": "你的分析思路"
}"""

        ctx = f"\n用户背景：{user_context}" if user_context else ""
        cons = f"\n约束条件：{constraints}" if constraints else ""
        
        user_prompt = f"任务：{task_description}{ctx}{cons}\n\n请拆解任务，输出 JSON："
        
        try:
            response = self.llm.quick_chat(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.4,
                max_tokens=800
            )
            
            if response:
                import json
                json_str = response
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0]
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0]
                
                data = json.loads(json_str.strip())
                
                steps = []
                for s in data.get("steps", []):
                    steps.append(TaskStep(
                        step_number=s.get("number", 1),
                        description=s.get("description", ""),
                        action=s.get("action", ""),
                        estimated_time=s.get("time", "未知"),
                        dependencies=s.get("dependencies", []),
                        tools_needed=s.get("tools", [])
                    ))
                
                return LogicOutput(
                    task_complexity=data.get("complexity", 0.5),
                    estimated_total_time=data.get("estimated_time", "未知"),
                    steps=steps,
                    prerequisites=data.get("prerequisites", []),
                    potential_issues=data.get("potential_issues", []),
                    success_criteria=data.get("success_criteria", []),
                    llm_reasoning=data.get("reasoning", ""),
                    alternative_approaches=data.get("alternative_approaches", [])
                )
        except Exception as e:
            print(f"[LogicParser] LLM 失败: {e}")
        
        return None
    
    def _fallback_parse(self, task_description: str) -> LogicOutput:
        """LLM 失败时的简单 fallback"""
        return LogicOutput(
            task_complexity=0.5,
            estimated_total_time="未知",
            steps=[
                TaskStep(
                    step_number=1,
                    description="分析任务",
                    action="理解需求",
                    estimated_time="5分钟",
                    dependencies=[],
                    tools_needed=[]
                ),
                TaskStep(
                    step_number=2,
                    description="执行任务",
                    action="完成工作",
                    estimated_time="视情况而定",
                    dependencies=[1],
                    tools_needed=[]
                )
            ],
            prerequisites=[],
            potential_issues=["可能需要更多信息"],
            success_criteria=["任务完成"],
            llm_reasoning="fallback"
        )


# ============ 单例 ============
_parser_instance: Optional[LogicParser] = None

def get_instance(llm_client: Optional[LLMClient] = None) -> LogicParser:
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = LogicParser(llm_client)
    return _parser_instance


def parse_task(
    task_description: str,
    user_context: Optional[Dict] = None,
    constraints: Optional[List[str]] = None
) -> LogicOutput:
    """快捷函数"""
    return get_instance().parse(task_description, user_context, constraints)


# ============ 测试 ============
if __name__ == "__main__":
    parser = LogicParser()
    
    test_tasks = [
        "帮我做一个电商数据分析报告",
        "我想学 Python，从零开始",
        "帮我整理桌面文件",
        "写一份求职简历",
    ]
    
    print("=== 逻辑解析测试 (Real Version) ===\n")
    for task in test_tasks:
        result = parser.parse(task)
        print(f"任务: {task}")
        print(f"  复杂度: {result.task_complexity}")
        print(f"  预估时间: {result.estimated_total_time}")
        print(f"  步骤数: {len(result.steps)}")
        for step in result.steps[:3]:  # 只显示前3步
            print(f"    {step.step_number}. {step.description} ({step.estimated_time})")
        if result.potential_issues:
            print(f"  潜在问题: {result.potential_issues[0]}")
        print()
