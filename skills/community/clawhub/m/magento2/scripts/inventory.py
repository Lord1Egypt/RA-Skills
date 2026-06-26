#!/usr/bin/env python3
"""Inventory management — stock levels, updates, low-stock alerts."""

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


def cmd_check(args):
    client = get_client(args.site)
    try:
        item = client.get(f"stockItems/{args.sku}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("SKU", args.sku),
        ("Qty", item.get("qty")),
        ("In Stock", "Yes" if item.get("is_in_stock") else "No"),
        ("Manage Stock", "Yes" if item.get("manage_stock") else "No"),
        ("Min Qty", item.get("min_qty")),
        ("Backorders", {0: "No", 1: "Allow (no notify)", 2: "Allow (notify)"}.get(item.get("backorders"), "Unknown")),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_update(args):
    client = get_client(args.site)
    try:
        current = client.get(f"stockItems/{args.sku}")
        item_id = current.get("item_id")
        current["qty"] = float(args.qty)
        current["is_in_stock"] = float(args.qty) > 0
        client.put(f"products/{args.sku}/stockItems/{item_id}", {"stockItem": current})
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Stock for {args.sku} updated to {args.qty}.")


def cmd_low_stock(args):
    client = get_client(args.site)
    threshold = args.threshold

    # Fetch all enabled, in-catalog products and check their stock
    try:
        result = client.search(
            "stockItems",
            filters=[{"field": "qty", "value": str(threshold), "condition_type": "lteq"},
                     {"field": "manage_stock", "value": "1", "condition_type": "eq"}],
            page_size=100,
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print(f"No products below stock threshold of {threshold}.")
        return

    rows = [
        [i.get("sku"), i.get("qty"), "Yes" if i.get("is_in_stock") else "No"]
        for i in items
    ]
    rows.sort(key=lambda r: r[1])
    print(tabulate(rows, headers=["SKU", "Qty", "In Stock"], tablefmt="github"))
    print(f"\n{len(rows)} product(s) at or below {threshold} units.")


def cmd_bulk_check(args):
    client = get_client(args.site)
    skus = [s.strip() for s in args.skus.split(",") if s.strip()]
    if not skus:
        print("No SKUs provided.")
        return

    try:
        # Use 'in' condition for bulk check
        result = client.search(
            "stockItems",
            filters=[{"field": "sku", "value": ",".join(skus), "condition_type": "in"}],
            page_size=len(skus)
        )
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    found_skus = {i.get("sku") for i in items}
    rows = [
        [i.get("sku"), i.get("qty"), "Yes" if i.get("is_in_stock") else "No"]
        for i in items
    ]
    if rows:
        print(tabulate(rows, headers=["SKU", "Qty", "In Stock"], tablefmt="github"))

    missing = [sku for sku in skus if sku not in found_skus]
    if missing:
        print(f"\nNot found: {', '.join(missing)}")


def cmd_sources(args):
    client = get_client(args.site)
    try:
        result = client.search("inventory/sources", page_size=args.limit)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No inventory sources found.")
        return

    rows = [
        [s.get("source_code"), s.get("name"), s.get("country_id", ""),
         "Yes" if s.get("enabled") else "No"]
        for s in items
    ]
    print(tabulate(rows, headers=["Source Code", "Name", "Country", "Enabled"], tablefmt="github"))
    print(f"\n{len(items)} source(s).")


def cmd_source_get(args):
    client = get_client(args.site)
    try:
        source = client.get(f"inventory/sources/{args.source_code}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("Source Code", source.get("source_code")),
        ("Name", source.get("name")),
        ("Enabled", "Yes" if source.get("enabled") else "No"),
        ("Country", source.get("country_id", "")),
        ("Region", source.get("region", "")),
        ("City", source.get("city", "")),
        ("Street", source.get("street", "")),
        ("Postcode", source.get("postcode", "")),
        ("Contact Name", source.get("contact_name", "")),
        ("Email", source.get("email", "")),
        ("Phone", source.get("phone", "")),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_source_items(args):
    client = get_client(args.site)
    filters = []
    if args.sku:
        filters.append({"field": "sku", "value": args.sku, "condition_type": "eq"})
    if args.source:
        filters.append({"field": "source_code", "value": args.source, "condition_type": "eq"})
    if not filters:
        print("Error: At least one of --sku or --source must be provided.")
        sys.exit(1)

    try:
        result = client.search("inventory/source-items", filters=filters, page_size=args.limit)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No source items found.")
        return

    rows = [
        [i.get("sku"), i.get("source_code"), i.get("quantity"), i.get("status")]
        for i in items
    ]
    print(tabulate(rows, headers=["SKU", "Source", "Quantity", "Status"], tablefmt="github"))
    print(f"\n{len(items)} of {result.get('total_count', len(items))} item(s).")


def cmd_source_item_update(args):
    client = get_client(args.site)
    try:
        qty = float(args.qty)
    except ValueError:
        print(f"Error: '{args.qty}' is not a valid number.")
        sys.exit(1)
    try:
        client.post("inventory/source-items", {
            "sourceItems": [{
                "sku": args.sku,
                "source_code": args.source_code,
                "quantity": qty,
                "status": 1,
            }]
        })
    except MagentoAPIError as e:
        print_error_and_exit(e)
    print(f"Source item {args.sku} at source '{args.source_code}' updated to qty {args.qty}.")


def cmd_salable_qty(args):
    client = get_client(args.site)
    try:
        qty = client.get(f"inventory/get-product-salable-quantity/{args.sku}/{args.stock_id}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    fields = [
        ("SKU", args.sku),
        ("Stock ID", args.stock_id),
        ("Salable Qty", qty),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_is_salable(args):
    client = get_client(args.site)
    try:
        result = client.get(f"inventory/is-product-salable/{args.sku}/{args.stock_id}")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    salable = bool(result)
    fields = [
        ("SKU", args.sku),
        ("Stock ID", args.stock_id),
        ("Salable", "Yes" if salable else "No"),
    ]
    print(tabulate(fields, tablefmt="simple"))


def cmd_stocks(args):
    client = get_client(args.site)
    try:
        result = client.search("inventory/stocks", page_size=args.limit)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    items = result.get("items", [])
    if not items:
        print("No stocks found.")
        return

    rows = []
    for s in items:
        sales_channels = s.get("extension_attributes", {}).get("sales_channels", [])
        channels_str = ", ".join(
            f"{ch.get('type')}:{ch.get('code')}" for ch in sales_channels
        ) if sales_channels else ""
        rows.append([s.get("stock_id"), s.get("name"), channels_str])

    print(tabulate(rows, headers=["Stock ID", "Name", "Sales Channels"], tablefmt="github"))
    print(f"\n{len(items)} stock(s).")


def cmd_bulk_update(args):
    client = get_client(args.site)
    delay_ms = env_default("OPENCLAW_DELAY_MS", args.delay_ms, 200)

    items = parse_csv_input(args.csv, args.items, ["sku", "qty"])
    if not items:
        print("No items provided. Use --csv or --items.")
        sys.exit(1)

    # Validate quantities
    parsed: list[tuple[str, float]] = []
    for item in items:
        sku = item.get("sku", "")
        qty_str = item.get("qty", "")
        if not sku or not qty_str:
            print(f"Skipping invalid entry: {item}")
            continue
        try:
            qty = float(qty_str)
        except ValueError:
            print(f"Skipping {sku}: invalid qty '{qty_str}'")
            continue
        parsed.append((sku, qty))

    if not parsed:
        print("No valid items to process.")
        return

    if len(parsed) > 20:
        print(f"Warning: {len(parsed)} items in batch — may trigger rate limiting.")

    # Preview: batch fetch current stock
    skus = [sku for sku, _ in parsed]
    try:
        result = client.search("stockItems", filters=[
            {"field": "sku", "value": ",".join(skus), "condition_type": "in"},
        ], page_size=len(skus))
        existing = {}
        existing_ids = {}
        for i in result.get("items", []):
            existing[i.get("sku")] = i.get("qty", 0)
            existing_ids[i.get("sku")] = i.get("item_id")
    except MagentoAPIError as e:
        print_error_and_exit(e)
        return

    # Build preview table
    preview_rows = []
    update_map: dict[str, tuple[float, float, str]] = {}
    for sku, new_qty in parsed:
        current = existing.get(sku)
        if current is None:
            preview_rows.append([sku, "NOT FOUND", new_qty, "N/A"])
            continue
        current = float(current)
        item_id = existing_ids.get(sku)
        update_map[sku] = (current, new_qty, item_id)
        preview_rows.append([sku, current, new_qty, f"{new_qty - current:+.0f}"])

    print("Stock Update Preview:")
    print(tabulate(preview_rows, headers=["SKU", "Current Qty", "New Qty", "Change"], tablefmt="github"))

    not_found = [sku for sku, _ in parsed if sku not in existing]
    if not_found:
        print(f"\nNot found: {', '.join(not_found)}")

    if not args.execute:
        print(f"\n{len(update_map)} item(s) would be updated. Run with --execute to apply changes.")
        return

    # Execute — send minimal payload to avoid overwriting concurrent changes
    success = 0
    failed: list[tuple[str, str]] = []
    for sku, (old_qty, new_qty, item_id) in update_map.items():
        try:
            client.put(f"products/{sku}/stockItems/{item_id}", {
                "stockItem": {
                    "qty": new_qty,
                    "is_in_stock": new_qty > 0,
                },
            })
            success += 1
        except MagentoAPIError as e:
            failed.append((sku, str(e)))
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

    print(f"\nUpdated: {success} | Failed: {len(failed)} | Total: {len(update_map)}")
    if failed:
        print("\nFailed items:")
        for sku, err in failed:
            print(f"  {sku}: {err}")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 inventory management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Check stock for a SKU")
    p_check.add_argument("sku")

    p_update = sub.add_parser("update", help="Update stock quantity")
    p_update.add_argument("sku")
    p_update.add_argument("qty")

    p_low = sub.add_parser("low-stock", help="List products below a stock threshold")
    p_low.add_argument("--threshold", type=int, default=10)

    p_bulk = sub.add_parser("bulk-check", help="Check stock for multiple SKUs")
    p_bulk.add_argument("skus", help="Comma-separated list of SKUs")

    # MSI commands
    p_sources = sub.add_parser("sources", help="List inventory sources (MSI)")
    p_sources.add_argument("--limit", type=int, default=50)

    p_source_get = sub.add_parser("source-get", help="Get source details (MSI)")
    p_source_get.add_argument("source_code")

    p_sitems = sub.add_parser("source-items", help="List source items by SKU or source (MSI)")
    p_sitems.add_argument("--sku", default=None, help="Filter by SKU")
    p_sitems.add_argument("--source", default=None, help="Filter by source_code")
    p_sitems.add_argument("--limit", type=int, default=50)

    p_si_update = sub.add_parser("source-item-update", help="Update source item quantity (MSI)")
    p_si_update.add_argument("sku")
    p_si_update.add_argument("source_code")
    p_si_update.add_argument("qty")

    p_salable = sub.add_parser("salable-qty", help="Get salable quantity for SKU in a stock (MSI)")
    p_salable.add_argument("sku")
    p_salable.add_argument("stock_id", type=int)

    p_is_salable = sub.add_parser("is-salable", help="Check if product is salable in a stock (MSI)")
    p_is_salable.add_argument("sku")
    p_is_salable.add_argument("stock_id", type=int)

    p_stocks = sub.add_parser("stocks", help="List inventory stocks (MSI)")
    p_stocks.add_argument("--limit", type=int, default=50)

    p_bulk = sub.add_parser("bulk-update", help="Bulk update stock quantities")
    p_bulk.add_argument("--csv", default=None, help="CSV file (sku,qty)")
    p_bulk.add_argument("--items", default=None, help="Inline: SKU1:100,SKU2:50")
    p_bulk.add_argument("--execute", action="store_true", help="Execute changes (default: preview only)")
    p_bulk.add_argument("--delay-ms", type=int, default=None, help="Delay between writes in ms (default: 200)")

    args = parser.parse_args()
    {
        "check": cmd_check,
        "update": cmd_update,
        "low-stock": cmd_low_stock,
        "bulk-check": cmd_bulk_check,
        "sources": cmd_sources,
        "source-get": cmd_source_get,
        "source-items": cmd_source_items,
        "source-item-update": cmd_source_item_update,
        "salable-qty": cmd_salable_qty,
        "is-salable": cmd_is_salable,
        "stocks": cmd_stocks,
        "bulk-update": cmd_bulk_update,
    }[args.command](args)


if __name__ == "__main__":
    main()