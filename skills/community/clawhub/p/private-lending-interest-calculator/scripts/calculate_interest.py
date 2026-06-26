#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP, getcontext
from pathlib import Path
from typing import Iterable, Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

getcontext().prec = 28

DECIMAL_ZERO = Decimal("0")
DECIMAL_ONE = Decimal("1")
RATE_24 = Decimal("24")
RATE_36 = Decimal("36")
RATE_6 = Decimal("6")
DATE_2015 = date(2015, 9, 1)
DATE_2020 = date(2020, 8, 20)
FIRST_LPR_DATE = date(2019, 8, 20)


class CalculationError(Exception):
    """命令行计算异常。"""


@dataclass(frozen=True)
class LprRecord:
    quoted_on: date
    one_year_rate: Decimal


@dataclass
class Repayment:
    repayment_date: date
    amount: Decimal
    note: str = ""


@dataclass
class Segment:
    start: date
    end: date
    days: int
    phase: str
    principal: Decimal
    applied_rate: Decimal
    rate_cap: Decimal
    charge_amount: Decimal
    legal_basis: str
    penalty_rate: Decimal = DECIMAL_ZERO


@dataclass
class RepaymentAllocation:
    repayment_date: date
    amount: Decimal
    to_fees: Decimal
    to_within_interest: Decimal
    to_overdue_interest: Decimal
    to_penalty: Decimal
    to_principal: Decimal
    remaining_principal: Decimal
    note: str = ""


@dataclass
class CalculationResult:
    original_principal: Decimal
    contract_principal: Optional[Decimal]
    principal: Decimal
    loan_date: date
    loan_end: Optional[date]
    as_of: date
    regime_name: str
    lpr_used: Optional[Decimal]
    segments: list[Segment]
    repayments: list[RepaymentAllocation]
    within_interest_total: Decimal
    overdue_interest_total: Decimal
    penalty_total: Decimal
    within_interest_outstanding: Decimal
    overdue_interest_outstanding: Decimal
    penalty_outstanding: Decimal
    fees_outstanding: Decimal
    warnings: list[str]
    assumptions: list[str]
    compound_capitalized: Decimal = DECIMAL_ZERO


def quantize_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_money(value: Decimal) -> str:
    return f"¥ {float(quantize_money(value)):,.2f}"


def format_rate(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}%"


