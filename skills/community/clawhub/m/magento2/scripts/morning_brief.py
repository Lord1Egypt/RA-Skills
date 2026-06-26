#!/usr/bin/env python3
"""Morning Brief — daily store health summary with actionable insights."""

import sys
import time
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import (
    get_client, MagentoAPIError,
    fetch_all, utc_range, env_default, SectionResult, render_sections,
    _section_to_dict,
)

try:
    import pandas as pd
except ImportError:
    sys.exit("Missing dependencies: uv pip install pandas tabulate")


def _section_sales(client, hours: int) -> SectionResult:
    """Sales summary for the last N hours."""
    t0 = time.monotonic()
    start, end = utc_range(hours)
    filters = [
        {"field": "created_at", "value": start, "condition_type": "gteq"},
        {"field": "created_at", "value": end, "condition_type": "lteq"},
    ]
    try:
        orders = fetch_all(client, "orders", filters=filters)
    except MagentoAPIError as e:
        return SectionResult("Sales", "error", time.monotonic() - t0, error=str(e))

    if not orders:
        return SectionResult("Sales (Last {}h)".format(hours), "ok", time.monotonic() - t0,
                             findings=[f"No orders in the last {hours}h."])

    df = pd.DataFrame(orders)
    currency = df["base_currency_code"].mode()[0] if "base_currency_code" in df.columns else ""
    total_orders = len(df)
    total_revenue = df["base_grand_total"].sum()
    avg_order = total_revenue / total_orders if total_orders else 0

    rows = [
        {"Metric": "Orders", "Value": str(total_orders)},
        {"Metric": "Revenue", "Value": f"{total_revenue:.2f} {currency}"},
        {"Metric": "Avg. Order Value", "Value": f"{avg_order:.2f} {currency}"},
    ]
    return SectionResult(f"Sales (Last {hours}h)", "ok", time.monotonic() - t0, rows=rows)


def _section_order_anomalies(client, hours: int) -> SectionResult:
    """Stuck orders: pending too long, payment_review, recent cancellations."""
    t0 = time.monotonic()
    findings: list[str] = []
    rows: list[dict] = []
    _, now_str = utc_range(0)

    # 1. Stuck pending (>hours)
    pending_cutoff_start, _ = utc_range(hours)  # created more than hours ago
    try:
        pending_result = client.search("orders", filters=[
            {"field": "status", "value": "pending", "condition_type": "eq"},
            {"field": "created_at", "value": pending_cutoff_start, "condition_type": "lteq"},
        ], page_size=50)
        pending_items = pending_result.get("items", [])
        pending_count = pending_result.get("total_count", len(pending_items))
        if pending_count:
            findings.append(f"{pending_count} order(s) stuck in pending for >{hours}h")
            for o in pending_items[:10]:
                rows.append({
                    "Order #": o.get("increment_id"),
                    "Status": "pending",
                    "Customer": o.get("customer_email", ""),
                    "Total": f"{o.get('base_grand_total', 0):.2f}",
                    "Created": o.get("created_at", "")[:16],
                })
    except MagentoAPIError:
        pass

    # 2. Payment review
    try:
        review_result = client.search("orders", filters=[
            {"field": "status", "value": "payment_review", "condition_type": "eq"},
        ], page_size=50)
        review_items = review_result.get("items", [])
        review_count = review_result.get("total_count", len(review_items))
        if review_count:
            findings.append(f"{review_count} order(s) in payment_review")
            for o in review_items[:10]:
                rows.append({
                    "Order #": o.get("increment_id"),
                    "Status": "payment_review",
                    "Customer": o.get("customer_email", ""),
                    "Total": f"{o.get('base_grand_total', 0):.2f}",
                    "Created": o.get("created_at", "")[:16],
                })
    except MagentoAPIError:
        pass

    # 3. Recent cancellations
    cancel_start, cancel_end = utc_range(hours)
    try:
        cancel_result = client.search("orders", filters=[
            {"field": "status", "value": "canceled", "condition_type": "eq"},
            {"field": "created_at", "value": cancel_start, "condition_type": "gteq"},
        ], page_size=50)
        cancel_count = cancel_result.get("total_count", 0)
        if cancel_count > 0:
            findings.append(f"{cancel_count} order(s) canceled in last {hours}h")
    except MagentoAPIError:
        pass

    status = "warning" if findings else "ok"
    elapsed = time.monotonic() - t0
    return SectionResult("Order Anomalies", status, elapsed,
                         rows=rows or None, findings=findings or None)


