#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
"""
诉讼费用计算器
依据：《诉讼费用交纳办法》（国务院令第481号）第十三条、第十四条

用法：
    python3 calc_litigation_fee.py --type property --amount 1500000
    python3 calc_litigation_fee.py --type divorce --property 250000
    python3 calc_litigation_fee.py --type enforcement --amount 800000
    python3 calc_litigation_fee.py --type preservation --amount 120000

支持的案件类型（--type 参数）：
    property            财产案件受理费
    divorce             离婚案件受理费
    personality         侵害人格权案件受理费
    other_non           其他非财产案件受理费
    ip_no_amount        知识产权案件（无争议金额）
    ip_with_amount      知识产权案件（有争议金额，同财产案件）
    labor               劳动争议案件受理费
    admin_ip            商标/专利/海事行政案件受理费
    admin_other         其他行政案件受理费
    jurisdiction        管辖权异议费
    enforcement         申请执行费（有金额）
    enforcement_no      申请执行费（无金额）
    preservation        申请保全措施费
    payment_order       申请支付令
    public_notice       申请公示催告
    arbitration_set_aside 申请撤销仲裁裁决/认定仲裁协议效力
    bankruptcy          破产案件申请费
    maritime_fund       海事赔偿责任限制基金
    maritime_injunction 海事强制令
    maritime_priority   船舶优先权催告
    maritime_claim      海事债权登记
    maritime_average    共同海损理算
"""

from decimal import Decimal, ROUND_HALF_UP
import argparse
import sys


