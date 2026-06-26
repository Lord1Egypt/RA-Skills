#!/usr/bin/env python3
"""
风险指标计算器
计算夏普比率、最大回撤、VaR、索提诺比率等风险指标
"""

import argparse
import json
import math
import sys


def calculate_returns(prices):
    """
    从价格序列计算收益率序列

    Args:
        prices: 价格列表

    Returns:
        list: 收益率列表
    """
    returns = []
    for i in range(1, len(prices)):
        ret = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(ret)
    return returns


def calculate_mean(returns):
    """计算平均值"""
    return sum(returns) / len(returns) if returns else 0


def calculate_std(returns):
    """计算标准差"""
    if len(returns) < 2:
        return 0
    mean = calculate_mean(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    return math.sqrt(variance)


def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
    """
    计算夏普比率

    Args:
        returns: 收益率列表（年化收益率）
        risk_free_rate: 无风险收益率（年化）

    Returns:
        float: 夏普比率
    """
    mean_return = calculate_mean(returns)
    std_return = calculate_std(returns)

    if std_return == 0:
        return 0

    excess_return = mean_return - risk_free_rate
    sharpe = excess_return / std_return
    return sharpe


def calculate_max_drawdown(prices):
    """
    计算最大回撤

    Args:
        prices: 价格列表

    Returns:
        dict: 包含最大回撤及其相关信息
    """
    if not prices:
        return {"max_drawdown": 0, "peak_index": -1, "trough_index": -1}

    max_drawdown = 0
    peak_index = 0
    trough_index = 0
    current_peak = prices[0]
    current_peak_index = 0

    for i in range(1, len(prices)):
        if prices[i] > current_peak:
            current_peak = prices[i]
            current_peak_index = i

        drawdown = (current_peak - prices[i]) / current_peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
            peak_index = current_peak_index
            trough_index = i

    return {
        "max_drawdown": max_drawdown,
        "peak_index": peak_index,
        "trough_index": trough_index,
        "peak_value": prices[peak_index] if prices else 0,
        "trough_value": prices[trough_index] if prices else 0
    }


def calculate_var(returns, confidence_level=0.95):
    """
    计算VaR（参数法）

    Args:
        returns: 收益率列表
        confidence_level: 置信水平

    Returns:
        dict: 包含VaR和CVaR
    """
    if not returns:
        return {"var": 0, "cvar": 0}

    # 参数法：假设正态分布
    mean = calculate_mean(returns)
    std = calculate_std(returns)

    # Z分数
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
    z = z_scores.get(confidence_level, 1.65)

    # 计算VaR
    var = mean - z * std

    # 计算CVaR（条件风险价值）
    # CVaR是超过VaR的平均损失
    threshold_returns = [r for r in returns if r < var]
    cvar = sum(threshold_returns) / len(threshold_returns) if threshold_returns else var

    return {
        "var": var,
        "cvar": cvar,
        "confidence_level": confidence_level
    }


def calculate_sortino_ratio(returns, mar=0.0):
    """
    计算索提诺比率

    Args:
        returns: 收益率列表
        mar: 最低可接受收益率（Minimum Acceptable Return）

    Returns:
        float: 索提诺比率
    """
    mean_return = calculate_mean(returns)

    # 计算下行标准差（只计算负收益）
    downside_returns = [r for r in returns if r < mar]
    if len(downside_returns) == 0:
        return float('inf') if mean_return > mar else 0

    downside_std = calculate_std(downside_returns)

    if downside_std == 0:
        return 0

    sortino = (mean_return - mar) / downside_std
    return sortino


def calculate_all_metrics(prices, returns=None, risk_free_rate=0.03, confidence_level=0.95, mar=0.0):
    """
    计算所有风险指标

    Args:
        prices: 价格列表（可选，用于计算最大回撤）
        returns: 收益率列表（如果提供则直接使用，否则从prices计算）
        risk_free_rate: 无风险收益率
        confidence_level: VaR置信水平
        mar: 最低可接受收益率

    Returns:
        dict: 所有风险指标
    """
    # 如果没有提供returns，从prices计算
    if returns is None:
        if prices is None or len(prices) < 2:
            return {"status": "error", "message": "需要提供prices或returns"}
        returns = calculate_returns(prices)

    if len(returns) == 0:
        return {"status": "error", "message": "无法计算收益率"}

    result = {
        "status": "success",
        "basic_stats": {
            "mean_return": calculate_mean(returns),
            "std_return": calculate_std(returns),
            "num_observations": len(returns)
        },
        "sharpe_ratio": calculate_sharpe_ratio(returns, risk_free_rate),
        "sortino_ratio": calculate_sortino_ratio(returns, mar),
        "var": calculate_var(returns, confidence_level)
    }

    # 如果提供了prices，计算最大回撤
    if prices is not None:
        result["max_drawdown"] = calculate_max_drawdown(prices)

    # 生成评估和建议
    warnings = []
    recommendations = []

    # 夏普比率评估
    if result["sharpe_ratio"] < 0:
        warnings.append("夏普比率小于0，收益低于无风险收益。")
    elif result["sharpe_ratio"] < 0.5:
        recommendations.append("夏普比率较低，风险调整后收益一般。")
    elif result["sharpe_ratio"] > 2.0:
        warnings.append("夏普比率异常高（>2），可能存在风险低估或数据问题。")

    # 最大回撤评估
    if "max_drawdown" in result:
        if result["max_drawdown"]["max_drawdown"] > 0.5:
            warnings.append(f"最大回撤超过50%（{result['max_drawdown']['max_drawdown']:.2%}），风险极高。")
        elif result["max_drawdown"]["max_drawdown"] > 0.3:
            recommendations.append(f"最大回撤较高（{result['max_drawdown']['max_drawdown']:.2%}），需要严格控制仓位。")

    # VaR评估
    var_cvar_ratio = abs(result["var"]["cvar"] / result["var"]["var"]) if result["var"]["var"] != 0 else 1
    if var_cvar_ratio > 3:
        warnings.append(f"CVaR是VaR的{var_cvar_ratio:.1f}倍，尾部风险严重。")

    # 索提诺比率与夏普比率对比
    if result["sharpe_ratio"] > 0:
        sortino_sharpe_diff = abs(result["sortino_ratio"] - result["sharpe_ratio"]) / result["sharpe_ratio"]
        if sortino_sharpe_diff > 1.0:
            warnings.append("索提诺比率显著低于夏普比率，下行风险严重。")

    result["warnings"] = warnings
    result["recommendations"] = recommendations

    return result


def main():
    parser = argparse.ArgumentParser(
        description='风险指标计算器 - 计算夏普比率、最大回撤、VaR、索提诺比率',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用价格序列计算所有指标
  python scripts/risk_metrics.py --prices '[100,105,110,108,112,115,113,118]'

  # 使用收益率序列计算（不计算最大回撤）
  python scripts/risk_metrics.py --returns '[0.05,0.0476,-0.0182,0.037,0.0268,-0.0174,0.0442]'

  # 自定义参数
  python scripts/risk_metrics.py --prices '[100,105,110,108,112]' --risk-free-rate 0.02 --confidence-level 0.99
        """
    )

    parser.add_argument(
        '--prices',
        type=str,
        help='价格列表（JSON格式，例如"[100,105,110,108,112]"）'
    )

    parser.add_argument(
        '--returns',
        type=str,
        help='收益率列表（JSON格式，例如"[0.05,0.0476,-0.0182]"）'
    )

    parser.add_argument(
        '--risk-free-rate',
        type=float,
        default=0.03,
        help='无风险收益率（默认0.03，即3%）'
    )

    parser.add_argument(
        '--confidence-level',
        type=float,
        choices=[0.90, 0.95, 0.99],
        default=0.95,
        help='VaR置信水平（默认0.95）'
    )

    parser.add_argument(
        '--mar',
        type=float,
        default=0.0,
        help='最低可接受收益率，用于计算索提诺比率（默认0.0）'
    )

    args = parser.parse_args()

    try:
        # 解析输入数据
        prices = None
        returns = None

        if args.prices:
            prices = json.loads(args.prices)

        if args.returns:
            returns = json.loads(args.returns)

        # 计算指标
        result = calculate_all_metrics(
            prices=prices,
            returns=returns,
            risk_free_rate=args.risk_free_rate,
            confidence_level=args.confidence_level,
            mar=args.mar
        )

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"JSON解析错误: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"计算失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
