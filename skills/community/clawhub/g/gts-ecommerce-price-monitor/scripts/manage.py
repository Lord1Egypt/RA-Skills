#!/usr/bin/env python3
"""
E-commerce Price Monitor — Data Management CLI
Usage: python3 manage.py <command> [options]

Commands:
  products add <url>      Add a new product to track
  products list           List all tracked products
  products remove <id>    Remove a product
  alerts add              Add a price alert
  alerts list             List all alerts
  alerts remove <id>      Remove an alert
  history export          Export price history
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent
PRICES_FILE = DATA_DIR / "prices.json"
HISTORY_FILE = DATA_DIR / "price_history.jsonl"
ALERTS_FILE = DATA_DIR / "alerts.json"
REPORTS_DIR = DATA_DIR.parent / "reports"


def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def cmd_products_add(args):
    products = load_json(PRICES_FILE)
    if "products" not in products:
        products["products"] = []
        products["next_id"] = 1

    url = args[0] if args else input("URL: ")
    name = input("Product name (optional): ").strip()
    interval = input("Check interval in hours (default 24): ").strip() or "24"
    alert_price = input("Alert price (optional): ").strip()

    pid = products["next_id"]
    products["next_id"] += 1

    entry = {
        "id": pid,
        "url": url,
        "name": name or f"Product #{pid}",
        "interval_hours": int(interval),
        "alert_price": float(alert_price) if alert_price else None,
        "last_price": None,
        "currency": None,
        "last_checked": None,
        "created_at": datetime.now().isoformat(),
    }
    products["products"].append(entry)
    save_json(PRICES_FILE, products)
    print(f"✅ Added product #{pid}: {entry['name']}")


def cmd_products_list(args):
    products = load_json(PRICES_FILE).get("products", [])
    if not products:
        print("📭 No products tracked yet.")
        return
    print(f"📦 {len(products)} product(s) tracked:\n")
    for p in products:
        price_str = f"{p['currency'] or 'RM'} {p['last_price']:.2f}" if p.get("last_price") else "—"
        checked = p.get("last_checked", "never")[:16] if p.get("last_checked") else "never"
        print(f"  #{p['id']} {p['name']}")
        print(f"     URL: {p['url']}")
        print(f"     Price: {price_str}  |  Last checked: {checked}")
        print(f"     Interval: {p['interval_hours']}h  |  Alert: {'RM ' + str(p['alert_price']) if p.get('alert_price') else 'None'}")
        print()


def cmd_products_remove(args):
    if not args:
        print("Usage: products remove <id>")
        return
    pid = int(args[0])
    products = load_json(PRICES_FILE)
    before = len(products.get("products", []))
    products["products"] = [p for p in products.get("products", []) if p["id"] != pid]
    if len(products["products"]) < before:
        save_json(PRICES_FILE, products)
        print(f"🗑️  Removed product #{pid}")
    else:
        print(f"❌ Product #{pid} not found")


def cmd_alerts_add(args):
    alerts = load_json(ALERTS_FILE)
    if "alerts" not in alerts:
        alerts["alerts"] = []
        alerts["next_id"] = 1

    pid = input("Product ID: ").strip()
    alert_type = input("Alert type (below/above/drop_pct): ").strip() or "below"
    value = input("Value: ").strip()
    channel = input("Notify via (telegram/email): ").strip() or "telegram"

    aid = alerts["next_id"]
    alerts["next_id"] += 1
    alerts["alerts"].append({
        "id": aid,
        "product_id": int(pid) if pid.isdigit() else None,
        "type": alert_type,
        "value": float(value) if value else None,
        "channel": channel,
        "active": True,
        "created_at": datetime.now().isoformat(),
    })
    save_json(ALERTS_FILE, alerts)
    print(f"✅ Alert #{aid} created")


def cmd_alerts_list(args):
    alerts = load_json(ALERTS_FILE).get("alerts", [])
    if not alerts:
        print("📭 No alerts configured.")
        return
    print(f"🔔 {len(alerts)} alert(s):\n")
    for a in alerts:
        status = "✅ Active" if a.get("active") else "⏸️  Paused"
        prod = f"Product #{a['product_id']}" if a.get("product_id") else "Any"
        print(f"  #{a['id']} {status} — {prod} {a['type']} {a['value']} via {a.get('channel', 'telegram')}")


def cmd_alerts_remove(args):
    if not args:
        print("Usage: alerts remove <id>")
        return
    aid = int(args[0])
    alerts = load_json(ALERTS_FILE)
    before = len(alerts.get("alerts", []))
    alerts["alerts"] = [a for a in alerts.get("alerts", []) if a["id"] != aid]
    if len(alerts["alerts"]) < before:
        save_json(ALERTS_FILE, alerts)
        print(f"🗑️  Removed alert #{aid}")
    else:
        print(f"❌ Alert #{aid} not found")


def cmd_history_export(args):
    import csv
    if not HISTORY_FILE.exists():
        print("📭 No price history found.")
        return

    days = 30
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])

    reports_dir = REPORTS_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    outfile = reports_dir / f"price_report_{datetime.now().strftime('%Y-%m-%d')}.csv"

    entries = []
    cutoff = datetime.now().timestamp() - days * 86400
    with open(HISTORY_FILE) as f:
        for line in f:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry.get("timestamp", "")).timestamp()
            if ts >= cutoff:
                entries.append(entry)

    if not entries:
        print(f"📭 No history in the last {days} days.")
        return

    with open(outfile, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "product_id", "product_name", "price", "currency", "url", "seller", "in_stock"])
        writer.writeheader()
        for e in entries:
            writer.writerow({
                "timestamp": e.get("timestamp", ""),
                "product_id": e.get("product_id", ""),
                "product_name": e.get("product_name", ""),
                "price": e.get("price", ""),
                "currency": e.get("currency", "RM"),
                "url": e.get("url", ""),
                "seller": e.get("seller", ""),
                "in_stock": e.get("in_stock", True),
            })

    print(f"✅ Exported {len(entries)} records to {outfile}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].replace("-", "_")
    args = sys.argv[2:]

    commands = {
        "products_add": cmd_products_add,
        "products_list": cmd_products_list,
        "products_remove": cmd_products_remove,
        "alerts_add": cmd_alerts_add,
        "alerts_list": cmd_alerts_list,
        "alerts_remove": cmd_alerts_remove,
        "history_export": cmd_history_export,
    }

    # Allow: "products add", "products list", "alerts add", etc.
    if len(sys.argv) >= 3 and sys.argv[1] in ("products", "alerts", "history"):
        sub = sys.argv[1]
        subcmd = sys.argv[2]
        key = f"{sub}_{subcmd}"
        if key in commands:
            commands[key](sys.argv[3:])
        else:
            print(f"Unknown command: {sub} {subcmd}")
            sys.exit(1)
    elif cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
