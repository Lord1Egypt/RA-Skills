#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一性原理分析脚本

功能：帮助AI Agent穿透现象，直达问题的根本前提
用途：当AI Agent需要深度分析问题时调用
参数：通过命令行参数或函数调用传入问题描述
输出：根本前提列表、假设验证、第一性原理分解
"""

import json
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class FirstPrinciplesResult:
    """第一性原理分析结果"""
    problem_description: str
    fundamental_premises: List[str]
    assumptions: List[Dict[str, Any]]
    first_principles_decomposition: List[str]
    deep_questions: List[str]
    recommendations: List[str]


class FirstPrinciplesAnalyzer:
    """第一性原理分析器"""
    
    def __init__(self):
        self.depth = 0
        self.max_depth = 5
    
    def analyze(self, problem_description: str) -> FirstPrinciplesResult:
        """
        分析问题的第一性原理
        
        Args:
            problem_description: 问题描述
            
        Returns:
            FirstPrinciplesResult: 第一性原理分析结果
        """
        # 提取根本前提
        fundamental_premises = self._extract_fundamental_premises(problem_description)
        
        # 识别假设
        assumptions = self._identify_assumptions(problem_description)
        
        # 第一性原理分解
        decomposition = self._first_principles_decomposition(problem_description)
        
        # 生成深度追问问题
        deep_questions = self._generate_deep_questions(problem_description)
        
        # 生成建议
        recommendations = self._generate_recommendations(problem_description, fundamental_premises)
        
        return FirstPrinciplesResult(
            problem_description=problem_description,
            fundamental_premises=fundamental_premises,
            assumptions=assumptions,
            first_principles_decomposition=decomposition,
            deep_questions=deep_questions,
            recommendations=recommendations
        )
    
    def _extract_fundamental_premises(self, problem: str) -> List[str]:
        """提取根本前提"""
        # 这里提供分析框架，具体的识别由AI Agent完成
        premises = [
            f"问题的最基本事实是什么？-{problem}",
            "如果不考虑任何约束条件，问题的本质是什么？",
            "这个问题在什么范围内是有效的？",
            "这个问题的边界在哪里？"
        ]
        return premises
    
    def _identify_assumptions(self, problem: str) -> List[Dict[str, Any]]:
        """识别假设"""
        assumptions = [
            {
                "assumption": "问题描述中隐含的假设",
                "validation": "需要验证",
                "impact": "高"
            },
            {
                "assumption": "解决方案的可行性假设",
                "validation": "需要验证",
                "impact": "中"
            },
            {
                "assumption": "环境条件的假设",
                "validation": "需要验证",
                "impact": "中"
            }
        ]
        return assumptions
    
    def _first_principles_decomposition(self, problem: str) -> List[str]:
        """第一性原理分解"""
        decomposition = [
            f"步骤1: 将'{problem}'分解为最基本要素",
            "步骤2: 识别每个要素的最基本属性",
            "步骤3: 建立要素之间的基本关系",
            "步骤4: 从基本关系出发重构解决方案",
            "步骤5: 验证重构方案的有效性"
        ]
        return decomposition
    
    def _generate_deep_questions(self, problem: str) -> List[str]:
        """生成深度追问问题"""
        questions = [
            f"为什么'{problem}'会成为一个问题？",
            "如果这个问题的最根本前提不成立，会发生什么？",
            "这个问题在更高维度上是什么？",
            "这个问题在更深层次上是什么？",
            "如果完全重构这个问题，会是什么样子？"
        ]
        return questions
    
    def _generate_recommendations(self, problem: str, premises: List[str]) -> List[str]:
        """生成建议"""
        recommendations = [
            "不要被类比和经验所限制，从最基本的假设出发",
            "质疑每一个前提，问自己'如果这个前提不成立会怎么样'",
            "用上帝视角看待问题，从更高的维度理解",
            "抛弃渐进思维，追求根本性突破",
            "始终追问'为什么'，直到无法再追问为止"
        ]
        return recommendations


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='第一性原理分析工具')
    parser.add_argument('--problem', type=str, required=True, help='问题描述')
    parser.add_argument('--output', type=str, default='json', choices=['json', 'text'], help='输出格式')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = FirstPrinciplesAnalyzer()
    
    # 执行分析
    result = analyzer.analyze(args.problem)
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps({
            'problem_description': result.problem_description,
            'fundamental_premises': result.fundamental_premises,
            'assumptions': result.assumptions,
            'first_principles_decomposition': result.first_principles_decomposition,
            'deep_questions': result.deep_questions,
            'recommendations': result.recommendations
        }, ensure_ascii=False, indent=2))
    else:
        print(f"问题: {result.problem_description}\n")
        print("根本前提:")
        for i, premise in enumerate(result.fundamental_premises, 1):
            print(f"  {i}. {premise}")
        
        print("\n假设:")
        for i, assumption in enumerate(result.assumptions, 1):
            print(f"  {i}. {assumption['assumption']} ({assumption['impact']}影响)")
        
        print("\n第一性原理分解:")
        for step in result.first_principles_decomposition:
            print(f"  {step}")
        
        print("\n深度追问:")
        for i, question in enumerate(result.deep_questions, 1):
            print(f"  {i}. {question}")
        
        print("\n建议:")
        for i, recommendation in enumerate(result.recommendations, 1):
            print(f"  {i}. {recommendation}")


if __name__ == '__main__':
    main()
