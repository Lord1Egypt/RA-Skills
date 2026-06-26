#!/usr/bin/env python3
"""
二阶思维者 - 基于霍华德·马克斯的逆向思维模型

无需外部数据，纯逻辑分析
"""

import sys
import os
from datetime import datetime


def first_level_thinking(question: str) -> list:
    """
    一阶思维（直觉反应）
    
    Args:
        question: 问题或决策
    
    Returns:
        一阶思维结果列表
    """
    # 一阶思维通常是直觉的、表面的
    return [
        f"直觉反应：{question}",
        "大多数人会怎么想？",
        "表面看起来是什么？",
        "立即的后果是什么？",
    ]


def second_level_thinking(question: str, first_order: list) -> list:
    """
    二阶思维（深度分析）
    
    Args:
        question: 问题或决策
        first_order: 一阶思维结果
    
    Returns:
        二阶思维结果列表
    """
    return [
        "然后呢？后果的后果是什么？",
        "3 个月后会怎样？1 年后呢？",
        "如果每个人都这么想，会怎样？",
        "什么情况下这个决策会失败？",
        "相反的观点有道理吗？",
        "我在忽略什么重要因素？",
    ]


def analyze_decision(question: str, context: str = None) -> dict:
    """
    二阶思维分析
    
    Args:
        question: 决策问题
        context: 背景信息
    
    Returns:
        分析结果字典
    """
    result = {
        'question': question,
        'context': context or '无',
        'timestamp': datetime.now().isoformat(),
    }
    
    # 一阶思维
    result['first_order'] = first_level_thinking(question)
    
    # 二阶思维
    result['second_order'] = second_level_thinking(question, result['first_order'])
    
    # 逆向思考
    result['contrarian_questions'] = [
        "如果我要确保失败，会怎么做？",
        "什么假设必须是正确的，这个决策才会成功？",
        "如果相反的做法才是对的呢？",
        "我在逃避什么不舒服的真相？",
    ]
    
    # 概率评估
    result['probability_assessment'] = {
        'best_case': '最佳情况是什么？概率多大？',
        'base_case': '最可能情况是什么？概率多大？',
        'worst_case': '最坏情况是什么？概率多大？',
        'expected_value': '期望值 = Σ(概率 × 结果)',
    }
    
    # 综合建议
    result['recommendation'] = {
        'action': '基于二阶思维的决定',
        'risks': '需要关注的风险',
        'monitoring': '需要持续监控的信号',
    }
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print("🤔 二阶思维分析")
    print("="*60)
    
    print(f"\n📋 决策问题")
    print(f"   {result['question']}")
    print(f"\n📝 背景")
    print(f"   {result['context']}")
    
    print(f"\n🧠 一阶思维（直觉反应）")
    for i, thought in enumerate(result['first_order'], 1):
        print(f"   {i}. {thought}")
    
    print(f"\n🎯 二阶思维（深度分析）")
    for i, thought in enumerate(result['second_order'], 1):
        print(f"   {i}. {thought}")
    
    print(f"\n🔄 逆向思考")
    for i, question in enumerate(result['contrarian_questions'], 1):
        print(f"   {i}. {question}")
    
    print(f"\n📊 概率评估")
    for key, value in result['probability_assessment'].items():
        print(f"   • {value}")
    
    print(f"\n💡 综合建议")
    print(f"   行动：{result['recommendation']['action']}")
    print(f"   风险：{result['recommendation']['risks']}")
    print(f"   监控：{result['recommendation']['monitoring']}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 诚实回答每个二阶思维问题")
    print(f"   2. 考虑至少 3 种可能的结果")
    print(f"   3. 评估每种结果的概率")
    print(f"   4. 计算期望值，做出决策")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python3 second-level.py <决策问题>")
        print("示例：python3 second-level.py \"是否应该买入这只股票？\"")
        return 1
    
    question = sys.argv[1]
    context = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = analyze_decision(question, context)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
