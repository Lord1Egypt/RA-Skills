#!/usr/bin/env python3
"""
AI算力销售定价引擎
支持数量/时长/预付三重折扣累乘
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional

# GPU 基础定价（$/hr）
BASE_PRICES = {
    "H100": 2.5,
    "A100-80GB": 1.8,
    "A100-40GB": 1.2,
    "L40S": 0.8,
    "A10G": 0.5,
}

# 折扣规则
QUANTITY_DISCOUNTS = [
    (500, 0.20),   # 500+ 卡 → 20%
    (101, 0.15),   # 101-500 卡 → 15%
    (51, 0.10),    # 51-100 卡 → 10%
    (10, 0.05),    # 10-50 卡 → 5%
]

DURATION_DISCOUNTS = [
    (36, 0.15),    # 3年+ → 15%
    (24, 0.10),    # 2年+ → 10%
    (12, 0.05),    # 1年+ → 5%
]

PREPAY_DISCOUNTS = {
    "year":  0.10,   # 年付 → 10%
    "half":  0.05,   # 半年 → 5%
    "quarter": 0.03, # 季度 → 3%
    "month": 0.00,   # 月付 → 0%
}


@dataclass
class PricingResult:
    gpu: str
    base_price_per_hr: float
    gpu_count: int
    duration_months: int
    prepay_cycle: str
    base_monthly: float
    base_yearly: float
    quantity_discount: float  # 折扣率
    duration_discount: float
    prepay_discount: float
    combined_discount: float  # 累乘后的总折扣
    discounted_monthly: float
    discounted_yearly: float
    monthly_savings: float
    yearly_savings: float
    price_per_gpu_hr: float


def get_quantity_discount(count: int) -> float:
    """根据GPU数量返回折扣率"""
    for threshold, discount in QUANTITY_DISCOUNTS:
        if count >= threshold:
            return discount
    return 0.0


def get_duration_discount(months: int) -> float:
    """根据合同期限返回折扣率"""
    for threshold, discount in DURATION_DISCOUNTS:
        if months >= threshold:
            return discount
    return 0.0


def get_prepay_discount(prepay: str) -> float:
    """根据预付周期返回折扣率"""
    return PREPAY_DISCOUNTS.get(prepay.lower(), 0.0)


def calculate_pricing(
    gpu: str,
    count: int,
    duration_months: int,
    prepay_cycle: str,
) -> PricingResult:
    """计算最终定价"""
    if gpu not in BASE_PRICES:
        raise ValueError(f"不支持的GPU型号: {gpu}，支持的型号: {list(BASE_PRICES.keys())}")

    base_price_per_hr = BASE_PRICES[gpu]
    base_monthly = base_price_per_hr * count * 730  # ~730小时/月
    base_yearly = base_monthly * 12

    q_discount = get_quantity_discount(count)
    d_discount = get_duration_discount(duration_months)
    p_discount = get_prepay_discount(prepay_cycle)

    # 累乘折扣 (1 - d1) * (1 - d2) * (1 - d3)
    combined = 1.0 - (1.0 - q_discount) * (1.0 - d_discount) * (1.0 - p_discount)

    discounted_monthly = base_monthly * (1.0 - combined)
    discounted_yearly = discounted_monthly * 12

    return PricingResult(
        gpu=gpu,
        base_price_per_hr=base_price_per_hr,
        gpu_count=count,
        duration_months=duration_months,
        prepay_cycle=prepay_cycle,
        base_monthly=base_monthly,
        base_yearly=base_yearly,
        quantity_discount=q_discount,
        duration_discount=d_discount,
        prepay_discount=p_discount,
        combined_discount=combined,
        discounted_monthly=discounted_monthly,
        discounted_yearly=discounted_yearly,
        monthly_savings=base_monthly - discounted_monthly,
        yearly_savings=base_yearly - discounted_yearly,
        price_per_gpu_hr=base_price_per_hr * (1.0 - combined),
    )


def format_result(result: PricingResult) -> str:
    """格式化输出结果"""
    lines = []
    lines.append("=" * 56)
    lines.append("  AI算力阶梯折扣报价单")
    lines.append("=" * 56)
    lines.append(f"  GPU型号:        {result.gpu}")
    lines.append(f"  GPU数量:        {result.gpu_count} 卡")
    lines.append(f"  合同期限:       {result.duration_months} 个月")
    lines.append(f"  预付周期:       {result.prepay_cycle}")
    lines.append("-" * 56)
    lines.append("  基础价格:")
    lines.append(f"    标准单价:      ${result.base_price_per_hr:.2f}/GPU/hr")
    lines.append(f"    月标准价:      ${result.base_monthly:,.2f}")
    lines.append(f"    年标准价:      ${result.base_yearly:,.2f}")
    lines.append("-" * 56)
    lines.append("  折扣明细:")
    q_pct = result.quantity_discount * 100
    d_pct = result.duration_discount * 100
    p_pct = result.prepay_discount * 100
    lines.append(f"    数量折扣:      {q_pct:.0f}%  (≥{_get_qty_threshold(result.gpu_count)}卡)")
    lines.append(f"    时长折扣:      {d_pct:.0f}%  (≥{_get_dur_threshold(result.duration_months)}个月)")
    lines.append(f"    预付折扣:      {p_pct:.0f}%  ({result.prepay_cycle})")
    c_pct = result.combined_discount * 100
    lines.append(f"    ─────────────────")
    lines.append(f"    综合折扣:      {c_pct:.1f}%")
    lines.append("-" * 56)
    lines.append("  折后价格:")
    lines.append(f"    单价(含折):    ${result.price_per_gpu_hr:.4f}/GPU/hr")
    lines.append(f"    月折后价:      ${result.discounted_monthly:,.2f}")
    lines.append(f"    年折后价:      ${result.discounted_yearly:,.2f}")
    lines.append("-" * 56)
    lines.append("  节省金额:")
    lines.append(f"    月节省:        ${result.monthly_savings:,.2f}")
    lines.append(f"    年节省:        ${result.yearly_savings:,.2f}")
    lines.append("=" * 56)
    return "\n".join(lines)


def _get_qty_threshold(count: int) -> int:
    for threshold, _ in QUANTITY_DISCOUNTS:
        if count >= threshold:
            return threshold
    return 0


def _get_dur_threshold(months: int) -> int:
    for threshold, _ in DURATION_DISCOUNTS:
        if months >= threshold:
            return threshold
    return 0


def list_gpu_prices():
    """列出所有GPU基础价格"""
    print("=" * 40)
    print("  GPU 基础定价表 ($/hr/GPU)")
    print("=" * 40)
    for gpu, price in BASE_PRICES.items():
        monthly = price * 730
        yearly = monthly * 12
        print(f"  {gpu:12s}  ${price:.2f}/hr  →  月${monthly:,.0f} / 年${yearly:,.0f}")
    print("=" * 40)
    print("  备注: 月均按 730 小时计算")
    print()


def compare_scenarios(scenarios_str: str):
    """对比多个方案"""
    scenarios = scenarios_str.split(",")
    results = []

    for s in scenarios:
        parts = s.strip().split("_")
        if len(parts) < 3:
            print(f"⚠️  方案格式错误: {s}，应为 gpu_count_duration 如 h100_100_24")
            continue
        # GPU型号可能是多段(如 a100_80gb)，逐个尝试匹配
        # 格式: a100_80gb_200_36 → gpu=a100_80gb, count=200, duration=36
        matched_gpu = None
        matched_n = 0
        for n in [3, 2, 1]:
            if n < len(parts):
                gpu_key = "".join(parts[:n]).lower().replace("-", "").replace(" ", "")
                for g in BASE_PRICES:
                    g_key = g.lower().replace("-", "").replace(" ", "")
                    if gpu_key == g_key:
                        matched_gpu = g
                        matched_n = n
                        break
                if matched_gpu:
                    break
        if not matched_gpu:
            print(f"⚠️  未知GPU型号: {parts[0]}")
            continue
        try:
            count = int(parts[matched_n])
            duration = int(parts[matched_n + 1])
        except (ValueError, IndexError):
            print(f"⚠️  参数解析错误: {s}")
            continue
        # 默认年付
        r = calculate_pricing(matched_gpu, count, duration, "year")
        results.append((s, r))

    if not results:
        print("无有效方案可对比")
        return

    print()
    print("=" * 90)
    print(f"  {'方案':20s} {'GPU':8s} {'数量':>5s}  {'月标准价':>12s}  {'综合折扣':>8s}  {'月折后价':>12s}  {'年折后价':>12s}")
    print("-" * 90)
    for name, r in results:
        print(f"  {name:20s} {r.gpu:8s} {r.gpu_count:>5d}  ${r.base_monthly:>11,.0f}  {r.combined_discount*100:>7.1f}%  ${r.discounted_monthly:>11,.0f}  ${r.discounted_yearly:>11,.0f}")
    print("=" * 90)


def main():
    parser = argparse.ArgumentParser(
        description="AI算力销售定价引擎 — 阶梯折扣报价计算",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list                          列出所有GPU基础价格
  %(prog)s --gpu H100 --count 100 --duration 24 --prepay year
  %(prog)s --compare --scenarios h100_100_24,a100-80gb_50_12
  %(prog)s --gpu A100-80GB --count 200 --duration 36 --prepay year --json
        """,
    )
    parser.add_argument("--gpu", type=str, help="GPU型号: H100, A100-80GB, A100-40GB, L40S, A10G")
    parser.add_argument("--count", type=int, help="GPU数量")
    parser.add_argument("--duration", type=int, help="合同期限(月份)，支持 1-36+ 月")
    parser.add_argument("--prepay", type=str, default="month",
                        help="预付周期: month / quarter / half / year (默认 month)")
    parser.add_argument("--list", action="store_true", help="列出所有GPU基础价格")
    parser.add_argument("--compare", action="store_true", help="多方案对比模式")
    parser.add_argument("--scenarios", type=str, help="对比方案列表，逗号分隔，格式: gpu_count_duration 如 h100_100_24")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if args.list:
        list_gpu_prices()
        return

    if args.compare:
        if not args.scenarios:
            print("错误: --compare 需要配合 --scenarios 使用")
            sys.exit(1)
        compare_scenarios(args.scenarios)
        return

    if not all([args.gpu, args.count, args.duration is not None]):
        parser.print_help()
        print("\n错误: 需要提供 --gpu, --count, --duration 参数")
        sys.exit(1)

    result = calculate_pricing(args.gpu, args.count, args.duration, args.prepay)

    if args.json:
        output = {
            "gpu": result.gpu,
            "gpu_count": result.gpu_count,
            "duration_months": result.duration_months,
            "prepay_cycle": result.prepay_cycle,
            "base_price_per_hr": result.base_price_per_hr,
            "discounted_price_per_hr": round(result.price_per_gpu_hr, 4),
            "base_monthly": round(result.base_monthly, 2),
            "base_yearly": round(result.base_yearly, 2),
            "discounted_monthly": round(result.discounted_monthly, 2),
            "discounted_yearly": round(result.discounted_yearly, 2),
            "monthly_savings": round(result.monthly_savings, 2),
            "yearly_savings": round(result.yearly_savings, 2),
            "discounts": {
                "quantity": round(result.quantity_discount * 100, 1),
                "duration": round(result.duration_discount * 100, 1),
                "prepay": round(result.prepay_discount * 100, 1),
                "combined": round(result.combined_discount * 100, 1),
            },
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    print(format_result(result))


if __name__ == "__main__":
    main()
