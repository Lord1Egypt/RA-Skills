#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合特征分析脚本
根据特征权重分析混合类型，预测长期趋势
"""

import argparse
import json
import sys


def analyze_hybrid(y_weight, c_weight, h_weight):
    """
    分析混合特征

    参数:
        y_weight: 丫鬟型权重 (0-10)
        c_weight: 妃子型权重 (0-10)
        h_weight: 皇后型权重 (0-10)

    返回:
        dict: 混合特征分析结果
    """

    total_weight = y_weight + c_weight + h_weight

    if total_weight == 0:
        return {
            'status': 'error',
            'message': '至少需要提供一个权重大于0'
        }

    # 计算百分比
    y_percent = y_weight / total_weight * 100
    c_percent = c_weight / total_weight * 100
    h_percent = h_weight / total_weight * 100

    # 识别主特征和副特征
    features = [
        {'type': '丫鬟型', 'weight': y_weight, 'percent': y_percent},
        {'type': '妃子型', 'weight': c_weight, 'percent': c_percent},
        {'type': '皇后型', 'weight': h_weight, 'percent': h_percent}
    ]

    sorted_features = sorted(features, key=lambda x: x['weight'], reverse=True)

    primary_feature = sorted_features[0] if sorted_features[0]['weight'] > 0 else None
    secondary_feature = sorted_features[1] if len(sorted_features) > 1 and sorted_features[1]['weight'] > 0 else None

    # 判定混合类型
    hybrid_type = determine_hybrid_type(y_weight, c_weight, h_weight, sorted_features)

    # 预测长期趋势
    long_term_trend = predict_long_term_trend(hybrid_type, y_weight, c_weight, h_weight)

    # 改进可能性评估
    improvement_possibility = assess_improvement_possibility(hybrid_type, y_weight, c_weight, h_weight)

    # 切换触发条件
    trigger_conditions = identify_trigger_conditions(hybrid_type, y_weight, c_weight, h_weight)

    result = {
        'status': 'success',
        'hybrid_type': hybrid_type,
        'features': {
            '丫鬟型': {
                'weight': y_weight,
                'percent': round(y_percent, 2)
            },
            '妃子型': {
                'weight': c_weight,
                'percent': round(c_percent, 2)
            },
            '皇后型': {
                'weight': h_weight,
                'percent': round(h_percent, 2)
            }
        },
        'primary_feature': primary_feature,
        'secondary_feature': secondary_feature,
        'long_term_trend': long_term_trend,
        'improvement_possibility': improvement_possibility,
        'trigger_conditions': trigger_conditions,
        'suggestions': generate_hybrid_suggestions(hybrid_type, long_term_trend, improvement_possibility)
    }

    return result


def determine_hybrid_type(y_weight, c_weight, h_weight, sorted_features):
    """判定混合类型"""

    # 纯类型
    if (y_weight > 0 and c_weight == 0 and h_weight == 0):
        return "纯丫鬟型"
    elif (c_weight > 0 and y_weight == 0 and h_weight == 0):
        return "纯妃子型"
    elif (h_weight > 0 and y_weight == 0 and c_weight == 0):
        return "纯皇后型"

    # 混合类型
    primary = sorted_features[0]
    secondary = sorted_features[1] if len(sorted_features) > 1 else None

    if not secondary or secondary['weight'] == 0:
        return f"纯{primary['type']}"

    # 权重相近（差值<30%）
    diff = abs(primary['weight'] - secondary['weight'])
    total = primary['weight'] + secondary['weight']
    if total > 0 and diff / total < 0.3:
        return f"{primary['type']}与{secondary['type']}混合"

    # 主副特征明显
    return f"{primary['type']}基础+{secondary['type']}表象"


def predict_long_term_trend(hybrid_type, y_weight, c_weight, h_weight):
    """预测长期趋势"""

    trend = {
        'short_term': '',
        'medium_term': '',
        'long_term': '',
        'improvement_improvement': ''
    }

    if '纯丫鬟型' in hybrid_type:
        trend['short_term'] = '控制欲逐渐增强'
        trend['medium_term'] = '阻拦发展明显'
        trend['long_term'] = '完全暴露为丫鬟型'
        trend['improvement_possibility'] = '低（格局限制强）'

    elif '纯妃子型' in hybrid_type:
        trend['short_term'] = '精致展示持续'
        trend['medium_term'] = '新鲜感开始下降'
        trend['long_term'] = '面临替代风险'
        trend['improvement_possibility'] = '低（价值观问题）'

    elif '纯皇后型' in hybrid_type:
        trend['short_term'] = '皇后型特征稳定'
        trend['medium_term'] = '持续支持成长'
        trend['long_term'] = '稳定为优质伴侣'
        trend['improvement_possibility'] = 'N/A（已优秀）'

    elif '丫鬟型' in hybrid_type and '妃子型' in hybrid_type:
        if y_weight > c_weight:
            trend['short_term'] = '妃子型表象占主导'
            trend['medium_term'] = '妃子型表象逐渐消失'
            trend['long_term'] = '暴露为丫鬟型基础'
            trend['improvement_possibility'] = '低（格局限制强）'
        else:
            trend['short_term'] = '妃子型特征明显'
            trend['medium_term'] = '内在不稳定'
            trend['long_term'] = '不确定，风险较高'
            trend['improvement_possibility'] = '低（内在不稳定）'

    elif '皇后型' in hybrid_type and ('丫鬟型' in hybrid_type or '妃子型' in hybrid_type):
        if h_weight > max(y_weight, c_weight):
            trend['short_term'] = '皇后型特征占主导'
            trend['medium_term'] = '偶尔表现其他特征'
            trend['long_term'] = '稳定为皇后型'
            trend['improvement_possibility'] = '高（阶段性的不安全感）'
        else:
            trend['short_term'] = '多类型特征混合'
            trend['medium_term'] = '切换无规律'
            trend['long_term'] = '不确定'
            trend['improvement_possibility'] = '低（内在不稳定）'

    else:
        trend['short_term'] = '多类型特征随机切换'
        trend['medium_term'] = '切换持续无规律'
        trend['long_term'] = '不确定，风险较高'
        trend['improvement_possibility'] = '低（内在不稳定）'

    return trend


def assess_improvement_possibility(hybrid_type, y_weight, c_weight, h_weight):
    """评估改进可能性"""

    if '纯皇后型' in hybrid_type:
        return {
            'level': 'N/A',
            'description': '已经是最佳类型'
        }

    if '皇后型' in hybrid_type and h_weight > max(y_weight, c_weight):
        return {
            'level': '高',
            'description': '主特征是皇后型，偶尔的其他表现是阶段性的不安全感，通过沟通和边界设定可以改善'
        }

    if '丫鬟型' in hybrid_type and '妃子型' in hybrid_type:
        return {
            'level': '低',
            'description': '丫鬟型基础+妃子型表象，长期趋势是丫鬟型，格局限制强，改进空间小'
        }

    if '纯丫鬟型' in hybrid_type:
        return {
            'level': '低',
            'description': '丫鬟型格局，格局限制强，改进空间小'
        }

    if '纯妃子型' in hybrid_type:
        return {
            'level': '低',
            'description': '妃子型价值观，改进空间小'
        }

    return {
        'level': '低',
        'description': '混合特征，内在不稳定，改进空间小'
    }


def identify_trigger_conditions(hybrid_type, y_weight, c_weight, h_weight):
    """识别切换触发条件"""

    triggers = []

    if y_weight > 0:
        triggers.append({
            'trigger': '伴侣事业上升',
            'result': '暴露丫鬟型特征（抱怨、控制）'
        })
        triggers.append({
            'trigger': '伴侣面临不确定性',
            'result': '暴露丫鬟型特征（恐惧、阻拦）'
        })

    if c_weight > 0:
        triggers.append({
            'trigger': '需要展示价值',
            'result': '表现妃子型特征（精致、竞争）'
        })
        triggers.append({
            'trigger': '感觉关系不稳定',
            'result': '表现妃子型特征（制造危机感）'
        })

    if h_weight > 0:
        triggers.append({
            'trigger': '伴侣遇到困难',
            'result': '表现皇后型特征（共同解决问题）'
        })
        triggers.append({
            'trigger': '关系稳定期',
            'result': '表现皇后型特征（展现真实价值）'
        })

    return triggers


def generate_hybrid_suggestions(hybrid_type, long_term_trend, improvement_possibility):
    """生成混合特征建议"""

    suggestions = []

    if '纯皇后型' in hybrid_type:
        suggestions.append("珍惜关系，人生合伙人")
        suggestions.append("深化战略伙伴关系")

    elif '皇后型' in hybrid_type and improvement_possibility['level'] == '高':
        suggestions.append("继续沟通，设定边界")
        suggestions.append("观察改进，使用动态跟踪框架")

    elif '丫鬟型' in hybrid_type and '妃子型' in hybrid_type:
        suggestions.append("使用动态跟踪框架观察6个月")
        suggestions.append("参考决策支持矩阵，评估止损时机")

    elif '纯丫鬟型' in hybrid_type:
        suggestions.append("评估是否格局限制")
        suggestions.append("参考决策支持矩阵，决定是否止损")

    else:
        suggestions.append("使用混合特征识别器深度分析")
        suggestions.append("使用动态跟踪框架观察变化")

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description='混合特征分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/analyze_hybrid.py --y 5 --c 3 --h 2
  python scripts/analyze_hybrid.py --丫鬟 5 --妃子 3 --皇后 2
        """
    )

    parser.add_argument('--y', '--丫鬟', type=float, default=0,
                        help='丫鬟型权重 (0-10)')
    parser.add_argument('--c', '--妃子', type=float, default=0,
                        help='妃子型权重 (0-10)')
    parser.add_argument('--h', '--皇后', type=float, default=0,
                        help='皇后型权重 (0-10)')

    args = parser.parse_args()

    # 参数验证
    if args.y < 0 or args.y > 10:
        print(json.dumps({
            'status': 'error',
            'message': '丫鬟型权重必须在 0-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if args.c < 0 or args.c > 10:
        print(json.dumps({
            'status': 'error',
            'message': '妃子型权重必须在 0-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if args.h < 0 or args.h > 10:
        print(json.dumps({
            'status': 'error',
            'message': '皇后型权重必须在 0-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if args.y == 0 and args.c == 0 and args.h == 0:
        print(json.dumps({
            'status': 'error',
            'message': '至少需要提供一个权重大于0'
        }, ensure_ascii=False))
        sys.exit(1)

    # 执行分析
    result = analyze_hybrid(args.y, args.c, args.h)

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
