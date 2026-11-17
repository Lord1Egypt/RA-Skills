#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具16 · 公积金贷款额度测算器（四限取最低：上限封顶/房价成数/还贷能力/余额倍数）

用法:
  python3 fund.py --city 昆明 --family couple --balances 80000,60000 \
      --months 40 --base 9000,7000 --price 1200000 --first 1 --years 30
  python3 fund.py --city 昆明 --family single --balances 50000 --months 20 \
      --base 8000 --boost multi_child --set base_cap_single=700000

口径（2026-08 查证）:
  · 四限取最低 = 全国通行框架（昆明《个人住房贷款实施细则》2024-12-02 施行第十条；
    武汉公积金中心官网公式 FAQ 2026-05-26；深圳住建局 FAQ 2026-04-30）
  · 昆明上限：单缴存人 70 万 / 双缴存人 100 万（2026-04-07 起执行，有效期 1 年，
    昆明市公积金中心《关于优化调整住房公积金个人住房贷款政策的通知》）
  · 昆明上浮：多子女+30%；现房/绿建+20%（可叠加至+50%）；高层次人才+50%
  · 缴存时间系数 / 还贷能力系数：城市差异大，规则库存梯度演示值，--set 可覆盖，
    最终以各中心审核为准
输出: 四限分项 → 取最低 → 向下取整到 1000 元（昆明细则口径）→ 组合贷缺口提示
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance  # noqa: E402


def annuity_payment(principal: float, annual_rate: float, months: int) -> float:
    """等额本息月供"""
    if principal <= 0 or months <= 0:
        return 0.0
    r = annual_rate / 12
    if r == 0:
        return principal / months
    return principal * r / (1 - (1 + r) ** (-months))


def fmt_money(x: float) -> str:
    return f"{x:,.0f}"


def months_coefficient(months: int, table_str: str) -> float:
    """缴存时间系数：表格式 '6:12:0.5;12:24:0.8;24:36:1.0;36:60:1.2;60:99999:1.5'
    每段 = 下限(含):上限(不含):系数；不足最低档 → 0（不满足申贷缴存时长）"""
    for seg in table_str.split(";"):
        lo, hi, coef = seg.split(":")
        if int(lo) <= months < int(hi):
            return float(coef)
    return 0.0


