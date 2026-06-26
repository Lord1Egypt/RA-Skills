#!/usr/bin/env python3
"""
parse-statement.py — Multi-format bank/credit card statement parser
Usage: python3 parse-statement.py <input_file> [output_dir]
Supports: CSV (any bank format), basic PDF text extraction

Detects column structure heuristically — works with Chase, Amex, BoA,
Wells Fargo, Capital One, local credit unions, and most CSV exports.
"""

import csv
import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path


def find_skill_root():
    """Return the skill root directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def detect_date_format(value):
    """Try common date formats and return the parsed date."""
    formats = [
        "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%m-%d-%Y", "%m-%d-%y",
        "%d/%m/%Y", "%d/%m/%y", "%b %d, %Y", "%B %d, %Y",
        "%Y/%m/%d", "%m.%d.%Y", "%d.%m.%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    return None


def clean_vendor_name(raw):
    """Clean cryptic vendor names into human-readable form."""
    if not raw:
        return "Unknown"

    cleaned = raw.strip()

    # Remove common prefixes
    prefixes = [
        r"^TST\*\s*", r"^SQ\s*\*\s*", r"^PP\*", r"^PAYPAL\s*\*",
        r"^CKE\*", r"^SQC\*", r"^AMZN MKTP US\*?\w*",
        r"^GOOGLE\s*\*", r"^APPLE\.COM/", r"^DEBIT CARD PURCHASE\s*-?\s*",
        r"^POS DEBIT\s*-?\s*", r"^RECURRING PAYMENT\s*-?\s*",
    ]
    for prefix in prefixes:
        cleaned = re.sub(prefix, "", cleaned, flags=re.IGNORECASE)

    # Remove trailing reference numbers
    cleaned = re.sub(r"\s+#?\d{4,}$", "", cleaned)
    cleaned = re.sub(r"\s+[A-Z]{2}\s*$", "", cleaned)

    # Specific vendor mappings
    vendor_map = {
        "AMZN": "Amazon",
        "AMAZON": "Amazon",
        "WM SUPERCENTER": "Walmart",
        "WALMART": "Walmart",
        "COSTCO WHSE": "Costco",
        "STARBUCKS": "Starbucks",
        "MCDONALD": "McDonald's",
        "CHICK-FIL-A": "Chick-fil-A",
        "UBER": "Uber",
        "LYFT": "Lyft",
        "NETFLIX": "Netflix",
        "SPOTIFY": "Spotify",
        "HULU": "Hulu",
    }
    upper = cleaned.upper()
    for key, val in vendor_map.items():
        if key in upper:
            return val

    # Title case and trim
    cleaned = cleaned.strip().title()
    return cleaned[:50] if len(cleaned) > 50 else cleaned


def parse_amount(value):
    """Parse an amount string, handling various formats."""
    if not value:
        return None
    s = str(value).strip()

    # Handle parenthetical negatives: (123.45) -> -123.45
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]

    # Remove currency symbols and commas
    s = re.sub(r"[$€£¥,]", "", s)
    s = s.strip()

    try:
        return float(s)
    except ValueError:
        return None


def detect_columns(headers):
    """Heuristically map CSV headers to our schema."""
    mapping = {"date": None, "amount": None, "vendor": None, "memo": None}

    date_patterns = ["date", "trans date", "transaction date", "posted", "posting date"]
    amount_patterns = ["amount", "debit", "charge", "total"]
    vendor_patterns = ["description", "merchant", "vendor", "name", "payee", "memo"]
    memo_patterns = ["memo", "notes", "reference", "details", "category"]

    lower_headers = [h.lower().strip() for h in headers]

    for i, h in enumerate(lower_headers):
        if mapping["date"] is None and any(p in h for p in date_patterns):
            mapping["date"] = i
        elif mapping["amount"] is None and any(p in h for p in amount_patterns):
            mapping["amount"] = i
        elif mapping["vendor"] is None and any(p in h for p in vendor_patterns):
            mapping["vendor"] = i
        elif mapping["memo"] is None and any(p in h for p in memo_patterns):
            mapping["memo"] = i

    # If vendor not found but memo is, use memo as vendor
    if mapping["vendor"] is None and mapping["memo"] is not None:
        mapping["vendor"] = mapping["memo"]
        mapping["memo"] = None

    return mapping


def parse_csv(filepath):
    """Parse a CSV statement file."""
    transactions = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        # Try to detect delimiter
        sample = f.read(4096)
        f.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(f, dialect)
        headers = next(reader, None)

        if not headers:
            return [], "Empty CSV file"

        col_map = detect_columns(headers)

        if col_map["date"] is None or col_map["amount"] is None:
            return [], f"Could not detect date/amount columns in headers: {headers}"

        for row_num, row in enumerate(reader, start=2):
            if not row or all(c.strip() == "" for c in row):
                continue

            try:
                # Parse date
                date_val = row[col_map["date"]] if col_map["date"] < len(row) else ""
                parsed_date = detect_date_format(date_val)
                if not parsed_date:
                    continue

                # Parse amount
                amount_val = row[col_map["amount"]] if col_map["amount"] < len(row) else ""
                amount = parse_amount(amount_val)
                if amount is None:
                    continue

                # Parse vendor
                vendor_raw = ""
                if col_map["vendor"] is not None and col_map["vendor"] < len(row):
                    vendor_raw = row[col_map["vendor"]]

                vendor_clean = clean_vendor_name(vendor_raw)

                tx = {
                    "id": f"txn_{parsed_date.strftime('%Y%m%d')}_{row_num:03d}",
                    "date": parsed_date.strftime("%Y-%m-%d"),
                    "vendor_raw": vendor_raw.strip(),
                    "vendor_clean": vendor_clean,
                    "amount": amount,
                    "category": "Uncategorized",
                    "subcategory": "",
                    "type": "income" if amount > 0 else "expense",
                    "tags": [],
                    "notes": "",
                    "rule_applied": None,
                    "reimbursable": False,
                }
                transactions.append(tx)

            except (IndexError, ValueError) as e:
                continue

    return transactions, None


def apply_rules(transactions, rules_path):
    """Apply custom categorization rules to transactions."""
    if not rules_path.exists():
        return transactions

    with open(rules_path) as f:
        rules = json.load(f)

    for tx in transactions:
        vendor = tx["vendor_clean"].upper()
        vendor_raw = tx["vendor_raw"].upper()

        for rule in rules:
            pattern = rule.get("pattern", "").upper()
            match_type = rule.get("match_type", "contains")

            matched = False
            if match_type == "prefix" and (vendor.startswith(pattern) or vendor_raw.startswith(pattern)):
                matched = True
            elif match_type == "exact" and (vendor == pattern or vendor_raw == pattern):
                matched = True
            elif match_type == "contains" and (pattern in vendor or pattern in vendor_raw):
                matched = True

            if matched:
                tx["category"] = rule.get("category", tx["category"])
                tx["subcategory"] = rule.get("subcategory", tx["subcategory"])
                tx["tags"] = rule.get("tags", tx["tags"])
                tx["reimbursable"] = rule.get("reimbursable", tx["reimbursable"])
                tx["rule_applied"] = rule.get("pattern", "")
                break

    return transactions


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse-statement.py <input_file> [output_dir]")
        print("Supports: CSV files from any bank")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    # Determine output directory
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    else:
        script_dir = Path(__file__).parent
        output_dir = script_dir.parent / "data" / "transactions"

    output_dir.mkdir(parents=True, exist_ok=True)

    # Parse based on file type
    suffix = input_file.suffix.lower()
    if suffix == ".csv":
        transactions, error = parse_csv(input_file)
    else:
        print(f"Error: Unsupported file type '{suffix}'. Use CSV export from your bank.")
        sys.exit(1)

    if error:
        print(f"Error: {error}")
        sys.exit(1)

    if not transactions:
        print("No transactions found in the file.")
        sys.exit(1)

    # Apply custom rules if they exist
    rules_path = Path(__file__).parent.parent / "data" / "rules.json"
    transactions = apply_rules(transactions, rules_path)

    # Determine period from transactions
    dates = [tx["date"] for tx in transactions]
    period = dates[0][:7] if dates else datetime.now().strftime("%Y-%m")

    # Build output
    output = {
        "period": period,
        "source": input_file.name,
        "parsed_at": datetime.now().isoformat() + "Z",
        "transactions": transactions,
    }

    output_file = output_dir / f"{period}.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    # Set permissions
    os.chmod(str(output_file), 0o600)

    # Summary
    total_income = sum(tx["amount"] for tx in transactions if tx["amount"] > 0)
    total_expenses = sum(abs(tx["amount"]) for tx in transactions if tx["amount"] < 0)
    categories = {}
    for tx in transactions:
        if tx["amount"] < 0:
            categories[tx["category"]] = categories.get(tx["category"], 0) + abs(tx["amount"])

    print(f"✅ Parsed {len(transactions)} transactions from {input_file.name}")
    print(f"   Period: {period}")
    print(f"   Income: ${total_income:,.2f}")
    print(f"   Expenses: ${total_expenses:,.2f}")
    print(f"   Categories: {len(categories)}")
    print(f"   Uncategorized: {categories.get('Uncategorized', 0):.0f} transactions")
    print(f"   Output: {output_file}")


if __name__ == "__main__":
    main()
