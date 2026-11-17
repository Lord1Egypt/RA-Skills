#!/usr/bin/env python3
"""Persist user-confirmed activity classifications and build portfolio_activity.v2."""

from __future__ import annotations

import argparse
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .policy_store import default_state_root, locked, user_key
except ImportError:
    from policy_store import default_state_root, locked, user_key


ACTIVITY_SCHEMA = "portfolio_activity.v2"
CLASSIFICATION_SCHEMA = "activity_classification.v1"
KINDS = {"PROTECTIVE_SELL", "RISK_OFF_REENTRY"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def classification_paths(root: Path, key: str) -> tuple[Path, Path]:
    directory = root / "users" / key
    return directory / "activity-classifications.jsonl", directory / ".activity-lock"


def load_classifications(root: Path, key: str) -> list[dict[str, Any]]:
    path, _ = classification_paths(root, key)
    if not path.exists():
        return []
    values: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict) or value.get("schemaVersion") != CLASSIFICATION_SCHEMA:
            raise ValueError(f"invalid classification at line {line_number}")
        values.append(value)
    return values


def append_classification(
    root: Path,
    key: str,
    *,
    event_id: str,
    kind: str,
    trade_date: str,
    transaction_ids: list[str],
    reason: str,
    user_confirmed: bool,
) -> dict[str, Any]:
    normalized_event_id = str(event_id or "").strip()
    normalized_kind = str(kind or "").strip()
    normalized_reason = str(reason or "").strip()
    normalized_transactions = list(dict.fromkeys(str(item or "").strip() for item in transaction_ids))
    if not user_confirmed:
        raise ValueError("explicit user confirmation is required")
    if not normalized_event_id:
        raise ValueError("event_id is required")
    if normalized_kind not in KINDS:
        raise ValueError("kind must be PROTECTIVE_SELL or RISK_OFF_REENTRY")
    try:
        date.fromisoformat(trade_date)
    except ValueError as exc:
        raise ValueError("trade_date must be YYYY-MM-DD") from exc
    if not normalized_transactions or any(not item for item in normalized_transactions):
        raise ValueError("at least one non-empty transaction_id is required")
    if not normalized_reason:
        raise ValueError("reason is required")

    path, lock_path = classification_paths(root, key)
    with locked(lock_path):
        existing = load_classifications(root, key)
        if normalized_event_id in {str(item.get("eventId")) for item in existing}:
            raise ValueError("event_id already exists")
        existing_transactions = {
            str(transaction_id)
            for item in existing
            for transaction_id in item.get("transactionIds") or []
        }
        duplicates = existing_transactions.intersection(normalized_transactions)
        if duplicates:
            raise ValueError(f"transaction already classified: {sorted(duplicates)[0]}")
        event = {
            "schemaVersion": CLASSIFICATION_SCHEMA,
            "eventId": normalized_event_id,
            "kind": normalized_kind,
            "tradeDate": trade_date,
            "transactionIds": normalized_transactions,
            "classificationSource": "USER_CONFIRMED",
            "reason": normalized_reason,
            "recordedAt": utc_now(),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def _ledger_items(value: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = value.get("items")
    if not isinstance(candidates, list):
        raise ValueError("ledger JSON must contain an items array")
    return [item for item in candidates if isinstance(item, dict)]


def _amount(item: dict[str, Any]) -> float:
    raw = item.get("amount")
    if isinstance(raw, bool):
        raise ValueError("transaction amount is invalid")
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("transaction amount is invalid") from exc
    if not math.isfinite(value) or value < 0:
        raise ValueError("transaction amount is invalid")
    return value


def build_activity(
    ledger: dict[str, Any],
    classifications: list[dict[str, Any]],
    *,
    as_of_date: str,
    total_assets_cny: float,
) -> dict[str, Any]:
    try:
        parsed_as_of = date.fromisoformat(as_of_date)
    except ValueError as exc:
        raise ValueError("as_of_date must be YYYY-MM-DD") from exc
    if not math.isfinite(total_assets_cny) or total_assets_cny <= 0:
        raise ValueError("total_assets_cny must be positive")
    month_prefix = parsed_as_of.strftime("%Y-%m")
    items = [
        item
        for item in _ledger_items(ledger)
        if item.get("status") == "CONFIRMED"
        and item.get("type") in {"BUY", "SELL"}
        and str(item.get("tradeDate") or "").startswith(month_prefix)
        and str(item.get("tradeDate") or "") <= as_of_date
    ]
    by_id = {str(item.get("transactionId") or ""): item for item in items if item.get("transactionId")}
    classified_by_transaction: dict[str, str] = {}
    current_events: list[dict[str, Any]] = []
    for classification in classifications:
        trade_date = str(classification.get("tradeDate") or "")
        if not trade_date.startswith(month_prefix) or trade_date > as_of_date:
            continue
        kind = str(classification.get("kind") or "")
        if kind not in KINDS:
            raise ValueError("classification kind is invalid")
        transaction_ids = [str(item) for item in classification.get("transactionIds") or []]
        if not transaction_ids:
            raise ValueError("classification has no transaction ids")
        expected_type = "SELL" if kind == "PROTECTIVE_SELL" else "BUY"
        event_amount = 0.0
        for transaction_id in transaction_ids:
            if transaction_id in classified_by_transaction:
                raise ValueError(f"transaction classified more than once: {transaction_id}")
            transaction = by_id.get(transaction_id)
            if transaction is None:
                raise ValueError(f"classified transaction missing from current-month ledger: {transaction_id}")
            if transaction.get("type") != expected_type:
                raise ValueError(f"classification kind does not match transaction side: {transaction_id}")
            classified_by_transaction[transaction_id] = kind
            event_amount += _amount(transaction)
        current_events.append({
            "eventId": classification.get("eventId"),
            "kind": kind,
            "tradeDate": trade_date,
            "transactionIds": transaction_ids,
            "classificationSource": classification.get("classificationSource"),
            "turnoverPct": round(event_amount / total_assets_cny * 100, 6),
        })

    gross_amount = sum(_amount(item) for item in items)
    protective_amount = sum(
        _amount(item)
        for transaction_id, item in by_id.items()
        if classified_by_transaction.get(transaction_id) == "PROTECTIVE_SELL"
    )
    reentry_amount = sum(
        _amount(item)
        for transaction_id, item in by_id.items()
        if classified_by_transaction.get(transaction_id) == "RISK_OFF_REENTRY"
    )
    ordinary_amount = gross_amount - protective_amount - reentry_amount
    if ordinary_amount < -0.01:
        raise ValueError("classified activity exceeds gross activity")
    return {
        "schemaVersion": ACTIVITY_SCHEMA,
        "source": "classified_transaction_ledger",
        "asOfDate": as_of_date,
        "grossMonthlyTurnoverUsedPct": round(gross_amount / total_assets_cny * 100, 6),
        "ordinaryMonthlyTurnoverUsedPct": round(max(0.0, ordinary_amount) / total_assets_cny * 100, 6),
        "protectiveSellTurnoverPct": round(protective_amount / total_assets_cny * 100, 6),
        "riskOffReentryUsedPct": round(reentry_amount / total_assets_cny * 100, 6),
        "classificationEvents": current_events,
        "ledgerDataUpdatedAt": ledger.get("dataUpdatedAt"),
        "ledgerPortfolioEtag": ledger.get("portfolioEtag"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify = subparsers.add_parser("classify")
    classify.add_argument("--user-id", required=True)
    classify.add_argument("--event-id", required=True)
    classify.add_argument("--kind", choices=sorted(KINDS), required=True)
    classify.add_argument("--trade-date", required=True)
    classify.add_argument("--transaction-id", action="append", required=True)
    classify.add_argument("--reason", required=True)
    classify.add_argument("--user-confirmed", action="store_true")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--user-id", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("--user-id", required=True)
    build.add_argument("--ledger", required=True)
    build.add_argument("--as-of-date", required=True)
    build.add_argument("--total-assets-cny", type=float, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.state_dir).expanduser().resolve() if args.state_dir else default_state_root()
    key = user_key(args.user_id)
    if args.command == "classify":
        result: Any = append_classification(
            root,
            key,
            event_id=args.event_id,
            kind=args.kind,
            trade_date=args.trade_date,
            transaction_ids=args.transaction_id,
            reason=args.reason,
            user_confirmed=args.user_confirmed,
        )
    elif args.command == "list":
        result = {"items": load_classifications(root, key)}
    else:
        ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
        if not isinstance(ledger, dict):
            raise ValueError("ledger JSON must be an object")
        result = build_activity(
            ledger,
            load_classifications(root, key),
            as_of_date=args.as_of_date,
            total_assets_cny=args.total_assets_cny,
        )
    json.dump(result, fp=__import__("sys").stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()


if __name__ == "__main__":
    main()
