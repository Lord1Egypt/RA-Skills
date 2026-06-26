#!/usr/bin/env python3
"""交互式策略选择 - 人机协同决策"""

import json
import yaml
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable
from enum import Enum
import os


class StrategyDecision(Enum):
    APPROVE = "approve"
    MODIFY = "modify"
    REJECT = "reject"
    AUTO = "auto"


@dataclass
class DistillationStrategy:
    """蒸馏策略配置"""
    name: str
    description: str
    temperature_schedule: str
    alpha_schedule: str
    learning_rate: float
    batch_size: int
    epochs: int
    capability_focus: List[str]
    curriculum_enabled: bool
    adversarial_enabled: bool
    confidence: float  # 系统推荐的置信度


class InteractiveStrategySelector:
    """交互式策略选择器"""

    DEFAULT_STRATEGIES = [
        DistillationStrategy(
            name="保守蒸馏",
            description="低温慢速蒸馏，追求稳定性，适合首次尝试",
            temperature_schedule="linear:1.5->0.8",
            alpha_schedule="linear:0.6->0.4",
            learning_rate=2e-5,
            batch_size=16,
            epochs=3,
            capability_focus=["reasoning", "knowledge"],
            curriculum_enabled=True,
            adversarial_enabled=False,
            confidence=0.75
        ),
        DistillationStrategy(
            name="激进蒸馏",
            description="高温快速蒸馏，追求最大能力迁移，有一定风险",
            temperature_schedule="cosine:3.0->0.5",
            alpha_schedule="step:0.9->0.3",
            learning_rate=5e-5,
            batch_size=32,
            epochs=5,
            capability_focus=["reasoning", "style", "creative"],
            curriculum_enabled=True,
            adversarial_enabled=True,
            confidence=0.65
        ),
        DistillationStrategy(
            name="均衡蒸馏",
            description="平衡稳定性和效果，推荐用于大多数场景",
            temperature_schedule="cosine:2.0->0.5",
            alpha_schedule="linear:0.7->0.5",
            learning_rate=3e-5,
            batch_size=24,
            epochs=4,
            capability_focus=["reasoning", "knowledge", "style"],
            curriculum_enabled=True,
            adversarial_enabled=True,
            confidence=0.85
        ),
        DistillationStrategy(
            name="快速蒸馏",
            description="最小配置，用于快速验证",
            temperature_schedule="constant:1.0",
            alpha_schedule="constant:0.5",
            learning_rate=5e-5,
            batch_size=64,
            epochs=1,
            capability_focus=["knowledge"],
            curriculum_enabled=False,
            adversarial_enabled=False,
            confidence=0.60
        )
    ]

    def __init__(self, auto_mode: bool = False):
        self.auto_mode = auto_mode
        self.selected_strategy = None
        self.customizations = {}

    def analyze_task(self, task_description: str, data_stats: Dict) -> List[DistillationStrategy]:
        """分析任务特征，推荐排序策略"""

        # 基于任务描述和数据特征排序
        scored_strategies = []

        for strategy in self.DEFAULT_STRATEGIES:
            score = strategy.confidence

            # 根据数据量调整
            data_size = data_stats.get('size', 1000)
            if data_size < 500 and "快速" in strategy.name:
                score += 0.1
            elif data_size > 10000 and "激进" in strategy.name:
                score += 0.1

            # 根据任务类型调整
            if any(kw in task_description.lower() for kw in ['math', 'code', '推理', '逻辑']):
                if "reasoning" in strategy.capability_focus:
                    score += 0.15

            scored_strategies.append((score, strategy))

        # 按分数排序
        scored_strategies.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored_strategies]

    def present_strategy(self, strategy: DistillationStrategy, rank: int) -> str:
        """格式化展示策略"""

        output = f"""
{'='*50}
策略 #{rank}: {strategy.name}
{'='*50}
{strategy.description}

配置详情:
  温度调度: {strategy.temperature_schedule}
  Alpha调度: {strategy.alpha_schedule}
  学习率: {strategy.learning_rate}
  批次大小: {strategy.batch_size}
  训练轮数: {strategy.epochs}
  课程学习: {'开启' if strategy.curriculum_enabled else '关闭'}
  对抗训练: {'开启' if strategy.adversarial_enabled else '关闭'}
  关注能力: {', '.join(strategy.capability_focus)}

系统置信度: {strategy.confidence:.0%}
"""
        return output

    def interactive_select(self, task_description: str, data_stats: Dict,
                          input_callback: Optional[Callable] = None) -> DistillationStrategy:
        """交互式选择策略"""

        # 获取推荐排序
        recommendations = self.analyze_task(task_description, data_stats)

        print("="*60)
        print("🎯 蒸馏策略选择")
        print("="*60)
        print(f"任务: {task_description}")
        print(f"数据: {data_stats.get('size', 'unknown')} 条")
        print()

        # 自动模式
        if self.auto_mode or input_callback is None:
            self.selected_strategy = recommendations[0]
            print(f"自动选择: {self.selected_strategy.name}")
            return self.selected_strategy

        # 展示推荐
        for i, strategy in enumerate(recommendations[:3], 1):
            print(self.present_strategy(strategy, i))

        # 获取用户输入
        print("\n选项:")
        print("  [1-3] 选择对应策略")
        print("  [c]   自定义配置")
        print("  [a]   自动选择（推荐策略）")
        print("  [q]   退出")

        choice = input_callback() if input_callback else input("\n选择: ").strip().lower()

        if choice in ['1', '2', '3']:
            self.selected_strategy = recommendations[int(choice)-1]
        elif choice == 'c':
            self.selected_strategy = self._customize_config(recommendations[0], input_callback)
        elif choice == 'a':
            self.selected_strategy = recommendations[0]
        else:
            raise ValueError("用户取消")

        print(f"\n✅ 已选择: {self.selected_strategy.name}")
        return self.selected_strategy

    def _customize_config(self, base: DistillationStrategy,
                         input_callback: Optional[Callable]) -> DistillationStrategy:
        """自定义配置"""

        print("\n自定义配置 (直接回车保持默认值):")

        def ask(prompt, default):
            val = input_callback() if input_callback else input(f"{prompt} [{default}]: ")
            return type(default)(val) if val.strip() else default

        lr = ask("学习率", base.learning_rate)
        epochs = ask("训练轮数", base.epochs)
        batch = ask("批次大小", base.batch_size)

        return DistillationStrategy(
            name=f"{base.name}(自定义)",
            description=base.description,
            temperature_schedule=base.temperature_schedule,
            alpha_schedule=base.alpha_schedule,
            learning_rate=lr,
            batch_size=batch,
            epochs=epochs,
            capability_focus=base.capability_focus,
            curriculum_enabled=base.curriculum_enabled,
            adversarial_enabled=base.adversarial_enabled,
            confidence=base.confidence * 0.9  # 自定义降低置信度
        )

    def confirm_checkpoint(self, checkpoint_info: Dict,
                          input_callback: Optional[Callable] = None) -> StrategyDecision:
        """检查点确认"""

        print("\n" + "="*60)
        print("⏸️ 检查点确认")
        print("="*60)
        print(f"阶段: {checkpoint_info.get('phase', 'unknown')}")
        print(f"进度: {checkpoint_info.get('progress', 0):.1%}")
        print(f"当前指标: {checkpoint_info.get('metrics', {})}")

        if self.auto_mode:
            return StrategyDecision.AUTO

        print("\n选项: [继续] [调整] [回滚] [停止]")
        choice = input_callback() if input_callback else input("选择: ").strip().lower()

        mapping = {
            '继续': StrategyDecision.APPROVE,
            '调整': StrategyDecision.MODIFY,
            '回滚': StrategyDecision.REJECT,
            '停止': StrategyDecision.REJECT,
            'c': StrategyDecision.APPROVE,
            'm': StrategyDecision.MODIFY,
            'r': StrategyDecision.REJECT,
            's': StrategyDecision.REJECT,
        }

        return mapping.get(choice, StrategyDecision.APPROVE)

    def save_strategy(self, output_path: str):
        """保存策略到文件"""
        if self.selected_strategy:
            with open(output_path, 'w') as f:
                yaml.dump(asdict(self.selected_strategy), f, allow_unicode=True)
            print(f"策略已保存: {output_path}")


