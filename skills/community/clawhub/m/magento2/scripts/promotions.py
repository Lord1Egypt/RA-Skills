#!/usr/bin/env python3
"""Promotions management — cart price rules and coupon codes."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_list(args):
    client = get_client(args.site)
    filters = []
    if args.active_only:
        filters.append({"field": "is_active", "value": "1", "condition_type": "eq"})
    try:
        result = client.search("salesRules/search", filters=filters, page_size=50)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No promotions found.")
        return

    rows = [
        [
            r.get("rule_id"),
            r.get("name"),
            r.get("coupon_type"),
            "Active" if r.get("is_active") else "Inactive",
            f"{r.get('discount_amount', 0):.0f}{'%' if r.get('simple_action') in ('by_percent', 'cart_fixed') else ''}",
            r.get("from_date") or "—",
            r.get("to_date") or "—",
        ]
        for r in items
    ]
    print(tabulate(rows, headers=["ID", "Name", "Type", "Status", "Discount", "From", "To"], tablefmt="github"))


def cmd_get(args):
    client = get_client(args.site)
    try:
        r = client.get(f"salesRules/{args.rule_id}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("Rule ID", r.get("rule_id")),
        ("Name", r.get("name")),
        ("Description", r.get("description") or "—"),
        ("Status", "Active" if r.get("is_active") else "Inactive"),
        ("Coupon Type", r.get("coupon_type")),
        ("Discount", f"{r.get('discount_amount', 0):.2f}"),
        ("Action", r.get("simple_action")),
        ("Uses Per Coupon", r.get("uses_per_coupon") or "Unlimited"),
        ("Uses Per Customer", r.get("uses_per_customer") or "Unlimited"),
        ("From Date", r.get("from_date") or "—"),
        ("To Date", r.get("to_date") or "—"),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_create_coupon(args):
    client = get_client(args.site)
    body = {
        "coupon": {
            "rule_id": int(args.rule_id),
            "code": args.code,
            "is_primary": False,
            "type": 1,
        }
    }
    if args.uses:
        body["coupon"]["usage_limit"] = int(args.uses)

    try:
        result = client.post("coupons", body)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    print(f"Coupon '{args.code}' created (ID: {result.get('coupon_id')}) for rule {args.rule_id}.")
    if args.uses:
        print(f"Usage limit: {args.uses}")


def cmd_disable(args):
    client = get_client(args.site)
    try:
        rule = client.get(f"salesRules/{args.rule_id}")
        rule["is_active"] = False
        client.put(f"salesRules/{args.rule_id}", {"rule": rule})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Promotion rule {args.rule_id} disabled.")


def cmd_coupon_stats(args):
    client = get_client(args.site)
    filters = [{"field": "code", "value": args.coupon_code, "condition_type": "eq"}]
    try:
        result = client.search("coupons/search", filters=filters, page_size=1)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print(f"Coupon '{args.coupon_code}' not found.")
        return

    c = items[0]
    fields = [
        ("Code", c.get("code")),
        ("Coupon ID", c.get("coupon_id")),
        ("Rule ID", c.get("rule_id")),
        ("Times Used", c.get("times_used", 0)),
        ("Usage Limit", c.get("usage_limit") or "Unlimited"),
        ("Is Primary", "Yes" if c.get("is_primary") else "No"),
        ("Expiration", c.get("expiration_date") or "—"),
    ]
    print(tabulate(fields, tablefmt="simple"))


def main():
    parser = argparse.ArgumentParser(description="Magento 2 promotions management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List cart price rules")
    p_list.add_argument("--active-only", action="store_true")

    p_get = sub.add_parser("get", help="Get a promotion rule by ID")
    p_get.add_argument("rule_id")

    p_coupon = sub.add_parser("create-coupon", help="Create a coupon code for a rule")
    p_coupon.add_argument("rule_id")
    p_coupon.add_argument("code")
    p_coupon.add_argument("--uses", type=int, help="Max usage limit")

    p_disable = sub.add_parser("disable", help="Disable a promotion rule")
    p_disable.add_argument("rule_id")

    p_stats = sub.add_parser("coupon-stats", help="Show usage stats for a coupon code")
    p_stats.add_argument("coupon_code")

    args = parser.parse_args()
    {"list": cmd_list, "get": cmd_get, "create-coupon": cmd_create_coupon,
     "disable": cmd_disable, "coupon-stats": cmd_coupon_stats}[args.command](args)


if __name__ == "__main__":
    main()
