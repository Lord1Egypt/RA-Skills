#!/usr/bin/env python3
"""Store diagnostics — inventory risk, promotion audit, order exceptions, pricing anomalies."""

import sys
import time
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import (
    get_client, MagentoAPIError, print_error_and_exit,
    fetch_all, utc_range, env_default, SectionResult, render_sections,
)

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def _format_age(created_at: str) -> str:
    """Convert a timestamp to a human-readable age like '2d 4h'."""
    try:
        dt = datetime.fromisoformat(created_at.replace(" ", "T")).replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days}d {hours}h"
        return f"{hours}h"
    except (ValueError, AttributeError):
        return "unknown"


# ---------------------------------------------------------------------------
# inventory-risk
# ---------------------------------------------------------------------------

def cmd_inventory_risk(args):
    client = get_client(args.site)
    days = args.days
    threshold = env_default("OPENCLAW_STOCK_THRESHOLD", args.threshold, 10)
    limit = args.limit
    fmt = args.format

    t0 = time.monotonic()
    rows: list[dict] = []

    # 1. Get low-stock items
    try:
        stock_result = client.search("stockItems", filters=[
            {"field": "qty", "value": str(threshold), "condition_type": "lteq"},
            {"field": "manage_stock", "value": "1", "condition_type": "eq"},
        ], page_size=200, sort_field="qty", sort_dir="ASC")
        stock_items = stock_result.get("items", [])
    except MagentoAPIError as e:
        print_error_and_exit(e)
        return

    if not stock_items:
        print("No low-stock products found.")
        return

    # Collect SKUs
    low_stock_skus = [i.get("sku") for i in stock_items if i.get("sku")]
    stock_map = {i.get("sku"): i.get("qty", 0) for i in stock_items}

    # 2. Fetch recent orders to compute velocity
    start, end = utc_range(days * 24)
    try:
        orders = fetch_all(client, "orders", filters=[
            {"field": "created_at", "value": start, "condition_type": "gteq"},
            {"field": "created_at", "value": end, "condition_type": "lteq"},
        ], max_pages=20)
    except MagentoAPIError:
        orders = []

    # Compute velocity per SKU — only count simple/virtual with no parent_item_id
    sku_qty_sold: dict[str, float] = defaultdict(float)
    for order in orders:
        for item in order.get("items", []):
            if item.get("parent_item_id"):
                continue
            if item.get("product_type") not in ("simple", "virtual"):
                continue
            sku = item.get("sku", "")
            qty = float(item.get("qty_ordered", 0))
            sku_qty_sold[sku] += qty

    # 3. Compute days until stockout
    for sku in low_stock_skus:
        current_qty = float(stock_map.get(sku, 0))
        velocity = sku_qty_sold.get(sku, 0) / days if days > 0 else 0
        if velocity > 0:
            days_left = current_qty / velocity
            if days_left <= 3:
                severity = "CRITICAL"
                issue = "Stockout imminent"
            elif days_left <= 7:
                severity = "HIGH"
                issue = ""
            elif days_left <= 14:
                severity = "MEDIUM"
                issue = ""
            else:
                severity = "LOW"
                issue = ""
        else:
            days_left = float("inf")
            severity = "LOW"
            issue = "No recent sales"

        rows.append({
            "Severity": severity,
            "SKU": sku,
            "Qty": current_qty,
            "Velocity/day": round(velocity, 1),
            "Days Left": f"{days_left:.1f}" if days_left != float("inf") else "∞",
            "Issue": issue,
        })

    # 4. MSI check (optional) — batch in chunks of 50 (API limit for "in" filter)
    msi_checked = 0
    try:
        chunk_size = 50
        for offset in range(0, len(low_stock_skus), chunk_size):
            chunk = low_stock_skus[offset:offset + chunk_size]
            source_items = client.search("inventory/source-items", filters=[
                {"field": "sku", "value": ",".join(chunk), "condition_type": "in"},
            ], page_size=200)
            sku_sources: dict[str, list] = defaultdict(list)
            for si in source_items.get("items", []):
                sku_sources[si.get("sku", "")].append(si)
            msi_checked += len(chunk)

            for sku, sources in sku_sources.items():
                all_disabled = all(not s.get("status") for s in sources)
                if all_disabled and sources:
                    for r in rows:
                        if r["SKU"] == sku:
                            r["Issue"] = (r["Issue"] + "; All sources disabled").strip("; ")
                            if r["Severity"] not in ("CRITICAL",):
                                r["Severity"] = "HIGH"
    except MagentoAPIError:
        pass  # MSI not available, skip

    if msi_checked < len(low_stock_skus):
        print(f"Warning: MSI check covered {msi_checked} of {len(low_stock_skus)} SKUs.", file=sys.stderr)

    # 5. Check enabled products with qty=0 and no backorders
    try:
        zero_stock = client.search("stockItems", filters=[
            {"field": "qty", "value": "0", "condition_type": "eq"},
            {"field": "manage_stock", "value": "1", "condition_type": "eq"},
            {"field": "backorders", "value": "0", "condition_type": "eq"},
        ], page_size=100)
        for item in zero_stock.get("items", []):
            sku = item.get("sku", "")
            if sku not in stock_map:
                rows.append({
                    "Severity": "CRITICAL",
                    "SKU": sku,
                    "Qty": 0,
                    "Velocity/day": 0,
                    "Days Left": "0",
                    "Issue": "Out of stock, no backorders",
                })
    except MagentoAPIError:
        pass

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    rows.sort(key=lambda r: severity_order.get(r["Severity"], 9))
    rows = rows[:limit]

    elapsed = time.monotonic() - t0

    if fmt == "json":
        section = SectionResult("Inventory Risk", "ok" if rows else "ok",
                                elapsed, rows=rows)
        print(render_sections([section], format="json"))
    else:
        print(f"Inventory Risk Report (last {days} days, threshold ≤{threshold})")
        print(f"Generated in {elapsed:.1f}s\n")
        if rows:
            headers = ["Severity", "SKU", "Qty", "Velocity/day", "Days Left", "Issue"]
            print(tabulate([[r[h] for h in headers] for r in rows],
                           headers=headers, tablefmt="github"))
        else:
            print("No inventory risks detected.")