def _section_inventory(client, threshold: int) -> SectionResult:
    """Low stock products (qty <= threshold and manage_stock=1)."""
    t0 = time.monotonic()
    try:
        result = client.search("stockItems", filters=[
            {"field": "qty", "value": str(threshold), "condition_type": "lteq"},
            {"field": "manage_stock", "value": "1", "condition_type": "eq"},
        ], page_size=100, sort_field="qty", sort_dir="ASC")
    except MagentoAPIError as e:
        return SectionResult("Inventory Risks", "error", time.monotonic() - t0, error=str(e))

    items = result.get("items", [])
    if not items:
        return SectionResult("Inventory Risks", "ok", time.monotonic() - t0,
                             findings=[f"No products below threshold of {threshold}."])

    findings = [f"{len(items)} product(s) at or below {threshold} units"]
    rows = []
    for i in items[:20]:
        rows.append({
            "SKU": i.get("sku", ""),
            "Qty": i.get("qty", 0),
            "In Stock": "Yes" if i.get("is_in_stock") else "No",
        })

    return SectionResult("Inventory Risks", "warning" if items else "ok",
                         time.monotonic() - t0, rows=rows, findings=findings)


def _section_promotions(client) -> SectionResult:
    """Check for expired-but-active rules and rules expiring soon."""
    t0 = time.monotonic()
    findings: list[str] = []
    rows: list[dict] = []

    try:
        result = client.search("salesRules/search", filters=[
            {"field": "is_active", "value": "1", "condition_type": "eq"},
        ], page_size=100)
        rules = result.get("items", [])
    except MagentoAPIError as e:
        return SectionResult("Promotion Status", "error", time.monotonic() - t0, error=str(e))

    utc_now = datetime.now(timezone.utc)

    expired = []
    expiring_soon = []
    no_end_date = []

    for rule in rules:
        to_date = rule.get("to_date")
        rule_id = rule.get("rule_id")
        name = rule.get("name", "")

        if to_date and to_date != "NULL":
            try:
                to_dt = datetime.fromisoformat(to_date.replace(" ", "T")).replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                continue
            if to_dt < utc_now:
                expired.append((rule_id, name, to_date))
                rows.append({
                    "Rule ID": rule_id,
                    "Name": name,
                    "Issue": "Expired but still active",
                    "To Date": to_date[:10],
                })
            elif to_dt.timestamp() < utc_now.timestamp() + 48 * 3600:
                expiring_soon.append((rule_id, name, to_date))
                rows.append({
                    "Rule ID": rule_id,
                    "Name": name,
                    "Issue": "Expiring within 48h",
                    "To Date": to_date[:10],
                })
        else:
            no_end_date.append((rule_id, name))

    if expired:
        findings.append(f"{len(expired)} rule(s) expired but still active")
    if expiring_soon:
        findings.append(f"{len(expiring_soon)} rule(s) expiring within 48h")
    if no_end_date:
        findings.append(f"{len(no_end_date)} active rule(s) with no end date")

    status = "warning" if expired else "ok"
    elapsed = time.monotonic() - t0
    if not rows and not findings:
        return SectionResult("Promotion Status", "ok", elapsed,
                             findings=["No active promotions found."])
    return SectionResult("Promotion Status", status, elapsed,
                         rows=rows or None, findings=findings or ["All promotions look healthy."])


