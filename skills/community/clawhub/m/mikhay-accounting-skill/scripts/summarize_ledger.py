#!/usr/bin/env python3
"""Summarize Chinese personal ledger CSV/JSON files.

花销 is spending after refunds. 内部转账 counts each transfer pair once and is
not part of 花销. Totals always come from scanning every file passed in.
"""

from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

from ledgerlib import (
    SkillConfig,
    accumulate,
    apply_buckets,
    category_net,
    currency_totals,
    fmt,
    fmt_pct,
    index_shard_files,
    iter_ledger_files,
    load_buckets,
    load_file,
    load_skill_config,
    parse_time,
)


def collect_records(
    paths: list[Path],
    config: SkillConfig | None = None,
) -> tuple[list[dict[str, Any]], list[Path]]:
    records: list[dict[str, Any]] = []
    files: list[Path] = []
    for path in paths:
        candidates = iter_ledger_files(path) if path.is_dir() else [path]
        for candidate in candidates:
            book, errors = load_file(candidate)
            if not book.get("is_ledger", True):
                continue
            if errors:
                raise SystemExit(f"{candidate}: {errors[0]}")
            if config is not None:
                config.apply_to_book(book)
            files.append(candidate)
            records.extend(row for row in book["records"] if isinstance(row, dict))
    return records, files


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Chinese personal ledger CSV/JSON files.")
    parser.add_argument("paths", nargs="+", type=Path, help="Ledger files or directories. Directories are scanned fully.")
    parser.add_argument("--month", help="Filter by YYYY-MM after the full scan.")
    parser.add_argument("--shard", choices=["day", "month"], help="Index scanned files by day or month basename.")
    parser.add_argument("--buckets", type=Path, help="Optional bucket map. Omit to skip bucket totals.")
    parser.add_argument("--as-of", help="Date used to age 待报销 rows, YYYY-MM-DD. Default: today.")
    parser.add_argument("--accounts", type=Path, help="Account config. Default: data/accounts.json when present.")
    parser.add_argument("--categories", type=Path, help="Category config. Default: data/categories.json when present.")
    parser.add_argument("--settings", type=Path, help="Workspace settings. Default: data/settings.json when present.")
    args = parser.parse_args()
    if args.as_of:
        parsed_as_of = parse_time(args.as_of)
        if parsed_as_of is None:
            raise SystemExit("--as-of must be YYYY-MM-DD")
        as_of = parsed_as_of.date()
    else:
        as_of = date.today()

    config = load_skill_config(args.paths, args.accounts, args.categories, args.settings)
    if config.errors:
        raise SystemExit("\n".join(config.errors))
    records, files = collect_records(args.paths, config)
    if not files:
        raise SystemExit("no ledger files found")
    if args.month:
        records = [row for row in records if str(row.get("时间", "")).startswith(args.month)]
    totals = accumulate(
        records,
        config.catalog,
        config.categories,
        config.invest_out_subcategory,
    )
    nets = category_net(totals)
    net_whole = sum(nets.values(), Decimal("0"))

    label = files[0].name if len(files) == 1 else f"{len(files)} files"
    print(f"# 记账统计: {label}")
    print(f"扫描文件: {len(files)}")
    shard_mode = args.shard or "month"
    grouped = index_shard_files(files, shard_mode)
    keys = [key for key in sorted(grouped) if key != "unkeyed"]
    print(f"分片({shard_mode}): {', '.join(keys) if keys else '无'}")
    if args.month:
        print(f"月份: {args.month}")
    print()
    print(f"- 记录数: {len(records)}")
    print(f"- 收入: {fmt(totals.income)}")
    print(f"- 支出: {fmt(totals.expense_gross)}")
    print(f"- 花销毛额: {fmt(totals.expense_gross)}")
    print(f"- 退款: {fmt(totals.refunds)}")
    print(f"- 已报销: {fmt(totals.reimbursed)}")
    print(f"- 待报销: {fmt(totals.pending_reimburse)}")
    print(f"- 花销净额: {fmt(totals.expense_net)}")
    print(f"- 还款: {fmt(totals.repayment)}")
    print(f"- 转账: {fmt(totals.transfer_legs)}")
    print(f"- 内部转账: {fmt(totals.internal_transfer)}")
    print(f"- 投资净投入: {fmt(totals.investment_net)}")
    print(f"- 结余(不含还款): {fmt(totals.income - totals.expense_net)}")
    print(f"- 现金流结余: {fmt(totals.income - totals.expense_net - totals.repayment - totals.investment_net)}")
    print("\n## 双口径")
    print(f"- 花销口径: 毛额 {fmt(totals.expense_gross)}, 退款 {fmt(totals.refunds)}, 净额 {fmt(totals.expense_net)}")
    print(f"- 内部转账口径: {fmt(totals.internal_transfer)}")
    print(f"- 基础币种: {config.base_currency}")

    by_currency = currency_totals(records, config.base_currency)
    if by_currency:
        print("\n## 按币种（原币，不折算）")
        for currency in sorted(by_currency):
            bucket = by_currency[currency]
            print(
                f"- {currency}: 记录 {int(bucket['count'])}, 收入 {fmt(bucket['income'])}, "
                f"支出毛额 {fmt(bucket['expense_gross'])}, 退款 {fmt(bucket['refunds'])}, "
                f"已报销 {fmt(bucket['reimbursed'])}, 花销净额 {fmt(bucket['expense_gross'] - bucket['refunds'] - bucket['reimbursed'])}"
            )

    if nets:
        print("\n## 花销按类别")
        ordered = sorted(nets.items(), key=lambda item: (item[1], item[0]), reverse=True)
        for name, value in ordered:
            print(f"- {name}: {fmt(value)} ({fmt_pct(value, net_whole)})")

    subcategory_net = {
        name: totals.by_subcategory[name] - totals.by_subcategory_refund[name] - totals.by_subcategory_reimburse[name]
        for name in set(totals.by_subcategory) | set(totals.by_subcategory_refund) | set(totals.by_subcategory_reimburse)
    }
    if subcategory_net:
        print("\n## 支出Top子类")
        ranked = sorted(subcategory_net.items(), key=lambda item: item[1], reverse=True)[:10]
        for name, value in ranked:
            print(f"- {name}: {fmt(value)}")

    if totals.repayment_by_account:
        print("\n## 还款按账户")
        for name, value in sorted(totals.repayment_by_account.items(), key=lambda item: item[1], reverse=True):
            print(f"- {name}: {fmt(value)}")

    if args.buckets:
        buckets = load_buckets(args.buckets)
        print("\n## 分桶")
        rolled = apply_buckets(nets, buckets)
        whole = sum((value for _, value in rolled), Decimal("0"))
        for name, value in rolled:
            print(f"- {name}: {fmt(value)} ({fmt_pct(value, whole)})")

    print("\n## 待报销")
    if not totals.pending_items:
        print("- 无")
    else:
        for item in totals.pending_items:
            when = str(item.get("时间") or "")
            waited = ""
            if when:
                stamped = parse_time(when)
                if stamped is not None:
                    days = (as_of - stamped.date()).days
                    waited = f" 已等待 {days} 天"
            label = str(item.get("备注") or item.get("id") or "未命名")
            print(f"- {when} {label}: {fmt(item['金额'])}{waited}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
