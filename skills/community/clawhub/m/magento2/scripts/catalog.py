#!/usr/bin/env python3
"""Catalog management — products and categories."""

import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit, env_default, parse_csv_input

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_search(args):
    client = get_client(args.site)
    # OR filter between SKU and Name
    filters = [[
        {"field": "name", "value": f"%{args.query}%", "condition_type": "like"},
        {"field": "sku", "value": f"%{args.query}%", "condition_type": "like"}
    ]]
    try:
        result = client.search("products", filters=filters, page_size=args.limit)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No products found.")
        return

    rows = [
        [
            p.get("sku"),
            p.get("name"),
            f"{p.get('price', 0):.2f}",
            p.get("status", ""),
            p.get("type_id", ""),
        ]
        for p in items
    ]
    print(tabulate(rows, headers=["SKU", "Name", "Price", "Status", "Type"], tablefmt="github"))
    print(f"\n{len(items)} of {result.get('total_count', len(items))} products.")


def cmd_get(args):
    client = get_client(args.site)
    try:
        p = client.get(f"products/{args.sku}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    stock = None
    try:
        stock_info = client.get(f"stockItems/{args.sku}")
        stock = stock_info.get("qty")
    except MagentoAPIError:
        pass

    fields = [
        ("SKU", p.get("sku")),
        ("Name", p.get("name")),
        ("Price", f"{p.get('price', 0):.2f}"),
        ("Status", "Enabled" if p.get("status") == 1 else "Disabled"),
        ("Type", p.get("type_id")),
        ("Weight", p.get("weight")),
        ("Stock Qty", stock if stock is not None else "N/A"),
        ("Created", (p.get("created_at") or "")[:10]),
        ("Updated", (p.get("updated_at") or "")[:10]),
    ]
    print(tabulate(fields, tablefmt="simple"))

    cats = p.get("extension_attributes", {}).get("category_links", [])
    if cats:
        print(f"\nCategory IDs: {', '.join(str(c['category_id']) for c in cats)}")


def cmd_update_price(args):
    client = get_client(args.site)
    try:
        client.put(
            f"products/{args.sku}",
            {"product": {"sku": args.sku, "price": float(args.price)}},
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Price for {args.sku} updated to {float(args.price):.2f}.")


def cmd_update_attribute(args):
    client = get_client(args.site)
    custom_attrs = [{"attribute_code": args.attribute, "value": args.value}]
    body = {"product": {"sku": args.sku, "custom_attributes": custom_attrs}}
    # Price and name are top-level fields, not custom attributes
    if args.attribute == "price":
        body = {"product": {"sku": args.sku, "price": args.value}}
    elif args.attribute == "name":
        body = {"product": {"sku": args.sku, "name": args.value}}
    try:
        client.put(f"products/{args.sku}", body)
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Attribute '{args.attribute}' for {args.sku} updated to '{args.value}'.")


def cmd_categories(args):
    client = get_client(args.site)
    try:
        result = client.get("categories")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    def flatten(node, depth=0):
        rows = [(node.get("id"), "  " * depth + node.get("name", ""), node.get("level"), node.get("product_count", 0))]
        for child in node.get("children_data", []):
            rows.extend(flatten(child, depth + 1))
        return rows

    rows = flatten(result)
    print(tabulate(rows, headers=["ID", "Name", "Level", "Products"], tablefmt="github"))


def cmd_delete(args):
    client = get_client(args.site)
    try:
        client.delete(f"products/{args.sku}")
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Product {args.sku} deleted successfully.")


def cmd_update_status(args):
    client = get_client(args.site)
    status = 1 if args.status.lower() in ("enabled", "1", "true", "active") else 2
    try:
        client.put(f"products/{args.sku}", {"product": {"sku": args.sku, "status": status}})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Product {args.sku} status updated to {'Enabled' if status == 1 else 'Disabled'}.")


def cmd_bulk_update_price(args):
    client = get_client(args.site)
    delay_ms = env_default("OPENCLAW_DELAY_MS", args.delay_ms, 200)

    # Parse input
    items = parse_csv_input(args.csv, args.items, ["sku", "price"])
    if not items:
        print("No items provided. Use --csv or --items.")
        sys.exit(1)

    # Validate prices
    parsed: list[tuple[str, float]] = []
    for item in items:
        sku = item.get("sku", "")
        price_str = item.get("price", "")
        if not sku or not price_str:
            print(f"Skipping invalid entry: {item}")
            continue
        try:
            price = float(price_str)
        except ValueError:
            print(f"Skipping {sku}: invalid price '{price_str}'")
            continue
        parsed.append((sku, price))

    if not parsed:
        print("No valid items to process.")
        return

    # Large batch warning
    if len(parsed) > 20:
        print(f"Warning: {len(parsed)} items in batch — may trigger rate limiting. Consider splitting.")

    # Preview: batch fetch current prices
    skus = [sku for sku, _ in parsed]
    try:
        result = client.search("products", filters=[
            {"field": "sku", "value": ",".join(skus), "condition_type": "in"},
        ], page_size=len(skus))
        existing = {p.get("sku"): p.get("price", 0) for p in result.get("items", [])}
    except MagentoAPIError as e:
        print_error_and_exit(e)
        return

    # Build preview table
    preview_rows = []
    price_map = {}
    for sku, new_price in parsed:
        current = existing.get(sku)
        if current is None:
            preview_rows.append([sku, "NOT FOUND", f"{new_price:.2f}", "N/A"])
            continue
        current = float(current)
        price_map[sku] = (current, new_price)
        if current:
            change_pct = (new_price - current) / current * 100
            change_str = f"{change_pct:+.1f}%"
        else:
            # When current price is 0, percentage change is undefined; show absolute delta instead.
            if new_price == current:
                change_str = "+0.0%"
            else:
                change_str = f"{(new_price - current):+.2f}"
        preview_rows.append([sku, f"{current:.2f}", f"{new_price:.2f}", change_str])

    print("Price Change Preview:")
    print(tabulate(preview_rows, headers=["SKU", "Current Price", "New Price", "Change"], tablefmt="github"))

    not_found = [sku for sku, _ in parsed if sku not in existing]
    if not_found:
        print(f"\nNot found: {', '.join(not_found)}")

    if not args.execute:
        print(f"\n{len(price_map)} item(s) would be updated. Run with --execute to apply changes.")
        return

    # Execute
    success = 0
    failed: list[tuple[str, str]] = []
    for sku, (old_price, new_price) in price_map.items():
        try:
            client.put(f"products/{sku}", {"product": {"sku": sku, "price": new_price}})
            success += 1
        except MagentoAPIError as e:
            failed.append((sku, str(e)))
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

    print(f"\nUpdated: {success} | Failed: {len(failed)} | Total: {len(price_map)}")
    if failed:
        print("\nFailed items:")
        for sku, err in failed:
            print(f"  {sku}: {err}")
    if success > 0:
        print("\nTip: run `system.py cache-flush` to reflect price changes on the frontend.")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 catalog management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search products by name")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)

    p_get = sub.add_parser("get", help="Get product by SKU")
    p_get.add_argument("sku")

    p_price = sub.add_parser("update-price", help="Update product price")
    p_price.add_argument("sku")
    p_price.add_argument("price")

    p_attr = sub.add_parser("update-attribute", help="Update a product attribute")
    p_attr.add_argument("sku")
    p_attr.add_argument("attribute")
    p_attr.add_argument("value")

    p_status = sub.add_parser("update-status", help="Enable or disable a product")
    p_status.add_argument("sku")
    p_status.add_argument("status", choices=["enabled", "disabled"])

    p_del = sub.add_parser("delete", help="Delete a product")
    p_del.add_argument("sku")

    sub.add_parser("categories", help="List category tree")

    p_bulk_price = sub.add_parser("bulk-update-price", help="Bulk update product prices")
    p_bulk_price.add_argument("--csv", default=None, help="CSV file (sku,price)")
    p_bulk_price.add_argument("--items", default=None, help="Inline: SKU1:29.99,SKU2:49.99")
    p_bulk_price.add_argument("--execute", action="store_true", help="Execute changes (default: preview only)")
    p_bulk_price.add_argument("--delay-ms", type=int, default=None, help="Delay between writes in ms (default: 200)")

    args = parser.parse_args()
    {"search": cmd_search, "get": cmd_get, "update-price": cmd_update_price,
     "update-attribute": cmd_update_attribute, "update-status": cmd_update_status,
     "delete": cmd_delete, "categories": cmd_categories,
     "bulk-update-price": cmd_bulk_update_price}[args.command](args)


if __name__ == "__main__":
    main()