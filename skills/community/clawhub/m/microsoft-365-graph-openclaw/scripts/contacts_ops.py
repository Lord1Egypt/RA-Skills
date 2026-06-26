#!/usr/bin/env python3
"""Manage Outlook contacts via Microsoft Graph."""
import argparse
import json

from utils import append_log, authorized_request, graph_url, cli_main


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage contacts via Microsoft Graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List contacts.")
    p_list.add_argument("--top", type=int, default=25, help="Maximum number of contacts.")
    p_list.add_argument("--search", help="Search text to filter by display name or email.")

    p_get = sub.add_parser("get", help="Get a contact by ID.")
    p_get.add_argument("contact_id", help="Contact ID")

    p_create = sub.add_parser("create", help="Create a contact.")
    p_create.add_argument("--given-name", required=True, help="Given name")
    p_create.add_argument("--surname", required=True, help="Surname")
    p_create.add_argument("--email", required=True, help="Primary email address")
    p_create.add_argument("--mobile", help="Mobile phone")
    p_create.add_argument("--company", help="Company name")

    p_update = sub.add_parser("update", help="Update a contact.")
    p_update.add_argument("contact_id", help="Contact ID")
    p_update.add_argument("--given-name", help="Given name")
    p_update.add_argument("--surname", help="Surname")
    p_update.add_argument("--email", help="Primary email address")
    p_update.add_argument("--mobile", help="Mobile phone")
    p_update.add_argument("--company", help="Company name")

    p_delete = sub.add_parser("delete", help="Delete a contact.")
    p_delete.add_argument("contact_id", help="Contact ID")

    return parser


def handle_list(args: argparse.Namespace) -> None:
    params = {
        "$top": args.top,
        "$select": "id,displayName,givenName,surname,emailAddresses,mobilePhone,companyName",
    }
    if args.search:
        search = args.search.replace("'", "''")
        params["$filter"] = (
            f"contains(displayName,'{search}') or "
            f"contains(givenName,'{search}') or "
            f"contains(surname,'{search}')"
        )
    resp = authorized_request("GET", graph_url("/me/contacts"), params=params)
    data = resp.json()
    append_log({"action": "contacts_list", "count": len(data.get("value", [])), "search": args.search})
    print(json.dumps(data, indent=2))


def handle_get(args: argparse.Namespace) -> None:
    resp = authorized_request("GET", graph_url(f"/me/contacts/{args.contact_id}"))
    data = resp.json()
    append_log({"action": "contacts_get", "id": args.contact_id})
    print(json.dumps(data, indent=2))


def handle_create(args: argparse.Namespace) -> None:
    payload = {
        "givenName": args.given_name,
        "surname": args.surname,
        "emailAddresses": [{"address": args.email, "name": f"{args.given_name} {args.surname}".strip()}],
    }
    if args.mobile:
        payload["mobilePhone"] = args.mobile
    if args.company:
        payload["companyName"] = args.company
    resp = authorized_request("POST", graph_url("/me/contacts"), json=payload)
    data = resp.json()
    append_log({"action": "contacts_create", "id": data.get("id"), "email": args.email})
    print(json.dumps(data, indent=2))


def handle_update(args: argparse.Namespace) -> None:
    patch = {}
    if args.given_name is not None:
        patch["givenName"] = args.given_name
    if args.surname is not None:
        patch["surname"] = args.surname
    if args.email is not None:
        display = " ".join(v for v in [args.given_name, args.surname] if v) or args.email
        patch["emailAddresses"] = [{"address": args.email, "name": display}]
    if args.mobile is not None:
        patch["mobilePhone"] = args.mobile
    if args.company is not None:
        patch["companyName"] = args.company
    if not patch:
        raise SystemExit("No fields to update.")
    authorized_request("PATCH", graph_url(f"/me/contacts/{args.contact_id}"), json=patch)
    append_log({"action": "contacts_update", "id": args.contact_id, "fields": list(patch.keys())})
    print("Contact updated.")


def handle_delete(args: argparse.Namespace) -> None:
    authorized_request("DELETE", graph_url(f"/me/contacts/{args.contact_id}"))
    append_log({"action": "contacts_delete", "id": args.contact_id})
    print("Contact deleted.")


def handler() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list":
        handle_list(args)
    elif args.command == "get":
        handle_get(args)
    elif args.command == "create":
        handle_create(args)
    elif args.command == "update":
        handle_update(args)
    elif args.command == "delete":
        handle_delete(args)


if __name__ == "__main__":
    cli_main(handler)
