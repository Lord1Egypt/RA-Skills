#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具22 · 开发项目投前测算器（总货值 / 总投资 / 净利率 / IRR / 盈亏平衡售价 / 敏感性）

定位：拿地前的"这项目能不能做"快算，不是可研报告替代品。
      它算的是量级与结构，不是分月现金流；结论用于"要不要往下投钱做可研"。

用法:
  # 呈贡某地块：60 亩、容积率 2.0、楼面地价 2500、建安 3800、均价 11000
  python3 feasibility.py --land-area 40000 --far 2.0 --land-floor-price 2500 \\
      --build-cost 3800 --price 11000 --sell-years 3

  # 土地总价已知时直接给总价
  python3 feasibility.py --land-area 40000 --far 2.0 --land-price 200000000 \\
      --build-cost 3800 --price 11000

  # 只看盈亏平衡售价（愿意卖多少钱才不亏）
  python3 feasibility.py --land-area 40000 --far 2.0 --land-floor-price 2500 \\
      --build-cost 3800 --price 11000 --breakeven-only

口径（必须按项目当地实际调整）:
  · 容积率=地上计容建面/用地面积；可售比=可售建面/计容建面（含配套、架空、不可售部分）
  · 销售税费综合 ~ 增值税及附加 + 土地增值税 + 企业所得税，住宅项目常按销售额 8%~14% 综合
  · 管理营销费 常按销售额 4%~8%；财务费用 常按土地+建安+其他 的 3%~6%
  · IRR 按年度现金流近似：土地款首年全额支付，建安与其他按去化年限均摊，税费与管理营销随回款
  · 本工具不含：分期开发、融资结构、预售监管资金占用、土增税清算细则、精装与车位单独口径
警告：结果对"售价"和"建安单方"最敏感，先跑敏感性表再看结论。
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
    return f"{x:,.0f} 元"


def fmt_yuan(x):
    return f"{x:,.0f}"


def per(x, _percent, name, hi=100.0, lo=0.0) -> float:
    """把"人话里的百分数"（15=15%）换成小数，越界直接报错。"""
    if x < lo or x > hi:
        raise SystemExit(
            f"参数 {name} 需为百分数（{lo:g}~{hi:g}，如 15 表示 15%），收到 {x:g}"
        )
    return x / 100.0


def frac(x, name, lo, hi):
    """把"小数口径"的参数校验在范围内（0.95=95%）。"""
    if x < lo or x > hi:
        raise SystemExit(
            f"参数 {name} 需为小数（{lo:g}~{hi:g}，如 0.95 表示 95%），收到 {x:g}"
        )
    return x


def irr(cashflows, lo=-0.99, hi=3.0, tol=1e-7):
    """二分法求 IRR（现金流按年，第 0 年为负）。无解返回 None。"""
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
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def compute(args):
    """按输入算一遍，返回一个结果字典（供主流程与敏感性复用）。"""
    land_area = args.land_area
    if land_area <= 0:
        raise SystemExit("--land-area 必须大于 0（单位：平方米）")
    if args.far <= 0:
        raise SystemExit("--far 容积率必须大于 0")
    sell_ratio = frac(args.sellable_ratio, "--sellable-ratio", 0.3, 1.0)
    build_area = land_area * args.far
    sellable = build_area * sell_ratio

    if args.land_price is not None:
        land_total = args.land_price
    elif args.land_floor_price is not None:
        land_total = args.land_floor_price * build_area
    else:
        raise SystemExit("必须给 --land-price（土地总价，元）或 --land-floor-price（楼面地价，元/㎡）")

    build_total = args.build_cost * build_area
    other = build_total * per(args.other_pct, "--other-pct", 100.0)
    hard = land_total + build_total + other
    finance = hard * per(args.finance_pct, "--finance-pct", 100.0)
    revenue = sellable * args.price
    admin = revenue * per(args.admin_pct, "--admin-pct", 100.0)
    tax = revenue * per(args.tax_pct, "--tax-pct", 100.0)
    total_cost = hard + finance + admin + tax
    profit = revenue - total_cost
    margin = profit / revenue if revenue else 0.0

    # 盈亏平衡售价：让利润为 0 的均价（管理营销与税费随销售额走）
    flow_pct = per(args.admin_pct, "--admin-pct", 100.0) + per(args.tax_pct, "--tax-pct", 100.0)
    breakeven = hard + finance
    breakeven_price = breakeven / (sellable * (1 - flow_pct)) if sellable and flow_pct < 1 else float("nan")

    # IRR 两个口径，必须同时给，否则会被当成"收益率 30% 的好生意"：
    # ①全投资 IRR：总投资与销售回款都按年摊，不含任何融资杠杆（最保守、可对外引用）
    # ②自有资金 IRR：只把土地款放在第 0 年，其余成本靠销售回款滚动（乐观上限）
    years = max(1, int(args.sell_years))
    per_year_rev = revenue / years
    per_year_flow = (admin + tax) / years

    # 全投资口径：期初一次性投入硬成本+财务费用（土地+建安+其他+财务），
    # 每年回收（销售额 - 管理营销 - 销售税费）/年限；不再重复扣管理营销与税费。
    cash_all = [-(hard + finance)]
    net_inflow_per_year = (revenue - admin - tax) / years
    for _ in range(years):
        cash_all.append(net_inflow_per_year)
    irr_all = irr(cash_all)

    cash_equity = [-land_total]
    per_year_out = (build_total + other + finance) / years
    for _ in range(years):
        cash_equity.append(per_year_rev - per_year_out - per_year_flow)
    irr_equity = irr(cash_equity)

    return {
        "build_area": build_area, "sellable": sellable, "land_total": land_total,
        "build_total": build_total, "other": other, "finance": finance,
        "revenue": revenue, "admin": admin, "tax": tax, "total_cost": total_cost,
        "profit": profit, "margin": margin, "breakeven_price": breakeven_price,
        "irr": irr_all, "irr_equity": irr_equity, "years": years, "floor_price": land_total / build_area,
        "unit_cost": total_cost / sellable if sellable else 0.0,
        "land_to_revenue": land_total / revenue if revenue else 0.0,
    }


