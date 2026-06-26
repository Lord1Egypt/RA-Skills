#!/usr/bin/env python3
import csv
import re
import sys
from collections import defaultdict


def parse_amount(raw):
    text = raw.strip().replace(",", "")
    text = re.sub(r"[^0-9().-]", "", text)
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    return float(text or 0)


if len(sys.argv) != 2:
    print("Usage: python3 cashflow_rollup.py transactions.csv")
    sys.exit(1)

path = sys.argv[1]
months = defaultdict(lambda: {"in": 0.0, "out": 0.0})
categories = defaultdict(float)
merchants = defaultdict(float)
days = set()
count = 0

with open(path, newline="", encoding="utf-8-sig") as fh:
    for row in csv.DictReader(fh):
        amount = parse_amount(row.get("amount", "0"))
        date = (row.get("date") or "")[:10]
        month = date[:7] or "unknown"
        merchant = (row.get("merchant") or "unknown").strip()
        category = (row.get("category") or "uncategorized").strip()
        count += 1
        if date:
            days.add(date)
        if amount >= 0:
            months[month]["in"] += amount
        else:
            spend = -amount
            months[month]["out"] += spend
            categories[category] += spend
            merchants[merchant] += spend

total_in = sum(v["in"] for v in months.values())
total_out = sum(v["out"] for v in months.values())
daily_burn = total_out / max(len(days), 1)

print("Cashflow Rollup")
print(f"Transactions: {count}")
print(f"Total inflow:  {total_in:,.2f}")
print(f"Total outflow: {total_out:,.2f}")
print(f"Net cashflow:  {total_in - total_out:,.2f}")
print(f"Average daily burn: {daily_burn:,.2f}")

print("\nMonthly totals")
for month in sorted(months):
    inflow = months[month]["in"]
    outflow = months[month]["out"]
    print(f"- {month}: in {inflow:,.2f} | out {outflow:,.2f} | net {inflow - outflow:,.2f}")

print("\nTop categories")
for name, value in sorted(categories.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"- {name}: {value:,.2f}")

print("\nTop merchants")
for name, value in sorted(merchants.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"- {name}: {value:,.2f}")