def main() -> None:
    ap = argparse.ArgumentParser(description="公积金贷款额度测算（四限取最低）")
    ap.add_argument("--city", default=None, help="城市（规则库内置城市档）")
    ap.add_argument("--district", default=None, help="区/县（城市内二级覆盖）")
    ap.add_argument("--family", default="couple", choices=["single", "couple"],
                    help="single=单缴存人家庭 / couple=双缴存人家庭（默认 couple）")
    ap.add_argument("--balances", required=True,
                    help="公积金账户余额，逗号分隔：本人 或 本人,配偶")
    ap.add_argument("--months", type=int, required=True, help="本人连续缴存月数")
    ap.add_argument("--spouse-months", type=int, default=None, help="配偶连续缴存月数")
    ap.add_argument("--base", default=None,
                    help="缴存基数（月），逗号分隔：本人 或 本人,配偶；未提供则需 --price 由还贷能力反推场景可缺省")
    ap.add_argument("--price", type=float, default=None, help="房屋总价（元）")
    ap.add_argument("--first", type=int, default=1, choices=[1, 2], help="1=首套 2=二套")
    ap.add_argument("--years", type=int, default=30, help="贷款年限（默认30）")
    ap.add_argument("--debts", type=float, default=0, help="现有贷款月供合计（元/月）")
    ap.add_argument("--rate", type=float, default=None,
                    help="公积金利率（默认取规则库 provident_rate）")
    ap.add_argument("--boost", default=None,
                    help="额度上浮标签，逗号组合：multi_child(多子女) / green(现房或绿建) / elite(高层次人才)")
    ap.add_argument("--template", default=None, help="我的模板名（用户自定义规则）")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="临时覆盖规则参数 k=v，可多次（如 --set balance_multiple=16）")
    args = ap.parse_args()

    # --set 列表 → dict（对齐 capacity 约定：int → float → str）
    def _num(s):
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

    rules, srcmap = get_rules("fund", city=args.city, district=args.district,
                              user_template=args.template, overrides=overrides)

    # ---- 解析家庭输入 ----
    bal = [float(x) for x in str(args.balances).replace("，", ",").split(",") if x.strip()]
    if args.family == "single":
        bal = bal[:1]
    total_balance = sum(bal)
    bases = []
    if args.base:
        bases = [float(x) for x in str(args.base).replace("，", ",").split(",") if x.strip()]
        if args.family == "single":
            bases = bases[:1]
    total_base = sum(bases) if bases else None

    first = args.first
    years = min(args.years, int(rules.get("max_years", 30)))
    months = years * 12
    rate = args.rate if args.rate is not None else float(
        rules.get("provident_rate", 0.025))

    # ---- ① 上限封顶 ----
    cap_single = float(rules.get("base_cap_single", 600000))
    cap_couple = float(rules.get("base_cap_couple", 1000000))
    base_cap = cap_single if args.family == "single" else cap_couple

    boost_total = 0.0
    boost_notes = []
    if args.boost:
        for tag in [t.strip() for t in args.boost.split(",") if t.strip()]:
            v = rules.get(f"boost_{tag}")
            if v is None:
                print(f"⚠️ 未知上浮标签 {tag}（可用: multi_child/green/elite），已忽略")
                continue
            boost_total += float(v)
            boost_notes.append(f"{tag}+{float(v)*100:g}%")
    max_cap = base_cap * (1 + boost_total)
    if boost_total > 0:
        max_cap = min(max_cap, base_cap * (1 + float(rules.get("boost_cap", boost_total))))

    # ---- ② 房价成数 ----
    down_min = float(rules.get("downpay_min_first", 0.2) if first == 1
                     else rules.get("downpay_min_second", 0.3))
    price_cap = None
    if args.price:
        price_cap = args.price * (1 - down_min)

    # ---- ③ 还贷能力 ----
    repay_coef = float(rules.get("repay_coef", 0.40))
    income_cap = None
    monthly_payment_cap = None
    if total_base is not None:
        monthly_payment_cap = total_base * repay_coef - args.debts
        if monthly_payment_cap <= 0:
            monthly_payment_cap = 0.0
            income_cap = 0.0
        else:
            income_cap = monthly_payment_cap * 12 * years

    # ---- ④ 余额倍数 × 缴存时间系数 ----
    multiple = float(rules.get("balance_multiple", 20))
    table_str = str(rules.get("months_coef_table",
                              "6:12:0.5;12:24:0.8;24:36:1.0;36:60:1.2;60:99999:1.5"))
    coef_main = months_coefficient(args.months, table_str)
    coef_spouse = None
    if args.family == "couple" and args.spouse_months is not None:
        coef_spouse = months_coefficient(args.spouse_months, table_str)
        balance_cap = total_balance * multiple * min(coef_main, coef_spouse)
    else:
        balance_cap = total_balance * multiple * coef_main

    # ---- 四限取最低 → 取整到千元 ----
    limits = [("① 上限封顶", max_cap)]
    if price_cap is not None:
        limits.append((f"② 房价成数（首付≥{down_min*100:g}%）", price_cap))
    if income_cap is not None:
        limits.append((f"③ 还贷能力（系数{repay_coef*100:g}%）", income_cap))
    limits.append((f"④ 余额倍数（{multiple:g}倍×时间系数{coef_main:g}"
                   + (f"/{coef_spouse:g}" if coef_spouse is not None else "") + "）",
                   balance_cap))

    final = min(v for _, v in limits)
    final_floored = int(final // 1000 * 1000)
    eligible = coef_main > 0 and (coef_spouse is None or coef_spouse > 0)

    # ---- 输出 ----
    W = 46
    print("=" * W)
    print("公积金贷款额度测算（四限取最低）")
    print("=" * W)
    city_label = args.city or "全国通用档"
    print(f"城市: {city_label} ｜ 家庭: {'单' if args.family=='single' else '双'}缴存人"
          f" ｜ {'首套' if first==1 else '二套'} ｜ {years}年 ｜ 利率 {rate*100:.2f}%")
    print(f"账户余额: {fmt_money(total_balance)} 元"
          + (f" ｜ 缴存基数: {fmt_money(total_base)} 元/月" if total_base else ""))
    if boost_notes:
        print(f"上浮: {', '.join(boost_notes)} → 上限上浮 {boost_total*100:g}%")
    print("-" * W)
    for name, v in limits:
        print(f"{name:<28} {fmt_money(v):>14} 元")
    print("-" * W)
    if not eligible:
        print("❌ 缴存月数不足最低档（默认满6个月方可申贷），可贷额度按 0 计。")
        print("   （梯度表可用 --set months_coef_table='...' 覆盖）")
        return
    print(f"★ 测算可贷额度 ≈ {fmt_money(final_floored)} 元"
          f"（按 {city_label} 口径向下取整至千元）")
    # 瓶颈提示
    bottleneck = min(limits, key=lambda kv: kv[1])[0]
    print(f"   瓶颈：{bottleneck}")
    if final_floored <= 0:
        print("   提示：可贷额度为 0，请核对缴存状态/余额/基数输入。")
    if args.price and final_floored < args.price * (1 - down_min):
        gap = args.price * (1 - down_min) - final_floored
        print(f"   组合贷缺口 ≈ {fmt_money(gap)} 元"
              f"（可申请商贷补足；月供测算用 mortgage.py）")
    print(f"   参考：该额度 {years}年等额本息月供 ≈ "
          f"{fmt_money(annuity_payment(final_floored, rate, months))} 元/月")
    print("-" * W)
    print("口径出处:")
    keys = [k for k in ("base_cap_single", "base_cap_couple", "balance_multiple",
                        "months_coef_table", "repay_coef", "provident_rate") if k in rules]
    print(fmt_provenance(srcmap, keys))
    print("提醒: 各地缴存时间系数/还贷系数/上限动态调整，最终以公积金中心审核为准。")


if __name__ == "__main__":
    main()
