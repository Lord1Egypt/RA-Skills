#!/usr/bin/env python3
"""
诉讼费用自动计算模块
依据：《诉讼费用交纳办法》（国务院令第481号，2007年4月1日施行）

功能：
  1. 财产案件受理费（按标的额分段累计）
  2. 非财产案件受理费
  3. 申请费（执行/保全/支付令等）
  4. 减半规则（调解/撤诉/简易程序）
"""

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeeResult:
    """诉讼费计算结果"""
    case_type: str           # 案件类型
    amount: float            # 标的额（元）
    base_fee: float          # 基础受理费（元）
    reduced_fee: float       # 减半后费用（元）
    reduction_reason: str    # 减半原因
    calculation: str         # 计算过程说明
    applicable_laws: str     # 适用法条


# ─── 财产案件受理费（第十三条第一款） ─────────────────
PROPERTY_BRACKETS = [
    (10000,      50,    None),      # ≤1万：50元
    (100000,     None,  0.025),     # >1万~10万：2.5%
    (200000,     None,  0.02),      # >10万~20万：2%
    (500000,     None,  0.015),     # >20万~50万：1.5%
    (1000000,    None,  0.01),      # >50万~100万：1%
    (2000000,    None,  0.009),     # >100万~200万：0.9%
    (5000000,    None,  0.008),     # >200万~500万：0.8%
    (10000000,   None,  0.007),     # >500万~1000万：0.7%
    (20000000,   None,  0.006),     # >1000万~2000万：0.6%
    (float('inf'), None, 0.005),    # >2000万：0.5%
]


def calc_property_fee(amount: float) -> tuple:
    """
    计算财产案件受理费（分段累计）

    Args:
        amount: 诉讼标的额（元）

    Returns:
        (受理费, 计算过程说明)
    """
    if amount <= 0:
        return 0, "标的额为0"

    if amount <= 10000:
        return 50, "不超过1万元，每件交纳50元"

    total = 0
    steps = []
    prev_limit = 0

    for limit, fixed, rate in PROPERTY_BRACKETS:
        if amount <= prev_limit:
            break

        taxable = min(amount, limit) - prev_limit
        if taxable <= 0:
            prev_limit = limit
            continue

        if fixed is not None:
            # 第一档：固定50元
            total += fixed
            steps.append(f"≤1万元: 50元")
        else:
            tier_fee = taxable * rate
            total += tier_fee
            pct = rate * 100
            steps.append(f"{_fmt(prev_limit)}~{_fmt(min(amount, limit))}: {taxable:.0f}×{pct}%={tier_fee:.0f}元")

        prev_limit = limit

    # 四舍五入到元
    total = math.ceil(total)
    detail = " + ".join(steps)
    return total, f"分段累计: {detail} = {total}元"


def _fmt(n):
    """格式化金额"""
    if n >= 10000:
        return f"{n/10000:.0f}万"
    return f"{n:.0f}元"


# ─── 非财产案件受理费（第十三条第二款） ─────────────
def calc_non_property_fee(case_type: str, related_amount: float = 0) -> tuple:
    """
    计算非财产案件受理费

    Args:
        case_type: 案件类型（离婚/人格权/其他）
        related_amount: 涉及财产分割或损害赔偿的金额（元）

    Returns:
        (受理费, 计算过程说明)
    """
    if case_type == "离婚":
        base = 300  # 取上限
        if related_amount <= 200000:
            return base, f"离婚案件每件交纳300元，财产分割≤20万不另行交纳"
        else:
            extra = (related_amount - 200000) * 0.005
            total = math.ceil(base + extra)
            return total, f"离婚案件300元 + 超过20万部分({related_amount-200000:.0f}×0.5%={extra:.0f}元) = {total}元"

    elif case_type == "人格权":
        base = 500  # 取上限
        if related_amount <= 50000:
            return base, f"人格权案件每件交纳500元，赔偿金额≤5万不另行交纳"
        elif related_amount <= 100000:
            extra = (related_amount - 50000) * 0.01
            total = math.ceil(base + extra)
            return total, f"人格权案件500元 + 超过5万部分({related_amount-50000:.0f}×1%={extra:.0f}元) = {total}元"
        else:
            extra1 = 50000 * 0.01  # 5万~10万部分
            extra2 = (related_amount - 100000) * 0.005
            total = math.ceil(base + extra1 + extra2)
            return total, f"人格权案件500元 + 5万~10万(500元) + 超过10万({related_amount-100000:.0f}×0.5%={extra2:.0f}元) = {total}元"

    else:
        # 其他非财产案件
        return 100, "其他非财产案件每件交纳100元"