def decimal_arg(value: str) -> Decimal:
    try:
        return Decimal(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError(f"无效数字：{value}") from exc


def date_arg(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"无效日期：{value}，应为 YYYY-MM-DD") from exc


def load_lpr_data(reference_path: Path) -> list[LprRecord]:
    records: list[LprRecord] = []
    pattern = re.compile(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([\d.]+)%\s*\|")
    for line in reference_path.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if not match:
            continue
        records.append(
            LprRecord(
                quoted_on=datetime.strptime(match.group(1), "%Y-%m-%d").date(),
                one_year_rate=Decimal(match.group(2)),
            )
        )
    records.sort(key=lambda item: item.quoted_on)
    if not records:
        raise CalculationError(f"未从 LPR 参考文件中读取到数据：{reference_path}")
    return records


def find_lpr(as_of_date: date, lpr_records: list[LprRecord]) -> tuple[Decimal, Optional[str]]:
    chosen: Optional[LprRecord] = None
    for record in lpr_records:
        if record.quoted_on <= as_of_date:
            chosen = record
        else:
            break

    if chosen:
        return chosen.one_year_rate, None

    first = lpr_records[0]
    warning = (
        f"借款日期早于首个 LPR 报价日 {first.quoted_on.isoformat()}，"
        f"后 2020-08-20 时段改按首期 LPR {format_rate(first.one_year_rate)} 计算，需人工复核。"
    )
    return first.one_year_rate, warning


def determine_regime_name(loan_date: date) -> str:
    if loan_date < DATE_2015:
        return "旧民间借贷意见（银行同期贷款利率四倍）"
    if loan_date < DATE_2020:
        return "2015年《民间借贷规定》（24%/36%两线三区）"
    return "2020修订后规则（合同成立时1年期LPR四倍）"


def load_repayments(raw: str | None) -> list[Repayment]:
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("@"):
        payload = Path(raw[1:]).read_text(encoding="utf-8")
    else:
        payload = raw

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CalculationError(f"--repayments 不是合法 JSON：{exc}") from exc

    if not isinstance(parsed, list):
        raise CalculationError("--repayments 必须是 JSON 数组")

    result: list[Repayment] = []
    for item in parsed:
        if not isinstance(item, dict):
            raise CalculationError("--repayments 数组中的每一项都必须是对象")
        if "date" not in item or "amount" not in item:
            raise CalculationError("每条还款记录必须包含 date 和 amount 字段")
        repayment = Repayment(
            repayment_date=date_arg(str(item["date"])),
            amount=decimal_arg(str(item["amount"])),
            note=str(item.get("note", "") or item.get("nature", "") or "").strip(),
        )
        if repayment.amount <= 0:
            raise CalculationError("还款金额必须大于 0")
        result.append(repayment)
    result.sort(key=lambda item: (item.repayment_date, item.amount))
    return result


def unique_sorted_dates(values: Iterable[date]) -> list[date]:
    return sorted({item for item in values})


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def annual_interest(principal: Decimal, annual_rate: Decimal, days: int) -> Decimal:
    if principal <= 0 or annual_rate <= 0 or days <= 0:
        return DECIMAL_ZERO
    return quantize_money(principal * (annual_rate / Decimal("100")) * Decimal(days) / Decimal("365"))


def min_rate(left: Optional[Decimal], right: Decimal) -> Decimal:
    if left is None:
        return DECIMAL_ZERO
    return left if left <= right else right


def stage_cap_rate(
        *,
        loan_date: date,
        segment_start: date,
        lpr_records: list[LprRecord],
        legacy_base_rate: Optional[Decimal],
        warnings: list[str],
) -> Decimal:
    if segment_start < DATE_2015:
        if legacy_base_rate is None:
            raise CalculationError("借款日期早于 2015-09-01 时，必须提供 --legacy-base-rate（银行同期贷款年利率）。")
        return legacy_base_rate * Decimal("4")
    if segment_start < DATE_2020:
        return RATE_24

    lpr_rate, warning = find_lpr(loan_date, lpr_records)
    if warning and warning not in warnings:
        warnings.append(warning)
    return lpr_rate * Decimal("4")


def default_overdue_rate(
        *,
        segment_start: date,
        lpr_records: list[LprRecord],
        legacy_base_rate: Optional[Decimal],
        assumptions: list[str],
) -> Decimal:
    if segment_start < DATE_2015:
        if legacy_base_rate is None:
            raise CalculationError("旧规时段未约定逾期利率时，需要提供 --legacy-base-rate 以估算同期贷款利率。")
        assumptions.append("旧规时段未约定逾期利率，按提供的银行同期贷款年利率估算。")
        return legacy_base_rate
    if segment_start < DATE_2020:
        return RATE_6

    lpr_rate, _ = find_lpr(segment_start, lpr_records)
    assumptions.append("逾期利率未约定，2020-08-20后按逾期当时1年期LPR计算。")
    return lpr_rate


def legal_basis_text(segment_start: date, phase: str) -> str:
    if segment_start < DATE_2015:
        return "1991年意见第6条、第7条"
    if segment_start < DATE_2020:
        return "2015年规定第26条、第29条、第30条" if phase == "逾期" else "2015年规定第26条"
    return "2020/2021修正规定第26条、第29条、第30条" if phase == "逾期" else "2020修正规定第26条"


def calculate_interest(args: argparse.Namespace) -> CalculationResult:
    root = Path(__file__).resolve().parent.parent
    lpr_records = load_lpr_data(root / "references" / "lpr_data.md")

    principal = args.principal
    if principal <= 0:
        raise CalculationError("本金必须大于 0")

    if args.contract_principal is not None and args.contract_principal < principal:
        raise CalculationError("--contract-principal 不得小于 --principal（实际到账本金）")

    if args.loan_end and args.loan_end < args.loan_date:
        raise CalculationError("借款到期日不得早于借款日期")

    as_of = args.as_of or date.today()
    if as_of < args.loan_date:
        raise CalculationError("--as-of 不得早于借款日期")

    overdue_date = args.overdue_date
    if overdue_date is None and args.loan_end and as_of > args.loan_end:
        overdue_date = args.loan_end
    if overdue_date and overdue_date < args.loan_date:
        raise CalculationError("逾期日期不得早于借款日期")

    repayments = load_repayments(args.repayments)
    repayments = [item for item in repayments if args.loan_date <= item.repayment_date <= as_of]

    warnings: list[str] = []
    assumptions: list[str] = []
    regime_name = determine_regime_name(args.loan_date)
    lpr_used: Optional[Decimal] = None
    if args.loan_date >= DATE_2020 or as_of >= DATE_2020:
        lpr_used, warning = find_lpr(args.loan_date, lpr_records)
        if warning:
            warnings.append(warning)

    if args.rate is None:
        assumptions.append("未提供借期内约定利率，按无息处理。")

    dates: list[date] = [args.loan_date, as_of]
    if overdue_date:
        dates.append(overdue_date)
    if args.compound_date:
        dates.append(args.compound_date)
    if args.loan_date < DATE_2020 <= as_of:
        dates.append(DATE_2020)
    dates.extend(item.repayment_date for item in repayments)
    time_points = unique_sorted_dates(item for item in dates if args.loan_date <= item <= as_of)

    outstanding_principal = quantize_money(principal)
    original_principal = quantize_money(principal)
    fees_outstanding = quantize_money(args.fees or DECIMAL_ZERO)
    within_interest_outstanding = DECIMAL_ZERO
    overdue_interest_outstanding = DECIMAL_ZERO
    penalty_outstanding = DECIMAL_ZERO
    within_interest_total = DECIMAL_ZERO
    overdue_interest_total = DECIMAL_ZERO
    penalty_total = DECIMAL_ZERO
    compound_capitalized = DECIMAL_ZERO
    segments: list[Segment] = []
    repayment_allocations: list[RepaymentAllocation] = []
    capitalized = False

    repayment_map: dict[date, list[Repayment]] = {}
    for repayment in repayments:
        repayment_map.setdefault(repayment.repayment_date, []).append(repayment)

    for index in range(len(time_points) - 1):
        current = time_points[index]
        nxt = time_points[index + 1]
        if nxt <= current:
            continue

        days = (nxt - current).days
        phase = "逾期" if overdue_date and current >= overdue_date else "借期内"
        cap = stage_cap_rate(
            loan_date=args.loan_date,
            segment_start=current,
            lpr_records=lpr_records,
            legacy_base_rate=args.legacy_base_rate,
            warnings=warnings,
        )
        if phase == "借期内":
            applied_rate = min_rate(args.rate, cap)
            if args.rate is not None and args.rate > cap:
                warning = f"{current.isoformat()} 起借期内约定利率 {format_rate(args.rate)} 超过法定上限，已按 {format_rate(cap)} 截断。"
                if warning not in warnings:
                    warnings.append(warning)
            penalty_rate = DECIMAL_ZERO
        else:
            if args.overdue_rate is not None:
                applied_rate = min(args.overdue_rate, cap)
                if args.overdue_rate > cap:
                    warning = f"{current.isoformat()} 起约定逾期利率 {format_rate(args.overdue_rate)} 超过法定上限，已按 {format_rate(cap)} 截断。"
                    if warning not in warnings:
                        warnings.append(warning)
            elif args.rate is not None:
                applied_rate = min(args.rate, cap)
            else:
                applied_rate = default_overdue_rate(
                    segment_start=current,
                    lpr_records=lpr_records,
                    legacy_base_rate=args.legacy_base_rate,
                    assumptions=assumptions,
                )
                if applied_rate > cap:
                    applied_rate = cap

            requested_penalty = args.penalty_rate or DECIMAL_ZERO
            penalty_rate = min(requested_penalty, max(DECIMAL_ZERO, cap - applied_rate))
            if requested_penalty > penalty_rate:
                warning = (
                    f"{current.isoformat()} 起违约金年化 {format_rate(requested_penalty)} 与逾期利息合计超过法定上限，"
                    f"违约金已调整为 {format_rate(penalty_rate)}。"
                )
                if warning not in warnings:
                    warnings.append(warning)

        interest_amount = annual_interest(outstanding_principal, applied_rate, days)
        penalty_amount = annual_interest(outstanding_principal, penalty_rate, days)
        charge_amount = quantize_money(interest_amount + penalty_amount)

        if phase == "借期内":
            within_interest_outstanding = quantize_money(within_interest_outstanding + interest_amount)
            within_interest_total = quantize_money(within_interest_total + interest_amount)
        else:
            overdue_interest_outstanding = quantize_money(overdue_interest_outstanding + interest_amount)
            overdue_interest_total = quantize_money(overdue_interest_total + interest_amount)
            penalty_outstanding = quantize_money(penalty_outstanding + penalty_amount)
            penalty_total = quantize_money(penalty_total + penalty_amount)

        segments.append(
            Segment(
                start=current,
                end=nxt,
                days=days,
                phase=phase,
                principal=outstanding_principal,
                applied_rate=applied_rate,
                rate_cap=cap,
                charge_amount=charge_amount,
                legal_basis=legal_basis_text(current, phase),
                penalty_rate=penalty_rate,
            )
        )

        if args.compound_date and nxt == args.compound_date and not capitalized:
            if overdue_date and args.compound_date >= overdue_date:
                warnings.append("复利约定发生在逾期后，脚本未将逾期利息滚入本金，请人工核对复利效力。")
            elif within_interest_outstanding > 0:
                outstanding_principal = quantize_money(outstanding_principal + within_interest_outstanding)
                compound_capitalized = quantize_money(compound_capitalized + within_interest_outstanding)
                within_interest_outstanding = DECIMAL_ZERO
                capitalized = True
                assumptions.append("已按一次性结息转本处理复利；若实际存在多次滚利，应人工复核。")

        for repayment in repayment_map.get(nxt, []):
            remaining = repayment.amount
            to_fees = min(remaining, fees_outstanding)
            fees_outstanding = quantize_money(fees_outstanding - to_fees)
            remaining = quantize_money(remaining - to_fees)

            to_within = min(remaining, within_interest_outstanding)
            within_interest_outstanding = quantize_money(within_interest_outstanding - to_within)
            remaining = quantize_money(remaining - to_within)

            to_overdue = min(remaining, overdue_interest_outstanding)
            overdue_interest_outstanding = quantize_money(overdue_interest_outstanding - to_overdue)
            remaining = quantize_money(remaining - to_overdue)

            to_penalty = min(remaining, penalty_outstanding)
            penalty_outstanding = quantize_money(penalty_outstanding - to_penalty)
            remaining = quantize_money(remaining - to_penalty)

            to_principal = min(remaining, outstanding_principal)
            outstanding_principal = quantize_money(outstanding_principal - to_principal)

            repayment_allocations.append(
                RepaymentAllocation(
                    repayment_date=repayment.repayment_date,
                    amount=repayment.amount,
                    to_fees=to_fees,
                    to_within_interest=to_within,
                    to_overdue_interest=to_overdue,
                    to_penalty=to_penalty,
                    to_principal=to_principal,
                    remaining_principal=outstanding_principal,
                    note=repayment.note,
                )
            )

            if outstanding_principal <= 0:
                outstanding_principal = DECIMAL_ZERO

    if args.contract_principal is not None and args.contract_principal > original_principal:
        warnings.append(
            f"存在砍头息迹象：合同本金 {format_money(args.contract_principal)}，实际到账本金 {format_money(original_principal)}。"
        )

    if args.professional_lender:
        warnings.append("用户提示存在职业放贷风险，合同效力及利息保护范围需另行审查。")

    if args.rate is not None and DATE_2015 <= args.loan_date < DATE_2020 and args.rate > RATE_36:
        warnings.append("借期内约定利率超过年利率36%，超出部分无效；若借款人已支付，可主张返还超额部分。")

    if args.rate is not None and args.loan_date >= DATE_2020 and lpr_used is not None and args.rate > lpr_used * Decimal(
            "4"):
        warnings.append("借期内约定利率超过合同成立时1年期LPR四倍，超出部分不受保护。")

    return CalculationResult(
        original_principal=original_principal,
        contract_principal=args.contract_principal,
        principal=outstanding_principal,
        loan_date=args.loan_date,
        loan_end=args.loan_end,
        as_of=as_of,
        regime_name=regime_name,
        lpr_used=lpr_used,
        segments=segments,
        repayments=repayment_allocations,
        within_interest_total=within_interest_total,
        overdue_interest_total=overdue_interest_total,
        penalty_total=penalty_total,
        within_interest_outstanding=within_interest_outstanding,
        overdue_interest_outstanding=overdue_interest_outstanding,
        penalty_outstanding=penalty_outstanding,
        fees_outstanding=fees_outstanding,
        warnings=unique_preserve_order(warnings),
        assumptions=unique_preserve_order(assumptions),
        compound_capitalized=compound_capitalized,
    )


def render_section_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    if not rows:
        return ["   无"]
    header = "   | " + " | ".join(headers) + " |"
    split = "   | " + " | ".join("---" for _ in headers) + " |"
    body = ["   | " + " | ".join(row) + " |" for row in rows]
    return [header, split, *body]


def render_report(result: CalculationResult) -> str:
    lines: list[str] = ["【民间借贷利息计算书】", ""]
    lines.extend(
        [
            "一、基础信息",
            f"   实际借款本金：{format_money(result.original_principal)}",
            f"   借款日期：{result.loan_date.isoformat()}",
            f"   截止日期：{result.as_of.isoformat()}",
            f"   借款到期日：{result.loan_end.isoformat() if result.loan_end else '未提供'}",
        ]
    )
    if result.contract_principal is not None:
        lines.append(f"   合同载明本金：{format_money(result.contract_principal)}")
    if result.compound_capitalized > 0:
        lines.append(f"   已结息转本金额：{format_money(result.compound_capitalized)}")
    lines.append("")

    lines.extend(
        [
            "二、法律适用",
            f"   借款成立时适用规则：{result.regime_name}",
        ]
    )
    if result.lpr_used is not None:
        lines.append(f"   合同成立时对应1年期LPR：{format_rate(result.lpr_used)}")
        lines.append(f"   LPR四倍上限：{format_rate(result.lpr_used * Decimal('4'))}")
    lines.append("")

    segment_rows = [
        [
            f"{item.start.isoformat()} 至 {item.end.isoformat()}",
            format_money(item.principal),
            item.phase,
            format_rate(item.applied_rate),
            format_rate(item.penalty_rate) if item.penalty_rate > 0 else "-",
            str(item.days),
            format_money(item.charge_amount),
            item.legal_basis,
        ]
        for item in result.segments
    ]
    lines.extend(["三、分段计算明细表"])
    lines.extend(
        render_section_table(
            ["期间", "计息本金", "性质", "适用利率", "违约金利率", "天数", "利息/费用", "法律依据"],
            segment_rows,
        )
    )
    lines.append("")

    lines.extend(["四、还款冲抵明细"])
    repayment_rows = [
        [
            item.repayment_date.isoformat(),
            format_money(item.amount),
            format_money(item.to_fees),
            format_money(item.to_within_interest + item.to_overdue_interest + item.to_penalty),
            format_money(item.to_principal),
            format_money(item.remaining_principal),
            item.note or "-",
        ]
        for item in result.repayments
    ]
    lines.extend(
        render_section_table(
            ["还款日", "还款金额", "冲抵费用", "冲抵利息/违约金", "冲抵本金", "剩余本金", "备注"],
            repayment_rows,
        )
    )
    lines.append("")

    total_interest = quantize_money(
        result.within_interest_outstanding + result.overdue_interest_outstanding + result.penalty_outstanding)
    total_due = quantize_money(result.principal + total_interest + result.fees_outstanding)
    lines.extend(
        [
            "五、结论",
            f"   截至 {result.as_of.isoformat()}：",
            f"   - 尚欠本金：{format_money(result.principal)}",
            f"   - 尚欠借期内利息：{format_money(result.within_interest_outstanding)}",
            f"   - 尚欠逾期利息：{format_money(result.overdue_interest_outstanding)}",
            f"   - 尚欠违约金/其他费用：{format_money(result.penalty_outstanding)}",
            f"   - 尚欠债权实现费用：{format_money(result.fees_outstanding)}",
            f"   - 本息费用合计：{format_money(total_due)}",
            "",
            "六、累计发生额",
            f"   - 累计借期内利息：{format_money(result.within_interest_total)}",
            f"   - 累计逾期利息：{format_money(result.overdue_interest_total)}",
            f"   - 累计违约金/其他费用：{format_money(result.penalty_total)}",
            "",
            "七、风险提示与假设",
        ]
    )
    if result.warnings:
        lines.extend([f"   - {item}" for item in result.warnings])
    if result.assumptions:
        lines.extend([f"   - 假设：{item}" for item in result.assumptions])
    if not result.warnings and not result.assumptions:
        lines.append("   - 无特殊风险提示。")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="民间借贷利息计算器（依据 1991/2015/2020/2021 相关司法规则）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python3 scripts/calculate_interest.py --principal 100000 --loan-date 2024-06-15 --rate 12 --loan-end 2025-06-15 --as-of 2025-04-20
  python3 scripts/calculate_interest.py --principal 100000 --loan-date 2019-01-01 --rate 24 --loan-end 2021-01-01 --as-of 2021-06-01
  python3 scripts/calculate_interest.py --principal 100000 --loan-date 2014-06-01 --rate 18 --legacy-base-rate 6.0 --as-of 2015-06-01
  python3 scripts/calculate_interest.py --principal 100000 --loan-date 2024-01-01 --rate 12 --loan-end 2024-07-01 --overdue-date 2024-07-01 --penalty-rate 3 --repayments @repayments.json
""",
    )
    parser.add_argument("--principal", required=True, type=decimal_arg, help="实际到账本金")
    parser.add_argument("--contract-principal", type=decimal_arg, default=None, help="合同载明本金，用于识别砍头息")
    parser.add_argument("--loan-date", required=True, type=date_arg, help="借款日期，YYYY-MM-DD")
    parser.add_argument("--loan-end", type=date_arg, default=None, help="借款到期日，YYYY-MM-DD")
    parser.add_argument("--as-of", type=date_arg, default=None, help="计算截止日，默认今天")
    parser.add_argument("--rate", type=decimal_arg, default=None, help="借期内年化利率，单位：%%")
    parser.add_argument("--overdue-date", type=date_arg, default=None, help="逾期起算日，默认按 loan-end")
    parser.add_argument("--overdue-rate", type=decimal_arg, default=None, help="约定逾期年化利率，单位：%%")
    parser.add_argument("--penalty-rate", type=decimal_arg, default=DECIMAL_ZERO,
                        help="违约金或其他费用折算年化利率，单位：%%")
    parser.add_argument("--fees", type=decimal_arg, default=DECIMAL_ZERO, help="实现债权的有关费用余额")
    parser.add_argument("--repayments", default=None, help="还款记录 JSON 字符串，或 @文件路径")
    parser.add_argument("--compound-date", type=date_arg, default=None, help="一次性结息转本日期")
    parser.add_argument("--legacy-base-rate", type=decimal_arg, default=None,
                        help="2015-09-01前银行同期贷款年利率，用于计算四倍上限")
    parser.add_argument("--professional-lender", action="store_true", help="提示存在职业放贷风险")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = calculate_interest(args)
    except CalculationError as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1

    print(render_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
