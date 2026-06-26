#!/usr/bin/env python3
"""
Generate and validate invoice numbers with configurable format patterns.

Supports sequential numbering with configurable reset policies, multiple
document types (invoice, credit_note, proforma), and void number reservation.

Usage:
    python3 invoice_numbering.py --next [invoices_dir]
    python3 invoice_numbering.py --next --format "INV-{YYYY}-{NNN}" [invoices_dir]
    python3 invoice_numbering.py --validate INV-2026-001 [invoices_dir]
    python3 invoice_numbering.py --configure --format "INV-{YYYY}-{NNN}" [invoices_dir]

Options:
    --next              Generate the next invoice number
    --format FORMAT     Number format pattern (default from config or INV-{YYYY}-{NNN})
    --doc-type TYPE     Document type: invoice, credit_note, proforma (default: invoice)
    --validate NUMBER   Check if a number is valid and unique
    --configure         Save numbering configuration
    --json              Output as JSON
    --help              Show this help message

Format tokens:
    {YYYY}   4-digit year
    {YY}     2-digit year
    {MM}     2-digit month
    {NNN}    Zero-padded sequential (3 digits)
    {NNNN}   Zero-padded sequential (4 digits)
    {CLIENT} Client slug prefix

Dependencies: Python 3.8+ stdlib only.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

DEFAULT_FORMAT = "INV-{YYYY}-{NNN}"
CONFIG_FILE = ".numbering-config.json"

DOC_TYPE_PREFIXES = {
    "invoice": "INV",
    "credit_note": "CN",
    "proforma": "PRO",
}

DEFAULT_CONFIG = {
    "formats": {
        "invoice": "INV-{YYYY}-{NNN}",
        "credit_note": "CN-{YYYY}-{NNN}",
        "proforma": "PRO-{YYYY}-{NNN}"
    },
    "reset_policy": "yearly",
    "sequence_scope": "global",
    "void_number_reservation": True,
    "allowed_document_types": ["invoice", "credit_note", "proforma"]
}


def load_config(invoices_dir):
    """Load numbering configuration."""
    config_path = invoices_dir / CONFIG_FILE
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(saved)
                return config
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG.copy()


def save_config(invoices_dir, config):
    """Save numbering configuration."""
    config_path = invoices_dir / CONFIG_FILE
    invoices_dir.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Configuration saved to {config_path}", file=sys.stderr)


def load_index(invoices_dir):
    """Load INDEX.json if it exists."""
    index_path = invoices_dir / "INDEX.json"
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def extract_sequence_number(invoice_number, fmt):
    """Extract the sequential component from an invoice number."""
    # Build a regex from the format pattern
    pattern = fmt
    pattern = pattern.replace("{YYYY}", r"\d{4}")
    pattern = pattern.replace("{YY}", r"\d{2}")
    pattern = pattern.replace("{MM}", r"\d{2}")
    pattern = pattern.replace("{CLIENT}", r"[A-Z0-9-]+")
    pattern = pattern.replace("{NNNN}", r"(\d{4})")
    pattern = pattern.replace("{NNN}", r"(\d{3})")

    match = re.match(pattern, invoice_number)
    if match:
        return int(match.group(1))
    return None


def get_existing_numbers(index, doc_type=None):
    """Get all existing invoice numbers from the index."""
    numbers = set()
    for entry in index:
        num = entry.get("invoice_number")
        if num:
            if doc_type is None or entry.get("document_type", "invoice") == doc_type:
                numbers.add(num)
    return numbers


def get_max_sequence(index, fmt, doc_type, reset_policy):
    """Find the maximum sequence number in use."""
    today = date.today()
    max_seq = 0

    for entry in index:
        num = entry.get("invoice_number", "")
        entry_type = entry.get("document_type", "invoice")

        if entry_type != doc_type:
            continue

        # Check reset policy
        if reset_policy == "yearly":
            issue_date = entry.get("issue_date", "")
            if issue_date and not issue_date.startswith(str(today.year)):
                continue
        elif reset_policy == "monthly":
            issue_date = entry.get("issue_date", "")
            if issue_date and not issue_date.startswith(today.strftime("%Y-%m")):
                continue

        seq = extract_sequence_number(num, fmt)
        if seq is not None and seq > max_seq:
            max_seq = seq

    return max_seq


def generate_number(fmt, sequence, client_slug=None):
    """Generate an invoice number from a format pattern and sequence."""
    today = date.today()
    result = fmt
    result = result.replace("{YYYY}", str(today.year))
    result = result.replace("{YY}", str(today.year)[2:])
    result = result.replace("{MM}", f"{today.month:02d}")
    result = result.replace("{NNNN}", f"{sequence:04d}")
    result = result.replace("{NNN}", f"{sequence:03d}")
    if client_slug:
        result = result.replace("{CLIENT}", client_slug.upper())
    return result


def get_next_number(invoices_dir, doc_type="invoice", fmt=None, client_slug=None):
    """Generate the next invoice number."""
    config = load_config(invoices_dir)
    index = load_index(invoices_dir)

    if fmt is None:
        formats = config.get("formats", {})
        fmt = formats.get(doc_type, DEFAULT_FORMAT)

    reset_policy = config.get("reset_policy", "yearly")
    max_seq = get_max_sequence(index, fmt, doc_type, reset_policy)
    next_seq = max_seq + 1

    return generate_number(fmt, next_seq, client_slug)


def validate_number(invoices_dir, number):
    """Validate an invoice number for format and uniqueness."""
    index = load_index(invoices_dir)
    existing = get_existing_numbers(index)

    result = {
        "number": number,
        "valid_format": bool(re.match(r'^[A-Z0-9-]+$', number)),
        "unique": number not in existing,
        "issues": []
    }

    if not result["valid_format"]:
        result["issues"].append("Number contains invalid characters. Use uppercase letters, digits, and hyphens only.")

    if not result["unique"]:
        result["issues"].append(f"Number '{number}' already exists in the index.")

    # Check for void reservation
    config = load_config(invoices_dir)
    if config.get("void_number_reservation"):
        for entry in index:
            if entry.get("invoice_number") == number and entry.get("status") == "void":
                result["unique"] = False
                result["issues"].append(f"Number '{number}' is reserved (voided invoice).")

    result["is_valid"] = result["valid_format"] and result["unique"]
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate and validate invoice numbers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python3 invoice_numbering.py --next\n"
               "  python3 invoice_numbering.py --next --format 'INV-{YYYY}-{NNN}'\n"
               "  python3 invoice_numbering.py --validate INV-2026-001\n"
               "  python3 invoice_numbering.py --configure --format 'INV-{YYYY}-{NNN}'\n"
    )
    parser.add_argument("invoices_dir", nargs="?", default="./invoices",
                        help="Path to invoices directory (default: ./invoices)")
    parser.add_argument("--next", action="store_true",
                        help="Generate the next invoice number")
    parser.add_argument("--format", type=str, default=None,
                        help="Number format pattern")
    parser.add_argument("--doc-type", type=str, default="invoice",
                        choices=["invoice", "credit_note", "proforma"],
                        help="Document type (default: invoice)")
    parser.add_argument("--validate", type=str, default=None, metavar="NUMBER",
                        help="Validate an invoice number")
    parser.add_argument("--configure", action="store_true",
                        help="Save numbering configuration")
    parser.add_argument("--client", type=str, default=None,
                        help="Client slug for {CLIENT} token")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()
    invoices_dir = Path(args.invoices_dir)

    if args.configure:
        config = load_config(invoices_dir)
        if args.format:
            if "formats" not in config:
                config["formats"] = {}
            config["formats"][args.doc_type] = args.format
        save_config(invoices_dir, config)
        if args.json:
            print(json.dumps(config, indent=2))
        return

    if args.validate:
        result = validate_number(invoices_dir, args.validate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["is_valid"]:
                print(f"✓ '{args.validate}' is valid and unique.")
            else:
                print(f"✗ '{args.validate}' has issues:")
                for issue in result["issues"]:
                    print(f"  - {issue}")
        sys.exit(0 if result["is_valid"] else 1)

    if args.next:
        number = get_next_number(invoices_dir, args.doc_type, args.format, args.client)
        if args.json:
            print(json.dumps({"next_number": number, "doc_type": args.doc_type}))
        else:
            print(number)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