# ─── 特殊案件受理费（第十三条第三~六款） ─────────────
def calc_special_fee(case_type: str, amount: float = 0) -> tuple:
    """
    计算特殊案件受理费

    Args:
        case_type: 案件类型
        amount: 争议金额（元）

    Returns:
        (受理费, 计算过程说明)
    """
    if case_type == "知识产权":
        if amount <= 0:
            return 1000, "知识产权案件无争议金额，每件交纳1000元"
        else:
            fee, detail = calc_property_fee(amount)
            return fee, f"知识产权案件有争议金额，按财产案件标准: {detail}"

    elif case_type == "劳动争议":
        return 10, "劳动争议案件每件交纳10元"

    elif case_type == "行政_商标专利海事":
        return 100, "商标、专利、海事行政案件每件交纳100元"

    elif case_type == "行政_其他":
        return 50, "其他行政案件每件交纳50元"

    elif case_type == "管辖权异议":
        return 100, "管辖权异议不成立，每件交纳100元"

    else:
        return 0, f"未知案件类型: {case_type}"


# ─── 申请费（第十四条） ──────────────────────────────
def calc_application_fee(fee_type: str, amount: float = 0) -> tuple:
    """
    计算申请费

    Args:
        fee_type: 申请类型（执行/保全/支付令/公示催告/撤销仲裁/破产）
        amount: 执行金额/保全金额/破产财产总额（元）

    Returns:
        (申请费, 计算过程说明)
    """
    if fee_type == "执行":
        if amount <= 0:
            return 500, "无执行金额，每件交纳500元"
        elif amount <= 10000:
            return 50, "执行金额≤1万，每件交纳50元"
        elif amount <= 500000:
            fee = math.ceil(50 + (amount - 10000) * 0.015)
            return fee, f"50元 + 超过1万部分({amount-10000:.0f}×1.5%) = {fee}元"
        elif amount <= 5000000:
            fee = math.ceil(50 + 490000 * 0.015 + (amount - 500000) * 0.01)
            return fee, f"50元 + 7350元 + 超过50万部分({amount-500000:.0f}×1%) = {fee}元"
        elif amount <= 10000000:
            fee = math.ceil(50 + 490000 * 0.015 + 4500000 * 0.01 + (amount - 5000000) * 0.005)
            return fee, f"50元 + 7350元 + 45000元 + 超过500万部分({amount-5000000:.0f}×0.5%) = {fee}元"
        else:
            fee = math.ceil(50 + 490000 * 0.015 + 4500000 * 0.01 + 5000000 * 0.005 + (amount - 10000000) * 0.001)
            return fee, f"分段累计 = {fee}元"

    elif fee_type == "保全":
        if amount <= 1000:
            return 30, "保全金额≤1000元，每件交纳30元"
        elif amount <= 100000:
            fee = math.ceil(30 + (amount - 1000) * 0.01)
            return min(fee, 5000), f"30元 + 超过1000元部分({amount-1000:.0f}×1%) = {min(fee,5000)}元"
        else:
            fee = math.ceil(30 + 99000 * 0.01 + (amount - 100000) * 0.005)
            return min(fee, 5000), f"30元 + 990元 + 超过10万部分({amount-100000:.0f}×0.5%) = {min(fee,5000)}元"

    elif fee_type == "支付令":
        fee, detail = calc_property_fee(amount)
        pay_fee = math.ceil(fee / 3)
        return pay_fee, f"财产案件受理费{fee}元的1/3 = {pay_fee}元"

    elif fee_type == "公示催告":
        return 100, "申请公示催告，每件交纳100元"

    elif fee_type == "撤销仲裁":
        return 400, "申请撤销仲裁裁决或认定仲裁协议效力，每件交纳400元"

    elif fee_type == "破产":
        fee, detail = calc_property_fee(amount)
        half = math.ceil(fee / 2)
        return min(half, 300000), f"财产案件受理费{fee}元减半={half}元，最高不超过30万元"

    else:
        return 0, f"未知申请类型: {fee_type}"


