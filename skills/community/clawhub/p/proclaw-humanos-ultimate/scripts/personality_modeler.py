#!/usr/bin/env python3
"""
7层人格建模：全息人格模型构建
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List


class PersonalityModeler:
    """7层人格建模器"""

    # 7层定义
    LAYERS = [
        'layer0_prototype',      # 层0: 原型
        'layer1_zodiac',         # 层1: 星座
        'layer2_cognitive',      # 层2: 认知
        'layer3_emotional',      # 层3: 情感
        'layer4_behavioral',     # 层4: 行为
        'layer5_social',         # 层5: 社交
        'layer6_integration'     # 层6: 整合
    ]

    def __init__(self):
        self.layer_models = {}

    def build_model(self, zodiac_prototype: Dict, scan_result: Dict,
                   personal_data: Dict) -> Dict:
        """构建7层人格模型"""

        model = {
            'metadata': {
                'zodiac_sign': zodiac_prototype.get('sign'),
                'created_at': str(np.datetime64('now')),
                'total_layers': len(self.LAYERS)
            },
            'layers': {}
        }

        # 构建每一层
        for i, layer_name in enumerate(self.LAYERS):
            model['layers'][layer_name] = self._build_layer(
                layer_name,
                i,
                zodiac_prototype,
                scan_result,
                personal_data
            )

        # 计算层间交互
        model['layer_interactions'] = self._calculate_layer_interactions(
            model['layers']
        )

        # 识别核心模式
        model['core_patterns'] = self._identify_core_patterns(
            model['layers']
        )

        # 生成整合画像
        model['integrated_profile'] = self._generate_integrated_profile(
            model['layers']
        )

        return model

    def _build_layer(self, layer_name: str, layer_index: int,
                     zodiac_prototype: Dict, scan_result: Dict,
                     personal_data: Dict) -> Dict:
        """构建单层模型"""

        layer_model = {
            'layer_id': layer_index,
            'layer_name': layer_name,
            'content': {},
            'weights': {},
            'activation_patterns': {}
        }

        # 根据层级不同构建内容
        if layer_name == 'layer0_prototype':
            layer_model['content'] = self._build_prototype_layer(
                zodiac_prototype
            )

        elif layer_name == 'layer1_zodiac':
            layer_model['content'] = self._build_zodiac_layer(
                zodiac_prototype,
                scan_result
            )

        elif layer_name in ['layer2_cognitive', 'layer3_emotional']:
            layer_model['content'] = self._build_cognitive_emotional_layer(
                layer_name,
                scan_result
            )

        elif layer_name in ['layer4_behavioral', 'layer5_social']:
            layer_model['content'] = self._build_behavioral_social_layer(
                layer_name,
                scan_result,
                personal_data
            )

        elif layer_name == 'layer6_integration':
            layer_model['content'] = self._build_integration_layer(
                layer_index,
                scan_result
            )

        # 计算权重
        layer_model['weights'] = self._calculate_layer_weights(
            layer_index,
            layer_model['content']
        )

        # 识别激活模式
        layer_model['activation_patterns'] = self._identify_activation_patterns(
            layer_model['content']
        )

        return layer_model

    def _build_prototype_layer(self, zodiac_prototype: Dict) -> Dict:
        """构建原型层"""
        return {
            'archetype': zodiac_prototype.get('sign'),
            'symbol': zodiac_prototype.get('info', {}).get('symbol'),
            'element': zodiac_prototype.get('info', {}).get('element'),
            'mode': zodiac_prototype.get('info', {}).get('mode'),
            'ruling_planet': zodiac_prototype.get('info', {}).get('ruling_planet'),
            'core_drive': zodiac_prototype.get('core_drive', ''),
            'cognitive_filter': zodiac_prototype.get('cognitive_filter', '')
        }

    def _build_zodiac_layer(self, zodiac_prototype: Dict,
                           scan_result: Dict) -> Dict:
        """构建星座层"""
        return {
            'zodiac_sign': zodiac_prototype.get('sign'),
            'element_expression': zodiac_prototype.get('info', {}).get('element'),
            'mode_expression': zodiac_prototype.get('info', {}).get('mode'),
            'planetary_influence': zodiac_prototype.get('info', {}).get('ruling_planet'),
            'dimensional_signature': self._extract_dimensional_signature(scan_result)
        }

    def _extract_dimensional_signature(self, scan_result: Dict) -> Dict:
        """提取维度特征"""
        if 'dimensions' not in scan_result:
            return {}

        signature = {}
        for dim_name, dim_info in scan_result['dimensions'].items():
            signature[dim_name] = dim_info['scores']['raw_score']

        return signature

    def _build_cognitive_emotional_layer(self, layer_name: str,
                                         scan_result: Dict) -> Dict:
        """构建认知/情感层"""
        base_dim = layer_name.split('_')[1]

        if base_dim not in scan_result.get('dimensions', {}):
            return {}

        dim_info = scan_result['dimensions'][base_dim]

        return {
            'primary_function': f"{base_dim}_processing",
            'dominant_traits': dim_info.get('primary_traits', []),
            'developmental_level': dim_info.get('developmental_level', ''),
            'integration_degree': dim_info.get('integration_degree', 0),
            'activation_patterns': self._extract_activation_patterns(
                dim_info['scores']
            )
        }

    def _extract_activation_patterns(self, scores: Dict) -> List[str]:
        """提取激活模式"""
        patterns = []

        if scores['raw_score'] >= 9:
            patterns.append('high_activation')
        elif scores['raw_score'] >= 7:
            patterns.append('moderate_activation')
        else:
            patterns.append('low_activation')

        if scores['stability'] >= 0.8:
            patterns.append('stable')

        if scores['flexibility'] >= 0.8:
            patterns.append('flexible')

        return patterns

    def _build_behavioral_social_layer(self, layer_name: str,
                                       scan_result: Dict,
                                       personal_data: Dict) -> Dict:
        """构建行为/社交层"""
        base_dim = layer_name.split('_')[1]

        if base_dim not in scan_result.get('dimensions', {}):
            return {}

        dim_info = scan_result['dimensions'][base_dim]

        return {
            'expression_style': f"{base_dim}_style",
            'interaction_patterns': dim_info.get('primary_traits', []),
            'contextual_adaptability': dim_info.get('integration_degree', 0),
            'personalized_aspects': self._extract_personalized_aspects(
                base_dim,
                personal_data
            )
        }

    def _extract_personalized_aspects(self, dimension: str,
                                      personal_data: Dict) -> Dict:
        """提取个性化方面"""
        # 简化处理，实际需要更复杂的分析
        return {
            'customizations': [],
            'preferences': personal_data.get('preferences', {}),
            'constraints': personal_data.get('constraints', {})
        }

    def _build_integration_layer(self, layer_index: int,
                                 scan_result: Dict) -> Dict:
        """构建整合层"""
        return {
            'integration_function': 'layer_coordination',
            'overall_signature': scan_result.get('overall_signature', {}),
            'paradox_patterns': scan_result.get('paradox_patterns', []),
            'core_strengths': scan_result.get('core_strengths', []),
            'blind_spots': scan_result.get('blind_spots', []),
            'evolution_direction': self._identify_evolution_direction(
                scan_result
            )
        }

    def _identify_evolution_direction(self, scan_result: Dict) -> str:
        """识别演化方向"""
        # 简化处理
        strengths = scan_result.get('core_strengths', [])
        blind_spots = scan_result.get('blind_spots', [])

        if not blind_spots:
            return 'mastery'
        elif len(strengths) > len(blind_spots):
            return 'integration'
        else:
            return 'development'

    def _calculate_layer_weights(self, layer_index: int,
                                 content: Dict) -> Dict:
        """计算层级权重"""
        # 简化处理：高层级权重更高
        base_weight = 0.5 + (layer_index / len(self.LAYERS)) * 0.5

        return {
            'base_weight': base_weight,
            'contextual_weights': {},
            'adaptive_adjustments': {}
        }

    def _identify_activation_patterns(self, content: Dict) -> List[str]:
        """识别激活模式"""
        patterns = []

        # 简化处理
        if content:
            patterns.append('active')
            patterns.append('responsive')

        return patterns

    def _calculate_layer_interactions(self, layers: Dict) -> Dict:
        """计算层间交互"""
        interactions = {}

        # 简化处理：每层与相邻层交互
        for i, layer_name in enumerate(self.LAYERS):
            interactions[layer_name] = {
                'upward_interaction': [],
                'downward_interaction': [],
                'lateral_interaction': []
            }

            if i > 0:
                interactions[layer_name]['downward_interaction'].append(self.LAYERS[i-1])
            if i < len(self.LAYERS) - 1:
                interactions[layer_name]['upward_interaction'].append(self.LAYERS[i+1])

        return interactions

    def _identify_core_patterns(self, layers: Dict) -> List[Dict]:
        """识别核心模式"""
        patterns = []

        # 简化处理：从每层提取关键模式
        for layer_name, layer_data in layers.items():
            if layer_data.get('content'):
                patterns.append({
                    'layer': layer_name,
                    'pattern': 'dominant_expression',
                    'description': f"{layer_name}层的主导表达模式"
                })

        return patterns

    def _generate_integrated_profile(self, layers: Dict) -> Dict:
        """生成整合画像"""
        return {
            'personality_type': 'holographic',
            'dominant_layers': list(layers.keys())[:3],
            'overall_complexity': len(layers),
            'integration_level': 0.8,
            'unique_signature': self._generate_unique_signature(layers)
        }

    def _generate_unique_signature(self, layers: Dict) -> str:
        """生成唯一签名"""
        # 简化处理
        return "Holographic-Personality-Signature"


def main():
    import argparse

    parser = argparse.ArgumentParser(description='7层人格建模')
    parser.add_argument('--prototype', type=str, required=True,
                       help='星座原型文件路径 (JSON)')
    parser.add_argument('--scan', type=str, required=True,
                       help='扫描结果文件路径 (JSON)')
    parser.add_argument('--personal', type=str, required=True,
                       help='个人数据文件路径 (JSON)')

    args = parser.parse_args()

    # 读取输入文件
    with open(args.prototype, 'r', encoding='utf-8') as f:
        zodiac_prototype = json.load(f)

    with open(args.scan, 'r', encoding='utf-8') as f:
        scan_result = json.load(f)

    with open(args.personal, 'r', encoding='utf-8') as f:
        personal_data = json.load(f)

    # 构建模型
    modeler = PersonalityModeler()
    model = modeler.build_model(zodiac_prototype, scan_result, personal_data)

    print(json.dumps(model, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
