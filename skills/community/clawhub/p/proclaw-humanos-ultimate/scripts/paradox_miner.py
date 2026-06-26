#!/usr/bin/env python3
"""
矛盾深度挖掘：识别和解析人格矛盾
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List


class ParadoxMiner:
    """矛盾挖掘器"""

    # 矛盾类型
    PARADOX_TYPES = [
        'tension_paradox',      # 张力矛盾
        'shadow_paradox',       # 阴影矛盾
        'integration_paradox',  # 整合矛盾
        'transcendence_paradox' # 超越矛盾
    ]

    # 常见矛盾模式
    COMMON_PARADOXES = {
        'autonomy_vs_connection': '自主性与连接性的矛盾',
        'stability_vs_growth': '稳定性与成长的矛盾',
        'authenticity_vs_adaptation': '真实性与适应性的矛盾',
        'idealism_vs_pragmatism': '理想主义与实用主义的矛盾',
        'expression_vs_privacy': '表达与隐私的矛盾'
    }

    def __init__(self):
        self.paradox_database = {}

    def mine_paradoxes(self, personality_model: Dict,
                      scan_result: Dict,
                      axis_analysis: Dict) -> Dict:
        """挖掘人格矛盾"""

        paradox_result = {
            'identified_paradoxes': [],
            'paradox_depth': {},
            'paradox_impact': {},
            'paradox_integrations': [],
            'paradox_recommendations': []
        }

        # 从扫描结果中识别矛盾
        scan_paradoxes = self._mine_scan_paradoxes(scan_result)
        paradox_result['identified_paradoxes'].extend(scan_paradoxes)

        # 从轴分析中识别矛盾
        axis_paradoxes = self._mine_axis_paradoxes(axis_analysis)
        paradox_result['identified_paradoxes'].extend(axis_paradoxes)

        # 从人格模型中识别矛盾
        model_paradoxes = self._mine_model_paradoxes(personality_model)
        paradox_result['identified_paradoxes'].extend(model_paradoxes)

        # 分析矛盾深度
        for paradox in paradox_result['identified_paradoxes']:
            paradox_id = paradox['paradox_id']
            paradox_result['paradox_depth'][paradox_id] = self._assess_paradox_depth(paradox)
            paradox_result['paradox_impact'][paradox_id] = self._assess_paradox_impact(paradox)

        # 生成矛盾整合方案
        paradox_result['paradox_integrations'] = self._generate_integrations(
            paradox_result['identified_paradoxes']
        )

        # 生成建议
        paradox_result['paradox_recommendations'] = self._generate_recommendations(
            paradox_result['identified_paradoxes'],
            paradox_result['paradox_integrations']
        )

        return paradox_result

    def _mine_scan_paradoxes(self, scan_result: Dict) -> List[Dict]:
        """从扫描结果中挖掘矛盾"""

        paradoxes = []

        if 'paradox_patterns' in scan_result:
            for pattern in scan_result['paradox_patterns']:
                paradox = {
                    'paradox_id': f"scan_{pattern['type']}",
                    'type': pattern['type'],
                    'tension': pattern.get('tension', 0.0),
                    'higher_dimension': pattern.get('higher_dimension'),
                    'lower_dimension': pattern.get('lower_dimension'),
                    'description': pattern.get('description', ''),
                    'source': 'scan'
                }

                paradoxes.append(paradox)

        return paradoxes

    def _mine_axis_paradoxes(self, axis_analysis: Dict) -> List[Dict]:
        """从轴分析中挖掘矛盾"""

        paradoxes = []

        if 'axis_interactions' in axis_analysis:
            for interaction_name, interaction in axis_analysis['axis_interactions'].items():
                if interaction.get('type') == 'tension':
                    paradox = {
                        'paradox_id': f"axis_{interaction_name}",
                        'type': 'axis_tension',
                        'tension': interaction.get('strength', 0.0),
                        'axis1': interaction.get('axis1'),
                        'axis2': interaction.get('axis2'),
                        'position1': interaction.get('position1'),
                        'position2': interaction.get('position2'),
                        'description': f"张力矛盾: {interaction.get('axis1')} vs {interaction.get('axis2')}",
                        'source': 'axis',
                        'effects': interaction.get('effects', [])
                    }

                    paradoxes.append(paradox)

        return paradoxes

    def _mine_model_paradoxes(self, personality_model: Dict) -> List[Dict]:
        """从人格模型中挖掘矛盾"""

        paradoxes = []

        # 检查层级间的矛盾
        if 'layer_interactions' in personality_model:
            for layer_name, interactions in personality_model['layer_interactions'].items():
                # 简化处理：识别潜在矛盾
                upward = interactions.get('upward_integration', [])
                downward = interactions.get('downward_integration', [])

                if upward and downward:
                    paradox = {
                        'paradox_id': f"layer_{layer_name}",
                        'type': 'layer_tension',
                        'tension': 0.6,  # 默认值
                        'layer': layer_name,
                        'upward_connections': upward,
                        'downward_connections': downward,
                        'description': f"层间张力: {layer_name}",
                        'source': 'model'
                    }

                    paradoxes.append(paradox)

        return paradoxes

    def _assess_paradox_depth(self, paradox: Dict) -> Dict:
        """评估矛盾深度"""

        depth = {
            'structural_depth': 0.0,
            'existential_depth': 0.0,
            'emotional_depth': 0.0,
            'overall_depth': 0.0
        }

        # 结构深度：基于张力和复杂性
        tension = paradox.get('tension', 0.0)
        depth['structural_depth'] = tension

        # 存在深度：基于矛盾类型
        paradox_type = paradox.get('type', '')
        if 'shadow' in paradox_type or 'existential' in paradox_type:
            depth['existential_depth'] = 0.8
        elif 'integration' in paradox_type:
            depth['existential_depth'] = 0.6
        else:
            depth['existential_depth'] = 0.4

        # 情感深度：基于来源
        source = paradox.get('source', '')
        if source == 'scan':
            depth['emotional_depth'] = 0.7
        elif source == 'axis':
            depth['emotional_depth'] = 0.5
        else:
            depth['emotional_depth'] = 0.3

        # 总体深度
        depth['overall_depth'] = np.mean([
            depth['structural_depth'],
            depth['existential_depth'],
            depth['emotional_depth']
        ])

        return depth

    def _assess_paradox_impact(self, paradox: Dict) -> Dict:
        """评估矛盾影响"""

        impact = {
            'psychological_impact': 0.0,
            'behavioral_impact': 0.0,
            'developmental_impact': 0.0,
            'overall_impact': 0.0
        }

        tension = paradox.get('tension', 0.0)

        # 心理影响
        impact['psychological_impact'] = tension * 0.8

        # 行为影响
        impact['behavioral_impact'] = tension * 0.7

        # 发展影响
        depth = self._assess_paradox_depth(paradox)
        impact['developmental_impact'] = depth['overall_depth'] * 0.6

        # 总体影响
        impact['overall_impact'] = np.mean([
            impact['psychological_impact'],
            impact['behavioral_impact'],
            impact['developmental_impact']
        ])

        return impact

    def _generate_integrations(self, paradoxes: List[Dict]) -> List[Dict]:
        """生成矛盾整合方案"""

        integrations = []

        for paradox in paradoxes:
            paradox_id = paradox['paradox_id']

            integration = {
                'paradox_id': paradox_id,
                'integration_strategy': self._determine_integration_strategy(paradox),
                'integration_approaches': self._generate_integration_approaches(paradox),
                'integration_potential': self._assess_integration_potential(paradox)
            }

            integrations.append(integration)

        return integrations

    def _determine_integration_strategy(self, paradox: Dict) -> str:
        """确定整合策略"""

        tension = paradox.get('tension', 0.0)

        if tension > 0.8:
            return 'transcendence'
        elif tension > 0.6:
            return 'integration'
        elif tension > 0.4:
            return 'balancing'
        else:
            return 'acknowledgment'

    def _generate_integration_approaches(self, paradox: Dict) -> List[str]:
        """生成整合方法"""

        strategy = self._determine_integration_strategy(paradox)

        approaches_map = {
            'transcendence': [
                "Embrace both poles as complementary aspects",
                "Find higher perspective that transcends duality",
                "Cultivate paradoxical thinking"
            ],
            'integration': [
                "Create synergistic relationship between poles",
                "Identify context where each pole is valuable",
                "Develop dynamic balance based on situation"
            ],
            'balancing': [
                "Maintain equilibrium between poles",
                "Monitor for dominance patterns",
                "Practice conscious shifting"
            ],
            'acknowledgment': [
                "Recognize the existence of tension",
                "Observe patterns without judgment",
                "Allow natural unfolding"
            ]
        }

        return approaches_map.get(strategy, [])

    def _assess_integration_potential(self, paradox: Dict) -> Dict:
        """评估整合潜力"""

        tension = paradox.get('tension', 0.0)

        potential = {
            'ease_of_integration': 1 - tension,
            'creative_potential': tension * 0.8,
            'transformation_potential': tension * 0.9,
            'overall_potential': tension * 0.7
        }

        return potential

    def _generate_recommendations(self, paradoxes: List[Dict],
                                  integrations: List[Dict]) -> List[str]:
        """生成建议"""

        recommendations = []

        # 识别最高影响力的矛盾
        sorted_paradoxes = sorted(
            paradoxes,
            key=lambda p: self._assess_paradox_impact(p)['overall_impact'],
            reverse=True
        )

        if sorted_paradoxes:
            top_paradox = sorted_paradoxes[0]
            paradox_id = top_paradox['paradox_id']

            # 找到对应的整合方案
            integration = next(
                (i for i in integrations if i['paradox_id'] == paradox_id),
                None
            )

            if integration:
                recommendations.append(
                    f"Primary focus: {integration['integration_strategy']} of {top_paradox['type']}"
                )

                for approach in integration['integration_approaches']:
                    recommendations.append(f"  - {approach}")

        # 一般建议
        recommendations.extend([
            "Practice self-observation of paradox patterns",
            "Cultivate tolerance for internal contradictions",
            "Seek contexts where paradoxes can be expressed"
        ])

        return recommendations

    def generate_paradox_report(self, paradox_result: Dict) -> str:
        """生成矛盾报告"""

        report_lines = [
            "=== 人格矛盾深度分析报告 ===\n",
            "识别到的矛盾："
        ]

        for paradox in paradox_result['identified_paradoxes']:
            paradox_id = paradox['paradox_id']
            depth = paradox_result['paradox_depth'][paradox_id]
            impact = paradox_result['paradox_impact'][paradox_id]

            report_lines.append(f"\n{paradox_id}:")
            report_lines.append(f"  类型: {paradox['type']}")
            report_lines.append(f"  描述: {paradox['description']}")
            report_lines.append(f"  深度: {depth['overall_depth']:.2f}")
            report_lines.append(f"  影响: {impact['overall_impact']:.2f}")

        report_lines.append("\n整合方案：")

        for integration in paradox_result['paradox_integrations']:
            paradox_id = integration['paradox_id']
            report_lines.append(f"\n{paradox_id}:")
            report_lines.append(f"  策略: {integration['integration_strategy']}")
            report_lines.append(f"  潜力: {integration['integration_potential']['overall_potential']:.2f}")
            report_lines.append(f"  方法:")
            for approach in integration['integration_approaches']:
                report_lines.append(f"    - {approach}")

        report_lines.append("\n建议：")

        for rec in paradox_result['paradox_recommendations']:
            report_lines.append(f"- {rec}")

        return "\n".join(report_lines)

    def create_paradox_journal(self, paradox_result: Dict,
                              output_path: Path):
        """创建矛盾日志"""

        journal_data = {
            'paradoxes': paradox_result['identified_paradoxes'],
            'depth_analysis': paradox_result['paradox_depth'],
            'impact_analysis': paradox_result['paradox_impact'],
            'integrations': paradox_result['paradox_integrations'],
            'recommendations': paradox_result['paradox_recommendations'],
            'created_at': str(np.datetime64('now'))
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(journal_data, f, ensure_ascii=False, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='矛盾深度挖掘')
    parser.add_argument('--model', type=str, required=True,
                       help='人格模型文件路径 (JSON)')
    parser.add_argument('--scan', type=str, required=True,
                       help='扫描结果文件路径 (JSON)')
    parser.add_argument('--axis', type=str, required=True,
                       help='轴分析文件路径 (JSON)')

    args = parser.parse_args()

    # 读取输入文件
    with open(args.model, 'r', encoding='utf-8') as f:
        personality_model = json.load(f)

    with open(args.scan, 'r', encoding='utf-8') as f:
        scan_result = json.load(f)

    with open(args.axis, 'r', encoding='utf-8') as f:
        axis_analysis = json.load(f)

    # 挖掘矛盾
    miner = ParadoxMiner()
    paradox_result = miner.mine_paradoxes(personality_model, scan_result, axis_analysis)

    # 输出报告
    report = miner.generate_paradox_report(paradox_result)
    print(report)

    # 输出JSON结果
    print("\n=== JSON 结果 ===")
    print(json.dumps(paradox_result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
