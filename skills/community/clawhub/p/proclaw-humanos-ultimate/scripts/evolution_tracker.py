#!/usr/bin/env python3
"""
演化追踪：人格演化的动态追踪系统
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class EvolutionTracker:
    """演化追踪器"""

    # 演化阶段
    EVOLUTION_STAGES = [
        'emergence',           # 萌发
        'differentiation',     # 分化
        'integration',         # 整合
        'transcendence',       # 超越
        'actualization'        # 实现
    ]

    # 演化指标
    EVOLUTION_METRICS = [
        'complexity',          # 复杂度
        'coherence',           # 一致性
        'adaptability',        # 适应性
        'mastery',             # 掌握度
        'integration_level'    # 整合水平
    ]

    def __init__(self):
        self.evolution_history = []
        self.milestones = {}

    def track_evolution(self, base_state: Dict,
                       new_state: Dict,
                       timestamp: str = None) -> Dict:
        """追踪演化状态"""

        if timestamp is None:
            timestamp = str(datetime.now())

        evolution_record = {
            'timestamp': timestamp,
            'base_state': self._extract_signature(base_state),
            'new_state': self._extract_signature(new_state),
            'changes': self._analyze_changes(base_state, new_state),
            'metrics': self._calculate_evolution_metrics(base_state, new_state),
            'stage': self._determine_evolution_stage(new_state),
            'insights': self._generate_evolution_insights(base_state, new_state)
        }

        self.evolution_history.append(evolution_record)

        return evolution_record

    def _extract_signature(self, state: Dict) -> Dict:
        """提取状态签名"""

        signature = {
            'overall_score': 0.0,
            'dimensional_scores': {},
            'axis_positions': {},
            'path_progress': {}
        }

        # 提取整体分数
        if 'integrated_profile' in state:
            signature['overall_score'] = state['integrated_profile'].get('integration_level', 0.5)

        # 提取维度分数
        if 'overall_signature' in state:
            signature['overall_score'] = state['overall_signature'].get('composite_score', 0.5)

        # 提取路径进展
        if 'path_progressions' in state:
            for path_name, progression in state['path_progressions'].items():
                total_nodes = progression.get('total_nodes', 1)
                completed_nodes = progression.get('completed_nodes', 0)
                signature['path_progress'][path_name] = completed_nodes / total_nodes

        return signature

    def _analyze_changes(self, base_state: Dict, new_state: Dict) -> Dict:
        """分析状态变化"""

        base_sig = self._extract_signature(base_state)
        new_sig = self._extract_signature(new_state)

        changes = {
            'overall_delta': new_sig['overall_score'] - base_sig['overall_score'],
            'dimensional_deltas': {},
            'axis_shifts': {},
            'path_advancements': {}
        }

        # 计算路径进展变化
        for path_name in set(list(base_sig['path_progress'].keys()) +
                             list(new_sig['path_progress'].keys())):

            base_progress = base_sig['path_progress'].get(path_name, 0.0)
            new_progress = new_sig['path_progress'].get(path_name, 0.0)

            changes['path_advancements'][path_name] = new_progress - base_progress

        # 识别显著变化
        changes['significant_changes'] = self._identify_significant_changes(changes)

        return changes

    def _identify_significant_changes(self, changes: Dict) -> List[str]:
        """识别显著变化"""

        significant = []

        # 整体分数显著变化
        if abs(changes['overall_delta']) > 0.1:
            direction = 'increase' if changes['overall_delta'] > 0 else 'decrease'
            significant.append(f"overall_score_{direction}")

        # 路径进展显著变化
        for path_name, advancement in changes['path_advancements'].items():
            if advancement > 0.2:
                significant.append(f"{path_name}_major_advancement")
            elif advancement < -0.1:
                significant.append(f"{path_name}_regression")

        return significant

    def _calculate_evolution_metrics(self, base_state: Dict,
                                     new_state: Dict) -> Dict:
        """计算演化指标"""

        base_sig = self._extract_signature(base_state)
        new_sig = self._extract_signature(new_state)

        metrics = {}

        # 复杂度：基于路径多样性和维度整合
        metrics['complexity'] = self._calculate_complexity(new_state)

        # 一致性：基于轴间协调性
        metrics['coherence'] = self._calculate_coherence(new_state)

        # 适应性：基于状态变化幅度
        metrics['adaptability'] = min(abs(new_sig['overall_score'] - base_sig['overall_score']) * 5, 1.0)

        # 掌握度：基于路径完成度
        metrics['mastery'] = np.mean(list(new_sig['path_progress'].values())) if new_sig['path_progress'] else 0.5

        # 整合水平
        metrics['integration_level'] = new_sig['overall_score']

        return metrics

    def _calculate_complexity(self, state: Dict) -> float:
        """计算复杂度"""
        # 简化处理：基于路径和维度数量
        complexity = 0.5

        if 'path_progressions' in state:
            complexity += len(state['path_progressions']) * 0.1

        if 'dimensions' in state:
            complexity += len(state['dimensions']) * 0.05

        return min(complexity, 1.0)

    def _calculate_coherence(self, state: Dict) -> float:
        """计算一致性"""
        # 简化处理：基于轴间张力
        coherence = 0.7

        if 'paradox_patterns' in state:
            paradox_count = len(state['paradox_patterns'])
            coherence -= paradox_count * 0.05

        return max(coherence, 0.3)

    def _determine_evolution_stage(self, state: Dict) -> str:
        """确定演化阶段"""

        metrics = self._calculate_evolution_metrics(state, state)

        mastery = metrics.get('mastery', 0.0)
        integration_level = metrics.get('integration_level', 0.0)

        if integration_level < 0.4:
            return 'emergence'
        elif integration_level < 0.6:
            return 'differentiation'
        elif integration_level < 0.75:
            return 'integration'
        elif integration_level < 0.9:
            return 'transcendence'
        else:
            return 'actualization'

    def _generate_evolution_insights(self, base_state: Dict,
                                    new_state: Dict) -> List[str]:
        """生成演化洞察"""

        insights = []

        changes = self._analyze_changes(base_state, new_state)

        # 整体变化洞察
        if changes['overall_delta'] > 0.15:
            insights.append("Significant overall growth detected")
        elif changes['overall_delta'] < -0.1:
            insights.append("Regression observed - attention needed")

        # 路径进展洞察
        for path_name, advancement in changes['path_advancements'].items():
            if advancement > 0.2:
                insights.append(f"Major advancement in {path_name}")
            elif advancement < -0.1:
                insights.append(f"Setback in {path_name}")

        # 演化阶段洞察
        new_stage = self._determine_evolution_stage(new_state)
        base_stage = self._determine_evolution_stage(base_state)

        if new_stage != base_stage:
            insights.append(f"Evolution stage transition: {base_stage} → {new_stage}")

        return insights

    def create_milestone(self, state: Dict, milestone_name: str,
                        description: str = "") -> Dict:
        """创建演化里程碑"""

        timestamp = str(datetime.now())

        milestone = {
            'milestone_id': len(self.milestones) + 1,
            'timestamp': timestamp,
            'name': milestone_name,
            'description': description,
            'state_signature': self._extract_signature(state),
            'stage': self._determine_evolution_stage(state),
            'metrics': self._calculate_evolution_metrics(state, state)
        }

        self.milestones[milestone_name] = milestone

        return milestone

    def generate_evolution_report(self) -> Dict:
        """生成演化报告"""

        if not self.evolution_history:
            return {
                'status': 'no_data',
                'message': 'No evolution history available'
            }

        report = {
            'summary': self._generate_summary(),
            'timeline': self._generate_timeline(),
            'stage_progression': self._analyze_stage_progression(),
            'metric_trends': self._analyze_metric_trends(),
            'milestones': list(self.milestones.values()),
            'recommendations': self._generate_recommendations()
        }

        return report

    def _generate_summary(self) -> Dict:
        """生成摘要"""

        if not self.evolution_history:
            return {}

        first_record = self.evolution_history[0]
        last_record = self.evolution_history[-1]

        return {
            'total_records': len(self.evolution_history),
            'time_span': {
                'start': first_record['timestamp'],
                'end': last_record['timestamp']
            },
            'overall_change': last_record['changes']['overall_delta'],
            'current_stage': last_record['stage'],
            'total_milestones': len(self.milestones)
        }

    def _generate_timeline(self) -> List[Dict]:
        """生成时间线"""
        return [
            {
                'timestamp': record['timestamp'],
                'stage': record['stage'],
                'overall_score': record['new_state']['overall_score'],
                'significant_changes': record['changes']['significant_changes']
            }
            for record in self.evolution_history
        ]

    def _analyze_stage_progression(self) -> Dict:
        """分析阶段进展"""

        stage_sequence = [record['stage'] for record in self.evolution_history]

        # 计算阶段停留时间
        stage_durations = {}
        current_stage = None
        stage_start = None

        for i, stage in enumerate(stage_sequence):
            if stage != current_stage:
                if current_stage:
                    duration = i - stage_start
                    stage_durations[current_stage] = duration

                current_stage = stage
                stage_start = i

        # 处理最后一个阶段
        if current_stage and current_stage not in stage_durations:
            stage_durations[current_stage] = len(stage_sequence) - stage_start

        return {
            'stage_sequence': stage_sequence,
            'stage_transitions': len(set(stage_sequence)),
            'stage_durations': stage_durations,
            'current_stage': current_stage
        }

    def _analyze_metric_trends(self) -> Dict:
        """分析指标趋势"""

        trends = {}

        for metric in self.EVOLUTION_METRICS:
            metric_values = [
                record['metrics'].get(metric, 0.0)
                for record in self.evolution_history
            ]

            if metric_values:
                trends[metric] = {
                    'initial': metric_values[0],
                    'final': metric_values[-1],
                    'change': metric_values[-1] - metric_values[0],
                    'trend': 'increasing' if metric_values[-1] > metric_values[0] else 'decreasing',
                    'volatility': np.std(metric_values) if len(metric_values) > 1 else 0.0
                }

        return trends

    def _generate_recommendations(self) -> List[str]:
        """生成建议"""

        recommendations = []

        if not self.evolution_history:
            return recommendations

        last_record = self.evolution_history[-1]
        current_stage = last_record['stage']

        # 基于当前阶段的建议
        stage_recommendations = {
            'emergence': [
                "Focus on self-awareness and exploration",
                "Experiment with different approaches",
                "Identify core strengths and interests"
            ],
            'differentiation': [
                "Develop distinct capabilities",
                "Specialize in chosen areas",
                "Build foundational skills"
            ],
            'integration': [
                "Connect different aspects of self",
                "Find synergies between strengths",
                "Create cohesive personal framework"
            ],
            'transcendence': [
                "Push beyond current boundaries",
                "Integrate higher perspectives",
                "Embrace transformative experiences"
            ],
            'actualization': [
                "Live in alignment with true self",
                "Share unique contributions",
                "Mentor and guide others"
            ]
        }

        recommendations.extend(stage_recommendations.get(current_stage, []))

        # 基于趋势的建议
        metric_trends = self._analyze_metric_trends()

        for metric, trend in metric_trends.items():
            if trend['change'] < -0.1:
                recommendations.append(f"Address decline in {metric}")

        return recommendations

    def export_evolution_data(self, output_path: Path):
        """导出演化数据"""

        data = {
            'evolution_history': self.evolution_history,
            'milestones': self.milestones,
            'report': self.generate_evolution_report()
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='演化追踪')
    parser.add_argument('--base-state', type=str, required=True,
                       help='基础状态文件路径 (JSON)')
    parser.add_argument('--new-state', type=str, required=True,
                       help='新状态文件路径 (JSON)')
    parser.add_argument('--report', action='store_true',
                       help='生成演化报告')

    args = parser.parse_args()

    # 读取状态文件
    with open(args.base_state, 'r', encoding='utf-8') as f:
        base_state = json.load(f)

    with open(args.new_state, 'r', encoding='utf-8') as f:
        new_state = json.load(f)

    # 追踪演化
    tracker = EvolutionTracker()
    evolution_record = tracker.track_evolution(base_state, new_state)

    print(json.dumps(evolution_record, ensure_ascii=False, indent=2))

    # 生成报告
    if args.report:
        report = tracker.generate_evolution_report()
        print("\n=== Evolution Report ===")
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
