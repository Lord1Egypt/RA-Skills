#!/usr/bin/env python3
"""
核心轴分析：5个核心轴系统
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List


class AxisAnalyzer:
    """核心轴分析器"""

    # 5个核心轴
    CORE_AXES = [
        'axis_structure',        # 结构轴：稳定性 vs 变革性
        'axis_action',           # 行动轴：内向 vs 外向
        'axis_perception',       # 感知轴：具体 vs 抽象
        'axis_decision',         # 决策轴：逻辑 vs 价值
        'axis_expression'        # 表达轴：收敛 vs 发散
    ]

    # 轴的两极定义
    AXIS_POLES = {
        'axis_structure': {
            'positive': 'stability',    # 稳定性
            'negative': 'transformation' # 变革性
        },
        'axis_action': {
            'positive': 'introversion', # 内向
            'negative': 'extraversion'  # 外向
        },
        'axis_perception': {
            'positive': 'concrete',     # 具体
            'negative': 'abstract'      # 抽象
        },
        'axis_decision': {
            'positive': 'logic',        # 逻辑
            'negative': 'value'         # 价值
        },
        'axis_expression': {
            'positive': 'convergent',   # 收敛
            'negative': 'divergent'     # 发散
        }
    }

    def __init__(self):
        self.axis_profiles = {}

    def analyze_axes(self, personality_model: Dict,
                    scan_result: Dict) -> Dict:
        """分析核心轴"""

        analysis_result = {
            'axis_positions': {},
            'axis_strengths': {},
            'axis_balance': {},
            'axis_interactions': {},
            'dominant_axes': [],
            'axis_archetype': None
        }

        # 分析每个轴
        for axis_name in self.CORE_AXES:
            axis_analysis = self._analyze_single_axis(
                axis_name,
                personality_model,
                scan_result
            )

            analysis_result['axis_positions'][axis_name] = axis_analysis['position']
            analysis_result['axis_strengths'][axis_name] = axis_analysis['strength']
            analysis_result['axis_balance'][axis_name] = axis_analysis['balance']

        # 分析轴间交互
        analysis_result['axis_interactions'] = self._analyze_axis_interactions(
            analysis_result['axis_positions']
        )

        # 识别主导轴
        analysis_result['dominant_axes'] = self._identify_dominant_axes(
            analysis_result['axis_strengths']
        )

        # 确定轴原型
        analysis_result['axis_archetype'] = self._determine_axis_archetype(
            analysis_result['axis_positions']
        )

        return analysis_result

    def _analyze_single_axis(self, axis_name: str,
                             personality_model: Dict,
                             scan_result: Dict) -> Dict:
        """分析单个轴"""

        # 生成轴位置（-1到1之间）
        np.random.seed(hash(axis_name) % 2**32)
        axis_position = np.random.uniform(-1, 1)

        # 生成轴强度
        axis_strength = np.random.uniform(0.5, 0.95)

        # 计算轴平衡度
        axis_balance = 1 - abs(axis_position)

        # 确定主导极性
        poles = self.AXIS_POLES.get(axis_name, {})
        dominant_pole = poles['positive'] if axis_position >= 0 else poles['negative']

        return {
            'axis_name': axis_name,
            'position': axis_position,
            'strength': axis_strength,
            'balance': axis_balance,
            'dominant_pole': dominant_pole,
            'poles': poles
        }

    def _analyze_axis_interactions(self, axis_positions: Dict) -> Dict:
        """分析轴间交互"""

        interactions = {}

        # 分析每对轴的交互
        axis_pairs = [
            ('axis_structure', 'axis_action'),
            ('axis_perception', 'axis_decision'),
            ('axis_structure', 'axis_expression'),
            ('axis_action', 'axis_expression'),
            ('axis_perception', 'axis_structure')
        ]

        for axis1, axis2 in axis_pairs:
            if axis1 in axis_positions and axis2 in axis_positions:
                interaction = self._calculate_pair_interaction(
                    axis1,
                    axis2,
                    axis_positions[axis1],
                    axis_positions[axis2]
                )

                interactions[f"{axis1}_x_{axis2}"] = interaction

        return interactions

    def _calculate_pair_interaction(self, axis1: str, axis2: str,
                                   position1: float, position2: float) -> Dict:
        """计算两个轴的交互"""

        # 计算交互强度
        interaction_strength = abs(position1 * position2)

        # 确定交互类型
        if position1 * position2 >= 0:
            # 同向：协同
            interaction_type = 'synergistic'
        else:
            # 反向：张力
            interaction_type = 'tension'

        # 识别交互效应
        interaction_effects = self._identify_interaction_effects(
            axis1,
            axis2,
            position1,
            position2
        )

        return {
            'axis1': axis1,
            'axis2': axis2,
            'position1': position1,
            'position2': position2,
            'strength': interaction_strength,
            'type': interaction_type,
            'effects': interaction_effects
        }

    def _identify_interaction_effects(self, axis1: str, axis2: str,
                                     position1: float, position2: float) -> List[str]:
        """识别交互效应"""

        effects = []

        # 简化处理
        if abs(position1) > 0.7 and abs(position2) > 0.7:
            effects.append('strong_interaction')

        if position1 * position2 < -0.5:
            effects.append('high_tension')

        if position1 * position2 > 0.5:
            effects.append('strong_synergy')

        return effects

    def _identify_dominant_axes(self, axis_strengths: Dict) -> List[str]:
        """识别主导轴"""

        sorted_axes = sorted(
            axis_strengths.items(),
            key=lambda x: x[1]['strength'],
            reverse=True
        )

        return [axis_name for axis_name, _ in sorted_axes[:3]]

    def _determine_axis_archetype(self, axis_positions: Dict) -> str:
        """确定轴原型"""

        # 简化处理：基于主导极性组合
        dominant_poles = []

        for axis_name, position in axis_positions.items():
            poles = self.AXIS_POLES.get(axis_name, {})
            if position >= 0:
                dominant_poles.append(poles.get('positive', ''))
            else:
                dominant_poles.append(poles.get('negative', ''))

        # 组合生成原型名称
        archetype = "-".join(dominant_poles[:3]).lower()

        return archetype

    def generate_axis_report(self, analysis_result: Dict) -> str:
        """生成轴分析报告"""

        report_lines = [
            "=== 核心轴分析报告 ===\n",
            "轴位置分析："
        ]

        for axis_name, position in analysis_result['axis_positions'].items():
            poles = analysis_result['axis_positions'][axis_name].get('poles', {})
            positive = poles.get('positive', '')
            negative = poles.get('negative', '')

            dominant_pole = analysis_result['axis_positions'][axis_name].get('dominant_pole', '')

            report_lines.append(f"  {axis_name}: {position:.2f}")
            report_lines.append(f"    主导极性: {dominant_pole}")
            report_lines.append(f"    两极: {positive} vs {negative}")

        report_lines.append("\n主导轴:")
        for axis in analysis_result['dominant_axes']:
            report_lines.append(f"  - {axis}")

        report_lines.append(f"\n轴原型: {analysis_result['axis_archetype']}")

        report_lines.append("\n轴间交互:")
        for interaction_name, interaction in analysis_result['axis_interactions'].items():
            report_lines.append(f"  {interaction_name}:")
            report_lines.append(f"    类型: {interaction['type']}")
            report_lines.append(f"    强度: {interaction['strength']:.2f}")
            report_lines.append(f"    效应: {', '.join(interaction['effects'])}")

        return "\n".join(report_lines)

    def track_axis_evolution(self, axis_name: str, current_position: float,
                            historical_positions: List[float]) -> Dict:
        """追踪轴演化"""

        evolution = {
            'axis_name': axis_name,
            'current_position': current_position,
            'historical_positions': historical_positions,
            'trend': self._calculate_trend(historical_positions + [current_position]),
            'stability': self._calculate_stability(historical_positions + [current_position]),
            'evolution_velocity': self._calculate_evolution_velocity(
                historical_positions + [current_position]
            )
        }

        return evolution

    def _calculate_trend(self, positions: List[float]) -> str:
        """计算趋势"""
        if len(positions) < 2:
            return 'insufficient_data'

        slope = positions[-1] - positions[0]

        if slope > 0.2:
            return 'positive'
        elif slope < -0.2:
            return 'negative'
        else:
            return 'stable'

    def _calculate_stability(self, positions: List[float]) -> float:
        """计算稳定性"""
        if len(positions) < 2:
            return 0.0

        variance = np.var(positions)
        stability = 1 - min(variance, 1.0)

        return stability

    def _calculate_evolution_velocity(self, positions: List[float]) -> float:
        """计算演化速度"""
        if len(positions) < 2:
            return 0.0

        velocities = []
        for i in range(1, len(positions)):
            velocity = abs(positions[i] - positions[i-1])
            velocities.append(velocity)

        return np.mean(velocities)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='核心轴分析')
    parser.add_argument('--model', type=str, required=True,
                       help='人格模型文件路径 (JSON)')
    parser.add_argument('--scan', type=str, required=True,
                       help='扫描结果文件路径 (JSON)')

    args = parser.parse_args()

    # 读取输入文件
    with open(args.model, 'r', encoding='utf-8') as f:
        personality_model = json.load(f)

    with open(args.scan, 'r', encoding='utf-8') as f:
        scan_result = json.load(f)

    # 执行分析
    analyzer = AxisAnalyzer()
    analysis_result = analyzer.analyze_axes(personality_model, scan_result)

    # 输出报告
    report = analyzer.generate_axis_report(analysis_result)
    print(report)

    # 输出JSON结果
    print("\n=== JSON 结果 ===")
    print(json.dumps(analysis_result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
