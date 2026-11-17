#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具18 · 得房率与单价换算器（建面↔套内↔公摊 / 双盘比价照妖镜）

用法:
  # 面积链：建面120㎡/得房率78% → 套内/公摊分解 + 使用面积估算
  python3 efficiency.py --mode area --gross 120 --rate 78

  # 单价换算：建面单价15000 → 套内单价
  python3 efficiency.py --mode price --gross 120 --rate 78 --price-gross 15000

  # 双盘比价（照妖镜）：建面便宜的盘，套内可能更贵！
  python3 efficiency.py --mode compare \
      --label-a A盘 --gross-a 100 --rate-a 75 --price-a 14500 \
      --label-b B盘 --gross-b 100 --rate-b 82 --price-b 15200

  # 反推：已知套内110㎡/得房率81% → 该买多大建面
  python3 efficiency.py --mode area --inner 110 --rate 81

口径（2026-08）:
  · 得房率 = 套内建面 / 建筑面积（行业参考区间，非官方标准）：
    洋房/低密 82-90% ｜ 小高层板楼 80-85% ｜ 高层塔楼 75-80% ｜ 超高层 72-78% ｜
    商住公寓 55-70%（公摊大）
  · 套内建面 = 套内使用面积 + 套内墙体 + 阳台一半（使用面积≈套内建面×85-90%）
  · 公摊 = 电梯井/楼梯间/公共门厅/设备房/外墙一半等（2023-08住建部拟推"套内计价"，
    目前买卖合同仍以建面计价为主流）
