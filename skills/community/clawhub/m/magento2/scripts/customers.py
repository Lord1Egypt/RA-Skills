#!/usr/bin/env python3
"""Customer management — search, get, order history, update group."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_search(args):
    client = get_client(args.site)
    # OR filter between Email, Firstname and Lastname
    filters = [[
        {"field": "email", "value": f"%{args.query}%", "condition_type": "like"},
        {"field": "firstname", "value": f"%{args.query}%", "condition_type": "like"},
        {"field": "lastname", "value": f"%{args.query}%", "condition_type": "like"}
    ]]
    try:
        result = client.search("customers/search", filters=filters, page_size=args.limit)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No customers found.")
        return

    rows = [
        [
            c.get("id"),
            f"{c.get('firstname', '')} {c.get('lastname', '')}".strip(),
            c.get("email"),
            c.get("group_id"),
            (c.get("created_at") or "")[:10],
        ]
        for c in items
    ]
    print(tabulate(rows, headers=["ID", "Name", "Email", "Group", "Created"], tablefmt="github"))
    print(f"\n{len(items)} of {result.get('total_count', len(items))} customers.")


def cmd_get(args):
    client = get_client(args.site)
    try:
        c = client.get(f"customers/{args.customer_id}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("ID", c.get("id")),
        ("Name", f"{c.get('firstname', '')} {c.get('lastname', '')}".strip()),
        ("Email", c.get("email")),
        ("Group ID", c.get("group_id")),
        ("Created", (c.get("created_at") or "")[:10]),
        ("Updated", (c.get("updated_at") or "")[:10]),
        ("DOB", c.get("dob") or "—"),
        ("Gender", {1: "Male", 2: "Female"}.get(c.get("gender"), "—")),
    ]
    print(tabulate(fields, tablefmt="simple"))

    addrs = c.get("addresses", [])
    if addrs:
        default = [a for a in addrs if a.get("default_billing") or a.get("default_shipping")]
        addr = default[0] if default else addrs[0]
        print(f"\nDefault address: {', '.join(filter(None, addr.get('street', [])))} "
              f"{addr.get('city', '')}, {addr.get('region', {}).get('region', '')} "
              f"{addr.get('postcode', '')} {addr.get('country_id', '')}")


def cmd_orders(args):
    client = get_client(args.site)
    filters = [{"field": "customer_id", "value": args.customer_id, "condition_type": "eq"}]
    try:
        result = client.search("orders", filters=filters, page_size=20, sort_field="created_at", sort_dir="DESC")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print(f"No orders found for customer {args.customer_id}.")
        return

    rows = [
        [
            o.get("increment_id"),
            o.get("status"),
            f"{o.get('base_grand_total', 0):.2f} {o.get('base_currency_code', '')}",
            (o.get("created_at") or "")[:10],
        ]
        for o in items
    ]
    print(tabulate(rows, headers=["Order #", "Status", "Total", "Date"], tablefmt="github"))
    total_spent = sum(o.get("base_grand_total", 0) for o in items)
    currency = items[0].get("base_currency_code", "") if items else ""
    print(f"\nTotal spent: {total_spent:.2f} {currency} across {len(items)} orders.")


def cmd_update_group(args):
    client = get_client(args.site)
    try:
        c = client.get(f"customers/{args.customer_id}")
        c["group_id"] = int(args.group_id)
        client.put(f"customers/{args.customer_id}", {"customer": c})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Customer {args.customer_id} moved to group {args.group_id}.")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 customer management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search customers by email or name")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)

    p_get = sub.add_parser("get", help="Get customer by ID")
    p_get.add_argument("customer_id")

    p_orders = sub.add_parser("orders", help="Get order history for a customer")
    p_orders.add_argument("customer_id")

    p_group = sub.add_parser("update-group", help="Update customer group")
    p_group.add_argument("customer_id")
    p_group.add_argument("group_id")

    args = parser.parse_args()
    {"search": cmd_search, "get": cmd_get, "orders": cmd_orders, "update-group": cmd_update_group}[args.command](args)


if __name__ == "__main__":
    main()