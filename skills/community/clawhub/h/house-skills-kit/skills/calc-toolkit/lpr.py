#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具20 · LPR变动影响测算器（重定价月供变化 / 情景沙盘 / 重定价周期选择）

用法:
  # 重定价测算：100万30年，当前利率3.6%，LPR降至3.5%时月供怎么变
  python3 lpr.py --loan 1000000 --years 30 --rate 3.6 --new-lpr 3.5

  # 情景沙盘：LPR ±10/25/50BP 全景表
  python3 lpr.py --loan 1000000 --years 25 --paid 24 --rate 4.0 --sand

  # 重定价周期选择：3/6/12个月怎么选（利率趋势--trend down/up/flat）
  python3 lpr.py --loan 1000000 --years 30 --rate 3.6 --cycle-choose --trend down

口径（2026-08-31查证）:
  · 5年期以上LPR=3.50%（2025-05-20起未动，中国银行LPR官方表2026-07-20）
  · 1年期LPR=3.00%；LPR每月20日发布（节假日顺延），0.05%步长
  · 房贷利率=LPR+加点；重定价时加点不变，仅LPR部分浮动
  · 重定价周期：默认12个月；2024-11-01起可申请改3/6个月（存续期仅可改一次，央行11号公告）
  · 锚点：100万/30年/等额本息，LPR降25BP→月供省约145元/30年累计约5.2万（百度百科官方测算）
