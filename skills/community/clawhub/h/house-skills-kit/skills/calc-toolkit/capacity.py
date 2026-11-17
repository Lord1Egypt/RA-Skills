#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具08 · 购房能力测算器（收入负债→可贷上限→可买总价，银行双线口径）
清单序号：⑦-5｜规则来源：tools/rules/cities.yaml::capacity（三层引擎 + 层4 --set）
银行审批两条硬线（取较小者定瓶颈）：
  ① 月供收入比（DTI）：(新月供+存量负债月供) ≤ 家庭月收入 × dti（默认 0.5）
  ② 首付成数：首付 ≥ 总价 × 最低首付比例（首套/二套分档）
输出：可买总价上限、瓶颈诊断（卡月供 or 卡首付）、推荐总价区间（留余量）、
      落地方案（总价→首付/贷款/月供/占比）与改善建议。
审批口径说明：银行按等额本息审贷，本工具仅按等额本息测算。
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance


def annuity_payment(principal: float, annual_rate: float, months: int) -> float:
    """等额本息月供。annual_rate=年利率（如0.031），months=总月数。"""
    r = annual_rate / 12.0
    if r <= 0:
        return principal / months
    k = (1 + r) ** months
    return principal * r * k / (k - 1)


def fmt_money(x: float) -> str:
    return f"{x:,.0f}"


