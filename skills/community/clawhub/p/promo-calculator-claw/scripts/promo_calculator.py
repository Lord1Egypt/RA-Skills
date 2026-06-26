#!/usr/bin/env python3
"""
促销方案测算核心脚本
用法：
  python3 promo_calculator.py single --cost 80 --price 199 --discount 0.8 --commission 0.05 --shipping 8 --return-rate 0.08 --marketing 15 --volume 2000
  python3 promo_calculator.py compare --cost 80 --price 199 --discounts 0.7,0.75,0.8,0.85,0.9 --commission 0.05 --shipping 8 --return-rate 0.08 --marketing 15 --volume 2000
  python3 promo_calculator.py breakeven --cost 80 --price 199 --commission 0.05 --shipping 8 --return-rate 0.08 --marketing 15
  python3 promo_calculator.py batch --input products.csv --discounts 0.7,0.75,0.8,0.85,0.9
"""

import argparse
import json
import sys
import csv
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ProductCost:
    purchase_cost: float      # 采购成本
    original_price: float     # 原售价
    commission_rate: float    # 平台佣金率（如0.05表示5%）
    shipping_cost: float      # 物流成本（元/件）
    return_rate: float        # 退货率（如0.08表示8%）
    marketing_cost: float     # 营销成本（元/件）
    storage_cost: float = 0   # 仓储成本（元/件）


@dataclass
class PromoResult:
    discount: float
    promo_price: float
    gross_profit: float       # 毛利润
    net_profit: float         # 净利润
    gross_margin: float       # 毛利率
    net_margin: float         # 净利率
    total_cost: float         # 总成本
    breakeven_volume: Optional[float] = None  # 盈亏平衡销量（需固定成本时）
    total_net_profit: Optional[float] = None  # 总净利润（需销量时）


def calculate_single(cost: ProductCost, discount: float, volume: Optional[float] = None,
                     fixed_cost: float = 0) -> PromoResult:
    """计算单个促销方案的利润"""
    promo_price = cost.original_price * discount

    # 按促销价计算佣金
    commission = promo_price * cost.commission_rate

    # 退货成本 = 退货率 × (采购成本 + 物流成本)
    return_cost = cost.return_rate * (cost.purchase_cost + cost.shipping_cost)

    # 总成本
    total_cost = (cost.purchase_cost + cost.shipping_cost + commission +
                  cost.marketing_cost + return_cost + cost.storage_cost)

    # 毛利润（不含营销、仓储、退货）
    gross_profit = promo_price - cost.purchase_cost - cost.shipping_cost - commission

    # 净利润
    net_profit = promo_price - total_cost

    gross_margin = gross_profit / promo_price if promo_price > 0 else 0
    net_margin = net_profit / promo_price if promo_price > 0 else 0

    result = PromoResult(
        discount=discount,
        promo_price=round(promo_price, 2),
        gross_profit=round(gross_profit, 2),
        net_profit=round(net_profit, 2),
        gross_margin=round(gross_margin * 100, 2),
        net_margin=round(net_margin * 100, 2),
        total_cost=round(total_cost, 2),
    )

    if fixed_cost > 0 and net_profit > 0:
        result.breakeven_volume = round(fixed_cost / net_profit, 0)

    if volume is not None:
        result.total_net_profit = round(net_profit * volume, 2)

    return result


def format_result(r: PromoResult, volume: Optional[float] = None) -> str:
    lines = [
        f"  促销价:    ¥{r.promo_price}",
        f"  总成本:    ¥{r.total_cost}",
        f"  毛利润:    ¥{r.gross_profit}  (毛利率 {r.gross_margin}%)",
        f"  净利润:    ¥{r.net_profit}  (净利率 {r.net_margin}%)",
    ]
    if r.net_profit < 0:
        lines.append(f"  ⚠️  亏损方案！每件亏损 ¥{abs(r.net_profit)}")
    if r.breakeven_volume is not None:
        lines.append(f"  盈亏平衡销量: {int(r.breakeven_volume)} 件")
    if r.total_net_profit is not None:
        lines.append(f"  预期总净利润: ¥{r.total_net_profit:,.0f}（销量 {int(volume)} 件）")
    return "\n".join(lines)


