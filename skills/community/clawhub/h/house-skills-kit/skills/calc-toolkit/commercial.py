#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具23 · 商业物业（商铺/写字楼/公寓）收益测算与收益法估值

定位：商业地产的定价逻辑是"租金决定价值"，不是"隔壁卖多少"。
      这个工具算三件事：租金能撑起多少估值、当下这个价买贵还是便宜、持有 N 年 IRR 多少。

用法:
  # 商铺：建面 60㎡、总价 180 万、月租 120 元/㎡、空置 8%、运营成本 15%、税费 12%
  python3 commercial.py --area 60 --price 1800000 --rent 120

  # 写字楼：建面 300㎡、单价 12000、月租 65 元/㎡、年递增 3%、持有 10 年退出
  python3 commercial.py --area 300 --unit-price 12000 --rent 65 --growth 3 --hold 10

  # 只看"这个价对应的资本化率是多少"（反向问：卖方要价隐含 cap）
  python3 commercial.py --area 60 --price 1800000 --rent 120 --implied-cap

口径（商业与住宅完全不同，别拿住宅经验套）:
  · 收益法估值 V = NOI / 资本化率；NOI = 有效租金 - 运营成本 - 出租税费
  · 出租税费：商业房产税从租计征 12%、增值税 9%（小规模/简易计税另算）、附加税、企业所得税或个税
    → 综合常见 12%~20%，本工具默认 12%，务必按当地税务核定调整
  · 运营成本（opex）：物业费自持部分、维修、保险、招商佣金摊销，常见占有效租金 10%~20%
  · 资本化率（cap rate）：一线核心商铺 3.5%~5%、社区底商 4.5%~6.5%、写字楼 5%~7%；
    县城/远郊商业常 7% 以上仍难成交 —— 这是"这类资产市场愿意给的价格"，不是你能选的
  · 空置率：商业空置远高于住宅，社区底商 5%~15%、新商圈 20%+ 都常见