输出: 面积链分解 → 单价双向换算 → 双盘套内口径比价（防"建面便宜"幻觉）
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
    ap = argparse.ArgumentParser(description="得房率与单价换算（建面↔套内↔公摊/双盘比价）")
    ap.add_argument("--mode", default="area", choices=["area", "price", "compare"],
                    help="area=面积链 / price=单价换算 / compare=双盘比价（默认 area）")
    ap.add_argument("--gross", type=float, default=None, help="建筑面积（㎡）")
    ap.add_argument("--inner", type=float, default=None, help="套内建面（㎡，与--gross二选一，另一个反推）")
    ap.add_argument("--rate", type=float, default=None, help="得房率%（如 78；缺省按 --type 档位）")
    ap.add_argument("--type", default=None,
                    help="物业类型: garden洋房/plate板楼/tower塔楼/super超高层/apartment公寓")
    ap.add_argument("--use-coef", type=float, default=None, help="使用面积系数（套内建面×该系数，默认88%%）")
    ap.add_argument("--price-gross", type=float, default=None, help="建面单价（元/㎡）")
    ap.add_argument("--price-inner", type=float, default=None, help="套内单价（元/㎡）")
    ap.add_argument("--label-a", default="A盘", help="比价A盘名称")
    ap.add_argument("--gross-a", type=float, help="A盘建面单价对照用：--rate-a 得房率 --price-a 建面单价")
    ap.add_argument("--rate-a", type=float, help="A盘得房率%%")
    ap.add_argument("--price-a", type=float, help="A盘建面单价（元/㎡）")
    ap.add_argument("--label-b", default="B盘", help="比价B盘名称")
    ap.add_argument("--rate-b", type=float, help="B盘得房率%%")
    ap.add_argument("--price-b", type=float, help="B盘建面单价（元/㎡）")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="临时覆盖规则参数 k=v，可多次")
    args = ap.parse_args()

    overrides = {}
    for kv in args.overrides:
        if "=" not in kv:
            ap.error(f"--set 需 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, srcmap = get_rules("efficiency", city=None, district=None,
                              user_template=None, overrides=overrides)
    W = 52
    print("=" * W)
    print("得房率与单价换算器")
    print("=" * W)

    # ===== 模式1：双盘比价 =====
    if args.mode == "compare":
        if args.price_a is None or args.price_b is None or args.rate_a is None or args.rate_b is None:
            ap.error("compare 需要 --rate-a/--price-a/--rate-b/--price-b")
        ia = args.price_a / (args.rate_a / 100)
        ib = args.price_b / (args.rate_b / 100)
        ga, gb = args.label_a, args.label_b
        print(f"{'':<6}{'建面单价':>12}{'得房率':>8}{'套内单价':>12}")
        print(f"  {ga:<6}{args.price_a:>10,.0f}{args.rate_a:>7g}%{ia:>10,.0f}")
        print(f"  {gb:<6}{args.price_b:>10,.0f}{args.rate_b:>7g}%{ib:>10,.0f}")
        print("-" * W)
        if abs(ia - ib) < 0.5:
            print(f"★ 套内口径两盘打平（均 {fmt_money(ia)} 元/㎡）——建面价差刚好被得房率差抵消")
        else:
            winner, loser = (ga, gb) if ia < ib else (gb, ga)
            wv, lv = min(ia, ib), max(ia, ib)
            pct = (lv - wv) / lv * 100
            print(f"★ 套内口径实际更便宜：{winner}（{fmt_money(wv)} vs {fmt_money(lv)} 元/㎡，"
                  f"便宜 {pct:.1f}%）")
            if (args.price_a < args.price_b and ia > ib) or (args.price_b < args.price_a and ib > ia):
                cheap_gross = ga if args.price_a < args.price_b else gb
                print(f"  ⚠️ {cheap_gross}建面单价更低是幻觉——得房率差距吃掉了价差，"
                      f"同样的'一平米家'你多花钱了。")
        return

    # ===== 得房率解析 =====
    type_rate = {"garden": 0.86, "plate": 0.82, "tower": 0.77,
                 "super": 0.75, "apartment": 0.62}
    type_label = {"garden": "洋房/低密", "plate": "小高层板楼", "tower": "高层塔楼",
                  "super": "超高层", "apartment": "商住公寓"}
    if args.rate is not None:
        rate = args.rate / 100
        rate_src = f"指定 {args.rate:g}%"
    elif args.type and args.type in type_rate:
        rate = float(rules.get(f"rate_{args.type}", type_rate[args.type]))
        rate_src = f"{type_label[args.type]}档 {rate*100:g}%"
    else:
        rate = float(rules.get("rate_default", 0.78))
        rate_src = f"默认档 {rate*100:g}%（--type/--rate 可指定）"

    # ===== 模式2/3：面积链 & 单价换算 =====
    if args.gross is None and args.inner is None:
        ap.error("需要 --gross（建面）或 --inner（套内建面）其一")
    if args.gross is not None:
        inner = args.gross * rate
        gross = args.gross
    else:
        inner = args.inner
        gross = inner / rate

    shared = gross - inner
    use_coef = args.use_coef if args.use_coef is not None else float(rules.get("use_coef", 0.88))
    use_area = inner * use_coef
    total_price_hint = f"｜ 总价≈{fmt_money(gross * args.price_gross)} 元" if args.price_gross and args.mode == "price" else ""

    print(f"得房率: {rate_src}")
    print(f"建筑面积: {gross:.2f} ㎡ → 套内建面: {inner:.2f} ㎡ ｜ 公摊: {shared:.2f} ㎡")
    print(f"套内使用面积估算: ≈{use_area:.2f} ㎡（系数{use_coef*100:g}%，"
          f"扣套内墙体/阳台半积）")
    print(f"  → 你花钱买 {gross:.0f}㎡，实际能用 ≈{use_area:.1f} ㎡"
          f"（{use_area/gross*100:.1f}%）")
    if args.mode == "price" or args.price_gross or args.price_inner:
        print("-" * W)
        if args.price_gross:
            print(f"建面单价 {fmt_money(args.price_gross)} 元/㎡ "
                  f"→ 套内单价 {fmt_money(args.price_gross/rate)} 元/㎡")
        if args.price_inner:
            print(f"套内单价 {fmt_money(args.price_inner)} 元/㎡ "
                  f"→ 建面单价 {fmt_money(args.price_inner*rate)} 元/㎡")
        if args.price_gross and args.price_inner:
            implied = args.price_inner * rate
            diff = args.price_gross - implied
            tag = "一致✓" if abs(diff) < 1 else f"差异 {diff:+,.0f} 元/㎡"
            print(f"  双向核对: {tag}")
    if total_price_hint:
        print(total_price_hint)
    print("-" * W)
    keys = [k for k in ("rate_default", "use_coef") if k in rules]
    if args.type and f"rate_{args.type}" in rules:
        keys.insert(0, f"rate_{args.type}")
    print("口径出处:")
    print(fmt_provenance(srcmap, keys) if keys else "  · 行业参考区间（非官方标准），以测绘报告/合同为准")
    print("提醒: 得房率以《面积测绘报告》为准；2023-08住建部拟推套内计价，现行合同仍按建面。")


if __name__ == "__main__":
    main()