def main():
    ap = argparse.ArgumentParser(
        description="开发项目投前测算器：总货值 / 总投资 / 净利率 / IRR / 盈亏平衡售价 / 敏感性")
    ap.add_argument("--land-area", type=float, required=True, help="用地面积（㎡，1 亩=666.67㎡）")
    ap.add_argument("--far", type=float, required=True, help="容积率（地上计容建面 = 用地面积 × 容积率）")
    ap.add_argument("--sellable-ratio", type=float, default=0.95,
                    help="可售比（小数，0.95=95%%；扣配套/架空/不可售部分，默认 0.95）")
    ap.add_argument("--land-price", type=float, default=None, help="土地总价（元）")
    ap.add_argument("--land-floor-price", type=float, default=None, help="楼面地价（元/㎡ 计容建面）")
    ap.add_argument("--build-cost", type=float, required=True, help="建安单方（元/㎡ 计容建面，含粗装）")
    ap.add_argument("--other-pct", type=float, default=15.0,
                    help="前期+配套+间接费占建安的比例（百分数，默认 15）")
    ap.add_argument("--price", type=float, required=True, help="可售部分均价（元/㎡）")
    ap.add_argument("--sell-years", type=float, default=3.0, help="去化年限（默认 3 年）")
    ap.add_argument("--admin-pct", type=float, default=6.0, help="管理营销费占销售额（百分数，默认 6）")
    ap.add_argument("--tax-pct", type=float, default=10.0,
                    help="销售税费综合占销售额（百分数，默认 10；含增值税附加/土增税/所得税）")
    ap.add_argument("--finance-pct", type=float, default=4.0,
                    help="财务费用占（土地+建安+其他）（百分数，默认 4）")
    ap.add_argument("--breakeven-only", action="store_true", help="只输出盈亏平衡售价")
    ap.add_argument("--no-sensitivity", action="store_true", help="不打敏感性表")
    args = ap.parse_args()

    r = compute(args)

    if args.breakeven_only:
        print(f"盈亏平衡售价（利润=0）≈ {fmt_yuan(r['breakeven_price'])} 元/㎡")
        print(f"当前输入均价 {fmt_yuan(args.price)} 元/㎡，"
              f"安全垫 {(args.price / r['breakeven_price'] - 1) * 100:+.1f}%")
        return 0

    print("＝" * W)
    print(f"开发项目投前测算 ｜ 用地 {args.land_area:,.0f}㎡ × 容积率 {args.far:g}"
          f" = 计容 {r['build_area']:,.0f}㎡ ｜ 可售 {r['sellable']:,.0f}㎡")
    print("─" * W)
    print("【一、投入】")
    print(f"  · 土地款（楼面 {fmt_yuan(r['floor_price'])} 元/㎡）：{fmt_money(r['land_total'])}")
    print(f"  · 建安（{fmt_yuan(args.build_cost)} 元/㎡ × 计容）：{fmt_money(r['build_total'])}")
    print(f"  · 其他费用（建安 × {args.other_pct:g}%）：{fmt_money(r['other'])}")
    print(f"  · 财务费用（{args.finance_pct:g}%）：{fmt_money(r['finance'])}")
    print("【二、收入与随量费用】")
    print(f"  · 总货值（可售 {r['sellable']:,.0f}㎡ × {fmt_yuan(args.price)} 元/㎡）：{fmt_money(r['revenue'])}")
    print(f"  · 管理营销费（{args.admin_pct:g}% × 销售额）：{fmt_money(r['admin'])}")
    print(f"  · 销售税费（{args.tax_pct:g}% × 销售额）：{fmt_money(r['tax'])}")
    print("─" * W)
    print(f"  总投资 ≈ {fmt_money(r['total_cost'])} ｜ 单方可售投资 {fmt_yuan(r['unit_cost'])} 元/㎡")
    verdict = "可继续做可研" if r["margin"] >= 0.08 else ("偏薄，需压成本或抬价" if r["margin"] > 0 else "亏损，暂不建议推进")
    print(f"  ★ 净利润 ≈ {fmt_money(r['profit'])}（净利率 {r['margin'] * 100:.1f}%）→ {verdict}")
    print(f"  · 地货比 {r['land_to_revenue'] * 100:.1f}%" +
          ("（<35% 相对安全）" if r["land_to_revenue"] < 0.35 else "（≥35% 偏紧，靠售价支撑）"))
    if r["irr"] is not None:
        print(f"  · 全投资 IRR ≈ {r['irr'] * 100:.1f}%（硬成本期初一次投入、回款按年摊，无杠杆，可对外引用）")
    else:
        print("  · 全投资 IRR：现金流全负，无内部收益率（项目不成立）")
    if r["irr_equity"] is not None:
        print(f"  · 自有资金 IRR ≈ {r['irr_equity'] * 100:.1f}%（仅土地款期初支付，其余靠回款滚动 → 乐观上限）")
    print(f"  · 静态投资回报率 {r['profit'] / r['total_cost'] * 100:.1f}%"
          f"（净利/总投资，{r['years']} 年去化折算年化约 {r['profit'] / r['total_cost'] / r['years'] * 100:.1f}%）")
    print(f"  · 盈亏平衡售价 ≈ {fmt_yuan(r['breakeven_price'])} 元/㎡"
          f"（当前 {fmt_yuan(args.price)}，安全垫 {(args.price / r['breakeven_price'] - 1) * 100:+.1f}%）")
    print("=" * W)

    if not args.no_sensitivity:
        print("\n【三、敏感性：单因子 ±10% 对净利率 / IRR 的影响】")
        print(f"{'情景':<22}{'净利率':>10}{'IRR(全投资)':>14}{'净利润':>18}")
        base = dict(vars(args))

        def scenario(label, **over):
            ns = argparse.Namespace(**base)
            for k, v in over.items():
                setattr(ns, k, v)
            try:
                rr = compute(ns)
            except SystemExit:
                return
            irr_txt = f"{rr['irr'] * 100:.1f}%" if rr["irr"] is not None else "无"
            print(f"{label:<22}{rr['margin'] * 100:>9.1f}%{irr_txt:>12}{fmt_money(rr['profit']):>18}")

        scenario("基准", )
        scenario("售价 -10%", price=args.price * 0.9)
        scenario("售价 +10%", price=args.price * 1.1)
        scenario("建安 -10%", build_cost=args.build_cost * 0.9)
        scenario("建安 +10%", build_cost=args.build_cost * 1.1)
        if args.land_price is not None:
            scenario("地价 -10%", land_price=args.land_price * 0.9)
            scenario("地价 +10%", land_price=args.land_price * 1.1)
        elif args.land_floor_price is not None:
            scenario("地价 -10%", land_floor_price=args.land_floor_price * 0.9)
            scenario("地价 +10%", land_floor_price=args.land_floor_price * 1.1)
        print("\n读法：净利率跌破 8% 就要回头看成本与售价假设；售价 -10% 仍为正才是安全的。")
        print("注意：IRR 列是全投资口径（无杠杆）；自有资金 IRR 会高得多，但那是上限，不是承诺。")

    print("\n口径提醒：")
    print("  · 税费/管理营销/财务三率按项目实际调整（--tax-pct/--admin-pct/--finance-pct），别用默认值对外报价")
    print("  · 本工具是年度近似模型，不含分期开发、预售监管资金占用、土增税清算细则与精装车位拆分")
    print("  · 结果为量级判断，不是可研结论；对外使用请注明假设与测算日期")
    return 0


if __name__ == "__main__":
    sys.exit(main())
