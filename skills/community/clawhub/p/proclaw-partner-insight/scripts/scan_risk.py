#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伴侣风险扫描脚本
根据危险信号清单扫描，判定风险等级
"""

import argparse
import json
import sys


def scan_risk(red_signals, orange_signals, yellow_signals, assessment_score=None):
    """
    扫描风险等级

    参数:
        red_signals: 红色信号数量 (0-5)
        orange_signals: 橙色信号数量 (0-5)
        yellow_signals: 黄色信号数量 (0-5)
        assessment_score: 评估得分 (可选, 0-10)

    返回:
        dict: 风险扫描结果
    """

    total_signals = red_signals + orange_signals + yellow_signals

    # 判定风险等级
    risk_level = "低风险"
    risk_code = "green"
    risk_detail = "关系整体健康，建议定期扫描"

    if red_signals >= 1 or orange_signals >= 3 or (assessment_score and assessment_score <= 4):
        risk_level = "极高风险"
        risk_code = "red"
        risk_detail = "出现红色信号或评估得分≤4分，建议立即止损"
    elif (orange_signals >= 2 or
          (red_signals >= 1 and yellow_signals >= 2) or
          (assessment_score and 4 < assessment_score <= 5)):
        risk_level = "高风险"
        risk_code = "orange"
        risk_detail = "出现2-3个橙色信号或评估得分4-5分，建议设定观察期"
    elif (yellow_signals >= 2 or orange_signals >= 1 or
          (assessment_score and 5 < assessment_score <= 6)):
        risk_level = "中风险"
        risk_code = "yellow"
        risk_detail = "出现2-4个黄色信号或评估得分5-6分，建议识别问题根源"

    # 生成危险信号详情
    signal_details = generate_signal_details(red_signals, orange_signals, yellow_signals)

    # 生成应对策略
    coping_strategy = generate_coping_strategy(risk_code, red_signals, orange_signals, yellow_signals)

    result = {
        'status': 'success',
        'risk_level': risk_level,
        'risk_code': risk_code,
        'risk_detail': risk_detail,
        'signal_summary': {
            'red_signals': red_signals,
            'orange_signals': orange_signals,
            'yellow_signals': yellow_signals,
            'total_signals': total_signals
        },
        'signal_details': signal_details,
        'assessment_score': assessment_score,
        'coping_strategy': coping_strategy,
        'action_items': generate_action_items(risk_code)
    }

    return result


def generate_signal_details(red_signals, orange_signals, yellow_signals):
    """生成危险信号详情"""

    red_signal_names = [
        "极端控制行为",
        "情绪暴力",
        "经济剥削",
        "隔离策略",
        "持续性贬低"
    ]

    orange_signal_names = [
        "频繁情绪爆发",
        "阻拦发展",
        "缺乏边界感",
        "价值交换模式",
        "反复无常"
    ]

    yellow_signal_names = [
        "偶尔情绪波动",
        "轻微控制行为",
        "成长支持不足",
        "自我价值锚点偏移",
        "长期匹配度存疑"
    ]

    details = {
        'red': [],
        'orange': [],
        'yellow': []
    }

    for i in range(red_signals):
        if i < len(red_signal_names):
            details['red'].append({
                'name': red_signal_names[i],
                'severity': '极高'
            })

    for i in range(orange_signals):
        if i < len(orange_signal_names):
            details['orange'].append({
                'name': orange_signal_names[i],
                'severity': '高'
            })

    for i in range(yellow_signals):
        if i < len(yellow_signal_names):
            details['yellow'].append({
                'name': yellow_signal_names[i],
                'severity': '中'
            })

    return details


def generate_coping_strategy(risk_code, red_signals, orange_signals, yellow_signals):
    """生成应对策略"""

    strategies = []

    if risk_code == "red":
        strategies.append("立即止损")
        strategies.append("明确表达关系结束，拒绝情感勒索")
        strategies.append("保护人身安全和财产安全")
        strategies.append("必要时寻求法律保护")
        strategies.append("切断所有联系")

    elif risk_code == "orange":
        strategies.append("深度沟通，明确边界")
        strategies.append("使用决策支持矩阵评估止损时机")
        strategies.append("设定3个月观察期，无改善则止损")
        strategies.append("使用动态跟踪框架记录变化")

    elif risk_code == "yellow":
        strategies.append("识别问题根源")
        strategies.append("明确沟通，设定期望")
        strategies.append("使用动态跟踪框架观察改进")
        strategies.append("评估改进可能性")

    else:  # green
        strategies.append("持续优化")
        strategies.append("定期扫描（每3个月）")
        strategies.append("深化合作关系")

    return strategies


def generate_action_items(risk_code):
    """生成具体行动项"""

    if risk_code == "red":
        return [
            "立即执行止损策略",
            "清理共同财产",
            "寻求家人朋友支持",
            "必要时寻求法律帮助"
        ]
    elif risk_code == "orange":
        return [
            "本周内进行深度沟通",
            "设定明确边界和期望",
            "启动3个月观察期",
            "准备止损策略"
        ]
    elif risk_code == "yellow":
        return [
            "识别问题根源（能力/意愿/格局）",
            "制定沟通计划",
            "启动跟踪观察",
            "定期重新评估"
        ]
    else:  # green
        return [
            "继续维护关系",
            "定期扫描（每3个月）",
            "深化合作关系"
        ]


def main():
    parser = argparse.ArgumentParser(
        description='伴侣风险扫描工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/scan_risk.py --red 1 --orange 2 --yellow 1
  python scripts/scan_risk.py -r 0 -o 1 -y 2 --score 5.5
        """
    )

    parser.add_argument('--red', '-r', type=int, default=0,
                        help='红色信号数量 (0-5)')
    parser.add_argument('--orange', '-o', type=int, default=0,
                        help='橙色信号数量 (0-5)')
    parser.add_argument('--yellow', '-y', type=int, default=0,
                        help='黄色信号数量 (0-5)')
    parser.add_argument('--score', '-s', type=float, default=None,
                        help='评估得分 (可选, 0-10)')

    args = parser.parse_args()

    # 参数验证
    if not (0 <= args.red <= 5):
        print(json.dumps({
            'status': 'error',
            'message': '红色信号数量必须在 0-5 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if not (0 <= args.orange <= 5):
        print(json.dumps({
            'status': 'error',
            'message': '橙色信号数量必须在 0-5 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if not (0 <= args.yellow <= 5):
        print(json.dumps({
            'status': 'error',
            'message': '黄色信号数量必须在 0-5 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if args.score is not None and not (0 <= args.score <= 10):
        print(json.dumps({
            'status': 'error',
            'message': '评估得分必须在 0-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    # 执行扫描
    result = scan_risk(args.red, args.orange, args.yellow, args.score)

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
