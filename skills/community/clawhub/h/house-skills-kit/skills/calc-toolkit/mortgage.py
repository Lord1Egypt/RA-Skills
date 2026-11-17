#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具01 · 房贷月供计算器（商贷/公积金/组合 × 等额本息/本金）
清单序号：⑦-1｜规则来源：tools/rules/cities.yaml（三层引擎）
用法示例：
  python3 mortgage.py --price 1500000 --downpay 30 --years 30 --city 昆明
  python3 mortgage.py --loan 1000000 --years 30 --mode provident --city 成都
  python3 mortgage.py --price 2000000 --downpay 35 --years 30 --combo 1000000 --city 武汉
    （--combo = 公积金部分本金，其余为商贷）
  python3 mortgage.py --template my_kunming --price 1500000 --downpay 30 --years 30
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance, COMPLIANCE, save_user_template  # noqa: E402


def annuity(principal, monthly_rate, n):
    """等额本息：月供 / 总利息"""
    if monthly_rate == 0:
        return principal / n, 0.0
    m = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-n))
    return m, m * n - principal


def linear(principal, monthly_rate, n):
    """等额本金：首月月供 / 总利息 / 月递减额"""
    base = principal / n
    if monthly_rate == 0:
        return base, 0.0, 0.0
    first = base + principal * monthly_rate
    total_int = principal * monthly_rate * (n + 1) / 2
    return first, total_int, base * monthly_rate


def run_part(principal, rate, years, label):
    n = years * 12
    i = rate / 12
    am, ai = annuity(principal, i, n)
    lf, li, dec = linear(principal, i, n)
    return {
        "label": label, "principal": principal, "rate": rate,
        "annuity_monthly": am, "annuity_interest": ai,
        "linear_first": lf, "linear_interest": li, "linear_decrease": dec,
    }


def fmt_w(x):
    return f"{x/10000:,.2f}万"


def main():
    ap = argparse.ArgumentParser(description="房贷月供计算器（⑦-1）")
    ap.add_argument("--price", type=float, help="总价（元）")
    ap.add_argument("--downpay", type=float, help="首付成数（如 30 = 三成）")
    ap.add_argument("--loan", type=float, help="直接指定贷款本金（元，与price二选一）")
    ap.add_argument("--combo", type=float, default=0, help="组合贷：公积金部分本金（元）")
    ap.add_argument("--years", type=int, required=True, help="贷款年限")
    ap.add_argument("--mode", choices=["commercial", "provident"], default="commercial")
    ap.add_argument("--city"); ap.add_argument("--district")
    ap.add_argument("--template", help="我的模板名（层3）")
    ap.add_argument("--save-template", help="把本次城市参数存为我的模板（配合--city）")
    args = ap.parse_args()

    rules, prov = get_rules("loan", args.city, args.district, args.template)

    if args.save_template and args.city:
        import yaml
        p = save_user_template(args.save_template, {"loan": {k: v for k, v in rules.items() if not k.startswith("_")}})
        print(f"[模板] 已保存我的模板 → {p}\n")

    # 贷款本金
    if args.loan:
        principal = args.loan
    elif args.price and args.downpay:
        principal = args.price * (1 - args.downpay / 100)
    else:
        sys.exit("需要 --price+--downpay 或 --loan 之一")

    parts = []
    if args.combo > 0:
        rest = principal - args.combo
        if rest <= 0:
            sys.exit("--combo 不能大于等于贷款总额")
        parts.append(run_part(args.combo, rules["provident_rate"], args.years, "公积金"))
        parts.append(run_part(rest, rules["commercial_rate"], args.years, "商贷"))
    elif args.mode == "provident":
        parts.append(run_part(principal, rules["provident_rate"], args.years, "公积金"))
    else:
        parts.append(run_part(principal, rules["commercial_rate"], args.years, "商贷"))

    W = lambda x: f"{x:,.0f}"
    print(f"＝ 月供试算 ｜ 本金 {W(principal)} 元 ｜ {args.years}年（{args.years*12}期）"
          f"{' ｜ 城市:'+args.city if args.city else ' ｜ 全国默认档'}"
          f"{'/'+args.district if args.district else ''}\n")

    total_am = sum(p["annuity_monthly"] for p in parts)
    total_ai = sum(p["annuity_interest"] for p in parts)
    total_lf = sum(p["linear_first"] for p in parts)
    total_li = sum(p["linear_interest"] for p in parts)
    dec = sum(p["linear_decrease"] for p in parts)

    if len(parts) == 1:
        p = parts[0]
        rate_pct = f"{p['rate']*100:.2f}%"
        print(f"【{p['label']} 利率{rate_pct}】")
    else:
        detail = " + ".join(f"{p['label']}{fmt_w(p['principal'])}@{p['rate']*100:.2f}%" for p in parts)
        print(f"【组合贷】{detail}")

    print("─" * 56)
    print(f"{'方案':<10}{'月供':>14}{'利息总额':>14}")
    print(f"{'等额本息':<10}{W(total_am)+' 元':>16}{W(total_ai)+' 元':>16}")
    print(f"{'等额本金':<10}{'首月 '+W(total_lf):>16}{W(total_li)+' 元':>16}")
    print(f"  · 等额本金逐月递减约 {W(dec)} 元/月，末月约 {W(total_lf - dec*(args.years*12-1))} 元")
    print(f"  · 两方案利息差 ≈ {W(total_ai - total_li)} 元（等额本金更省息、前期压力更大）")

    if args.price and args.downpay:
        dp = args.price * args.downpay / 100
        min_dp = rules.get("downpay_min_first", 0.15)
        flag = "✓" if args.downpay / 100 >= min_dp - 1e-9 else "✗ 低于当地最低首付档"
        print(f"  · 首付 {W(dp)} 元（{args.downpay}成）{flag}")

    print()
    keys = ["commercial_rate", "provident_rate", "downpay_min_first"] if len(parts) > 1 or args.mode == "commercial" \
        else ["provident_rate"]
    print(fmt_provenance(prov, [k for k in keys if k in prov]))
    print()
    print(COMPLIANCE)


if __name__ == "__main__":
    main()