def main() -> None:
    ap = argparse.ArgumentParser(description="购房能力测算器（⑦-5）：收入负债→可贷→可买总价")
    ap.add_argument("--income", required=True,
                    help="家庭月收入（元；多人用逗号相加，如 8000,6000）")
    ap.add_argument("--cash", required=True, type=float,
                    help="可用于首付的现金（元）")
    ap.add_argument("--debts", type=float, default=0,
                    help="存量负债月供合计（元；车贷/信用贷/其他房贷等）")
    ap.add_argument("--city", default=None, help="城市（规则库内置城市档）")
    ap.add_argument("--district", default=None, help="区/县（城市内二级覆盖）")
    ap.add_argument("--first", type=int, default=1, choices=[1, 2],
                    help="1=首套（默认）2=二套（影响最低首付）")
    ap.add_argument("--rate", type=float, default=None,
                    help="商贷年利率，如 3.1 表示 3.1%（默认读城市档 loan.commercial_rate）")
    ap.add_argument("--years", type=int, default=30, help="贷款年限（默认30）")
    ap.add_argument("--reserve", type=float, default=0,
                    help="从现金中预留的资金（税费/装修等，先扣再算首付）")
    ap.add_argument("--template", default=None, help="我的模板名（用户自定义规则）")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="即时覆盖规则值，如 --set dti=0.55")
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

    # ── 输入整理 ──
    income = sum(float(x) for x in str(args.income).replace("，", ",").split(",") if x.strip())
    if income <= 0:
        sys.exit("错误：--income 必须为正数（多人收入用逗号分隔相加）")
    cash = args.cash - args.reserve
    if cash <= 0:
        sys.exit("错误：现金扣去 --reserve 预留后 ≤ 0，无法测算")

    # 显式给利率时同步进 override（与城市档 commercial_rate 同键，保持同源）
    if args.rate is not None:
        overrides["commercial_rate"] = args.rate / 100.0
    rules, srcmap = get_rules("capacity", city=args.city, district=args.district,
                              user_template=args.template, overrides=overrides)
    # 利率在 capacity 域缺省时回退 loan 域（与 mortgage 同源）
    if "commercial_rate" not in rules:
        rules_loan, _ = get_rules("loan", city=args.city, district=args.district,
                                  user_template=args.template)
        rules["commercial_rate"] = rules_loan.get("commercial_rate", 0.031)

    rate = rules["commercial_rate"]
    dti = rules.get("dti", 0.5)
    down_key = "min_down_first" if args.first == 1 else "min_down_second"
    down_min = rules.get(down_key, 0.15 if args.first == 1 else 0.25)
    months = args.years * 12

    # ── 两条硬线测算 ──
    max_payment = income * dti - args.debts          # 可承受新月供
    pay_factor = annuity_payment(1.0, rate, months)  # 每 1 元贷款的月供系数
    loan_cap_dti = max_payment / pay_factor if max_payment > 0 else 0.0
    total_cap_dti = loan_cap_dti + cash              # 月供线总价上限（现金全部用作首付）

    total_cap_down = cash / down_min                 # 首付线总价上限

    total_cap = min(total_cap_dti, total_cap_down)
    bottleneck = "月供收入比（DTI）" if total_cap_dti <= total_cap_down else "首付成数"
    loan_cap = total_cap - cash                      # 对应贷款额（瓶颈方案下）

    # ── 输出 ──
    W = 52
    out = []
    out.append("═" * W)
    out.append("购房能力测算 · 银行双线口径（⑦-5）")
    out.append("═" * W)
    out.append(f"家庭月收入 {fmt_money(income)} 元 ｜ 存量负债月供 {fmt_money(args.debts)} 元"
               f" ｜ 可用首付现金 {fmt_money(cash)} 元" +
               (f"（已预留 {fmt_money(args.reserve)}）" if args.reserve else ""))
    out.append(f"利率 {rate*100:g}% ｜ {args.years}年 等额本息 ｜ "
               f"{'首套' if args.first == 1 else '二套'}最低首付 {down_min*100:g}%"
               + (f" ｜ 城市[{args.city}]" if args.city else " ｜ 默认档"))
    out.append("-" * W)
    out.append(f"① 月供线：可承受月供 {fmt_money(max_payment)} 元"
               f"（收入×{dti:g} − 存量负债）→ 可贷 {fmt_money(loan_cap_dti)} 元")
    out.append(f"② 首付线：现金 {fmt_money(cash)} ÷ {down_min*100:g}% → 总价上限 "
               f"{fmt_money(total_cap_down)} 元")
    out.append("-" * W)
    out.append(f"★ 可买总价上限 ≈ {fmt_money(total_cap)} 元（瓶颈：{bottleneck}）")
    # 推荐区间：留 5% 余量防评估价/税费挤占
    rec_hi = total_cap * 0.95
    out.append(f"  推荐看房总价区间：{fmt_money(rec_hi*0.85)} ~ {fmt_money(rec_hi)} 元"
               f"（上限留 5% 余量）")
    out.append("")
    out.append(f"落地方案（按上限）：总价 {fmt_money(total_cap)} = 首付 {fmt_money(cash)}"
               f" + 贷款 {fmt_money(loan_cap)}")
    pay = annuity_payment(loan_cap, rate, months)
    out.append(f"  月供 {fmt_money(pay)} 元（占收入 {pay/income*100:.1f}%，"
               f"含存量负债后 {(pay+args.debts)/income*100:.1f}%）")
    out.append("")
    # 瓶颈诊断与建议
    if bottleneck.startswith("月供"):
        out.append("【瓶颈诊断】卡在月供收入比——改善通道：")
        if args.years < 30:
            out.append(f"  · 延长年限：当前 {args.years} 年 → 30 年，同月供约多贷一档（用 --years 30 复测）")
        out.append(f"  · 降低利率：利率每降 0.3 个百分点，同月供约多贷 {fmt_money(loan_cap_dti*0.03)} 元")
        out.append(f"  · 增加共同借款人（合并收入）；或先清偿存量负债：每减 1,000 元月供，"
                   f"按本利率约多贷 {fmt_money(1000/pay_factor)} 元")
    else:
        out.append("【瓶颈诊断】卡在首付——改善通道：")
        out.append("  · 降总价（月供线尚有空间）或动用公积金余额/家庭互助凑首付")
        out.append(f"  · 首付比例已按下限 {down_min*100:g}%；再往上提贷款成数监管不允许")
    if args.first == 2:
        out.append("  · 二套首付高：若首套已卖/贷款结清，部分城市可按首套认定——用⑦-6认定器核对")
    out.append("-" * W)
    out.append("口径说明：银行审贷按等额本息、认夫妻双方征信负债；本测算不含税费。")
    print("\n".join(out))

    # ── 来源追溯 ──
    print()
    print("参数来源（规则版本可追溯）：")
    keys = list(dict.fromkeys(["dti", "min_down_first", "min_down_second", "commercial_rate"] + sorted(overrides.keys())))
    print(fmt_provenance(srcmap, keys))


if __name__ == "__main__":
    main()