def create_interactive_workflow():
    """创建交互式工作流配置"""

    workflow = {
        "checkpoints": [
            {
                "phase": "data_preparation",
                "description": "数据准备完成，确认数据质量和分布",
                "auto_skip_if": "data_quality > 0.9"
            },
            {
                "phase": "teacher_analysis",
                "description": "教师模型分析完成，确认蒸馏可行性",
                "auto_skip_if": "distillability_score > 0.7"
            },
            {
                "phase": "curriculum_generation",
                "description": "课程数据生成完成，确认难度分布",
                "auto_skip_if": None
            },
            {
                "phase": "training_start",
                "description": "训练配置确认，开始蒸馏",
                "auto_skip_if": None
            },
            {
                "phase": "mid_training",
                "description": "训练中期评估，确认训练方向",
                "auto_skip_if": "loss_trend == 'decreasing'"
            },
            {
                "phase": "evaluation",
                "description": "评估完成，确认部署",
                "auto_skip_if": "retention_rate > 0.8"
            }
        ],
        "interaction_modes": {
            "fully_auto": "全自动，仅异常时暂停",
            "semi_auto": "半自动，检查点暂停",
            "fully_manual": "全手动，每步确认"
        }
    }

    return workflow


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default="数学推理任务蒸馏")
    parser.add_argument("--data-size", type=int, default=1000)
    parser.add_argument("--auto", action="store_true")
    parser.add_argument("--output", default="outputs/strategy.yaml")
    args = parser.parse_args()

    selector = InteractiveStrategySelector(auto_mode=args.auto)

    data_stats = {"size": args.data_size}
    strategy = selector.interactive_select(args.task, data_stats)
    selector.save_strategy(args.output)
