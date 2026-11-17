#!/usr/bin/env python3
"""Read-only lint for near-duplicates, alias drift, and missing fixed expenses.

Does not modify any ledger file. Exact duplicates stay validate errors; this
script only warns. A scheduled run is the host agent's job, not this script.
"""

from __future__ import annotations

import argparse
import calendar
import json
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from ledgerlib import (
    CategoryCatalog,
    decimal_value,
    default_account_catalog,
    find_optional_data_file,
    iter_ledger_files,
    load_file,
    load_skill_config,
    merge_account_policy,
    money,
    parse_time,
    reimburse_ref,
    reimburse_status,
    resolve_account,
    target_account,
)
from validate_ledger import validate_records


def _blank(value: Any) -> bool:
    return str(value if value is not None else "").strip() == ""


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _as_list(data: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        rows = data.get(key, data.get("items", []))
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def notes_similar(left: str, right: str) -> bool:
    def norm(text: str) -> str:
        return "".join(text.split()).casefold()

    a, b = norm(left), norm(right)
    if len(a) < 2 or len(b) < 2:
        return False
    if a == b or a in b or b in a:
        return True
    return SequenceMatcher(None, a, b).ratio() >= 0.75


def near_duplicates(rows: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    indexed: list[tuple[int, dict[str, Any], date, Decimal]] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        stamp = parse_time(row.get("时间"))
        amount = decimal_value(row.get("金额"))
        if stamp is None or amount is None:
            continue
        indexed.append((index, row, stamp.date(), abs(amount)))
    for left in range(len(indexed)):
        i, row, day, amount = indexed[left]
        for j, other, other_day, other_amount in indexed[left + 1 :]:
            if str(row.get("账户", "")).strip() != str(other.get("账户", "")).strip():
                continue
            if amount != other_amount:
                continue
            if abs((day - other_day).days) > 2:
                continue
            same_note = str(row.get("备注", "")).strip() == str(other.get("备注", "")).strip()
            same_type = str(row.get("收支类型", "")).strip() == str(other.get("收支类型", "")).strip()
            if day == other_day and same_note and same_type and str(row.get("时间", "")).strip() == str(other.get("时间", "")).strip():
                continue
            if not notes_similar(str(row.get("备注", "")), str(other.get("备注", ""))):
                continue
            warnings.append(
                f"近似重复 record[{i}] 与 record[{j}]：账户 {row.get('账户', '')}，金额 {amount}，备注相近"
            )
    return warnings


def configured_alias_windows(catalog: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Alias history lives with the account definition, not in a second file."""
    rows: list[dict[str, Any]] = []
    for account, meta in catalog.items():
        for window in meta.get("alias_windows") or []:
            if not isinstance(window, dict):
                continue
            name = str(window.get("名称", "") or "").strip()
            if not name:
                continue
            rows.append(
                {
                    "名称": name,
                    "含义": str(window.get("含义", "") or "").strip(),
                    "起": str(window.get("起", "") or "").strip(),
                    "止": str(window.get("止", "") or "").strip(),
                    "账户": account,
                }
            )
    return rows


def _in_window(day: date, row: dict[str, Any]) -> bool:
    start = parse_time(row.get("起"))
    stop = parse_time(row.get("止"))
    if start is not None and day < start.date():
        return False
    if stop is not None and day > stop.date():
        return False
    return True


def alias_warnings(
    rows: list[dict[str, Any]],
    windows: list[dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
) -> list[str]:
    warnings: list[str] = []
    known_names = {str(row.get("名称", "")).strip() for row in windows if str(row.get("名称", "")).strip()}
    known_names |= {str(row.get("含义", "")).strip() for row in windows if str(row.get("含义", "")).strip()}
    seen_accounts: set[str] = set()
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        account = str(row.get("账户", "")).strip()
        resolved = resolve_account(account, catalog) if account else ""
        note = str(row.get("备注", "")).strip()
        stamp = parse_time(row.get("时间"))
        day = stamp.date() if stamp else None
        for alias in windows:
            name = str(alias.get("名称", "")).strip()
            if not name or day is None:
                continue
            used = account == name or name in account or name in note
            if used and not _in_window(day, alias):
                meaning = str(alias.get("含义", "")).strip() or name
                warnings.append(
                    f"record[{index}]: 别名 {name}（{meaning}）用在生效区间外 {day.isoformat()}"
                )
        if resolved and resolved not in catalog and resolved not in known_names and resolved not in seen_accounts:
            seen_accounts.add(resolved)
            warnings.append(f"record[{index}]: 新账户 {account}")
    return warnings


def _spec_from_recurring(row: dict[str, Any]) -> dict[str, Any] | None:
    low = row.get("金额下限", row.get("最小金额", row.get("金额", "")))
    high = row.get("金额上限", row.get("最大金额", row.get("金额", "")))
    if _blank(low) or _blank(high):
        return None
    return {
        "名称": str(row.get("名称", "")).strip() or "固定支出",
        "账户": str(row.get("账户", "")).strip(),
        "最小": abs(money(low)),
        "最大": abs(money(high)),
        "周期": str(row.get("周期", "")).strip() or "月",
        "日": int(row.get("日")) if str(row.get("日", "")).strip().isdigit() else None,
        "id": "",
        "来源": "recurring",
    }


def _spec_from_subscription(row: dict[str, Any]) -> dict[str, Any] | None:
    if str(row.get("状态", "")).strip() not in {"", "active"}:
        return None
    if str(row.get("状态", "")).strip() == "已取消":
        return None
    if _blank(row.get("金额")):
        return None
    renewal = parse_time(row.get("续费日"))
    day = renewal.day if renewal else None
    amount = abs(money(row.get("金额")))
    return {
        "名称": str(row.get("名称", "")).strip() or str(row.get("id", "")).strip() or "订阅",
        "账户": str(row.get("扣款账户", "")).strip(),
        "最小": amount,
        "最大": amount,
        "周期": str(row.get("周期", "")).strip() or "月",
        "日": day,
        "id": str(row.get("id", "")).strip(),
        "来源": "subscription",
    }


def load_fixed(recurring: Path | None, items: Path | None) -> tuple[list[dict[str, Any]], list[str]]:
    specs: list[dict[str, Any]] = []
    warnings: list[str] = []
    if recurring is not None and recurring.exists():
        try:
            data = _load_json(recurring)
        except json.JSONDecodeError as exc:
            warnings.append(f"recurring: invalid JSON: {exc}")
        else:
            for row in _as_list(data, "items"):
                spec = _spec_from_recurring(row)
                if spec is None:
                    warnings.append(f"recurring: {row.get('名称', '')} 缺少金额范围")
                else:
                    specs.append(spec)
    if items is not None and items.exists():
        try:
            data = _load_json(items)
        except json.JSONDecodeError as exc:
            warnings.append(f"items: invalid JSON: {exc}")
        else:
            rows = data.get("subscriptions", []) if isinstance(data, dict) else []
            for row in rows if isinstance(rows, list) else []:
                if not isinstance(row, dict):
                    continue
                spec = _spec_from_subscription(row)
                if spec is not None:
                    specs.append(spec)
    return specs, warnings


def _matches_fixed(row: dict[str, Any], spec: dict[str, Any]) -> bool:
    if str(row.get("收支类型", "")).strip() != "支出":
        return False
    item_id = str(row.get("item_id", "")).strip()
    if spec["id"] and item_id == spec["id"]:
        return True
    amount = abs(money(row.get("金额")))
    if amount < spec["最小"] or amount > spec["最大"]:
        return False
    account = str(row.get("账户", "")).strip()
    expected_account = spec["账户"]
    note = str(row.get("备注", "")).strip()
    if expected_account and account == expected_account:
        return True
    if spec["来源"] == "subscription" and spec["名称"] and spec["名称"] in note:
        return True
    return not expected_account and spec["来源"] != "subscription"


def _month_key(day: date) -> str:
    return f"{day.year:04d}-{day.month:02d}"


def _iter_months(start: date, end: date) -> list[date]:
    cursor = date(start.year, start.month, 1)
    last = date(end.year, end.month, 1)
    months: list[date] = []
    while cursor <= last:
        months.append(cursor)
        year = cursor.year + (1 if cursor.month == 12 else 0)
        month = 1 if cursor.month == 12 else cursor.month + 1
        cursor = date(year, month, 1)
    return months


def _cycle_keys(spec: dict[str, Any], start: date, end: date) -> list[str]:
    cycle = spec["周期"]
    keys: list[str] = []
    if cycle == "周":
        seen: set[tuple[int, int]] = set()
        cursor = start
        while cursor <= end:
            iso = cursor.isocalendar()
            token = (iso.year, iso.week)
            if token not in seen:
                seen.add(token)
                keys.append(f"{iso.year}-W{iso.week:02d}")
            cursor += timedelta(days=1)
        return keys
    if cycle == "年":
        return [str(year) for year in range(start.year, end.year + 1)]
    if cycle == "季":
        seen_q: set[str] = set()
        for month_start in _iter_months(start, end):
            quarter = (month_start.month - 1) // 3 + 1
            key = f"{month_start.year}-Q{quarter}"
            if key not in seen_q:
                seen_q.add(key)
                keys.append(key)
        return keys
    return [_month_key(month_start) for month_start in _iter_months(start, end)]


def _row_cycle_key(spec: dict[str, Any], day: date) -> str:
    cycle = spec["周期"]
    if cycle == "周":
        iso = day.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    if cycle == "年":
        return str(day.year)
    if cycle == "季":
        return f"{day.year}-Q{(day.month - 1) // 3 + 1}"
    return _month_key(day)


def missing_fixed(rows: list[dict[str, Any]], specs: list[dict[str, Any]], as_of: date) -> tuple[list[str], dict[str, set[str]]]:
    warnings: list[str] = []
    dated: list[tuple[dict[str, Any], date]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        stamp = parse_time(row.get("时间"))
        if stamp is not None:
            dated.append((row, stamp.date()))
    hits: dict[str, set[str]] = defaultdict(set)
    if not dated or not specs:
        return warnings, hits
    start = min(day for _, day in dated)
    end = min(max(day for _, day in dated), as_of)
    if end < start:
        return warnings, hits
    for spec in specs:
        found: set[str] = set()
        for row, day in dated:
            if day > as_of:
                continue
            if _matches_fixed(row, spec):
                found.add(_row_cycle_key(spec, day))
                hits[_month_key(day)].add(spec["名称"])
        for key in _cycle_keys(spec, start, end):
            if key not in found:
                day_text = f"，预计每月 {spec['日']} 日" if spec["日"] and spec["周期"] == "月" else ""
                warnings.append(f"固定支出缺月 {spec['名称']} {key}{day_text}")
    return warnings, hits


def flow_warnings(rows: list[dict[str, Any]], as_of: date) -> list[str]:
    warnings: list[str] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        tx_type = str(row.get("收支类型", "")).strip()
        if tx_type == "还款" and not target_account(row):
            warnings.append(f"record[{index}]: 还款没有 target_account")
        if tx_type == "报销" and not reimburse_ref(row):
            warnings.append(f"record[{index}]: 报销没有 reimburse_of")
    return warnings


def _pending_text(row: dict[str, Any]) -> bool:
    text = f"{row.get('备注', '')} {row.get('note', '')}"
    return "待确认" in text


def coverage_lines(
    rows: list[dict[str, Any]],
    specs: list[dict[str, Any]],
    hits: dict[str, set[str]],
    as_of: date,
) -> list[str]:
    by_month: dict[str, list[dict[str, Any]]] = defaultdict(list)
    undated: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        stamp = parse_time(row.get("时间"))
        if stamp is None:
            undated.append(row)
            continue
        by_month[_month_key(stamp.date())].append(row)
    lines: list[str] = []
    total = len(specs)
    for key in sorted(by_month):
        month_rows = by_month[key]
        year, month = (int(part) for part in key.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        end_day = as_of.day if as_of.year == year and as_of.month == month else last_day
        occupied = {parse_time(row.get("时间")).day for row in month_rows if parse_time(row.get("时间"))}
        blank = 0
        longest = 0
        for day in range(1, end_day + 1):
            if day in occupied:
                longest = max(longest, blank)
                blank = 0
            else:
                blank += 1
        longest = max(longest, blank)
        confirmed = sum(1 for row in month_rows if _pending_text(row))
        hit_count = len(hits.get(key, set()))
        lines.append(
            f"- {key}: 记录 {len(month_rows)}, 有记录天数 {len(occupied)}, 最长连续空白 {longest} 天, "
            f"时间为空 0, 待确认 {confirmed}, 固定支出 {hit_count}/{total}"
        )
    if undated:
        confirmed = sum(1 for row in undated if _pending_text(row))
        lines.append(
            f"- 无时间: 记录 {len(undated)}, 有记录天数 0, 最长连续空白 0 天, "
            f"时间为空 {len(undated)}, 待确认 {confirmed}, 固定支出 0/{total}"
        )
    if not lines:
        lines.append("- 无记录")
    return lines


def collect_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(iter_ledger_files(path))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only lint for a Chinese personal ledger.")
    parser.add_argument("paths", nargs="+", type=Path, help="Ledger files or directories.")
    parser.add_argument("--recurring", type=Path, help="Fixed expenses. Default: data/recurring.json when that file exists.")
    parser.add_argument("--items", type=Path, help="Subscriptions file. Default: data/items/items.json when that file exists.")
    parser.add_argument("--as-of", help="Age pending reimbursements and fixed expenses as of YYYY-MM-DD. Default: today.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()
    if args.as_of:
        parsed = parse_time(args.as_of)
        if parsed is None:
            raise SystemExit("--as-of must be YYYY-MM-DD")
        as_of = parsed.date()
    else:
        as_of = date.today()

    recurring_path = args.recurring
    if recurring_path is None:
        recurring_path = find_optional_data_file("recurring.json", args.paths)
    items_path = args.items
    if items_path is None:
        items_path = find_optional_data_file("items.json", args.paths)
        if items_path is None:
            items_path = find_optional_data_file("items/items.json", args.paths)

    files = collect_files(args.paths)
    if not files:
        raise SystemExit("no ledger files found")
    config = load_skill_config(args.paths, args.accounts, args.categories, args.settings)
    rows: list[dict[str, Any]] = []
    errors: list[str] = list(config.errors)
    catalog: dict[str, dict[str, Any]] = {}
    for path in files:
        book, load_errors = load_file(path)
        if not book.get("is_ledger", True):
            continue
        if load_errors:
            errors.extend(f"{path}: {item}" for item in load_errors)
        merged, policy_errors = merge_account_policy(book.get("account_policy") or [], base=config.catalog)
        catalog.update(merged)
        errors.extend(policy_errors)
        rows.extend(row for row in book.get("records") or [] if isinstance(row, dict))
    if not catalog:
        catalog = default_account_catalog()

    categories: CategoryCatalog = config.categories
    aliases = configured_alias_windows(catalog)
    specs, fixed_load_warnings = load_fixed(recurring_path, items_path)
    _, validate_warnings = validate_records(
        rows,
        max_date=as_of + timedelta(days=366),
        strict_refs=len(files) > 1,
        catalog=catalog,
        categories=categories,
        base_currency=config.base_currency,
    )
    missing, hits = missing_fixed(rows, specs, as_of)
    warnings = [
        *fixed_load_warnings,
        *validate_warnings,
        *near_duplicates(rows),
        *alias_warnings(rows, aliases, catalog),
        *missing,
        *flow_warnings(rows, as_of),
    ]
    label = files[0] if len(files) == 1 else f"{len(files)} files"
    if errors:
        print(f"LINT INVALID: {label}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"LINT: {label}")
    print(f"records: {len(rows)}")
    print(f"warnings: {len(warnings)}")
    for warning in warnings:
        print(f"- {warning}")
    print("\n## 月度覆盖")
    for line in coverage_lines(rows, specs, hits, as_of):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