# ---------------------------------------------------------------------------
# promotion-audit
# ---------------------------------------------------------------------------

def cmd_promotion_audit(args):
    client = get_client(args.site)
    warn_hours = env_default("OPENCLAW_WARN_HOURS", args.warn_hours, 48)
    fmt = args.format

    t0 = time.monotonic()
    rows: list[dict] = []

    try:
        result = client.search("salesRules/search", filters=[
            {"field": "is_active", "value": "1", "condition_type": "eq"},
        ], page_size=200)
        rules = result.get("items", [])
    except MagentoAPIError as e:
        print_error_and_exit(e)
        return

    utc_now = datetime.now(timezone.utc)
    warn_cutoff = utc_now + timedelta(hours=warn_hours)

    # Collect rule IDs with coupon_type=3 for batch coupon check
    auto_coupon_rule_ids = []

    for rule in rules:
        rule_id = rule.get("rule_id")
        name = rule.get("name", "")
        coupon_type = rule.get("coupon_type")
        to_date = rule.get("to_date")
        times_used = int(rule.get("times_used", 0))
        usage_limit = rule.get("usage_limit")

        # Check 1: Expired but still active
        if to_date and to_date != "NULL":
            try:
                to_dt = datetime.fromisoformat(to_date.replace(" ", "T")).replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                to_dt = None
            if to_dt and to_dt < utc_now:
                rows.append({
                    "Severity": "HIGH",
                    "Rule ID": rule_id,
                    "Name": name,
                    "Issue": f"Expired on {to_date[:10]} but still active",
                })
                continue  # Don't double-report
            if to_dt and to_dt <= warn_cutoff:
                rows.append({
                    "Severity": "LOW",
                    "Rule ID": rule_id,
                    "Name": name,
                    "Issue": f"Expiring within {warn_hours}h ({to_date[:10]})",
                })

        # Check 2: Specific coupon but no code
        if coupon_type == 2:
            code = rule.get("code")
            if not code:
                rows.append({
                    "Severity": "HIGH",
                    "Rule ID": rule_id,
                    "Name": name,
                    "Issue": "coupon_type=2 but no code set",
                })

        # Check 3: Auto-generated coupons — collect for batch check
        if coupon_type == 3:
            auto_coupon_rule_ids.append(rule_id)

        # Check 4: Coupon exhausted
        if usage_limit and times_used >= int(usage_limit):
            rows.append({
                "Severity": "MEDIUM",
                "Rule ID": rule_id,
                "Name": name,
                "Issue": f"Coupon exhausted ({times_used}/{usage_limit})",
            })

        # Check 6: No end date
        if not to_date or to_date == "NULL":
            rows.append({
                "Severity": "INFO",
                "Rule ID": rule_id,
                "Name": name,
                "Issue": "No end date (runs indefinitely)",
            })

    # Batch check auto-generated coupons (coupon_type=3)
    if auto_coupon_rule_ids:
        for rule_id in auto_coupon_rule_ids:
            try:
                coupon_result = client.search("coupons/search", filters=[
                    {"field": "rule_id", "value": str(rule_id), "condition_type": "eq"},
                ], page_size=1)
                if coupon_result.get("total_count", 0) == 0:
                    # Find rule name
                    rule_name = next((r.get("name", "") for r in rules if r.get("rule_id") == rule_id), "")
                    rows.append({
                        "Severity": "HIGH",
                        "Rule ID": rule_id,
                        "Name": rule_name,
                        "Issue": "coupon_type=3 but no coupons generated",
                    })
            except MagentoAPIError:
                pass

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    rows.sort(key=lambda r: severity_order.get(r["Severity"], 9))

    elapsed = time.monotonic() - t0

    if fmt == "json":
        section = SectionResult("Promotion Audit", "ok", elapsed, rows=rows)
        print(render_sections([section], format="json"))
    else:
        print("Promotion Audit Report")
        print(f"Generated in {elapsed:.1f}s\n")
        if rows:
            headers = ["Severity", "Rule ID", "Name", "Issue"]
            print(tabulate([[r[h] for h in headers] for r in rows],
                           headers=headers, tablefmt="github"))
        else:
            print("No promotion issues detected.")


