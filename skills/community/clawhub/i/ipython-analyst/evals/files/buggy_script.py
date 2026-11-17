"""
Sample buggy script for the debugging test case.

The user says: "This script keeps throwing KeyError when I run it on the
sample data — help me figure out what's wrong."

The bug is in `calculate_totals`: when `record` is missing the 'discount'
key, `record['discount']` raises KeyError. The fix is `record.get('discount', 0)`.
"""

import json
from pathlib import Path


def load_records(path):
    """Load JSON records from a file."""
    with open(path) as f:
        return json.load(f)


def calculate_totals(records):
    """Calculate total price for each record.

    Each record has: 'product', 'quantity', 'unit_price', and optionally 'discount'.
    Returns a list of dicts with 'product' and 'total' keys.
    """
    results = []
    for record in records:
        # BUG: 'discount' may not be present. Should use .get('discount', 0).
        subtotal = record['quantity'] * record['unit_price']
        total = subtotal - (subtotal * record['discount'] / 100)
        results.append({'product': record['product'], 'total': total})
    return results


def main():
    records = load_records('/home/z/my-project/upload/sample_records.json')
    totals = calculate_totals(records)
    print(f"Processed {len(totals)} records")
    for t in totals[:5]:
        print(f"  {t['product']}: ${t['total']:.2f}")
    return totals


if __name__ == '__main__':
    main()
