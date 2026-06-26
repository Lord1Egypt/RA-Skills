#!/usr/bin/env python3
"""
决策清单 - 基于芒格多元思维模型和认知偏差检查

无需外部数据，纯逻辑分析
"""

import sys
import os
from datetime import datetime


# 认知偏差检查清单
COGNITIVE_BIASES = [
    {
        'name': '确认偏误',
        'question': '我是否只寻找支持自己观点的信息？',
        'check': '主动寻找反面证据，考虑对立观点',
    },
    {
        'name': '过度自信',
        'question': '我是否高估了自己的预测能力？',
        'check': '回顾历史预测准确率，考虑最坏情况',
    },
    {
        'name': '从众心理',
        'question': '我是否因为别人都在做而跟随？',
        'check': '独立思考，分析基本面而非市场情绪',
    },
    {
        'name': '损失厌恶',
        'question': '我是否因为害怕损失而错过机会？',
        'check': '理性评估风险收益比，设定止损点',
    },
    {
        'name': '锚定效应',
        'question': '我是否过度依赖某个初始信息？',
        'check': '多角度分析，不单一依赖某个指标',
    },
    {
        'name': '代表性偏误',
        'question': '我是否过度简化了复杂情况？',
        'check': '考虑多种可能性，避免刻板印象',
    },
    {
        'name': '可得性偏误',
        'question': '我是否过度依赖容易获得的信息？',
        'check': '主动搜寻全面信息，不局限于表面',
    },
    {
        'name': '沉没成本谬误',
        'question': '我是否因为已投入而继续错误决策？',
        'check': '基于当前和未来价值决策，忽略沉没成本',
    },
]


# 多元思维模型检查清单
MENTAL_MODELS = [
    {
        'name': '第一性原理',
        'question': '我是否回归到事物本质思考？',
        'check': '拆解到基本原理，从源头推理',
    },
    {
        'name': '逆向思维',
        'question': '我是否考虑了相反的情况？',
        'check': '反过来想：如何确保失败？然后避免',
    },
    {
        'name': '二阶思维',
        'question': '我是否考虑了后果的后果？',
        'check': '问"然后呢？"至少三次',
    },
    {
        'name': '概率思维',
        'question': '我是否用概率而非确定性思考？',
        'check': '估算各种结果的概率和期望值',
    },
    {
        'name': '机会成本',
        'question': '我是否考虑了放弃的 alternatives？',
        'check': '列出所有可选方案，比较最优替代',
    },
    {
        'name': '能力圈',
        'question': '我是否在自己的能力圈内决策？',
        'check': '诚实评估自己的知识和经验边界',
    },
    {
        'name': '安全边际',
        'question': '我是否留有足够的犯错空间？',
        'check': '保守估计，预留 30%+ 安全边际',
    },
    {
        'name': '复利思维',
        'question': '我是否考虑了长期复利效应？',
        'check': '思考 5 年、10 年后的累积效果',
    },
]


def check_biases(user_answers: dict = None) -> dict:
    """
    认知偏差检查
    
    Args:
        user_answers: 用户回答（可选）
    
    Returns:
        检查结果字典
    """
    result = {
        'type': '认知偏差检查',
        'total': len(COGNITIVE_BIASES),
        'flagged': 0,
        'items': [],
    }
    
    for bias in COGNITIVE_BIASES:
        item = {
            'name': bias['name'],
            'question': bias['question'],
            'check': bias['check'],
            'risk': '中',  # 默认中等风险
        }
        
        # 如果有用户回答，根据回答判断风险
        if user_answers:
            answer = user_answers.get(bias['name'], '')
            if '是' in answer or '可能' in answer:
                item['risk'] = '高'
                result['flagged'] += 1
            elif '否' in answer:
                item['risk'] = '低'
        
        result['items'].append(item)
    
    return result


def check_mental_models(user_answers: dict = None) -> dict:
    """
    多元思维模型检查
    
    Args:
        user_answers: 用户回答（可选）
    
    Returns:
        检查结果字典
    """
    result = {
        'type': '多元思维模型检查',
        'total': len(MENTAL_MODELS),
        'applied': 0,
        'items': [],
    }
    
    for model in MENTAL_MODELS:
        item = {
            'name': model['name'],
            'question': model['question'],
            'check': model['check'],
            'applied': '否',
        }
        
        # 如果有用户回答，根据回答判断
        if user_answers:
            answer = user_answers.get(model['name'], '')
            if '是' in answer or '已应用' in answer:
                item['applied'] = '是'
                result['applied'] += 1
        
        result['items'].append(item)
    
    return result


def generate_checklist(decision_type: str = '投资') -> dict:
    """
    生成决策清单
    
    Args:
        decision_type: 决策类型（投资/商业/生活）
    
    Returns:
        完整检查清单
    """
    result = {
        'decision_type': decision_type,
        'timestamp': datetime.now().isoformat(),
        'cognitive_biases': check_biases(),
        'mental_models': check_mental_models(),
        'summary': '',
        'recommendation': '',
    }
    
    # 生成总结
    bias_count = result['cognitive_biases']['flagged']
    model_count = result['mental_models']['applied']
    
    if bias_count == 0 and model_count >= 5:
        result['summary'] = '决策质量：优秀'
        result['recommendation'] = '✅ 可以执行决策（已充分检查）'
    elif bias_count <= 2 and model_count >= 3:
        result['summary'] = '决策质量：良好'
        result['recommendation'] = '⚠️ 可以执行，但需注意已识别的风险'
    else:
        result['summary'] = '决策质量：需改进'
        result['recommendation'] = '❌ 建议暂停，重新思考并应用更多思维模型'
    
    return result


def print_checklist(result: dict) -> None:
    """打印检查清单"""
    print("="*60)
    print(f"📋 决策清单 - {result['decision_type']}")
    print("="*60)
    print(f"\n生成时间：{result['timestamp']}")
    
    # 认知偏差检查
    print(f"\n🧠 认知偏差检查")
    print(f"   已识别风险：{result['cognitive_biases']['flagged']}/{result['cognitive_biases']['total']}")
    
    for item in result['cognitive_biases']['items']:
        risk_icon = '⚠️' if item['risk'] == '高' else '➡️'
        print(f"\n   {risk_icon} {item['name']}")
        print(f"      问题：{item['question']}")
        print(f"      检查：{item['check']}")
    
    # 多元思维模型
    print(f"\n🎯 多元思维模型")
    print(f"   已应用：{result['mental_models']['applied']}/{result['mental_models']['total']}")
    
    for item in result['mental_models']['items']:
        applied_icon = '✅' if item['applied'] == '是' else '❌'
        print(f"\n   {applied_icon} {item['name']}")
        print(f"      问题：{item['question']}")
        print(f"      检查：{item['check']}")
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 总结")
    print(f"   {result['summary']}")
    print(f"\n💡 建议")
    print(f"   {result['recommendation']}")
    
    # 使用说明
    print(f"\n📝 使用说明")
    print(f"   1. 逐项回答每个问题")
    print(f"   2. 标记高风险认知偏差")
    print(f"   3. 应用至少 5 个思维模型")
    print(f"   4. 根据建议决定是否执行")


def main():
    """主函数"""
    decision_type = sys.argv[1] if len(sys.argv) > 1 else '投资'
    
    result = generate_checklist(decision_type)
    print_checklist(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
