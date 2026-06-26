#!/usr/bin/env python3
"""
流动性分析工具
分析订单簿、流动性需求、流动性供给和流动性风险
"""

import argparse
import json
import sys


def calculate_spread(bid_price, ask_price):
    """
    计算买卖价差

    Args:
        bid_price: 最高买价
        ask_price: 最低卖价

    Returns:
        dict: 价差信息
    """
    spread_amount = ask_price - bid_price
    spread_percentage = (spread_amount / ask_price) * 100

    return {
        "spread_amount": spread_amount,
        "spread_percentage": spread_percentage,
        "bid_price": bid_price,
        "ask_price": ask_price
    }


def calculate_order_imbalance(bid_volume, ask_volume):
    """
    计算订单不平衡

    Args:
        bid_volume: 买入总量
        ask_volume: 卖出总量

    Returns:
        dict: 订单不平衡信息
    """
    total_volume = bid_volume + ask_volume

    if total_volume == 0:
        return {
            "imbalance_ratio": 0,
            "direction": "none",
            "bid_volume": bid_volume,
            "ask_volume": ask_volume,
            "total_volume": total_volume
        }

    imbalance_ratio = abs(bid_volume - ask_volume) / total_volume

    if bid_volume > ask_volume:
        direction = "buy_pressure"
    elif ask_volume > bid_volume:
        direction = "sell_pressure"
    else:
        direction = "balanced"

    return {
        "imbalance_ratio": imbalance_ratio,
        "direction": direction,
        "bid_volume": bid_volume,
        "ask_volume": ask_volume,
        "total_volume": total_volume
    }


def analyze_liquidity_demand(panic_sell_volume, normal_volume):
    """
    分析流动性需求

    Args:
        panic_sell_volume: 恐慌抛售量
        normal_volume: 正常成交量

    Returns:
        dict: 流动性需求分析
    """
    if normal_volume == 0:
        liquidity_demand = float('inf')
    else:
        liquidity_demand = panic_sell_volume / normal_volume

    if liquidity_demand > 5:
        status = "critical"
        warning = "流动性极度不足，即将崩盘"
    elif liquidity_demand > 3:
        status = "severe"
        warning = "流动性严重不足"
    elif liquidity_demand > 1:
        status = "moderate"
        warning = "流动性压力较大"
    else:
        status = "normal"
        warning = "流动性正常"

    return {
        "liquidity_demand": liquidity_demand,
        "panic_sell_volume": panic_sell_volume,
        "normal_volume": normal_volume,
        "status": status,
        "warning": warning
    }


def analyze_liquidity_supply(available_funds, panic_sell_volume):
    """
    分析流动性供给

    Args:
        available_funds: 可用资金
        panic_sell_volume: 恐慌抛售量

    Returns:
        dict: 流动性供给分析
    """
    if panic_sell_volume == 0:
        liquidity_supply = float('inf')
    else:
        liquidity_supply = available_funds / panic_sell_volume

    if liquidity_supply < 0.2:
        status = "critical"
        warning = "流动性严重枯竭"
    elif liquidity_supply < 0.3:
        status = "severe"
        warning = "流动性严重不足"
    elif liquidity_supply < 0.5:
        status = "moderate"
        warning = "流动性不足"
    else:
        status = "normal"
        warning = "流动性充足"

    return {
        "liquidity_supply": liquidity_supply,
        "available_funds": available_funds,
        "panic_sell_volume": panic_sell_volume,
        "status": status,
        "warning": warning
    }


