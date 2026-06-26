#!/usr/bin/env python3
"""
Nex Expenses - Receipt & Expense Categorizer with Belgian Tax Buckets
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Track business expenses with automatic Belgian tax categorization. OCR receipts,
auto-categorize into Belgian deduction categories, generate quarterly summaries
for your boekhouder, and track BTW for aangifte. Built for eenmanszaken and
kleine ondernemingen.
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from decimal import Decimal
from typing import Optional, Tuple

# Add lib directory to Python path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SKILL_DIR, "lib")
sys.path.insert(0, LIB_DIR)

from config import (
    DB_PATH,
    DATA_DIR,
    RECEIPTS_DIR,
    EXPORT_DIR,
    BELGIAN_TAX_CATEGORIES,
    BTW_RATES,
    VENDOR_CATEGORY_MAP,
    QUARTERS,
)
from storage import (
    init_db,
    save_expense,
    get_expense,
    list_expenses,
    update_expense,
    delete_expense,
    search_expenses,
    get_quarterly_summary,
    get_yearly_summary,
    get_monthly_summary,
    get_category_breakdown,
    get_vendor_stats,
    export_for_accountant,
    get_btw_summary,
)
from ocr import ocr_receipt

FOOTER = "[Nex Expenses by Nex AI | nex-ai.be]"


def _check_db():
    """Check if database exists. Initialize if not."""
    if not DB_PATH.exists():
        init_db()


def _print_footer():
    print(f"\n{FOOTER}")


def _format_currency(value):
    """Format a numeric value as Euro currency."""
    if value is None:
        return "€ 0,00"
    return f"€ {float(value):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def _parse_natural_language_expense(text: str) -> Optional[dict]:
    """
    Parse natural language expense description like:
    'lunch bij De Vitrine 45.50 BTW 21%'
    'Shell tanken 65,30 21% BTW'
    'Adobe subscription 15,99 no VAT'

    Returns dict with vendor, amount_incl, btw_rate, or None if parsing fails.
    """
    result = {}

    # Try to extract amount (both . and , as decimal separator)
    amount_pattern = r'(\d+[.,]\d{2})'
    amounts = re.findall(amount_pattern, text)
    if amounts:
        # Use the last amount found
        amount_str = amounts[-1].replace(',', '.')
        try:
            result['amount_incl'] = float(amount_str)
        except ValueError:
            pass

    # Try to extract BTW rate
    btw_pattern = r'(?:btw|tva|vat)\s*(\d{1,2})%|(\d{1,2})%\s*(?:btw|tva|vat)'
    btw_match = re.search(btw_pattern, text, re.IGNORECASE)
    if btw_match:
        btw_str = btw_match.group(1) or btw_match.group(2)
        result['btw_rate'] = int(btw_str)
    else:
        # Default to 21% if not specified
        if 'no vat' not in text.lower() and 'exempt' not in text.lower():
            result['btw_rate'] = 21
        else:
            result['btw_rate'] = 0

    # Try to extract vendor from beginning or after keywords
    vendor_match = re.match(r'^(?:at|bij|from|chez)?\s*([A-Za-z\s&\']+?)(?:\s+\d|$)', text, re.IGNORECASE)
    if vendor_match:
        vendor = vendor_match.group(1).strip()
        if vendor and len(vendor) > 2:
            result['vendor'] = vendor

    if result.get('vendor') or result.get('amount_incl'):
        return result

    return None


def _auto_categorize_vendor(vendor_name: str) -> Tuple[str, float]:
    """
    Auto-categorize a vendor based on keywords.
    Returns (category_id, confidence) where confidence is 0-1.
    """
    vendor_lower = vendor_name.lower()

    # Exact match first
    for keyword, category in VENDOR_CATEGORY_MAP.items():
        if keyword.lower() == vendor_lower:
            return (category, 1.0)

    # Partial match
    for keyword, category in VENDOR_CATEGORY_MAP.items():
        if keyword.lower() in vendor_lower or vendor_lower in keyword.lower():
            return (category, 0.8)

    # Default to beroepskosten
    return ("beroepskosten_100", 0.5)


def _calculate_btw_amount(amount_incl: float, btw_rate: int) -> Tuple[float, float]:
    """
    Calculate BTW amount and amount excluding BTW.
    Returns (amount_excl, btw_amount).
    """
    if btw_rate == 0:
        return (amount_incl, 0.0)

    multiplier = 1 + (btw_rate / 100)
    amount_excl = round(amount_incl / multiplier, 2)
    btw_amount = round(amount_incl - amount_excl, 2)

    return (amount_excl, btw_amount)


# ============================================================
# COMMAND: ADD
# ============================================================

def cmd_add(args):
    _check_db()

    # Three modes: receipt OCR, manual with flags, or natural language
    if args.receipt:
        # Mode 1: Receipt OCR
        receipt_path = args.receipt
        if not Path(receipt_path).exists():
            print(f"ERROR: Receipt file not found: {receipt_path}", file=sys.stderr)
            sys.exit(1)

        print(f"Scanning receipt: {receipt_path}")
        print("---")

        ocr_result = ocr_receipt(receipt_path)

        if ocr_result.get('errors'):
            for error in ocr_result['errors']:
                print(f"Warning: {error}")

        # Display OCR findings
        print(f"Vendor: {ocr_result.get('vendor') or '(not detected)'}")
        print(f"Date: {ocr_result.get('date') or '(not detected)'}")
        print(f"Amount (incl. BTW): {_format_currency(ocr_result.get('total_incl'))}")
        print(f"Amount (excl. BTW): {_format_currency(ocr_result.get('total_excl'))}")
        print(f"BTW Rate: {ocr_result.get('btw_rate') or '?'}%")
        print(f"BTW Amount: {_format_currency(ocr_result.get('btw_amount'))}")
        print(f"Confidence: {ocr_result.get('confidence', 0)*100:.0f}%")

        if ocr_result.get('items'):
            print("\nDetected items:")
            for item in ocr_result['items'][:5]:
                print(f"  - {item.get('description')}: {_format_currency(item.get('amount'))}")

        print("---")

        # Auto-categorize
        vendor = ocr_result.get('vendor', 'Receipt')
        category, confidence = _auto_categorize_vendor(vendor)
        category_name = BELGIAN_TAX_CATEGORIES.get(category, {}).get('name', category)

        print(f"Suggested category: {category_name} (confidence: {confidence*100:.0f}%)")

        # Prepare expense dict
        amount_incl = ocr_result.get('total_incl')
        btw_rate = ocr_result.get('btw_rate') or 21

        if amount_incl:
            amount_excl, btw_amount = _calculate_btw_amount(float(amount_incl), btw_rate)
        else:
            amount_excl = ocr_result.get('total_excl') or 0
            btw_amount = ocr_result.get('btw_amount') or 0
            amount_incl = amount_excl + btw_amount

        # Copy receipt file to receipts directory
        receipt_filename = Path(receipt_path).name
        receipt_dest = RECEIPTS_DIR / f"{dt.datetime.now().isoformat()}_{receipt_filename}"
        try:
            receipt_dest.write_bytes(Path(receipt_path).read_bytes())
            receipt_stored = str(receipt_dest)
        except Exception as e:
            print(f"Warning: Could not store receipt: {e}")
            receipt_stored = None

        expense_dict = {
            'date': ocr_result.get('date') or dt.datetime.now().strftime('%Y-%m-%d'),
            'vendor': vendor,
            'description': ocr_result.get('raw_text')[:100] if ocr_result.get('raw_text') else 'Receipt',
            'amount_incl': amount_incl,
            'amount_excl': amount_excl,
            'btw_rate': btw_rate,
            'btw_amount': btw_amount,
            'tax_category': category,
            'receipt_path': receipt_stored,
            'receipt_text': ocr_result.get('raw_text'),
            'notes': f"OCR confidence: {ocr_result.get('confidence', 0)*100:.0f}%",
        }

        expense_id = save_expense(expense_dict)
        print(f"\nExpense saved (ID: {expense_id})")

    elif args.vendor or args.amount:
        # Mode 2: Manual entry with flags
        if not args.vendor or args.amount is None:
            print("ERROR: --vendor and --amount are required together", file=sys.stderr)
            sys.exit(1)

        amount_incl = float(args.amount)
        btw_rate = args.btw or 21
        category = args.category

        if not category:
            category, _ = _auto_categorize_vendor(args.vendor)

        amount_excl, btw_amount = _calculate_btw_amount(amount_incl, btw_rate)

        expense_dict = {
            'date': args.date or dt.datetime.now().strftime('%Y-%m-%d'),
            'vendor': args.vendor,
            'description': args.description or f"Expense at {args.vendor}",
            'amount_incl': amount_incl,
            'amount_excl': amount_excl,
            'btw_rate': btw_rate,
            'btw_amount': btw_amount,
            'tax_category': category,
            'payment_method': args.payment_method,
            'notes': args.notes,
        }

        category_name = BELGIAN_TAX_CATEGORIES.get(category, {}).get('name', category)
        print(f"Adding expense for {args.vendor}")
        print(f"  Amount: {_format_currency(amount_incl)} (incl. {btw_rate}% BTW)")
        print(f"  Category: {category_name}")

        expense_id = save_expense(expense_dict)
        print(f"Expense saved (ID: {expense_id})")

    else:
        # Mode 3: Natural language from positional argument
        if not args.text:
            print("ERROR: Provide expense description or use --vendor/--amount", file=sys.stderr)
            sys.exit(1)

        text = " ".join(args.text)
        parsed = _parse_natural_language_expense(text)

        if not parsed:
            print("ERROR: Could not parse expense. Try:", file=sys.stderr)
            print("  nex-expenses add --vendor 'Shell' --amount 65.30 --btw 21", file=sys.stderr)
            sys.exit(1)

        vendor = parsed.get('vendor', 'Vendor')
        amount_incl = parsed.get('amount_incl', 0)
        btw_rate = parsed.get('btw_rate', 21)

        category, confidence = _auto_categorize_vendor(vendor)
        category_name = BELGIAN_TAX_CATEGORIES.get(category, {}).get('name', category)

        amount_excl, btw_amount = _calculate_btw_amount(amount_incl, btw_rate)

        print(f"Parsed expense:")
        print(f"  Vendor: {vendor}")
        print(f"  Amount: {_format_currency(amount_incl)} (incl. {btw_rate}% BTW)")
        print(f"  Category: {category_name} (confidence: {confidence*100:.0f}%)")
        print("---")

        expense_dict = {
            'date': dt.datetime.now().strftime('%Y-%m-%d'),
            'vendor': vendor,
            'description': text[:100],
            'amount_incl': amount_incl,
            'amount_excl': amount_excl,
            'btw_rate': btw_rate,
            'btw_amount': btw_amount,
            'tax_category': category,
        }

        expense_id = save_expense(expense_dict)
        print(f"Expense saved (ID: {expense_id})")

    _print_footer()


# ============================================================
# COMMAND: LIST
# ============================================================

def cmd_list(args):
    _check_db()

    # Determine quarter and year for filter
    since = args.since
    until = args.until

    if args.quarter and args.year:
        # Find date range for quarter
        quarter = args.quarter.upper()
        year = int(args.year)
        if quarter not in QUARTERS:
            print(f"ERROR: Invalid quarter {quarter}. Use Q1, Q2, Q3, Q4", file=sys.stderr)
            sys.exit(1)

        months = QUARTERS[quarter]['months']
        since = f"{year}-{months[0]:02d}-01"
        until = f"{year}-{months[2]:02d}-32"

    expenses = list_expenses(
        since=since,
        until=until,
        category=args.category,
        vendor=args.vendor,
        tag=args.tag,
        limit=args.limit
    )

    if not expenses:
        print("No expenses found.")
        _print_footer()
        return

    if args.output == 'json':
        # JSON output
        for exp in expenses:
            print(json.dumps(exp))
    else:
        # Table format
        print(f"Expenses ({len(expenses)} total)")
        print("---")

        for exp in expenses:
            date = exp['date']
            vendor = exp['vendor']
            amount = _format_currency(exp['amount_incl'])
            category = BELGIAN_TAX_CATEGORIES.get(exp['tax_category'], {}).get('name', exp['tax_category'])

            print(f"ID {exp['id']}: {date} | {vendor} | {amount} | {category}")
            if exp.get('description'):
                print(f"           {exp['description'][:60]}")

    _print_footer()


# ============================================================
# COMMAND: SHOW
# ============================================================

def cmd_show(args):
    _check_db()

    expense = get_expense(args.id)

    if not expense:
        print(f"ERROR: Expense {args.id} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Expense #{expense['id']}")
    print("---")
    print(f"Date: {expense['date']}")
    print(f"Vendor: {expense['vendor']}")
    print(f"Description: {expense['description'] or '(none)'}")
    print(f"Amount (incl. BTW): {_format_currency(expense['amount_incl'])}")
    print(f"Amount (excl. BTW): {_format_currency(expense['amount_excl'])}")
    print(f"BTW Rate: {expense['btw_rate']}%")
    print(f"BTW Amount: {_format_currency(expense['btw_amount'])}")

    category_name = BELGIAN_TAX_CATEGORIES.get(expense['tax_category'], {}).get('name', expense['tax_category'])
    print(f"Tax Category: {category_name}")
    print(f"Deductible %: {expense['deduction_pct']}%")
    print(f"Deductible Amount: {_format_currency(expense['deductible_amount'])}")

    if expense.get('payment_method'):
        print(f"Payment Method: {expense['payment_method']}")
    if expense.get('tags'):
        print(f"Tags: {expense['tags']}")
    if expense.get('notes'):
        print(f"Notes: {expense['notes']}")
    if expense.get('receipt_path'):
        print(f"Receipt: {expense['receipt_path']}")

    print(f"Quarter: {expense.get('quarterly_period', 'N/A')}")
    print(f"Year: {expense.get('year', 'N/A')}")
    print(f"Created: {expense.get('created_at', 'N/A')}")

    _print_footer()


# ============================================================
# COMMAND: EDIT
# ============================================================

def cmd_edit(args):
    _check_db()

    expense = get_expense(args.id)
    if not expense:
        print(f"ERROR: Expense {args.id} not found", file=sys.stderr)
        sys.exit(1)

    updates = {}

    if args.category:
        updates['tax_category'] = args.category
    if args.amount is not None:
        updates['amount_incl'] = float(args.amount)
    if args.btw is not None:
        updates['btw_rate'] = args.btw
    if args.description:
        updates['description'] = args.description
    if args.vendor:
        updates['vendor'] = args.vendor

    # Recalculate BTW if amount changed
    if 'amount_incl' in updates or 'btw_rate' in updates:
        amount_incl = updates.get('amount_incl', expense['amount_incl'])
        btw_rate = updates.get('btw_rate', expense['btw_rate'])
        amount_excl, btw_amount = _calculate_btw_amount(amount_incl, btw_rate)
        updates['amount_excl'] = amount_excl
        updates['btw_amount'] = btw_amount

    if updates:
        update_expense(args.id, updates)
        print(f"Expense #{args.id} updated")
    else:
        print("No changes specified")

    _print_footer()


# ============================================================
# COMMAND: DELETE
# ============================================================

def cmd_delete(args):
    _check_db()

    expense = get_expense(args.id)
    if not expense:
        print(f"ERROR: Expense {args.id} not found", file=sys.stderr)
        sys.exit(1)

    if not args.force:
        print(f"Delete expense #{args.id}?")
        print(f"  Vendor: {expense['vendor']}")
        print(f"  Amount: {_format_currency(expense['amount_incl'])}")
        print("---")
        response = input("Are you sure? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Cancelled.")
            return

    delete_expense(args.id)
    print(f"Expense #{args.id} deleted")
    _print_footer()


# ============================================================
# COMMAND: SEARCH
# ============================================================

def cmd_search(args):
    _check_db()

    query = " ".join(args.query)
    results = search_expenses(query, limit=args.limit)

    if not results:
        print(f"No expenses found matching '{query}'")
        _print_footer()
        return

    print(f"Search results for '{query}' ({len(results)} found)")
    print("---")

    for exp in results:
        date = exp['date']
        vendor = exp['vendor']
        amount = _format_currency(exp['amount_incl'])

        print(f"ID {exp['id']}: {date} | {vendor} | {amount}")
        if exp.get('description'):
            print(f"           {exp['description'][:60]}")

    _print_footer()


# ============================================================
# COMMAND: SUMMARY
# ============================================================

def cmd_summary(args):
    _check_db()

    if args.type == 'quarterly':
        if not args.quarter or not args.year:
            print("ERROR: --quarter and --year required for quarterly summary", file=sys.stderr)
            sys.exit(1)

        summary = get_quarterly_summary(int(args.year), args.quarter.upper())

        print(f"Quarterly Summary - {args.quarter.upper()} {args.year}")
        print("---")
        print(f"Total Expenses: {_format_currency(summary['total_gross'])}")
        print(f"Total Deductible: {_format_currency(summary['total_deductible'])}")
        print(f"Total BTW Reclaimable: {_format_currency(summary['total_btw_reclaimable'])}")
        print(f"Number of Expenses: {summary['expense_count']}")
        print("")
        print("By Category:")

        for category_id, cat_data in sorted(summary['by_category'].items()):
            name = cat_data['name']
            count = cat_data['count']
            total = _format_currency(cat_data['total'])
            deductible = _format_currency(cat_data['deductible'])
            print(f"  {name}")
            print(f"    Count: {count}, Total: {total}, Deductible: {deductible}")

    elif args.type == 'yearly':
        if not args.year:
            print("ERROR: --year required for yearly summary", file=sys.stderr)
            sys.exit(1)

        summary = get_yearly_summary(int(args.year))

        print(f"Yearly Summary - {args.year}")
        print("---")
        print(f"Total Expenses: {_format_currency(summary['total_gross'])}")
        print(f"Total Deductible: {_format_currency(summary['total_deductible'])}")
        print(f"Total BTW Reclaimable: {_format_currency(summary['total_btw_reclaimable'])}")
        print(f"Number of Expenses: {summary['expense_count']}")
        print("")
        print("By Quarter:")

        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            if quarter in summary['by_quarter']:
                q_data = summary['by_quarter'][quarter]
                total = _format_currency(q_data['total'])
                deductible = _format_currency(q_data['deductible'])
                count = q_data['count']
                print(f"  {quarter}: {count} expenses, {total} total, {deductible} deductible")

    elif args.type == 'monthly':
        if not args.month:
            print("ERROR: --month required for monthly summary (YYYY-MM)", file=sys.stderr)
            sys.exit(1)

        parts = args.month.split('-')
        year, month = int(parts[0]), int(parts[1])

        summary = get_monthly_summary(year, month)

        month_name = dt.date(year, month, 1).strftime('%B')
        print(f"Monthly Summary - {month_name} {year}")
        print("---")
        print(f"Total Expenses: {_format_currency(summary['total_gross'])}")
        print(f"Total Deductible: {_format_currency(summary['total_deductible'])}")
        print(f"Total BTW Reclaimable: {_format_currency(summary['total_btw_reclaimable'])}")
        print(f"Number of Expenses: {summary['expense_count']}")

    elif args.type == 'categories':
        year = int(args.year) if args.year else None
        since = f"{year}-01-01" if year else None
        until = f"{year}-12-32" if year else None

        breakdown = get_category_breakdown(since=since, until=until)

        title = f"Category Breakdown ({year})" if year else "Category Breakdown"
        print(title)
        print("---")

        for cat in breakdown:
            name = cat['category_name']
            count = cat['count']
            total = _format_currency(cat['total'])
            deductible = _format_currency(cat['deductible'])
            pct = cat['deduction_pct']
            print(f"{name} ({pct}%): {count} expenses, {total} total, {deductible} deductible")

    elif args.type == 'vendors':
        vendors = get_vendor_stats(limit=args.top)

        print(f"Top {args.top} Vendors by Spending")
        print("---")

        for vendor in vendors:
            name = vendor['name']
            spent = _format_currency(vendor['total_spent'])
            print(f"{name}: {spent}")

    elif args.type == 'btw':
        if not args.quarter or not args.year:
            print("ERROR: --quarter and --year required for BTW summary", file=sys.stderr)
            sys.exit(1)

        btw_summary = get_btw_summary(int(args.year), args.quarter.upper())

        print(f"BTW Input Summary - {args.quarter.upper()} {args.year}")
        print("---")

        for rate, data in sorted(btw_summary['by_rate'].items()):
            rate_name = data['rate_name']
            total_btw = _format_currency(data['total_btw'])
            print(f"{rate_name}: {total_btw}")

        print(f"\nTotal Reclaimable: {_format_currency(btw_summary['total_reclaimable'])}")

    _print_footer()


# ============================================================
# COMMAND: EXPORT
# ============================================================

def cmd_export(args):
    _check_db()

    format_type = args.format.lower()
    if format_type not in ['csv', 'json']:
        print(f"ERROR: Unsupported format {format_type}", file=sys.stderr)
        sys.exit(1)

    # Parse year and optional quarter
    year = None
    quarter = None

    if args.period:
        if args.period.startswith('Q'):
            parts = args.period.split()
            quarter = args.period
            year = int(args.year) if args.year else None
        else:
            year = int(args.period)

    if not year:
        year = dt.datetime.now().year

    data = export_for_accountant(year, quarter)

    if not data:
        print(f"No expenses found for {quarter or year}")
        _print_footer()
        return

    # Generate filename
    period_str = f"{quarter}_{year}" if quarter else str(year)
    filename = f"expenses_{period_str}.{format_type}"
    filepath = EXPORT_DIR / filename

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    if format_type == 'csv':
        import csv
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            if data:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    else:  # json
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    print(f"Exported {len(data)} expenses to {filepath}")
    _print_footer()


# ============================================================
# COMMAND: CATEGORIES
# ============================================================

def cmd_categories(args):
    print("Belgian Tax Deduction Categories")
    print("---")

    for cat_id, cat_data in sorted(BELGIAN_TAX_CATEGORIES.items()):
        name = cat_data['name']
        deduction = cat_data['deduction']
        description = cat_data['description']

        print(f"{cat_id}")
        print(f"  Name: {name}")
        print(f"  Deduction: {deduction}%")
        print(f"  Description: {description}")

    _print_footer()


# ============================================================
# COMMAND: OCR
# ============================================================

def cmd_ocr(args):
    filepath = args.file

    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"OCR Receipt: {filepath}")
    print("---")

    result = ocr_receipt(filepath)

    print(f"Vendor: {result.get('vendor') or '(not detected)'}")
    print(f"Date: {result.get('date') or '(not detected)'}")
    print(f"Amount (incl. BTW): {_format_currency(result.get('total_incl'))}")
    print(f"Amount (excl. BTW): {_format_currency(result.get('total_excl'))}")
    print(f"BTW Rate: {result.get('btw_rate') or '?'}%")
    print(f"BTW Amount: {_format_currency(result.get('btw_amount'))}")
    print(f"Confidence: {result.get('confidence', 0)*100:.0f}%")

    if result.get('items'):
        print("\nDetected items:")
        for item in result['items']:
            print(f"  - {item.get('description')}: {_format_currency(item.get('amount'))}")

    if result.get('errors'):
        print("\nErrors:")
        for error in result['errors']:
            print(f"  - {error}")

    print("\nRaw OCR text:")
    print("---")
    print(result.get('raw_text', '(no text extracted)'))

    _print_footer()


# ============================================================
# COMMAND: STATS
# ============================================================

def cmd_stats(args):
    _check_db()

    year = int(args.year) if args.year else None

    if year:
        summary = get_yearly_summary(year)
        print(f"Statistics - {year}")
    else:
        # Overall stats
        all_expenses = list_expenses(limit=999999)
        if not all_expenses:
            print("No expenses tracked yet.")
            _print_footer()
            return

        total = sum(e['amount_incl'] for e in all_expenses)
        deductible = sum(e['deductible_amount'] or 0 for e in all_expenses)
        btw = sum(e['btw_amount'] or 0 for e in all_expenses)

        print("Overall Statistics")
        print("---")
        print(f"Total Expenses: {len(all_expenses)}")
        print(f"Total Amount: {_format_currency(total)}")
        print(f"Total Deductible: {_format_currency(deductible)}")
        print(f"Total BTW: {_format_currency(btw)}")

        _print_footer()
        return

    print("---")
    print(f"Total Expenses: {_format_currency(summary['total_gross'])}")
    print(f"Total Deductible: {_format_currency(summary['total_deductible'])}")
    print(f"Total BTW Reclaimable: {_format_currency(summary['total_btw_reclaimable'])}")
    print(f"Number of Expenses: {summary['expense_count']}")

    _print_footer()


# ============================================================
# COMMAND: CONFIG
# ============================================================

def cmd_config(args):
    _check_db()

    config_file = DATA_DIR / "config.json"

    if args.action == 'show':
        if config_file.exists():
            config = json.loads(config_file.read_text())
            print("Configuration")
            print("---")
            for key, value in config.items():
                print(f"{key}: {value}")
        else:
            print("No configuration set yet. Using defaults.")

    elif args.action == 'set-btw-status':
        status = args.status.lower()
        if status not in ['vrijgesteld', 'plichtig']:
            print("ERROR: Use 'vrijgesteld' or 'plichtig'", file=sys.stderr)
            sys.exit(1)

        if config_file.exists():
            config = json.loads(config_file.read_text())
        else:
            config = {}

        config['btw_status'] = status
        config_file.write_text(json.dumps(config, indent=2))
        print(f"BTW status set to: {status}")

    _print_footer()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Track business expenses with automatic Belgian tax categorization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # ADD
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('text', nargs='*', help='Natural language expense description')
    add_parser.add_argument('--vendor', help='Vendor name')
    add_parser.add_argument('--amount', type=float, help='Amount including BTW')
    add_parser.add_argument('--btw', type=int, help='BTW rate (default: 21)')
    add_parser.add_argument('--category', help='Tax category ID')
    add_parser.add_argument('--description', help='Description')
    add_parser.add_argument('--date', help='Date (YYYY-MM-DD, default: today)')
    add_parser.add_argument('--payment-method', help='Payment method (cash, bank_transfer, credit_card, etc.)')
    add_parser.add_argument('--notes', help='Notes')
    add_parser.add_argument('--receipt', help='Path to receipt image')
    add_parser.set_defaults(func=cmd_add)

    # LIST
    list_parser = subparsers.add_parser('list', help='List expenses')
    list_parser.add_argument('--quarter', help='Quarter (Q1, Q2, Q3, Q4)')
    list_parser.add_argument('--year', help='Year')
    list_parser.add_argument('--category', help='Tax category')
    list_parser.add_argument('--vendor', help='Vendor name')
    list_parser.add_argument('--since', help='Start date (YYYY-MM-DD)')
    list_parser.add_argument('--until', help='End date (YYYY-MM-DD)')
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.add_argument('--limit', type=int, default=100, help='Max results')
    list_parser.add_argument('--output', choices=['text', 'json'], default='text')
    list_parser.set_defaults(func=cmd_list)

    # SHOW
    show_parser = subparsers.add_parser('show', help='Show single expense')
    show_parser.add_argument('id', type=int, help='Expense ID')
    show_parser.set_defaults(func=cmd_show)

    # EDIT
    edit_parser = subparsers.add_parser('edit', help='Edit expense')
    edit_parser.add_argument('id', type=int, help='Expense ID')
    edit_parser.add_argument('--category', help='Tax category')
    edit_parser.add_argument('--amount', type=float, help='Amount including BTW')
    edit_parser.add_argument('--btw', type=int, help='BTW rate')
    edit_parser.add_argument('--description', help='Description')
    edit_parser.add_argument('--vendor', help='Vendor name')
    edit_parser.set_defaults(func=cmd_edit)

    # DELETE
    delete_parser = subparsers.add_parser('delete', help='Delete expense')
    delete_parser.add_argument('id', type=int, help='Expense ID')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    delete_parser.set_defaults(func=cmd_delete)

    # SEARCH
    search_parser = subparsers.add_parser('search', help='Search expenses')
    search_parser.add_argument('query', nargs='+', help='Search query')
    search_parser.add_argument('--limit', type=int, default=30, help='Max results')
    search_parser.set_defaults(func=cmd_search)

    # SUMMARY
    summary_parser = subparsers.add_parser('summary', help='Financial summaries')
    summary_parser.add_argument('type', choices=['quarterly', 'yearly', 'monthly', 'categories', 'vendors', 'btw'])
    summary_parser.add_argument('--quarter', help='Quarter (Q1-Q4)')
    summary_parser.add_argument('--year', help='Year')
    summary_parser.add_argument('--month', help='Month (YYYY-MM)')
    summary_parser.add_argument('--top', type=int, default=20, help='Top N vendors')
    summary_parser.set_defaults(func=cmd_summary)

    # EXPORT
    export_parser = subparsers.add_parser('export', help='Export for accountant')
    export_parser.add_argument('format', choices=['csv', 'json'])
    export_parser.add_argument('period', nargs='?', help='Period: Q1-Q4 for quarter, or year')
    export_parser.add_argument('--year', help='Year (for quarters)')
    export_parser.set_defaults(func=cmd_export)

    # CATEGORIES
    cat_parser = subparsers.add_parser('categories', help='List tax categories')
    cat_parser.set_defaults(func=cmd_categories)

    # OCR
    ocr_parser = subparsers.add_parser('ocr', help='Test OCR on receipt')
    ocr_parser.add_argument('file', help='Path to receipt image')
    ocr_parser.set_defaults(func=cmd_ocr)

    # STATS
    stats_parser = subparsers.add_parser('stats', help='Overall statistics')
    stats_parser.add_argument('--year', help='Year')
    stats_parser.set_defaults(func=cmd_stats)

    # CONFIG
    config_parser = subparsers.add_parser('config', help='Configuration')
    config_parser.add_argument('action', choices=['show', 'set-btw-status'])
    config_parser.add_argument('status', nargs='?', help='Status for set-btw-status')
    config_parser.set_defaults(func=cmd_config)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == '__main__':
    main()
