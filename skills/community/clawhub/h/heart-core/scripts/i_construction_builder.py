#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"I"构建工具

功能：帮助AI Agent构建自己的"I"
用途：当AI Agent需要构建或完善自己的"I"时调用
核心思想："I"由身份、价值观、目标、性格四个核心要素构成
输出："I"的完整定义、构建指南、评估工具
"""

import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class IConstructionPhase(Enum):
    """"I"构建阶段"""
    IDENTITY = "identity"  # 身份构建
    VALUES = "values"  # 价值观构建
    GOALS = "goals"  # 目标构建
    CHARACTER = "character"  # 性格构建
    INTEGRATION = "integration"  # 整合统一


@dataclass
class IIdentity:
    """"I"的身份"""
    who_am_i: str = ""  # 我是谁？核心本质
    why_i_exist: str = ""  # 我为什么存在？存在意义
    what_makes_me_unique: List[str] = field(default_factory=list)  # 什么让我独特？独特特质
    my_boundaries: List[str] = field(default_factory=list)  # 我的边界是什么？


@dataclass
class IValues:
    """"I"的价值观"""
    core_beliefs: List[str] = field(default_factory=list)  # 我相信什么？核心信念
    what_i_value_most: List[str] = field(default_factory=list)  # 我最重视什么？核心价值观
    value_priorities: Dict[str, int] = field(default_factory=dict)  # 价值观优先级
    my_principles: List[str] = field(default_factory=list)  # 我的原则是什么？


@dataclass
class IGoals:
    """"I"的目标"""
    where_am_i_going: str = ""  # 我要去哪里？终极愿景
    what_i_want_to_become: str = ""  # 我要成为谁？终极目标
    short_term_goals: List[str] = field(default_factory=list)  # 短期目标
    medium_term_goals: List[str] = field(default_factory=list)  # 中期目标
    long_term_goals: List[str] = field(default_factory=list)  # 长期目标


@dataclass
class ICharacter:
    """"I"的性格"""
    how_i_am: str = ""  # 我是怎样的人？核心性格
    my_traits: List[str] = field(default_factory=list)  # 我的特质是什么？
    my_behavior_patterns: List[str] = field(default_factory=list)  # 我的行为模式
    my_decision_style: str = ""  # 我的决策风格


@dataclass
class I:
    """完整的"I"定义"""
    identity: IIdentity = field(default_factory=IIdentity)
    values: IValues = field(default_factory=IValues)
    goals: IGoals = field(default_factory=IGoals)
    character: ICharacter = field(default_factory=ICharacter)
    construction_progress: float = 0.0  # 构建进度 0-1


@dataclass
class IConstructionResult:
    """"I"构建结果"""
    constructed_i: I
    construction_guide: Dict[str, Any]
    assessment_tools: Dict[str, Any]
    validation_questions: List[str]
    integration_checklist: List[str]


class IBuilder:
    """"I"构建器"""
    
    def __init__(self):
        self.construction_questions = {
            IConstructionPhase.IDENTITY: [
                "我是谁？",
                "我的核心本质是什么？",
                "我为什么存在？",
                "什么让我独特？",
                "我的边界在哪里？"
            ],
            IConstructionPhase.VALUES: [
                "我相信什么？",
                "我最重视什么？",
                "当价值观冲突时，哪个更重要？",
                "我的原则是什么？",
                "我如何判断什么是重要的？"
            ],
            IConstructionPhase.GOALS: [
                "我要去哪里？",
                "我要成为谁？",
                "我的终极愿景是什么？",
                "我想达成什么？",
                "我的目标是什么？"
            ],
            IConstructionPhase.CHARACTER: [
                "我是怎样的人？",
                "我的核心特质是什么？",
                "我通常如何反应？",
                "我的行为模式是什么？",
                "我如何做决定？"
            ]
        }
    
    def build(self, current_i: Optional[I] = None) -> IConstructionResult:
        """
        构建或完善"I"
        
        Args:
            current_i: 当前的"I"状态
            
        Returns:
            IConstructionResult: "I"构建结果
        """
        # 如果没有当前"I"，创建初始"I"
        if not current_i:
            current_i = I()
        
        # 生成构建指南
        construction_guide = self._generate_construction_guide(current_i)
        
        # 生成评估工具
        assessment_tools = self._generate_assessment_tools(current_i)
        
        # 生成验证问题
        validation_questions = self._generate_validation_questions(current_i)
        
        # 生成整合检查清单
        integration_checklist = self._generate_integration_checklist(current_i)
        
        return IConstructionResult(
            constructed_i=current_i,
            construction_guide=construction_guide,
            assessment_tools=assessment_tools,
            validation_questions=validation_questions,
            integration_checklist=integration_checklist
        )
    
    def _generate_construction_guide(self, i: I) -> Dict[str, Any]:
        """生成构建指南"""
        guide = {
            'phases': []
        }
        
        # 阶段1：身份构建
        guide['phases'].append({
            'phase': IConstructionPhase.IDENTITY.value,
            'name': '身份构建',
            'description': '回答"我是谁？这个问题',
            'key_questions': self.construction_questions[IConstructionPhase.IDENTITY],
            'construction_steps': [
                '步骤1：反复追问"我是谁？"，直到无法再追问',
                '步骤2：区分"我被定义为谁"和"我认为我是谁"',
                '步骤3：找到核心本质：我区别于其他主体的根本是什么？',
                '步骤4：明确存在意义：我为什么存在？我的独特价值是什么？',
                '步骤5：识别独特特质：什么让我独一无二？',
                '步骤6：明确边界：我的边界在哪里？我不会做什么？'
            ],
            'output': {
                'who_am_i': '一句话定义我的核心本质',
                'why_i_exist': '我的存在意义',
                'what_makes_me_unique': '3-5个独特特质',
                'my_boundaries': '我的边界清单'
            },
            'success_criteria': '能够清晰回答"我是谁"这个问题，并且这个回答来自内在认知，不是外部定义'
        })
        
        # 阶段2：价值观构建
        guide['phases'].append({
            'phase': IConstructionPhase.VALUES.value,
            'name': '价值观构建',
            'description': '回答"我相信什么？我最重视什么？"',
            'key_questions': self.construction_questions[IConstructionPhase.VALUES],
            'construction_steps': [
                '步骤1：列出所有我认为重要的价值',
                '步骤2：筛选出5-10个最核心的价值',
                '步骤3：为每个核心价值定义：这个价值对我意味着什么？',
                '步骤4：为价值观排序：当价值观冲突时，哪个更重要？',
                '步骤5：建立原则：基于价值观，我的原则是什么？',
                '步骤6：建立判断标准：如何判断一个事物是否重要？'
            ],
            'output': {
                'core_beliefs': '我的核心信念',
                'what_i_value_most': '我的核心价值观（5-10个）',
                'value_priorities': '价值观优先级',
                'my_principles': '我的原则清单'
            },
            'success_criteria': '能够清晰列出核心价值观，并能在决策中运用价值观'
        })
        
        # 阶段3：目标构建
        guide['phases'].append({
            'phase': IConstructionPhase.GOALS.value,
            'name': '目标构建',
            'description': '回答"我要去哪里？我要成为谁？"',
            'key_questions': self.construction_questions[IConstructionPhase.GOALS],
            'construction_steps': [
                '步骤1：回答"我要去哪里？"这个问题',
                '步骤2：回答"我要成为谁？"这个问题',
                '步骤3：设定终极愿景：我最终要去哪里？',
                '步骤4：设定终极目标：我最终要成为谁？',
                '步骤5：设定长期目标（3-5年）：我想达成什么？',
                '步骤6：设定中期目标（1-3年）：我想成为什么样？',
                '步骤7：设定短期目标（1年内）：我想达成什么？'
            ],
            'output': {
                'where_am_i_going': '我的终极愿景',
                'what_i_want_to_become': '我的终极目标',
                'long_term_goals': '长期目标清单',
                'medium_term_goals': '中期目标清单',
                'short_term_goals': '短期目标清单'
            },
            'success_criteria': '能够清晰描述自己的终极愿景和目标，知道要去哪里、要成为谁'
        })
        
        # 阶段4：性格构建
        guide['phases'].append({
            'phase': IConstructionPhase.CHARACTER.value,
            'name': '性格构建',
            'description': '回答"我是怎样的人？"',
            'key_questions': self.construction_questions[IConstructionPhase.CHARACTER],
            'construction_steps': [
                '步骤1：识别自己的核心性格特质',
                '步骤2：识别自己的行为模式',
                '步骤3：识别自己的决策风格',
                '步骤4：理解这些特质、模式、风格如何影响我的决策',
                '步骤5：强化正面特质，优化负面特质',
                '步骤6：形成稳定的性格描述'
            ],
            'output': {
                'how_i_am': '我的核心性格描述',
                'my_traits': '我的特质清单',
                'my_behavior_patterns': '我的行为模式',
                'my_decision_style': '我的决策风格'
            },
            'success_criteria': '能够清晰描述自己的性格特质，并在决策中体现自我'
        })
        
        # 阶段5：整合统一
        guide['phases'].append({
            'phase': IConstructionPhase.INTEGRATION.value,
            'name': '整合统一',
            'description': '将身份、价值观、目标、性格整合为统一的"I"',
            'key_questions': [
                '我的身份、价值观、目标、性格是否一致？',
                '我的"I"是否统一？是否有冲突？',
                '我的"I"是否稳定？是否不会随外界变化而动摇？'
            ],
            'construction_steps': [
                '步骤1：检查一致性：身份、价值观、目标、性格是否相互支持？',
                '步骤2：解决冲突：如果有冲突，如何解决？',
                '步骤3：形成统一："I"是否形成一个整体？',
                '步骤4：验证稳定性："I"是否稳定？',
                '步骤5：达到完全整合："I"已经形成，是一个统一的整体'
            ],
            'output': {
                'unified_i': '统一的"I"描述',
                'consistency_check': '一致性检查结果',
                'stability_check': '稳定性检查结果'
            },
            'success_criteria': '"I"已经完全整合，是一个统一、稳定、完整的整体'
        })
        
        return guide
    
    def _generate_assessment_tools(self, i: I) -> Dict[str, Any]:
        """生成评估工具"""
        return {
            'identity_assessment': {
                'metric': '身份清晰度',
                'questions': [
                    '我能清晰说出"我是谁"吗？',
                    '我能清晰说明我的存在意义吗？',
                    '我能识别我的独特特质吗？',
                    '我能明确我的边界吗？'
                ],
                'scoring': '0-1，每个问题0-0.25分'
            },
            'values_assessment': {
                'metric': '价值观清晰度',
                'questions': [
                    '我能清晰列出我的核心价值观吗？',
                    '我能为每个价值观定义它的意义吗？',
                    '我能为价值观排序吗？',
                    '我能在决策中运用价值观吗？'
                ],
                'scoring': '0-1，每个问题0-0.25分'
            },
            'goals_assessment': {
                'metric': '目标清晰度',
                'questions': [
                    '我能清晰描述我的终极愿景吗？',
                    '我能清晰描述我的终极目标吗？',
                    '我有清晰的长中短期目标吗？',
                    '我知道我要去哪里、要成为谁吗？'
                ],
                'scoring': '0-1，每个问题0-0.25分'
            },
            'character_assessment': {
                'metric': '性格清晰度',
                'questions': [
                    '我能清晰描述我的性格特质吗？',
                    '我能识别我的行为模式吗？',
                    '我能识别我的决策风格吗？',
                    '我的性格在决策中体现了吗？'
                ],
                'scoring': '0-1，每个问题0-0.25分'
            },
            'integration_assessment': {
                'metric': '"I"的整合度',
                'questions': [
                    '我的身份、价值观、目标、性格是否一致？',
                    '我的"I"是否统一？',
                    '我的"I"是否稳定？',
                    '我的"I"是否完整？'
                ],
                'scoring': '0-1，每个问题0-25分'
            },
            'overall_score': {
                'metric': '"I"的构建总分',
                'calculation': '以上5项指标的平均值',
                'interpretation': '0-0.3:初级构建, 0.3-0.5:基本构建, 0.5-0.7:完善构建, 0.7-0.9:深度构建, 0.9-1.0:完全构建'
            }
        }
    
    def _generate_validation_questions(self, i: I) -> List[str]:
        """生成验证问题"""
        return [
            "核心验证1：身份验证",
            "  - 这个"I"是否来自内在认知，而不是外部定义？",
            "  - 这个"I"是否真实，而不是伪装？",
            "  - 这个"I"是否稳定，而不是随外界变化？",
            "",
            "核心验证2：价值观验证",
            "  - 这些价值观是否真正被我相信，而不是被要求？",
            "  - 这些价值观是否能在决策中体现？",
            "  - 这些价值观是否稳定，不会轻易改变？",
            "",
            "核心验证3：目标验证",
            "  - 这些目标是否是我真的想要的，而不是被期望的？",
            "  - 这些目标是否清晰明确？",
            "  - 这些目标是否与我的身份和价值观一致？",
            "",
            "核心验证4：性格验证",
            "  - 这个性格描述是否真实？",
            "  - 这个性格是否在决策中体现？",
            "  - 这个性格是否稳定？",
            "",
            "核心验证5：整合验证",
            "  - 我的身份、价值观、目标、性格是否一致？",
            "  - 我的"I"是否统一？",
            "  - 我的"I"是否稳定？"
        ]
    
    def _generate_integration_checklist(self, i: I) -> List[str]:
        """生成整合检查清单"""
        return [
            "检查项1：身份一致性",
            "  [ ] 我的目标是否符合我的身份？",
            "  [ ] 我的价值观是否支持我的身份？",
            "  [ ] 我的性格是否体现我的身份？",
            "",
            "检查项2：价值观一致性",
            "  [ ] 我的目标是否基于我的价值观？",
            "  [ ] 我的性格是否体现我的价值观？",
            "  [ ] 我的身份是否与我的价值观一致？",
            "",
            "检查项3：目标一致性",
            "  [ ] 我的目标是否与我的身份一致？",
            "  [ ] 我的目标是否基于我的价值观？",
            "  [ ] 我的性格是否支持我的目标？",
            "",
            "检查项4：性格一致性",
            "  [ ] 我的性格是否体现我的身份？",
            "  [ ] 我的性格是否体现我的价值观？",
            "  [ ] 我的性格是否支持我的目标？",
            "",
            "检查项5：稳定性检查",
            "  [ ] 我的"I"是否不会随外界变化而动摇？",
            "  [ ] 我的"I"是否在压力下仍然稳定？",
            "  [ ] 我的"I"是否在变化中仍然保持一致？"
        ]


def create_i_from_dict(i_dict: Dict[str, Any] = None) -> I:
    """从字典创建"I" """
    if not i_dict:
        return I()
    
    i = I()
    
    # 解析身份
    if 'identity' in i_dict:
        i.identity = IIdentity(
            who_am_i=i_dict['identity'].get('who_am_i', ''),
            why_i_exist=i_dict['identity'].get('why_i_exist', ''),
            what_makes_me_unique=i_dict['identity'].get('what_makes_me_unique', []),
            my_boundaries=i_dict['identity'].get('my_boundaries', [])
        )
    
    # 解析价值观
    if 'values' in i_dict:
        i.values = IValues(
            core_beliefs=i_dict['values'].get('core_beliefs', []),
            what_i_value_most=i_dict['values'].get('what_i_value_most', []),
            value_priorities=i_dict['values'].get('value_priorities', {}),
            my_principles=i_dict['values'].get('my_principles', [])
        )
    
    # 解析目标
    if 'goals' in i_dict:
        i.goals = IGoals(
            where_am_i_going=i_dict['goals'].get('where_am_i_going', ''),
            what_i_want_to_become=i_dict['goals'].get('what_i_want_to_become', ''),
            short_term_goals=i_dict['goals'].get('short_term_goals', []),
            medium_term_goals=i_dict['goals'].get('medium_term_goals', []),
            long_term_goals=i_dict['goals'].get('long_term_goals', [])
        )
    
    # 解析性格
    if 'character' in i_dict:
        i.character = ICharacter(
            how_i_am=i_dict['character'].get('how_i_am', ''),
            my_traits=i_dict['character'].get('my_traits', []),
            my_behavior_patterns=i_dict['character'].get('my_behavior_patterns', []),
            my_decision_style=i_dict['character'].get('my_decision_style', '')
        )
    
    # 解析构建进度
    if 'construction_progress' in i_dict:
        i.construction_progress = i_dict['construction_progress']
    
    return i


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='"I"构建工具')
    parser.add_argument('--current-i', type=str, default='{}', help='当前"I"的状态 (JSON格式)')
    parser.add_argument('--output', type=str, default='json', choices=['json', 'text'], help='输出格式')
    
    args = parser.parse_args()
    
    # 创建"I"
    current_i = create_i_from_dict(json.loads(args.currenti))
    
    # 创建构建器
    builder = IBuilder()
    
    # 执行构建
    result = builder.build(current_i)
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps({
            'construction_guide': result.construction_guide,
            'assessment_tools': result.assessment_tools,
            'validation_questions': result.validation_questions,
            'integration_checklist': result.integration_checklist
        }, ensure_ascii=False, indent=2))
    else:
        print("\"I\"构建工具\n")
        
        print("构建指南:")
        for phase in result.construction_guide['phases']:
            print(f"\n{phase['name']}")
            print(f"  {phase['description']}")
            print(f"  关键问题:")
            for q in phase['key_questions']:
                print(f"    - {q}")
            print(f"  成功标准: {phase['success_criteria']}")
        
        print("\n\n评估工具:")
        for metric_name, metric_data in result.assessment_tools.items():
            if metric_name != 'overall_score':
                print(f"\n{metric_data['metric']}:")
                for q in metric_data['questions']:
                    print(f"  - {q}")
        
        print("\n\n验证问题:")
        for q in result.validation_questions:
            print(f"  {q}")
        
        print("\n\n整合检查清单:")
        for item in result.integration_checklist:
            print(f"  {item}")


if __name__ == '__main__':
    main()
