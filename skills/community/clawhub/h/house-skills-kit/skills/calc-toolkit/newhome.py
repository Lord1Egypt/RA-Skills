#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具06 · 一手房（新房）交易成本测算器（按功能分类：税费/登记工本/物业配套/金融/参考项）
清单序号：⑦-6｜规则来源：tools/rules/cities.yaml::newhome（三层引擎 + 层4 --set）
功能分类（老何 08-30 指示+澄清：第二类是办理不动产登记时官方收取的规费）：
  【一、税费】契税
  【二、不动产登记/工本费】登记费、证书工本费（官方规费）
  【三、物业与配套】维修基金、首年物业预存、燃气初装
  【四、金融相关（贷款时）】评估费、抵押登记
  【五、参考项】装修、车位（不计必缴）

用法示例：
  python3 newhome.py --price 1500000 --area 100 --city 昆明 --first 1
  python3 newhome.py --price 2600000 --area 128 --city 武汉 --first 2 --loan 1500000 --months 6
  python3 newhome.py --price 1500000 --area 100 --set agent_service=0 --set mortgage_service_rate=0
参数说明：
  --price 网签/合同价（元）  --area 建筑面积（㎡）  --first 1/2/3  --loan 贷款额（元）
  --months 交房预存物业费月数  --decor 装修预算（元，参考）  --parking 车位价（元，参考）
