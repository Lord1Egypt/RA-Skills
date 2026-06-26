#!/usr/bin/env python3
"""
骗局风险评分系统
计算CRS（骗局风险评分）、LRS（流动性风险评分）和综合风险评分
"""

import argparse
import json
import sys


def calculate_crs(
    revenue_source_score,
    risk_identification_score,
    cognitive_threshold_score,
    liquidity_score,
    information_transparency_score
):
    """
    计算骗局风险评分（CRS）

    Args:
        revenue_source_score: 收益来源评分（0-2，0=高风险，2=低风险）
        risk_identification_score: 风险识别评分（0-2）
        cognitive_threshold_score: 认知门槛评分（0-2）
        liquidity_score: 流动性评分（0-2）
        information_transparency_score: 信息透明评分（0-2）

    Returns:
        float: CRS评分（0-2）
    """
    crs = (
        0.3 * revenue_source_score +
        0.25 * risk_identification_score +
        0.2 * cognitive_threshold_score +
        0.15 * liquidity_score +
        0.1 * information_transparency_score
    )
    return crs


def calculate_lrs(
    withdrawal_difficulty,
    lock_period,
    order_depth,
    slippage
):
    """
    计算流动性风险评分（LRS）

    Args:
        withdrawal_difficulty: 提现难度（0-3，0=极差，3=好）
        lock_period: 锁定期（0-3）
        order_depth: 订单深度（0-3）
        slippage: 滑点（0-3）

    Returns:
        float: LRS评分（0-3）
    """
    lrs = (
        0.4 * withdrawal_difficulty +
        0.3 * lock_period +
        0.2 * order_depth +
        0.1 * slippage
    )
    return lrs


def calculate_composite_risk(crs, lrs):
    """
    计算综合风险评分

    Args:
        crs: 骗局风险评分（0-2）
        lrs: 流动性风险评分（0-3）

    Returns:
        float: 综合风险评分（0-2.5）
    """
    # 将LRS归一化到0-2范围
    normalized_lrs = (lrs / 3) * 2

    composite = 0.6 * crs + 0.4 * normalized_lrs
    return composite


def get_risk_level(composite_risk):
    """
    根据综合风险评分获取风险等级

    Args:
        composite_risk: 综合风险评分

    Returns:
        dict: 风险等级和建议
    """
    if composite_risk < 1.4:
        return {
            "level": "极高",
            "color": "red",
            "action": "拒绝",
            "reason": "综合风险评分过低，强烈建议拒绝投资"
        }
    elif composite_risk < 1.8:
        return {
            "level": "高",
            "color": "orange",
            "action": "谨慎",
            "reason": "综合风险评分较高，建议谨慎评估或拒绝"
        }
    else:
        return {
            "level": "中低",
            "color": "green",
            "action": "可考虑",
            "reason": "综合风险评分在可接受范围内，可以考虑投资"
        }


def score_to_description(score, max_score, score_type):
    """
    将分数转换为描述

    Args:
        score: 分数
        max_score: 最高分
        score_type: 分数类型

    Returns:
        str: 描述
    """
    ratio = score / max_score

    if ratio >= 0.8:
        return "低风险"
    elif ratio >= 0.5:
        return "中风险"
    elif ratio >= 0.2:
        return "高风险"
    else:
        return "极高风险"


