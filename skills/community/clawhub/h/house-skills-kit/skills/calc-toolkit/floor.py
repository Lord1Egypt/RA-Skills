#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具15 · 楼层差价 + 折扣叠加计算器（折上折顺序引擎）
清单序号：⑦-15｜规则来源：tools/rules/cities.yaml（三层引擎）
核心价值（售楼处实战）：帮客户算清"楼层加价×付款折扣×营销折上折"的真实成交价，
并揭穿"折扣注水"套路（先涨价后打折）。

用法示例：
  # 基础：备案均价25000，选中15/30层，楼层系数+300元/㎡，总价打98折再99折
  python3 floor.py --price 25000 --area 100 --floor 15 --top 30 \
      --floor-adj 300 --d 98 --d 99
  # 对比：销售说"一次性付款再减2个点"
  python3 floor.py --price 25000 --area 100 --floor 15 --top 30 --floor-adj 300 --d 98 --pay one_time
  # 揭套路：基准价改高后同样折扣，看清"先涨后折"
  python3 floor.py --price 25000 --area 100 --floor 15 --top 30 --floor-adj 300 --d 98 --d 99 --baseline 26000
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance, COMPLIANCE  # noqa: E402

W = lambda x: f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description="楼层差价+折扣叠加计算器（⑦-15）")
    ap.add_argument("--price", type=float, required=True, help="备案/基准单价（元/㎡）")
    ap.add_argument("--baseline", type=float, help="名义基准价（揭套路对比用，选填）")
    ap.add_argument("--area", type=float, required=True, help="建筑面积㎡")
    ap.add_argument("--floor", type=int, required=True, help="所在层")
    ap.add_argument("--top", type=int, required=True, help="总层数")
    ap.add_argument("--floor-adj", type=float, default=0, help="楼层差价（元/㎡，正加负减，可自定义口径）")
    ap.add_argument("--d", type=float, action="append", default=[],
                    help="折扣（98 = 98折，可多次=折上折，按顺序相乘）")
    ap.add_argument("--pay", choices=["one_time", "mortgage"], help="付款方式折扣（读城市规则）")
    ap.add_argument("--city"); ap.add_argument("--district"); ap.add_argument("--template")
    args = ap.parse_args()

    rules, prov = get_rules("discount", args.city, args.district, args.template)

    unit = args.price + args.floor_adj
    gross = unit * args.area
    tag = []
    if args.floor_adj:
        tag.append(f"楼层{args.floor_adj:+g}元/㎡")

    # 折扣序列：营销折上折（用户给定，按序相乘） + 付款方式（城市规则）
    chain = []
    factor = 1.0
    for d in args.d:
        f = d / 100
        chain.append((f"{d:g}折", f))
        factor *= f
    if args.pay:
        pd = rules.get("payment_discounts", {})
        off = pd.get(args.pay)
        if off:
            f = 1 - off  # YAML 存"优惠点数"（0.02=让2个点），换算为支付因子
            chain.append((f"付款{'一次性' if args.pay=='one_time' else '按揭'}让{(off)*100:g}%", f))
            factor *= f

    net = gross * factor
    saved = gross - net

    print(f"＝ 成交价试算（楼层×折上折） ｜ {args.area:g}㎡ ｜ {args.floor}/{args.top}层"
          f"{' ｜ 城市:'+args.city if args.city else ''}{'/'+args.district if args.district else ''}")
    print("─" * 56)
    print(f"  基准单价 {W(args.price)} 元/㎡ " + ("  ".join(tag) if tag else ""))
    print(f"  → 适用单价 {W(unit)} 元/㎡ × {args.area:g}㎡ = 总价 {W(gross)} 元")
    if chain:
        steps = " × ".join(f"{name}({f:.4f})" for name, f in chain)
        print(f"  折扣链：{steps}")
        print(f"  → 综合折扣 {factor:.4f}（相当于 {(1-factor)*100:.1f} 个点优惠）")
        print(f"  → 成交总价 {W(net)} 元（优惠 {W(saved)} 元）")
    else:
        print(f"  → 成交总价 {W(net)} 元")
    eff = net / args.area
    print(f"  → 实际成交单价 {W(eff)} 元/㎡")

    # ── 折扣真伪校验（实战防坑）──
    if args.baseline:
        b_unit = args.baseline + args.floor_adj
        b_gross = b_unit * args.area
        b_net = b_gross * factor
        print()
        print(f"  【套路校验】若名义基准 {W(args.baseline)} 元/㎡：折后 {W(b_net)} 元")
        if b_net > net + 1:
            print(f"  ⚠ 名义基准折后仍比真实成交高 {W(b_net-net)} 元——'先涨价后打折'，折扣有水")
        elif b_net < net - 1:
            print(f"  ✓ 名义基准折后更低 {W(net-b_net)} 元——可拿此对比要求同等价格")
        else:
            print("  · 两种基准折后一致，折扣是实的")

    # ── 一房一价表（可选：上下楼层扫描）──
    print()
    print("  邻层速查（同一折扣链，锚定所选层差价口径）：")
    for fl in sorted({max(1, args.floor-2), max(1, args.floor-1), args.floor,
                      min(args.top, args.floor+1), min(args.top, args.floor+2)}):
        u = unit + args.floor_adj * (fl - args.floor)  # unit 已含所选层楼层差
        g = u * args.area
        mark = " ←所选" if fl == args.floor else ""
        print(f"    {fl}层：单价 {W(u)} → 折后 {W(g*factor)} 元{mark}")

    print()
    print(fmt_provenance(prov, ["payment_discounts"]))
    print()
    print("口径提示：楼层差价按'每层递增X元/㎡'线性简化；一房一价精确口径以销控表为准。")
    print("折扣顺序：价格型修正（楼层/付款）先行，营销型折扣依次相乘（折上折≠先总和多再打折）。")
    print(COMPLIANCE)


if __name__ == "__main__":
    main()
