#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策支持脚本
根据五维度数据匹配决策矩阵，输出决策建议
"""

import argparse
import json
import sys


def support_decision(assessment_score, relationship_duration, improvement_possibility,
                    sunk_cost, risk_level):
    """
    决策支持

    参数:
        assessment_score: 评估得分 (0-10)
        relationship_duration: 关系时长（月）
        improvement_possibility: 改进可能性 (1-10)
        sunk_cost: 沉没成本 (1-10)
        risk_level: 风险等级 (1-4, 1=低, 2=中, 3=高, 4=极高)

    返回:
        dict: 决策建议
    """

    # 决策矩阵匹配
    decision_type, decision_detail = match_decision_matrix(
        assessment_score,
        relationship_duration,
        improvement_possibility,
        sunk_cost,
        risk_level
    )

    # 场景化策略
    scenario_strategy = generate_scenario_strategy(
        assessment_score,
        relationship_duration,
        risk_level
    )

    # 执行策略
    execution_strategy = generate_execution_strategy(decision_type)

    result = {
        'status': 'success',
        'decision_type': decision_type,
        'decision_detail': decision_detail,
        'scenario_strategy': scenario_strategy,
        'execution_strategy': execution_strategy,
        'dimensions': {
            'assessment_score': {
                'value': assessment_score,
                'name': '评估得分',
                'weight': 0.30
            },
            'relationship_duration': {
                'value': relationship_duration,
                'name': '关系时长（月）',
                'weight': 0.20
            },
            'improvement_possibility': {
                'value': improvement_possibility,
                'name': '改进可能性',
                'weight': 0.20
            },
            'sunk_cost': {
                'value': sunk_cost,
                'name': '沉没成本',
                'weight': 0.15
            },
            'risk_level': {
                'value': risk_level,
                'name': '风险等级',
                'weight': 0.15
            }
        },
        'recommendations': generate_recommendations(decision_type, assessment_score, risk_level)
    }

    return result


def match_decision_matrix(assessment_score, relationship_duration, improvement_possibility,
                         sunk_cost, risk_level):
    """匹配决策矩阵"""

    # 立即止损
    if (assessment_score <= 4 and relationship_duration < 6 and
        improvement_possibility <= 3 and sunk_cost <= 3 and risk_level >= 4):
        return "立即止损", "评估得分≤4分 + 关系时长<6个月 + 改进可能性低 + 沉没成本低 + 风险等级极高"

    # 观察后止损
    if (assessment_score <= 6 and relationship_duration <= 24 and
        4 <= improvement_possibility <= 6 and sunk_cost <= 5 and risk_level >= 3):
        return "观察后止损", "评估得分4-6分 + 关系时长≤2年 + 改进可能性中等 + 沉没成本中等 + 风险等级高"

    # 积极改进
    if (assessment_score >= 6 and improvement_possibility >= 7):
        return "积极改进", "评估得分≥6分 + 改进可能性高"

    # 长期优化
    if (assessment_score >= 6 and relationship_duration >= 24 and sunk_cost >= 7):
        return "长期优化", "评估得分≥6分 + 关系时长≥2年 + 沉没成本高"

    # 珍惜关系
    if assessment_score >= 8:
        return "珍惜关系", "评估得分≥8分，关系优质"

    # 默认决策
    if assessment_score <= 4:
        return "观察后止损", "评估得分较低，建议观察后决定"
    elif assessment_score <= 6:
        return "积极改进", "评估得分中等，建议尝试改进"
    else:
        return "长期优化", "评估得分较高，建议优化关系"


def generate_scenario_strategy(assessment_score, relationship_duration, risk_level):
    """生成场景化策略"""

    strategy = {
        'scenario': '',
        'characteristics': [],
        'recommendations': []
    }

    # 新关系（<6个月）
    if relationship_duration < 6:
        strategy['scenario'] = '新关系'
        strategy['characteristics'].append('伪装期风险高')
        strategy['characteristics'].append('沉没成本低')

        if assessment_score <= 4:
            strategy['recommendations'].append('立即止损（无需犹豫）')
        elif assessment_score <= 6:
            strategy['recommendations'].append('观察到6个月，使用伪装验证方法')
        elif assessment_score <= 8:
            strategy['recommendations'].append('继续观察，使用动态跟踪框架')
        else:
            strategy['recommendations'].append('继续发展，但要警惕伪装')

    # 中期关系（6个月-2年）
    elif relationship_duration <= 24:
        strategy['scenario'] = '中期关系'
        strategy['characteristics'].append('伪装期基本结束')
        strategy['characteristics'].append('评估相对可靠')
        strategy['characteristics'].append('沉没成本中等')

        if assessment_score <= 4:
            strategy['recommendations'].append('立即止损（除非改进可能性高+沉没成本高）')
        elif assessment_score <= 6:
            strategy['recommendations'].append('观察后止损或积极改进（根据改进可能性）')
        elif assessment_score <= 8:
            strategy['recommendations'].append('长期优化，深化合作')
        else:
            strategy['recommendations'].append('珍惜关系')

    # 长期关系（2-5年）
    elif relationship_duration <= 60:
        strategy['scenario'] = '长期关系'
        strategy['characteristics'].append('关系稳定')
        strategy['characteristics'].append('沉没成本高')
        strategy['characteristics'].append('改进难度大')

        if assessment_score <= 4:
            strategy['recommendations'].append('谨慎止损（需要评估可行性）')
        elif assessment_score <= 6:
            strategy['recommendations'].append('长期优化或积极改进（根据改进可能性）')
        elif assessment_score <= 8:
            strategy['recommendations'].append('长期优化，接受不完美')
        else:
            strategy['recommendations'].append('珍惜关系')

    # 超长期关系（>5年）
    else:
        strategy['scenario'] = '超长期关系'
        strategy['characteristics'].append('沉没成本极高')
        strategy['characteristics'].append('情感依赖强')
        strategy['characteristics'].append('改进可能性低')

        if assessment_score <= 4:
            strategy['recommendations'].append('评估可行性，谨慎决策（可能不现实）')
        elif assessment_score <= 6:
            strategy['recommendations'].append('维持现状，降低期望')
        else:
            strategy['recommendations'].append('珍惜关系，接受不完美')

    return strategy


def generate_execution_strategy(decision_type):
    """生成执行策略"""

    strategies = {
        "立即止损": [
            "明确表达关系结束",
            "拒绝任何情感勒索",
            "清理共同财产",
            "切断所有联系",
            "必要时寻求专业帮助"
        ],
        "观察后止损": [
            "深度沟通，明确边界和期望",
            "设定3个月观察期",
            "使用动态跟踪框架记录",
            "观察期结束重新评估",
            "无明显改善则止损"
        ],
        "积极改进": [
            "深度沟通，识别问题根源",
            "明确改进目标和边界",
            "提供引导和支持",
            "使用动态跟踪框架记录",
            "定期评估改进效果"
        ],
        "长期优化": [
            "识别优化空间",
            "持续沟通和调整",
            "设定长期目标",
            "深化合作关系",
            "接受不完美"
        ],
        "珍惜关系": [
            "珍惜当前关系",
            "深化战略伙伴关系",
            "共同规划未来",
            "扩大合作范围",
            "共同成长"
        ]
    }

    return strategies.get(decision_type, [])


def generate_recommendations(decision_type, assessment_score, risk_level):
    """生成综合建议"""

    recommendations = []

    if decision_type == "立即止损":
        recommendations.append("这是最优决策，不要犹豫")
        recommendations.append("保护人身安全和财产安全")
        recommendations.append("寻求家人朋友支持")

    elif decision_type == "观察后止损":
        recommendations.append("设定明确的观察期（3个月）")
        recommendations.append("严格执行边界和期望")
        recommendations.append("使用动态跟踪框架记录变化")

    elif decision_type == "积极改进":
        recommendations.append("评估改进可能性是否真实")
        recommendations.append("明确改进的目标和时间节点")
        recommendations.append("定期评估改进效果")

    elif decision_type == "长期优化":
        recommendations.append("接受关系的不完美")
        recommendations.append("寻找可优化的具体领域")
        recommendations.append("设定长期目标")

    elif decision_type == "珍惜关系":
        recommendations.append("这是优质关系，值得珍惜")
        recommendations.append("深化战略伙伴关系")
        recommendations.append("共同规划未来")

    # 风险等级补充建议
    if risk_level >= 4:
        recommendations.append("⚠️  高风险关系，建议优先处理")

    # 评估得分补充建议
    if assessment_score <= 4:
        recommendations.append("⚠️  评估得分极低，关系严重拖垮")
    elif assessment_score >= 8:
        recommendations.append("✅ 评估得分优秀，关系质量高")

    return recommendations


def main():
    parser = argparse.ArgumentParser(
        description='决策支持工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/support_decision.py --score 4.5 --duration 18 --improvement 5 --cost 6 --risk 3
  python scripts/support_decision.py -s 8.2 -d 12 -i 9 -c 5 -r 1
        """
    )

    parser.add_argument('--score', '-s', type=float, required=True,
                        help='评估得分 (0-10)')
    parser.add_argument('--duration', '-d', type=int, required=True,
                        help='关系时长（月）')
    parser.add_argument('--improvement', '-i', type=float, required=True,
                        help='改进可能性 (1-10)')
    parser.add_argument('--cost', '-c', type=float, required=True,
                        help='沉没成本 (1-10)')
    parser.add_argument('--risk', '-r', type=int, required=True,
                        help='风险等级 (1-4, 1=低, 2=中, 3=高, 4=极高)')

    args = parser.parse_args()

    # 参数验证
    if not (0 <= args.score <= 10):
        print(json.dumps({
            'status': 'error',
            'message': '评估得分必须在 0-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if args.duration < 0:
        print(json.dumps({
            'status': 'error',
            'message': '关系时长必须大于等于0'
        }, ensure_ascii=False))
        sys.exit(1)

    if not (1 <= args.improvement <= 10):
        print(json.dumps({
            'status': 'error',
            'message': '改进可能性必须在 1-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if not (1 <= args.cost <= 10):
        print(json.dumps({
            'status': 'error',
            'message': '沉没成本必须在 1-10 之间'
        }, ensure_ascii=False))
        sys.exit(1)

    if not (1 <= args.risk <= 4):
        print(json.dumps({
            'status': 'error',
            'message': '风险等级必须在 1-4 之间 (1=低, 2=中, 3=高, 4=极高)'
        }, ensure_ascii=False))
        sys.exit(1)

    # 执行决策支持
    result = support_decision(
        args.score,
        args.duration,
        args.improvement,
        args.cost,
        args.risk
    )

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
