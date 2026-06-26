#!/usr/bin/env python3
"""
Intent Translation Skill - Core Engine
Translates vague user intentions into structured AI prompts.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

class IntentTranslator:
    def __init__(self, scenario_path: Optional[str] = None):
        self.scenario_path = scenario_path or Path(__file__).parent.parent / "scenarios"
        self.current_scenario = None
        self.answers = {}
        self.question_index = 0
    
    def load_scenario(self, scenario_name: str) -> Dict:
        """Load a scenario configuration."""
        scenario_file = Path(self.scenario_path) / f"{scenario_name}.json"
        if not scenario_file.exists():
            # Try to auto-detect scenario from user input
            return self._create_dynamic_scenario(scenario_name)
        
        with open(scenario_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_dynamic_scenario(self, user_input: str) -> Dict:
        """Create a dynamic scenario based on user input."""
        # Detect scenario type from keywords
        keywords = {
            "equity": ["股权", "股份", "合伙", "出资", "分红"],
            "career": ["辞职", "创业", "转行", "工作", "职业"],
            "creative": ["设计", "文案", "写作", "风格", "感觉"],
            "communication": ["谈薪", "谈判", "沟通", "矛盾", "拒绝"],
            "learning": ["学习", "不懂", "解释", "教程", "技能"],
            "planning": ["计划", "方案", "整理", "规划", "拆解"]
        }
        
        detected_type = "general"
        for scenario_type, words in keywords.items():
            if any(word in user_input for word in words):
                detected_type = scenario_type
                break
        
        # Return appropriate scenario template
        return self._get_scenario_template(detected_type)
    
    def _get_scenario_template(self, scenario_type: str) -> Dict:
        """Get default scenario template by type."""
        templates = {
            "equity": {
                "name": "股权分配决策",
                "description": "帮助合伙人理清股权分配的核心诉求",
                "questions": [
                    {
                        "id": "fairness_definition",
                        "text": "你说的'公平'是指按出钱分、按干活分、还是大家平均？或者你有别的想法？",
                        "purpose": "明确公平定义"
                    },
                    {
                        "id": "contribution_breakdown", 
                        "text": "每个人具体出什么？钱、时间、技术、资源？",
                        "purpose": "量化各方贡献"
                    },
                    {
                        "id": "biggest_concern",
                        "text": "一年后最担心的场景是什么？有人觉得吃亏？有人中途退出？还是决策僵局？",
                        "purpose": "识别风险点"
                    },
                    {
                        "id": "bottom_line",
                        "text": "有没有绝对不能接受的底线？",
                        "purpose": "确定约束条件"
                    }
                ],
                "prompt_template": """【角色】股权分配与治理顾问

【背景】
{context}

【核心诉求】
{concerns}

【约束条件】
{constraints}

【目标】
给出具体的股权比例建议 + 决策权设计 + 退出机制"""
            },
            "creative": {
                "name": "创意风格翻译",
                "description": "把抽象感觉翻译成具体的AI描述词",
                "questions": [
                    {
                        "id": "vibe_description",
                        "text": "用一个词形容你想要的感觉？（比如：高级感、治愈系、电影感、复古风）",
                        "purpose": "捕捉核心感觉"
                    },
                    {
                        "id": "reference_examples",
                        "text": "有没有具体的例子或参考？某个品牌？某部电影？某张图片？",
                        "purpose": "建立参照系"
                    },
                    {
                        "id": "audience_context",
                        "text": "给谁看的？目标受众是谁？他们看到应该有什么感受？",
                        "purpose": "明确受众"
                    },
                    {
                        "id": "must_avoid",
                        "text": "绝对不要什么感觉？（比如：不要冷冰冰的、不要太花哨）",
                        "purpose": "设定排除项"
                    }
                ],
                "prompt_template": """【角色】{creative_type}专家

【风格要求】
{vibe}

【参考方向】
{references}

【目标受众】
{audience}

【排除项】
{avoid}

【目标】
生成符合上述风格的{output_type}"""
            },
            "career": {
                "name": "职业决策分析",
                "description": "帮助理清职业选择的权衡因素",
                "questions": [
                    {
                        "id": "current_pain",
                        "text": "现在的工作，最让你受不了的一点是什么？",
                        "purpose": "识别痛点"
                    },
                    {
                        "id": "ideal_state",
                        "text": "理想状态下，3年后你希望自己在做什么？",
                        "purpose": "明确目标"
                    },
                    {
                        "id": "risk_tolerance",
                        "text": "如果新选择失败了，最坏情况你能接受吗？",
                        "purpose": "评估风险承受力"
                    },
                    {
                        "id": "support_factors",
                        "text": "做这个决定，有什么支持你？（存款、技能、人脉、家庭）",
                        "purpose": "盘点资源"
                    }
                ],
                "prompt_template": """【角色】职业规划顾问