# ─── 综合计算入口 ────────────────────────────────────
def calculate_fee(
    case_type: str,
    amount: float = 0,
    simplified: bool = False,
    mediation: bool = False,
    withdrawal: bool = False,
) -> FeeResult:
    """
    综合计算诉讼费用

    Args:
        case_type: 案件类型
            - "财产": 财产案件
            - "离婚": 离婚案件
            - "人格权": 人格权案件
            - "知识产权": 知识产权案件
            - "劳动争议": 劳动争议案件
            - "行政": 行政案件
            - "其他非财产": 其他非财产案件
        amount: 诉讼标的额或相关金额（元）
        simplified: 是否适用简易程序
        mediation: 是否调解结案
        withdrawal: 是否撤诉

    Returns:
        FeeResult
    """
    # 1. 计算基础受理费
    if case_type == "财产":
        base_fee, calculation = calc_property_fee(amount)
        applicable = "《诉讼费用交纳办法》第十三条第一款"
    elif case_type == "离婚":
        base_fee, calculation = calc_non_property_fee("离婚", amount)
        applicable = "《诉讼费用交纳办法》第十三条第二款第1项"
    elif case_type == "人格权":
        base_fee, calculation = calc_non_property_fee("人格权", amount)
        applicable = "《诉讼费用交纳办法》第十三条第二款第2项"
    elif case_type == "知识产权":
        base_fee, calculation = calc_special_fee("知识产权", amount)
        applicable = "《诉讼费用交纳办法》第十三条第三款"
    elif case_type == "劳动争议":
        base_fee, calculation = calc_special_fee("劳动争议")
        applicable = "《诉讼费用交纳办法》第十三条第四款"
    elif case_type == "行政":
        base_fee, calculation = calc_special_fee("行政_其他")
        applicable = "《诉讼费用交纳办法》第十三条第五款"
    else:
        base_fee, calculation = calc_non_property_fee("其他")
        applicable = "《诉讼费用交纳办法》第十三条第二款第3项"

    # 2. 减半规则
    reduced_fee = base_fee
    reduction_reason = ""

    if mediation or withdrawal:
        reduced_fee = math.ceil(base_fee / 2)
        reduction_reason = "调解/撤诉减半（第十五条）"
    elif simplified:
        reduced_fee = math.ceil(base_fee / 2)
        reduction_reason = "简易程序减半（第十六条）"

    return FeeResult(
        case_type=case_type,
        amount=amount,
        base_fee=base_fee,
        reduced_fee=reduced_fee,
        reduction_reason=reduction_reason,
        calculation=calculation,
        applicable_laws=applicable,
    )


# ─── 格式化输出 ──────────────────────────────────────
def format_fee_text(result: FeeResult) -> str:
    """格式化为文本"""
    lines = [
        f"案件受理费计算",
        f"  案件类型: {result.case_type}",
        f"  标的额: {result.amount:,.0f}元",
        f"  计算过程: {result.calculation}",
        f"  基础受理费: {result.base_fee:,.0f}元",
    ]
    if result.reduction_reason:
        lines.append(f"  减半原因: {result.reduction_reason}")
        lines.append(f"  实际受理费: {result.reduced_fee:,.0f}元")
    lines.append(f"  依据: {result.applicable_laws}")
    return "\n".join(lines)


def format_fee_html(result: FeeResult) -> str:
    """格式化为HTML片段"""
    return f"""
<div style="background:#fafaf8;border:1px solid #d4d0c8;border-left:3px solid #8b0000;padding:12px 16px;margin:12px 0;border-radius:2px;font-size:14pt;line-height:24pt">
  <strong>案件受理费</strong><br>
  案件类型: {result.case_type} | 标的额: {result.amount:,.0f}元<br>
  计算: {result.calculation}<br>
  基础受理费: {result.base_fee:,.0f}元<br>
  {"<em>" + result.reduction_reason + "</em> → 实际: " + f"{result.reduced_fee:,.0f}" + "元<br>" if result.reduction_reason else ""}
  依据: {result.applicable_laws}
</div>
"""


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse
    p = argparse.ArgumentParser(description="诉讼费用计算器")
    p.add_argument("--type", "-t", default="财产", help="案件类型")
    p.add_argument("--amount", "-a", type=float, default=0, help="标的额（元）")
    p.add_argument("--simplified", action="store_true", help="简易程序")
    p.add_argument("--mediation", action="store_true", help="调解结案")
    p.add_argument("--withdrawal", action="store_true", help="撤诉")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    result = calculate_fee(args.type, args.amount, args.simplified, args.mediation, args.withdrawal)

    if args.json:
        import json
        print(json.dumps({
            "case_type": result.case_type,
            "amount": result.amount,
            "base_fee": result.base_fee,
            "reduced_fee": result.reduced_fee,
            "reduction_reason": result.reduction_reason,
            "calculation": result.calculation,
            "applicable_laws": result.applicable_laws,
        }, ensure_ascii=False, indent=2))
    else:
        print(format_fee_text(result))


if __name__ == "__main__":
    main()
