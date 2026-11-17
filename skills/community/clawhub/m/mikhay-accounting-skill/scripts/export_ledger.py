#!/usr/bin/env python3
"""Export standard ledger JSON to CSV or normalized JSON."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ledgerlib import SCHEMA_VERSION


FIELDS = [
    "时间",
    "收支类型",
    "金额",
    "类别",
    "子类",
    "账户",
    "备注",
    "tags",
    "note",
    "id",
    "refund_of",
    "reimburse_of",
    "报销状态",
    "预计报销",
    "item_id",
    "pairid",
    "target_account",
    "currency",
    "original_amount",
    "fx_rate",
    "cny_amount",
]


def load_records(path: Path) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return "mixed", data, {}
    if isinstance(data, dict):
        return str(data.get("month", "mixed")), data.get("records", data.get("transactions", [])), data
    raise SystemExit(f"Unsupported JSON shape: {path}")


def cell(value: Any) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def export_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({field: cell(record.get(field, "")) for field in FIELDS})


def export_json(path: Path, month: str, records: list[dict[str, Any]], source: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": str(source.get("schema_version") or SCHEMA_VERSION),
        "month": month,
        "records": records,
    }
    if source.get("asset_snapshots"):
        payload["asset_snapshots"] = source["asset_snapshots"]
    if source.get("credit_accounts"):
        payload["credit_accounts"] = source["credit_accounts"]
    if source.get("installment_plans"):
        payload["installment_plans"] = source["installment_plans"]
    if source.get("repayment_reminders"):
        payload["repayment_reminders"] = source["repayment_reminders"]
    if source.get("account_policy"):
        payload["account_policy"] = source["account_policy"]
    if source.get("credit_policy"):
        payload["credit_policy"] = source["credit_policy"]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def infer_format(output: Path, explicit: str) -> str:
    if explicit != "auto":
        return explicit
    if output.suffix.lower() == ".csv":
        return "csv"
    return "json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export standard ledger JSON to CSV or normalized JSON.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", required=True, type=Path)
    parser.add_argument("--format", choices=["auto", "csv", "json"], default="auto")
    parser.add_argument("--month", help="Only export records whose 时间 starts with YYYY-MM.")
    args = parser.parse_args()

    month, records, source = load_records(args.input)
    if args.month:
        records = [record for record in records if str(record.get("时间", "")).startswith(args.month)]
        month = args.month
    fmt = infer_format(args.output, args.format)
    if fmt == "csv":
        export_csv(args.output, records)
    else:
        export_json(args.output, month, records, source)
    print(f"wrote {args.output} records={len(records)} format={fmt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