# ---------------------------------------------------------------------------
# order-exceptions
# ---------------------------------------------------------------------------

def cmd_order_exceptions(args):
    client = get_client(args.site)
    pending_hours = env_default("OPENCLAW_PENDING_HOURS", args.pending_hours, 24)
    processing_hours = env_default("OPENCLAW_PROCESSING_HOURS", args.processing_hours, 48)
    limit = args.limit
    fmt = args.format

    t0 = time.monotonic()
    rows: list[dict] = []

    # 1. Stuck pending
    pending_cutoff, _ = utc_range(pending_hours)
    try:
        pending = client.search("orders", filters=[
            {"field": "status", "value": "pending", "condition_type": "eq"},
            {"field": "created_at", "value": pending_cutoff, "condition_type": "lteq"},
        ], page_size=limit)
        for o in pending.get("items", []):
            rows.append({
                "Type": "Stuck Pending",
                "Order #": o.get("increment_id"),
                "Customer": o.get("customer_email", ""),
                "Total": f"{o.get('base_grand_total', 0):.2f}",
                "Age": _format_age(o.get("created_at", "")),
            })
    except MagentoAPIError:
        pass

    # 2. Payment review
    try:
        review = client.search("orders", filters=[
            {"field": "status", "value": "payment_review", "condition_type": "eq"},
        ], page_size=limit)
        for o in review.get("items", []):
            rows.append({
                "Type": "Payment Review",
                "Order #": o.get("increment_id"),
                "Customer": o.get("customer_email", ""),
                "Total": f"{o.get('base_grand_total', 0):.2f}",
                "Age": _format_age(o.get("created_at", "")),
            })
    except MagentoAPIError:
        pass

    # 3. Processing too long
    proc_cutoff, _ = utc_range(processing_hours)
    try:
        processing = client.search("orders", filters=[
            {"field": "status", "value": "processing", "condition_type": "eq"},
            {"field": "created_at", "value": proc_cutoff, "condition_type": "lteq"},
        ], page_size=limit)
        for o in processing.get("items", []):
            rows.append({
                "Type": "Stuck Processing",
                "Order #": o.get("increment_id"),
                "Customer": o.get("customer_email", ""),
                "Total": f"{o.get('base_grand_total', 0):.2f}",
                "Age": _format_age(o.get("created_at", "")),
            })
    except MagentoAPIError:
        pass

    # 4. Cancellation spike detection
    cancel_24h_start, cancel_end = utc_range(24)
    try:
        recent_cancel = client.search("orders", filters=[
            {"field": "status", "value": "canceled", "condition_type": "eq"},
            {"field": "updated_at", "value": cancel_24h_start, "condition_type": "gteq"},
        ], page_size=1)
        recent_cancel_count = recent_cancel.get("total_count", 0)

        # 7-day average
        week_ago_start, _ = utc_range(7 * 24)
        try:
            week_cancel = client.search("orders", filters=[
                {"field": "status", "value": "canceled", "condition_type": "eq"},
                {"field": "updated_at", "value": week_ago_start, "condition_type": "gteq"},
            ], page_size=1)
            week_cancel_count = week_cancel.get("total_count", 0)
            daily_avg = week_cancel_count / 7

            if daily_avg > 0 and recent_cancel_count > daily_avg * 2:
                rows.append({
                    "Type": "Cancel Spike",
                    "Order #": f"{recent_cancel_count} in last 24h",
                    "Customer": f"7d avg: {daily_avg:.1f}/day",
                    "Total": f"{recent_cancel_count / daily_avg:.1f}x normal",
                    "Age": "",
                })
        except MagentoAPIError:
            pass
    except MagentoAPIError:
        pass

    elapsed = time.monotonic() - t0

    if fmt == "json":
        section = SectionResult("Order Exceptions", "ok", elapsed, rows=rows)
        print(render_sections([section], format="json"))
    else:
        print(f"Order Exceptions Report (pending >{pending_hours}h, processing >{processing_hours}h)")
        print(f"Generated in {elapsed:.1f}s\n")
        if rows:
            headers = ["Type", "Order #", "Customer", "Total", "Age"]
            print(tabulate([[r[h] for h in headers] for r in rows],
                           headers=headers, tablefmt="github"))
        else:
            print("No order exceptions detected.")