"""
import argparse
import sys

W = 58


def fmt_money(x):
    return f"{x:,.0f}"


def annuity_payment(principal, annual_rate, months):
    """等额本息月供。利率为0时直接摊本金。"""
    if months <= 0:
        return 0.0
    r = annual_rate / 12
    if r <= 0:
        return principal / months
    g = (1 + r) ** months
    return principal * r * g / (g - 1)


def remaining_balance(pay, annual_rate, months_left):
    """剩余本金（等额本息，给定月供/利率/剩余期数）"""
    r = annual_rate / 12
    if r <= 0:
        return pay * months_left
    g = (1 + r) ** months_left
    return pay * (g - 1) / (r * g)


def total_interest(pay, principal, months):
    return pay * months - principal


def get_rules():
    """与库内其他工具一致的规则读取（cities.yaml lpr域）。"""
    try:
        from ruleengine import get_rules as _gr
        rules, srcmap = _gr("lpr")
        return rules, srcmap
    except Exception:
        return {}, {}


def main():
    ap = argparse.ArgumentParser(description="LPR变动影响测算器（演示档）")
    ap.add_argument("--loan", type=float, help="贷款余额/本金（元）")
    ap.add_argument("--years", type=float, help="原贷款年限（年）")
    ap.add_argument("--paid", type=float, default=0, help="已还期数（月，默认0=新贷）")
    ap.add_argument("--rate", type=float, help="当前执行利率%%（如3.6）")
    ap.add_argument("--new-lpr", type=float, help="新5Y+LPR%%（重定价基准，默认取规则库现值3.5）")
    ap.add_argument("--spread", type=float, default=None,
                    help="合同加点BP（重定价时保持不变）。默认=当前利率−现行LPR（适用于近期贷款）；"
                         "老贷款务必按合同填，如签约时LPR4.2%%+55BP则填55，勿按现行LPR反推")
    ap.add_argument("--method", choices=["equal", "principal"], default="equal",
                    help="还款方式：equal=等额本息（默认）/ principal=等额本金（重定价测算仅支持equal）")
    ap.add_argument("--sand", action="store_true", help="情景沙盘：±10/25/50BP全景表")
    ap.add_argument("--cycle-choose", action="store_true", help="重定价周期3/6/12选择建议")
    ap.add_argument("--trend", choices=["down", "up", "flat"], default="flat",
                    help="利率趋势判断（配合--cycle-choose）")
    ap.add_argument("--next-days", type=int, default=None, help="距下次重定价天数（配合--cycle-choose）")
    ap.add_argument("--city", default=None, help="城市名（读城市档，暂全国默认档）")
    ap.add_argument("--set", action="append", default=[], help="覆盖参数 k=v（可多次）")
    args = ap.parse_args()

    if not args.loan or not args.rate:
        ap.print_help()
        sys.exit(1)
    if args.method == "principal" and (args.new_lpr is not None or args.sand):
        print("提示：等额本金场景建议改用 mortgage.py（重定价重算逻辑不同），或切 --method equal")
        sys.exit(1)

    rules, srcmap = get_rules()
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

    cur_lpr = float(rules.get("lpr_5y", 3.5)) / 100
    if args.new_lpr is not None:
        new_lpr = args.new_lpr / 100
    else:
        new_lpr = cur_lpr
    cur_rate = args.rate / 100
    spread = (args.spread / 10000) if args.spread is not None else (cur_rate - cur_lpr)

    years = args.years
    total_months = int(round(years * 12))
    paid = int(round(args.paid))
    months_left = total_months - paid
    loan = args.loan

    # 当前状态
    pay_now = annuity_payment(loan, cur_rate, months_left if paid > 0 else total_months)
    n_now = months_left if paid > 0 else total_months

    print("=" * W)
    print("LPR 变动影响测算（演示档 · 以合同与银行核算为准）")
    print("=" * W)
    src_note = "全国默认档" if not args.city else f"{args.city}档"
    print(f"规则来源: {src_note} · 5Y+LPR现值 {cur_lpr*100:.2f}%（规则库时点见 cities.yaml as_of）")
    print(f"贷款余额 {fmt_money(loan)} 元 ｜ 剩余 {n_now} 期 ｜ 当前利率 {cur_rate*100:.2f}%"
          f"（=LPR {cur_lpr*100:.2f}% {'+' if spread>=0 else '−'}{abs(spread)*10000:.0f}BP）")

    # ── 单次重定价测算 ──
    new_rate = new_lpr + spread
    basis_from = cur_rate - spread   # 上一个重定价基准 = 当前执行利率 − 合同加点（老贷款≠现行LPR）
    if abs(new_rate - cur_rate) > 1e-9:
        pay_new = annuity_payment(loan, new_rate, n_now)
        diff_m = pay_now - pay_new
        diff_total = diff_m * n_now
        print("-" * W)
        print(f"重定价：定价基准 {basis_from*100:.2f}% → {new_lpr*100:.2f}%"
              f"（合同加点 {spread*10000:+.0f}BP 不变）")
        print(f"  执行利率: {cur_rate*100:.2f}% → {new_rate*100:.2f}%")
        print(f"  月供: {fmt_money(pay_now)} → {fmt_money(pay_new)} 元"
              f"（{'省' if diff_m > 0 else '增'}{fmt_money(abs(diff_m))} 元/月）")
        print(f"  剩余期数合计: {'省' if diff_total > 0 else '多付'} {fmt_money(abs(diff_total))} 元利息")
        print(f"  （重定价日生效，当期按旧利率计息，次月起按新月供）")
    else:
        print("-" * W)
        print(f"LPR维持 {new_lpr*100:.2f}%：重定价月供不变（{fmt_money(pay_now)} 元）")

    # ── 情景沙盘 ──
    if args.sand:
        print("-" * W)
        print(f"情景沙盘（余额 {fmt_money(loan)} 元 / 剩余 {n_now} 期 / 等额本息）")
        print(f"{'LPR变动':>8} {'执行利率':>9} {'月供':>10} {'月供变化':>9} {'剩余利息':>12}")
        base_pay = pay_now
        base_int = total_interest(pay_now, loan, n_now)
        for bp in (-50, -25, -10, 0, 10, 25, 50):
            r = cur_rate + bp / 10000
            p = annuity_payment(loan, r, n_now)
            ti = total_interest(p, loan, n_now)
            d = base_pay - p
            print(f"{bp:>+6d}BP {r*100:>8.2f}% {fmt_money(p):>10} "
                  f"{'省' if d > 0 else '增'}{fmt_money(abs(d)) if bp != 0 else '—':>7} "
                  f"{fmt_money(ti):>12}")
        print(f"  基准：当前月供 {fmt_money(base_pay)} 元 / 剩余利息合计 {fmt_money(base_int)} 元")

    # ── 重定价周期选择 ──
    if args.cycle_choose:
        print("-" * W)
        print("重定价周期选择（3/6/12个月，存续期内仅可改一次·央行2024-11机制）")
        cyc = {3: "3个月", 6: "6个月", 12: "12个月"}
        trend_txt = {"down": "利率下行期", "up": "利率上行期", "flat": "利率平稳期"}[args.trend]
        rec = {"down": "选短周期（3个月）：每次降息最快吃到，重定价等待最短",
               "up": "选长周期（12个月）：锁定当前低利率更久，推迟加息冲击",
               "flat": "维持12个月默认即可，改周期收益有限（存续期仅一次，留着降息前用）"}[args.trend]
        print(f"  当前判断: {trend_txt}")
        print(f"  ★ 建议: {rec}")
        if args.next_days is not None:
            months_wait = args.next_days / 30
            save_est = None
            if args.trend == "down" and abs(new_rate - cur_rate) > 1e-9:
                pay_new = annuity_payment(loan, new_rate, n_now)
                save_est = (pay_now - pay_new) * months_wait
                print(f"  距下次重定价 {args.next_days} 天（≈{months_wait:.1f}个月）："
                      f"若期间LPR降至{new_lpr*100:.2f}%，晚重定价≈多付 {fmt_money(save_est)} 元")
            elif args.next_days == 0:
                print(f"  已到重定价日：本次LPR即生效")
        print("  提示: 改周期一次机会，利率下行初期改短最划算；已处低位慎改（防止上行期反噬）")

    # ── 溯源 ──
    print("-" * W)
    print("参数来源（规则版本可追溯）:")
    for k in ("lpr_5y", "lpr_1y"):
        if k in rules:
            src = srcmap.get(k, "全国默认档") if isinstance(srcmap, dict) else "全国默认档"
            print(f"  · {k} = {rules[k]}  来源[{src}]")
    print("  · 锚点验证: 100万30年降25BP→月供省145元/累计5.2万（百科官方测算口径）")
    print("免责声明: 演示档，重定价细则以贷款合同与承贷银行核算为准")


if __name__ == "__main__":
    main()
