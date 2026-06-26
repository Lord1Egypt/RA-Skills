#!/usr/bin/env python3
"""Append a single ledger entry to a QianJi CSV file."""

import argparse
import csv
import io
import os
import random
import time


def generate_id():
    """Generate a QianJi-style ID: 'qj' + 13-digit ms timestamp + 6-digit random."""
    ms_timestamp = int(time.time() * 1000)
    rand_suffix = random.randint(100000, 199999)
    return f"qj{ms_timestamp}{rand_suffix}"


def format_amount(amount):
    """Format amount: whole numbers get 1 decimal, others keep up to 2."""
    if amount == int(amount):
        return f"{amount:.1f}"
    else:
        return f"{amount:.2f}".rstrip("0")


def build_row(args):
    """Build a CSV row list from parsed arguments."""
    entry_id = generate_id()
    return [
        entry_id,
        args.time,
        args.category,
        args.subcategory or "",
        args.type,
        format_amount(args.amount),
        "CNY",
        args.account1,
        args.account2 or "",
        args.note or "",
        "",  # 已报销
        "",  # 手续费
        "",  # 优惠券
        args.recorder,
        args.bill_mark or "",
        args.tag or "",
        "",  # 账单图片
        "",  # 关联账单
    ], entry_id


def row_to_csv_string(row):
    """Convert a row list to a CSV string (no trailing newline)."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(row)
    return buf.getvalue().rstrip("\n")


def append_to_file(csv_file, csv_line):
    """Append a CSV line to the file, handling the no-trailing-newline convention."""
    # Check if file ends with newline
    needs_newline = True
    if os.path.getsize(csv_file) > 0:
        with open(csv_file, "rb") as f:
            f.seek(-1, 2)
            needs_newline = f.read(1) != b"\n"

    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        if needs_newline:
            f.write("\n")
        f.write(csv_line)


def main():
    parser = argparse.ArgumentParser(description="Append entry to QianJi CSV")
    parser.add_argument("--csv-file", required=True, help="Path to the CSV file")
    parser.add_argument("--time", required=True, help="Timestamp (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--category", required=True, help="Primary category (分类)")
    parser.add_argument("--subcategory", default="", help="Subcategory (二级分类)")
    parser.add_argument("--type", default="支出", help="Type: 支出/收入/转账/退款")
    parser.add_argument("--amount", type=float, required=True, help="Amount")
    parser.add_argument("--account1", default="工资卡", help="Primary account (账户1)")
    parser.add_argument("--account2", default="", help="Secondary account (账户2)")
    parser.add_argument("--note", default="", help="Note/memo (备注)")
    parser.add_argument("--recorder", default="小明", help="Recorder (记账者)")
    parser.add_argument("--bill-mark", default="", help="Bill mark (账单标记)")
    parser.add_argument("--tag", default="", help="Tag (标签)")

    args = parser.parse_args()

    row, entry_id = build_row(args)
    csv_line = row_to_csv_string(row)
    append_to_file(args.csv_file, csv_line)

    print(entry_id)


if __name__ == "__main__":
    main()