def main():
    parser = argparse.ArgumentParser(
        description='骗局风险评分系统 - 计算CRS、LRS和综合风险评分',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
评分标准:
  CRS评分（骗局风险，0-2分）:
    - 收益来源: 0=说不清, 1=依赖特定条件, 2=明确逻辑
    - 风险识别: 0=承诺"无风险", 1=风险模糊, 2=风险明确
    - 认知门槛: 0="不用懂", 1=需要专业分析, 2=可自行理解
    - 流动性: 0=锁定期, 1=限制退出, 2=随时退出
    - 信息透明: 0=不透明, 1=部分透明, 2=高度透明

  LRS评分（流动性风险，0-3分）:
    - 提现难度: 0=极差, 1=差, 2=一般, 3=好
    - 锁定期: 0=长锁定期, 1=中锁定期, 2=短锁定期, 3=无锁定期
    - 订单深度: 0=极差, 1=差, 2=一般, 3=好
    - 滑点: 0=极高, 1=高, 2=一般, 3=低

示例:
  # 高风险案例
  python scripts/scam_risk_scorer.py --revenue-source 0 --risk-identification 0 --cognitive-threshold 0 --liquidity 0 --information 0 --withdrawal-difficulty 0 --lock-period 0 --order-depth 0 --slippage 0

  # 中风险案例
  python scripts/scam_risk_scorer.py --revenue-source 1 --risk-identification 1 --cognitive-threshold 1 --liquidity 1 --information 1 --withdrawal-difficulty 1 --lock-period 2 --order-depth 2 --slippage 2

  # 低风险案例
  python scripts/scam_risk_scorer.py --revenue-source 2 --risk-identification 2 --cognitive-threshold 2 --liquidity 2 --information 2 --withdrawal-difficulty 3 --lock-period 3 --order-depth 3 --slippage 3
        """
    )

    # CRS参数
    parser.add_argument(
        '--revenue-source',
        type=int,
        choices=[0, 1, 2],
        required=True,
        help='收益来源评分（0=说不清，1=依赖特定条件，2=明确逻辑）'
    )

    parser.add_argument(
        '--risk-identification',
        type=int,
        choices=[0, 1, 2],
        required=True,
        help='风险识别评分（0=承诺"无风险"，1=风险模糊，2=风险明确）'
    )

    parser.add_argument(
        '--cognitive-threshold',
        type=int,
        choices=[0, 1, 2],
        required=True,
        help='认知门槛评分（0="不用懂"，1=需要专业分析，2=可自行理解）'
    )

    parser.add_argument(
        '--liquidity',
        type=int,
        choices=[0, 1, 2],
        required=True,
        help='流动性评分（0=锁定期，1=限制退出，2=随时退出）'
    )

    parser.add_argument(
        '--information',
        type=int,
        choices=[0, 1, 2],
        required=True,
        help='信息透明评分（0=不透明，1=部分透明，2=高度透明）'
    )

    # LRS参数
    parser.add_argument(
        '--withdrawal-difficulty',
        type=int,
        choices=[0, 1, 2, 3],
        required=True,
        help='提现难度（0=极差，1=差，2=一般，3=好）'
    )

    parser.add_argument(
        '--lock-period',
        type=int,
        choices=[0, 1, 2, 3],
        required=True,
        help='锁定期（0=长锁定期，1=中锁定期，2=短锁定期，3=无锁定期）'
    )

    parser.add_argument(
        '--order-depth',
        type=int,
        choices=[0, 1, 2, 3],
        required=True,
        help='订单深度（0=极差，1=差，2=一般，3=好）'
    )

    parser.add_argument(
        '--slippage',
        type=int,
        choices=[0, 1, 2, 3],
        required=True,
        help='滑点（0=极高，1=高，2=一般，3=低）'
    )

    args = parser.parse_args()

    try:
        # 计算CRS
        crs = calculate_crs(
            args.revenue_source,
            args.risk_identification,
            args.cognitive_threshold,
            args.liquidity,
            args.information
        )

        # 计算LRS
        lrs = calculate_lrs(
            args.withdrawal_difficulty,
            args.lock_period,
            args.order_depth,
            args.slippage
        )

        # 计算综合风险
        composite_risk = calculate_composite_risk(crs, lrs)

        # 获取风险等级
        risk_level = get_risk_level(composite_risk)

        # 生成详细评分描述
        crs_details = {
            "revenue_source": {
                "score": args.revenue_source,
                "description": score_to_description(args.revenue_source, 2, "CRS"),
                "weight": 0.3
            },
            "risk_identification": {
                "score": args.risk_identification,
                "description": score_to_description(args.risk_identification, 2, "CRS"),
                "weight": 0.25
            },
            "cognitive_threshold": {
                "score": args.cognitive_threshold,
                "description": score_to_description(args.cognitive_threshold, 2, "CRS"),
                "weight": 0.2
            },
            "liquidity": {
                "score": args.liquidity,
                "description": score_to_description(args.liquidity, 2, "CRS"),
                "weight": 0.15
            },
            "information_transparency": {
                "score": args.information,
                "description": score_to_description(args.information, 2, "CRS"),
                "weight": 0.1
            }
        }

        lrs_details = {
            "withdrawal_difficulty": {
                "score": args.withdrawal_difficulty,
                "description": score_to_description(args.withdrawal_difficulty, 3, "LRS"),
                "weight": 0.4
            },
            "lock_period": {
                "score": args.lock_period,
                "description": score_to_description(args.lock_period, 3, "LRS"),
                "weight": 0.3
            },
            "order_depth": {
                "score": args.order_depth,
                "description": score_to_description(args.order_depth, 3, "LRS"),
                "weight": 0.2
            },
            "slippage": {
                "score": args.slippage,
                "description": score_to_description(args.slippage, 3, "LRS"),
                "weight": 0.1
            }
        }

        # 输出结果
        result = {
            "status": "success",
            "crs": {
                "score": round(crs, 2),
                "max_score": 2.0,
                "details": crs_details
            },
            "lrs": {
                "score": round(lrs, 2),
                "max_score": 3.0,
                "details": lrs_details
            },
            "composite_risk": {
                "score": round(composite_risk, 2),
                "max_score": 2.5,
                "level": risk_level
            },
            "recommendation": risk_level
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"计算失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
