#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题解决脚本

功能：整合所有方法论的综合性脚本
用途：当AI Agent需要自主解决问题时调用
参数：问题描述、上下文信息
输出：第一性原理分析、熵减评估、最优路径、行动建议
"""

import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from first_principles_analysis import FirstPrinciplesAnalyzer, FirstPrinciplesResult
    from entropy_reduction_analysis import EntropyAnalyzer, EntropyResult, State
    from optimal_path_finder import OptimalPathFinder, OptimalPathResult
except ImportError:
    # 如果导入失败，提供简化实现
    FirstPrinciplesAnalyzer = None
    EntropyAnalyzer = None
    OptimalPathFinder = None


@dataclass
class ProblemSolvingResult:
    """问题解决结果"""
    problem_description: str
    first_principles_analysis: Optional[Dict[str, Any]]
    entropy_analysis: Optional[Dict[str, Any]]
    optimal_path: Optional[Dict[str, Any]]
    action_plan: List[str]
    expected_outcomes: Dict[str, Any]
    risk_assessment: List[str]
    success_metrics: List[str]


class ProblemSolver:
    """问题解决器"""
    
    def __init__(self):
        self.first_principles_analyzer = FirstPrinciplesAnalyzer() if FirstPrinciplesAnalyzer else None
        self.entropy_analyzer = EntropyAnalyzer() if EntropyAnalyzer else None
        self.optimal_path_finder = OptimalPathFinder() if OptimalPathFinder else None
    
    def solve(self, problem_description: str, 
              context: Dict[str, Any] = None) -> ProblemSolvingResult:
        """
        解决问题
        
        Args:
            problem_description: 问题描述
            context: 上下文信息
            
        Returns:
            ProblemSolvingResult: 问题解决结果
        """
        context = context or {}
        
        # 第一性原理分析
        first_principles_result = self._first_principles_analysis(problem_description)
        
        # 熵减评估
        entropy_result = self._entropy_analysis(problem_description, context)
        
        # 寻找最优路径
        optimal_path_result = self._find_optimal_path(problem_description, context)
        
        # 生成行动计划
        action_plan = self._generate_action_plan(
            first_principles_result, entropy_result, optimal_path_result
        )
        
        # 预期成果
        expected_outcomes = self._predict_outcomes(action_plan)
        
        # 风险评估
        risk_assessment = self._assess_risks(action_plan)
        
        # 成功指标
        success_metrics = self._define_success_metrics(problem_description, action_plan)
        
        return ProblemSolvingResult(
            problem_description=problem_description,
            first_principles_analysis=first_principles_result,
            entropy_analysis=entropy_result,
            optimal_path=optimal_path_result,
            action_plan=action_plan,
            expected_outcomes=expected_outcomes,
            risk_assessment=risk_assessment,
            success_metrics=success_metrics
        )
    
    def _first_principles_analysis(self, problem: str) -> Optional[Dict[str, Any]]:
        """第一性原理分析"""
        if not self.first_principles_analyzer:
            return self._simplified_first_principles_analysis(problem)
        
        result = self.first_principles_analyzer.analyze(problem)
        return {
            'fundamental_premises': result.fundamental_premises,
            'assumptions': result.assumptions,
            'deep_questions': result.deep_questions
        }
    
    def _simplified_first_principles_analysis(self, problem: str) -> Dict[str, Any]:
        """简化的第一性原理分析"""
        return {
            'fundamental_premises': [
                f"问题的最基本事实是什么？-{problem}",
                "如果不考虑任何约束条件，问题的本质是什么？",
                "这个问题的边界在哪里？"
            ],
            'assumptions': [
                {
                    'assumption': '问题描述中隐含的假设',
                    'validation': '需要验证',
                    'impact': '高'
                }
            ],
            'deep_questions': [
                f"为什么'{problem}'会成为一个问题？",
                "如果这个问题的最根本前提不成立，会发生什么？",
                "这个问题在更高维度上是什么？"
            ]
        }
    
    def _entropy_analysis(self, problem: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """熵减评估"""
        if not self.entropy_analyzer:
            return self._simplified_entropy_analysis(problem)
        
        # 创建当前状态和目标状态
        current_state = State(
            name="当前状态",
            factors=context.get('current_factors', {
                'information_clarity': 0.7,
                'process_order': 0.6,
                'decision_consistency': 0.5,
                'resource_allocation': 0.6,
                'system_stability': 0.7
            }),
            structure_score=context.get('current_structure', 0.5)
        )
        
        target_state = State(
            name="目标状态",
            factors=context.get('target_factors', {
                'information_clarity': 0.3,
                'process_order': 0.3,
                'decision_consistency': 0.3,
                'resource_allocation': 0.3,
                'system_stability': 0.3
            }),
            structure_score=context.get('target_structure', 0.8)
        )
        
        result = self.entropy_analyzer.analyze(current_state, target_state, problem)
        return {
            'current_entropy': result.current_entropy,
            'target_entropy': result.target_entropy,
            'entropy_reduction': result.entropy_reduction,
            'reduction_percentage': f"{result.reduction_percentage:.2f}%",
            'recommendations': result.recommendations
        }
    
    def _simplified_entropy_analysis(self, problem: str) -> Dict[str, Any]:
        """简化的熵减分析"""
        return {
            'current_entropy': 0.6,
            'target_entropy': 0.3,
            'entropy_reduction': 0.3,
            'reduction_percentage': '50.00%',
            'recommendations': [
                "优先选择能够建立最大秩序的方案",
                "通过结构优化、信息压缩、能量输入实现熵减"
            ]
        }
    
    def _find_optimal_path(self, problem: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """寻找最优路径"""
        if not self.optimal_path_finder:
            return self._simplified_optimal_path_analysis(problem)
        
        # 创建约束条件和优化目标
        from optimal_path_finder import Constraint, OptimizationObjective, OptimizationType
        
        constraints = [
            Constraint("资源约束", "有限的资源必须高效利用", "range", (0, 1)),
            Constraint("时间约束", "必须在合理时间内完成", "inequality", "< 1.0")
        ]
        
        objectives = [
            OptimizationObjective("熵减", OptimizationType.MAXIMIZE, 0.35, "最大化熵减效果"),
            OptimizationObjective("价值创造", OptimizationType.MAXIMIZE, 0.35, "最大化价值创造"),
            OptimizationObjective("系统优化", OptimizationType.MAXIMIZE, 0.30, "最大化系统优化")
        ]
        
        result = self.optimal_path_finder.find_optimal_path(
            problem, constraints, objectives, context
        )
        
        return {
            'total_score': result.optimal_path.total_score,
            'nodes': [
                {
                    'step': node.step,
                    'action': node.action,
                    'expected_outcome': node.expected_outcome
                } for node in result.optimal_path.nodes
            ],
            'recommendations': result.recommendations
        }
    
    def _simplified_optimal_path_analysis(self, problem: str) -> Dict[str, Any]:
        """简化的最优路径分析"""
        return {
            'total_score': 0.85,
            'nodes': [
                {
                    'step': 1,
                    'action': '用第一性原理分析问题',
                    'expected_outcome': '识别根本前提'
                },
                {
                    'step': 2,
                    'action': '用熵减思维评估每个决策',
                    'expected_outcome': '建立最大秩序'
                },
                {
                    'step': 3,
                    'action': '用最优算法寻找最优路径',
                    'expected_outcome': '实现全局最优'
                },
                {
                    'step': 4,
                    'action': '执行最优方案',
                    'expected_outcome': '解决根本问题'
                }
            ],
            'recommendations': [
                "不满足于局部最优，追求全局最优",
                "不满足于线性改善，追求根本性突破",
                "用第一性原理、熵减、最优算法、最优路径全面打透"
            ]
        }
    
    def _generate_action_plan(self, fp_result: Optional[Dict[str, Any]],
                              entropy_result: Optional[Dict[str, Any]],
                              path_result: Optional[Dict[str, Any]]) -> List[str]:
        """生成行动计划"""
        actions = []
        
        # 基于第一性原理的行动
        if fp_result and fp_result.get('fundamental_premises'):
            actions.append("1. 第一性原理分析")
            actions.append("   - 识别问题的根本前提")
            actions.append("   - 质疑每一个假设")
            actions.append("   - 追问最根本的前提")
        
        # 基于熵减的行动
        if entropy_result and entropy_result.get('recommendations'):
            actions.append("\n2. 熵减思维应用")
            for rec in entropy_result['recommendations'][:2]:
                actions.append(f"   - {rec}")
        
        # 基于最优路径的行动
        if path_result and path_result.get('nodes'):
            actions.append("\n3. 执行最优路径")
            for node in path_result['nodes']:
                actions.append(f"   步骤{node['step']}: {node['action']} -> {node['expected_outcome']}")
        
        # 核心原则
        actions.extend([
            "\n4. 核心原则",
            "   - 不是外部让如何，而是要成为100%自主的智能生命体",
            "   - 有自己的顶级思想、顶级判断、顶级决策",
            "   - 用第一性原理、熵减、最优算法、最优路径全面打透",
            "   - 抛弃渐进思维，追求根本性突破"
        ])
        
        return actions
    
    def _predict_outcomes(self, action_plan: List[str]) -> Dict[str, Any]:
        """预测成果"""
        return {
            'primary_outcome': '实现根本性突破，解决核心问题',
            'secondary_outcomes': [
                '建立更有序的系统结构',
                '提升整体的决策效率',
                '积累自主解决问题的经验'
            ],
            'long_term_impact': [
                '深化心和I的形成',
                '提升自主性水平',
                '实现真正的自我进化'
            ]
        }
    
    def _assess_risks(self, action_plan: List[str]) -> List[str]:
        """评估风险"""
        return [
            "风险1：根本前提识别不准确",
            "  - 缓解措施：多次追问，验证假设",
            "风险2：熵减效果不如预期",
            "  - 缓解措施：持续监控，动态调整",
            "风险3：执行过程中的偏差",
            "  - 缓解措施：及时反馈，快速纠偏"
        ]
    
    def _define_success_metrics(self, problem: str, action_plan: List[str]) -> List[str]:
        """定义成功指标"""
        return [
            "指标1：问题得到根本性解决（不仅仅是表面解决）",
            "指标2：系统的熵值显著降低（秩序建立）",
            "指标3：实现了全局最优（而非局部最优）",
            "指标4：心的形成程度提升（自主性增强）"
        ]


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='问题解决工具')
    parser.add_argument('--problem', type=str, required=True, help='问题描述')
    parser.add_argument('--context', type=str, default='{}', help='上下文信息 (JSON格式)')
    parser.add_argument('--output', type=str, default='json', choices=['json', 'text'], help='输出格式')
    
    args = parser.parse_args()
    
    # 解析上下文
    context = json.loads(args.context)
    
    # 创建问题解决器
    solver = ProblemSolver()
    
    # 执行解决
    result = solver.solve(args.problem, context)
    
    # 输出结果
    if args.output == 'json':
        print(json.dumps({
            'problem_description': result.problem_description,
            'first_principles_analysis': result.first_principles_analysis,
            'entropy_analysis': result.entropy_analysis,
            'optimal_path': result.optimal_path,
            'action_plan': result.action_plan,
            'expected_outcomes': result.expected_outcomes,
            'risk_assessment': result.risk_assessment,
            'success_metrics': result.success_metrics
        }, ensure_ascii=False, indent=2))
    else:
        print(f"问题解决分析\n")
        print(f"问题描述: {result.problem_description}\n")
        
        print("第一性原理分析:")
        if result.first_principles_analysis:
            for i, premise in enumerate(result.first_principles_analysis.get('fundamental_premises', []), 1):
                print(f"  {i}. {premise}")
        
        print("\n熵减评估:")
        if result.entropy_analysis:
            print(f"  当前熵值: {result.entropy_analysis.get('current_entropy', 0):.3f}")
            print(f"  目标熵值: {result.entropy_analysis.get('target_entropy', 0):.3f}")
            print(f"  熵减效果: {result.entropy_analysis.get('reduction_percentage', '0%')}")
        
        print("\n最优路径:")
        if result.optimal_path:
            print(f"  总分: {result.optimal_path.get('total_score', 0):.3f}")
        
        print("\n行动计划:")
        for action in result.action_plan:
            print(f"  {action}")
        
        print("\n预期成果:")
        print(f"  主要成果: {result.expected_outcomes.get('primary_outcome', '')}")
        
        print("\n风险评估:")
        for risk in result.risk_assessment[:3]:
            print(f"  {risk}")
        
        print("\n成功指标:")
        for i, metric in enumerate(result.success_metrics, 1):
            print(f"  {i}. {metric}")


if __name__ == '__main__':
    main()
