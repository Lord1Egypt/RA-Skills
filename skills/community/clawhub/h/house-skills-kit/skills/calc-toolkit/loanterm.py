#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具25 · 房龄与贷款年限测算器（三线取短）

用法:
  # 房龄12年 借款人35岁 商贷
  python3 loanterm.py --house-age 12 --age 35 --mode commercial

  # 公积金 退休后+5 年口径（昆明等）
  python3 loanterm.py --house-age 8 --age 50 --mode provident --city 昆明

  # 看未来：5年/10年后这房还能贷几年
  python3 loanterm.py --house-age 12 --age 35 --years-later 5

规则（三线取最短，演示档参数可 --set 覆盖）:
  ① 商贷上限:     默认30年
  ② 房龄线:       max_term + house_age ≤ 40（部分银行30/50，--set age_plus_term_cap）
  ③ 年龄线:       age + term ≤ 65（部分银行70/80，--set age_cap）
     公积金: 上限25年(国管) / 30年(地方)，age+term ≤ 法定退休+5（男65/女60演示档），
             且须低于土地剩余年限（这里按房龄线简化）
  超龄房: 房龄>25年普遍降成/慎贷，>40年基本拒贷（可 --set 调）
"""
import argparse

W = 58


def get_rules(city=None):
    try:
        from ruleengine import get_rules as _gr
        rules, _ = _gr("loanterm", city=city)
        return rules
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description="房龄与贷款年限测算（三线取短）")
    ap.add_argument("--house-age", type=int, help="房龄（年）")
    ap.add_argument("--age", type=int, default=35, help="借款人年龄（默认35）")
    ap.add_argument("--mode", choices=["commercial", "provident"], default="commercial")
    ap.add_argument("--city", default=None)
    ap.add_argument("--years-later", type=int, default=0, help="看N年后可贷年限（默认0=现在）")
    ap.add_argument("--set", action="append", default=[])
    args = ap.parse_args()

    if args.house_age is None:
        ap.print_help()
        return

    R = get_rules(city=args.city)
    for kv in args.set:
        if "=" in kv:
            k, v = kv.split("=", 1)
            try:
                R[k] = float(v)
            except ValueError:
                R[k] = v

    ha = args.house_age + args.years_later
    age = args.age + args.years_later

    if args.mode == "provident":
        cap = float(R.get("pf_max_term", 25))          # 上限（国管25/地方30）
        retire = float(R.get("pf_retire_plus5", 65))   # 法定退休+5（演示档男65）
        age_plus = 65.0                                # 公积金无房龄线，但受退休线约束
        age_cap = retire
    else:
        cap = float(R.get("max_term", 30))
        age_plus = float(R.get("age_plus_term_cap", 40))
        age_cap = float(R.get("age_cap", 65))

    t1 = cap
    t2 = age_plus - ha
    t3 = age_cap - age
    best = max(0, min(t1, t2, t3))
    binding = ["①上限线", "②房龄线", "③年龄线"][[t1, t2, t3].index(min(t1, t2, t3))] if best > 0 else "—"

    print("=" * W)
    print(f"房龄与贷款年限测算（{args.years_later}年后视角 · 演示档）")
    print("=" * W)
    print(f"房龄 {ha} 年 ｜ 借款人 {age} 岁 ｜ {'公积金' if args.mode == 'provident' else '商贷'}"
          + (f" ｜ {args.city}档" if args.city else ""))
    print("-" * W)
    print("三条线（取最短）:")
    print(f"  ① 贷款上限线:   {t1:g} 年")
    print(f"  ② 房龄线:       {age_plus:g} − {ha} = {t2:g} 年")
    print(f"  ③ 年龄线:       {age_cap:g} − {age} = {t3:g} 年")
    print("-" * W)
    if best == 0:
        print("★ 可贷年限: 0 年 —— 基本拒贷区间")
        print("  （房龄超25年普遍降成慎贷、超40年基本拒贷；可--set放宽银行口径再试）")
    else:
        print(f"★ 可贷年限: {best:g} 年（瓶颈={binding}）")
    print("-" * W)
    print("房龄递减表（同龄借款人，每5年）:")
    print(f"  {'房龄':>6} {'房龄线':>8} {'年龄线':>8} {'可贷':>8}")
    for h in range(ha, min(ha + 26, 45), 5):
        t2i = age_plus - h
        t3i = age_cap - age + (h - ha)
        bi = max(0, min(cap, t2i, t3i))
        mark = " ←当前" if h == ha else ""
        print(f"  {h:>6} {t2i:>8g} {t3i:>8g} {bi:>8g}{mark}")
    print("-" * W)
    print("提示:")
    print("  · 各银行差异大：房龄线30/40/50年、年龄上限65/70/80均有；以经办行口径为准")
    print("  · 公积金上限: 国管25年/地方30年；退休+5口径（男65/女60演示档）")
    print("  · 二手房另有土地剩余年限约束（贷款到期≤土地到期，通常还须余3年+）")


if __name__ == "__main__":
    main()
