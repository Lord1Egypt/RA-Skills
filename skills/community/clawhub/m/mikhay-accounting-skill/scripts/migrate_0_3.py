#!/usr/bin/env python3
"""Preview legacy reimbursement rows and possible investment rows.

This script never rewrites a ledger. Historical ``收入/报销`` rows stay as
they are and keep their old totals. Whether to edit them is the user's decision.
``--apply`` is refused on purpose.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from ledgerlib import fmt, iter_ledger_files, load_file, money


INVEST_KEYWORDS = ("定投", "基金", "证券", "入金")


def _text(row: dict[str, Any]) -> str:
    return " ".join(str(row.get(field, "") or "") for field in ("类别", "子类", "账户", "备注", "note"))


def _is_legacy_reimburse(row: dict[str, Any]) -> bool:
    tx_type = str(row.get("收支类型", "")).strip()
    subcategory = str(row.get("子类", "")).strip()
    return tx_type == "收入" and subcategory == "报销"


def _investment_keyword(row: dict[str, Any]) -> str:
    if str(row.get("收支类型", "")).strip() == "投资":
        return ""
    text = _text(row)
    for keyword in INVEST_KEYWORDS:
        if keyword in text:
            return keyword
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preview a 0.3 migration. Does not modify files. --apply is refused."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Ledger files or directories.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Refused. Automatic migration is disabled; edit records only if you decide to.",
    )
    args = parser.parse_args()
    if args.apply:
        print(
            "拒绝自动迁移。历史「收入/报销」保持原样，统计不变。"
            "是否改成新的「报销」类型由用户自己决定。投资候选也不会自动改写。",
            file=sys.stderr,
        )
        return 2

    files: list[Path] = []
    for path in args.paths:
        if path.is_dir():
            files.extend(iter_ledger_files(path))
        else:
            files.append(path)
    if not files:
        raise SystemExit("no ledger files found")

    print("# 迁移预览（不写文件）")
    legacy = 0
    candidates = 0
    for path in files:
        book, errors = load_file(path)
        if errors and not book.get("records"):
            print(f"- 跳过 {path}: {errors[0]}")
            continue
        for index, row in enumerate(book.get("records") or [], 1):
            if not isinstance(row, dict):
                continue
            if _is_legacy_reimburse(row):
                legacy += 1
                print(
                    f"- 收入/报销 {path} record[{index}] {row.get('时间', '')} "
                    f"{fmt(abs(money(row.get('金额'))))} {row.get('备注', '')}"
                )
            keyword = _investment_keyword(row)
            if keyword:
                candidates += 1
                print(
                    f"- 投资候选[{keyword}] {path} record[{index}] {row.get('时间', '')} "
                    f"{row.get('收支类型', '')} {fmt(abs(money(row.get('金额'))))} {row.get('备注', '')}"
                )
    print(f"收入/报销: {legacy}")
    print(f"投资候选: {candidates}")
    print("未改写任何文件。投资候选只列出，不自动改。是否改写旧「收入/报销」由用户决定。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