# ---------------------------------------------------------------------------
# pricing-anomaly
# ---------------------------------------------------------------------------

def cmd_pricing_anomaly(args):
    client = get_client(args.site)
    limit = args.limit
    fmt = args.format

    t0 = time.monotonic()
    rows: list[dict] = []
    utc_now = datetime.now(timezone.utc)
    utc_now_str = utc_now.strftime("%Y-%m-%d %H:%M:%S")

    # Query 1: Zero price + enabled
    try:
        zero_price = client.search("products", filters=[
            {"field": "price", "value": "0", "condition_type": "eq"},
            {"field": "status", "value": "1", "condition_type": "eq"},
        ], page_size=limit)
        for p in zero_price.get("items", []):
            rows.append({
                "Severity": "HIGH",
                "SKU": p.get("sku"),
                "Name": p.get("name", "")[:40],
                "Price": 0,
                "Special Price": _get_special_price(p),
                "Issue": "Zero price on enabled product",
            })
    except MagentoAPIError:
        pass

    # Query 2: Negative price
    try:
        neg_price = client.search("products", filters=[
            {"field": "price", "value": "0", "condition_type": "lt"},
        ], page_size=limit)
        for p in neg_price.get("items", []):
            rows.append({
                "Severity": "CRITICAL",
                "SKU": p.get("sku"),
                "Name": p.get("name", "")[:40],
                "Price": p.get("price", 0),
                "Special Price": _get_special_price(p),
                "Issue": "Negative price",
            })
    except MagentoAPIError:
        pass

    # Query 3: Special price anomalies (special_price > 0 on enabled products)
    try:
        special_products = client.search("products", filters=[
            {"field": "special_price", "value": "0", "condition_type": "gt"},
            {"field": "status", "value": "1", "condition_type": "eq"},
        ], page_size=limit * 2)
        for p in special_products.get("items", []):
            special = _get_special_price(p)
            regular = float(p.get("price", 0) or 0)
            if special is not None and special > regular:
                rows.append({
                    "Severity": "MEDIUM",
                    "SKU": p.get("sku"),
                    "Name": p.get("name", "")[:40],
                    "Price": regular,
                    "Special Price": special,
                    "Issue": f"Special price ({special}) > regular price ({regular})",
                })
    except MagentoAPIError:
        pass

    # Query 4: Special price expired but still set
    try:
        expired_special = client.search("products", filters=[
            {"field": "special_to_date", "value": utc_now_str, "condition_type": "lt"},
            {"field": "special_price", "value": "0", "condition_type": "gt"},
        ], page_size=limit)
        for p in expired_special.get("items", []):
            special = _get_special_price(p)
            if special is not None:
                special_to = _get_custom_attr(p, "special_to_date")
                rows.append({
                    "Severity": "LOW",
                    "SKU": p.get("sku"),
                    "Name": p.get("name", "")[:40],
                    "Price": float(p.get("price", 0) or 0),
                    "Special Price": special,
                    "Issue": f"Special price expired {special_to or 'unknown'}",
                })
    except MagentoAPIError:
        pass

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    rows.sort(key=lambda r: severity_order.get(r["Severity"], 9))
    rows = rows[:limit]

    elapsed = time.monotonic() - t0

    if fmt == "json":
        section = SectionResult("Pricing Anomaly", "ok", elapsed, rows=rows)
        print(render_sections([section], format="json"))
    else:
        print("Pricing Anomaly Report")
        print(f"Generated in {elapsed:.1f}s\n")
        if rows:
            headers = ["Severity", "SKU", "Name", "Price", "Special Price", "Issue"]
            print(tabulate([[r[h] for h in headers] for r in rows],
                           headers=headers, tablefmt="github"))
        else:
            print("No pricing anomalies detected.")