警告：商铺最大的风险不是租金高低，是"租不出去"与"业态被替换"。参数里空置率请按保守值填。
"""
import argparse
import signal
import sys

# 被 `| head` / `| grep -q` 提前关闭管道时安静退出，别吐 BrokenPipeError 堆栈
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

W = 66


def fmt_money(x):
    if abs(x) >= 1e8:
        return f"{x / 1e8:,.2f} 亿元"
    if abs(x) >= 1e4:
        return f"{x / 1e4:,.1f} 万元"
    return f"{x:,.0f} 元"


def per(x, name, hi=100.0, lo=0.0) -> float:
    if x < lo or x > hi:
        raise SystemExit(
            f"参数 {name} 需为百分数（{lo:g}~{hi:g}，如 5 表示 5%），收到 {x:g}")
    return x / 100.0


def irr(cashflows, lo=-0.99, hi=3.0, tol=1e-7):
    def npv(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(cashflows))

    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo * f_hi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = npv(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid <= 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser(
        description="商业物业收益测算与收益法估值（NOI / 资本化率 / 净回报 / 持有期 IRR）")
    ap.add_argument("--area", type=float, required=True, help="建筑面积（㎡）")
    ap.add_argument("--price", type=float, default=None, help="总价（元）")
    ap.add_argument("--unit-price", type=float, default=None, help="单价（元/㎡），与 --price 二选一")
    ap.add_argument("--rent", type=float, required=True, help="月租金（元/㎡·月）")
    ap.add_argument("--vacancy", type=float, default=8.0, help="空置率%%（默认 8）")
    ap.add_argument("--opex-pct", type=float, default=15.0, help="运营成本占有效租金%%（默认 15）")
    ap.add_argument("--tax-pct", type=float, default=12.0, help="出租税费综合占有效租金%%（默认 12）")
    ap.add_argument("--cap", type=float, default=5.0, help="市场资本化率%%（默认 5.0，用于收益法估值）")
    ap.add_argument("--growth", type=float, default=2.0, help="租金年递增%%（默认 2）")
    ap.add_argument("--hold", type=int, default=10, help="持有年限（默认 10）")
    ap.add_argument("--exit-cap", type=float, default=None, help="退出时资本化率%%（默认同 --cap）")
    ap.add_argument("--implied-cap", action="store_true", help="只输出当前价隐含的资本化率")
    args = ap.parse_args()

    if args.area <= 0:
        raise SystemExit("--area 必须大于 0")
    if args.rent <= 0:
        raise SystemExit("--rent 必须大于 0（月租金，元/㎡·月）")
    if args.price is not None:
        price = args.price
    elif args.unit_price is not None:
        price = args.unit_price * args.area
    else:
        raise SystemExit("必须给 --price（总价）或 --unit-price（单价）")
    if price <= 0:
        raise SystemExit("总价必须大于 0")

    vacancy = per(args.vacancy, "--vacancy")
    opex = per(args.opex_pct, "--opex-pct")
    tax = per(args.tax_pct, "--tax-pct")
    cap = per(args.cap, "--cap")
    growth = per(args.growth, "--growth")
    exit_cap = per(args.exit_cap, "--exit-cap") if args.exit_cap is not None else cap
    if cap <= 0:
        raise SystemExit("--cap 必须大于 0（资本化率百分数，如 5 表示 5%）")
    if exit_cap <= 0:
        raise SystemExit("--exit-cap 必须大于 0")

    monthly_total = args.rent * args.area
    annual_potential = monthly_total * 12
    effective = annual_potential * (1 - vacancy)
    opex_amt = effective * opex
    tax_amt = effective * tax
    noi = effective - opex_amt - tax_amt

    gross_yield = annual_potential / price
    net_yield = noi / price
    value_by_cap = noi / cap
    gap = price / value_by_cap - 1
    payback = price / noi if noi > 0 else float("inf")
    implied = noi / price

    if args.implied_cap:
        print(f"当前价隐含资本化率 ≈ {implied * 100:.2f}%（市场常见参照 {args.cap:g}%）")
        print(f"若按市场 {args.cap:g}% 估值应值 {fmt_money(value_by_cap)}，现价 {fmt_money(price)}"
              f"（{gap * 100:+.1f}%）")
        return 0

    years = max(1, args.hold)
    cash = [-price]
    noi_t = noi
    for _ in range(years):
        cash.append(noi_t)
        noi_t *= (1 + growth)
    exit_value = noi_t / exit_cap            # 期末按"下一年 NOI / 退出 cap"退出
    cash[-1] += exit_value
    irr_value = irr(cash)

    print("＝" * W)
    print(f"商业物业收益测算 ｜ 建面 {args.area:,.0f}㎡ ｜ 总价 {fmt_money(price)}"
          f"（单价 {price / args.area:,.0f} 元/㎡）")
    print("─" * W)
    print("【一、租金与 NOI】")
    print(f"  · 月租 {args.rent:g} 元/㎡·月 → 月租合计 {fmt_money(monthly_total)}，年潜在租金 {fmt_money(annual_potential)}")
    print(f"  · 空置 {args.vacancy:g}% → 有效租金 {fmt_money(effective)}")
    print(f"  · 运营成本 {args.opex_pct:g}% → {fmt_money(opex_amt)} ｜ 出租税费 {args.tax_pct:g}% → {fmt_money(tax_amt)}")
    print(f"  ★ NOI（净营运收入）≈ {fmt_money(noi)} / 年（月均 {fmt_money(noi / 12)}）")
    print("【二、回报口径】")
    print(f"  · 毛租金回报率 {gross_yield * 100:.2f}%（不含空置与成本，别拿这个对外说）")
    print(f"  · 净回报率（NOI/总价）{net_yield * 100:.2f}%")
    print(f"  · 租售比 1:{price / monthly_total:,.0f}（总价 ÷ 月租）")
    print(f"  · 静态回收年限 {payback:.1f} 年（NOI 全部用于回本，不含增值）")
    print("【三、收益法估值】")
    print(f"  · 按资本化率 {args.cap:g}% → 合理估值 {fmt_money(value_by_cap)}"
          f"（现价 {gap * 100:+.1f}%）")
    if gap > 0.15:
        print("    → 现价明显高于收益法估值：要么租金假设过于乐观，要么你在为增值预期付钱")
    elif gap < -0.15:
        print("    → 现价低于收益法估值：先查租金是否可持续、业态是否会被替换，再谈便宜")
    else:
        print("    → 与收益法基本匹配（±15% 内），定价主要看租约质量与位置")
    if irr_value is not None:
        print(f"  · 持有 {years} 年 IRR ≈ {irr_value * 100:.1f}%"
              f"（租金年递增 {args.growth:g}%、期末按 {exit_cap * 100:g}% cap 退出）")
    else:
        print(f"  · 持有 {years} 年 IRR：现金流无解（租金不足以覆盖持有成本，退出价也救不回来）")
    print("=" * W)
    print("\n口径提醒：")
    print("  · 出租税费按当地税务核定填（商业房产税从租 12% + 增值税及附加 + 所得税），默认 12% 可能偏低")
    print("  · 免租期、装修补贴、招商佣金摊销未单列，谈判时把它们折算进有效租金再算一遍")
    print("  · 商铺请额外确认：是否独立水电、是否可餐饮（排烟/燃气）、租约剩余年限与递增条款")
    return 0


if __name__ == "__main__":
    sys.exit(main())