def round2(value: Decimal) -> Decimal:
    """四舍五入到分（2位小数）"""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def decimal_arg(value: str) -> Decimal:
    """直接从字符串解析 Decimal，避免经由 float 引入精度噪音。"""
    try:
        return Decimal(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError(f"无效金额：{value}") from exc


def money_text(value: Decimal) -> str:
    return f"¥ {float(round2(value)):,.2f} 元"


# ─────────────────────────────────────────────
# 第十三条（一）：财产案件受理费（分段累计）
# ─────────────────────────────────────────────
PROPERTY_TIERS = [
    # (下限, 上限, 比例)  单位：元
    (Decimal("0"), Decimal("10000"), None),  # 固定50元
    (Decimal("10000"), Decimal("100000"), Decimal("0.025")),
    (Decimal("100000"), Decimal("200000"), Decimal("0.02")),
    (Decimal("200000"), Decimal("500000"), Decimal("0.015")),
    (Decimal("500000"), Decimal("1000000"), Decimal("0.01")),
    (Decimal("1000000"), Decimal("2000000"), Decimal("0.009")),
    (Decimal("2000000"), Decimal("5000000"), Decimal("0.008")),
    (Decimal("5000000"), Decimal("10000000"), Decimal("0.007")),
    (Decimal("10000000"), Decimal("20000000"), Decimal("0.006")),
    (Decimal("20000000"), None, Decimal("0.005")),
]


def calc_property_fee(amount: Decimal) -> Decimal:
    """
    计算财产案件受理费（分段累计）
    第十三条（一）
    """
    if amount <= 0:
        raise ValueError("诉讼金额必须大于 0")

    if amount <= Decimal("10000"):
        return Decimal("50")

    fee = Decimal("50")  # 第一段固定50元
    for low, high, rate in PROPERTY_TIERS[1:]:
        if amount <= low:
            break
        upper = min(amount, high) if high is not None else amount
        fee += (upper - low) * rate
        if high is None or amount <= high:
            break

    return round2(fee)


def build_property_breakdown(amount: Decimal) -> list[str]:
    """返回财产案件分段计算明细。"""
    if amount <= 0:
        raise ValueError("诉讼金额必须大于 0")

    lines = ["第十三条第（一）项：财产案件受理费（分段累计）"]
    if amount <= Decimal("10000"):
        lines.append(f"  不超过1万元：固定 50 元")
        return lines

    lines.append("  不超过1万元：固定 50 元")
    for low, high, rate in PROPERTY_TIERS[1:]:
        if amount <= low:
            break
        upper = min(amount, high) if high is not None else amount
        segment = upper - low
        segment_fee = round2(segment * rate)
        high_label = f"{int(high):,}" if high is not None else "以上"
        lines.append(
            f"  超过 {int(low):,} 元至 {high_label} 的部分：{int(segment):,} x {rate * 100}% = {float(segment_fee):,.2f} 元"
        )
        if high is None or amount <= high:
            break
    return lines


# ─────────────────────────────────────────────
# 第十三条（二）-1：离婚案件受理费
# ─────────────────────────────────────────────
def calc_divorce_fee(
        property_amount: Decimal = Decimal("0"),
        base_fee: Decimal = Decimal("50"),
) -> dict:
    """
    计算离婚案件受理费
    base_fee: 基础费，50~300元，默认取下限50元（具体由地方标准确定）
    property_amount: 涉及财产分割的财产总额（元）
    """
    extra = Decimal("0")
    if property_amount > Decimal("200000"):
        extra = round2((property_amount - Decimal("200000")) * Decimal("0.005"))

    total = base_fee + extra
    return {
        "base_fee": float(base_fee),
        "extra_fee": float(extra),
        "total": float(total),
        "note": "基础费50~300元，以当地法院标准为准。财产总额超过20万元部分按0.5%另行计算。",
    }


# ─────────────────────────────────────────────
# 第十三条（二）-2：侵害人格权案件受理费
# ─────────────────────────────────────────────
def calc_personality_fee(
        damages: Decimal = Decimal("0"),
        base_fee: Decimal = Decimal("100"),
) -> dict:
    """
    计算侵害人格权案件受理费
    base_fee: 基础费，100~500元，默认取下限100元
    damages: 损害赔偿金额（元）
    """
    extra = Decimal("0")
    if damages > Decimal("50000"):
        tier1 = min(damages, Decimal("100000")) - Decimal("50000")
        extra += round2(tier1 * Decimal("0.01"))
    if damages > Decimal("100000"):
        extra += round2((damages - Decimal("100000")) * Decimal("0.005"))

    total = base_fee + extra
    return {
        "base_fee": float(base_fee),
        "extra_fee": float(extra),
        "total": float(total),
        "note": "基础费100~500元，以当地法院标准为准。赔偿额超5万元部分按1%，超10万元部分按0.5%另行计算。",
    }


# ─────────────────────────────────────────────
# 第十四条（一）：申请执行费（分段累计）
# ─────────────────────────────────────────────
ENFORCEMENT_TIERS = [
    (Decimal("0"), Decimal("10000"), None),
    (Decimal("10000"), Decimal("500000"), Decimal("0.015")),
    (Decimal("500000"), Decimal("5000000"), Decimal("0.01")),
    (Decimal("5000000"), Decimal("10000000"), Decimal("0.005")),
    (Decimal("10000000"), None, Decimal("0.001")),
]


def calc_enforcement_fee(amount: Decimal) -> Decimal:
    """
    计算申请执行费（分段累计）
    第十四条（一）
    """
    if amount <= 0:
        raise ValueError("执行金额必须大于 0")

    if amount <= Decimal("10000"):
        return Decimal("50")

    fee = Decimal("50")
    for low, high, rate in ENFORCEMENT_TIERS[1:]:
        if amount <= low:
            break
        upper = min(amount, high) if high is not None else amount
        fee += (upper - low) * rate
        if high is None or amount <= high:
            break

    return round2(fee)


def build_enforcement_breakdown(amount: Decimal) -> list[str]:
    """返回申请执行费分段计算明细。"""
    if amount <= 0:
        raise ValueError("执行金额必须大于 0")

    lines = ["第十四条第（一）项：申请执行费（分段累计）"]
    if amount <= Decimal("10000"):
        lines.append("  不超过1万元：固定 50 元")
        return lines

    lines.append("  不超过1万元：固定 50 元")
    for low, high, rate in ENFORCEMENT_TIERS[1:]:
        if amount <= low:
            break
        upper = min(amount, high) if high is not None else amount
        segment = upper - low
        segment_fee = round2(segment * rate)
        high_label = f"{int(high):,}" if high is not None else "以上"
        lines.append(
            f"  超过 {int(low):,} 元至 {high_label} 的部分：{int(segment):,} x {rate * 100}% = {float(segment_fee):,.2f} 元"
        )
        if high is None or amount <= high:
            break
    return lines


# ─────────────────────────────────────────────
# 第十四条（二）：申请保全措施费
# ─────────────────────────────────────────────
def calc_preservation_fee(amount: Decimal) -> Decimal:
    """
    计算申请保全措施费
    第十四条（二），上限5000元
    """
    if amount <= Decimal("1000"):
        fee = Decimal("30")
    elif amount <= Decimal("100000"):
        fee = Decimal("30") + round2((amount - Decimal("1000")) * Decimal("0.01"))
    else:
        fee = Decimal("30") + round2((Decimal("100000") - Decimal("1000")) * Decimal("0.01"))
        fee += round2((amount - Decimal("100000")) * Decimal("0.005"))

    # 上限5000元
    return min(round2(fee), Decimal("5000"))


# ─────────────────────────────────────────────
# 第十四条（三）：申请支付令
# ─────────────────────────────────────────────
def calc_payment_order_fee(amount: Decimal) -> Decimal:
    """申请支付令：财产案件受理费的1/3"""
    base = calc_property_fee(amount)
    return round2(base / Decimal("3"))


# ─────────────────────────────────────────────
# 第十四条（六）：破产案件申请费
# ─────────────────────────────────────────────
def calc_bankruptcy_fee(total_assets: Decimal) -> Decimal:
    """
    破产案件申请费：财产案件受理费标准减半，最高30万元
    """
    base = calc_property_fee(total_assets)
    fee = round2(base / Decimal("2"))
    return min(fee, Decimal("300000"))


def fixed_fee_result(
        case_type: str,
        fee: Decimal,
        article: str,
        note: str | None = None,
        breakdown: list[str] | None = None,
) -> dict:
    result = {
        "case_type": case_type,
        "article": article,
        "total": round2(fee),
    }
    if note:
        result["note"] = note
    if breakdown:
        result["breakdown"] = breakdown
    return result


# ─────────────────────────────────────────────
# 统一输出格式
# ─────────────────────────────────────────────
def format_result(fee_info: dict) -> str:
    lines = [f"\n{'=' * 50}", f"  案件类型：{fee_info['case_type']}", f"{'=' * 50}", f"  法律依据：{fee_info['article']}"]

    for item in fee_info.get("breakdown", []):
        lines.append(f"  {item}")

    if "base_fee" in fee_info:
        lines.append(f"  基础费：{money_text(fee_info['base_fee'])}")
    if "extra_fee" in fee_info:
        lines.append(f"  额外费用：{money_text(fee_info['extra_fee'])}")

    lines.append(f"  【应缴费用合计】：{money_text(fee_info['total'])}")

    if "note" in fee_info:
        lines.append(f"  备注：{fee_info['note']}")

    lines.append("=" * 50)
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="诉讼费用计算器（依据《诉讼费用交纳办法》）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--type", "-t", required=True,
        choices=[
            "property", "divorce", "personality", "other_non",
            "ip_no_amount", "ip_with_amount", "labor",
            "admin_ip", "admin_other", "jurisdiction",
            "enforcement", "enforcement_no",
            "preservation", "payment_order", "public_notice",
            "arbitration_set_aside", "bankruptcy",
            "maritime_fund", "maritime_injunction",
            "maritime_priority", "maritime_claim", "maritime_average",
        ],
        help="案件类型",
    )
    parser.add_argument("--amount", "-a", type=decimal_arg, default=Decimal("0"),
                        help="诉讼/执行/保全金额（元）")
    parser.add_argument("--property", "-p", type=decimal_arg, default=Decimal("0"),
                        help="离婚案件中涉及财产分割的财产总额（元）")
    parser.add_argument("--damages", "-d", type=decimal_arg, default=Decimal("0"),
                        help="人格权案件损害赔偿金额（元）")
    parser.add_argument("--base-fee", "-b", type=decimal_arg, default=None,
                        help="幅度费用中的基础费（元），如不指定则取区间下限")

    args = parser.parse_args()
    amount = args.amount
    property_amount = args.property
    damages = args.damages

    t = args.type
    try:
        if t == "property":
            result = fixed_fee_result(
                "财产案件受理费",
                calc_property_fee(amount),
                "《诉讼费用交纳办法》第十三条第（一）项",
                breakdown=build_property_breakdown(amount),
            )
            print(format_result(result))

        elif t == "divorce":
            base = args.base_fee if args.base_fee is not None else Decimal("50")
            result = calc_divorce_fee(property_amount, base)
            result.update({
                "case_type": "离婚案件受理费",
                "article": "《诉讼费用交纳办法》第十三条第（二）项第1目",
                "base_fee": Decimal(str(result["base_fee"])),
                "extra_fee": Decimal(str(result["extra_fee"])),
                "total": Decimal(str(result["total"])),
                "breakdown": ["超过20万元的财产分割部分按 0.5% 另行交纳。"],
            })
            print(format_result(result))

        elif t == "personality":
            base = args.base_fee if args.base_fee is not None else Decimal("100")
            result = calc_personality_fee(damages, base)
            result.update({
                "case_type": "侵害人格权案件受理费",
                "article": "《诉讼费用交纳办法》第十三条第（二）项第2目",
                "base_fee": Decimal(str(result["base_fee"])),
                "extra_fee": Decimal(str(result["extra_fee"])),
                "total": Decimal(str(result["total"])),
                "breakdown": ["超过5万元至10万元部分按 1%，超过10万元部分按 0.5%。"],
            })
            print(format_result(result))

        elif t == "other_non":
            print(format_result(fixed_fee_result(
                "其他非财产案件受理费",
                Decimal("50"),
                "《诉讼费用交纳办法》第十三条第（二）项第3目",
                note="每件50~100元；此处默认取下限50元，以当地法院标准为准。",
            )))

        elif t == "ip_no_amount":
            print(format_result(fixed_fee_result(
                "知识产权案件受理费（无争议金额）",
                Decimal("500"),
                "《诉讼费用交纳办法》第十三条第（三）项",
                note="每件500~1000元；此处默认取下限500元，以当地法院标准为准。",
            )))

        elif t == "ip_with_amount":
            result = fixed_fee_result(
                "知识产权案件受理费（有争议金额）",
                calc_property_fee(amount),
                "《诉讼费用交纳办法》第十三条第（三）项",
                note="有争议金额或价额时，按财产案件标准计算。",
                breakdown=build_property_breakdown(amount),
            )
            print(format_result(result))

        elif t == "labor":
            print(format_result(fixed_fee_result(
                "劳动争议案件受理费",
                Decimal("10"),
                "《诉讼费用交纳办法》第十三条第（四）项",
            )))

        elif t == "admin_ip":
            print(format_result(fixed_fee_result(
                "商标、专利、海事行政案件受理费",
                Decimal("100"),
                "《诉讼费用交纳办法》第十三条第（五）项",
            )))

        elif t == "admin_other":
            print(format_result(fixed_fee_result(
                "其他行政案件受理费",
                Decimal("50"),
                "《诉讼费用交纳办法》第十三条第（五）项",
            )))

        elif t == "jurisdiction":
            print(format_result(fixed_fee_result(
                "管辖权异议费",
                Decimal("50"),
                "《诉讼费用交纳办法》第十三条第（六）项",
                note="异议不成立时，每件50~100元；此处默认取下限50元，以当地法院标准为准。",
            )))

        elif t == "enforcement":
            result = fixed_fee_result(
                "申请执行费",
                calc_enforcement_fee(amount),
                "《诉讼费用交纳办法》第十四条第（一）项",
                breakdown=build_enforcement_breakdown(amount),
            )
            print(format_result(result))

        elif t == "enforcement_no":
            print(format_result(fixed_fee_result(
                "申请执行费（无金额）",
                Decimal("50"),
                "《诉讼费用交纳办法》第十四条第（一）项",
                note="无执行金额或价额时，每件50~500元；此处默认取下限50元。",
            )))

        elif t == "preservation":
            result = fixed_fee_result(
                "申请保全措施费",
                calc_preservation_fee(amount),
                "《诉讼费用交纳办法》第十四条第（二）项",
                note="不超过1000元或不涉及财产数额的，每件30元；最高不超过5000元。",
            )
            print(format_result(result))

        elif t == "payment_order":
            result = fixed_fee_result(
                "申请支付令费用",
                calc_payment_order_fee(amount),
                "《诉讼费用交纳办法》第十四条第（三）项",
                note="按财产案件受理费标准的 1/3 交纳。",
                breakdown=build_property_breakdown(amount),
            )
            print(format_result(result))

        elif t == "public_notice":
            print(format_result(fixed_fee_result(
                "申请公示催告费",
                Decimal("100"),
                "《诉讼费用交纳办法》第十四条第（四）项",
            )))

        elif t == "arbitration_set_aside":
            print(format_result(fixed_fee_result(
                "申请撤销仲裁裁决或认定仲裁协议效力费",
                Decimal("400"),
                "《诉讼费用交纳办法》第十四条第（五）项",
            )))

        elif t == "bankruptcy":
            result = fixed_fee_result(
                "破产案件申请费",
                calc_bankruptcy_fee(amount),
                "《诉讼费用交纳办法》第十四条第（六）项",
                note="依据破产财产总额，按财产案件受理费标准减半交纳，最高不超过30万元。",
                breakdown=build_property_breakdown(amount),
            )
            print(format_result(result))

        elif t == "maritime_fund":
            print(format_result(fixed_fee_result(
                "申请设立海事赔偿责任限制基金费",
                Decimal("1000"),
                "《诉讼费用交纳办法》第十四条第（七）项",
                note="法定区间为1000元至1万元；此处默认取下限1000元。",
            )))

        elif t == "maritime_injunction":
            print(format_result(fixed_fee_result(
                "申请海事强制令费",
                Decimal("1000"),
                "《诉讼费用交纳办法》第十四条第（七）项",
                note="法定区间为1000元至5000元；此处默认取下限1000元。",
            )))

        elif t == "maritime_priority":
            print(format_result(fixed_fee_result(
                "申请船舶优先权催告费",
                Decimal("1000"),
                "《诉讼费用交纳办法》第十四条第（七）项",
                note="法定区间为1000元至5000元；此处默认取下限1000元。",
            )))

        elif t == "maritime_claim":
            print(format_result(fixed_fee_result(
                "申请海事债权登记费",
                Decimal("1000"),
                "《诉讼费用交纳办法》第十四条第（七）项",
            )))

        elif t == "maritime_average":
            print(format_result(fixed_fee_result(
                "申请共同海损理算费",
                Decimal("1000"),
                "《诉讼费用交纳办法》第十四条第（七）项",
            )))

    except ValueError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)


# ─────────────────────────────────────────────
# 供其他脚本 import 使用的公开 API
# ─────────────────────────────────────────────
__all__ = [
    "calc_property_fee",
    "calc_divorce_fee",
    "calc_personality_fee",
    "calc_enforcement_fee",
    "calc_preservation_fee",
    "calc_payment_order_fee",
    "calc_bankruptcy_fee",
    "build_property_breakdown",
    "build_enforcement_breakdown",
]

if __name__ == "__main__":
    main()
