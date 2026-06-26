#!/usr/bin/env python3
"""
凯利公式计算器
计算最优投资仓位比例
"""

import argparse
import json
import sys


def calculate_kelly_criterion(win_rate, win_amount, loss_amount):
    """
    计算凯利公式最优仓位

    Args:
        win_rate: 胜率 (0-1)
        win_amount: 盈利金额或百分比
        loss_amount: 亏损金额或百分比

    Returns:
        dict: 包含最优仓位和建议的信息
    """
    # 计算赔率
    b = win_amount / loss_amount if loss_amount > 0 else 0

    # 计算败率
    q = 1 - win_rate

    # 凯利公式
    if b > 0:
        f_star = (b * win_rate - q) / b
    else:
        f_star = 0

    # 确保f_star在合理范围内
    f_star = max(0, min(f_star, 1))

    return {
        "optimal_fraction": f_star,
        "odds": b,
        "win_rate": win_rate,
        "lose_rate": q,
        "win_amount": win_amount,
        "loss_amount": loss_amount
    }


def get_conventional_recommendations(f_star, conservative_factor=0.5):
    """
    获取保守策略建议

    Args:
        f_star: 凯利公式计算的最优仓位
        conservative_factor: 保守系数 (0.25 或 0.5)

    Returns:
        dict: 保守策略建议
    """
    quarter_kelly = f_star * 0.25
    half_kelly = f_star * 0.5

    return {
        "quarter_kelly": quarter_kelly,
        "half_kelly": half_kelly,
        "conservative_factor": conservative_factor,
        "recommended_fraction": f_star * conservative_factor
    }


def main():
    parser = argparse.ArgumentParser(
        description='凯利公式计算器 - 计算最优投资仓位比例',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 对称盈亏（胜率60%，盈利100%，亏损100%）
  python scripts/kelly_criterion.py --win-rate 0.6 --win-amount 100 --loss-amount 100

  # 非对称盈亏（胜率40%，盈利50%，亏损10%）
  python scripts/kelly_criterion.py --win-rate 0.4 --win-amount 50 --loss-amount 10 --conservative 0.25

  # 使用百分比（胜率55%，盈利50%，亏损30%）
  python scripts/kelly_criterion.py --win-rate 0.55 --win-amount 0.5 --loss-amount 0.3
        """
    )

    parser.add_argument(
        '--win-rate',
        type=float,
        required=True,
        help='胜率 (0-1之间，例如0.6表示60%胜率)'
    )

    parser.add_argument(
        '--win-amount',
        type=float,
        required=True,
        help='盈利金额或百分比（例如100表示赚100%，0.5表示赚50%）'
    )

    parser.add_argument(
        '--loss-amount',
        type=float,
        required=True,
        help='亏损金额或百分比（例如100表示亏100%，0.3表示亏30%）'
    )

    parser.add_argument(
        '--conservative',
        type=float,
        choices=[0.25, 0.5],
        default=0.5,
        help='保守系数：0.25（四分之一凯利）或0.5（半凯利），默认0.5'
    )

    args = parser.parse_args()

    # 验证输入
    if not 0 <= args.win_rate <= 1:
        print(json.dumps({
            "status": "error",
            "message": "胜率必须在0和1之间"
        }, ensure_ascii=False))
        sys.exit(1)

    if args.win_amount <= 0 or args.loss_amount <= 0:
        print(json.dumps({
            "status": "error",
            "message": "盈利和亏损金额必须大于0"
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        # 计算凯利公式
        kelly_result = calculate_kelly_criterion(args.win_rate, args.win_amount, args.loss_amount)

        # 获取保守策略建议
        recommendations = get_conventional_recommendations(
            kelly_result["optimal_fraction"],
            args.conservative
        )

        # 生成警告和建议
        warnings = []
        if kelly_result["optimal_fraction"] > 0.5:
            warnings.append("凯利公式计算的最优仓位超过50%，这可能过于乐观。建议使用保守策略。")

        if kelly_result["optimal_fraction"] < 0.05:
            warnings.append("凯利公式计算的最优仓位很低，可能期望值不高。建议重新评估。")

        if kelly_result["optimal_fraction"] == 0:
            warnings.append("凯利公式计算的最优仓位为0，说明期望值为负。不应该投资。")

        # 输出结果
        result = {
            "status": "success",
            "kelly_criterion": kelly_result,
            "recommendations": recommendations,
            "warnings": warnings,
            "decision": {
                "should_invest": kelly_result["optimal_fraction"] > 0,
                "recommended_action": "invest" if kelly_result["optimal_fraction"] > 0 else "reject",
                "reason": "期望值为正" if kelly_result["optimal_fraction"] > 0 else "期望值为负"
            }
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
