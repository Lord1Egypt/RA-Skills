#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
熵减评估脚本

功能：评估决策的熵减效果，计算熵值
用途：当AI Agent需要评估决策的熵减效果时调用
参数：当前状态、目标状态、决策方案
输出：熵值计算、熵减效果评估、建议优化方案
"""

import json
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass
import math


@dataclass
class State:
    """状态定义"""
    name: str
    factors: Dict[str, float]  # 因素名称 -> 因素值 (0-1, 0最有序, 1最混乱)
    structure_score: float  # 结构化程度 (0-1, 0无结构, 1完全结构化)


@dataclass
class EntropyResult:
    """熵减评估结果"""
    current_entropy: float
    target_entropy: float
    entropy_reduction: float
    reduction_percentage: float
    factor_analysis: Dict[str, Any]
    recommendations: List[str]


class EntropyAnalyzer:
    """熵减分析器"""
    
    def __init__(self):
        self.default_factors = {
            'information_clarity': 0.7,  # 信息清晰度
            'process_order': 0.6,  # 流程有序性
            'decision_consistency': 0.5,  # 决策一致性
            'resource_allocation': 0.6,  # 资源分配有序性
            'system_stability': 0.7,  # 系统稳定性
        }
    
    def calculate_entropy(self, state: State) -> float:
        """
        计算状态的熵值
        
        Args:
            state: 状态定义
            
        Returns:
            float: 熵值 (0-1, 0最有序, 1最混乱)
        """
        # 计算各因素的加权熵
        factor_entropy = sum(state.factors.values()) / len(state.factors)
        
        # 结构化程度的反比作为结构熵
        structure_entropy = 1.0 - state.structure_score
        
        # 综合熵值
        total_entropy = 0.6 * factor_entropy + 0.4 * structure_entropy
        
        return min(max(total_entropy, 0.0), 1.0)
    
    def analyze(self, current_state: State, target_state: State, 
                decision_description: str = "") -> EntropyResult:
        """
        分析熵减效果
        
        Args:
            current_state: 当前状态
            target_state: 目标状态
            decision_description: 决策描述
            
        Returns:
            EntropyResult: 熵减评估结果
        """
        # 计算当前熵
        current_entropy = self.calculate_entropy(current_state)
        
        # 计算目标熵
        target_entropy = self.calculate_entropy(target_state)
        
        # 计算熵减
        entropy_reduction = current_entropy - target_entropy
        
        # 计算熵减百分比
        reduction_percentage = (entropy_reduction / current_entropy * 100) if current_entropy > 0 else 0
        
        # 因素分析
        factor_analysis = self._analyze_factors(current_state, target_state)
        
        # 生成建议
        recommendations = self._generate_recommendations(entropy_reduction, factor_analysis)
        
        return EntropyResult(
            current_entropy=current_entropy,
            target_entropy=target_entropy,
            entropy_reduction=entropy_reduction,
            reduction_percentage=reduction_percentage,
            factor_analysis=factor_analysis,
            recommendations=recommendations
        )
    
    def _analyze_factors(self, current: State, target: State) -> Dict[str, Any]:
        """分析各因素的变化"""
        analysis = {}
        
        for factor_name in current.factors:
            current_value = current.factors.get(factor_name, 0.5)
            target_value = target.factors.get(factor_name, 0.5)
            improvement = current_value - target_value
            
            analysis[factor_name] = {
                'current': current_value,
                'target': target_value,
                'improvement': improvement,
                'improvement_percentage': (improvement / current_value * 100) if current_value > 0 else 0,
                'impact': 'high' if improvement > 0.3 else 'medium' if improvement > 0.1 else 'low'
            }
        
        return analysis
    
    def _generate_recommendations(self, entropy_reduction: float, 
                                   factor_analysis: Dict[str, Any]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 总体评估
        if entropy_reduction > 0.5:
            recommendations.append("✓ 该决策能够实现显著的熵减，建议执行")
        elif entropy_reduction > 0.2:
            recommendations.append("✓ 该决策能够实现一定的熵减，建议进一步优化后执行")
        else:
            recommendations.append("✗ 该决策的熵减效果不明显，建议重新考虑")
        
        # 因素优化建议
        high_impact_factors = [
            name for name, data in factor_analysis.items() 
            if data['impact'] == 'high' and data['improvement'] > 0
        ]
        
        if high_impact_factors:
            recommendations.append(f"重点关注以下高影响因素: {', '.join(high_impact_factors)}")
        
        # 一般性建议
        recommendations.extend([
            "每个决策都应该问：这个选择是增加熵还是减少熵？",
            "优先选择能够建立最大秩序的方案",
            "通过结构优化、信息压缩、能量输入实现熵减",
            "主动对抗系统的熵增趋势"
        ])
        
        return recommendations


def create_state_from_dict(state_dict: Dict[str, Any]) -> State:
    """从字典创建状态"""
    return State(
        name=state_dict.get('name', 'unknown'),
        factors=state_dict.get('factors', {}),
        structure_score=state_dict.get('structure_score', 0.5)
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='熵减分析工具')
    parser.add_argument('--current-state', type=str, required=True, help='当前状态 (JSON格式)')
    parser.add_argument('--target-state', type=str, required=True, help='目标状态 (JSON格式)')
    parser.add_argument('--decision', type=str, default='', help='决策描述')
    parser.add_argument('--output', type=str, default='json', choices=['json', 'text'], help='输出格式')
    
    args = parser.parse_args()
    
    # 创建状态
    current_state = create_state_from_dict(json.loads(args.current_state))
    target_state = create_state_from_dict(json.loads(args.target_state))
    
    # 创建分析器
    analyzer = EntropyAnalyzer()
    
    # 执行分析
    result = analyzer.analyze(current_state, target_state, args.decision)
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps({
            'current_entropy': result.current_entropy,
            'target_entropy': result.target_entropy,
            'entropy_reduction': result.entropy_reduction,
            'reduction_percentage': f"{result.reduction_percentage:.2f}%",
            'factor_analysis': result.factor_analysis,
            'recommendations': result.recommendations
        }, ensure_ascii=False, indent=2))
    else:
        print(f"当前熵值: {result.current_entropy:.3f}")
        print(f"目标熵值: {result.target_entropy:.3f}")
        print(f"熵减效果: {result.entropy_reduction:.3f} ({result.reduction_percentage:.2f}%)\n")
        
        print("因素分析:")
        for factor_name, data in result.factor_analysis.items():
            print(f"  {factor_name}:")
            print(f"    当前: {data['current']:.3f} -> 目标: {data['target']:.3f}")
            print(f"    改善: {data['improvement']:.3f} ({data['improvement_percentage']:.2f}%)")
            print(f"    影响: {data['impact']}")
        
        print("\n建议:")
        for i, recommendation in enumerate(result.recommendations, 1):
            print(f"  {i}. {recommendation}")


if __name__ == '__main__':
    main()
