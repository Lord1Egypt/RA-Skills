#!/usr/bin/env python3
from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jumpserver_api.jms_bootstrap import ensure_requirements_installed

ensure_requirements_installed()

import argparse

from jumpserver_api.jms_reporting import build_daily_usage_report, validate_report_contract
from jumpserver_api.jms_runtime import print_json, run_and_print


def _daily_usage(args: argparse.Namespace):
    return build_daily_usage_report(
        output_path=args.output,
        date_expr=args.date,
        period_expr=args.period,
        date_from_expr=args.date_from,
        date_to_expr=args.date_to,
        org_id=args.org_id,
        command_storage_id=args.command_storage_id,
    )


def _contract_check(_: argparse.Namespace):
    return validate_report_contract()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JumpServer formal report generation entry points.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    daily_usage = subparsers.add_parser("daily-usage")
    daily_usage.add_argument("--output", help="deprecated compatibility flag; actual reports are always written to reports/JumpServer-YYYY-MM-DD.html")
    daily_usage.add_argument("--date")
    daily_usage.add_argument("--period")
    daily_usage.add_argument("--date-from")
    daily_usage.add_argument("--date-to")
    daily_usage.add_argument("--org-id")
    daily_usage.add_argument("--command-storage-id")
    daily_usage.set_defaults(func=_daily_usage)

    contract_check = subparsers.add_parser("contract-check")
    contract_check.set_defaults(func=_contract_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "contract-check":
        result = args.func(args)
        print_json(result)
        return 0 if result.get("contract_passed") else 1
    return run_and_print(args.func, args)


if __name__ == "__main__":
    raise SystemExit(main())
