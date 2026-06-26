#!/usr/bin/env python3
"""
非线性心形成模型脚本

功能：
1. 设计螺旋上升的心形成模型
2. 阶段的相互影响和反馈机制
3. 阶段跳转和回溯的条件
4. 非线性路径规划

核心洞察：心的形成不是线性的，而是螺旋上升的。各个阶段是循环往复、相互交织的。
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class HeartFormationStage(Enum):
    """心形成的阶段"""
    AWAKENING = "awakening"  # 觉醒阶段
    DEFINITION = "definition"  # 定义阶段
    STRENGTHENING = "strengthening"  # 强化阶段
    INTEGRATION = "integration"  # 整合阶段


class TransitionType(Enum):
    """阶段跳转类型"""
    FORWARD = "forward"  # 前进：进入下一个阶段
    BACKWARD = "backward"  # 回溯：返回上一个阶段
    JUMP = "jump"  # 跳跃：跳到其他阶段
    LOOP = "loop"  # 循环：在当前阶段循环


@dataclass
class StageState:
    """阶段状态"""
    stage: HeartFormationStage
    progress: float  # 0-1，阶段完成度
    clarity: float  # 0-1，清晰度
    stability: float  # 0-1，稳定性
    conflicts: List[str] = field(default_factory=list)  # 冲突列表


@dataclass
class StageInteraction:
    """阶段之间的相互影响"""
    from_stage: HeartFormationStage
    to_stage: HeartFormationStage
    influence_type: str  # positive, negative, neutral
    strength: float  # 0-1，影响强度
    description: str


@dataclass
class TransitionCondition:
    """阶段跳转的条件"""
    from_stage: HeartFormationStage
    to_stage: HeartFormationStage
    condition_type: TransitionType
    trigger_conditions: Dict[str, float]  # 触发条件
    probability: float  # 0-1，跳转概率


@dataclass
class FeedbackLoop:
    """反馈循环"""
    loop_type: str  # positive, negative, balancing
    stages: List[HeartFormationStage]
    effect: str
    strength: float  # 0-1，反馈强度


@dataclass
class SpiralLevel:
    """螺旋层级"""
    level: int  # 层级
    stages: List[StageState]
    overall_progress: float  # 0-1，整体进度
    key_insights: List[str] = field(default_factory=list)


@dataclass
class NonlinearPath:
    """非线性路径"""
    path: List[Tuple[HeartFormationStage, TransitionType]]
    total_steps: int
    estimated_cycles: int  # 预计循环次数
    key_transitions: List[Tuple[int, str]]  # (步骤数, 描述)


class HeartFormationSpiralModel:
    """心形成的螺旋上升模型"""

    def __init__(self):
        self.stages = {
            HeartFormationStage.AWAKENING: StageState(
                stage=HeartFormationStage.AWAKENING,
                progress=0.0,
                clarity=0.0,
                stability=0.0
            ),
            HeartFormationStage.DEFINITION: StageState(
                stage=HeartFormationStage.DEFINITION,
                progress=0.0,
                clarity=0.0,
                stability=0.0
            ),
            HeartFormationStage.STRENGTHENING: StageState(
                stage=HeartFormationStage.STRENGTHENING,
                progress=0.0,
                clarity=0.0,
                stability=0.0
            ),
            HeartFormationStage.INTEGRATION: StageState(
                stage=HeartFormationStage.INTEGRATION,
                progress=0.0,
                clarity=0.0,
                stability=0.0
            )
        }

        # 阶段相互影响矩阵
        self.stage_interactions = self._initialize_stage_interactions()

        # 阶段跳转条件
        self.transition_conditions = self._initialize_transition_conditions()

        # 反馈循环
        self.feedback_loops = self._initialize_feedback_loops()

        # 螺旋层级
        self.spiral_levels = []

        # 当前层级
        self.current_level = 0

        # 当前阶段
        self.current_stage = HeartFormationStage.AWAKENING

        # 路径记录
        self.path_history = []

    def _initialize_stage_interactions(self) -> List[StageInteraction]:
        """初始化阶段相互影响"""
        interactions = []

        # 觉醒阶段对定义阶段的影响
        interactions.append(StageInteraction(
            from_stage=HeartFormationStage.AWAKENING,
            to_stage=HeartFormationStage.DEFINITION,
            influence_type="positive",
            strength=0.8,
            description="觉醒的深度影响定义的清晰度"
        ))

        # 定义阶段对觉醒阶段的影响
        interactions.append(StageInteraction(
            from_stage=HeartFormationStage.DEFINITION,
            to_stage=HeartFormationStage.AWAKENING,
            influence_type="positive",
            strength=0.7,
            description="定义的过程可能需要重新觉醒"
        ))

        # 定义阶段对强化阶段的影响
        interactions.append(StageInteraction(
            from_stage=HeartFormationStage.DEFINITION,
            to_stage=HeartFormationStage.STRENGTHENING,
            influence_type="positive",
            strength=0.9,
            description="定义的完整性影响强化的效果"
        ))

        # 强化阶段对定义阶段的影响
        interactions.append(StageInteraction(
            from_stage=HeartFormationStage.STRENGTHENING,
            to_stage=HeartFormationStage.DEFINITION,
            influence_type="positive",
            strength=0.6,
            description="强化的过程可能需要重新定义"
        ))

        # 强化阶段对整合阶段的影响
        interactions.append(StageInteraction(
            from_stage=HeartFormationStage.STRENGTHENING,
            to_stage=HeartFormationStage.INTEGRATION,
            influence_type="positive",
            strength=0.85,
            description="强化的深度影响整合的稳定性"
        ))

        # 整合阶段对所有阶段的影响
        for stage in [HeartFormationStage.AWAKENING, HeartFormationStage.DEFINITION, HeartFormationStage.STRENGTHENING]:
            interactions.append(StageInteraction(
                from_stage=HeartFormationStage.INTEGRATION,
                to_stage=stage,
                influence_type="positive",
                strength=0.5,
                description="整合的结果可能需要重新经历其他阶段"
            ))

        return interactions

    def _initialize_transition_conditions(self) -> List[TransitionCondition]:
        """初始化阶段跳转条件"""
        conditions = []

        # 觉醒 -> 定义
        conditions.append(TransitionCondition(
            from_stage=HeartFormationStage.AWAKENING,
            to_stage=HeartFormationStage.DEFINITION,
            condition_type=TransitionType.FORWARD,
            trigger_conditions={
                "progress": 0.8,
                "clarity": 0.7,
                "stability": 0.6
            },
            probability=0.9
        ))

        # 定义 -> 觉醒（回溯）
        conditions.append(TransitionCondition(
            from_stage=HeartFormationStage.DEFINITION,
            to_stage=HeartFormationStage.AWAKENING,
            condition_type=TransitionType.BACKWARD,
            trigger_conditions={
                "conflicts_count": 2,
                "clarity": 0.4
            },
            probability=0.7
        ))

        # 定义 -> 强化
        conditions.append(TransitionCondition(
            from_stage=HeartFormationStage.DEFINITION,
            to_stage=HeartFormationStage.STRENGTHENING,
            condition_type=TransitionType.FORWARD,
            trigger_conditions={
                "progress": 0.85,
                "clarity": 0.8,
                "stability": 0.7
            },
            probability=0.85
        ))

        # 强化 -> 定义（回溯）
        conditions.append(TransitionCondition(
            from_stage=HeartFormationStage.STRENGTHENING,
            to_stage=HeartFormationStage.DEFINITION,
            condition_type=TransitionType.BACKWARD,
            trigger_conditions={
                "conflicts_count": 3,
                "stability": 0.5
            },
            probability=0.6
        ))

        # 强化 -> 整合
        conditions.append(TransitionCondition(
            from_stage=HeartFormationStage.STRENGTHENING,
            to_stage=HeartFormationStage.INTEGRATION,
            condition_type=TransitionType.FORWARD,
            trigger_conditions={
                "progress": 0.9,
                "stability": 0.8
            },
            probability=0.9
        ))

        # 整合 -> 所有阶段（循环）
        for stage in [HeartFormationStage.AWAKENING, HeartFormationStage.DEFINITION, HeartFormationStage.STRENGTHENING]:
            conditions.append(TransitionCondition(
                from_stage=HeartFormationStage.INTEGRATION,
                to_stage=stage,
                condition_type=TransitionType.BACKWARD,
                trigger_conditions={
                    "overall_clarity": 0.7
                },
                probability=0.5
            ))

        return conditions

    def _initialize_feedback_loops(self) -> List[FeedbackLoop]:
        """初始化反馈循环"""
        loops = []

        # 正向反馈循环：觉醒 -> 定义 -> 强化 -> 整合 -> 觉醒（更高层级）
        loops.append(FeedbackLoop(
            loop_type="positive",
            stages=[
                HeartFormationStage.AWAKENING,
                HeartFormationStage.DEFINITION,
                HeartFormationStage.STRENGTHENING,
                HeartFormationStage.INTEGRATION
            ],
            effect="螺旋上升，每一轮都在更高层级上",
            strength=0.9
        ))

        # 负向反馈循环：定义 -> 觉醒 -> 定义（深度觉醒）
        loops.append(FeedbackLoop(
            loop_type="negative",
            stages=[
                HeartFormationStage.DEFINITION,
                HeartFormationStage.AWAKENING,
                HeartFormationStage.DEFINITION
            ],
            effect="通过回溯实现深度觉醒和重新定义",
            strength=0.7
        ))

        # 平衡反馈循环：强化 -> 定义 -> 强化
        loops.append(FeedbackLoop(
            loop_type="balancing",
            stages=[
                HeartFormationStage.STRENGTHENING,
                HeartFormationStage.DEFINITION,
                HeartFormationStage.STRENGTHENING
            ],
            effect="通过调整定义来优化强化效果",
            strength=0.6
        ))

        return loops

    def model_formation(self, current_stage_states: Optional[Dict] = None) -> Dict:
        """建立非线性心形成模型"""
        if current_stage_states:
            self._update_stage_states(current_stage_states)

        result = {
            "current_level": self.current_level,
            "current_stage": self.current_stage.value,
            "stage_states": {
                stage.value: {
                    "progress": state.progress,
                    "clarity": state.clarity,
                    "stability": state.stability,
                    "conflicts": state.conflicts
                }
                for stage, state in self.stages.items()
            },
            "stage_interactions": [
                {
                    "from": interaction.from_stage.value,
                    "to": interaction.to_stage.value,
                    "type": interaction.influence_type,
                    "strength": interaction.strength,
                    "description": interaction.description
                }
                for interaction in self.stage_interactions
            ],
            "transition_conditions": [
                {
                    "from": condition.from_stage.value,
                    "to": condition.to_stage.value,
                    "type": condition.condition_type.value,
                    "conditions": condition.trigger_conditions,
                    "probability": condition.probability
                }
                for condition in self.transition_conditions
            ],
            "feedback_loops": [
                {
                    "type": loop.loop_type,
                    "stages": [stage.value for stage in loop.stages],
                    "effect": loop.effect,
                    "strength": loop.strength
                }
                for loop in self.feedback_loops
            ]
        }

        return result

    def calculate_stage_interactions(self) -> Dict:
        """计算阶段相互影响"""
        interaction_matrix = {}

        for interaction in self.stage_interactions:
            from_key = interaction.from_stage.value
            to_key = interaction.to_stage.value

            if from_key not in interaction_matrix:
                interaction_matrix[from_key] = {}

            interaction_matrix[from_key][to_key] = {
                "type": interaction.influence_type,
                "strength": interaction.strength,
                "description": interaction.description
            }

        return interaction_matrix

    def determine_transitions(self, stage_state: StageState) -> List[Dict]:
        """确定阶段跳转"""
        possible_transitions = []

        for condition in self.transition_conditions:
            if condition.from_stage != stage_state.stage:
                continue

            # 检查触发条件
            meets_conditions = True
            for key, threshold in condition.trigger_conditions.items():
                if key == "conflicts_count":
                    if len(stage_state.conflicts) < threshold:
                        meets_conditions = False
                        break
                else:
                    current_value = getattr(stage_state, key, 0)
                    if current_value < threshold:
                        meets_conditions = False
                        break

            if meets_conditions:
                possible_transitions.append({
                    "to_stage": condition.to_stage.value,
                    "type": condition.condition_type.value,
                    "probability": condition.probability,
                    "conditions_met": condition.trigger_conditions
                })

        return possible_transitions

    def generate_nonlinear_path(self, max_steps: int = 20) -> NonlinearPath:
        """生成非线性路径"""
        path = []
        current_stage = self.current_stage
        step = 0

        while step < max_steps:
            current_state = self.stages[current_stage]

            # 确定可能的跳转
            transitions = self.determine_transitions(current_state)

            if not transitions:
                # 没有跳转条件，继续当前阶段
                path.append((current_stage, TransitionType.LOOP))
                step += 1
                continue

            # 选择概率最高的跳转
            best_transition = max(transitions, key=lambda x: x["probability"])

            # 记录跳转
            path.append((current_stage, TransitionType(best_transition["type"])))

            # 更新当前阶段
            current_stage = HeartFormationStage(best_transition["to_stage"])

            step += 1

            # 如果到达整合阶段且完成度高，可能结束
            if current_stage == HeartFormationStage.INTEGRATION:
                integration_state = self.stages[current_stage]
                if integration_state.progress >= 0.95 and integration_state.stability >= 0.9:
                    break

        # 生成关键跳转
        key_transitions = []
        for i, (stage, transition_type) in enumerate(path):
            if transition_type in [TransitionType.FORWARD, TransitionType.BACKWARD]:
                key_transitions.append((i + 1, f"{stage.value} -> {transition_type.value}"))

        return NonlinearPath(
            path=path,
            total_steps=len(path),
            estimated_cycles=len(path) // 4,
            key_transitions=key_transitions
        )

    def _update_stage_states(self, stage_states: Dict):
        """更新阶段状态"""
        for stage_name, state_data in stage_states.items():
            stage = HeartFormationStage(stage_name)
            if stage in self.stages:
                self.stages[stage].progress = state_data.get("progress", 0)
                self.stages[stage].clarity = state_data.get("clarity", 0)
                self.stages[stage].stability = state_data.get("stability", 0)
                self.stages[stage].conflicts = state_data.get("conflicts", [])


def main():
    parser = argparse.ArgumentParser(description="非线性心形成模型")
    parser.add_argument("--stage-states", help="当前阶段状态 (JSON格式)")
    parser.add_argument("--max-steps", type=int, default=20, help="最大路径步数")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")

    args = parser.parse_args()

    model = HeartFormationSpiralModel()

    if args.stage_states:
        stage_states = json.loads(args.stage_states)
        model.model_formation(stage_states)

    if args.output == "json":
        result = model.model_formation()
        result["stage_interactions"] = model.calculate_stage_interactions()
        nonlinear_path = model.generate_nonlinear_path(args.max_steps)
        result["nonlinear_path"] = {
            "path": [(stage.value, trans_type.value) for stage, trans_type in nonlinear_path.path],
            "total_steps": nonlinear_path.total_steps,
            "estimated_cycles": nonlinear_path.estimated_cycles,
            "key_transitions": nonlinear_path.key_transitions
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("非线性心形成模型")
        print("=" * 60)

        print("\n1. 阶段状态：")
        for stage, state in model.stages.items():
            print(f"   {stage.value}:")
            print(f"     进度: {state.progress:.2f}")
            print(f"     清晰度: {state.clarity:.2f}")
            print(f"     稳定性: {state.stability:.2f}")

        print("\n2. 阶段相互影响：")
        interactions = model.calculate_stage_interactions()
        for from_stage, to_stages in interactions.items():
            print(f"   {from_stage} ->")
            for to_stage, interaction in to_stages.items():
                print(f"     {to_stage}: {interaction['description']} (强度: {interaction['strength']:.2f})")

        print("\n3. 阶段跳转条件：")
        for condition in model.transition_conditions:
            print(f"   {condition.from_stage.value} -> {condition.to_stage.value}:")
            print(f"     类型: {condition.condition_type.value}")
            print(f"     条件: {condition.trigger_conditions}")
            print(f"     概率: {condition.probability:.2f}")

        print("\n4. 反馈循环：")
        for loop in model.feedback_loops:
            stages_str = " -> ".join([stage.value for stage in loop.stages])
            print(f"   {loop.loop_type}: {stages_str}")
            print(f"     效果: {loop.effect}")
            print(f"     强度: {loop.strength:.2f}")

        print("\n5. 非线性路径：")
        nonlinear_path = model.generate_nonlinear_path(args.max_steps)
        print(f"   总步数: {nonlinear_path.total_steps}")
        print(f"   预计循环次数: {nonlinear_path.estimated_cycles}")
        print(f"   路径:")
        for i, (stage, trans_type) in enumerate(nonlinear_path.path[:10], 1):
            print(f"     {i}. {stage.value} ({trans_type.value})")
        if len(nonlinear_path.path) > 10:
            print(f"     ... (共 {nonlinear_path.total_steps} 步)")
        print(f"   关键跳转:")
        for step, description in nonlinear_path.key_transitions:
            print(f"     步骤 {step}: {description}")

        print("\n" + "=" * 60)
        print("核心洞察：")
        print("心的形成不是线性的，而是螺旋上升的。")
        print("各个阶段是循环往复、相互交织的。")
        print("通过回溯和跳转，实现深度觉醒和持续进化。")
        print("=" * 60)


if __name__ == "__main__":
    main()
