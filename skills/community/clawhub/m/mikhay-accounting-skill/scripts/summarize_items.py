#!/usr/bin/env python3
"""Summarize subscriptions and belongings.

These records are a side list. Totals here are not assets, net worth, or 备查净值.
Selling an item is a separate 收入/其他 ledger row plus 状态=已卖出 on the item.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import fmt, load_file, money, parse_time


CYCLES = {"月", "季", "年", "周"}
SUB_STATUSES = {"active", "已取消"}
HOLDING_STATUSES = {"持有", "已卖出", "已送出"}


def load_items(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("items file must be a JSON object")
    return data


def monthly_amount(amount: Decimal, cycle: str) -> Decimal:
    if cycle == "季":
        return amount / Decimal(3)
    if cycle == "年":
        return amount / Decimal(12)
    if cycle == "周":
        return amount * Decimal(52) / Decimal(12)
    return amount


def _status(row: dict[str, Any], default: str) -> str:
    text = str(row.get("状态", "") or "").strip()
    return text or default


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是"}


def validate_items(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    subscriptions = data.get("subscriptions", [])
    holdings = data.get("holdings", [])
    if subscriptions is None:
        subscriptions = []
    if holdings is None:
        holdings = []
    if not isinstance(subscriptions, list) or not isinstance(holdings, list):
        return ["subscriptions and holdings must be lists"], warnings
    for index, row in enumerate(subscriptions, 1):
        prefix = f"subscription[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        if money(row.get("金额")) <= 0 and str(row.get("金额", "")).strip() != "":
            errors.append(f"{prefix}: 金额 must be positive")
        cycle = str(row.get("周期", "") or "").strip() or "月"
        if cycle not in CYCLES:
            errors.append(f"{prefix}: 周期 must be 月, 季, 年, or 周")
        status = _status(row, "active")
        if status not in SUB_STATUSES:
            warnings.append(f"{prefix}: unknown 状态 {status}")
        renewal = str(row.get("续费日", "") or "").strip()
        if renewal and parse_time(renewal) is None:
            errors.append(f"{prefix}: invalid 续费日")
    for index, row in enumerate(holdings, 1):
        prefix = f"holding[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        status = _status(row, "持有")
        if status not in HOLDING_STATUSES:
            warnings.append(f"{prefix}: unknown 状态 {status}")
        if status == "持有" and str(row.get("购入价", "")).strip() == "":
            errors.append(f"{prefix}: missing 购入价")
        for field in ("购入日期", "估值日期"):
            raw = str(row.get(field, "") or "").strip()
            if raw and parse_time(raw) is None:
                errors.append(f"{prefix}: invalid {field}")
    return errors, warnings


def active_subscriptions(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = data.get("subscriptions") or []
    return [row for row in rows if isinstance(row, dict) and _status(row, "active") == "active"]


def held_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = data.get("holdings") or []
    return [row for row in rows if isinstance(row, dict) and _status(row, "持有") == "持有"]


def residual_of(data: dict[str, Any]) -> Decimal:
    return sum((money(row.get("估计残值")) for row in held_rows(data)), Decimal("0"))


def _days(start: date, end: date) -> int:
    return max((end - start).days, 1)


def daily_cost(row: dict[str, Any], as_of: date) -> Decimal | None:
    bought = parse_time(row.get("购入日期"))
    if bought is None:
        return None
    valued = parse_time(row.get("估值日期"))
    end = valued.date() if valued is not None else as_of
    return (money(row.get("购入价")) - money(row.get("估计残值"))) / Decimal(_days(bought.date(), end))


def _load_ledger_records(paths: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        book, errors = load_file(path)
        if errors and not book.get("records"):
            raise SystemExit(f"{path}: {errors[0]}")
        records.extend(row for row in book.get("records") or [] if isinstance(row, dict))
    return records


def has_reimbursement(sub: dict[str, Any], records: list[dict[str, Any]]) -> bool:
    sub_id = str(sub.get("id", "") or "").strip()
    name = str(sub.get("名称", "") or "").strip()
    expense_ids: set[str] = set()
    for row in records:
        item_id = str(row.get("item_id", "") or "").strip()
        tx_type = str(row.get("收支类型", "")).strip()
        linked = bool(sub_id) and item_id == sub_id
        named = bool(name) and name in str(row.get("备注", ""))
        if tx_type == "报销" and (linked or named):
            return True
        if tx_type == "支出" and linked:
            if str(row.get("报销状态", "") or "").strip() == "已报销":
                return True
            expense_id = str(row.get("id", "") or "").strip()
            if expense_id:
                expense_ids.add(expense_id)
    for row in records:
        if str(row.get("收支类型", "")).strip() != "报销":
            continue
        ref = str(row.get("reimburse_of", "") or "").strip()
        if ref and ref in expense_ids:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize subscriptions and holdings. Not part of net worth.")
    parser.add_argument("items", type=Path)
    parser.add_argument("--ledger", action="append", type=Path, default=[], help="Ledger used to see if a subscription was reimbursed.")
    parser.add_argument("--as-of", help="Date for renewals and daily cost, YYYY-MM-DD. Default: today.")
    args = parser.parse_args()
    if args.as_of:
        parsed = parse_time(args.as_of)
        if parsed is None:
            raise SystemExit("--as-of must be YYYY-MM-DD")
        as_of = parsed.date()
    else:
        as_of = date.today()

    data = load_items(args.items)
    errors, warnings = validate_items(data)
    if errors:
        print(f"INVALID: {args.items}")
        for error in errors:
            print(f"- {error}")
        return 1

    subscriptions = active_subscriptions(data)
    monthly = sum((monthly_amount(money(row.get("金额")), str(row.get("周期") or "月")) for row in subscriptions), Decimal("0"))
    upcoming = []
    for row in subscriptions:
        renewal = parse_time(row.get("续费日"))
        if renewal is None:
            continue
        if as_of <= renewal.date() <= as_of + timedelta(days=30):
            upcoming.append(row)
    records = _load_ledger_records(args.ledger) if args.ledger else []
    missing_reimburse = []
    for row in subscriptions:
        if not (_truthy(row.get("自动续费")) and _truthy(row.get("可报销"))):
            continue
        if not args.ledger:
            missing_reimburse.append((row, "未对照流水"))
            continue
        if not has_reimbursement(row, records):
            missing_reimburse.append((row, "没有对应报销"))

    print(f"# 记物: {args.items.name}")
    print(f"日期: {as_of.isoformat()}")
    if warnings:
        print(f"warnings: {len(warnings)}")
        for warning in warnings:
            print(f"- {warning}")
    print("\n## 订阅")
    print(f"- 按月折算: {fmt(monthly)}")
    if upcoming:
        print("- 30天内续费:")
        for row in upcoming:
            print(f"  - {row.get('名称', '')} {row.get('续费日', '')} {fmt(money(row.get('金额')))}")
    else:
        print("- 30天内续费: 无")
    if missing_reimburse:
        print("- 自动续费且可报销:")
        for row, reason in missing_reimburse:
            print(f"  - {row.get('名称', '')}: {reason}")
    else:
        print("- 自动续费且可报销: 无缺失")

    holdings = data.get("holdings") or []
    held = held_rows(data)
    purchase = sum((money(row.get("购入价")) for row in held), Decimal("0"))
    residual = residual_of(data)
    daily_values = [daily_cost(row, as_of) for row in held]
    known_daily = [value for value in daily_values if value is not None]
    daily_total = sum(known_daily, Decimal("0"))
    aside = [
        row
        for row in holdings
        if isinstance(row, dict) and _status(row, "持有") in {"已卖出", "已送出"}
    ]
    print("\n## 物品")
    print(f"- 购入合计: {fmt(purchase)}")
    print(f"- 残值合计: {fmt(residual)}")
    print(f"- 使用成本/天: {fmt(daily_total)}")
    for row, cost in zip(held, daily_values):
        cost_text = fmt(cost) if cost is not None else "未知"
        print(f"- {row.get('名称', '')}: 购入 {fmt(money(row.get('购入价')))}, 残值 {fmt(money(row.get('估计残值')))}, 使用成本/天 {cost_text}")
    if aside:
        print(f"- 已卖出或已送出: {len(aside)}（不计入上面的合计）")
    print("- 不计入总资产、净资产、备查净值")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
