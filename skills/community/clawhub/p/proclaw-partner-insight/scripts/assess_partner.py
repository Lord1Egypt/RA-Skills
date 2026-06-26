#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伴侣结构化评估脚本
根据六个维度打分，计算综合得分，判定类型和风险等级
"""

import argparse
import json
import sys


def assess_partner(emotional_stability, growth_support, value_independence,
                   self_value_anchor, crisis_response, long_term_match):
    """
    评估伴侣格局

    参数:
        emotional_stability: 情绪稳定性 (1-10)
        growth_support: 成长支持度 (1-10)
        value_independence: 价值独立性 (1-10)
        self_value_anchor: 自我价值锚点 (1-10)
        crisis_response: 危机应对能力 (1-10)
        long_term_match: 长期匹配度 (1-10)

    返回:
        dict: 评估结果
    """

    # 权重配置
    weights = {
        'emotional_stability': 0.25,
        'growth_support': 0.20,
        'value_independence': 0.15,
        'self_value_anchor': 0.15,
        'crisis_response': 0.10,
        'long_term_match': 0.15
    }

    # 计算综合得分
    overall_score = (
        emotional_stability * weights['emotional_stability'] +
        growth_support * weights['growth_support'] +
        value_independence * weights['value_independence'] +
        self_value_anchor * weights['self_value_anchor'] +
        crisis_response * weights['crisis_response'] +
        long_term_match * weights['long_term_match']
    )

    # 判定类型
    personality_type = "混合型"

    if (emotional_stability <= 3 and growth_support <= 3 and
        value_independence <= 3):
        personality_type = "丫鬟型"
    elif (self_value_anchor <= 3 and value_independence <= 5 and
          emotional_stability >= 5):
        personality_type = "妃子型"
    elif (emotional_stability >= 7 and growth_support >= 7 and
          value_independence >= 7 and self_value_anchor >= 7):
        personality_type = "皇后型"

    # 判定风险等级
    if overall_score <= 4:
        risk_level = "高风险"
        risk_detail = "严重拖垮关系，建议立即止损或深度干预"
    elif overall_score <= 6:
        risk_level = "中风险"
        risk_detail = "有消耗，但存在调整空间，建议观察+沟通+边界设定"
    elif overall_score <= 8:
        risk_level = "低风险"
        risk_detail = "基本健康，有成长潜力，建议持续优化"
    else:
        risk_level = "优质"
        risk_detail = "皇后型伴侣，建议珍惜并深度合作"

    # 维度分析
    dimensions = {
        'emotional_stability': {
            'score': emotional_stability,
            'weight': weights['emotional_stability'],
            'weighted_score': emotional_stability * weights['emotional_stability'],
            'name': '情绪稳定性'
        },
        'growth_support': {
            'score': growth_support,
            'weight': weights['growth_support'],
            'weighted_score': growth_support * weights['growth_support'],
            'name': '成长支持度'
        },
        'value_independence': {
            'score': value_independence,
            'weight': weights['value_independence'],
            'weighted_score': value_independence * weights['value_independence'],
            'name': '价值独立性'
        },
        'self_value_anchor': {
            'score': self_value_anchor,
            'weight': weights['self_value_anchor'],
            'weighted_score': self_value_anchor * weights['self_value_anchor'],
            'name': '自我价值锚点'
        },
        'crisis_response': {
            'score': crisis_response,
            'weight': weights['crisis_response'],
            'weighted_score': crisis_response * weights['crisis_response'],
            'name': '危机应对能力'
        },
        'long_term_match': {
            'score': long_term_match,
            'weight': weights['long_term_match'],
            'weighted_score': long_term_match * weights['long_term_match'],
            'name': '长期匹配度'
        }
    }

    # 识别短板维度（得分最低的2个）
    sorted_dimensions = sorted(
        [(key, val['score'], val['name']) for key, val in dimensions.items()],
        key=lambda x: x[1]
    )
    weak_dimensions_raw = sorted_dimensions[:2]
    weak_dimensions_formatted = [
        {'name': name, 'score': score}
        for key, score, name in weak_dimensions_raw
    ]

    result = {
        'status': 'success',
        'overall_score': round(overall_score, 2),
        'personality_type': personality_type,
        'risk_level': risk_level,
        'risk_detail': risk_detail,
        'dimensions': dimensions,
        'weak_dimensions': weak_dimensions_formatted,
        'suggestions': generate_suggestions(personality_type, overall_score, weak_dimensions_formatted)
    }

    return result


def generate_suggestions(personality_type, overall_score, weak_dimensions):
    """生成改进建议"""

    suggestions = []

    if personality_type == "丫鬟型":
        suggestions.append("评估是阶段性的不安全感，还是深层的格局限制")
        suggestions.append("关键因素：在一起时间长度、伴侣成长意愿、你的野心程度")
        suggestions.append("处理空间：有些还有调整空间，有些已到必须止损节点")

    elif personality_type == "妃子型":
        suggestions.append("评估已投入的感情和资源")
        suggestions.append("关键因素：替代风险、真实连接程度、长期价值")
        suggestions.append("止损判断：是否继续投入会被更多消耗")

    elif personality_type == "皇后型":
        suggestions.append("验证真实性：关系稳定期是否保持皇后型特征")
        suggestions.append("时间测试：半年以上观察期")
        suggestions.append("关键因素：不可替代性、战略价值、共同成长度")

    else:  # 混合型
        suggestions.append("使用混合特征识别器进行深度分析")
        suggestions.append("识别主特征和副特征")
        suggestions.append("分析切换触发条件")

    # 针对短板维度的建议
    if weak_dimensions:
        weak_names = [d['name'] for d in weak_dimensions]
        suggestions.append(f"短板维度：{', '.join(weak_names)}，建议重点改进")

    if overall_score <= 4:
        suggestions.append("高风险关系，建议使用决策支持矩阵评估止损时机")
    elif overall_score <= 6:
        suggestions.append("中风险关系，建议使用动态跟踪框架观察改进")
    elif overall_score <= 8:
        suggestions.append("低风险关系，建议持续优化")

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description='伴侣结构化评估工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/assess_partner.py --emotional 7 --growth 8 --independence 7 --anchor 8 --crisis 7 --match 8
  python scripts/assess_partner.py -e 3 -g 2 -v 2 -s 3 -c 3 -l 2
        """
    )

    parser.add_argument('--emotional', '-e', type=float, required=True,
                        help='情绪稳定性 (1-10)')
    parser.add_argument('--growth', '-g', type=float, required=True,
                        help='成长支持度 (1-10)')
    parser.add_argument('--independence', '-v', type=float, required=True,
                        help='价值独立性 (1-10)')
    parser.add_argument('--anchor', '-s', type=float, required=True,
                        help='自我价值锚点 (1-10)')
    parser.add_argument('--crisis', '-c', type=float, required=True,
                        help='危机应对能力 (1-10)')
    parser.add_argument('--match', '-l', type=float, required=True,
                        help='长期匹配度 (1-10)')

    args = parser.parse_args()

    # 参数验证
    for name, value in [
        ('emotional', args.emotional),
        ('growth', args.growth),
        ('independence', args.independence),
        ('anchor', args.anchor),
        ('crisis', args.crisis),
        ('match', args.match)
    ]:
        if not (1 <= value <= 10):
            print(json.dumps({
                'status': 'error',
                'message': f'参数 {name} 必须在 1-10 之间'
            }, ensure_ascii=False))
            sys.exit(1)

    # 执行评估
    result = assess_partner(
        args.emotional,
        args.growth,
        args.independence,
        args.anchor,
        args.crisis,
        args.match
    )

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
