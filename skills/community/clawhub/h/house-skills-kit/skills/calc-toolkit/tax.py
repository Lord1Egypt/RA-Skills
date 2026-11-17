#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具02 · 二手房交易全成本测算器（税 4 项 + 费 6+ 项，买/卖分账）
清单序号：⑦-2｜规则来源：tools/rules/cities.yaml（三层引擎 + 层4 即时覆盖）
税：契税/增值税及附加/个税/印花税（住宅免征展示）｜费：中介/交易手续费/登记/评估/担保赎楼/土地收益金

用法示例：
  python3 tax.py --price 1500000 --area 89 --city 昆明 --first 1 --held 6 --unique 1
  python3 tax.py --price 2000000 --area 120 --city 武汉 --first 2 --held 1 --loan 1000000 --agent 1.5
  python3 tax.py --price 800000 --area 70 --city 昆明 --housing-reform 1        # 房改房
核心铁律（老何 08-30 指示）：
  真实交易不止税——各类费用尽量完整列出，使用者可以不填（不填=0 或默认档），
  但测算器必须包括；且所有测算目标/税费标准/城市/地域均可自行调整修改（--set 任意覆盖）。
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance, COMPLIANCE  # noqa: E402

W = lambda x: f"{x:,.0f}"


def _num(s):
    """--set 值解析：int → float → str"""
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def main():
    ap = argparse.ArgumentParser(description="二手房交易全成本测算器（⑦-2）")
    ap.add_argument("--price", type=float, required=True, help="网签/成交价（元）")
    ap.add_argument("--area", type=float, required=True, help="建筑面积（㎡）")
    ap.add_argument("--first", type=int, default=1, choices=[1, 2, 3], help="1=首套 2=二套 3=三套及以上")
    ap.add_argument("--held", type=float, default=0, help="卖方持有年限（≥2满二免增值税，≥5且唯一免个税）")
    ap.add_argument("--unique", type=int, default=0, help="1=卖方家庭唯一住房")
    ap.add_argument("--orig", type=float, default=0, help="卖方原值（元，选填：个税差额对比）")
    ap.add_argument("--loan", type=float, default=0, help="买方贷款额（元，>0 时计评估费+抵押登记费）")
    ap.add_argument("--redeem", type=float, default=0, help="卖方未结清贷款余额（元，>0 时计赎楼担保费）")
    ap.add_argument("--agent", type=float, default=None, help="中介费率%%（如 1.5=1.5%%；不填用城市/默认档）")
    ap.add_argument("--housing-reform", type=int, default=0, help="1=房改房/经适房（计土地收益金）")
    ap.add_argument("--city"); ap.add_argument("--district")
    ap.add_argument("--template")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="即时覆盖任意规则参数，如 --set agent_rate=0.015 --set registration=40（可多次）")
    args = ap.parse_args()

    overrides = {}
    for kv in getattr(args, "set"):
        if "=" not in kv:
            ap.error(f"--set 需要 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, prov = get_rules("tax", args.city, args.district, args.template, overrides=overrides)
    P, A = args.price, args.area
    fees = rules.get("fees", {})
    lines = [f"＝ 二手房交易全成本试算 ｜ 成交价 {W(P)} 元 ｜ {A:g}㎡ ｜"
             f" {'首套' if args.first==1 else '二套' if args.first==2 else '三套及以上'}"
             f" ｜ 满{'五' if args.held>=5 else '二' if args.held>=2 else '未满二'}"
             f"{'·家庭唯一' if args.unique else ''}"
             f"{' ｜ 城市:'+args.city if args.city else ' ｜ 全国默认档'}"
             f"{'/'+args.district if args.district else ''}", "─"*56]

    tax_items = []    # (名称, 金额, 买方额, 卖方额)
    fee_items = []

    # ═══ 一、税费 ═══
    # 契税（买方）2024年16号公告：140㎡线
    deed = rules["deed_tax"]
    if args.first == 1:
        rate = deed["first_140le"] if A <= 140 else deed["first_140gt"]
        basis = f"首套{'≤140㎡' if A <= 140 else '>140㎡'}"
    elif args.first == 2:
        rate = deed["second_140le"] if A <= 140 else deed["second_140gt"]
        basis = f"二套{'≤140㎡' if A <= 140 else '>140㎡'}"
    else:
        rate = deed["third_plus"]
        basis = "三套及以上"
    deed_tax = P * rate
    tax_items.append((f"契税（{basis}，{rate*100:g}%）", deed_tax, deed_tax, 0.0))

    # 增值税及附加（卖方）2025年17号公告：满2免，未满2 3%含税换算
    if args.held >= 2:
        vat, extra, vat_note = 0.0, 0.0, "满2年免征（全国统一，含北上广深）"
    else:
        vat_rate = rules["vat_rate"]
        vat_net = P / (1 + vat_rate) if rules.get("vat_price_in", 1) else P
        vat = vat_net * vat_rate
        extra = vat * rules.get("vat_extra_rate", 0.0)
        vat_note = "未满2年 3%征收率（含税换算）"
    tax_items.append((f"增值税（{vat_note}）", vat, 0.0, vat))
    if extra > 0:
        tax_items.append(("  ↳ 附加税费（增值税额×12%）", extra, 0.0, extra))

    # 个税（卖方）
    if args.held >= 5 and args.unique:
        indiv, indiv_note = 0.0, "满五唯一免征"
    else:
        it = rules["indiv_tax"]
        normal = P * it["normal"]
        if args.orig and P > args.orig:
            diff_tax = (P - args.orig) * 0.20
            indiv = min(normal, diff_tax)
            indiv_note = f"全额{it['normal']*100:g}%={W(normal)} 与 差额20%={W(diff_tax)} 取低"
        else:
            indiv = normal
            indiv_note = f"核定{it['normal']*100:g}%（未提供原值/未满五唯一）"
    tax_items.append((f"个税（{indiv_note}）", indiv, 0.0, indiv))

    # 印花税（住宅免征；非住宅按 stamp_tax）——列出仅为完整性，让使用者知道这项存在
    stamp = rules.get("stamp_tax", 0.0) * P
    if stamp > 0:
        tax_items.append(("印花税（双方各半）", stamp, stamp/2, stamp/2))
    else:
        tax_items.append(("印花税（住宅免征，0 元）", 0.0, 0.0, 0.0))

    # ═══ 二、交易费用（真实交易不止税）═══
    def fee_get(key, default):
        """读取费用参数：优先层4顶层覆盖值，否则 fees.key，否则 default"""
        if key in rules:          # --set 顶层覆盖优先
            return rules[key]
        return fees.get(key, default)

    # 中介费
    agent_rate = (args.agent / 100) if args.agent is not None else fee_get("agent_rate", 0.02)
    agent_fee = P * agent_rate
    split = fee_get("agent_split", "both")
    if split == "buyer":
        ab, asg = agent_fee, 0.0
        split_note = "买方承担"
    elif split == "seller":
        ab, asg = 0.0, agent_fee
        split_note = "卖方承担"
    else:
        ab, asg = agent_fee/2, agent_fee/2
        split_note = "双方各半（可谈）"
    fee_items.append((f"中介费（{agent_rate*100:g}%×成交价，{split_note}）", agent_fee, ab, asg))

    # 交易手续费（元/㎡，双方各半）
    tf_per = fee_get("transaction_fee", 6)
    tf = tf_per * A
    fee_items.append((f"交易手续费（{tf_per:g} 元/㎡，双方各半）", tf, tf/2, tf/2))

    # 登记费（买方）
    reg = fee_get("registration", 80)
    fee_items.append((f"不动产登记费（{reg:g} 元/套，买方）", reg, reg, 0.0))

    # 贷款相关（买方贷款时才产生）
    if args.loan > 0:
        appr = fee_get("appraisal_rate", 0.001)
        ap_fee = args.loan * appr
        fee_items.append((f"贷款评估费（贷款额×{appr*100:g}%，买方）", ap_fee, ap_fee, 0.0))
        mreg = fee_get("mortgage_reg", 80)
        fee_items.append((f"抵押登记费（{mreg:g} 元/套，买方）", mreg, mreg, 0.0))

    # 赎楼/担保费（卖方有未结清贷款时）
    if args.redeem > 0:
        g_rate = fee_get("guarantee_rate", 0.006)
        g_fee = args.redeem * g_rate
        fee_items.append((f"赎楼/担保费（未结清 {W(args.redeem)}×{g_rate*100:g}%，卖方）", g_fee, 0.0, g_fee))

    # 土地收益金（房改房/经适房）
    if args.housing_reform:
        lg_rate = fee_get("land_gain_rate", 0.02)
        lg = P * lg_rate
        fee_items.append((f"土地收益金（房改房，{lg_rate*100:g}%×成交价，卖方）", lg, 0.0, lg))

    # ═══ 汇总输出 ═══
    def dump(title, items):
        lines.append(title)
        sub = sum(v for _, v, _, _ in items)
        for name, v, _, _ in items:
            lines.append(f"  · {name}：{W(v)} 元")
        return sub

    tax_total = dump("【一、税费】", tax_items)
    fee_total = dump("【二、交易费用】", fee_items)
    buyer = sum(b for _, _, b, _ in tax_items + fee_items)
    seller = sum(s for _, _, _, s in tax_items + fee_items)
    lines.append("─" * 56)
    lines.append(f"  税费小计 ≈ {W(tax_total)} 元 ｜ 费用小计 ≈ {W(fee_total)} 元")
    lines.append(f"  ★ 交易全成本 ≈ {W(tax_total + fee_total)} 元（占房价 {(tax_total+fee_total)/P*100:.2f}%）")
    lines.append(f"  · 买方口径 {W(buyer)} 元 ｜ 卖方口径 {W(seller)} 元"
                 f"（实际承担以谈判为准，交易习惯多为买方包税）")

    lines.append("")
    lines.append(fmt_provenance(prov, ["deed_tax", "vat_rate", "indiv_tax", "fees"]
                                + sorted(overrides.keys())))
    lines.append("")
    lines.append("口诀提醒：满二免增值税（全国统一），满五唯一再免个税；首二套140㎡内契税均1%。")
    lines.append("没填的项按默认档/0处理——每一项都可 --set 覆盖（如 --set agent_rate=0.015）。")
    lines.append(COMPLIANCE)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