def _section_customers(client, hours: int) -> SectionResult:
    """New customer registrations in the last N hours vs previous period."""
    t0 = time.monotonic()
    start, end = utc_range(hours)

    # Previous period for comparison
    utc_end = datetime.now(timezone.utc)
    utc_start = utc_end - timedelta(hours=hours)
    prev_start = utc_start - timedelta(hours=hours)

    filters_current = [
        {"field": "created_at", "value": start, "condition_type": "gteq"},
        {"field": "created_at", "value": end, "condition_type": "lteq"},
    ]
    filters_prev = [
        {"field": "created_at", "value": prev_start.strftime("%Y-%m-%d %H:%M:%S"), "condition_type": "gteq"},
        {"field": "created_at", "value": start, "condition_type": "lteq"},
    ]

    try:
        current_result = client.search("customers/search", filters=filters_current, page_size=1)
        current_count = current_result.get("total_count", 0)
    except MagentoAPIError:
        current_count = 0

    try:
        prev_result = client.search("customers/search", filters=filters_prev, page_size=1)
        prev_count = prev_result.get("total_count", 0)
    except MagentoAPIError:
        prev_count = 0

    # Calculate change
    if prev_count > 0:
        change_pct = ((current_count - prev_count) / prev_count) * 100
        arrow = "↑" if change_pct > 0 else "↓"
        change_str = f"{current_count - prev_count:+d} ({arrow}{abs(change_pct):.1f}%)"
    elif current_count > 0:
        change_str = f"+{current_count} (new)"
    else:
        change_str = "—"

    rows = [
        {"Metric": "New Registrations", "Value": str(current_count)},
        {"Metric": "vs Previous Period", "Value": change_str},
    ]
    elapsed = time.monotonic() - t0
    return SectionResult(f"New Customers (Last {hours}h)", "ok", elapsed, rows=rows)


def _build_key_findings(sections: list[SectionResult]) -> list[str]:
    """Aggregate warnings/errors from all sections into key findings."""
    findings: list[str] = []
    for s in sections:
        if s.status == "error":
            findings.append(f"[{s.title}] Failed: {s.error}")
        elif s.status == "warning" and s.findings:
            for f in s.findings:
                findings.append(f"[{s.title}] {f}")
    return findings


def cmd_brief(args):
    client = get_client(args.site)
    hours = env_default("OPENCLAW_PENDING_HOURS", args.hours, 24)
    threshold = env_default("OPENCLAW_STOCK_THRESHOLD", args.stock_threshold, 10)
    fmt = args.format

    total_start = time.monotonic()

    # Run all sections (independent try/except per section)
    sections: list[SectionResult] = []

    # Sales
    try:
        sections.append(_section_sales(client, hours))
    except Exception as e:
        sections.append(SectionResult("Sales", "error", 0, error=str(e)))

    # Order anomalies
    try:
        sections.append(_section_order_anomalies(client, hours))
    except Exception as e:
        sections.append(SectionResult("Order Anomalies", "error", 0, error=str(e)))

    # Inventory
    try:
        sections.append(_section_inventory(client, threshold))
    except Exception as e:
        sections.append(SectionResult("Inventory Risks", "error", 0, error=str(e)))

    # Promotions
    try:
        sections.append(_section_promotions(client))
    except Exception as e:
        sections.append(SectionResult("Promotion Status", "error", 0, error=str(e)))

    # Customers
    try:
        sections.append(_section_customers(client, hours))
    except Exception as e:
        sections.append(SectionResult("New Customers", "error", 0, error=str(e)))

    total_elapsed = time.monotonic() - total_start

    # Key findings
    key_findings = _build_key_findings(sections)
    findings_section = SectionResult(
        "Key Findings",
        "warning" if key_findings else "ok",
        elapsed_seconds=0,
        findings=key_findings or ["Nothing requiring immediate attention."],
    )

    if fmt == "json":
        all_sections = sections + [findings_section]
        output = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "total_elapsed_seconds": round(total_elapsed, 1),
            "sections": [_section_to_dict(s) for s in all_sections],
        }
        import json
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Data as of {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | Generated in {total_elapsed:.1f}s\n")
        print(render_sections(sections, format="markdown"))
        print("## Key Findings")
        for f in key_findings or ["Nothing requiring immediate attention."]:
            print(f"- {f}")


def main():
    parser = argparse.ArgumentParser(description="Magento 2 Morning Brief")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    parser.add_argument("--hours", type=int, default=None,
                         help="Time window in hours (default: 24)")
    parser.add_argument("--stock-threshold", type=int, default=None,
                         help="Low stock threshold (default: 10)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                         help="Output format (default: markdown)")

    args = parser.parse_args()
    cmd_brief(args)


if __name__ == "__main__":
    main()
