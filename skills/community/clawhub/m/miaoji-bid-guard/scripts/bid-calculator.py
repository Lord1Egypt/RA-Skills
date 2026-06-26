#!/usr/bin/env python3
"""
Amazon Bid Calculator & Budget Simulator
Calculates optimal bid ranges, simulates budget scenarios, and generates
bid guardrails for different keyword positions.

Usage:
    python bid-calculator.py --daily-budget 50 --target-acos 18 \
        --avg-cpc 1.2 --conv-rate 0.10 --avg-order-value 25 --product-margin 40

    python bid-calculator.py --input '{"daily_budget":50,"target_acos":18,"avg_cpc":1.2,"conv_rate":0.10,"aov":25,"margin":40}'
"""

import argparse
import json
import sys
from datetime import datetime


# ── Calculation Functions ────────────────────────────────────────

def calc_max_cpc(aov: float, conv_rate: float, target_acos: float) -> float:
    """Maximum CPC to maintain target ACoS.
    Max CPC = AOV * Conv Rate * (Target ACoS / 100)
    """
    return round(aov * conv_rate * (target_acos / 100), 2)


def calc_profitable_cpc(aov: float, conv_rate: float, margin: float) -> float:
    """Maximum CPC before losing money.
    Profitable CPC = AOV * Conv Rate * (Margin / 100)
    """
    return round(aov * conv_rate * (margin / 100), 2)


def calc_break_even_acos(margin: float) -> float:
    """ACoS at which you make zero profit = Margin."""
    return margin


def calc_daily_clicks(daily_budget: float, avg_cpc: float) -> float:
    """Estimated daily clicks from budget."""
    if avg_cpc == 0:
        return 0
    return round(daily_budget / avg_cpc, 1)


def calc_daily_orders(daily_clicks: float, conv_rate: float) -> float:
    """Estimated daily orders."""
    return round(daily_clicks * conv_rate, 1)


def calc_daily_revenue(daily_orders: float, aov: float) -> float:
    """Estimated daily revenue."""
    return round(daily_orders * aov, 2)


def calc_actual_acos(daily_budget: float, daily_revenue: float) -> float:
    """Actual ACoS from daily budget and revenue."""
    if daily_revenue == 0:
        return 0
    return round((daily_budget / daily_revenue) * 100, 1)


def simulate_budget_scenarios(daily_budget: float, avg_cpc: float,
                               conv_rate: float, aov: float, margin: float) -> list:
    """Simulate multiple budget levels."""
    multipliers = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    scenarios = []
    for m in multipliers:
        budget = round(daily_budget * m, 2)
        clicks = calc_daily_clicks(budget, avg_cpc)
        orders = calc_daily_orders(clicks, conv_rate)
        revenue = calc_daily_revenue(orders, aov)
        acos = calc_actual_acos(budget, revenue)
        profit = round(revenue * margin / 100 - budget, 2)
        scenarios.append({
            "budget_level": f"{int(m*100)}%",
            "daily_budget": budget,
            "est_clicks": clicks,
            "est_orders": orders,
            "est_revenue": revenue,
            "est_acos": acos,
            "est_daily_profit": profit,
        })
    return scenarios


def generate_bid_guardrails(max_cpc: float, profitable_cpc: float, avg_cpc: float) -> dict:
    """Generate bid guardrails for different positions."""
    return {
        "max_safe_bid": profitable_cpc,
        "target_bid": max_cpc,
        "top_of_search_bid": round(min(max_cpc * 1.3, profitable_cpc), 2),
        "first_page_bid": round(min(max_cpc * 0.8, profitable_cpc * 0.9), 2),
        "rest_of_search_bid": round(min(max_cpc * 0.4, profitable_cpc * 0.5), 2),
        "bid_ceiling": profitable_cpc,
        "current_vs_safe": "WITHIN LIMIT" if avg_cpc <= profitable_cpc else "EXCEEDING LIMIT",
    }


def generate_bid_rules(target_acos: float, margin: float, max_cpc: float, avg_cpc: float) -> list:
    """Generate actionable bid rules."""
    rules = []

    # Rule 1: ACoS vs Margin check
    if target_acos > margin * 0.8:
        rules.append({
            "rule": "ACOS_MARGIN_CHECK",
            "severity": "warning",
            "message": f"Target ACoS ({target_acos}%) is close to margin ({margin}%) — little room for error",
        })

    # Rule 2: Current CPC vs safe CPC
    if avg_cpc > max_cpc:
        rules.append({
            "rule": "CPC_OVER_TARGET",
            "severity": "critical",
            "message": f"Current CPC (${avg_cpc}) exceeds target max CPC (${max_cpc}) — reduce bids immediately",
        })

    # Rule 3: Flywheel bid reduction
    rules.append({
        "rule": "FLYWHEEL_BID_ADJUST",
        "severity": "info",
        "message": f"For organic flywheel: reduce bids on keywords with >3% conv rate by 10-15% to shift spend to organic",
    })

    # Rule 4: Position-specific bid
    rules.append({
        "rule": "POSITION_BID_STRATEGY",
        "severity": "info",
        "message": f"Top of Search premium: bid up to ${round(max_cpc * 1.3, 2)} only for keywords with >8% conv rate",
    })

    return rules


