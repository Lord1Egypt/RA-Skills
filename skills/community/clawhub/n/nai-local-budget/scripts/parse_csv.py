#!/usr/bin/env python3
"""
parse_csv.py — Parse bank/credit card CSV exports into a unified JSON format.

Supported formats: Chase, Bank of America (BoA), generic (auto-detected).
Output: JSON array of transaction objects.

Usage:
    python3 parse_csv.py <input.csv> [--format chase|boa|generic] [--output transactions.json]
"""

import csv
import json
import os
import sys
import argparse
from datetime import datetime


# ── Format definitions ────────────────────────────────────────────────────────

FORMATS = {
    "chase": {
        "date": "Transaction Date",
        "description": "Description",
        "amount": "Amount",
        "category": "Category",
        # Positive = debit in Chase exports (already correct)
        "amount_sign": "native",  # positive = spend, negative = credit
    },
    "boa": {
        "date": "Date",
        "description": "Description",
        "amount": "Amount",
        "category": None,
        # BoA: positive = debit, negative = credit
        "amount_sign": "native",
    },
    "generic": {
        "date": ["Date", "Transaction Date", "Posted Date", "Posting Date"],
        "description": ["Description", "Merchant", "Name", "Payee", "Transaction Description"],
        "amount": ["Amount", "Debit", "Credit", "Transaction Amount"],
        "category": ["Category", "Type", None],
        "amount_sign": "native",
    },
}

