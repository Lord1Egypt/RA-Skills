#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具09 · 首套/二套认定器（商贷/公积金/契税三口径）
清单序号：⑥｜规则来源：tools/rules/cities.yaml::recognition（三层引擎 + 层4 --set）
三个口径分别认定（同一套房在三个系统里可能档位不同，销售最易踩坑）：
  ① 商贷口径：认房不认贷（2023-08 三部门推动，全国主要城市已落地）→ 只看家庭在本市住房套数；
     认房又认贷城市（城市段覆盖 commerce_mode）→ 还看全国房贷记录
  ② 公积金口径：普遍认房又认贷+看公积金使用次数（二次使用利率上浮）
  ③ 契税口径：按家庭在本市住房套数（认房不认贷），三套及以上无优惠
输出联动：认出的 first 档可直接传给 tax.py --first / capacity.py --first / mortgage.py

示例：
  python3 status.py --city 昆明 --local-homes 0 --prior-loans 2   # 名下无房但有过2次房贷→商贷仍按首套
  python3 status.py --city 昆明 --local-homes 1 --selling 1       # 卖一买一→按首套
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance


def main():
    p = argparse.ArgumentParser(description="首套/二套认定器：商贷/公积金/契税三口径分别判定")
    p.add_argument("--city", default=None, help="城市（读城市段认定口径档）")
    p.add_argument("--district", default=None, help="区县（第三层覆盖）")
    p.add_argument("--local-homes", type=int, default=0, help="家庭在本市名下成套住宅套数")
    p.add_argument("--prior-loans", type=int, default=0, help="家庭全国住房贷款记录次数（含已结清）")
    p.add_argument("--selling", type=int, default=0, help="本次同步卖出套数（卖一买一）")
    p.add_argument("--fund-used", type=int, default=0, help="家庭历史使用公积金贷款次数")
    p.add_argument("--area", type=float, default=None, help="本次购买面积㎡（用于契税档提示）")
    p.add_argument("--price", type=float, default=None, help="总价元（用于首付金额示例）")
    p.add_argument("--template", default=None, help="用户模板名（第四层）")
    p.add_argument("--set", action="append", default=[], dest="overrides",
                   help="即时覆盖规则值，如 --set commerce_mode=home_and_loan")
    args = p.parse_args()

    def _num(s):
        s = s.strip()
        try:
            return int(s)
        except ValueError:
            pass
        try:
            return float(s)
        except ValueError:
            return s          # 枚举值（如 home_and_loan）原样返回

    ov = {}
    for kv in args.overrides or []:
        k, _, v = kv.partition("=")
        ov[k.strip()] = _num(v)

    rules, srcmap = get_rules("recognition", city=args.city, district=args.district,
                              user_template=args.template, overrides=ov)
    cap_rules, _ = get_rules("capacity", city=args.city, district=args.district,
                             user_template=args.template)

    city_label = args.city or "全国默认档"
    selling = min(max(args.selling, 0), max(args.local_homes, 0))
    if selling < args.selling:
        print(f"⚠ 卖出套数({args.selling})大于名下套数({args.local_homes})，已按 {selling} 计算")
    homes_after = max(args.local_homes - selling, 0)   # 扣除同步卖出后的名下套数
    loans = max(args.prior_loans, 0)
    fund_used = max(args.fund_used, 0)

    # ── ① 商贷口径 ──
    mode = str(rules.get("commerce_mode", "no_loan"))
    if mode == "no_loan":
        c_first = homes_after == 0
        basis = f"认房不认贷：只看本市名下住房 {homes_after} 套（房贷记录 {loans} 次不影响）"
    else:
        c_first = homes_after == 0 and loans == 0
        basis = f"认房又认贷：本市住房 {homes_after} 套 × 全国房贷记录 {loans} 次"
    c_grade = 1 if c_first else (2 if homes_after <= 1 or mode == "no_loan" else 3)

    # ── ② 公积金口径 ──
    f_mode = str(rules.get("fund_mode", "home_and_loan"))
    if homes_after == 0 and fund_used == 0:
        fund_grade, fund_note = 1, "首次使用公积金，利率按首套"
    elif homes_after == 0 and fund_used >= 1:
        fund_grade, fund_note = 2, f"名下无房但公积金已用 {fund_used} 次→二次贷款，利率上浮约10%"
    else:
        fund_grade, fund_note = 2, f"名下有房 {homes_after} 套→按二套公积金（部分城市停贷，以当地公积金中心为准）"

    # ── ③ 契税口径 ──
    t_grade = 1 if homes_after == 0 else (2 if homes_after == 1 else 3)
    area = args.area
    if t_grade <= 2:
        if area is not None and area > 140:
            deed_note = f"{("首套" if t_grade == 1 else "二套")}套/{area:g}㎡>140㎡→契税 {'1.5%' if t_grade == 1 else '2%'}"
        else:
            deed_note = f"{("首套" if t_grade == 1 else "二套")}套{'/' + format(area, 'g') + '㎡≤140㎡' if area else ''}→契税 1%"
    else:
        deed_note = "三套及以上→契税 3%（无优惠档）"

    # ── 首付联动（读 capacity 域） ──
    down_first = cap_rules.get("min_down_first", 0.15)
    down_second = cap_rules.get("min_down_second", 0.25)
    down_rate = down_first if c_grade == 1 else down_second
    down_line = f"商贷最低首付 {down_rate:.0%}" + (
        f"（如总价 200 万→首付 {2000000 * down_rate:,.0f} 元）" if not args.price and c_grade <= 2 else (
            f"（本次总价 {args.price:,.0f} 元→首付约 {args.price * down_rate:,.0f} 元）" if args.price else ""))

    W = 46
    print("┌" + "─" * W + "┐")
    print(f"│ 首套/二套认定 · {city_label}".ljust(W + 1) + "│")
    print("├" + "─" * W + "┤")
    print(f"│ 输入：本市住房 {args.local_homes} 套（同步卖出 {selling}）".ljust(W + 1) + "│")
    print(f"│       全国房贷记录 {loans} 次 ｜ 公积金已用 {fund_used} 次".ljust(W + 1) + "│")
    print("├" + "─" * W + "┤")
    print(f"│ ① 商贷认定：{'首套' if c_grade == 1 else ('二套' if c_grade == 2 else '三套及以上')}".ljust(W + 1) + "│")
    print(f"│    {basis}".ljust(W + 1) + "│")
    print(f"│    {down_line}".ljust(W + 1) + "│")
    print(f"│ ② 公积金认定：{'首套（首次）' if fund_grade == 1 else '二套/受限'}".ljust(W + 1) + "│")
    print(f"│    {fund_note}".ljust(W + 1) + "│")
    print(f"│ ③ 契税认定：{'首套' if t_grade == 1 else ('二套' if t_grade == 2 else '三套及以上')}".ljust(W + 1) + "│")
    print(f"│    {deed_note}".ljust(W + 1) + "│")
    print("├" + "─" * W + "┤")
    g = 1 if c_grade == 1 else 2
    print(f"│ 联动：tax.py --first {t_grade if t_grade <= 2 else 2} …（契税）".ljust(W + 1) + "│")
    print(f"│       capacity.py / mortgage.py --first {g}（商贷）".ljust(W + 1) + "│")
    if c_grade >= 3:
        print("│ ⚠ 名下多套：多数城市三套停贷，需全款或先卖".ljust(W + 1) + "│")
    print("└" + "─" * W + "┘")
    print("假设与免责：各城市认定口径与执行时点差异大（多孩/区县/公积金细则），以当地住建、银行与公积金中心当期口径为准；--set 可覆盖 commerce_mode/fund_mode。")
    print(fmt_provenance(srcmap, list(dict.fromkeys(["commerce_mode", "fund_mode"] + sorted(ov.keys())))))


if __name__ == "__main__":
    main()