【现状痛点】
{pain_points}

【理想目标】
{goals}

【风险承受力】
{risk_tolerance}

【支持资源】
{resources}

【目标】
给出职业决策分析 + 行动步骤 + 风险预案"""
            },
            "communication": {
                "name": "沟通策略设计",
                "description": "设计高情商的沟通话术",
                "questions": [
                    {
                        "id": "communication_goal",
                        "text": "你这次沟通，最想达成的具体结果是什么？",
                        "purpose": "明确目标"
                    },
                    {
                        "id": "relationship_context",
                        "text": "和对方是什么关系？这段关系对你重要吗？",
                        "purpose": "评估关系权重"
                    },
                    {
                        "id": "potential_pushback",
                        "text": "对方最可能怎么拒绝或反驳你？",
                        "purpose": "预判阻力"
                    },
                    {
                        "id": "emotional_state",
                        "text": "你现在情绪怎么样？能冷静地谈吗？",
                        "purpose": "评估情绪状态"
                    }
                ],
                "prompt_template": """【角色】高情商沟通顾问

【沟通目标】
{goal}

【关系背景】
{relationship}

【预期阻力】
{pushback}

【情绪状态】
{emotional_state}

【目标】
设计沟通话术 + 时机选择 + 应对方案"""
            },
            "general": {
                "name": "通用意图翻译",
                "description": "通用场景的意图澄清",
                "questions": [
                    {
                        "id": "what_you_want",
                        "text": "你最想要的结果是什么？",
                        "purpose": "明确目标"
                    },
                    {
                        "id": "current_situation",
                        "text": "现在是什么情况？",
                        "purpose": "了解现状"
                    },
                    {
                        "id": "constraints",
                        "text": "有什么限制或必须遵守的条件？",
                        "purpose": "识别约束"
                    },
                    {
                        "id": "concerns",
                        "text": "你最担心什么？",
                        "purpose": "挖掘顾虑"
                    }
                ],
                "prompt_template": """【背景】
{context}

【目标】
{goal}

【约束条件】
{constraints}

【顾虑】
{concerns}"""
            }
        }
        
        return templates.get(scenario_type, templates["general"])
    
    def get_next_question(self) -> Optional[Dict]:
        """Get the next question to ask."""
        if not self.current_scenario:
            return None
        
        questions = self.current_scenario.get("questions", [])
        if self.question_index >= len(questions):
            return None
        
        question = questions[self.question_index]
        self.question_index += 1
        return question
    
    def record_answer(self, question_id: str, answer: str):
        """Record user's answer."""
        self.answers[question_id] = answer
    
    def generate_prompt(self) -> str:
        """Generate the final structured prompt."""
        if not self.current_scenario:
            return "Error: No scenario loaded"
        
        template = self.current_scenario.get("prompt_template", "")
        
        # Build context from answers
        context_parts = []
        concerns = []
        constraints = []
        
        for q in self.current_scenario.get("questions", []):
            qid = q["id"]
            if qid in self.answers:
                purpose = q.get("purpose", "")
                answer = self.answers[qid]
                
                if "顾虑" in purpose or "担心" in purpose or "concern" in qid:
                    concerns.append(f"- {answer}")
                elif "约束" in purpose or "底线" in purpose or "limit" in qid:
                    constraints.append(f"- {answer}")
                else:
                    context_parts.append(f"{purpose}: {answer}")
        
        # Fill template
        prompt = template.format(
            context="\n".join(context_parts) if context_parts else "详见背景",
            concerns="\n".join(concerns) if concerns else "无特殊顾虑",
            constraints="\n".join(constraints) if constraints else "无硬性约束",
            **self.answers
        )
        
        return prompt
    
    def is_complete(self) -> bool:
        """Check if all questions have been answered."""
        if not self.current_scenario:
            return False
        questions = self.current_scenario.get("questions", [])
        return self.question_index >= len(questions)


def main():
    """CLI interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python translate.py <scenario_or_user_input>")
        print("Example: python translate.py equity")
        print("Example: python translate.py '我和朋友合伙开工作室'")
        sys.exit(1)
    
    user_input = sys.argv[1]
    translator = IntentTranslator()
    
    # Load scenario
    scenario = translator.load_scenario(user_input)
    translator.current_scenario = scenario
    
    print(f"\n🎯 场景: {scenario['name']}")
    print(f"📋 {scenario['description']}\n")
    print("=" * 50)
    
    # Ask questions
    while True:
        question = translator.get_next_question()
        if not question:
            break
        
        print(f"\n❓ {question['text']}")
        print(f"   (目的: {question['purpose']})")
        
        # In real usage, this would wait for user input
        # For testing, we simulate
        print("   [等待用户回答...]")
    
    print("\n" + "=" * 50)
    print("✅ 所有问题回答完毕，可以生成结构化Prompt")


if __name__ == "__main__":
    main()
