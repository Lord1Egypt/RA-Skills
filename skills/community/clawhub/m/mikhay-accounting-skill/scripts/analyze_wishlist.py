#!/usr/bin/env python3
"""Analyze purchase wishlist pressure and priority."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from ledgerlib import DEFAULT_ACCOUNTS, accumulate, load_skill_config


REQUIRED_FIELDS = ["名称", "预计金额", "类型", "优先级", "状态"]
PRIORITIES = {"P0", "P1", "P2", "P3"}
STATUSES = {"想买", "观望", "计划购买", "已购买", "放弃"}
ACTIVE_STATUSES = {"想买", "观望", "计划购买"}
# Fallback only: configured account kinds win.
LIABILITY_ACCOUNTS = {name for name, meta in DEFAULT_ACCOUNTS.items() if meta["kind"] == "负债"}
NEED_TYPES = {"健康", "医疗", "工作", "学习", "必需", "维修"}


def decimal_value(value: Any) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def money(value: Any) -> Decimal:
    return decimal_value(value) or Decimal("0")


def fmt(value: Decimal | None) -> str:
    if value is None:
        return "未知"
    return f"{value.quantize(Decimal('0.01'))}"


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是", "可", "可以"}


def parse_day(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def load_wishlist(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return data, []
    if isinstance(data, dict):
        items = data.get("items", data.get("wishlist", []))
        buckets = data.get("budget_buckets", [])
        if isinstance(items, list) and isinstance(buckets, list):
            return items, buckets
    raise SystemExit(f"Unsupported wishlist JSON shape: {path}")


def load_ledger(path: Path, config: Any = None) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    else:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = data.get("records", data.get("transactions", []))
        else:
            raise SystemExit(f"Unsupported ledger file: {path}")
    if config is not None:
        config.apply_to_book({"records": rows})
    return rows


def validate_items(items: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for i, item in enumerate(items, 1):
        prefix = f"wishlist[{i}]"
        for field in REQUIRED_FIELDS:
            if str(item.get(field, "")).strip() == "":
                errors.append(f"{prefix}: missing {field}")
        amount = decimal_value(item.get("预计金额"))
        if amount is None or amount <= 0:
            errors.append(f"{prefix}: 预计金额 must be positive")
        priority = str(item.get("优先级", "")).strip()
        if priority and priority not in PRIORITIES:
            errors.append(f"{prefix}: 优先级 must be P0/P1/P2/P3")
        status = str(item.get("状态", "")).strip()
        if status and status not in STATUSES:
            errors.append(f"{prefix}: invalid 状态 {status!r}")
        target = str(item.get("目标日期", "")).strip()
        if target:
            try:
                datetime.fromisoformat(target)
            except ValueError:
                errors.append(f"{prefix}: invalid 目标日期")
        if status in {"已购买", "放弃"}:
            warnings.append(f"{prefix}: 状态={status}, analysis will skip buy recommendation")
        if status == "放弃" and str(item.get("放弃原因", "")).strip() == "":
            warnings.append(f"{prefix}: 放弃需要填写放弃原因")
        if status == "已购买" and str(item.get("record_id", "")).strip() == "":
            warnings.append(f"{prefix}: 已购买缺少 record_id")
        if str(item.get("加入日期", "")).strip() == "":
            warnings.append(f"{prefix}: 缺少加入日期，暂用文件里最早的日期")
        raw_cool = item.get("冷静天数", "")
        if str(raw_cool).strip() != "":
            try:
                cool = int(raw_cool)
            except (TypeError, ValueError):
                errors.append(f"{prefix}: 冷静天数 must be an integer")
            else:
                if cool < 0:
                    errors.append(f"{prefix}: 冷静天数 cannot be negative")
        raw_target = item.get("目标价", "")
        if str(raw_target).strip() != "":
            target_price = decimal_value(raw_target)
            if target_price is None or target_price < 0:
                errors.append(f"{prefix}: 目标价 must be a non-negative number")
        joined = str(item.get("加入日期", "")).strip()
        if joined and parse_day(joined) is None:
            errors.append(f"{prefix}: invalid 加入日期")
    return errors, warnings


def validate_buckets(buckets: list[dict[str, Any]], items: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    names: set[str] = set()
    for index, bucket in enumerate(buckets, 1):
        prefix = f"budget_bucket[{index}]"
        name = str(bucket.get("名称", "")).strip()
        if not name:
            errors.append(f"{prefix}: missing 名称")
            continue
        if name in names:
            errors.append(f"{prefix}: duplicate bucket {name}")
        names.add(name)
        limit = decimal_value(bucket.get("额度"))
        if limit is None or limit < 0:
            errors.append(f"{prefix}: 额度 must be a non-negative number")
        for field in ("起", "止"):
            raw = str(bucket.get(field, "")).strip()
            if raw and parse_day(raw) is None:
                errors.append(f"{prefix}: invalid {field}")
    for index, item in enumerate(items, 1):
        bucket_name = str(item.get("额度桶", "")).strip()
        if bucket_name and bucket_name not in names:
            warnings.append(f"wishlist[{index}]: 未知额度桶 {bucket_name}")
    return errors, warnings


def ledger_context(
    paths: list[Path],
    config: Any = None,
) -> tuple[Decimal | None, Decimal, Decimal, Decimal, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    if not paths:
        return None, Decimal("0"), Decimal("0"), Decimal("0"), rows
    for path in paths:
        rows.extend(load_ledger(path, config))
    flows = accumulate(
        rows,
        config.catalog if config is not None else None,
        config.categories if config is not None else None,
        config.invest_out_subcategory if config is not None else "赎回",
    )
    expense = flows.expense_net
    surplus = flows.income - expense - flows.repayment - flows.investment_net
    return surplus, flows.income, expense, flows.repayment, rows


def asset_context(path: Path | None, config: Any = None) -> tuple[Decimal | None, Decimal | None, Decimal | None]:
    if path is None:
        return None, None, None
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        return None, None, None
    if config is not None:
        config.apply_to_book(data)
    assets: dict[str, Decimal] = {}
    liabilities: dict[str, Decimal] = {}
    for row in data.get("asset_snapshots", []):
        account = str(row.get("账户", "")).strip()
        amount = money(row.get("金额"))
        kind = str(row.get("账户类型", "")).strip()
        if not kind and config is not None:
            kind = config.catalog.get(account, {}).get("kind", "")
        if kind == "负债" or account in LIABILITY_ACCOUNTS:
            liabilities[account] = abs(amount)
        else:
            assets[account] = amount
    for row in data.get("credit_accounts", []):
        account = str(row.get("账户", "")).strip()
        liabilities[account] = abs(money(row.get("欠款")))
    asset_total = sum(assets.values(), Decimal("0"))
    liability_total = sum(liabilities.values(), Decimal("0"))
    return asset_total - liability_total, asset_total, liability_total


def pressure(amount: Decimal, surplus: Decimal | None, net_assets: Decimal | None) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if surplus is None and net_assets is None:
        return "未知", ["缺少账本或资产上下文"]
    if surplus is not None:
        if surplus <= 0:
            reasons.append("月现金流为负或为零")
            return "高", reasons
        ratio = amount / surplus
        if ratio >= Decimal("1.5"):
            reasons.append("预计金额超过 1.5 个月现金流结余")
            return "高", reasons
        if ratio >= Decimal("0.5"):
            reasons.append("预计金额超过半个月现金流结余")
            return "中", reasons
    if net_assets is not None:
        if net_assets <= 0:
            reasons.append("净资产为负或为零")
            return "高", reasons
        ratio = amount / net_assets
        if ratio >= Decimal("0.20"):
            reasons.append("预计金额超过净资产 20%")
            return "高", reasons
        if ratio >= Decimal("0.10"):
            reasons.append("预计金额超过净资产 10%")
            return "中", reasons
    return "低", reasons or ["金额相对现金流和净资产可控"]


def suggested_priority(item: dict[str, Any], pressure_level: str) -> str:
    priority = str(item.get("优先级", "")).strip()
    item_type = str(item.get("类型", "")).strip()
    deferrable = truthy(item.get("可延期", False))
    if priority == "P0":
        return "P0"
    if priority == "P1" and (item_type in NEED_TYPES or not deferrable):
        return "P1"
    if item_type in NEED_TYPES and pressure_level != "高":
        return "P1"
    if item_type in NEED_TYPES:
        return "P2"
    if pressure_level == "高":
        return "P3" if deferrable else "P2"
    if pressure_level == "中":
        return priority if priority in {"P1", "P2"} else "P2"
    return priority or "P2"


def recommendation(item: dict[str, Any], pressure_level: str, priority: str) -> tuple[str, str]:
    status = str(item.get("状态", "")).strip()
    if status == "已购买":
        return "已购买", "无需重复购买"
    if status == "放弃":
        return "不建议", "已标记放弃"
    deferrable = truthy(item.get("可延期", False))
    if priority in {"P0", "P1"} and pressure_level != "高":
        return "建议", "必要性较高且压力可控"
    if pressure_level == "高":
        return "不建议" if deferrable else "观望", "经济压力较高"
    if pressure_level == "中":
        return "观望", "建议等现金流更充裕或降价"
    if deferrable and priority == "P3":
        return "观望", "可延期且优先级较低"
    return "建议", "压力较低"


def cooling_days(item: dict[str, Any]) -> int:
    raw = item.get("冷静天数", "")
    if str(raw).strip() == "":
        return 0 if str(item.get("优先级", "")).strip() == "P0" else 7
    return int(raw)


def file_origin(items: list[dict[str, Any]], buckets: list[dict[str, Any]]) -> date | None:
    found: list[date] = []
    for item in items:
        for field in ("加入日期", "目标日期"):
            parsed = parse_day(item.get(field))
            if parsed is not None:
                found.append(parsed)
    for bucket in buckets:
        for field in ("起", "止"):
            parsed = parse_day(bucket.get(field))
            if parsed is not None:
                found.append(parsed)
    return min(found) if found else None


def cooling_end(item: dict[str, Any], origin: date | None) -> date | None:
    start = parse_day(item.get("加入日期")) or origin
    if start is None:
        return None
    return start + timedelta(days=cooling_days(item))


def cooling_remaining(item: dict[str, Any], as_of: date, origin: date | None) -> int:
    if cooling_days(item) <= 0:
        return 0
    end = cooling_end(item, origin)
    if end is None or as_of >= end:
        return 0
    return (end - as_of).days


def bucket_is_open(bucket: dict[str, Any], as_of: date) -> bool:
    start = parse_day(bucket.get("起"))
    stop = parse_day(bucket.get("止"))
    if start is not None and as_of < start:
        return False
    if stop is not None and as_of > stop:
        return False
    return True


def bucket_remaining(
    bucket: dict[str, Any],
    items: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> tuple[Decimal, Decimal]:
    name = str(bucket.get("名称", "")).strip()
    limit = money(bucket.get("额度"))
    ids = {
        str(item.get("record_id", "")).strip()
        for item in items
        if str(item.get("额度桶", "")).strip() == name
        and str(item.get("状态", "")).strip() == "已购买"
        and str(item.get("record_id", "")).strip()
    }
    used = Decimal("0")
    for row in records:
        if str(row.get("id", "")).strip() not in ids:
            continue
        if str(row.get("收支类型", "")).strip() != "支出":
            continue
        used += abs(money(row.get("金额")))
    return limit, limit - used


def suggested_time(decision: str, pressure_level: str) -> str:
    if decision == "建议":
        return "现在或目标日期前"
    if pressure_level == "高":
        return "还款后或现金流转正后"
    if pressure_level == "中":
        return "下月或降价后"
    return "目标日期前"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze purchase wishlist pressure and priority.")
    parser.add_argument("wishlist", type=Path)
    parser.add_argument("--ledger", action="append", type=Path, default=[], help="Ledger CSV/JSON file. Can be repeated.")
    parser.add_argument("--assets", type=Path, help="Assets JSON file.")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--as-of", help="Date for the cooling-off clock, YYYY-MM-DD. Default: today.")
    parser.add_argument("--due", action="store_true", help="Print wishes whose cooling-off period has ended.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()
    if args.as_of:
        as_of = parse_day(args.as_of)
        if as_of is None:
            raise SystemExit("--as-of must be YYYY-MM-DD")
    else:
        as_of = date.today()

    config = load_skill_config(
        [args.wishlist, *args.ledger] + ([args.assets] if args.assets else []),
        args.accounts,
        args.categories,
        args.settings,
    )
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    items, buckets = load_wishlist(args.wishlist)
    errors, warnings = validate_items(items)
    bucket_errors, bucket_warnings = validate_buckets(buckets, items)
    errors.extend(bucket_errors)
    warnings.extend(bucket_warnings)
    if errors:
        print(f"INVALID: {args.wishlist}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {args.wishlist}")
    print(f"items: {len(items)}")
    if warnings:
        print(f"warnings: {len(warnings)}")
        for warning in warnings[:20]:
            print(f"- {warning}")
    origin = file_origin(items, buckets)
    if args.due:
        print("\n## 冷静期到期")
        due_rows = []
        for item in items:
            if str(item.get("状态", "")).strip() not in ACTIVE_STATUSES:
                continue
            if cooling_days(item) <= 0:
                continue
            end = cooling_end(item, origin)
            if end is not None and end <= as_of:
                due_rows.append((end, item))
        if not due_rows:
            print("- 无")
        for end, item in sorted(due_rows, key=lambda pair: (pair[0], str(pair[1].get("名称", "")))):
            print(f"- {item.get('名称', '')}: 冷静期至 {end.isoformat()}，已到期")
        return 0

    if args.validate_only:
        return 0

    surplus, income, expense, repayment, records = ledger_context(args.ledger, config)
    net_assets, asset_total, liability_total = asset_context(args.assets, config)

    print("\n## 财务上下文")
    print(f"- 月现金流结余: {fmt(surplus)}")
    print(f"- 收入/支出/还款: {fmt(income)} / {fmt(expense)} / {fmt(repayment)}")
    print(f"- 总资产/总负债/净资产: {fmt(asset_total)} / {fmt(liability_total)} / {fmt(net_assets)}")
    open_buckets = [bucket for bucket in buckets if bucket_is_open(bucket, as_of)]
    bucket_limits = {str(bucket.get("名称", "")).strip(): bucket_remaining(bucket, items, records) for bucket in open_buckets}
    if bucket_limits:
        print("\n## 额度桶")
        for name, (limit, remaining_limit) in bucket_limits.items():
            print(f"- {name}: 额度 {fmt(limit)}, 已用 {fmt(limit - remaining_limit)}, 剩余 {fmt(remaining_limit)}")

    print("\n## 预购建议")
    active_items = [item for item in items if str(item.get("状态", "")).strip() in ACTIVE_STATUSES]
    rows = []
    for item in active_items:
        amount = money(item.get("预计金额"))
        pressure_level, reasons = pressure(amount, surplus, net_assets)
        priority = suggested_priority(item, pressure_level)
        remaining_days = cooling_remaining(item, as_of, origin)
        bucket_name = str(item.get("额度桶", "")).strip()
        over_bucket = False
        if bucket_name in bucket_limits:
            _, remaining_limit = bucket_limits[bucket_name]
            over_bucket = amount > remaining_limit
        if remaining_days > 0:
            decision = f"观望（冷静期剩 {remaining_days} 天）"
            decision_reason = "冷静期未结束"
        elif over_bucket:
            decision = "不建议"
            decision_reason = "超出额度桶剩余额度"
        else:
            decision, decision_reason = recommendation(item, pressure_level, priority)
        target_price = decimal_value(item.get("目标价"))
        if target_price is not None and target_price < amount:
            decision_reason = f"{decision_reason}；等降价"
        rows.append((priority, pressure_level, item, decision, decision_reason, reasons))

    pressure_order = {"高": 0, "中": 1, "低": 2, "未知": 3}
    rows.sort(key=lambda row: (row[0], pressure_order.get(row[1], 9), str(row[2].get("名称", ""))))
    for priority, pressure_level, item, decision, decision_reason, reasons in rows:
        name = item.get("名称", "")
        amount = money(item.get("预计金额"))
        when = suggested_time(decision, pressure_level)
        reason_text = "；".join([decision_reason, *reasons])
        print(f"- {name}: {fmt(amount)}，{decision}，压力={pressure_level}，优先级={priority}，建议时间={when}，原因={reason_text}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
