#!/usr/bin/env python3
"""
E-commerce Price Monitor — Report Generator
Usage: python3 report.py [options]

Options:
  --csv              Export full history to CSV
  --product <id>     Show history for a specific product
  --trends           Show price trend analysis
  --days <n>         Look back N days (default: 30)
"""

import json
import sys
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent
PRICES_FILE = DATA_DIR / "prices.json"
HISTORY_FILE = DATA_DIR / "price_history.jsonl"
ALERTS_FILE = DATA_DIR / "alerts.json"
REPORTS_DIR = DATA_DIR.parent / "reports"


def get_products():
    data = json.loads(PRICES_FILE.read_text()) if PRICES_FILE.exists() else {}
    return data.get("products", [])


def get_history(days=30):
    if not HISTORY_FILE.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    entries = []
    with open(HISTORY_FILE) as f:
        for line in f:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry.get("timestamp", ""))
            if ts >= cutoff:
                entries.append(entry)
    return entries


def format_price(price, currency="RM"):
    if price is None:
        return "—"
    return f"{currency} {price:.2f}"


def cmd_summary(args):
    products = get_products()
    if not products:
        print("📭 No products tracked yet.")
        return

    days = 30
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    history = get_history(days)

    print(f"\n📊 Price Watch — {len(products)} products tracked (last {days}d)")
    print("─" * 55)

    for p in products:
        name = p["name"]
        pid = p["id"]
        last_price = p.get("last_price")
        currency = p.get("currency", "RM")

        # Compute price change
        product_history = [h for h in history if h.get("product_id") == pid]
        change_str = "— No change"
        if len(product_history) >= 2:
            first = product_history[0]["price"]
            current = product_history[-1]["price"]
            if first and current and first > 0:
                pct = ((current - first) / first) * 100
                arrow = "▼" if pct < 0 else "▲" if pct > 0 else "—"
                change_str = f"{arrow} {abs(pct):.1f}%"

        price_str = format_price(last_price, currency)
        alert = p.get("alert_price")
        alert_str = f" [⚠️ Below RM {alert:.0f}]" if alert and last_price and last_price <= alert else ""
        checked = p.get("last_checked", "never")[:16] if p.get("last_checked") else "never"

        print(f"  #{pid} {name}")
        print(f"     {price_str}  {change_str}{alert_str}")
        print(f"     Last checked: {checked}")
        print()

    # Summary stats
    prices = [p["last_price"] for p in products if p.get("last_price")]
    if prices:
        print(f"  📈 Range: {format_price(min(prices))} — {format_price(max(prices))}")
        print(f"  📐 Avg:   {format_price(sum(prices) / len(prices))}")
        print(f"  🔔 Alerts triggered: {sum(1 for p in products if p.get('alert_price') and p.get('last_price') and p['last_price'] <= p['alert_price'])}")
    print()


def cmd_csv(args):
    days = 30
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    history = get_history(days)
    if not history:
        print("📭 No history data.")
        return

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    outfile = REPORTS_DIR / f"price_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(outfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Product ID", "Product Name", "Price", "Currency", "URL", "Seller", "In Stock"])
        for h in sorted(history, key=lambda x: x.get("timestamp", "")):
            writer.writerow([
                h.get("timestamp", ""),
                h.get("product_id", ""),
                h.get("product_name", ""),
                h.get("price", ""),
                h.get("currency", "RM"),
                h.get("url", ""),
                h.get("seller", ""),
                h.get("in_stock", True),
            ])

    print(f"✅ CSV exported: {outfile} ({len(history)} records)")


def cmd_product(args):
    if not args and "--product" in args:
        idx = args.index("--product")
        if idx + 1 < len(args):
            pid = int(args[idx + 1])
        else:
            print("Usage: --product <id>")
            return
    elif args and args[0].isdigit():
        pid = int(args[0])
    else:
        print("Usage: report.py --product <id>")
        return

    products = get_products()
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        print(f"❌ Product #{pid} not found")
        return

    history = get_history(days=90)
    ph = [h for h in history if h.get("product_id") == pid]

    print(f"\n📈 Price History: {product['name']} (#{pid})")
    print("─" * 45)
    if not ph:
        print("  No price history yet.")
        return

    prices = [h["price"] for h in ph if h.get("price")]
    print(f"  Period: {ph[0]['timestamp'][:10]} — {ph[-1]['timestamp'][:10]}")
    print(f"  Samples: {len(ph)}")
    if prices:
        print(f"  Low:  {format_price(min(prices))}")
        print(f"  High: {format_price(max(prices))}")
        print(f"  Avg:  {format_price(sum(prices) / len(prices))}")
        print(f"  Last: {format_price(prices[-1])}")
        print()
        print("  Recent prices:")
        for h in ph[-10:]:
            marker = " ← latest" if h == ph[-1] else ""
            print(f"    {h['timestamp'][:16]}  {format_price(h.get('price'), h.get('currency', 'RM'))}{marker}")
    print()


def cmd_trends(args):
    days = 30
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    products = get_products()
    history = get_history(days)

    print(f"\n📉 Price Trends (last {days}d)")
    print("─" * 45)

    for p in products:
        name = p["name"]
        pid = p["id"]
        ph = [h for h in history if h.get("product_id") == pid]
        if len(ph) < 2:
            print(f"  #{pid} {name} — insufficient data")
            continue

        prices = [h["price"] for h in ph if h.get("price")]
        if not prices or len(prices) < 2:
            continue

        first, last = prices[0], prices[-1]
        pct_change = ((last - first) / first) * 100
        volatility = sum(abs(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))) / (len(prices) - 1) * 100

        arrow = "📈" if pct_change > 0 else "📉" if pct_change < 0 else "➡️"
        print(f"  {arrow} #{pid} {name}")
        print(f"     Change: {pct_change:+.1f}% ({format_price(first)} → {format_price(last)})")
        print(f"     Volatility: {volatility:.1f}%")
        print()

    print()


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        cmd_summary(args)
    elif "--csv" in args:
        cmd_csv(args)
    elif "--product" in args or (args and args[0].isdigit() and not args[0].startswith("--")):
        cmd_product(args)
    elif "--trends" in args:
        cmd_trends(args)
    else:
        cmd_summary(args)
