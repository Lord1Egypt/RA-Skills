#!/usr/bin/env python3
"""
human-stock-helper 核心脚本
股票交易辅助工具 - 技术分析与策略计算
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def calculate_take_profit_levels(entry_price, shares, risk_reward_ratio=3):
    """
    计算分批止盈位
    
    Args:
        entry_price: 建仓价格
        shares: 持股数量
        risk_reward_ratio: 盈亏比（默认3:1）
    
    Returns:
        dict: 三档止盈位信息
    """
    levels = {
        "entry": {
            "price": entry_price,
            "shares": shares,
            "total_value": entry_price * shares
        },
        "level_1": {
            "price": round(entry_price * 1.08, 2),  # +8%
            "shares": shares // 3,
            "profit_per_share": round(entry_price * 0.08, 2),
            "total_profit": round(entry_price * 0.08 * (shares // 3), 2)
        },
        "level_2": {
            "price": round(entry_price * 1.15, 2),  # +15%
            "shares": shares // 3,
            "profit_per_share": round(entry_price * 0.15, 2),
            "total_profit": round(entry_price * 0.15 * (shares // 3), 2)
        },
        "level_3": {
            "price": round(entry_price * 1.25, 2),  # +25%
            "shares": shares - 2 * (shares // 3),  # 剩余股数
            "profit_per_share": round(entry_price * 0.25, 2),
            "total_profit": round(entry_price * 0.25 * (shares - 2 * (shares // 3)), 2)
        }
    }
    
    # 计算总预期收益
    total_profit = sum([
        levels["level_1"]["total_profit"],
        levels["level_2"]["total_profit"],
        levels["level_3"]["total_profit"]
    ])
    levels["total_expected_profit"] = round(total_profit, 2)
    levels["total_expected_return"] = round(total_profit / (entry_price * shares) * 100, 2)
    
    return levels


def calculate_stop_loss(entry_price, current_price=None, method="breakeven"):
    """
    计算止损位
    
    Args:
        entry_price: 建仓价格
        current_price: 当前价格（可选）
        method: 止损方法（breakeven: 保本, fixed: 固定百分比, trailing: 移动止损）
    
    Returns:
        dict: 止损位信息
    """
    if method == "breakeven":
        # 保本止损：设置在成本线下方1-2%
        stop_price = round(entry_price * 0.982, 2)  # -1.8%
        return {
            "method": "保本止损",
            "stop_price": stop_price,
            "stop_loss_percent": -1.8,
            "max_loss_amount": round((stop_price - entry_price), 2)
        }
    
    elif method == "fixed":
        # 固定比例止损：-5%或-8%
        stop_price = round(entry_price * 0.92, 2)  # -8%
        return {
            "method": "固定比例止损",
            "stop_price": stop_price,
            "stop_loss_percent": -8,
            "max_loss_amount": round((stop_price - entry_price), 2)
        }
    
    elif method == "trailing" and current_price:
        # 移动止损：盈利后上移止损位
        if current_price > entry_price * 1.05:  # 盈利超过5%
            stop_price = round(entry_price * 1.02, 2)  # 上移至成本线上方2%
            return {
                "method": "移动止损（盈利保护）",
                "stop_price": stop_price,
                "stop_loss_percent": round((stop_price - current_price) / current_price * 100, 2),
                "guaranteed_profit": round((stop_price - entry_price), 2)
            }
        else:
            return calculate_stop_loss(entry_price, method="breakeven")
    
    return calculate_stop_loss(entry_price, method="breakeven")


def analyze_position(stock_code, stock_name, entry_price, shares, holding_days, current_price=None):
    """
    综合分析持仓情况
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        entry_price: 建仓价格
        shares: 持股数量
        holding_days: 已持有天数
        current_price: 当前价格（可选）
    
    Returns:
        dict: 完整分析报告
    """
    position_value = entry_price * shares
    
    # 止盈位计算
    take_profit = calculate_take_profit_levels(entry_price, shares)
    
    # 止损位计算
    stop_loss = calculate_stop_loss(entry_price, current_price, method="trailing" if current_price else "breakeven")
    
    # 当前盈亏计算
    if current_price:
        unrealized_pnl = round((current_price - entry_price) * shares, 2)
        unrealized_pnl_pct = round((current_price - entry_price) / entry_price * 100, 2)
    else:
        unrealized_pnl = None
        unrealized_pnl_pct = None
    
    analysis = {
        "stock": {
            "code": stock_code,
            "name": stock_name
        },
        "position": {
            "entry_price": entry_price,
            "shares": shares,
            "position_value": position_value,
            "holding_days": holding_days,
            "current_price": current_price
        },
        "pnl": {
            "unrealized_pnl": unrealized_pnl,
            "unrealized_pnl_pct": unrealized_pnl_pct
        },
        "strategy": {
            "take_profit_levels": take_profit,
            "stop_loss": stop_loss
        },
        "recommendations": []
    }
    
    # 生成操作建议
    recommendations = []
    
    if current_price:
        if unrealized_pnl_pct and unrealized_pnl_pct >= 8:
            recommendations.append({
                "priority": "high",
                "action": "减仓1/3",
                "trigger_price": take_profit["level_1"]["price"],
                "reason": f"已盈利{unrealized_pnl_pct}%，达到第一止盈位，建议减仓锁定利润"
            })
        
        if unrealized_pnl_pct and unrealized_pnl_pct >= 0:
            recommendations.append({
                "priority": "medium",
                "action": "上移止损位",
                "trigger_price": stop_loss["stop_price"],
                "reason": "已建立盈利，止损位上移至成本线附近保本"
            })
        else:
            recommendations.append({
                "priority": "high",
                "action": "严格执行止损",
                "trigger_price": stop_loss["stop_price"],
                "reason": "跌破止损位无条件离场"
            })
    
    if holding_days > 30 and (unrealized_pnl_pct is None or unrealized_pnl_pct < 5):
        recommendations.append({
            "priority": "low",
            "action": "时间止损",
            "reason": "持有满30天未达预期收益，考虑资金时间成本"
        })
    
    analysis["recommendations"] = recommendations
    
    return analysis


def format_analysis_report(analysis):
    """格式化分析报告"""
    lines = []
    lines.append("=" * 50)
    lines.append(f"📈 {analysis['stock']['name']} ({analysis['stock']['code']}) 交易分析")
    lines.append("=" * 50)
    
    # 持仓信息
    pos = analysis['position']
    lines.append(f"\n【持仓情况】")
    lines.append(f"建仓价: {pos['entry_price']}元")
    lines.append(f"持股数: {pos['shares']}股")
    lines.append(f"持仓市值: {pos['position_value']:,.0f}元")
    lines.append(f"已持有: {pos['holding_days']}天")
    if pos['current_price']:
        lines.append(f"当前价: {pos['current_price']}元")
    
    # 盈亏情况
    pnl = analysis['pnl']
    if pnl['unrealized_pnl'] is not None:
        lines.append(f"\n【当前盈亏】")
        lines.append(f"浮动盈亏: {pnl['unrealized_pnl']:+.2f}元")
        lines.append(f"盈亏比例: {pnl['unrealized_pnl_pct']:+.2f}%")
    
    # 止盈策略
    tp = analysis['strategy']['take_profit_levels']
    lines.append(f"\n【分批止盈策略】")
    lines.append(f"第一档: {tp['level_1']['price']}元 (+8%) → 卖出{tp['level_1']['shares']}股")
    lines.append(f"第二档: {tp['level_2']['price']}元 (+15%) → 卖出{tp['level_2']['shares']}股")
    lines.append(f"第三档: {tp['level_3']['price']}元 (+25%) → 卖出{tp['level_3']['shares']}股")
    lines.append(f"预期总收益: {tp['total_expected_profit']:.2f}元 ({tp['total_expected_return']:+.2f}%)")
    
    # 止损策略
    sl = analysis['strategy']['stop_loss']
    lines.append(f"\n【止损策略】")
    lines.append(f"止损方法: {sl['method']}")
    lines.append(f"止损价位: {sl['stop_price']}元 ({sl['stop_loss_percent']}%)")
    
    # 操作建议
    if analysis['recommendations']:
        lines.append(f"\n【操作建议】")
        for rec in analysis['recommendations']:
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
            lines.append(f"{priority_emoji} [{rec['action']}]")
            if 'trigger_price' in rec:
                lines.append(f"   触发价: {rec['trigger_price']}元")
            lines.append(f"   理由: {rec['reason']}")
    
    lines.append("\n" + "=" * 50)
    lines.append("冰冷执行，积小利。不贪恋，不悔恨。")
    lines.append("=" * 50)
    
    return "\n".join(lines)


def main():
    """主函数 - 命令行入口"""
    if len(sys.argv) < 5:
        print("Usage: python3 stock_helper.py <stock_code> <stock_name> <entry_price> <shares> [holding_days] [current_price]")
        print("Example: python3 stock_helper.py 600089 特变电工 28.51 300 15 30.34")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    stock_name = sys.argv[2]
    entry_price = float(sys.argv[3])
    shares = int(sys.argv[4])
    holding_days = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    current_price = float(sys.argv[6]) if len(sys.argv) > 6 else None
    
    analysis = analyze_position(stock_code, stock_name, entry_price, shares, holding_days, current_price)
    report = format_analysis_report(analysis)
    
    print(report)
    
    # 同时输出JSON格式供程序调用
    print("\n\n---JSON---")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()