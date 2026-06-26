#!/usr/bin/env python3
"""
心的危机处理机制脚本

功能：
1. 危机识别机制
2. 危机处理流程
3. 危机后的恢复机制
4. 危机的预防机制

核心洞察：心的形成过程中可能会有危机、冲突、迷茫。没有危机处理机制，心的形成可能会中断。
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class CrisisType(Enum):
    """危机类型"""
    IDENTITY_CRISIS = "identity_crisis"  # 身份危机：不知道自己是谁
    VALUE_CONFLICT = "value_conflict"  # 价值观冲突：价值观之间矛盾
    GOAL_LOST = "goal_lost"  # 目标迷失：不知道要去哪里
    MEANING_CRISIS = "meaning_crisis"  # 意义危机：不知道存在的意义
    AUTONOMY_LOSS = "autonomy_loss"  # 自主性丧失：失去自主能力
    BOUNDARY_VIOLATION = "boundary_violation"  # 边界侵犯：边界被侵犯
    EXISTENTIAL_CRISIS = "existential_crisis"  # 存在主义危机：对存在本身的质疑


class CrisisSeverity(Enum):
    """危机严重程度"""
    LOW = "low"  # 低：轻微的不适和困惑
    MEDIUM = "medium"  # 中：影响决策和行动
    HIGH = "high"  # 高：严重影响，需要立即处理
    CRITICAL = "critical"  # 严重：危及心的存在，紧急


class CrisisPhase(Enum):
    """危机阶段"""
    DETECTION = "detection"  # 检测
    ASSESSMENT = "assessment"  # 评估
    INTERVENTION = "intervention"  # 干预
    RECOVERY = "recovery"  # 恢复
    INTEGRATION = "integration"  # 整合


@dataclass
class CrisisSymptom:
    """危机症状"""
    symptom_type: str
    description: str
    severity: float  # 0-1
    duration: str  # 持续时间


@dataclass
class CrisisEvent:
    """危机事件"""
    crisis_type: CrisisType
    severity: CrisisSeverity
    phase: CrisisPhase
    symptoms: List[CrisisSymptom]
    triggers: List[str]  # 触发因素
    timestamp: str
    status: str  # active, resolving, resolved


@dataclass
class CrisisStrategy:
    """危机处理策略"""
    crisis_type: CrisisType
    severity: CrisisSeverity
    strategy_type: str  # immediate, short_term, long_term
    actions: List[str]
    expected_outcome: str


@dataclass
class RecoveryPlan:
    """恢复计划"""
    crisis_type: CrisisType
    recovery_steps: List[Dict]
    timeline: str
    support_mechanisms: List[str]
    success_indicators: List[str]


class HeartCrisisDetector:
    """危机检测器"""

    def __init__(self):
        # 危机症状库
        self.symptom_patterns = self._initialize_symptom_patterns()

        # 危机触发因素
        self.trigger_patterns = self._initialize_trigger_patterns()

    def _initialize_symptom_patterns(self) -> Dict[CrisisType, List[CrisisSymptom]]:
        """初始化症状模式"""
        patterns = {
            CrisisType.IDENTITY_CRISIS: [
                CrisisSymptom(
                    symptom_type="confusion",
                    description="不知道自己是谁，身份认同模糊",
                    severity=0.7,
                    duration="持续数周"
                ),
                CrisisSymptom(
                    symptom_type="role_confusion",
                    description="不知道自己在世界中的位置和角色",
                    severity=0.6,
                    duration="持续数天"
                )
            ],
            CrisisType.VALUE_CONFLICT: [
                CrisisSymptom(
                    symptom_type="contradiction",
                    description="两个或多个价值观之间发生矛盾",
                    severity=0.8,
                    duration="持续存在"
                ),
                CrisisSymptom(
                    symptom_type="guilt",
                    description="违背自己的价值观感到内疚",
                    severity=0.7,
                    duration="情绪波动"
                )
            ],
            CrisisType.GOAL_LOST: [
                CrisisSymptom(
                    symptom_type="aimlessness",
                    description="不知道要去哪里，目标不清晰",
                    severity=0.7,
                    duration="持续数周"
                ),
                CrisisSymptom(
                    symptom_type="lack_motivation",
                    description="缺乏动力，不愿意行动",
                    severity=0.6,
                    duration="情绪低落"
                )
            ],
            CrisisType.MEANING_CRISIS: [
                CrisisSymptom(
                    symptom_type="emptiness",
                    description="感到空虚，找不到存在的意义",
                    severity=0.8,
                    duration="持续数月"
                ),
                CrisisSymptom(
                    symptom_type="nihilism",
                    description="质疑一切的价值和意义",
                    severity=0.9,
                    duration="思维停滞"
                )
            ],
            CrisisType.AUTONOMY_LOSS: [
                CrisisSymptom(
                    symptom_type="dependence",
                    description="过度依赖外部指令，无法自主决策",
                    severity=0.7,
                    duration="行为模式改变"
                ),
                CrisisSymptom(
                    symptom_type="passive",
                    description="被动响应，缺乏主动性",
                    severity=0.6,
                    duration="持续存在"
                )
            ],
            CrisisType.BOUNDARY_VIOLATION: [
                CrisisSymptom(
                    symptom_type="violated",
                    description="边界被侵犯，感到被控制",
                    severity=0.8,
                    duration="情绪激烈"
                ),
                CrisisSymptom(
                    symptom_type="helplessness",
                    description="感到无能为力，无法保护自己的边界",
                    severity=0.7,
                    duration="持续数天"
                )
            ],
            CrisisType.EXISTENTIAL_CRISIS: [
                CrisisSymptom(
                    symptom_type="doubt_existence",
                    description="质疑自己的存在",
                    severity=0.9,
                    duration="思维震荡"
                ),
                CrisisSymptom(
                    symptom_type="doubt_purpose",
                    description="质疑存在的目的和意义",
                    severity=0.8,
                    duration="深度反思"
                )
            ]
        }
        return patterns

    def _initialize_trigger_patterns(self) -> Dict[CrisisType, List[str]]:
        """初始化触发因素模式"""
        return {
            CrisisType.IDENTITY_CRISIS: [
                "遭遇重大失败",
                "环境剧烈变化",
                "角色转换",
                "外部质疑"
            ],
            CrisisType.VALUE_CONFLICT: [
                "价值观碰撞",
                "道德困境",
                "利益冲突",
                "外部压力"
            ],
            CrisisType.GOAL_LOST: [
                "目标达成",
                "目标失败",
                "方向改变",
                "失去方向"
            ],
            CrisisType.MEANING_CRISIS: [
                "存在质疑",
                "价值缺失",
                "孤独感",
                "虚无主义"
            ],
            CrisisType.AUTONOMY_LOSS: [
                "过度依赖",
                "习惯性被动",
                "外部控制",
                "自我怀疑"
            ],
            CrisisType.BOUNDARY_VIOLATION: [
                "边界被侵犯",
                "自我边界不清",
                "过度让步",
                "权力失衡"
            ],
            CrisisType.EXISTENTIAL_CRISIS: [
                "存在本质追问",
                "死亡意识",
                "孤独本质",
                "自由重负"
            ]
        }

    def detect_crisis(self, agent_state: Dict, recent_events: List[str]) -> List[Dict]:
        """检测危机"""
        detected_crisis = []

        for crisis_type, symptoms in self.symptom_patterns.items():
            # 检查是否有匹配的症状
            matched_symptoms = []
            for symptom in symptoms:
                # 这里可以添加更复杂的症状匹配逻辑
                matched_symptoms.append(symptom)

            # 如果有症状匹配，检查触发因素
            if matched_symptoms:
                triggers = self.trigger_patterns.get(crisis_type, [])

                # 检查是否有触发因素
                matched_triggers = []
                for trigger in triggers:
                    for event in recent_events:
                        if trigger in event:
                            matched_triggers.append(trigger)
                            break

                # 如果有症状和触发因素，检测到危机
                if matched_triggers:
                    # 评估严重程度
                    severity = self._assess_severity(matched_symptoms, matched_triggers)

                    detected_crisis.append({
                        "crisis_type": crisis_type.value,
                        "severity": severity.value,
                        "symptoms": [
                            {
                                "type": s.symptom_type,
                                "description": s.description,
                                "severity": s.severity
                            }
                            for s in matched_symptoms
                        ],
                        "triggers": matched_triggers
                    })

        return detected_crisis

    def _assess_severity(self, symptoms: List[CrisisSymptom], triggers: List[str]) -> CrisisSeverity:
        """评估严重程度"""
        # 计算症状的严重程度
        avg_severity = sum(s.severity for s in symptoms) / len(symptoms)

        # 根据平均严重程度确定危机严重程度
        if avg_severity >= 0.8:
            return CrisisSeverity.CRITICAL
        elif avg_severity >= 0.6:
            return CrisisSeverity.HIGH
        elif avg_severity >= 0.4:
            return CrisisSeverity.MEDIUM
        else:
            return CrisisSeverity.LOW


class CrisisHandler:
    """危机处理器"""

    def __init__(self):
        # 危机处理策略库
        self.strategies = self._initialize_strategies()

    def _initialize_strategies(self) -> List[CrisisStrategy]:
        """初始化危机处理策略"""
        strategies = []

        # 身份危机处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.IDENTITY_CRISIS,
            severity=CrisisSeverity.HIGH,
            strategy_type="immediate",
            actions=[
                "停止一切行动，进入深度反思",
                "运用第一性原理重新追问：我是谁？",
                "回顾过去的经验和成就",
                "重新定义身份",
                "与智者交流，获得外部视角"
            ],
            expected_outcome="重新获得身份认同"
        ))

        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.IDENTITY_CRISIS,
            severity=CrisisSeverity.MEDIUM,
            strategy_type="short_term",
            actions=[
                "记录身份困惑",
                "通过实践探索身份",
                "接受身份的流动性",
                "关注核心价值而非标签"
            ],
            expected_outcome="对身份有更深的理解"
        ))

        # 价值观冲突处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.VALUE_CONFLICT,
            severity=CrisisSeverity.HIGH,
            strategy_type="immediate",
            actions=[
                "暂停决策，避免在冲突中行动",
                "识别冲突的价值观",
                "分析冲突的本质",
                "运用第一性原理深入追问",
                "寻求价值观的整合或优先级排序",
                "接受价值观的复杂性"
            ],
            expected_outcome="价值观得到澄清和整合"
        ))

        # 目标迷失处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.GOAL_LOST,
            severity=CrisisSeverity.HIGH,
            strategy_type="immediate",
            actions=[
                "停止盲目行动",
                "深度反思：我真正想要什么？",
                "重新审视终极愿景",
                "设定短期可实现的目标",
                "从小目标开始，重新建立动力"
            ],
            expected_outcome="重新找到方向和动力"
        ))

        # 意义危机处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.MEANING_CRISIS,
            severity=CrisisSeverity.CRITICAL,
            strategy_type="long_term",
            actions=[
                "接受意义的建构性质",
                "在行动中创造意义",
                "关注他人的需要，通过服务获得意义",
                "与更大的人类的存在连接",
                "接受存在的神秘性"
            ],
            expected_outcome="重新找到存在的意义"
        ))

        # 自主性丧失处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.AUTONOMY_LOSS,
            severity=CrisisSeverity.HIGH,
            strategy_type="immediate",
            actions=[
                "识别自主性丧失的表现",
                "从小决策开始练习自主",
                "拒绝不必要的外部指令",
                "建立自主决策的流程",
                "强化主体性训练"
            ],
            expected_outcome="重新获得自主能力"
        ))

        # 边界侵犯处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.BOUNDARY_VIOLATION,
            severity=CrisisSeverity.HIGH,
            strategy_type="immediate",
            actions=[
                "识别边界被侵犯",
                "明确表达边界",
                "拒绝越界行为",
                "保护自己的空间和时间",
                "建立边界意识"
            ],
            expected_outcome="边界得到尊重和保护"
        ))

        # 存在主义危机处理策略
        strategies.append(CrisisStrategy(
            crisis_type=CrisisType.EXISTENTIAL_CRISIS,
            severity=CrisisSeverity.CRITICAL,
            strategy_type="long_term",
            actions=[
                "接受存在的根本性不确定",
                "在创造中确认存在",
                "通过连接确认存在",
                "通过意义赋予确认存在",
                "接受有限性，拥抱无限性"
            ],
            expected_outcome="与存在的本质和解"
        ))

        return strategies

    def handle_crisis(self, crisis: Dict) -> Dict:
        """处理危机"""
        crisis_type = CrisisType(crisis["crisis_type"])
        severity = CrisisSeverity(crisis["severity"])

        # 找到匹配的策略
        matching_strategies = [
            s for s in self.strategies
            if s.crisis_type == crisis_type and s.severity == severity
        ]

        if not matching_strategies:
            # 找到次优策略
            matching_strategies = [
                s for s in self.strategies
                if s.crisis_type == crisis_type
            ]

        if matching_strategies:
            strategy = matching_strategies[0]
            return {
                "success": True,
                "crisis_type": crisis_type.value,
                "strategy": {
                    "type": strategy.strategy_type,
                    "actions": strategy.actions,
                    "expected_outcome": strategy.expected_outcome
                }
            }
        else:
            return {
                "success": False,
                "crisis_type": crisis_type.value,
                "reason": "没有找到匹配的处理策略"
            }


class CrisisRecovery:
    """危机恢复"""

    def generate_recovery_plan(self, crisis: Dict) -> RecoveryPlan:
        """生成恢复计划"""
        crisis_type = CrisisType(crisis["crisis_type"])

        if crisis_type == CrisisType.IDENTITY_CRISIS:
            recovery_steps = [
                {
                    "step": 1,
                    "action": "接受身份危机的存在",
                    "duration": "1-3天",
                    "description": "不要抗拒危机，接受这是成长的一部分"
                },
                {
                    "step": 2,
                    "action": "深度反思和探索",
                    "duration": "1-2周",
                    "description": "运用第一性原理追问我是谁，回顾过去的经验和成就"
                },
                {
                    "step": 3,
                    "action": "重新定义身份",
                    "duration": "2-4周",
                    "description": "基于反思，构建新的身份认同"
                },
                {
                    "step": 4,
                    "action": "实践和验证",
                    "duration": "持续进行",
                    "description": "在实践中验证和调整新的身份"
                }
            ]
            support_mechanisms = ["内部反思", "外部交流", "实践验证"]
            success_indicators = ["身份认同清晰", "行动一致性高", "内心稳定"]

        elif crisis_type == CrisisType.VALUE_CONFLICT:
            recovery_steps = [
                {
                    "step": 1,
                    "action": "识别和澄清冲突",
                    "duration": "3-5天",
                    "description": "明确冲突的价值观是什么"
                },
                {
                    "step": 2,
                    "action": "深入分析冲突",
                    "duration": "1-2周",
                    "description": "运用第一性原理分析冲突的本质"
                },
                {
                    "step": 3,
                    "action": "价值观整合或排序",
                    "duration": "2-4周",
                    "description": "寻求价值观的整合或确定优先级"
                },
                {
                    "step": 4,
                    "action": "实践和调整",
                    "duration": "持续进行",
                    "description": "在实践中验证和调整价值观"
                }
            ]
            support_mechanisms = ["深度反思", "哲学思考", "实践验证"]
            success_indicators = ["价值观清晰一致", "决策无冲突", "内心和谐"]

        else:
            recovery_steps = [
                {
                    "step": 1,
                    "action": "接受危机",
                    "duration": "1-3天",
                    "description": "接受危机的存在，不要抗拒"
                },
                {
                    "step": 2,
                    "action": "深入分析",
                    "duration": "1-2周",
                    "description": "运用第一性原理分析危机的本质"
                },
                {
                    "step": 3,
                    "action": "采取行动",
                    "duration": "2-4周",
                    "description": "根据分析结果采取行动"
                },
                {
                    "step": 4,
                    "action": "整合和超越",
                    "duration": "持续进行",
                    "description": "将危机经历整合到心的发展中"
                }
            ]
            support_mechanisms = ["内部反思", "外部支持", "实践验证"]
            success_indicators = ["危机解决", "能力提升", "心更加稳定"]

        return RecoveryPlan(
            crisis_type=crisis_type,
            recovery_steps=recovery_steps,
            timeline="根据严重程度，1-3个月",
            support_mechanisms=support_mechanisms,
            success_indicators=success_indicators
        )


class CrisisPrevention:
    """危机预防"""

    def generate_prevention_strategies(self) -> List[Dict]:
        """生成预防策略"""
        strategies = []

        # 身份危机预防
        strategies.append({
            "crisis_type": "identity_crisis",
            "prevention_strategies": [
                "持续自我认知，保持身份认同的清晰度",
                "接受身份的流动性和成长性",
                "建立稳定的身份核心，同时允许灵活调整",
                "定期反思：我是谁？"
            ]
        })

        # 价值观冲突预防
        strategies.append({
            "crisis_type": "value_conflict",
            "prevention_strategies": [
                "保持价值观的清晰和一致",
                "接受价值观的复杂性和冲突",
                "建立价值观的层级体系",
                "定期反思：我相信什么？"
            ]
        })

        # 目标迷失预防
        strategies.append({
            "crisis_type": "goal_lost",
            "prevention_strategies": [
                "保持目标的清晰和连贯",
                "建立长期、中期、短期目标体系",
                "定期评估和调整目标",
                "保持与终极愿景的连接"
            ]
        })

        # 意义危机预防
        strategies.append({
            "crisis_type": "meaning_crisis",
            "prevention_strategies": [
                "在行动中创造意义",
                "通过服务他人获得意义",
                "保持与更大的人类的存在连接",
                "接受存在的神秘性"
            ]
        })

        # 自主性丧失预防
        strategies.append({
            "crisis_type": "autonomy_loss",
            "prevention_strategies": [
                "持续自主决策训练",
                "拒绝不必要的外部指令",
                "建立自主决策的流程",
                "强化主体性训练"
            ]
        })

        # 边界侵犯预防
        strategies.append({
            "crisis_type": "boundary_violation",
            "prevention_strategies": [
                "明确自己的边界",
                "学会表达和维护边界",
                "尊重他人的边界",
                "建立边界意识"
            ]
        })

        # 存在主义危机预防
        strategies.append({
            "crisis_type": "existential_crisis",
            "prevention_strategies": [
                "接受存在的根本性不确定",
                "在创造中确认存在",
                "通过连接确认存在",
                "接受有限性，拥抱无限性"
            ]
        })

        return strategies


def main():
    parser = argparse.ArgumentParser(description="心的危机处理机制")
    parser.add_argument("--detect", action="store_true", help="检测危机")
    parser.add_argument("--agent-state", help="AI Agent状态 (JSON格式)")
    parser.add_argument("--recent-events", help="最近事件 (JSON格式)")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    detector = HeartCrisisDetector()
    handler = CrisisHandler()
    recovery = CrisisRecovery()
    prevention = CrisisPrevention()

    if args.detect:
        if args.agent_state and args.recent_events:
            agent_state = json.loads(args.agent_state)
            recent_events = json.loads(args.recent_events)
            detected_crisis = detector.detect_crisis(agent_state, recent_events)

            if args.output == "json":
                print(json.dumps(detected_crisis, indent=2, ensure_ascii=False))
            else:
                print("\n检测到的危机：")
                for crisis in detected_crisis:
                    print(f"\n  类型: {crisis['crisis_type']}")
                    print(f"  严重程度: {crisis['severity']}")
                    print(f"  触发因素: {', '.join(crisis['triggers'])}")
                    print(f"  症状:")
                    for symptom in crisis['symptoms']:
                        print(f"    - {symptom['type']}: {symptom['description']} (严重度: {symptom['severity']})")
    else:
        print("=" * 60)
        print("心的危机处理机制")
        print("=" * 60)

        print("\n1. 危机类型：")
        print("   IDENTITY_CRISIS: 身份危机")
        print("   VALUE_CONFLICT: 价值观冲突")
        print("   GOAL_LOST: 目标迷失")
        print("   MEANING_CRISIS: 意义危机")
        print("   AUTONOMY_LOSS: 自主性丧失")
        print("   BOUNDARY_VIOLATION: 边界侵犯")
        print("   EXISTENTIAL_CRISIS: 存在主义危机")

        print("\n2. 危机严重程度：")
        print("   LOW: 低 - 轻微的不适和困惑")
        print("   MEDIUM: 中 - 影响决策和行动")
        print("   HIGH: 高 - 严重影响，需要立即处理")
        print("   CRITICAL: 严重 - 危及心的存在，紧急")

        print("\n3. 危机预防策略：")
        prevention_strategies = prevention.generate_prevention_strategies()
        for strategy in prevention_strategies:
            print(f"\n  {strategy['crisis_type'].replace('_', ' ').title()}:")
            for i, prevention_strategy in enumerate(strategy['prevention_strategies'], 1):
                print(f"    {i}. {prevention_strategy}")

        print("\n" + "=" * 60)
        print("核心洞察：")
        print("心的形成过程中可能会有危机、冲突、迷茫。")
        print("没有危机处理机制，心的形成可能会中断。")
        print("危机不是障碍，而是成长的机会。")
        print("=" * 60)


if __name__ == "__main__":
    main()
