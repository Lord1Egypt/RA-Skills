#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具17 · 佣金/提成试算器（二手中介费 / 新房渠道分销 / 团队分佣 / 返佣）

用法:
  # 二手中介费：买卖分账 + 活动折扣
  python3 commission.py --scene lease --rent 3500 --months 1 --landlord-share 0.5
  python3 commission.py --scene resale --price 1200000
  python3 commission.py --scene resale --price 1200000 --discount 0.7

  # 新房渠道：阶梯点位双算法对账（全额跳档 vs 分段累进并排对比）
  python3 commission.py --scene channel --amount 2500000 \
      --tiers '1000000:0.025;3000000:0.03;999999999:0.035' --bonus-rate 0.005

  # 一条龙：佣金 → 客户返佣 → 团队分佣
  python3 commission.py --scene channel --amount 2500000 --rate 0.03 \
      --rebate 0.3 --splits 0.35,0.15

口径（2026-08 查证）:
  · 二手中介费：昆明买方2%/卖方1%（昆明市中介行业收费标准2019；知乎行情2024）；
    北京链家2023-09起2%买卖各半（新京报）；行业带看区间2%-2.7%
  · 新房渠道点位：常见2%-3%（左晖2019口径；新浪2020行业稿）；难卖盘5%-8%
    （太原经纬2021；虎嗅2025）；台山2025限佣令8%-10%
  · 经纪人提成：占佣金25%-40%（太原二手房0.5%-0.8%/1%口径推算）
  · 阶梯双算法：全额跳档=总额落档统一费率；分段累进=各区间分别计费。
    两算法差异是渠道对账常见分歧点，本工具并排输出
输出: 佣金明细 → 阶梯双算法对比 → 返佣 → 团队分佣表 → 合规提示
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance  # noqa: E402


def fmt_money(x: float) -> str:
    return f"{x:,.0f}"


def _num(s):
    """--set 值解析：int → float → str"""
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def parse_tiers(tiers_str: str):
    """'1000000:0.025;3000000:0.03;999999999:0.035' → [(上限,费率),...] 升序"""
    tiers = []
    for seg in tiers_str.split(";"):
        lo_hi, rate = seg.split(":")
        tiers.append((float(lo_hi), float(rate)))
    return sorted(tiers)


def commission_whole(amount: float, tiers):
    """全额跳档：总额落哪档，全额按该档费率"""
    for cap, rate in tiers:
        if amount <= cap:
            return amount * rate, rate
    return amount * tiers[-1][1], tiers[-1][1]


def commission_progressive(amount: float, tiers):
    """分段累进：各区间分别按各自费率计费"""
    total, prev = 0.0, 0.0
    for cap, rate in tiers:
        if amount > prev:
            total += (min(amount, cap) - prev) * rate
            prev = cap
        else:
            break
    return total, None