def evaluate_liquidity_risk(spread, order_imbalance, liquidity_demand=None, liquidity_supply=None):
    """
    评估整体流动性风险

    Args:
        spread: 价差信息
        order_imbalance: 订单不平衡信息
        liquidity_demand: 流动性需求（可选）
        liquidity_supply: 流动性供给（可选）

    Returns:
        dict: 整体风险评估
    """
    warnings = []
    risk_factors = []

    # 价差评估
    if spread["spread_percentage"] > 5:
        warnings.append(f"买卖价差过大（{spread['spread_percentage']:.2f}%），流动性极差")
        risk_factors.append("high_spread")
    elif spread["spread_percentage"] > 1:
        warnings.append(f"买卖价差较大（{spread['spread_percentage']:.2f}%），流动性较差")
        risk_factors.append("moderate_spread")

    # 订单不平衡评估
    if order_imbalance["imbalance_ratio"] > 0.5:
        warnings.append(f"订单严重不平衡（{order_imbalance['imbalance_ratio']:.2%}），{order_imbalance['direction']}")
        risk_factors.append("severe_imbalance")
    elif order_imbalance["imbalance_ratio"] > 0.2:
        warnings.append(f"订单轻微不平衡（{order_imbalance['imbalance_ratio']:.2%}），{order_imbalance['direction']}")
        risk_factors.append("moderate_imbalance")

    # 流动性需求评估
    if liquidity_demand:
        if liquidity_demand["status"] in ["critical", "severe"]:
            warnings.append(liquidity_demand["warning"])
            risk_factors.append(f"{liquidity_demand['status']}_demand")

    # 流动性供给评估
    if liquidity_supply:
        if liquidity_supply["status"] in ["critical", "severe"]:
            warnings.append(liquidity_supply["warning"])
            risk_factors.append(f"{liquidity_supply['status']}_supply")

    # 综合风险评级
    num_critical = sum(1 for factor in risk_factors if "critical" in factor)
    num_severe = sum(1 for factor in risk_factors if "severe" in factor)
    num_moderate = sum(1 for factor in risk_factors if "moderate" in factor)

    if num_critical >= 1 or num_severe >= 2:
        overall_risk = "critical"
        action = "立即撤资"
    elif num_severe >= 1 or num_moderate >= 3:
        overall_risk = "severe"
        action = "警惕，考虑撤资"
    elif num_moderate >= 1:
        overall_risk = "moderate"
        action = "关注"
    else:
        overall_risk = "low"
        action = "正常"

    return {
        "overall_risk": overall_risk,
        "action": action,
        "warnings": warnings,
        "risk_factors": risk_factors,
        "risk_count": {
            "critical": num_critical,
            "severe": num_severe,
            "moderate": num_moderate
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='流动性分析工具 - 分析订单簿、流动性需求和供给',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本订单簿分析
  python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.05 --bid-volume 10000 --ask-volume 5000

  # 完整流动性分析（包含流动性需求和供给）
  python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.05 --bid-volume 10000 --ask-volume 5000 --panic-sell-volume 30000 --normal-volume 5000 --available-funds 10000

  # 高风险案例
  python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.50 --bid-volume 1000 --ask-volume 10000 --panic-sell-volume 30000 --normal-volume 5000 --available-funds 5000
        """
    )

    parser.add_argument(
        '--bid-price',
        type=float,
        required=True,
        help='最高买价'
    )

    parser.add_argument(
        '--ask-price',
        type=float,
        required=True,
        help='最低卖价'
    )

    parser.add_argument(
        '--bid-volume',
        type=float,
        required=True,
        help='买入总量'
    )

    parser.add_argument(
        '--ask-volume',
        type=float,
        required=True,
        help='卖出总量'
    )

    parser.add_argument(
        '--panic-sell-volume',
        type=float,
        help='恐慌抛售量（可选，用于计算流动性需求）'
    )

    parser.add_argument(
        '--normal-volume',
        type=float,
        help='正常成交量（可选，用于计算流动性需求）'
    )

    parser.add_argument(
        '--available-funds',
        type=float,
        help='可用资金（可选，用于计算流动性供给）'
    )

    args = parser.parse_args()

    try:
        # 基本分析
        spread = calculate_spread(args.bid_price, args.ask_price)
        order_imbalance = calculate_order_imbalance(args.bid_volume, args.ask_volume)

        result = {
            "status": "success",
            "spread": spread,
            "order_imbalance": order_imbalance
        }

        # 流动性需求和供给分析（如果提供了参数）
        if args.panic_sell_volume and args.normal_volume:
            result["liquidity_demand"] = analyze_liquidity_demand(
                args.panic_sell_volume,
                args.normal_volume
            )

        if args.available_funds and args.panic_sell_volume:
            result["liquidity_supply"] = analyze_liquidity_supply(
                args.available_funds,
                args.panic_sell_volume
            )

        # 综合风险评估
        result["risk_assessment"] = evaluate_liquidity_risk(
            spread,
            order_imbalance,
            result.get("liquidity_demand"),
            result.get("liquidity_supply")
        )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"分析失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
