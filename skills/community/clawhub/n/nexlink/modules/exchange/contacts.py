"""
Exchange contacts (EWS) operations.
Supports CRUD + search for Contacts via Exchange Web Services.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Dict, List, Optional

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from exchangelib import Contact, Folder
    from exchangelib.indexed_properties import PhoneNumber, EmailAddress, PhysicalAddress

    HAS_EXCHANGELIB = True
except ImportError:
    HAS_EXCHANGELIB = False
    Contact = None  # type: ignore
    Folder = None  # type: ignore
    PhoneNumber = None
    EmailAddress = None
    PhysicalAddress = None

from connection import get_account
from utils import out, die, add_json_argument


def add_parser(subparser) -> None:
    """Add contacts subcommands to the CLI parser."""
    # contacts list
    list_parser = subparser.add_parser("list", help="List contacts")
    add_json_argument(list_parser)
    list_parser.add_argument("--limit", type=int, default=50, help="Max contacts (default: 50)")
    list_parser.add_argument("--folder", type=str, default="contacts", help="Contacts folder name")

    # contacts get
    get_parser = subparser.add_parser("get", help="Get a contact by ID")
    add_json_argument(get_parser)
    get_parser.add_argument("--id", required=True, help="Contact item ID")

    # contacts create
    create_parser = subparser.add_parser("create", help="Create a new contact")
    add_json_argument(create_parser)
    create_parser.add_argument("--name", required=True, help="Full name")
    create_parser.add_argument("--email", help="Email address")
    create_parser.add_argument("--phone", help="Phone number")
    create_parser.add_argument("--mobile", help="Mobile phone number")
    create_parser.add_argument("--org", help="Organization")
    create_parser.add_argument("--title", help="Job title")
    create_parser.add_argument("--note", help="Notes")
    create_parser.add_argument("--folder", type=str, default="contacts", help="Target contacts folder")

    # contacts update
    update_parser = subparser.add_parser("update", help="Update a contact")
    add_json_argument(update_parser)
    update_parser.add_argument("--id", required=True, help="Contact item ID")
    update_parser.add_argument("--name", help="Full name")
    update_parser.add_argument("--email", help="Email address")
    update_parser.add_argument("--phone", help="Phone number")
    update_parser.add_argument("--mobile", help="Mobile phone number")
    update_parser.add_argument("--org", help="Organization")
    update_parser.add_argument("--title", help="Job title")
    update_parser.add_argument("--note", help="Notes")

    # contacts delete
    delete_parser = subparser.add_parser("delete", help="Move a contact to trash")
    add_json_argument(delete_parser)
    delete_parser.add_argument("--id", required=True, help="Contact item ID")

    # contacts search
    search_parser = subparser.add_parser("search", help="Search contacts")
    add_json_argument(search_parser)
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")

    # Wire commands
    list_parser.set_defaults(func=cmd_list)
    get_parser.set_defaults(func=cmd_get)
    create_parser.set_defaults(func=cmd_create)
    update_parser.set_defaults(func=cmd_update)
    delete_parser.set_defaults(func=cmd_delete)
    search_parser.set_defaults(func=cmd_search)


def _get_contacts_folder(account, folder_name: str = "contacts") -> Folder:
    """Resolve the contacts folder by name."""
    try:
        return account.contacts  # this is the Contacts folder class, not root
    except Exception as exc:
        raise ValueError(f"Cannot access contacts folder '{folder_name}': {exc}")


def _contact_to_dict(contact: Contact) -> Dict[str, Any]:
    """Convert an exchangelib Contact to a serializable dict."""
    result: Dict[str, Any] = {
        "id": contact.id,
        "changekey": contact.changekey,
        "name": contact.display_name or contact.full_name or "",
        "given_name": contact.given_name or "",
        "surname": contact.surname or "",
        "email": "",
        "phone": "",
        "mobile": "",
        "org": contact.company_name or "",
        "title": contact.job_title or "",
        "note": contact.body or "",
    }

    # Email addresses (supports both exchangelib objects and plain dicts)
    if hasattr(contact, "email_addresses") and contact.email_addresses:
        for ea in contact.email_addresses:
            if isinstance(ea, dict):
                ea_label = ea.get("label", "")
                ea_email = ea.get("email", "")
            else:
                ea_label = getattr(ea, "label", "")
                ea_email = getattr(ea, "email", "") or ""
            if ea_label == "EmailAddress1" or not result["email"]:
                result["email"] = ea_email

    # Phone numbers — PhoneNumber objects with label and phone_number
    if hasattr(contact, "phone_numbers") and contact.phone_numbers:
        for pn in contact.phone_numbers:
            if not hasattr(pn, "phone_number"):
                continue
            label = (pn.label or "").lower() if hasattr(pn, "label") else ""
            if "business" in label or "primary" in label:
                result["phone"] = pn.phone_number or ""
            if "mobile" in label or "car" in label:
                result["mobile"] = pn.phone_number or ""
        # Fallback: if no phone set yet, take first
        if not result["phone"] and not result["mobile"] and len(contact.phone_numbers) > 0:
            pn = contact.phone_numbers[0]
            if hasattr(pn, "phone_number") and pn.phone_number:
                result["phone"] = pn.phone_number

    return result


def cmd_list(args: argparse.Namespace) -> None:
    """List contacts from Exchange."""
    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    account = get_account()
    folder = _get_contacts_folder(account, args.folder)

    try:
        contacts = list(folder.all().order_by("display_name")[: args.limit])
        result = {
            "ok": True,
            "count": len(contacts),
            "contacts": [_contact_to_dict(c) for c in contacts],
        }
        out(result)
    except Exception as e:
        die(f"Failed to list contacts: {e}")


def cmd_get(args: argparse.Namespace) -> None:
    """Get a single contact by ID."""
    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    account = get_account()

    try:
        contact = account.contacts.get(id=args.id)
        if not contact:
            die(f"Contact not found: {args.id}")
        out({"ok": True, "contact": _contact_to_dict(contact)})
    except Exception as e:
        die(f"Failed to get contact: {e}")


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new contact."""
    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    account = get_account()

    try:
        contact = Contact(
            folder=account.contacts,
            display_name=args.name,
            given_name=args.name.split(" ")[0] if args.name else None,
            surname=" ".join(args.name.split(" ")[1:]) if args.name and " " in args.name else None,
            company_name=args.org,
            job_title=args.title,
            body=args.note,
        )

        if args.email:
            contact.email_addresses = [EmailAddress(email=args.email, label="EmailAddress1")]

        if args.phone:
            contact.phone_numbers = [PhoneNumber(label="BusinessPhone", phone_number=args.phone)]

        if args.mobile:
            phones = list(contact.phone_numbers or [])
            phones.append(PhoneNumber(label="MobilePhone", phone_number=args.mobile))
            contact.phone_numbers = phones

        contact.save()

        out({
            "ok": True,
            "message": f"Contact '{args.name}' created",
            "contact": _contact_to_dict(contact),
        })
    except Exception as e:
        die(f"Failed to create contact: {e}")