def analyze(params: dict) -> dict:
    """Run full bid analysis."""
    daily_budget = float(params.get("daily_budget", 50))
    target_acos = float(params.get("target_acos", 18))
    avg_cpc = float(params.get("avg_cpc", 1.0))
    conv_rate = float(params.get("conv_rate", 0.10))
    aov = float(params.get("aov", 25))
    margin = float(params.get("margin", 40))

    # Core calculations
    max_cpc = calc_max_cpc(aov, conv_rate, target_acos)
    profitable_cpc = calc_profitable_cpc(aov, conv_rate, margin)
    break_even_acos = calc_break_even_acos(margin)

    daily_clicks = calc_daily_clicks(daily_budget, avg_cpc)
    daily_orders = calc_daily_orders(daily_clicks, conv_rate)
    daily_revenue = calc_daily_revenue(daily_orders, aov)
    actual_acos = calc_actual_acos(daily_budget, daily_revenue)

    # Advanced
    guardrails = generate_bid_guardrails(max_cpc, profitable_cpc, avg_cpc)
    scenarios = simulate_budget_scenarios(daily_budget, avg_cpc, conv_rate, aov, margin)
    rules = generate_bid_rules(target_acos, margin, max_cpc, avg_cpc)

    return {
        "inputs": {
            "daily_budget": daily_budget,
            "target_acos": target_acos,
            "avg_cpc": avg_cpc,
            "conv_rate": conv_rate,
            "aov": aov,
            "margin": margin,
        },
        "core_metrics": {
            "max_cpc_for_target_acos": max_cpc,
            "profitable_cpc_limit": profitable_cpc,
            "break_even_acos": break_even_acos,
            "actual_acos": actual_acos,
            "daily_clicks": daily_clicks,
            "daily_orders": daily_orders,
            "daily_revenue": daily_revenue,
        },
        "guardrails": guardrails,
        "budget_scenarios": scenarios,
        "bid_rules": rules,
        "timestamp": datetime.now().isoformat(),
    }


def format_report(result: dict) -> str:
    """Format analysis result as readable report."""
    inp = result["inputs"]
    core = result["core_metrics"]
    guard = result["guardrails"]

    lines = []
    lines.append("🛡️ 竞价护栏报告")
    lines.append("━" * 40)
    lines.append("")
    lines.append("【输入参数】")
    lines.append(f"  日预算：${inp['daily_budget']}")
    lines.append(f"  目标ACoS：{inp['target_acos']}%")
    lines.append(f"  当前CPC：${inp['avg_cpc']}")
    lines.append(f"  转化率：{inp['conv_rate']*100:.0f}%")
    lines.append(f"  客单价：${inp['aov']}")
    lines.append(f"  毛利率：{inp['margin']}%")
    lines.append("")

    lines.append("【核心指标】")
    lines.append(f"  目标ACoS对应最高CPC：${core['max_cpc_for_target_acos']}")
    lines.append(f"  盈利线CPC（不亏钱）：${core['profitable_cpc_limit']}")
    lines.append(f"  盈亏平衡ACoS：{core['break_even_acos']}%")
    lines.append(f"  当前预估ACoS：{core['actual_acos']}%")
    lines.append(f"  日预估点击：{core['daily_clicks']}")
    lines.append(f"  日预估订单：{core['daily_orders']}")
    lines.append(f"  日预估收入：${core['daily_revenue']}")
    lines.append("")

    lines.append("【竞价护栏】")
    status_emoji = "🟢" if guard["current_vs_safe"] == "WITHIN LIMIT" else "🔴"
    lines.append(f"  当前状态：{status_emoji} {guard['current_vs_safe']}")
    lines.append(f"  搜索顶部出价上限：${guard['top_of_search_bid']}")
    lines.append(f"  首页出价上限：${guard['first_page_bid']}")
    lines.append(f"  其余位置出价上限：${guard['rest_of_search_bid']}")
    lines.append(f"  绝对出价上限：${guard['bid_ceiling']}")
    lines.append("")

    lines.append("【预算模拟】")
    for s in result["budget_scenarios"]:
        profit_emoji = "📈" if s["est_daily_profit"] > 0 else "📉"
        lines.append(f"  {s['budget_level']:>4} | 预算${s['daily_budget']:>6} | 点击{s['est_clicks']:>5} | "
                     f"订单{s['est_orders']:>4} | ACoS {s['est_acos']:>5}% | {profit_emoji} ${s['est_daily_profit']}")
    lines.append("")

    lines.append("【竞价规则】")
    for r in result["bid_rules"]:
        sev = {"critical": "🔴", "warning": "🟡", "info": "ℹ️"}.get(r["severity"], "⚪")
        lines.append(f"  {sev} {r['message']}")

    lines.append("")
    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Amazon Bid Calculator & Budget Simulator")
    parser.add_argument("--daily-budget", type=float, default=50, help="Daily ad budget")
    parser.add_argument("--target-acos", type=float, default=18, help="Target ACoS %")
    parser.add_argument("--avg-cpc", type=float, default=1.0, help="Current average CPC")
    parser.add_argument("--conv-rate", type=float, default=0.10, help="Conversion rate (0-1)")
    parser.add_argument("--aov", type=float, default=25, help="Average order value")
    parser.add_argument("--margin", type=float, default=40, help="Product margin %")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    if args.input:
        params = json.loads(args.input)
    else:
        params = {
            "daily_budget": args.daily_budget,
            "target_acos": args.target_acos,
            "avg_cpc": args.avg_cpc,
            "conv_rate": args.conv_rate,
            "aov": args.aov,
            "margin": args.margin,
        }

    result = analyze(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
