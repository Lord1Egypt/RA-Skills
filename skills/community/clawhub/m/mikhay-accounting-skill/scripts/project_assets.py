#!/usr/bin/env python3
"""Rebuild inferred asset balances from observed snapshots and later ledger items.

Method A (default) starts at the latest observed snapshot and applies later
records. Method B replays credit-card accounts from zero and ignores their
snapshots. Accounts with no observed baseline stay out of the totals.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import (
    CC_METHOD_A,
    CC_METHOD_B,
    CREDIT_CARDS,
    DEFAULT_ACCOUNTS,
    SCHEMA_VERSION,
    SkillConfig,
    apply_account_aliases,
    default_account_catalog,
    is_refund,
    json_money,
    load_file,
    load_skill_config,
    money,
    pair_id,
    parse_time,
    target_account,
)


# Fallback only: configured account kinds win. These names come from the starter catalog.
LIABILITY_ACCOUNTS = {name for name, meta in DEFAULT_ACCOUNTS.items() if meta["kind"] == "负债"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_records(paths: list[Path], config: SkillConfig | None = None) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        book, errors = load_file(path)
        if errors and not book["records"]:
            raise SystemExit(errors[0])
        if config is not None:
            config.apply_to_book(book)
        records.extend(row for row in book["records"] if isinstance(row, dict))
    return records


def _apply_delta(tx_type: str, amount: Decimal, account: str, target: str, row: dict[str, Any]) -> list[tuple[str, Decimal]]:
    magnitude = abs(amount)
    if is_refund(row) or tx_type == "报销":
        return [(account, magnitude)]
    if tx_type == "支出":
        return [(account, -magnitude)]
    if tx_type == "收入":
        return [(account, magnitude)]
    if tx_type == "还款":
        deltas = [(account, -magnitude)]
        if target:
            deltas.append((target, magnitude))
        return deltas
    if tx_type == "转账":
        if pair_id(row):
            # Each leg posts to its own account. Counting the paired leg again
            # would double the move.
            return [(account, amount)]
        if target:
            return [(account, -magnitude), (target, magnitude)]
    if tx_type == "投资":
        if pair_id(row):
            return [(account, amount)]
        if target:
            return [(account, amount), (target, -amount)]
        return [(account, amount)]
    return []


def project(
    asset_data: dict[str, Any],
    records: list[dict[str, Any]],
    as_of: datetime | None,
    *,
    cc_method: str = "A",
    catalog: dict[str, dict[str, Any]] | None = None,
    credit_cards: set[str] | None = None,
) -> dict[str, Any]:
    latest: dict[str, dict[str, Any]] = {}
    latest_time: dict[str, datetime] = {}
    for row in asset_data.get("asset_snapshots", []):
        account = str(row.get("账户", "")).strip()
        stamp = parse_time(row.get("时间"))
        if not account or stamp is None or (as_of and stamp > as_of):
            continue
        if account not in latest_time or stamp >= latest_time[account]:
            latest[account] = row
            latest_time[account] = stamp

    source = catalog if catalog is not None else default_account_catalog()
    catalog = {name: dict(meta) for name, meta in source.items()}
    for row in asset_data.get("account_policy", []) or []:
        name = str(row.get("账户", "")).strip()
        if not name:
            continue
        kind = str(row.get("账户类型", "")).strip()
        if name not in catalog:
            catalog[name] = {"kind": kind or "资产", "include": "included", "credit": False, "aliases": []}
        elif kind:
            catalog[name]["kind"] = kind

    balances: dict[str, Decimal] = {}
    kinds: dict[str, str] = {}
    for account, row in latest.items():
        balances[account] = money(row.get("余额", row.get("金额", 0)))
        explicit = str(row.get("账户类型", "")).strip()
        kinds[account] = explicit or catalog.get(account, {}).get("kind") or ("负债" if account in LIABILITY_ACCOUNTS else "资产")

    if cc_method.upper() == "B":
        declared = {str(row.get("账户", "")).strip() for row in asset_data.get("credit_accounts", [])}
        cards = credit_cards if credit_cards is not None else CREDIT_CARDS
        card_names = {name for name in balances if name in cards or name in declared}
        card_names |= {name for name in declared if name}
        for name in card_names:
            balances[name] = Decimal("0")
            latest_time[name] = datetime.fromisoformat("1970-01-01 00:00")
            kinds[name] = "负债"

    unknown: set[str] = set()
    applied: set[int] = set()
    valid_records: list[tuple[datetime, int, dict[str, Any]]] = []
    for index, row in enumerate(records):
        stamp = parse_time(row.get("时间"))
        if stamp is not None and (as_of is None or stamp <= as_of):
            valid_records.append((stamp, index, row))
    valid_records.sort(key=lambda item: (item[0], item[1]))

    def apply(account: str, delta: Decimal, stamp: datetime, record_index: int) -> None:
        if not account:
            return
        if account not in balances:
            unknown.add(account)
            return
        if stamp > latest_time[account]:
            balances[account] += delta
            applied.add(record_index)

    for stamp, record_index, row in valid_records:
        account = str(row.get("账户", "")).strip()
        tx_type = str(row.get("收支类型", "")).strip()
        amount = money(row.get("金额"))
        target = target_account(row)
        for name, delta in _apply_delta(tx_type, amount, account, target, row):
            apply(name, delta, stamp, record_index)

    rows = []
    total_assets = Decimal("0")
    total_liabilities = Decimal("0")
    for account in sorted(balances):
        balance = balances[account]
        kind = kinds[account]
        rows.append(
            {
                "账户": account,
                "账户类型": kind,
                "余额": json_money(balance),
                "基准快照时间": latest_time[account].isoformat(sep=" ", timespec="minutes"),
            }
        )
        if kind == "负债":
            total_liabilities += max(-balance, Decimal("0"))
        else:
            total_assets += balance

    candidates = [*latest_time.values(), *(stamp for stamp, _, _ in valid_records)]
    inferred_time = as_of or (max(candidates) if candidates else datetime.now())
    method = CC_METHOD_B if cc_method.upper() == "B" else CC_METHOD_A
    return {
        "schema_version": SCHEMA_VERSION,
        "时间": inferred_time.isoformat(sep=" ", timespec="minutes"),
        "类型": "推理",
        "信用卡余额算法": method,
        "账户余额": rows,
        "总资产": json_money(total_assets),
        "总负债": json_money(total_liabilities),
        "净资产": json_money(total_assets - total_liabilities),
        "应用记账数": len(applied),
        "未建立基线账户": sorted(unknown),
    }


def parse_cutoff(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if len(text) == 10:
        text = f"{text} 23:59"
    parsed = parse_time(text)
    if parsed is None:
        raise SystemExit("--as-of must be an ISO date or datetime")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild inferred asset snapshot.")
    parser.add_argument("assets", type=Path)
    parser.add_argument("ledger", nargs="*", type=Path)
    parser.add_argument("--as-of", help="Inference cutoff in ISO date or datetime format.")
    parser.add_argument("--cc-method", choices=["A", "B", "a", "b"], default="A", help="Credit-card snapshot method. Default: A.")
    parser.add_argument("--write", action="store_true", help="Replace inferred_snapshot in the asset file.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()

    config = load_skill_config([args.assets, *args.ledger], args.accounts, None, args.settings)
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    asset_data = load_json(args.assets)
    if not isinstance(asset_data, dict):
        raise SystemExit("Assets file must be a JSON object")
    config.apply_to_book(asset_data)
    records = list(asset_data.get("records", []))
    records.extend(load_records(args.ledger, config))
    inferred = project(
        asset_data,
        records,
        parse_cutoff(args.as_of),
        cc_method=args.cc_method.upper(),
        catalog=config.catalog,
        credit_cards=config.credit_cards,
    )
    if args.write:
        asset_data["inferred_snapshot"] = inferred
        asset_data.setdefault("schema_version", SCHEMA_VERSION)
        args.assets.write_text(json.dumps(asset_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"updated {args.assets}")
    print(json.dumps(inferred, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
