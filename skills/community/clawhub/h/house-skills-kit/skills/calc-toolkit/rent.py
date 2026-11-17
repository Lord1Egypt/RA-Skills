#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具19 · 租金回报率计算器（租售比 / 毛净回报率 / 回收年限 / 以租养贷判定）

用法:
  # 基础：100万的房月租2000
  python3 rent.py --price 1000000 --rent 2000

  # 净口径：扣空置/税费/维修（--net）
  python3 rent.py --price 1000000 --rent 2000 --net --city 昆明

  # 反推：目标回报率4% → 该收多少月租 / 只值多少钱
  python3 rent.py --price 1000000 --rent 2000 --target-yield 4

口径（2026-08 查证）:
  · 租售比国际合理区间 1:200~1:300（年化 6%~4%，MBA智库口径）
  · 2024 全国重点50城：租售比 1:582，租金回报率 2.06%（2019年以来新高，
    跑赢五大行存款"1字头"；一线 1.82% / 二线 2.04% / 三四线 2.55%，
    乌鲁木齐 3.77% 最高、厦门 1.36% 最低）——麟评居住大数据研究院
  · 价值线：≥5% 值得买入收租；3% 是靠出租回本的分界（国际通行）
  · 以租养贷：租金回报率 ≥ 房贷利率时财务上成立（2026 商贷约3.1%/公积金2.5%）
  · 净口径扣减（演示档，--set 可调）：空置+换租损耗 5%、个人出租住房综合税 5%
   （各地优惠口径 2.5%~5%，以主管税务机关为准）、年维修保养占房价 0.5%
输出: 租售比 → 毛回报率 → 净回报率 → 回收年限 → 五档坐标（区间/全国/价值线/存款/房贷）
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance  # noqa: E402


def fmt_money(x: float) -> str:
    return f"{x:,.0f}"


def _num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def main() -> None:
    ap = argparse.ArgumentParser(description="租金回报率（租售比/毛净回报率/回收年限/以租养贷）")
    ap.add_argument("--price", type=float, required=True, help="房屋总价（元）")
    ap.add_argument("--rent", type=float, required=True, help="月租金（元）")
    ap.add_argument("--net", action="store_true", help="同时计算净回报率（扣空置/税/维修）")
    ap.add_argument("--target-yield", type=float, default=None,
                    help="目标年化回报率%%（如 4）→ 反推该收月租/该买入价")
    ap.add_argument("--vacancy", type=float, default=None, help="空置+换租损耗%%（默认5）")
    ap.add_argument("--tax-rate", type=float, default=None, help="租金综合税负%%（默认5）")
    ap.add_argument("--maint", type=float, default=None, help="年维修保养占房价%%（默认0.5）")
    ap.add_argument("--city", default=None, help="城市（取规则库覆盖档）")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="临时覆盖规则参数 k=v，可多次")
    args = ap.parse_args()

    overrides = {}
    for kv in args.overrides:
        if "=" not in kv:
            ap.error(f"--set 需 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, srcmap = get_rules("rent", city=args.city, district=None,
                              user_template=None, overrides=overrides)
    W = 52
    print("=" * W)
    print("租金回报率计算器")
    print("=" * W)

    price, rent = args.price, args.rent
    annual = rent * 12
    gross = annual / price

    # ===== 反推模式 =====
    if args.target_yield:
        ty = args.target_yield / 100
        rent_need = price * ty / 12
        price_fair = annual / ty
        gap_rent = rent_need / rent - 1 if rent > 0 else float("inf")
        print(f"目标年化回报率: {args.target_yield:g}%")
        print("-" * W)
        if gap_rent > 0:
            print(f"  该房现价下应月收: {fmt_money(rent_need)} 元"
                  f"（比现租 {fmt_money(rent)} 高 {gap_rent*100:+.0f}%）")
            print(f"  或 现租金下合理买入价: {fmt_money(price_fair)} 元"
                  f"（比现价低 {(1 - price_fair/price)*100:.0f}%）")
        else:
            print(f"  已达标：现租 {fmt_money(rent)} 元 ≥ 应收 {fmt_money(rent_need)} 元")
        print("-" * W)

    ratio = price / rent if rent > 0 else float("inf")
    print(f"总价: {fmt_money(price)} 元 ｜ 月租: {fmt_money(rent)} 元"
          f"（年租 {fmt_money(annual)} 元）")
    print(f"租售比: 1 : {ratio:,.0f}（国际合理 1:200~1:300）")
    print(f"毛回报率: {gross*100:.2f}%/年 ｜ 静态回收年限 ≈ {1/gross:.1f} 年" if gross > 0 else "")

    # ===== 净口径 =====
    if args.net:
        vacancy = (args.vacancy if args.vacancy is not None
                   else float(rules.get("vacancy", 0.05)))
        tax_rate = (args.tax_rate if args.tax_rate is not None
                    else float(rules.get("tax_rate", 0.05)))
        maint = args.maint if args.maint is not None else float(rules.get("maint", 0.005))
        eff = annual * (1 - vacancy) * (1 - tax_rate) - price * maint
        net = eff / price
        print("-" * W)
        print(f"净口径扣减: 空置{vacancy*100:g}% × 税负{tax_rate*100:g}%"
              f" − 维修{maint*100:g}%/年")
        print(f"净年收益: {fmt_money(eff)} 元 → 净回报率 {net*100:.2f}%"
              f" ｜ 回收 ≈ {1/net:.1f} 年" if net > 0 else f"净收益为负: {fmt_money(eff)} 元")
        gross, show = net, net  # 坐标判定用净口径

    # ===== 五档坐标 =====
    print("-" * W)
    deposit = float(rules.get("deposit_bench", 0.0155))
    national = float(rules.get("national50", 0.0206))
    loan = float(rules.get("loan_commercial", 0.031))
    print("坐标（年化）:")
    marks = [
        ("买入价值线", 0.05, gross >= 0.05),
        ("出租回本线", 0.03, gross >= 0.03),
        ("50城均值(2024)", national, gross >= national),
        ("五大行存款(5年)", deposit, gross >= deposit),
        ("商贷利率", loan, gross >= loan),
    ]
    for label, bench, ok in marks:
        tag = "✓ 达标" if ok else "✗"
        if label == "商贷利率" and ok:
            tag = "✓ 可以租养贷"
        print(f"  {label:<10} {bench*100:>5.2f}%  {tag}")
    if ratio <= 300 and gross >= 0.04:
        verdict = "处于/优于国际合理区间，买入收租价值显著"
    elif gross >= 0.03:
        verdict = "超出3%出租回本线，长持收租可行（对比银行理财有优势）"
    elif gross >= deposit:
        verdict = "跑赢存款但仍低于3%回本线——自住为主、收租为辅的定位"
    else:
        verdict = "低于存款利率——靠租金回本遥遥无期，买的应是居住/增值预期而非租金"
    print(f"判定: {verdict}")
    print("-" * W)
    keys = [k for k in ("deposit_bench", "national50", "vacancy", "tax_rate",
                        "maint", "loan_commercial") if k in rules]
    print("口径出处:")
    print(fmt_provenance(srcmap, keys) if keys else "  · 国际区间/2024年50城报告（麟评居住大数据研究院）")
    print("提醒: 静态口径未计房价涨跌与利率变动；税费以主管税务机关核定为准。")


if __name__ == "__main__":
    main()
