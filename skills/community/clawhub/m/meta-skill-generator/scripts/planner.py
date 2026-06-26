"""
任务规划器 - 决定使用现有技能还是生成新技能
"""

import json
import os
from typing import Dict, Optional, Literal
from dataclasses import dataclass


@dataclass
class PlanResult:
    """规划结果"""
    action: Literal["use_skill", "generate_skill", "composite"]
    skill_id: Optional[str] = None
    task_description: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: float = 0.0
    composite_plan: Optional[list] = None


class TaskPlanner:
    """任务路由器 - 决定如何处理用户任务"""
    
    SYSTEM_PROMPT = """你是一个技能路由器。根据用户任务，决定最佳处理方式。

决策类型：
1. use_skill - 复用现有技能
2. generate_skill - 生成全新技能
3. composite - 组合多个现有技能

输出格式（JSON）：
{
    "action": "use_skill" | "generate_skill" | "composite",
    "skill_id": "xxx"（use_skill 时必需）,
    "task_description": "xxx"（generate_skill 时必需）,
    "composite_plan": [{"skill_id": "xxx", "inputs": {}}]（composite 时必需）,
    "reasoning": "为什么做出这个决定",
    "confidence": 0.85
}

决策规则：
- 如果存在相似度 > 0.8 的现有技能，优先复用
- 如果任务可以由 2-3 个现有技能组合完成，使用 composite
- 只有当任务完全超出现有技能范围时才生成新技能
"""
    
    def __init__(self, library, llm_client=None):
        """
        初始化规划器
        
        Args:
            library: SkillLibrary 实例
            llm_client: LLM 客户端（可选）
        """
        self.library = library
        self.llm_client = llm_client
        self.similarity_threshold = 0.8
    
    def plan(self, task: str) -> PlanResult:
        """
        规划任务执行
        
        Args:
            task: 用户任务描述
            
        Returns:
            PlanResult 执行计划
        """
        # 1. 检索现有技能
        search_results = self.library.search(task, top_k=5)
        
        if not search_results['ids'] or not search_results['ids'][0]:
            # 没有找到任何技能，生成新技能
            return PlanResult(
                action="generate_skill",
                task_description=task,
                reasoning="未找到相关技能，需要生成新技能",
                confidence=1.0
            )
        
        # 2. 分析检索结果
        best_match = search_results['ids'][0][0]
        best_distance = search_results['distances'][0][0]
        best_similarity = 1 - best_distance
        
        # 3. 判断是否满足需求
        if best_similarity >= self.similarity_threshold:
            # 找到足够相似的技能
            return PlanResult(
                action="use_skill",
                skill_id=best_match,
                reasoning=f"找到相似技能 {best_match}（相似度: {best_similarity:.2f}）",
                confidence=best_similarity
            )
        
        # 4. 检查是否需要组合
        if len(search_results['ids'][0]) >= 2:
            second_similarity = 1 - search_results['distances'][0][1]
            
            # 如果前两个技能组合能覆盖任务
            if best_similarity + second_similarity >= 1.4:
                return PlanResult(
                    action="composite",
                    composite_plan=[
                        {"skill_id": search_results['ids'][0][0], "inputs": {}},
                        {"skill_id": search_results['ids'][0][1], "inputs": {}}
                    ],
                    reasoning=f"组合技能 {search_results['ids'][0][0]} 和 {search_results['ids'][0][1]} 可完成任务",
                    confidence=(best_similarity + second_similarity) / 2
                )
        
        # 5. 需要生成新技能
        return PlanResult(
            action="generate_skill",
            task_description=task,
            reasoning=f"现有技能相似度不足（最高: {best_similarity:.2f}），需要生成新技能",
            confidence=1 - best_similarity
        )
    
    def plan_with_llm(self, task: str) -> PlanResult:
        """
        使用 LLM 辅助规划（更智能）
        
        Args:
            task: 用户任务描述
            
        Returns:
            PlanResult 执行计划
        """
        if not self.llm_client:
            return self.plan(task)
        
        # 先做本地检索
        search_results = self.library.search(task, top_k=5)
        
        # 构建上下文
        context = f"用户任务：{task}\n\n"
        context += "已找到的相关技能：\n"
        
        if search_results['ids'] and search_results['ids'][0]:
            for i, (skill_id, dist) in enumerate(zip(
                search_results['ids'][0], 
                search_results['distances'][0]
            )):
                similarity = 1 - dist
                context += f"- {i+1}. {skill_id}（相似度: {similarity:.2f}）\n"
        
        # 调用 LLM
        response = self.llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": context}
            ],
            response_format={"type": "json_object"}
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return PlanResult(
                action=result.get("action", "generate_skill"),
                skill_id=result.get("skill_id"),
                task_description=result.get("task_description"),
                composite_plan=result.get("composite_plan"),
                reasoning=result.get("reasoning", ""),
                confidence=result.get("confidence", 0.5)
            )
        except:
            # LLM 返回格式错误，回退到本地规划
            return self.plan(task)
    
    def explain_plan(self, plan: PlanResult) -> str:
        """生成计划说明"""
        if plan.action == "use_skill":
            return f"""
🎯 计划：使用现有技能
📦 技能 ID: {plan.skill_id}
📊 置信度: {plan.confidence:.2%}
💡 理由: {plan.reasoning}
"""
        elif plan.action == "generate_skill":
            return f"""
🎯 计划：生成新技能
📝 任务: {plan.task_description}
💡 理由: {plan.reasoning}
"""
        elif plan.action == "composite":
            skills = [s['skill_id'] for s in plan.composite_plan]
            return f"""
🎯 计划：组合技能
🔗 技能链: {' → '.join(skills)}
📊 置信度: {plan.confidence:.2%}
💡 理由: {plan.reasoning}
"""
        
        return "❓ 未知行动计划"


def create_planner(library, llm_client=None) -> TaskPlanner:
    """创建规划器实例"""
    return TaskPlanner(library, llm_client)


if __name__ == "__main__":
    # 测试
    from embed_skill import SkillLibrary
    
    library = SkillLibrary()
    planner = TaskPlanner(library)
    
    # 示例任务
    test_tasks = [
        "发送一封邮件给老板",
        "查询今天天气",
        "帮我写一个 Python 脚本处理 CSV 文件",
        "创建一个自动化工作流"
    ]
    
    for task in test_tasks:
        print(f"\n{'='*50}")
        print(f"📌 任务: {task}")
        print("="*50)
        
        plan = planner.plan(task)
        print(planner.explain_plan(plan))
