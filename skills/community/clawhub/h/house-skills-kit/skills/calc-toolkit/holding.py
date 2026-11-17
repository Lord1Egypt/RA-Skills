#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具21 · 持有成本测算器（自住全成本 / 出租净现金流 / 5年累计）

用法:
  # 自住：昆明120㎡物业费1.8元，房价100万（算资金占用）
  python3 holding.py --area 120 --property 1.8 --price 1000000

  # 北方：北京95㎡集中供暖
  python3 holding.py --area 95 --property 2.8 --price 4000000 --city 北京

  # 出租：月租2600，空置1个月，中介费半个月
  python3 holding.py --area 120 --property 1.8 --price 1000000 --rent 2600 --vacancy 1 --agent-months 0.5

口径（2026-08-31查证）:
  · 取暖费：北方20-30元/㎡·采暖季（北京大网24元；邢台20/廊坊22/吉林27/四平28.3）；南方=0
  · 出租税负：个人出租住房综合征收率——京沪深2.5%（房产税2%+个税0.5%，月租≤10万）；
    广州4%（2000-3万）；成都备案网签0%；"六税两费"减半优惠至2027-12-31
  · 增值税：月租金≤10万免征（分摊口径）；>10万减按1.5%
  · 资金占用=隐性成本：房价×无风险利率（默认存款1.55%，可--set）——自住不交钱但放弃了利息
"""
import argparse
import sys

W = 58


def fmt_money(x):
    return f"{x:,.0f}"


def get_rules(city=None):
    try:
        from ruleengine import get_rules as _gr
        rules, srcmap = _gr("holding", city=city)
        return rules, srcmap
    except Exception:
        return {}, {}


def main():
    ap = argparse.ArgumentParser(description="持有成本测算器（演示档）")
    ap.add_argument("--area", type=float, help="建筑面积（㎡）")
    ap.add_argument("--property", type=float, help="物业费（元/㎡·月）")
    ap.add_argument("--price", type=float, default=0, help="房价（元，算资金占用成本，可省略）")
    ap.add_argument("--rent", type=float, default=0, help="月租金（元，>0时输出出租口径）")
    ap.add_argument("--vacancy", type=float, default=1, help="年空置（月，默认1）")
    ap.add_argument("--agent-months", type=float, default=0.5, help="出租中介费（按月租金倍数，默认0.5=半月）")
    ap.add_argument("--tax-rate", type=float, default=None, help="出租税综合征收率%%（默认取规则库2.5）")
    ap.add_argument("--city", default=None, help="城市（读城市档取暖费等）")
    ap.add_argument("--set", action="append", default=[], help="覆盖参数 k=v（可多次）")
    args = ap.parse_args()

    if not args.area or not args.property:
        ap.print_help()
        sys.exit(1)

    rules, srcmap = get_rules(city=args.city)
    overrides = {}
    for kv in args.set:
        if "=" not in kv:
            print(f"--set 格式应为 k=v：{kv}")
            sys.exit(1)
        k, v = kv.split("=", 1)
        try:
            overrides[k] = int(v) if ("." not in v and "-" not in v) else float(v)
        except ValueError:
            overrides[k] = v
    rules.update(overrides)

    heating_fee = float(rules.get("heating_fee", 0))        # 元/㎡·采暖季；南方0
    risk_free = float(rules.get("risk_free", 1.55)) / 100   # 资金占用参考利率
    tax_rate = (args.tax_rate / 100) if args.tax_rate is not None \
        else float(rules.get("rent_tax_rate", 2.5)) / 100

    area = args.area
    # ── 现金成本（自住口径） ──
    prop_y = area * args.property * 12
    heat_y = area * heating_fee
    cash_y = prop_y + heat_y
    capital_y = args.price * risk_free
    total_y = cash_y + capital_y

    src_note = "全国默认档" if not args.city else f"{args.city}档"
    print("=" * W)
    print("持有成本测算（年口径 · 演示档，以当地实际为准）")
    print("=" * W)
    print(f"规则来源: {src_note} ｜ 面积 {area:g}㎡ ｜ 物业 {args.property:g} 元/㎡·月"
          f" ｜ 取暖 {heating_fee:g} 元/㎡·季")
    print("-" * W)
    print("【自住口径】")
    print(f"  物业费:      {fmt_money(prop_y):>10} 元/年（{fmt_money(prop_y/12)}/月）")
    if heating_fee > 0:
        print(f"  取暖费:      {fmt_money(heat_y):>10} 元/年（北方采暖季）")
    else:
        print(f"  取暖费:      {fmt_money(0):>10} 元/年（南方无集中供暖）")
    print(f"  现金成本小计: {fmt_money(cash_y):>10} 元/年（{fmt_money(cash_y/12)}/月）")
    if args.price > 0:
        print(f"  资金占用*:   {fmt_money(capital_y):>10} 元/年（房价{fmt_money(args.price)}"
              f"×{risk_free*100:g}%，隐性成本）")
        print(f"  ★ 全成本:    {fmt_money(total_y):>10} 元/年 ≈ {fmt_money(total_y/12)} 元/月"
              f"（每㎡{total_y/area:.0f}元/年）")
        print("  * 自住不交钱，但你放弃了这笔钱存银行的利息")
    print(f"  5年累计(现金): {fmt_money(cash_y*5)} 元")

    # ── 出租口径 ──
    if args.rent > 0:
        gross_y = args.rent * (12 - args.vacancy)
        tax_y = gross_y * tax_rate
        agent_fee = args.rent * args.agent_months
        net_y = gross_y - tax_y - agent_fee
        print("-" * W)
        print("【出租口径】")
        print(f"  租金收入:    {fmt_money(gross_y):>10} 元/年（{args.rent:g}/月×{12-args.vacancy:g}个月实收）")
        print(f"  出租税({tax_rate*100:g}%): {fmt_money(tax_y):>8} 元/年"
              f"（综合征收率，含房产税2%+个税0.5%）")
        if agent_fee > 0:
            print(f"  中介费:      {fmt_money(agent_fee):>10} 元（半月租口径，年度摊一次）")
        print(f"  ★ 净现金流:  {fmt_money(net_y):>10} 元/年 ≈ {fmt_money(net_y/12)} 元/月")
        if args.price > 0:
            print(f"  净回报率:    {net_y/args.price*100:.2f}%（rent.py五档坐标可对照）")
        print("  提示: 综合征收率各地不同——京沪深2.5%/广州4%/成都备案0%；月租≤10万免增值税")

    print("-" * W)
    print("参数来源（规则版本可追溯）:")
    for k in ("heating_fee", "risk_free", "rent_tax_rate"):
        if k in rules:
            src = srcmap.get(k, "全国默认档") if isinstance(srcmap, dict) else "全国默认档"
            print(f"  · {k} = {rules[k]}  来源[{src}]")
    print("  · 出租税负时效: '六税两费'减半优惠至2027-12-31，届时以新政策为准")
    print("免责声明: 演示档；物业费以合同、取暖费以当地供热文件、税费以税务口径为准")


if __name__ == "__main__":
    main()