def cmd_update(args: argparse.Namespace) -> None:
    """Update an existing contact."""
    confirm_or_die(f"Update contact {args.id}")

    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    account = get_account()

    try:
        contact = account.contacts.get(id=args.id)
        if not contact:
            die(f"Contact not found: {args.id}")

        changed = []
        if args.name:
            contact.display_name = args.name
            parts = args.name.split(" ", 1)
            contact.given_name = parts[0]
            contact.surname = parts[1] if len(parts) > 1 else ""
            changed.append("name")
        if args.email:
            contact.email_addresses = [EmailAddress(email=args.email, label="EmailAddress1")]
            changed.append("email")
        if args.phone:
            contact.phone_numbers = [PhoneNumber(label="BusinessPhone", phone_number=args.phone)]
            changed.append("phone")
        if args.mobile:
            phones = list(contact.phone_numbers or [])
            phones.append(PhoneNumber(label="MobilePhone", phone_number=args.mobile))
            contact.phone_numbers = phones
            changed.append("mobile")
        if args.org:
            contact.company_name = args.org
            changed.append("org")
        if args.title:
            contact.job_title = args.title
            changed.append("title")
        if args.note:
            contact.body = args.note
            changed.append("note")

        if not changed:
            die("No fields to update. Provide at least one --field to update.")

        contact.save()

        out({
            "ok": True,
            "message": f"Contact updated: {', '.join(changed)}",
            "contact": _contact_to_dict(contact),
        })
    except Exception as e:
        die(f"Failed to update contact: {e}")


def cmd_delete(args: argparse.Namespace) -> None:
    """Move contact to trash (soft delete)."""
    confirm_or_die(f"Delete contact {args.id}")

    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    account = get_account()

    try:
        contact = account.contacts.get(id=args.id)
        if not contact:
            die(f"Contact not found: {args.id}")

        name = contact.display_name or contact.full_name or args.id
        contact.move_to_trash()
        out({"ok": True, "message": f"Contact '{name}' moved to trash"})
    except Exception as e:
        die(f"Failed to delete contact: {e}")


def cmd_search(args: argparse.Namespace) -> None:
    """Search contacts by query string.

    Uses server-side filtering via exchangelib Q() for performance and
    correctness on large contact lists (>200 contacts).
    """
    if not HAS_EXCHANGELIB:
        die("exchangelib not available. Install: pip3 install exchangelib")

    from exchangelib import Q

    account = get_account()
    q = args.query.strip()

    if not q:
        die("Search query cannot be empty")

    try:
        # Server-side filter: match by name, company, or email
        q_lower = q.lower()
        query = (
            Q(display_name__contains=q_lower)
            | Q(given_name__contains=q_lower)
            | Q(surname__contains=q_lower)
            | Q(company_name__contains=q_lower)
            | Q(email_addresses__contains=q_lower)
        )

        limit = min(args.limit or 50, 500)
        contacts = list(
            account.contacts.filter(query).order_by("display_name")[:limit]
        )

        out({
            "ok": True,
            "query": args.query,
            "count": len(contacts),
            "contacts": [_contact_to_dict(c) for c in contacts],
        })
    except Exception as e:
        die(f"Failed to search contacts: {e}")