def _get_special_price(product: dict) -> float | None:
    """Extract special_price from custom_attributes."""
    val = _get_custom_attr(product, "special_price")
    if val is not None:
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    return None


def _get_custom_attr(product: dict, attr_code: str) -> str | None:
    """Get a custom_attribute value from a product dict."""
    for attr in product.get("custom_attributes", []):
        if attr.get("attribute_code") == attr_code:
            return attr.get("value")
    return None


def main():
    parser = argparse.ArgumentParser(description="Magento 2 Store Diagnostics")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    # inventory-risk
    p_ir = sub.add_parser("inventory-risk", help="Inventory risk radar with velocity prediction")
    p_ir.add_argument("--days", type=int, default=7, help="Days for velocity calculation (default: 7)")
    p_ir.add_argument("--threshold", type=int, default=None, help="Low stock threshold (default: 10)")
    p_ir.add_argument("--limit", type=int, default=50, help="Max results")
    p_ir.add_argument("--format", choices=["markdown", "json"], default="markdown")

    # promotion-audit
    p_pa = sub.add_parser("promotion-audit", help="Audit active promotions for issues")
    p_pa.add_argument("--warn-hours", type=int, default=None, help="Warn N hours before expiry (default: 48)")
    p_pa.add_argument("--format", choices=["markdown", "json"], default="markdown")

    # order-exceptions
    p_oe = sub.add_parser("order-exceptions", help="Find stuck and anomalous orders")
    p_oe.add_argument("--pending-hours", type=int, default=None, help="Pending threshold hours (default: 24)")
    p_oe.add_argument("--processing-hours", type=int, default=None, help="Processing threshold hours (default: 48)")
    p_oe.add_argument("--limit", type=int, default=50, help="Max results")
    p_oe.add_argument("--format", choices=["markdown", "json"], default="markdown")

    # pricing-anomaly
    p_pn = sub.add_parser("pricing-anomaly", help="Detect pricing issues (zero, negative, inverted)")
    p_pn.add_argument("--limit", type=int, default=50, help="Max results")
    p_pn.add_argument("--format", choices=["markdown", "json"], default="markdown")

    args = parser.parse_args()
    {
        "inventory-risk": cmd_inventory_risk,
        "promotion-audit": cmd_promotion_audit,
        "order-exceptions": cmd_order_exceptions,
        "pricing-anomaly": cmd_pricing_anomaly,
    }[args.command](args)


if __name__ == "__main__":
    main()
