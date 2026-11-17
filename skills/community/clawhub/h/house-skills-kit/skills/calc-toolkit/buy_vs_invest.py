#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具22 · 买房 vs 理财对比器（期末净资产对决 + 打平涨幅反推）

用法:
  # 100万房首付3成贷30年，持有10年 vs 理财
  python3 buy_vs_invest.py --price 1000000 --down-pct 30 --years 30 --horizon 10

  # 自住省租金口径：不买房就得租房（月租2000）
  python3 buy_vs_invest.py --price 1000000 --down-pct 30 --years 30 --horizon 10 --rent 2000

  # 自定义理财收益与三情景（负涨幅用 = 连接，如 --growth=-3,0,5）
  python3 buy_vs_invest.py --price 2000000 --down-pct 30 --years 30 --horizon 5 --rate-invest 2.5 --growth=-3,0,5

核心逻辑（现金流两端对齐，纯比资产端）:
  同一笔期初现金（首付+交易成本）+ 每月同等现金流：
  A 买房   → 期末 = 房价终值 − 剩余贷款 + 租金贡献终值（自住省租/出租净收）
  B 理财   → 期末 = 期初现金终值 + 月供滚存终值（按理财年化复利）
  打平涨幅 g*: 房价年均涨多少，A 才不输 B（数值二分解）

口径（2026-08-31查证）:
  · 银行理财平均收益率 1.98%（银行业理财登记托管中心《2025年报》，较2024年2.65%降67BP，历史新低）
  · 一年期定存 0.95%（2025口径）；五大行5年定存 1.55%
  · 2026年以来理财收益继续下探：2026-03 月均年化 1.01%（普益标准），现金管理类 1.25%
  · 交易成本默认 2%（买契税+卖增值税/个税/中介综合简化，--cost-pct 可调）
