#!/usr/bin/env python3
"""Generate a full homelab asset report in Markdown."""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, date


INVENTORY_PATH = os.environ.get(
    "HOMELAB_ASSETS_PATH",
    os.path.expanduser("~/.openclaw/workspace/homelab-assets/inventory.json"),
)

DEPRECIATION_YEARS = 5  # Straight-line over 5 years, 0% residual
DEFAULT_KWH_RATE = 0.12  # USD per kWh
HOURS_PER_MONTH = 730  # 24h * 365 / 12


def load_inventory(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def days_until(date_str):
    if not date_str:
        return None
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - date.today()).days
    except ValueError:
        return None


def estimated_current_value(asset):
    """Straight-line depreciation over DEPRECIATION_YEARS from purchase date."""
    price = asset.get("purchase_price")
    purchase_date = asset.get("purchase_date")
    if not price or not purchase_date:
        return None
    try:
        pd = datetime.strptime(purchase_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    days_owned = (date.today() - pd).days
    years_owned = days_owned / 365.25
    remaining_fraction = max(0.0, 1.0 - (years_owned / DEPRECIATION_YEARS))
    return round(price * remaining_fraction, 2)


def format_currency(value):
    return f"${value:,.2f}" if value is not None else "—"


def generate_report(assets, kwh_rate):
    today = date.today().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    lines.append(f"# Homelab Asset Report")
    lines.append(f"*Generated: {now}*")
    lines.append("")

    # --- Summary ---
    active = [a for a in assets if a.get("status", "active") == "active"]
    total_investment = sum(a["purchase_price"] for a in assets if a.get("purchase_price") is not None)
    active_investment = sum(a["purchase_price"] for a in active if a.get("purchase_price") is not None)

    current_values = [v for v in (estimated_current_value(a) for a in active) if v is not None]
    total_current_value = sum(current_values)
    depreciated = active_investment - total_current_value

    total_watts = sum(a["power_watts"] for a in active if a.get("power_watts") is not None)
    monthly_kwh = (total_watts / 1000) * HOURS_PER_MONTH
    monthly_cost = monthly_kwh * kwh_rate
    annual_cost = monthly_cost * 12

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total assets | {len(assets)} ({len(active)} active) |")
    lines.append(f"| Total investment (all) | {format_currency(total_investment)} |")
    lines.append(f"| Active assets investment | {format_currency(active_investment)} |")
    lines.append(f"| Estimated current value | {format_currency(total_current_value)} |")
    lines.append(f"| Total depreciation | {format_currency(depreciated)} |")
    lines.append(f"| Total active power draw | {total_watts:.1f}W |")
    lines.append(f"| Est. monthly power cost | {format_currency(monthly_cost)} (@ ${kwh_rate}/kWh) |")
    lines.append(f"| Est. annual power cost | {format_currency(annual_cost)} |")
    lines.append("")

    # --- Warranty Alerts ---
    expiring_soon = []
    already_expired = []
    for a in active:
        d = days_until(a.get("warranty_expiry"))
        if d is None:
            continue
        if d < 0:
            already_expired.append((a, d))
        elif d <= 90:
            expiring_soon.append((a, d))

    lines.append("## Warranty Alerts")
    lines.append("")
    if not expiring_soon and not already_expired:
        lines.append("✅ No warranty issues in the next 90 days.")
    else:
        if already_expired:
            lines.append("### ⚠️ Expired Warranties")
            lines.append("")
            lines.append("| Asset | Expiry | Days Ago |")
            lines.append("|-------|--------|----------|")
            for a, d in sorted(already_expired, key=lambda x: x[1]):
                lines.append(f"| {a['name']} | {a['warranty_expiry']} | {abs(d)} days ago |")
            lines.append("")
        if expiring_soon:
            lines.append("### 🔔 Expiring Within 90 Days")
            lines.append("")
            lines.append("| Asset | Expiry | Days Left |")
            lines.append("|-------|--------|-----------|")
            for a, d in sorted(expiring_soon, key=lambda x: x[1]):
                lines.append(f"| {a['name']} | {a['warranty_expiry']} | {d} days |")
            lines.append("")

    # --- Assets by Type ---
    lines.append("## Assets by Type")
    lines.append("")
    by_type = defaultdict(list)
    for a in assets:
        by_type[a.get("type", "other")].append(a)

    lines.append("| Type | Count | Investment |")
    lines.append("|------|-------|-----------|")
    for t in sorted(by_type.keys()):
        group = by_type[t]
        inv = sum(a["purchase_price"] for a in group if a.get("purchase_price") is not None)
        lines.append(f"| {t} | {len(group)} | {format_currency(inv)} |")
    lines.append("")

    # --- Assets by Location ---
    lines.append("## Assets by Location")
    lines.append("")
    by_loc = defaultdict(list)
    for a in active:
        loc = a.get("location") or "Unspecified"
        by_loc[loc].append(a)

    lines.append("| Location | Assets | Power Draw |")
    lines.append("|----------|--------|------------|")
    for loc in sorted(by_loc.keys()):
        group = by_loc[loc]
        watts = sum(a["power_watts"] for a in group if a.get("power_watts") is not None)
        lines.append(f"| {loc} | {len(group)} | {watts:.1f}W |")
    lines.append("")

    # --- Full Asset List ---
    lines.append("## Full Asset List")
    lines.append("")
    lines.append("| Name | Type | Brand/Model | Status | Purchase Price | Est. Value | Location | Warranty |")
    lines.append("|------|------|-------------|--------|---------------|------------|----------|---------|")
    for a in sorted(assets, key=lambda x: x.get("name", "")):
        bm = f"{a.get('brand', '')} {a.get('model', '')}".strip() or "—"
        price = format_currency(a.get("purchase_price"))
        ev = estimated_current_value(a)
        ev_str = format_currency(ev) if ev is not None else "—"
        status = a.get("status", "active")
        loc = a.get("location") or "—"
        d = days_until(a.get("warranty_expiry"))
        if d is None:
            warranty = "—"
        elif d < 0:
            warranty = f"Expired ({abs(d)}d ago)"
        elif d == 0:
            warranty = "Expires today"
        else:
            warranty = f"{a['warranty_expiry']} ({d}d)"
        lines.append(f"| {a['name']} | {a.get('type','—')} | {bm} | {status} | {price} | {ev_str} | {loc} | {warranty} |")
    lines.append("")

    lines.append("---")
    lines.append(f"*Power cost estimate assumes 24/7 operation at ${kwh_rate}/kWh ({HOURS_PER_MONTH}h/month). Depreciation: straight-line over {DEPRECIATION_YEARS} years.*")
    lines.append(f"*Report covers {len(assets)} total assets. Data source: {INVENTORY_PATH}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a full homelab asset report.")
    parser.add_argument(
        "--kwh-rate",
        type=float,
        default=DEFAULT_KWH_RATE,
        help=f"Electricity rate in USD/kWh (default: {DEFAULT_KWH_RATE})",
    )
    parser.add_argument("--output", metavar="FILE", help="Write report to file instead of stdout")
    parser.add_argument(
        "--inventory",
        default=INVENTORY_PATH,
        help=f"Path to inventory JSON (default: {INVENTORY_PATH})",
    )
    args = parser.parse_args()

    assets = load_inventory(args.inventory)
    if not assets:
        print("No inventory found. Use add_asset.py to add assets first.")
        sys.exit(0)

    report = generate_report(assets, args.kwh_rate)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
