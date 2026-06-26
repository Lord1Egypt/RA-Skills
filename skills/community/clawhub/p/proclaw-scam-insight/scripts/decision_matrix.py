#!/usr/bin/env python3
"""
决策矩阵评估工具
评估骗局风险判断矩阵和投资机会评估矩阵
"""

import argparse
import json
import sys


def evaluate_scam_matrix(scores):
    """
    评估骗局风险判断矩阵

    Args:
        scores: 各维度评分字典
            {
                "revenue_source": 0-2,
                "risk_identification": 0-2,
                "cognitive_threshold": 0-2,
                "trust_building": 0-2,
                "liquidity": 0-2,
                "information_transparency": 0-2
            }

    Returns:
        dict: 评估结果
    """
    # 计算总分（0-12分）
    total_score = sum(scores.values())

    # 风险等级判定
    if total_score <= 4:
        risk_level = "极高风险"
        action = "拒绝"
        reason = "多项高风险特征，强烈建议拒绝"
    elif total_score <= 8:
        risk_level = "高风险"
        action = "警惕"
        reason = "存在高风险特征，需要警惕"
    elif total_score <= 10:
        risk_level = "中风险"
        action = "审慎评估"
        reason = "存在中等风险，需要审慎评估"
    else:
        risk_level = "低风险"
        action = "可考虑"
        reason = "风险较低，可以考虑"

    # 检查必查项
    must_check_items = [
        ("revenue_source", scores.get("revenue_source", 0)),
        ("risk_identification", scores.get("risk_identification", 0)),
        ("cognitive_threshold", scores.get("cognitive_threshold", 0)),
        ("liquidity", scores.get("liquidity", 0)),
        ("information_transparency", scores.get("information_transparency", 0))
    ]

    failed_must_check = [item[0] for item in must_check_items if item[1] == 0]

    if failed_must_check:
        action = "拒绝"
        reason = f"必查项不符合标准: {', '.join(failed_must_check)}"

    return {
        "total_score": total_score,
        "max_score": 12,
        "risk_level": risk_level,
        "action": action,
        "reason": reason,
        "failed_must_check": failed_must_check,
        "details": scores
    }


def evaluate_investment_matrix(scores, weights=None):
    """
    评估投资机会矩阵

    Args:
        scores: 各维度评分字典（1-5分）
            {
                "expected_value": 1-5,
                "risk_control": 1-5,
                "liquidity": 1-5,
                "information_transparency": 1-5,
                "time_match": 1-5
            }
        weights: 权重字典（可选）
            {
                "expected_value": 0.3,
                "risk_control": 0.25,
                "liquidity": 0.15,
                "information_transparency": 0.15,
                "time_match": 0.15
            }

    Returns:
        dict: 评估结果
    """
    # 默认权重
    if weights is None:
        weights = {
            "expected_value": 0.30,
            "risk_control": 0.25,
            "liquidity": 0.15,
            "information_transparency": 0.15,
            "time_match": 0.15
        }

    # 计算加权总分
    weighted_score = sum(scores[key] * weights[key] for key in scores.keys())

    # 评分等级判定
    if weighted_score >= 4.0:
        grade = "优秀"
        action = "考虑"
        reason = "各方面表现优秀，可以考虑投资"
    elif weighted_score >= 3.0:
        grade = "良好"
        action = "可考虑"
        reason = "各方面表现良好，可以考虑投资"
    elif weighted_score >= 2.0:
        grade = "一般"
        action = "需谨慎"
        reason = "表现一般，需要谨慎评估"
    else:
        grade = "差"
        action = "拒绝"
        reason = "表现较差，建议拒绝"

    # 检查低分项
    low_score_items = [key for key, value in scores.items() if value <= 2]

    if low_score_items:
        reason += f"。低分项: {', '.join(low_score_items)}"

    return {
        "weighted_score": round(weighted_score, 2),
        "max_score": 5.0,
        "grade": grade,
        "action": action,
        "reason": reason,
        "low_score_items": low_score_items,
        "details": scores,
        "weights": weights
    }


def main():
    parser = argparse.ArgumentParser(
        description='决策矩阵评估工具 - 评估骗局风险和投资机会',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 骗局风险矩阵评估
  python scripts/decision_matrix.py --matrix-type scam --scores '{"revenue_source":0,"risk_identification":0,"cognitive_threshold":0,"trust_building":0,"liquidity":0,"information_transparency":0}'

  # 投资机会矩阵评估（使用默认权重）
  python scripts/decision_matrix.py --matrix-type investment --scores '{"expected_value":4,"risk_control":3,"liquidity":4,"information_transparency":3,"time_match":4}'

  # 投资机会矩阵评估（自定义权重）
  python scripts/decision_matrix.py --matrix-type investment --scores '{"expected_value":4,"risk_control":3,"liquidity":4,"information_transparency":3,"time_match":4}' --weights '{"expected_value":0.4,"risk_control":0.3,"liquidity":0.1,"information_transparency":0.1,"time_match":0.1}'
        """
    )

    parser.add_argument(
        '--matrix-type',
        type=str,
        choices=['scam', 'investment'],
        required=True,
        help='矩阵类型：scam（骗局风险）或investment（投资机会）'
    )

    parser.add_argument(
        '--scores',
        type=str,
        required=True,
        help='各维度评分（JSON格式）'
    )

    parser.add_argument(
        '--weights',
        type=str,
        help='权重（JSON格式，仅investment矩阵需要）'
    )

    args = parser.parse_args()

    try:
        # 解析评分
        scores = json.loads(args.scores)

        # 验证评分范围
        if args.matrix_type == 'scam':
            for key, value in scores.items():
                if not isinstance(value, int) or value not in [0, 1, 2]:
                    print(json.dumps({
                        "status": "error",
                        "message": f"评分错误: {key} 必须是0、1或2"
                    }, ensure_ascii=False))
                    sys.exit(1)

            # 评估骗局风险矩阵
            result = evaluate_scam_matrix(scores)

        elif args.matrix_type == 'investment':
            for key, value in scores.items():
                if not isinstance(value, (int, float)) or value < 1 or value > 5:
                    print(json.dumps({
                        "status": "error",
                        "message": f"评分错误: {key} 必须在1到5之间"
                    }, ensure_ascii=False))
                    sys.exit(1)

            # 解析权重
            weights = None
            if args.weights:
                weights = json.loads(args.weights)
                # 验证权重总和为1
                total_weight = sum(weights.values())
                if not (0.99 <= total_weight <= 1.01):
                    print(json.dumps({
                        "status": "error",
                        "message": f"权重总和必须为1，当前为{total_weight}"
                    }, ensure_ascii=False))
                    sys.exit(1)

            # 评估投资机会矩阵
            result = evaluate_investment_matrix(scores, weights)

        result["status"] = "success"
        result["matrix_type"] = args.matrix_type

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"JSON解析错误: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)
    except KeyError as e:
        print(json.dumps({
            "status": "error",
            "message": f"缺少必要字段: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"评估失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
