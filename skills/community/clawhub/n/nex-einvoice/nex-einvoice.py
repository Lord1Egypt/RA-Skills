#!/usr/bin/env python3
"""
Nex E-Invoice - CLI Tool
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Belgian UBL e-invoice generator. Create Peppol BIS 3.0 compliant invoices via the command line.
Built by Nex AI (nex-ai.be)
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from decimal import Decimal

# Add lib directory to Python path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SKILL_DIR, "lib")
sys.path.insert(0, LIB_DIR)

# Import as package to handle relative imports
sys.path.insert(0, SKILL_DIR)

from lib import config
from lib.storage import (
    init_db, next_invoice_number, save_invoice, get_invoice, list_invoices,
    update_invoice_status, save_contact, get_contact, list_contacts,
    get_invoice_stats, search_invoices
)
from lib.ubl_generator import generate_invoice_xml, validate_vat_number, generate_payment_reference
from lib.nl_parser import parse_invoice_text

FOOTER = "[Nex E-Invoice by Nex AI | nex-ai.be]"


def _print_footer():
    print("\n%s" % FOOTER)


def _format_currency(value):
    """Format a decimal value as EUR currency."""
    if isinstance(value, str):
        value = Decimal(value)
    elif not isinstance(value, Decimal):
        value = Decimal(str(value))
    return f"€{value:.2f}"


def _load_seller_config():
    """Load seller configuration from file or environment."""
    seller_config_path = config.DATA_DIR / "seller.json"

    if seller_config_path.exists():
        try:
            with open(seller_config_path, "r") as f:
                return json.load(f)
        except Exception:
            pass

    # Build from environment
    return {
        "name": config.SELLER_NAME,
        "vat": config.SELLER_VAT,
        "street": config.SELLER_STREET,
        "city": config.SELLER_CITY,
        "postcode": config.SELLER_POSTCODE,
        "country": config.SELLER_COUNTRY,
        "email": config.SELLER_EMAIL,
        "phone": config.SELLER_PHONE,
        "kbo": config.SELLER_KBO,
        "peppol_id": config.SELLER_PEPPOL_ID,
    }


def _load_payment_config():
    """Load payment configuration from file or environment."""
    payment_config_path = config.DATA_DIR / "payment.json"

    if payment_config_path.exists():
        try:
            with open(payment_config_path, "r") as f:
                return json.load(f)
        except Exception:
            pass

    # Build from environment
    return {
        "iban": config.SELLER_IBAN,
        "bic": config.SELLER_BIC,
        "means_code": "30",
        "terms": f"Betaling binnen {config.PAYMENT_TERMS_DAYS} dagen",
    }


def _save_seller_config(seller_data):
    """Save seller configuration to file."""
    seller_config_path = config.DATA_DIR / "seller.json"
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(seller_config_path, "w") as f:
        json.dump(seller_data, f, indent=2)


def _save_payment_config(payment_data):
    """Save payment configuration to file."""
    payment_config_path = config.DATA_DIR / "payment.json"
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(payment_config_path, "w") as f:
        json.dump(payment_data, f, indent=2)


def _parse_line_flags(line_strings):
    """Parse --line flags in format 'QTYx DESC @ PRICE, RATE%'."""
    lines = []
    for line_str in line_strings:
        # Expected format: "3x broodjes @ 2.50, 6%"
        # Or simpler: "3x broodjes @ 2.50, 6"
        line_str = line_str.strip()

        # Try to parse quantity
        import re
        qty_match = re.search(r'^(\d+)\s*[x×]\s*(.+?)\s*@\s*([0-9.,]+)\s*,\s*(\d+)', line_str)

        if qty_match:
            qty = Decimal(qty_match.group(1))
            desc = qty_match.group(2).strip()
            price = Decimal(qty_match.group(3).replace(",", "."))
            btw_rate = int(qty_match.group(4))

            lines.append({
                "description": desc,
                "quantity": qty,
                "unit_price": price,
                "btw_rate": btw_rate,
                "unit_code": "C62"
            })

    return lines


def _lookup_or_create_contact(name, vat=None, email=None):
    """
    Lookup contact by name or VAT. If not found and name is provided,
    return contact data for use in invoice creation.
    """
    contact = None

    if vat:
        contact = get_contact(vat)
        if contact:
            return contact

    # Search by name
    contacts = list_contacts(search=name, limit=1)
    if contacts:
        return contacts[0]

    # Contact not found, return minimal data for invoice
    return {
        "name": name,
        "vat_number": vat,
        "email": email,
    }


# ============================================================
# CREATE
# ============================================================

def cmd_create(args):
    init_db()

    seller = _load_seller_config()
    payment = _load_payment_config()

    if not seller.get("vat"):
        print("Error: Seller VAT not configured. Run 'nex-einvoice config set-seller' first.", file=sys.stderr)
        sys.exit(1)

    parsed = None
    buyer_data = None
    lines = []

    # Determine input source
    if args.from_json:
        # Load from JSON file
        try:
            with open(args.from_json, "r") as f:
                json_data = json.load(f)
            buyer_data = json_data.get("buyer", {})
            lines = json_data.get("lines", [])
            parsed = {"buyer_name": buyer_data.get("name", "")}
        except Exception as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.buyer or args.line:
        # Parse structured input
        buyer_data = {
            "name": args.buyer,
            "vat": args.buyer_vat,
            "email": args.buyer_email,
        }
        lines = _parse_line_flags(args.line)
        parsed = {"buyer_name": args.buyer}

    elif args.text:
        # Parse natural language
        text = " ".join(args.text)
        parsed = parse_invoice_text(text)

        if parsed.get("errors"):
            for err in parsed["errors"]:
                print(f"Warning: {err}", file=sys.stderr)

        # Lookup buyer from contacts
        buyer_name = parsed.get("buyer_name")
        contact = _lookup_or_create_contact(buyer_name)
        buyer_data = {
            "name": contact.get("name") or buyer_name,
            "vat": contact.get("vat_number"),
            "email": contact.get("email"),
            "street": contact.get("street"),
            "city": contact.get("city"),
            "postcode": contact.get("postcode"),
            "country": contact.get("country", "BE"),
            "kbo": contact.get("kbo"),
            "peppol_id": contact.get("peppol_id"),
        }
        lines = parsed.get("lines", [])

    else:
        print("Usage: nex-einvoice create <text> | --buyer <name> [--buyer-vat VAT] --line <spec> [--line ...] | --from-json <file>", file=sys.stderr)
        sys.exit(1)

    if not buyer_data or not buyer_data.get("name"):
        print("Error: Buyer name not specified.", file=sys.stderr)
        sys.exit(1)

    if not lines:
        print("Error: No line items found.", file=sys.stderr)
        sys.exit(1)

    # Auto-save buyer to contacts if not already there
    if buyer_data.get("name") and buyer_data.get("vat"):
        existing_contact = get_contact(buyer_data["vat"])
        if not existing_contact:
            contact_data = {
                "name": buyer_data["name"],
                "vat_number": buyer_data["vat"],
                "email": buyer_data.get("email"),
                "street": buyer_data.get("street"),
                "city": buyer_data.get("city"),
                "postcode": buyer_data.get("postcode"),
                "country": buyer_data.get("country", "BE"),
                "peppol_id": buyer_data.get("peppol_id"),
            }
            if buyer_data.get("kbo"):
                contact_data["kbo_number"] = buyer_data.get("kbo")
            save_contact(contact_data)

    # Generate invoice number
    invoice_number = next_invoice_number(config.INVOICE_PREFIX)

    # Calculate totals
    subtotal_excl = Decimal("0")
    total_btw = Decimal("0")

    # Convert all line quantities and prices to floats for database storage
    processed_lines = []
    for line in lines:
        qty = Decimal(str(line.get("quantity", 0)))
        price = Decimal(str(line.get("unit_price", 0)))
        btw_rate = int(line.get("btw_rate", 21))

        line_total = qty * price
        btw_amount = line_total * Decimal(str(btw_rate)) / Decimal("100")

        subtotal_excl += line_total
        total_btw += btw_amount

        # Create a new line dict with float values for database
        processed_line = {
            "description": line.get("description", ""),
            "quantity": float(qty),
            "unit_code": line.get("unit_code", "C62"),
            "unit_price": float(price),
            "btw_rate": btw_rate,
            "btw_amount": float(btw_amount),
            "line_total": float(line_total),
        }
        processed_lines.append(processed_line)

    lines = processed_lines

    total_incl = subtotal_excl + total_btw

    # Generate payment reference
    payment_ref = generate_payment_reference(invoice_number)

    # Prepare invoice data for database
    today = dt.date.today()
    due_date = today + dt.timedelta(days=config.PAYMENT_TERMS_DAYS)

    invoice_db_data = {
        "invoice_number": invoice_number,
        "issue_date": today.isoformat(),
        "due_date": due_date.isoformat(),
        "seller_vat": seller["vat"],
        "seller_name": seller["name"],
        "buyer_vat": buyer_data.get("vat", ""),
        "buyer_name": buyer_data.get("name", ""),
        "buyer_street": buyer_data.get("street", ""),
        "buyer_city": buyer_data.get("city", ""),
        "buyer_postcode": buyer_data.get("postcode", ""),
        "buyer_country": buyer_data.get("country", "BE"),
        "buyer_email": buyer_data.get("email", ""),
        "buyer_kbo": buyer_data.get("kbo", ""),
        "buyer_peppol_id": buyer_data.get("peppol_id", ""),
        "subtotal_excl": float(subtotal_excl),
        "total_btw": float(total_btw),
        "total_incl": float(total_incl),
        "currency": config.DEFAULT_CURRENCY,
        "payment_terms": config.PAYMENT_TERMS_DAYS,
        "payment_reference": payment_ref,
        "status": "draft",
        "lines": lines,
    }

    # Save to database
    invoice_id = save_invoice(invoice_db_data)

    # Generate UBL XML
    ubl_data = {
        "invoice_number": invoice_number,
        "issue_date": today.isoformat(),
        "due_date": due_date.isoformat(),
        "type_code": "380",
        "currency": config.DEFAULT_CURRENCY,
        "seller": {
            "name": seller["name"],
            "vat": seller["vat"],
            "street": seller.get("street", ""),
            "city": seller.get("city", ""),
            "postcode": seller.get("postcode", ""),
            "country": seller.get("country", "BE"),
            "email": seller.get("email", ""),
            "phone": seller.get("phone", ""),
            "kbo": seller.get("kbo", ""),
            "peppol_id": seller.get("peppol_id", ""),
        },
        "buyer": {
            "name": buyer_data.get("name", ""),
            "vat": buyer_data.get("vat", ""),
            "street": buyer_data.get("street", ""),
            "city": buyer_data.get("city", ""),
            "postcode": buyer_data.get("postcode", ""),
            "country": buyer_data.get("country", "BE"),
            "email": buyer_data.get("email", ""),
            "kbo": buyer_data.get("kbo", ""),
            "peppol_id": buyer_data.get("peppol_id", ""),
        },
        "payment": {
            "means_code": payment.get("means_code", "30"),
            "reference": payment_ref,
            "terms": payment.get("terms", ""),
            "iban": payment.get("iban", ""),
            "bic": payment.get("bic", ""),
        },
        "lines": lines,
    }

    xml_content = generate_invoice_xml(ubl_data)

    # Save XML to export directory
    config.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    xml_path = config.EXPORT_DIR / f"{invoice_number}.xml"
    with open(xml_path, "w") as f:
        f.write(xml_content)

    # Update invoice with XML path
    from storage import _connect
    with _connect() as conn:
        conn.execute(
            "UPDATE invoices SET xml_path = ? WHERE invoice_number = ?",
            (str(xml_path), invoice_number)
        )

    # Print summary
    print(f"Invoice: {invoice_number}")
    print(f"Status: draft")
    print(f"Date: {today.isoformat()} | Due: {due_date.isoformat()}")
    print("---")
    print(f"Seller: {seller['name']} ({seller['vat']})")
    print(f"Buyer: {buyer_data.get('name', '')} ({buyer_data.get('vat', '')})")
    print("---")
    print("Lines:")
    for idx, line in enumerate(lines, 1):
        qty = Decimal(str(line.get("quantity", 0)))
        price = Decimal(str(line.get("unit_price", 0)))
        btw_rate = int(line.get("btw_rate", 21))
        line_total = qty * price
        print(f"  {idx}. {qty}x {line.get('description', '')} @ {_format_currency(price)} {btw_rate}% BTW = {_format_currency(line_total)}")
    print("---")
    print(f"Subtotal (excl. BTW):  {_format_currency(subtotal_excl)}")
    print(f"BTW (avg {int(Decimal(str(total_btw)) / Decimal(str(subtotal_excl)) * Decimal(100)) if subtotal_excl > 0 else 0}%): {_format_currency(total_btw)}")
    print(f"Total (incl. BTW):     {_format_currency(total_incl)}")
    print("---")
    print(f"Payment ref: {payment_ref}")
    print(f"XML: {xml_path}")

    _print_footer()


# ============================================================
# SHOW
# ============================================================

def cmd_show(args):
    init_db()

    invoice = get_invoice(args.invoice_number)
    if not invoice:
        print(f"Invoice {args.invoice_number} not found.", file=sys.stderr)
        sys.exit(1)

    output_json = args.output == "json"

    if output_json:
        # Remove SQLite id field
        invoice_copy = {k: v for k, v in invoice.items() if k != "id"}
        # Convert lines similarly
        lines_copy = [{k: v for k, v in line.items() if k != "id" and k != "invoice_id"} for line in invoice.get("lines", [])]
        invoice_copy["lines"] = lines_copy
        print(json.dumps(invoice_copy, indent=2))
        return

    # Human-readable format
    print(f"Invoice: {invoice['invoice_number']}")
    print(f"Status: {invoice['status']}")
    print(f"Date: {invoice['issue_date']} | Due: {invoice['due_date']}")
    print("---")
    print(f"Seller: {invoice['seller_name']} ({invoice['seller_vat']})")
    print(f"Buyer: {invoice['buyer_name']} ({invoice['buyer_vat']})")
    print("---")
    print("Lines:")

    for line in invoice.get("lines", []):
        qty = Decimal(str(line.get("quantity", 0)))
        price = Decimal(str(line.get("unit_price", 0)))
        btw_rate = int(line.get("btw_rate", 21))
        line_total = qty * price
        print(f"  {line['line_number']}. {qty}x {line.get('description', '')} @ {_format_currency(price)} {btw_rate}% BTW = {_format_currency(line_total)}")

    print("---")
    print(f"Subtotal (excl. BTW):  {_format_currency(invoice['subtotal_excl'])}")
    print(f"BTW:                   {_format_currency(invoice['total_btw'])}")
    print(f"Total (incl. BTW):     {_format_currency(invoice['total_incl'])}")
    print("---")
    print(f"Payment ref: {invoice.get('payment_reference', '')}")
    print(f"XML: {invoice.get('xml_path', 'not generated')}")

    _print_footer()


# ============================================================
# LIST
# ============================================================

def cmd_list(args):
    init_db()

    invoices = list_invoices(
        status=args.status,
        since=args.since,
        until=args.until,
        buyer=args.buyer,
        limit=args.limit
    )

    output_json = args.output == "json"

    if output_json:
        invoices_clean = [{k: v for k, v in inv.items() if k != "id"} for inv in invoices]
        print(json.dumps(invoices_clean, indent=2))
        return

    # Human-readable format
    print(f"Invoices ({len(invoices)} results)")
    if args.status:
        print(f"Filter: status={args.status}")
    if args.since or args.until:
        date_range = f"{args.since or 'start'} to {args.until or 'now'}"
        print(f"Filter: date range {date_range}")
    if args.buyer:
        print(f"Filter: buyer={args.buyer}")
    print("---")

    for inv in invoices:
        status = inv["status"]
        total = _format_currency(inv["total_incl"])
        print(f"- {inv['invoice_number']} | {inv['issue_date']} | {inv['buyer_name'][:30]:30} | {total:>10} | {status}")

    if not invoices:
        print("No invoices found.")

    _print_footer()


# ============================================================
# SEARCH
# ============================================================

def cmd_search(args):
    init_db()

    query = " ".join(args.query)
    if not query:
        print("Usage: nex-einvoice search <query>", file=sys.stderr)
        sys.exit(1)

    results = search_invoices(query, limit=args.limit)

    output_json = args.output == "json"

    if output_json:
        results_clean = [{k: v for k, v in r.items() if k != "id"} for r in results]
        print(json.dumps(results_clean, indent=2))
        return

    # Human-readable format
    print(f"Search results for: {query}")
    print("---")

    for r in results:
        status = r.get("status", "?")
        total = _format_currency(r.get("total_incl", 0))
        print(f"- {r['invoice_number']} | {r['buyer_name'][:30]:30} | {total:>10} | {status}")
        if "matched_lines" in r and r["matched_lines"]:
            lines = r["matched_lines"].split(" | ")
            for line in lines[:2]:
                print(f"    {line[:60]}")

    if not results:
        print("No invoices found.")

    _print_footer()


# ============================================================
# STATUS
# ============================================================

def cmd_status(args):
    init_db()

    invoice = get_invoice(args.invoice_number)
    if not invoice:
        print(f"Invoice {args.invoice_number} not found.", file=sys.stderr)
        sys.exit(1)

    valid_statuses = ["draft", "sent", "paid", "cancelled"]
    if args.new_status not in valid_statuses:
        print(f"Invalid status. Must be one of: {', '.join(valid_statuses)}", file=sys.stderr)
        sys.exit(1)

    update_invoice_status(args.invoice_number, args.new_status)

    print(f"{args.invoice_number}: {invoice['status']} -> {args.new_status}")

    _print_footer()


# ============================================================
# XML
# ============================================================

def cmd_xml(args):
    init_db()

    invoice = get_invoice(args.invoice_number)
    if not invoice:
        print(f"Invoice {args.invoice_number} not found.", file=sys.stderr)
        sys.exit(1)

    # Prepare UBL data
    lines = invoice.get("lines", [])

    ubl_lines = []
    for line in lines:
        ubl_lines.append({
            "description": line["description"],
            "quantity": line["quantity"],
            "unit_code": line.get("unit_code", "C62"),
            "unit_price": line["unit_price"],
            "btw_rate": line["btw_rate"],
        })

    payment = _load_payment_config()

    ubl_data = {
        "invoice_number": invoice["invoice_number"],
        "issue_date": invoice["issue_date"],
        "due_date": invoice["due_date"],
        "type_code": "380",
        "currency": invoice.get("currency", "EUR"),
        "seller": {
            "name": invoice["seller_name"],
            "vat": invoice["seller_vat"],
        },
        "buyer": {
            "name": invoice["buyer_name"],
            "vat": invoice["buyer_vat"],
            "street": invoice.get("buyer_street", ""),
            "city": invoice.get("buyer_city", ""),
            "postcode": invoice.get("buyer_postcode", ""),
            "country": invoice.get("buyer_country", "BE"),
            "email": invoice.get("buyer_email", ""),
            "kbo": invoice.get("buyer_kbo", ""),
            "peppol_id": invoice.get("buyer_peppol_id", ""),
        },
        "payment": {
            "means_code": payment.get("means_code", "30"),
            "reference": invoice.get("payment_reference", ""),
            "terms": payment.get("terms", ""),
            "iban": payment.get("iban", ""),
            "bic": payment.get("bic", ""),
        },
        "lines": ubl_lines,
    }

    xml_content = generate_invoice_xml(ubl_data)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(xml_content)
        print(f"Exported to {output_path}")
    else:
        print(xml_content)

    _print_footer()


# ============================================================
# CONTACT
# ============================================================

def cmd_contact(args):
    init_db()

    action = args.action

    if action == "add":
        if not args.name:
            print("Usage: nex-einvoice contact add --name <name> [--vat VAT] [--street <street>] [--city <city>] [--postcode <code>]", file=sys.stderr)
            sys.exit(1)

        contact_data = {
            "name": args.name,
            "vat_number": args.vat,
            "street": args.street,
            "city": args.city,
            "postcode": args.postcode,
            "country": args.country or "BE",
            "email": args.email,
            "phone": args.phone,
        }

        contact_id = save_contact(contact_data)
        print(f"Contact added: {args.name} (ID: {contact_id})")

    elif action == "show":
        if not args.vat:
            print("Usage: nex-einvoice contact show <vat>", file=sys.stderr)
            sys.exit(1)

        contact = get_contact(args.vat)
        if not contact:
            print(f"Contact with VAT {args.vat} not found.", file=sys.stderr)
            sys.exit(1)

        print(f"Name: {contact.get('name', '')}")
        print(f"VAT: {contact.get('vat_number', '')}")
        if contact.get("street"):
            print(f"Street: {contact.get('street', '')}")
        if contact.get("city"):
            print(f"City: {contact.get('city', '')}")
        if contact.get("postcode"):
            print(f"Postcode: {contact.get('postcode', '')}")
        if contact.get("email"):
            print(f"Email: {contact.get('email', '')}")
        if contact.get("phone"):
            print(f"Phone: {contact.get('phone', '')}")

    elif action == "list":
        contacts = list_contacts(search=args.search, limit=args.limit)

        print(f"Contacts ({len(contacts)} results)")
        if args.search:
            print(f"Filter: search='{args.search}'")
        print("---")

        for c in contacts:
            vat = c.get("vat_number", "")
            print(f"- {c['name'][:40]:40} | VAT: {vat:15} | {c.get('city', '')}")

        if not contacts:
            print("No contacts found.")

    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# STATS
# ============================================================

def cmd_stats(args):
    init_db()

    year = args.year or dt.datetime.now().year
    stats = get_invoice_stats(year=year)

    print(f"Invoice Statistics ({year})")
    print("---")
    print(f"Total invoices: {stats['invoice_count']}")
    print(f"Total invoiced: {_format_currency(stats['total_invoiced'])}")
    print(f"Total BTW: {_format_currency(stats['total_btw'])}")
    print("---")
    print("By status:")
    for status, data in sorted(stats["by_status"].items()):
        count = data["count"]
        total = _format_currency(data["total"])
        print(f"- {status:10} {count:3} invoice(s)  {total}")

    _print_footer()


# ============================================================
# VALIDATE
# ============================================================

def cmd_validate(args):
    vat = args.vat.upper().strip()
    is_valid = validate_vat_number(vat)

    if is_valid:
        print(f"{vat}: valid")
    else:
        print(f"{vat}: invalid")
        sys.exit(1)

    _print_footer()


# ============================================================
# CONFIG
# ============================================================

def cmd_config(args):
    action = args.action

    if action == "show":
        seller = _load_seller_config()
        payment = _load_payment_config()

        print("Nex E-Invoice Configuration")
        print("---")
        print(f"Data directory: {config.DATA_DIR}")
        print(f"Database: {config.DB_PATH}")
        print(f"Export directory: {config.EXPORT_DIR}")
        print("---")
        print("Seller:")
        print(f"  Name: {seller.get('name', 'not set')}")
        print(f"  VAT: {seller.get('vat', 'not set')}")
        print(f"  Street: {seller.get('street', 'not set')}")
        print(f"  City: {seller.get('city', 'not set')}")
        print(f"  Postcode: {seller.get('postcode', 'not set')}")
        print("---")
        print("Payment:")
        print(f"  IBAN: {seller.get('iban', 'not set')}")
        print(f"  BIC: {seller.get('bic', 'not set')}")

    elif action == "set-seller":
        if not args.name:
            print("Usage: nex-einvoice config set-seller --name <name> --vat <vat> [--street <street>] [--city <city>] [--postcode <code>]", file=sys.stderr)
            sys.exit(1)

        seller = {
            "name": args.name,
            "vat": args.vat,
            "street": args.street,
            "city": args.city,
            "postcode": args.postcode,
            "country": args.country or "BE",
            "email": args.email,
            "phone": args.phone,
            "kbo": args.kbo,
            "peppol_id": args.peppol_id,
        }

        _save_seller_config(seller)
        print(f"Seller configured: {args.name}")

    elif action == "set-payment":
        payment = {
            "iban": args.iban,
            "bic": args.bic,
            "means_code": "30",
        }

        _save_payment_config(payment)
        print("Payment configured")

    elif action == "set-prefix":
        # Update prefix in environment or config file
        if not args.prefix:
            print("Usage: nex-einvoice config set-prefix <prefix>", file=sys.stderr)
            sys.exit(1)

        prefix_config_path = config.DATA_DIR / "prefix.txt"
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(prefix_config_path, "w") as f:
            f.write(args.prefix)

        print(f"Invoice prefix set to: {args.prefix}")

    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# SERVICE
# ============================================================

def cmd_service(args):
    action = args.action

    if action == "status":
        print("Nex E-Invoice service")
        print("---")
        print("Status: Ready")
        print("Database: %s" % config.DB_PATH)
        print("Export dir: %s" % config.EXPORT_DIR)

    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)

    _print_footer()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        prog="nex-einvoice",
        description="Belgian UBL e-invoice generator for Peppol BIS 3.0 compliance",
        add_help=True
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # CREATE
    p_create = subparsers.add_parser("create", help="Create invoice from natural language or structured input")
    p_create.add_argument("text", nargs="*", help="Natural language invoice description")
    p_create.add_argument("--buyer", help="Buyer company name")
    p_create.add_argument("--buyer-vat", help="Buyer VAT number")
    p_create.add_argument("--buyer-email", help="Buyer email")
    p_create.add_argument("--line", action="append", help="Line item in format: QTYx DESC @ PRICE, RATE")
    p_create.add_argument("--from-json", help="Load invoice data from JSON file")
    p_create.set_defaults(func=cmd_create)

    # SHOW
    p_show = subparsers.add_parser("show", help="Display invoice")
    p_show.add_argument("invoice_number", help="Invoice number (e.g., INV-2026-0001)")
    p_show.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    p_show.set_defaults(func=cmd_show)

    # LIST
    p_list = subparsers.add_parser("list", help="List invoices with optional filters")
    p_list.add_argument("--status", choices=["draft", "sent", "paid", "cancelled"], help="Filter by status")
    p_list.add_argument("--since", help="Start date (YYYY-MM-DD)")
    p_list.add_argument("--until", help="End date (YYYY-MM-DD)")
    p_list.add_argument("--buyer", help="Filter by buyer name")
    p_list.add_argument("--limit", type=int, default=50, help="Max results")
    p_list.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    p_list.set_defaults(func=cmd_list)

    # SEARCH
    p_search = subparsers.add_parser("search", help="Full-text search across invoices")
    p_search.add_argument("query", nargs="+", help="Search query")
    p_search.add_argument("--limit", type=int, default=30, help="Max results")
    p_search.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    p_search.set_defaults(func=cmd_search)

    # STATUS
    p_status = subparsers.add_parser("status", help="Update invoice status")
    p_status.add_argument("invoice_number", help="Invoice number")
    p_status.add_argument("new_status", choices=["draft", "sent", "paid", "cancelled"], help="New status")
    p_status.set_defaults(func=cmd_status)

    # XML
    p_xml = subparsers.add_parser("xml", help="Regenerate or export invoice XML")
    p_xml.add_argument("invoice_number", help="Invoice number")
    p_xml.add_argument("--output", help="Output file path")
    p_xml.set_defaults(func=cmd_xml)

    # CONTACT
    p_contact = subparsers.add_parser("contact", help="Manage contacts")
    p_contact_sub = p_contact.add_subparsers(dest="action", help="Contact actions")

    p_contact_add = p_contact_sub.add_parser("add", help="Add contact")
    p_contact_add.add_argument("--name", required=True, help="Company name")
    p_contact_add.add_argument("--vat", help="VAT number")
    p_contact_add.add_argument("--street", help="Street address")
    p_contact_add.add_argument("--city", help="City")
    p_contact_add.add_argument("--postcode", help="Postcode")
    p_contact_add.add_argument("--country", default="BE", help="Country code")
    p_contact_add.add_argument("--email", help="Email address")
    p_contact_add.add_argument("--phone", help="Phone number")

    p_contact_show = p_contact_sub.add_parser("show", help="Show contact")
    p_contact_show.add_argument("vat", help="VAT number")

    p_contact_list = p_contact_sub.add_parser("list", help="List contacts")
    p_contact_list.add_argument("--search", help="Search by name/email/VAT")
    p_contact_list.add_argument("--limit", type=int, default=50, help="Max results")

    p_contact.set_defaults(func=cmd_contact)

    # STATS
    p_stats = subparsers.add_parser("stats", help="Invoice statistics")
    p_stats.add_argument("--year", type=int, help="Year (default: current year)")
    p_stats.set_defaults(func=cmd_stats)

    # VALIDATE
    p_validate = subparsers.add_parser("validate", help="Validate VAT number")
    p_validate.add_argument("vat", help="VAT number (e.g., BE0123456789)")
    p_validate.set_defaults(func=cmd_validate)

    # CONFIG
    p_config = subparsers.add_parser("config", help="Configuration management")
    p_config_sub = p_config.add_subparsers(dest="action", help="Config actions")

    p_config_show = p_config_sub.add_parser("show", help="Show configuration")

    p_config_seller = p_config_sub.add_parser("set-seller", help="Configure seller details")
    p_config_seller.add_argument("--name", required=True, help="Seller name")
    p_config_seller.add_argument("--vat", required=True, help="VAT number")
    p_config_seller.add_argument("--street", help="Street address")
    p_config_seller.add_argument("--city", help="City")
    p_config_seller.add_argument("--postcode", help="Postcode")
    p_config_seller.add_argument("--country", default="BE", help="Country code")
    p_config_seller.add_argument("--email", help="Email address")
    p_config_seller.add_argument("--phone", help="Phone number")
    p_config_seller.add_argument("--kbo", help="KBO number")
    p_config_seller.add_argument("--peppol-id", help="Peppol ID")

    p_config_payment = p_config_sub.add_parser("set-payment", help="Configure payment details")
    p_config_payment.add_argument("--iban", required=True, help="IBAN")
    p_config_payment.add_argument("--bic", required=True, help="BIC")

    p_config_prefix = p_config_sub.add_parser("set-prefix", help="Set invoice prefix")
    p_config_prefix.add_argument("prefix", help="Invoice prefix (e.g., INV)")

    p_config.set_defaults(func=cmd_config)

    # SERVICE
    p_service = subparsers.add_parser("service", help="Service status")
    p_service.add_argument("action", choices=["status"], help="Action")
    p_service.set_defaults(func=cmd_service)

    # Initialize database
    init_db()

    # Parse and execute
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
