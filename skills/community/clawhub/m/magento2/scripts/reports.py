#!/usr/bin/env python3
"""
Sales & inventory reporting — uses pandas for aggregation and tabulate for output.
Default date range: last 30 days.
"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, MagentoAPIError, print_error_and_exit, fetch_all

try:
    import pandas as pd
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependencies: uv pip install pandas tabulate")


def default_date_range():
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def cmd_sales(args):
    client = get_client(args.site)
    date_from = args.__dict__.get("from") or default_date_range()[0]
    date_to = args.__dict__.get("to") or default_date_range()[1]

    filters = [
        {"field": "created_at", "value": f"{date_from} 00:00:00", "condition_type": "gteq"},
        {"field": "created_at", "value": f"{date_to} 23:59:59", "condition_type": "lteq"},
    ]
    try:
        orders = fetch_all(client, "orders", filters=filters)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    if not orders:
        print(f"No orders between {date_from} and {date_to}.")
        return

    df = pd.DataFrame(orders)
    currency = df["base_currency_code"].mode()[0] if "base_currency_code" in df.columns else ""

    total_orders = len(df)
    total_revenue = df["base_grand_total"].sum()
    total_tax = df["base_tax_amount"].sum() if "base_tax_amount" in df.columns else 0
    total_shipping = df["base_shipping_amount"].sum() if "base_shipping_amount" in df.columns else 0
    avg_order = total_revenue / total_orders if total_orders else 0
    cancelled = (df["status"] == "canceled").sum() if "status" in df.columns else 0

    print(f"\nSales Summary: {date_from} to {date_to}")
    print("─" * 40)
    summary = [
        ["Total orders", total_orders],
        ["Total revenue", f"{total_revenue:.2f} {currency}"],
        ["Avg. order value", f"{avg_order:.2f} {currency}"],
        ["Total tax collected", f"{total_tax:.2f} {currency}"],
        ["Total shipping", f"{total_shipping:.2f} {currency}"],
        ["Cancelled orders", cancelled],
    ]
    print(tabulate(summary, tablefmt="simple"))

    # Daily breakdown
    if "created_at" in df.columns:
        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        daily = df.groupby("date").agg(orders=("entity_id", "count"), revenue=("base_grand_total", "sum")).reset_index()
        daily["revenue"] = daily["revenue"].map(lambda x: f"{x:.2f}")
        print(f"\nDaily breakdown:")
        print(tabulate(daily.values.tolist(), headers=["Date", "Orders", f"Revenue ({currency})"], tablefmt="github"))


def cmd_top_products(args):
    client = get_client(args.site)
    date_from = args.__dict__.get("from") or default_date_range()[0]
    date_to = args.__dict__.get("to") or default_date_range()[1]

    filters = [
        {"field": "created_at", "value": f"{date_from} 00:00:00", "condition_type": "gteq"},
        {"field": "created_at", "value": f"{date_to} 23:59:59", "condition_type": "lteq"},
    ]
    try:
        orders = fetch_all(client, "orders", filters=filters)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    if not orders:
        print("No orders found.")
        return

    rows = []
    for order in orders:
        currency = order.get("base_currency_code", "")
        for item in order.get("items", []):
            rows.append({
                "sku": item.get("sku"),
                "name": item.get("name"),
                "qty": item.get("qty_ordered", 0),
                "revenue": item.get("base_row_total", 0),
                "currency": currency,
            })

    df = pd.DataFrame(rows)
    if df.empty:
        print("No order items found.")
        return

    currency = df["currency"].mode()[0]
    agg = df.groupby(["sku", "name"]).agg(
        units=("qty", "sum"), revenue=("revenue", "sum")
    ).reset_index().sort_values("revenue", ascending=False).head(args.limit)

    agg["revenue"] = agg["revenue"].map(lambda x: f"{x:.2f} {currency}")
    print(f"\nTop {args.limit} products by revenue ({date_from} to {date_to}):")
    print(tabulate(agg[["sku", "name", "units", "revenue"]].values.tolist(),
                   headers=["SKU", "Name", "Units Sold", "Revenue"], tablefmt="github"))


def cmd_top_customers(args):
    client = get_client(args.site)
    date_from = args.__dict__.get("from") or default_date_range()[0]
    date_to = args.__dict__.get("to") or default_date_range()[1]

    filters = [
        {"field": "created_at", "value": f"{date_from} 00:00:00", "condition_type": "gteq"},
        {"field": "created_at", "value": f"{date_to} 23:59:59", "condition_type": "lteq"},
    ]
    try:
        orders = fetch_all(client, "orders", filters=filters)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    rows = [
        {
            "email": o.get("customer_email"),
            "name": f"{o.get('customer_firstname', '')} {o.get('customer_lastname', '')}".strip(),
            "total": o.get("base_grand_total", 0),
            "currency": o.get("base_currency_code", ""),
        }
        for o in orders if o.get("customer_email")
    ]

    df = pd.DataFrame(rows)
    if df.empty:
        print("No customer data found.")
        return

    currency = df["currency"].mode()[0]
    agg = df.groupby(["email", "name"]).agg(
        orders=("total", "count"), spent=("total", "sum")
    ).reset_index().sort_values("spent", ascending=False).head(args.limit)

    agg["spent"] = agg["spent"].map(lambda x: f"{x:.2f} {currency}")
    print(f"\nTop {args.limit} customers by spend ({date_from} to {date_to}):")
    print(tabulate(agg[["email", "name", "orders", "spent"]].values.tolist(),
                   headers=["Email", "Name", "Orders", "Total Spent"], tablefmt="github"))


def cmd_order_status(args):
    client = get_client(args.site)
    date_from = args.__dict__.get("from") or default_date_range()[0]
    date_to = args.__dict__.get("to") or default_date_range()[1]

    filters = [
        {"field": "created_at", "value": f"{date_from} 00:00:00", "condition_type": "gteq"},
        {"field": "created_at", "value": f"{date_to} 23:59:59", "condition_type": "lteq"},
    ]
    try:
        orders = fetch_all(client, "orders", filters=filters)
    except MagentoAPIError as e:
        print_error_and_exit(e)

    df = pd.DataFrame(orders)
    if df.empty or "status" not in df.columns:
        print("No data.")
        return

    breakdown = df.groupby("status").agg(
        count=("entity_id", "count"),
        revenue=("base_grand_total", "sum"),
    ).reset_index().sort_values("count", ascending=False)

    currency = df["base_currency_code"].mode()[0] if "base_currency_code" in df.columns else ""
    breakdown["revenue"] = breakdown["revenue"].map(lambda x: f"{x:.2f} {currency}")
    print(f"\nOrder status breakdown ({date_from} to {date_to}):")
    print(tabulate(breakdown.values.tolist(), headers=["Status", "Count", "Revenue"], tablefmt="github"))


def cmd_inventory_value(args):
    client = get_client(args.site)
    try:
        stock_items = fetch_all(client, "stockItems")
        products = fetch_all(client, "products")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    stock_map = {i["sku"]: i.get("qty", 0) for i in stock_items if "sku" in i}
    rows = []
    total_value = 0.0

    for p in products:
        sku = p.get("sku")
        price = p.get("price", 0) or 0
        qty = stock_map.get(sku, 0)
        value = price * qty
        total_value += value
        rows.append([sku, p.get("name"), qty, f"{price:.2f}", f"{value:.2f}"])

    rows.sort(key=lambda r: float(r[4]), reverse=True)
    print(tabulate(rows[:100], headers=["SKU", "Name", "Qty", "Price", "Value"], tablefmt="github"))
    print(f"\nTotal inventory value: {total_value:.2f}")
    print(f"Items processed: {len(products)}")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 sales & inventory reporting")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("sales", "top-products", "top-customers", "order-status"):
        p = sub.add_parser(name)
        p.add_argument("--from", dest="from", metavar="YYYY-MM-DD")
        p.add_argument("--to", dest="to", metavar="YYYY-MM-DD")
        if name in ("top-products", "top-customers"):
            p.add_argument("--limit", type=int, default=10)

    sub.add_parser("inventory-value")

    args = parser.parse_args()
    {
        "sales": cmd_sales,
        "top-products": cmd_top_products,
        "top-customers": cmd_top_customers,
        "order-status": cmd_order_status,
        "inventory-value": cmd_inventory_value,
    }[args.command](args)


if __name__ == "__main__":
    main()