#!/usr/bin/env python3
import csv
import re
import sys
from collections import defaultdict
from datetime import datetime


def parse_amount(raw):
    text = raw.strip().replace(",", "")
    text = re.sub(r"[^0-9().-]", "", text)
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    return float(text or 0)


def similar_amounts(values):
    avg = sum(values) / len(values)
    return all(abs(v - avg) <= max(2, avg * 0.15) for v in values)


if len(sys.argv) != 2:
    print("Usage: python3 recurring_scan.py transactions.csv")
    sys.exit(1)

groups = defaultdict(list)
with open(sys.argv[1], newline="", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        amount = parse_amount(row.get("amount", "0"))
        if amount >= 0:
            continue
        merchant = (row.get("merchant") or "unknown").strip()
        raw_date = (row.get("date") or "").strip()[:10]
        if not raw_date:
            continue
        try:
            date = datetime.fromisoformat(raw_date)
        except ValueError:
            continue
        groups[merchant].append((date, -amount))

print("Recurring charge candidates")
found = 0

for merchant, items in sorted(groups.items()):
    if len(items) < 2:
        continue
    items.sort()
    gaps = [(items[i][0] - items[i - 1][0]).days for i in range(1, len(items))]
    amounts = [value for _, value in items]
    avg_gap = sum(gaps) / len(gaps)
    cadence = None
    if 25 <= avg_gap <= 35:
        cadence = "monthly"
    elif 330 <= avg_gap <= 380:
        cadence = "annual"
    if cadence and similar_amounts(amounts):
        found += 1
        print(
            f"- {merchant}: {cadence}, {len(items)} charges, "
            f"avg {sum(amounts) / len(amounts):,.2f}"
        )

if found == 0:
    print("- No strong recurring patterns found")