def cmd_single(args):
    cost = ProductCost(
        purchase_cost=args.cost,
        original_price=args.price,
        commission_rate=args.commission,
        shipping_cost=args.shipping,
        return_rate=args.return_rate,
        marketing_cost=args.marketing,
        storage_cost=getattr(args, 'storage', 0),
    )
    r = calculate_single(cost, args.discount, getattr(args, 'volume', None),
                         getattr(args, 'fixed_cost', 0))
    print(f"\n📊 单品促销测算（折扣 {args.discount*100:.0f}折）")
    print(format_result(r, getattr(args, 'volume', None)))
    print()


def cmd_compare(args):
    cost = ProductCost(
        purchase_cost=args.cost,
        original_price=args.price,
        commission_rate=args.commission,
        shipping_cost=args.shipping,
        return_rate=args.return_rate,
        marketing_cost=args.marketing,
        storage_cost=getattr(args, 'storage', 0),
    )
    discounts = [float(d) for d in args.discounts.split(',')]
    volume = getattr(args, 'volume', None)

    print(f"\n📊 多方案对比分析（原价 ¥{args.price}）")
    print("=" * 60)
    print(f"{'折扣':>6} {'促销价':>8} {'净利润':>8} {'净利率':>8} {'总净利润':>12}")
    print("-" * 60)

    results = []
    for d in discounts:
        r = calculate_single(cost, d, volume)
        results.append(r)
        total_str = f"¥{r.total_net_profit:>10,.0f}" if r.total_net_profit is not None else "     -"
        flag = " ⚠️亏损" if r.net_profit < 0 else ""
        print(f"{d*10:.1f}折  ¥{r.promo_price:>7.2f}  ¥{r.net_profit:>7.2f}  {r.net_margin:>7.1f}%  {total_str}{flag}")

    print("=" * 60)

    # 推荐方案
    profitable = [r for r in results if r.net_profit > 0]
    if profitable:
        best = max(profitable, key=lambda r: r.net_profit)
        print(f"\n✅ 推荐方案：{best.discount*10:.1f}折（¥{best.promo_price}），单件净利润最高 ¥{best.net_profit}")
        if volume:
            print(f"   预期总净利润：¥{best.total_net_profit:,.0f}")
    else:
        print("\n❌ 所有方案均亏损，建议重新审视成本结构或提高售价")

    # 最低不亏折扣
    min_price = cost.purchase_cost + cost.shipping_cost + cost.marketing_cost + \
                cost.storage_cost + cost.return_rate * (cost.purchase_cost + cost.shipping_cost)
    # 考虑佣金：promo_price * (1 - commission_rate) >= min_price
    min_promo_price = min_price / (1 - cost.commission_rate)
    min_discount = min_promo_price / cost.original_price
    print(f"\n📌 不亏本最低折扣：{min_discount*10:.2f}折（¥{min_promo_price:.2f}）")
    print()


def cmd_breakeven(args):
    cost = ProductCost(
        purchase_cost=args.cost,
        original_price=args.price,
        commission_rate=args.commission,
        shipping_cost=args.shipping,
        return_rate=args.return_rate,
        marketing_cost=args.marketing,
        storage_cost=getattr(args, 'storage', 0),
    )

    # 计算盈亏平衡折扣（净利润=0时的折扣）
    # promo_price - total_cost = 0
    # promo_price * (1 - commission_rate) = purchase_cost + shipping + marketing + storage + return_rate*(purchase+shipping)
    fixed_per_unit = (cost.purchase_cost + cost.shipping_cost + cost.marketing_cost +
                      cost.storage_cost + cost.return_rate * (cost.purchase_cost + cost.shipping_cost))
    breakeven_price = fixed_per_unit / (1 - cost.commission_rate)
    breakeven_discount = breakeven_price / cost.original_price

    print(f"\n📊 盈亏平衡分析")
    print(f"  单件固定成本（不含佣金）: ¥{fixed_per_unit:.2f}")
    print(f"  盈亏平衡售价: ¥{breakeven_price:.2f}")
    print(f"  盈亏平衡折扣: {breakeven_discount*10:.2f}折 ({breakeven_discount*100:.1f}%)")

    if hasattr(args, 'fixed_cost') and args.fixed_cost > 0:
        # 需要覆盖固定成本的销量
        # 以原价为基准计算
        r_original = calculate_single(cost, 1.0)
        if r_original.net_profit > 0:
            be_vol = args.fixed_cost / r_original.net_profit
            print(f"\n  固定成本 ¥{args.fixed_cost:,.0f} 的盈亏平衡销量（原价）: {be_vol:.0f} 件")
    print()