"""
import argparse
import sys

W = 58


def fmt_money(x):
    return f"{x:,.0f}"


def get_rules(city=None):
    try:
        from ruleengine import get_rules as _gr
        rules, srcmap = _gr("invest", city=city)
        return rules, srcmap
    except Exception:
        return {}, {}


def annuity_payment(principal, annual_rate, years):
    i = annual_rate / 12
    n = years * 12
    if i <= 0:
        return principal / n
    f = (1 + i) ** n
    return principal * i * f / (f - 1)


def loan_balance(principal, annual_rate, years, months_paid):
    """等额本息 k 期后剩余本金"""
    i = annual_rate / 12
    n = years * 12
    if i <= 0:
        return principal * (1 - months_paid / n)
    f = (1 + i) ** n
    return principal * (f - (1 + i) ** months_paid) / (f - 1)


def fv_annuity(pmt, monthly_rate, months):
    if monthly_rate <= 0:
        return pmt * months
    return pmt * (((1 + monthly_rate) ** months - 1) / monthly_rate)


def main():
    ap = argparse.ArgumentParser(description="买房 vs 理财对比器（演示档）")
    ap.add_argument("--price", type=float, help="房价（元）")
    ap.add_argument("--down-pct", type=float, default=30, help="首付比例%%（默认30）")
    ap.add_argument("--years", type=int, default=30, help="贷款年限（默认30）")
    ap.add_argument("--rate", type=float, default=None, help="房贷利率%%（默认取规则库商贷3.10）")
    ap.add_argument("--horizon", type=int, default=10, help="持有年限N（默认10）")
    ap.add_argument("--rate-invest", type=float, default=None, help="理财年化%%（默认取规则库1.98）")
    ap.add_argument("--growth", default="-2,0,3", help="三情景房价年涨幅%%（默认-2,0,3；负数须用=连接：--growth=-3,0,5）")
    ap.add_argument("--rent", type=float, default=0, help="月租金（元）：自住省租/出租净收，默认0不计")
    ap.add_argument("--cost-pct", type=float, default=None, help="交易成本%%（默认取规则库2.0）")
    ap.add_argument("--city", default=None, help="城市（读规则库）")
    ap.add_argument("--set", action="append", default=[], help="覆盖参数 k=v")
    args = ap.parse_args()

    if not args.price:
        ap.print_help()
        sys.exit(1)

    rules, _ = get_rules(city=args.city)
    for kv in args.set:
        if "=" in kv:
            k, v = kv.split("=", 1)
            try:
                rules[k] = float(v)
            except ValueError:
                rules[k] = v

    loan_rate = (args.rate if args.rate is not None else float(rules.get("commercial_rate", 3.10))) / 100
    inv_rate = (args.rate_invest if args.rate_invest is not None else float(rules.get("wealth_avg", 1.98))) / 100
    cost_pct = (args.cost_pct if args.cost_pct is not None else float(rules.get("cost_pct", 2.0))) / 100

    down = args.price * args.down_pct / 100
    loan = args.price - down
    cost0 = args.price * cost_pct
    equity0 = down + cost0                      # 期初现金投入（两端对称）
    pay = annuity_payment(loan, loan_rate, args.years)
    n_h = args.horizon * 12
    balance_h = loan_balance(loan, loan_rate, args.years, min(n_h, args.years * 12))
    rent_fv = fv_annuity(args.rent, inv_rate / 12, n_h) if args.rent > 0 else 0.0

    b_end = equity0 * (1 + inv_rate / 12) ** n_h + fv_annuity(pay, inv_rate / 12, n_h)

    def a_end(g):
        return args.price * (1 + g) ** args.horizon - balance_h + rent_fv

    print("=" * W)
    print("买房 vs 理财 · 期末净资产对决（演示档）")
    print("=" * W)
    print(f"房价 {fmt_money(args.price)} ｜ 首付{args.down_pct:g}%={fmt_money(down)}"
          f" ｜ 贷款 {fmt_money(loan)} @ {loan_rate*100:.2f}% {args.years}年")
    print(f"月供 {fmt_money(pay)} 元 ｜ 交易成本 {cost_pct*100:g}%={fmt_money(cost0)}"
          f" ｜ 持有 {args.horizon} 年")
    print(f"理财基准 {inv_rate*100:.2f}%（银行理财2025均值1.98%口径，可--rate-invest改）"
          + (f" ｜ 月租贡献 {args.rent:g} 元" if args.rent > 0 else " ｜ 未计租金（--rent可加）"))
    print("-" * W)
    print(f"{'房价年涨幅':>10} | {'买房净资产':>12} | {'理财终值':>12} | {'差额':>10}")
    for gs in args.growth.split(","):
        g = float(gs) / 100
        ae = a_end(g)
        diff = ae - b_end
        tag = "买房赢" if diff > 0 else ("持平" if abs(diff) < 1 else "理财赢")
        print(f"{gs:>9}% | {fmt_money(ae):>12} | {fmt_money(b_end):>12} | {fmt_money(diff):>10}  {tag}")

    # ── 打平涨幅（二分求解） ──
    lo, hi = -0.15, 0.30
    f_lo = a_end(lo) - b_end
    f_hi = a_end(hi) - b_end
    print("-" * W)
    if f_lo > 0:
        print(f"★ 打平涨幅: 房价年跌 {abs(lo)*100:.1f}% 仍不输理财（安全垫厚）")
    elif f_hi < 0:
        print(f"★ 打平涨幅: 超+30%仍跑不赢（租金/杠杆口径下理财优势过大，慎入）")
    else:
        for _ in range(80):
            mid = (lo + hi) / 2
            if a_end(mid) - b_end > 0:
                hi = mid
            else:
                lo = mid
        g_star = (lo + hi) / 2
        print(f"★ 打平涨幅: 房价年均涨 ≥ {g_star*100:.2f}% 才不输理财（{inv_rate*100:.2f}%基准）")
        print("  对照: 2024重点50城租金回报率2.06%；理财收益长期下行，打平线也在降")
    if args.rent == 0:
        print("  提示: 未计租金会高估打平线——自住加 --rent 省租口径再算一遍")
    print("-" * W)
    print("规则来源: " + "; ".join(f"{k}={rules[k]}" for k in ("wealth_avg", "commercial_rate", "cost_pct") if k in rules))
    print("免责声明: 演示档简化模型（未计通胀/维护/流动性差异）；理财非保本，历史收益不代表未来")


if __name__ == "__main__":
    main()