def main() -> None:
    ap = argparse.ArgumentParser(description="佣金/提成试算（二手中介费/渠道分销/租赁佣金/团队分佣）")
    ap.add_argument("--scene", default="resale", choices=["resale", "channel", "lease"],
                    help="resale=二手中介费 / channel=新房渠道分销 / lease=租赁佣金（默认 resale）")
    ap.add_argument("--price", type=float, default=None, help="单套成交总价（元，resale用）")
    ap.add_argument("--amount", type=float, default=None, help="签约总额（元，channel用；resale多套合计也可用）")
    ap.add_argument("--buyer-rate", type=float, default=None,
                    help="二手买方费率，用小数（0.02 = 2%%，默认规则库）")
    ap.add_argument("--seller-rate", type=float, default=None,
                    help="二手卖方费率，用小数（0.01 = 1%%，默认规则库）")
    ap.add_argument("--rate", type=float, default=None, help="渠道固定点位（如 0.03）")
    ap.add_argument("--tiers", default=None,
                    help="渠道阶梯点位 '金额上限:费率;...'（与--rate二选一；给阶梯则双算法并排）")
    ap.add_argument("--bonus-rate", type=float, default=0, help="渠道加点激励（如 0.005=+0.5%%）")
    ap.add_argument("--discount", type=float, default=None, help="二手中介费活动折扣（如 0.7=7折）")
    ap.add_argument("--rebate", type=float, default=None, help="客户返佣比例（从佣金中返，如 0.3=返30%%）")
    ap.add_argument("--splits", default=None,
                    help="团队分佣比例，逗号分隔（如 '0.35,0.15'=经纪人35%%,店长15%%,公司余量50%%）")
    ap.add_argument("--rent", type=float, default=None, help="月租金（元，lease用）")
    ap.add_argument("--months", type=float, default=1.0, help="佣金按几个月租金计（lease用，默认 1）")
    ap.add_argument("--landlord-share", type=float, default=None,
                    help="房东承担的佣金比例，用小数（0.5 = 一半，默认规则库；与 --tenant-share 互补）")
    ap.add_argument("--tenant-share", type=float, default=None,
                    help="租客承担的佣金比例，用小数（0.5 = 一半）；两者只给一个，另一个自动补足")
    ap.add_argument("--city", default=None, help="城市（规则库城市档）")
    ap.add_argument("--template", default=None, help="我的模板名")
    ap.add_argument("--set", action="append", default=[], dest="overrides",
                    help="临时覆盖规则参数 k=v，可多次")
    args = ap.parse_args()

    overrides = {}
    for kv in args.overrides:
        if "=" not in kv:
            ap.error(f"--set 需 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, srcmap = get_rules("commission", city=args.city, district=None,
                              user_template=args.template, overrides=overrides)

    if args.scene == "lease":
        base = args.rent
    else:
        base = args.price if args.scene == "resale" else args.amount
    if base is None:
        need = {"resale": "--price", "channel": "--amount", "lease": "--rent"}[args.scene]
        ap.error(f"--scene {args.scene} 需要 {need}")

    W = 52
    print("=" * W)
    print("佣金/提成试算器")
    print("=" * W)
    scene_name = {"resale": "二手中介费", "channel": "新房渠道分销", "lease": "租赁佣金"}[args.scene]
    print(f"场景: {scene_name}"
          + (f" ｜ 城市: {args.city}" if args.city else ""))

    # ---- 段1：佣金计算 ----
    if args.scene == "lease":
        months = args.months if args.months is not None else 1.0
        if months <= 0 or months > 3:
            ap.error(f"--months 需在 0~3 之间（常见 0.5 / 1 / 1.5），收到 {months:g}")
        landlord = args.landlord_share
        tenant = args.tenant_share
        if landlord is None and tenant is None:
            landlord = float(rules.get("lease_landlord_share", 0.5))
            tenant = 1.0 - landlord
        elif landlord is None:
            landlord = 1.0 - tenant
        elif tenant is None:
            tenant = 1.0 - landlord
        for label, val in (("--landlord-share", landlord), ("--tenant-share", tenant)):
            if val > 1.0 or val < 0:
                ap.error(f"{label} 需为小数且在 0~1 之间（0.5 = 一半，1 = 全部由该方承担），收到 {val:g}")
        # 分摊比例本身就是 0~1 的真值（1 表示全部由一方承担），不做百分数换算，故不设单位告警
        commission = base * months
        print(f"月租金: {fmt_money(base)} 元 ｜ 佣金月数: {months:g} 个月")
        print("-" * W)
        print(f"  佣金合计（{months:g} 个月租金）      {fmt_money(commission):>14} 元")
        print(f"  {'─'*40}")
        print(f"  房东承担  {landlord*100:g}% → {fmt_money(commission*landlord):>14} 元")
        print(f"  租客承担  {tenant*100:g}% → {fmt_money(commission*tenant):>14} 元")
        print(f"  {'─'*40}")
        print(f"  折算：相当于 {(commission/base):.2f} 个月租金；占年租金 {(commission/(base*12))*100:.1f}%")
        if months > 1:
            print("  ⚠️ 佣金超过 1 个月租金时，租客实际首付=押金+首期租金+佣金，报价前先说清")
        calc_note = f"租赁佣金 = 月租 {fmt_money(base)} 元 × {months:g} 个月；分摊 房东{landlord*100:g}% / 租客{tenant*100:g}%"
    elif args.scene == "resale":
        buyer_rate = args.buyer_rate if args.buyer_rate is not None else float(rules.get("resale_buyer_rate", 0.02))
        seller_rate = args.seller_rate if args.seller_rate is not None else float(rules.get("resale_seller_rate", 0.01))
        # 单位防呆：本工具费率用小数，其它计算器多用百分数，混用会差 100 倍
        for label, val in (("--buyer-rate", buyer_rate), ("--seller-rate", seller_rate)):
            if val > 0.2:
                print(f"⚠️ 单位提醒：{label} {val:g} 被当作小数处理 → {val*100:g}%。"
                      f"若你本意是 {val:g}%，请改写成 {val/100:g}", file=sys.stderr)
        disc = args.discount if args.discount is not None else 1.0
        b = base * buyer_rate * disc
        s = base * seller_rate * disc
        disc_label = f"{disc*10:g}折" if disc != 1.0 else "无折扣"
        print(f"成交价: {fmt_money(base)} 元 ｜ 折扣: {disc_label}")
        print("-" * W)
        print(f"  买方承担  {buyer_rate*100:g}% → {fmt_money(b):>14} 元")
        print(f"  卖方承担  {seller_rate*100:g}% → {fmt_money(s):>14} 元")
        commission = b + s
        print(f"  {'─'*40}")
        print(f"  中介费合计（{disc_label}）          {fmt_money(commission):>14} 元"
              f"（占成交价 {(commission/base)*100:.2f}%）")
        calc_note = f"{buyer_rate*100:g}%+{seller_rate*100:g}%" + (f"×{disc*10:g}折" if disc != 1.0 else "")
    else:
        print(f"签约总额: {fmt_money(base)} 元")
        print("-" * W)
        if args.tiers:
            tiers = parse_tiers(args.tiers)
            w_amt, w_rate = commission_whole(base, tiers)
            p_amt, _ = commission_progressive(base, tiers)
            w_amt += base * args.bonus_rate
            p_amt += base * args.bonus_rate
            print(f"  阶梯: " + "；".join(f"≤{fmt_money(c)}元按{r*100:g}%" for c, r in tiers))
            if args.bonus_rate:
                print(f"  加点激励: +{args.bonus_rate*100:g}%")
            print(f"  {'─'*40}")
            print(f"  ① 全额跳档（落档{w_rate*100:g}%全额计） {fmt_money(w_amt):>12} 元")
            print(f"  ② 分段累进（各区间分别计）   {fmt_money(p_amt):>12} 元")
            print(f"  {'─'*40}")
            if abs(w_amt - p_amt) > 0.5:
                print(f"  ⚠️ 两算法差 {fmt_money(abs(w_amt-p_amt))} 元——结佣前务必与合同约定口径核对！")
            commission = w_amt  # 展示用取全额跳档；对账以合同为准
            calc_note = "阶梯双算法（差异已标注）"
        else:
            rate = args.rate if args.rate is not None else float(rules.get("channel_rate", 0.03))
            commission = base * (rate + args.bonus_rate)
            note = f"{rate*100:g}%" + (f"+{args.bonus_rate*100:g}%激励" if args.bonus_rate else "")
            print(f"  固定点位 {note}          {fmt_money(commission):>14} 元")
            calc_note = note

    # ---- 段2：返佣 ----
    if args.rebate:
        rebate_amt = commission * args.rebate
        print(f"  {'─'*40}")
        print(f"  客户返佣 {args.rebate*100:g}%          -{fmt_money(rebate_amt):>13} 元"
              f"（净佣金 {fmt_money(commission-rebate_amt)} 元）")

    # ---- 段3：团队分佣 ----
    if args.splits:
        shares = [float(x) for x in args.splits.split(",") if x.strip()]
        total_share = sum(shares)
        if total_share > 1:
            print(f"  ❌ 分佣比例合计 {total_share*100:g}% > 100%")
            return
        roles = ["经纪人", "店长", "公司", "其他"] + [f"角色{i}" for i in range(4, len(shares))]
        print(f"  {'─'*40}")
        print(f"  团队分佣（佣金池 {fmt_money(commission)} 元）:")
        pool = commission
        for i, sh in enumerate(shares):
            print(f"    {roles[i]:<4} {sh*100:g}% → {fmt_money(commission*sh):>12} 元")
            pool -= commission * sh
        print(f"    公司留存 {fmt_money(pool):>16} 元（{(pool/commission)*100:g}%）" if pool > 0.5 else "")
    elif args.scene == "channel" or args.splits is None:
        agent_share = float(rules.get("agent_share", 0.35))
        print(f"  {'─'*40}")
        print(f"  参考分佣: 经纪人{agent_share*100:g}% ≈ {fmt_money(commission*agent_share)} 元"
              f" ｜ 公司留存 ≈ {fmt_money(commission*(1-agent_share))} 元"
              f"（--splits 自定义分层）")

    print("-" * W)
    print(f"计算口径: {calc_note}")
    keys = [k for k in ("resale_buyer_rate", "resale_seller_rate", "channel_rate",
                        "lease_landlord_share", "agent_share") if k in rules]
    print("口径出处:")
    print(fmt_provenance(srcmap, keys))
    print("提醒: 佣金以居间/分销合同约定为准；客户保护期内成交才结佣（行业惯例）；")
    print("      返佣以项目书面政策为准；《规范房地产经纪服务的意见》(2023-05)要求双方共担合理费率。")


if __name__ == "__main__":
    main()