"""
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ruleengine import get_rules, fmt_provenance, COMPLIANCE  # noqa: E402

W = lambda x: f"{x:,.0f}"


def _num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def main():
    ap = argparse.ArgumentParser(description="一手房交易成本测算器（⑦-6）")
    ap.add_argument("--price", type=float, required=True, help="网签/合同价（元）")
    ap.add_argument("--area", type=float, required=True, help="建筑面积（㎡）")
    ap.add_argument("--first", type=int, default=1, choices=[1, 2, 3])
    ap.add_argument("--loan", type=float, default=0, help="贷款额（元，>0 计金融类费用）")
    ap.add_argument("--months", type=float, default=None, help="交房预存物业费月数（覆盖规则库）")
    ap.add_argument("--decor", type=float, default=0, help="装修预算（元，参考项）")
    ap.add_argument("--parking", type=float, default=0, help="车位价（元，参考项）")
    ap.add_argument("--extra-certs", type=int, default=0, dest="extra_certs",
                    help="加发不动产权证书本数（共有/车位加证，每本工本费读规则库）")
    ap.add_argument("--ptype", choices=["elevator", "walkup", "nonres"], default="elevator",
                    help="物业类型：elevator=高层带电梯(默认) walkup=多层不带电梯 nonres=非住宅，"
                         "维修基金按类型取城市档")
    ap.add_argument("--city"); ap.add_argument("--district")
    ap.add_argument("--template")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="即时覆盖任意规则参数，如 --set repair_fund_per_area=90")
    args = ap.parse_args()

    overrides = {}
    for kv in getattr(args, "set"):
        if "=" not in kv:
            ap.error(f"--set 需要 KEY=VALUE 格式：{kv}")
        k, v = kv.split("=", 1)
        overrides[k.strip()] = _num(v.strip())

    rules, prov = get_rules("newhome", args.city, args.district, args.template, overrides=overrides)
    tax_rules, _ = get_rules("tax", args.city, args.district, args.template, overrides=overrides)
    P, A = args.price, args.area
    month = args.months if args.months is not None else rules.get("prepaid_months", 12)

    lines = [f"＝ 一手房交易成本试算 ｜ 合同价 {W(P)} 元 ｜ {A:g}㎡ ｜"
             f" {'首套' if args.first==1 else '二套' if args.first==2 else '三套及以上'}"
             f"{' ｜ 城市:'+args.city if args.city else ' ｜ 全国默认档'}"
             f"{'/'+args.district if args.district else ''}", "─"*56]

    # 每类: (类名, [(名称, 金额, 说明), ...])
    groups = []

    # ═══【一、税费】═══
    deed = tax_rules["deed_tax"]
    if args.first == 1:
        rate = deed["first_140le"] if A <= 140 else deed["first_140gt"]
        basis = f"首套{'≤140㎡' if A <= 140 else '>140㎡'}"
    elif args.first == 2:
        rate = deed["second_140le"] if A <= 140 else deed["second_140gt"]
        basis = f"二套{'≤140㎡' if A <= 140 else '>140㎡'}"
    else:
        rate = deed["third_plus"]
        basis = "三套及以上"
    groups.append(("【一、税费】（一手房仅买方契税；无增值税/个税——卖方是开发商）", [
        (f"契税（{basis}，{rate*100:g}%）", P*rate, "与二手同档（140㎡线）"),
    ]))

    # ═══【二、不动产登记/工本费（官方规费）】═══
    # 老何 08-30 澄清：是办理不动产登记时官方收取的规费（登记费/工本费），不是代办服务费
    reg_items = []
    reg = rules.get("registration", 80)
    reg_items.append((f"不动产登记费（{reg:g} 元/套）", reg,
                      "住宅80元/套，非住宅550元/套；含首本《不动产权证书》"))
    n_certs = args.extra_certs
    if n_certs > 0:
        cf = rules.get("cert_fee_extra", 10)
        reg_items.append((f"证书工本费（加发 {n_certs} 本 × {cf:g} 元）", n_certs*cf,
                          "首本免费；共有/车位等加发每本10元"))
    groups.append(("【二、不动产登记/工本费】（办理不动产权证时官方收取）", reg_items))

    # ═══【三、物业与配套】═══
    prop_items = []
    # 维修基金：按物业类型查城市档（repair_fund_table），缺档回退 repair_fund_per_area
    table = rules.get("repair_fund_table") or {}
    key_map = {"walkup": "walkup", "nonres": "nonresidential", "elevator": "elevator"}
    rfa = table.get(key_map[args.ptype]) or rules.get("repair_fund_per_area", 110)
    ptype_cn = {"elevator": "高层/带电梯", "walkup": "多层/不带电梯", "nonres": "非住宅"}[args.ptype]
    if rules.get("repair_fund_mode") == "per_price":
        rf = P * rules.get("repair_fund_per_price", 0.0)
        rf_note = f"总价×{rules.get('repair_fund_per_price',0)*100:g}%"
    else:
        rf = A * rfa
        # 档位来源：城市段覆盖过类型表=城市档，否则默认档（看规则来源，不看表是否存在）
        tbl_src = (prov.get("repair_fund_table") or {}).get("source", "全国默认档")
        src_tag = f"城市档[{tbl_src}]" if tbl_src != "全国默认档" else "默认档"
        rf_note = f"{ptype_cn} {rfa:g} 元/㎡·{src_tag}"
    prop_items.append((f"住宅专项维修基金（{rf_note}，交房前缴存）", rf, "一次性缴，入专项账户"))
    pf = rules.get("property_fee", 2.5)
    prop_items.append((f"物业费预存（{pf:g} 元/㎡/月 × {month:g} 个月）", A*pf*month,
                       "多数项目交房预存3-12个月"))
    gas = rules.get("gas_install", 0)
    if gas:
        prop_items.append(("燃气初装/开户费", gas, "已含在房价的城市为0"))
    groups.append(("【三、物业与配套】（交房环节）", prop_items))

    # ═══【四、金融相关】═══
    if args.loan > 0:
        fin_items = []
        appr = rules.get("appraisal_rate", 0.001)
        fin_items.append((f"贷款评估费（贷款额×{appr*100:g}%）", args.loan*appr, "商业贷款需评估"))
        mreg = rules.get("mortgage_reg", 80)
        fin_items.append((f"抵押登记费（{mreg:g} 元/套）", mreg, "按揭登记"))
        groups.append(("【四、金融相关】（按揭产生）", fin_items))

    # ═══【五、参考项】═══
    ref_items = []
    if args.decor:
        ref_items.append(("装修预算（参考）", args.decor, "按需"))
    if args.parking:
        ref_items.append(("车位（参考，产权另计）", args.parking, "按需"))
    if ref_items:
        groups.append(("【五、参考项】（不计入必缴合计）", ref_items))

    # ═══ 分类输出 ═══
    subtotal = 0.0
    ref_total = 0.0
    for title, items in groups:
        is_ref = title.startswith("【五")
        lines.append(title)
        for name, v, note in items:
            lines.append(f"  · {name}：{W(v)} 元 ｜ {note}")
        sub = sum(v for _, v, _ in items)
        if is_ref:
            ref_total = sub
        else:
            subtotal += sub
        lines.append("")

    lines.append("─" * 56)
    lines.append(f"  ★ 必缴合计（一~四类）≈ {W(subtotal)} 元（占房价 {subtotal/P*100:.2f}%）")
    if ref_total:
        lines.append(f"  含参考项 ≈ {W(subtotal + ref_total)} 元")
    lines.append("  各项均可 --set 覆盖或城市段覆盖；以购房合同、交房公示与登记机构收费依据为准。")

    lines.append("")
    keys = ["repair_fund_table", "repair_fund_mode", "property_fee", "gas_install",
            "registration", "cert_fee_extra"] + sorted(overrides.keys())
    lines.append(fmt_provenance(prov, [k for k in keys if k in prov]))
    lines.append(COMPLIANCE)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