DATE_FORMATS = [
    "%m/%d/%Y",
    "%Y-%m-%d",
    "%m/%d/%y",
    "%m-%d-%Y",
    "%Y/%m/%d",
    "%d/%m/%Y",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_date(raw: str) -> str:
    """Parse a date string into YYYY-MM-DD. Returns original string if unparseable."""
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    sys.stderr.write(f"WARNING: Could not parse date '{raw}', keeping as-is\n")
    return raw


def parse_amount(raw: str) -> float:
    """Parse a currency string into a float. Removes $, commas, parens (negatives)."""
    raw = raw.strip().replace(",", "").replace("$", "").replace(" ", "")
    negative = False
    if raw.startswith("(") and raw.endswith(")"):
        negative = True
        raw = raw[1:-1]
    if raw.startswith("-"):
        negative = True
        raw = raw[1:]
    try:
        value = float(raw)
        return -value if negative else value
    except ValueError:
        sys.stderr.write(f"WARNING: Could not parse amount '{raw}', defaulting to 0.0\n")
        return 0.0


def find_column(headers: list, candidates) -> str | None:
    """Find the first matching column name (case-insensitive)."""
    if candidates is None:
        return None
    if isinstance(candidates, str):
        candidates = [candidates]
    headers_lower = {h.lower(): h for h in headers}
    for candidate in candidates:
        if candidate and candidate.lower() in headers_lower:
            return headers_lower[candidate.lower()]
    return None


def detect_format(headers: list) -> str:
    """Auto-detect CSV format from header columns."""
    headers_set = {h.lower().strip() for h in headers}

    # Chase: has "Transaction Date" and "Post Date"
    if "transaction date" in headers_set and "post date" in headers_set:
        return "chase"

    # BoA: has "Date" and "Running Bal." or "Balance"
    if "date" in headers_set and ("running bal." in headers_set or "balance" in headers_set):
        return "boa"

    # BoA credit: has "Posted Date" and "Reference Number"
    if "posted date" in headers_set and "reference number" in headers_set:
        return "boa"

    return "generic"


# ── Main parser ───────────────────────────────────────────────────────────────

def parse_csv(filepath: str, format_name: str = None) -> list:
    """Parse a bank CSV file into a list of unified transaction dicts."""
    if not os.path.isfile(filepath):
        sys.stderr.write(f"ERROR: File not found: {filepath}\n")
        sys.exit(1)

    transactions = []
    skipped = 0

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        # Peek at first line to skip non-CSV headers (some banks add summary rows)
        raw_content = f.read()

    lines = raw_content.splitlines()

    # Find the actual header row (first row that looks like CSV headers)
    header_start = 0
    for i, line in enumerate(lines):
        if "," in line and any(
            kw in line.lower()
            for kw in ["date", "amount", "description", "merchant", "payee"]
        ):
            header_start = i
            break

    csv_content = "\n".join(lines[header_start:])

    reader = csv.DictReader(csv_content.splitlines())
    headers = reader.fieldnames or []

    if not headers:
        sys.stderr.write("ERROR: No headers found in CSV. Is this a valid export?\n")
        sys.exit(1)

    # Detect or validate format
    if format_name is None:
        format_name = detect_format(headers)
        sys.stderr.write(f"INFO: Auto-detected format: {format_name}\n")
    elif format_name not in FORMATS:
        sys.stderr.write(f"ERROR: Unknown format '{format_name}'. Use: {', '.join(FORMATS.keys())}\n")
        sys.exit(1)

    fmt = FORMATS[format_name]

    # Resolve column names
    date_col = find_column(headers, fmt["date"])
    desc_col = find_column(headers, fmt["description"])
    amount_col = find_column(headers, fmt["amount"])
    cat_col = find_column(headers, fmt.get("category"))

    if not date_col:
        sys.stderr.write(f"ERROR: Could not find date column in headers: {headers}\n")
        sys.exit(1)
    if not desc_col:
        sys.stderr.write(f"ERROR: Could not find description column in headers: {headers}\n")
        sys.exit(1)
    if not amount_col:
        sys.stderr.write(f"ERROR: Could not find amount column in headers: {headers}\n")
        sys.exit(1)

    # Handle BoA split debit/credit columns
    debit_col = find_column(headers, ["Debit", "Withdrawals"])
    credit_col = find_column(headers, ["Credit", "Deposits"])
    split_columns = debit_col and credit_col and not find_column(headers, ["Amount", "Transaction Amount"])

    for row_num, row in enumerate(reader, start=header_start + 2):
        raw_date = row.get(date_col, "").strip()
        raw_desc = row.get(desc_col, "").strip()

        # Skip empty or summary rows
        if not raw_date or not raw_desc:
            skipped += 1
            continue

        # Determine amount
        if split_columns:
            raw_debit = row.get(debit_col, "").strip()
            raw_credit = row.get(credit_col, "").strip()
            if raw_debit:
                amount = parse_amount(raw_debit)
                tx_type = "debit"
            elif raw_credit:
                amount = -parse_amount(raw_credit)  # credits are negative
                tx_type = "credit"
            else:
                skipped += 1
                continue
        else:
            raw_amount = row.get(amount_col, "").strip()
            if not raw_amount:
                skipped += 1
                continue
            amount = parse_amount(raw_amount)
            # Chase/most banks: negative amount = charge/debit (spending), positive = payment/credit (income)
            # This matches Chase, BoA credit, Citi, Amex conventions
            tx_type = "debit" if amount < 0 else "credit"

        date_str = parse_date(raw_date)
        original_category = row.get(cat_col, "").strip() if cat_col else None
        if original_category == "":
            original_category = None

        transactions.append({
            "date": date_str,
            "description": raw_desc,
            "amount": round(abs(amount), 2),
            "type": tx_type,
            "original_category": original_category,
            "source_format": format_name,
        })

    if skipped:
        sys.stderr.write(f"INFO: Skipped {skipped} rows (empty/invalid)\n")

    sys.stderr.write(f"INFO: Parsed {len(transactions)} transactions\n")
    return transactions


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Parse bank CSV exports into unified JSON")
    parser.add_argument("input", help="Path to the CSV file")
    parser.add_argument(
        "--format",
        choices=list(FORMATS.keys()),
        default=None,
        help="CSV format (default: auto-detect)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON file path (default: stdout)",
    )
    args = parser.parse_args()

    transactions = parse_csv(args.input, args.format)

    output = json.dumps(transactions, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        sys.stderr.write(f"INFO: Wrote {len(transactions)} transactions to {args.output}\n")
    else:
        print(output)


if __name__ == "__main__":
    main()