def cmd_batch(args):
    discounts = [float(d) for d in args.discounts.split(',')]

    try:
        with open(args.input, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)

    print(f"\n📊 批量促销测算（{len(rows)} 个SKU）")
    print("=" * 80)

    for row in rows:
        sku = row.get('SKU', row.get('sku', '未知'))
        try:
            cost = ProductCost(
                purchase_cost=float(row.get('采购成本', row.get('cost', 0))),
                original_price=float(row.get('原售价', row.get('price', 0))),
                commission_rate=float(row.get('佣金率', row.get('commission', 0.05))),
                shipping_cost=float(row.get('物流成本', row.get('shipping', 8))),
                return_rate=float(row.get('退货率', row.get('return_rate', 0.05))),
                marketing_cost=float(row.get('营销成本', row.get('marketing', 0))),
            )
            volume = float(row.get('预期销量', row.get('volume', 0))) or None

            print(f"\nSKU: {sku}")
            for d in discounts:
                r = calculate_single(cost, d, volume)
                flag = " ⚠️亏损" if r.net_profit < 0 else ""
                total_str = f"  总净利润¥{r.total_net_profit:,.0f}" if r.total_net_profit else ""
                print(f"  {d*10:.1f}折 ¥{r.promo_price} → 净利润¥{r.net_profit} ({r.net_margin}%){total_str}{flag}")
        except (ValueError, KeyError) as e:
            print(f"  ⚠️ SKU {sku} 数据有误: {e}")

    print()


def main():
    parser = argparse.ArgumentParser(description='促销方案测算工具')
    subparsers = parser.add_subparsers(dest='command')

    # 公共参数
    def add_cost_args(p):
        p.add_argument('--cost', type=float, required=True, help='采购成本（元）')
        p.add_argument('--price', type=float, required=True, help='原售价（元）')
        p.add_argument('--commission', type=float, default=0.05, help='平台佣金率，默认0.05')
        p.add_argument('--shipping', type=float, default=8, help='物流成本（元/件），默认8')
        p.add_argument('--return-rate', type=float, default=0.05, dest='return_rate', help='退货率，默认0.05')
        p.add_argument('--marketing', type=float, default=0, help='营销成本（元/件），默认0')
        p.add_argument('--storage', type=float, default=0, help='仓储成本（元/件），默认0')

    # single
    p_single = subparsers.add_parser('single', help='单品单方案测算')
    add_cost_args(p_single)
    p_single.add_argument('--discount', type=float, required=True, help='折扣率（如0.8表示8折）')
    p_single.add_argument('--volume', type=float, help='预期销量（件）')
    p_single.add_argument('--fixed-cost', type=float, default=0, dest='fixed_cost', help='固定成本（元）')

    # compare
    p_compare = subparsers.add_parser('compare', help='多方案对比')
    add_cost_args(p_compare)
    p_compare.add_argument('--discounts', type=str, default='0.7,0.75,0.8,0.85,0.9',
                           help='折扣率列表，逗号分隔，默认0.7,0.75,0.8,0.85,0.9')
    p_compare.add_argument('--volume', type=float, help='预期销量（件）')

    # breakeven
    p_be = subparsers.add_parser('breakeven', help='盈亏平衡分析')
    add_cost_args(p_be)
    p_be.add_argument('--fixed-cost', type=float, default=0, dest='fixed_cost', help='固定成本（元）')

    # batch
    p_batch = subparsers.add_parser('batch', help='批量SKU测算')
    p_batch.add_argument('--input', type=str, required=True, help='CSV文件路径')
    p_batch.add_argument('--discounts', type=str, default='0.7,0.75,0.8,0.85,0.9',
                         help='折扣率列表，逗号分隔')

    args = parser.parse_args()

    if args.command == 'single':
        cmd_single(args)
    elif args.command == 'compare':
        cmd_compare(args)
    elif args.command == 'breakeven':
        cmd_be = args
        cmd_breakeven(cmd_be)
    elif args.command == 'batch':
        cmd_batch(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
