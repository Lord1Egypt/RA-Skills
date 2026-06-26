#!/usr/bin/env python3
"""
format_alert.py - Format price change alerts as markdown.

Usage:
  python3 check_prices.py | python3 compare.py | python3 format_alert.py
  python3 format_alert.py < changes.json

Prints a markdown report to stdout. Empty report if no changes.
"""

import json
import sys
from datetime import datetime, timezone


def format_price(value):
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def format_change(amount, pct):
    if amount is None or pct is None:
        return "N/A"
    direction = "↓" if amount < 0 else "↑"
    pct_abs = abs(pct)
    amt_abs = abs(amount)
    if amount < 0:
        return f"{direction} -{pct_abs:.1f}% (-${amt_abs:.2f})"
    else:
        return f"{direction} +{pct_abs:.1f}% (+${amt_abs:.2f})"


def format_alert_md(items):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# 🏷️ Price Watch Alert — {now}", ""]

    if not items:
        lines.append("No significant price changes detected.")
        return "\n".join(lines)

    drops = [i for i in items if i.get("status") == "ok" and (i.get("change_amount") or 0) < 0]
    increases = [i for i in items if i.get("status") == "ok" and (i.get("change_amount") or 0) > 0]
    errors = [i for i in items if i.get("status") in ("fetch_error", "no_price")]

    if drops:
        lines.append("## 📉 Price Drops")
        lines.append("")
        for item in sorted(drops, key=lambda x: x.get("change_pct", 0)):
            lines.append(f"### {item['name']}")
            lines.append(f"- **Was:** {format_price(item.get('old_price'))}")
            lines.append(f"- **Now:** {format_price(item.get('new_price'))}")
            lines.append(f"- **Change:** {format_change(item.get('change_amount'), item.get('change_pct'))}")
            lines.append(f"- **Link:** [{item['url']}]({item['url']})")
            lines.append("")

    if increases:
        lines.append("## 📈 Price Increases")
        lines.append("")
        for item in sorted(increases, key=lambda x: x.get("change_pct", 0), reverse=True):
            lines.append(f"### {item['name']}")
            lines.append(f"- **Was:** {format_price(item.get('old_price'))}")
            lines.append(f"- **Now:** {format_price(item.get('new_price'))}")
            lines.append(f"- **Change:** {format_change(item.get('change_amount'), item.get('change_pct'))}")
            lines.append(f"- **Link:** [{item['url']}]({item['url']})")
            lines.append("")

    if errors:
        lines.append("## ⚠️ Check Errors")
        lines.append("")
        for item in errors:
            status = item.get("status", "error")
            err_msg = item.get("error", "Unknown error")
            icon = "🚫" if status == "fetch_error" else "🔍"
            lines.append(f"- {icon} **{item['name']}** — {err_msg}")
            lines.append(f"  [View product]({item['url']})")
        lines.append("")

    return "\n".join(lines)


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("[ERROR] No input received. Pipe compare.py output to this script.", file=sys.stderr)
        sys.exit(1)

    try:
        items = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(items, list):
        print("[ERROR] Expected a JSON array.", file=sys.stderr)
        sys.exit(1)

    print(format_alert_md(items))


if __name__ == "__main__":
    main()
