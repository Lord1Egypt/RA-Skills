#!/usr/bin/env python3
"""
路径映射：3条核心路径和节点系统
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List


class PathMapper:
    """路径映射器"""

    # 3条核心路径
    CORE_PATHS = [
        'path_hero',           # 英雄之路
        'path_creator',        # 创造者之路
        'path_wisdom'          # 智慧之路
    ]

    # 每条路径的核心节点
    PATH_NODES = {
        'path_hero': [
            'call_to_adventure',    # 召唤
            'threshold_crossing',   # 跨越门槛
            'trials_and_challenges', # 试炼与挑战
            'abyss_confrontation',  # 深渊对抗
            'transformation',       # 转化
            'return_with_gift'      # 携礼回归
        ],
        'path_creator': [
            'conception',           # 构思
            'incubation',           # 孕育
            'manifestation',        # 显化
            'refinement',           # 精炼
            'actualization',        # 实现
            'contribution'          # 贡献
        ],
        'path_wisdom': [
            'seeking',              # 寻求
            'learning',             # 学习
            'integration',          # 整合
            'realization',          # 领悟
            'transcendence',        # 超越
            'teaching'              # 传授
        ]
    }

    # 节点权重（默认）
    NODE_WEIGHTS = {
        'call_to_adventure': 0.2,
        'threshold_crossing': 0.15,
        'trials_and_challenges': 0.2,
        'abyss_confrontation': 0.15,
        'transformation': 0.15,
        'return_with_gift': 0.15
    }

    def __init__(self):
        self.path_mappings = {}

    def map_personality_to_paths(self, personality_model: Dict) -> Dict:
        """将人格模型映射到路径"""

        mapping_result = {
            'personality_signature': personality_model.get('integrated_profile', {}),
            'path_affinities': {},
            'primary_path': None,
            'secondary_path': None,
            'path_progressions': {},
            'recommended_journey': []
        }

        # 计算每条路径的亲和度
        for path_name in self.CORE_PATHS:
            affinity = self._calculate_path_affinity(path_name, personality_model)
            mapping_result['path_affinities'][path_name] = affinity

        # 确定主路径和次路径
        sorted_paths = sorted(
            mapping_result['path_affinities'].items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )

        if sorted_paths:
            mapping_result['primary_path'] = sorted_paths[0][0]
            mapping_result['secondary_path'] = sorted_paths[1][0] if len(sorted_paths) > 1 else None

        # 计算路径进展
        for path_name in self.CORE_PATHS:
            progression = self._calculate_path_progression(
                path_name,
                personality_model
            )
            mapping_result['path_progressions'][path_name] = progression

        # 生成推荐旅程
        mapping_result['recommended_journey'] = self._generate_recommended_journey(
            mapping_result
        )

        return mapping_result

    def _calculate_path_affinity(self, path_name: str,
                                 personality_model: Dict) -> Dict:
        """计算路径亲和度"""
        # 简化处理：随机生成亲和度分数
        np.random.seed(hash(path_name) % 2**32)

        affinity_score = np.random.uniform(0.5, 0.95)

        # 识别关键节点
        key_nodes = self.PATH_NODES.get(path_name, [])

        # 计算每个节点的完成度
        node_completions = {}
        for node in key_nodes:
            node_completions[node] = np.random.uniform(0.0, 1.0)

        # 计算整体完成度
        overall_completion = np.mean(list(node_completions.values()))

        return {
            'score': affinity_score,
            'completion': overall_completion,
            'key_nodes': key_nodes,
            'node_completions': node_completions,
            'alignment_factors': self._identify_alignment_factors(path_name)
        }

    def _identify_alignment_factors(self, path_name: str) -> List[str]:
        """识别对齐因素"""

        alignment_factors = {
            'path_hero': ['courage', 'resilience', 'transformation', 'purpose'],
            'path_creator': ['innovation', 'expression', 'craftsmanship', 'impact'],
            'path_wisdom': ['curiosity', 'insight', 'integration', 'teaching']
        }

        return alignment_factors.get(path_name, [])

    def _calculate_path_progression(self, path_name: str,
                                    personality_model: Dict) -> Dict:
        """计算路径进展"""

        nodes = self.PATH_NODES.get(path_name, [])

        progression = {
            'path_name': path_name,
            'total_nodes': len(nodes),
            'completed_nodes': 0,
            'current_node': None,
            'next_node': None,
            'node_sequence': []
        }

        # 随机确定当前位置
        np.random.seed(hash(f"{path_name}_progression") % 2**32)
        current_index = np.random.randint(0, len(nodes))

        progression['current_node'] = nodes[current_index]
        progression['next_node'] = nodes[current_index + 1] if current_index < len(nodes) - 1 else None
        progression['completed_nodes'] = current_index

        # 生成节点序列
        for i, node in enumerate(nodes):
            is_completed = i < current_index
            is_current = i == current_index
            progression['node_sequence'].append({
                'node_name': node,
                'position': i,
                'status': 'completed' if is_completed else 'current' if is_current else 'future'
            })

        return progression

    def _generate_recommended_journey(self, mapping_result: Dict) -> List[Dict]:
        """生成推荐旅程"""

        primary_path = mapping_result.get('primary_path')
        if not primary_path:
            return []

        progression = mapping_result['path_progressions'].get(primary_path, {})
        current_node = progression.get('current_node')
        next_node = progression.get('next_node')

        journey = []

        # 当前阶段
        if current_node:
            journey.append({
                'phase': 'current',
                'path': primary_path,
                'node': current_node,
                'focus': f"Focus on mastering {current_node}",
                'recommended_actions': self._generate_node_actions(current_node, 'current')
            })

        # 下一步
        if next_node:
            journey.append({
                'phase': 'next',
                'path': primary_path,
                'node': next_node,
                'focus': f"Prepare for {next_node}",
                'recommended_actions': self._generate_node_actions(next_node, 'next')
            })

        # 融合次路径的洞察
        secondary_path = mapping_result.get('secondary_path')
        if secondary_path:
            journey.append({
                'phase': 'integration',
                'path': secondary_path,
                'node': 'cross_path_learning',
                'focus': f"Integrate insights from {secondary_path}",
                'recommended_actions': [
                    "Identify complementary practices",
                    "Seek dual-path mentorship",
                    "Create integration rituals"
                ]
            })

        return journey

    def _generate_node_actions(self, node: str, phase: str) -> List[str]:
        """生成节点行动建议"""

        actions_map = {
            'call_to_adventure': ['Listen for inner calling', 'Identify life direction', 'Commit to journey'],
            'threshold_crossing': ['Embrace change', 'Leave comfort zone', 'Cross symbolic boundary'],
            'trials_and_challenges': ['Build resilience', 'Face obstacles', 'Learn from failures'],
            'abyss_confrontation': ['Face deepest fears', 'Surrender to transformation', 'Embrace death and rebirth'],
            'transformation': ['Integrate lessons', 'Embody new self', 'Release old identity'],
            'return_with_gift': ['Share insights', 'Serve community', 'Mentor others']
        }

        actions = actions_map.get(node, ['Explore', 'Learn', 'Grow'])

        if phase == 'next':
            return [f"Prepare for: {action}" for action in actions]

        return actions

    def track_journey_progress(self, path_name: str, current_node: str,
                               achievements: List[str]) -> Dict:
        """追踪旅程进展"""

        tracking = {
            'path_name': path_name,
            'current_node': current_node,
            'achievements': achievements,
            'milestones_reached': len(achievements),
            'next_milestone': self._get_next_milestone(path_name, current_node),
            'overall_progress': self._calculate_overall_progress(
                path_name,
                current_node,
                achievements
            )
        }

        return tracking

    def _get_next_milestone(self, path_name: str,
                           current_node: str) -> str:
        """获取下一个里程碑"""
        nodes = self.PATH_NODES.get(path_name, [])

        try:
            current_index = nodes.index(current_node)
            if current_index < len(nodes) - 1:
                return nodes[current_index + 1]
        except ValueError:
            pass

        return "journey_complete"

    def _calculate_overall_progress(self, path_name: str,
                                    current_node: str,
                                    achievements: List[str]) -> float:
        """计算总体进展"""
        nodes = self.PATH_NODES.get(path_name, [])

        try:
            current_index = nodes.index(current_node)
            node_progress = (current_index + 1) / len(nodes)

            achievement_factor = min(len(achievements) / len(nodes), 1.0)

            overall_progress = (node_progress + achievement_factor) / 2

            return overall_progress

        except ValueError:
            return 0.0


def main():
    import argparse

    parser = argparse.ArgumentParser(description='路径映射')
    parser.add_argument('--model', type=str, required=True,
                       help='人格模型文件路径 (JSON)')

    args = parser.parse_args()

    # 读取人格模型
    model_path = Path(args.model)
    with open(model_path, 'r', encoding='utf-8') as f:
        personality_model = json.load(f)

    # 执行映射
    mapper = PathMapper()
    mapping_result = mapper.map_personality_to_paths(personality_model)

    print(json.dumps(mapping_result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
