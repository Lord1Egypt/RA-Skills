#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具07 · 提前还款测算器（缩期 vs 减月供 + 违约金提示）
清单序号：⑦-3｜规则来源：tools/rules/cities.yaml::prepayment（三层引擎 + 层4 --set）
输入两通道：--balance 直接给剩余本金；或 --loan --rate --years --paid 由等额本息公式推导。
方案对比：A 不提前还（现状）｜B 提前还+缩短期限（月供不变）｜C 提前还+减少月供（期限不变）
数字口径：等额本息（与 mortgage.py 同引擎公式）；一切费率 --set 可覆盖。
"""
import argparse, sys, os, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance

def annuity_m(P, i, n):
    """等额本息月供：本金P、月利率i、n个月"""
    if i <= 0:
        return P / n
    return P * i / (1 - (1 + i) ** (-n))

def remaining_balance(P, i, n, paid):
    """等额本息还了 paid 期后的剩余本金"""
    if paid <= 0:
        return P
    if paid >= n:
        return 0.0
    m = annuity_m(P, i, n)
    # 剩余本金 = 月供的年金现值
    return m * (1 - (1 + i) ** (-(n - paid))) / i if i > 0 else m * (n - paid)

def months_to_payoff(P, m, i):
    """本金P、月供m、月利率i → 还清所需月数（向上取整）"""
    if i <= 0:
        return math.ceil(P / m)
    x = 1 - P * i / m
    if x <= 0:
        return 1  # 月供连本带息都不够还息（极端），至少1期
    return math.ceil(-math.log(x) / math.log(1 + i))

def fmt(n):
    return f"{n:,.0f}"

def main():
    ap = argparse.ArgumentParser(description="提前还款测算器：缩期 vs 减月供（等额本息）")
    ap.add_argument("--loan", type=float, help="原贷款本金（元）")
    ap.add_argument("--rate", type=float, help="年利率%（如 3.10）")
    ap.add_argument("--years", type=int, help="原贷款年限（年）")
    ap.add_argument("--paid", type=int, default=0, help="已还期数（月）")
    ap.add_argument("--balance", type=float, help="剩余本金（元）——直接给则忽略 loan/years 推导")
    ap.add_argument("--prepay", type=float, required=True, help="拟提前还款金额（元）")
    ap.add_argument("--city", default=None, help="城市（读城市段规则）")
    ap.add_argument("--district", default=None, help="区县（读区县段规则）")
    ap.add_argument("--template", default=None, help="我的模板名")
    ap.add_argument("--save-template", default=None, dest="save_template", help="把 --set 参数存为我的模板")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="即时覆盖任意规则值，如 --set penalty_rate=0.01")
    args = ap.parse_args()

    def _num(s):
        """--set 值解析：int → float → str"""
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s

    overrides = {}
    for kv in args.overrides:
        if "=" not in kv:
            ap.error(f"--set 需 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, srcmap = get_rules("prepayment", city=args.city, district=args.district,
                              user_template=args.template, overrides=overrides)

    # ── 入参归一 ─────────────────────────────────────
    if args.balance:
        P0, rate_note = args.balance, "直接给定剩余本金"
        if not (args.rate and args.paid is not None):
            ap.error("用 --balance 时仍需 --rate（当前执行利率%）和 --paid（已还期数，未还过填0）"
                     "以及 --years（原期限）以便计算剩余期数")
        n_total, n_left = args.years * 12, args.years * 12 - args.paid
    else:
        if not (args.loan and args.rate and args.years):
            ap.error("需 --loan --rate --years（或改用 --balance 直接给剩余本金）")
        P0, n_total = args.loan, args.years * 12
        n_left = n_total - (args.paid or 0)
        rate_note = "由贷款参数推导"

    i = args.rate / 100 / 12
    M = annuity_m(P0, i, n_left)                     # 现状月供（按剩余期限重算=实际值）
    if args.balance and args.paid:
        # 若给了已还期数，月供应取原合同月供（按原期限算），剩余本金已另行给定
        M = annuity_m(args.loan or P0, i, n_total) if args.loan else M

    A = args.prepay
    if A <= 0:
        ap.error("--prepay 必须大于 0")
    if A >= P0:
        print(f"⚠ 拟还金额 {fmt(A)} ≥ 剩余本金 {fmt(P0)}，属结清场景，本工具仅测算部分提前还款。")
        return
    min_prepay = rules.get("min_prepay", 10000)
    pen_rate = rules.get("penalty_rate", 0.0)
    penalty = A * pen_rate

    # ── 现状基线（方案A）─────────────────────────────
    base_total_int = M * n_left - P0

    # ── 方案B：缩期（月供不变）───────────────────────
    P1 = P0 - A
    n_b = months_to_payoff(P1, M, i)
    int_b = M * n_b - P1
    save_b = base_total_int - int_b - penalty

    # ── 方案C：减月供（期限不变）─────────────────────
    M_c = annuity_m(P1, i, n_left)
    int_c = M_c * n_left - P1
    save_c = base_total_int - int_c - penalty

    # ── 输出 ────────────────────────────────────────
    W = 46
    print("═" * W)
    print("提前还款测算 · 缩期 vs 减月供（等额本息）")
    print("═" * W)
    print(f"剩余本金        {fmt(P0)} 元        （{rate_note}）")
    print(f"执行利率        {args.rate:g}%/年（月利率 {i*100:.4f}%）")
    print(f"剩余期限        {n_left} 期（{n_left/12:.1f} 年）")
    print(f"现状月供        {fmt(M)} 元")
    print(f"拟提前还款      {fmt(A)} 元" + (f"　违约金 {pen_rate*100:g}% = {fmt(penalty)} 元" if penalty else ""))
    if A < min_prepay:
        print(f"⚠ 低于常见最低提前还款额 {fmt(min_prepay)} 元（多数银行要求1万起、按万取整），先与贷款行确认。")
    if pen_rate == 0:
        print("· 违约金按 0 计：多数银行还款满 1-3 年免收，具体以你的借款合同为准（可 --set penalty_rate=0.01 改）。")

    print("─" * W)
    print(f"【方案A】不提前还：总利息 {fmt(base_total_int)} 元（基准）")
    print("─" * W)
    print(f"【方案B】还 {fmt(A)} 元 + 缩短期限（月供不变 {fmt(M)}）")
    print(f"  剩余期限  {n_left} 期 → {n_b} 期（少还 {n_left-n_b} 期 ≈ {(n_left-n_b)/12:.1f} 年）")
    print(f"  剩余总利息 {fmt(int_b)} 元　**节省利息 {fmt(save_b)} 元**" +
          (f"（已扣违约金 {fmt(penalty)}）" if penalty else ""))
    print("─" * W)
    print(f"【方案C】还 {fmt(A)} 元 + 减少月供（期限不变 {n_left} 期）")
    print(f"  月供  {fmt(M)} → {fmt(M_c)} 元（每月少 {fmt(M-M_c)}）")
    print(f"  剩余总利息 {fmt(int_c)} 元　**节省利息 {fmt(save_c)} 元**" +
          (f"（已扣违约金 {fmt(penalty)}）" if penalty else ""))
    print("─" * W)
    better = "B（缩期）" if save_b >= save_c else "C（减月供）"
    print(f"★ 纯省钱角度：{better} 更划算，多省 {fmt(abs(save_b-save_c))} 元")
    print("· 月供压力不大 → 选缩期；现金流紧张、想松一口气 → 选减月供。两者都真实省息。")
    print("═" * W)
    print("参数来源：" + fmt_provenance(srcmap, ["penalty_rate", "min_prepay"] + sorted(overrides.keys())).replace("参数来源（规则版本可追溯）：\n", ""))
    print("  以贷款银行实际测算与借款合同约定为准。")

if __name__ == "__main__":
    main()
