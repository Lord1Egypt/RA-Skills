#!/usr/bin/env python3
"""
认知偏差评分脚本

基于卡尼曼《思考，快与慢》的 8 大认知偏差评估。

使用方法：
    python bias-scorer.py --biases "loss_aversion,confirmation,anchoring" --severity "high,medium,low"

输出：
    JSON 格式的偏差评分和建议
"""

import argparse
import json


# 8 大认知偏差定义
BIASES = {
    'loss_aversion': {
        'name': '损失厌恶',
        'description': '厌恶损失甚于获得同等收益',
        'check_questions': [
            '是否不愿止损？',
            '是否死扛亏损股？',
            '是否盈利就拿不住？'
        ],
        'risk_weight': 1.5
    },
    'anchoring': {
        'name': '锚定效应',
        'description': '过度依赖初始信息',
        'check_questions': [
            '是否锚定买入价？',
            '是否受历史高点影响？',
            '是否过度关注成本价？'
        ],
        'risk_weight': 1.2
    },
    'confirmation': {
        'name': '确认偏误',
        'description': '只找支持自己观点的证据',
        'check_questions': [
            '是否只看利好信息？',
            '是否忽视反面证据？',
            '是否只关注支持自己观点的分析师？'
        ],
        'risk_weight': 1.5
    },
    'disposition': {
        'name': '处置效应',
        'description': '过早卖出盈利，死扛亏损',
        'check_questions': [
            '是否盈利就拿不住？',
            '是否亏损就不愿卖？',
            '是否频繁卖出盈利股？'
        ],
        'risk_weight': 1.3
    },
    'herding': {
        'name': '从众心理',
        'description': '跟随大众行为',
        'check_questions': [
            '是否追涨杀跌？',
            '是否因为别人买而买？',
            '是否害怕错过（FOMO）？'
        ],
        'risk_weight': 1.4
    },
    'overconfidence': {
        'name': '过度自信',
        'description': '高估自己的能力和预测准确性',
        'check_questions': [
            '是否过度交易？',
            '是否认为自己能预测市场？',
            '是否忽视运气因素？'
        ],
        'risk_weight': 1.6
    },
    'representativeness': {
        'name': '代表性偏差',
        'description': '以偏概全，过度推断',
        'check_questions': [
            '是否只看近期表现？',
            '是否因为 3 年好就认为永远好？',
            '是否忽视均值回归？'
        ],
        'risk_weight': 1.2
    },
    'availability': {
        'name': '可得性偏差',
        'description': '易记的信息被认为更重要',
        'check_questions': [
            '是否受新闻标题影响？',
            '是否因为最近大跌而恐惧？',
            '是否过度关注极端事件？'
        ],
        'risk_weight': 1.1
    }
}


def calculate_score(biases_list, severity_list):
    """
    计算偏差评分
    
    Args:
        biases_list: list, 偏差列表 ['loss_aversion', 'confirmation', ...]
        severity_list: list, 严重程度列表 ['high', 'medium', 'low']
    
    Returns:
        dict: 评分结果
    """
    severity_map = {
        'high': 3,
        'medium': 2,
        'low': 1
    }
    
    total_score = 0
    max_score = 0
    detected_biases = []
    
    for bias, severity in zip(biases_list, severity_list):
        if bias in BIASES:
            weight = BIASES[bias]['risk_weight']
            score = severity_map.get(severity, 1) * weight
            total_score += score
            max_score += 3 * weight  # 最大严重程度 3
            
            detected_biases.append({
                'key': bias,
                'name': BIASES[bias]['name'],
                'severity': severity,
                'score': score,
                'max_score': 3 * weight,
                'check_questions': BIASES[bias]['check_questions']
            })
    
    # 计算百分比
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    # 风险等级
    if percentage >= 60:
        risk_level = '高'
        recommendation = '建议暂停决策，深入反思偏差'
    elif percentage >= 30:
        risk_level = '中'
        recommendation = '需要警惕偏差影响，使用清单检查'
    else:
        risk_level = '低'
        recommendation = '决策较客观，保持警惕'
    
    return {
        'total_score': round(total_score, 2),
        'max_score': round(max_score, 2),
        'percentage': round(percentage, 1),
        'risk_level': risk_level,
        'recommendation': recommendation,
        'detected_biases': detected_biases,
        'bias_count': len(biases_list)
    }


def format_output(result):
    """格式化输出"""
    output = []
    output.append("【认知偏差评分】")
    output.append("")
    output.append(f"检测到偏差数量：{result['bias_count']}个")
    output.append(f"总分：{result['total_score']}/{result['max_score']} ({result['percentage']}%)")
    output.append(f"风险等级：{result['risk_level']}")
    output.append(f"建议：{result['recommendation']}")
    output.append("")
    output.append("【检测到的偏差】")
    
    for bias in result['detected_biases']:
        output.append("")
        output.append(f"{bias['name']}（{bias['severity']}）")
        output.append(f"  得分：{bias['score']}/{bias['max_score']}")
        output.append(f"  检查问题：")
        for q in bias['check_questions'][:2]:  # 只显示前 2 个问题
            output.append(f"    - {q}")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='认知偏差评分脚本')
    parser.add_argument('--biases', type=str, required=True,
                       help='偏差列表，逗号分隔 (loss_aversion,confirmation,anchoring)')
    parser.add_argument('--severity', type=str, required=True,
                       help='严重程度列表，逗号分隔 (high,medium,low)')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    biases_list = [b.strip() for b in args.biases.split(',')]
    severity_list = [s.strip() for s in args.severity.split(',')]
    
    if len(biases_list) != len(severity_list):
        print("错误：偏差数量和严重程度数量必须一致")
        return
    
    result = calculate_score(biases_list, severity_list)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
