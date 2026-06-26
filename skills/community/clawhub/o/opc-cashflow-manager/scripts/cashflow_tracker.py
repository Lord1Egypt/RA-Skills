#!/usr/bin/env python3
"""
Cash Flow Tracker — Forecast engine, runway calculator, and alert system.

Solo founder cash flow management: probability-weighted forecasting,
3-scenario modeling, burn rate analysis, and survival alerts.

Usage:
    python3 cashflow_tracker.py [cashflow_dir] --index
    python3 cashflow_tracker.py [cashflow_dir] --forecast
    python3 cashflow_tracker.py [cashflow_dir] --runway
    python3 cashflow_tracker.py [cashflow_dir] --alerts
    python3 cashflow_tracker.py [cashflow_dir] --import-invoices [invoices_dir]
    python3 cashflow_tracker.py [cashflow_dir] --dashboard

Output: --json (default) | --human | --quiet (exit code only)
Exit codes: 0 = healthy, 1 = critical alerts exist
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONFIDENCE_PROBABILITY = {
    "high": Decimal("0.95"),
    "medium": Decimal("0.60"),
    "low": Decimal("0.20"),
}

DEFAULT_SCENARIOS = {
    "base": {"inflow_factor": Decimal("1.0"), "outflow_factor": Decimal("1.0")},
    "conservative": {"inflow_factor": Decimal("0.7"), "outflow_factor": Decimal("1.1")},
    "aggressive": {"inflow_factor": Decimal("1.3"), "outflow_factor": Decimal("0.9")},
}

FREQUENCY_DAYS = {
    "weekly": 7,
    "biweekly": 14,
    "monthly": 30,
    "quarterly": 91,
    "annual": 365,
}

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}
TYPE_ORDER = {
    "negative_cash": 0,
    "runway_warning": 1,
    "collection_urgent": 2,
    "large_outflow": 3,
    "concentration_risk": 4,
}

TWO_PLACES = Decimal("0.01")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_date(date_str):
    """Parse YYYY-MM-DD string to date object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def parse_amount(amount_str):
    """Parse decimal-safe string to Decimal. Strips currency symbols."""
    if not amount_str:
        return Decimal("0")
    cleaned = str(amount_str).replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
    try:
        return Decimal(cleaned)
    except Exception:
        return Decimal("0")


def fmt(amount):
    """Format Decimal to 2-place string."""
    return str(amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP))


def today():
    return date.today()


def add_months(d, months):
    """Add months to a date, capping at month end."""
    month = d.month + months
    year = d.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    return d.replace(year=year, month=month, day=min(d.day, max_day))


def week_number(d, reference):
    """Return week number (1-4+) relative to reference date."""
    delta = (d - reference).days
    return max(1, min(4, delta // 7 + 1))


# ---------------------------------------------------------------------------
# Snapshot I/O
# ---------------------------------------------------------------------------


def find_snapshots(cashflow_dir):
    """Find all snapshot.json files under snapshots/."""
    snapshots_dir = os.path.join(cashflow_dir, "snapshots")
    results = []
    if not os.path.isdir(snapshots_dir):
        return results
    for entry in sorted(os.listdir(snapshots_dir), reverse=True):
        path = os.path.join(snapshots_dir, entry, "snapshot.json")
        if os.path.isfile(path):
            results.append(path)
    return results


def load_snapshot(path):
    """Load and return snapshot dict."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_snapshot(path, data):
    """Save snapshot dict to JSON."""
    data["updated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_latest_snapshot(cashflow_dir):
    """Return the most recent snapshot or None."""
    snapshots = find_snapshots(cashflow_dir)
    if not snapshots:
        return None, None
    return snapshots[0], load_snapshot(snapshots[0])


# ---------------------------------------------------------------------------
# Forecast Engine
# ---------------------------------------------------------------------------


def get_probability(inflow):
    """Get probability factor for an inflow entry."""
    if "probability_factor" in inflow and inflow["probability_factor"] is not None:
        return Decimal(str(inflow["probability_factor"]))
    confidence = inflow.get("confidence", "medium")
    return CONFIDENCE_PROBABILITY.get(confidence, Decimal("0.60"))


def calculate_weighted_inflows(inflows, scenario_factor):
    """Calculate total weighted inflows for a scenario."""
    total = Decimal("0")
    for item in inflows:
        if item.get("status") in ("cancelled",):
            continue
        amount = parse_amount(item.get("amount", "0"))
        prob = get_probability(item)
        total += amount * prob * scenario_factor
    return total


def calculate_outflows_for_period(outflows, recurring, period_start, period_end, scenario_factor):
    """Calculate total outflows (committed + expanded recurring) for a date range."""
    total = Decimal("0")

    # Committed outflows within period
    for item in outflows:
        if item.get("status") in ("paid", "cancelled"):
            continue
        due = parse_date(item.get("due_date"))
        if due and period_start <= due <= period_end:
            total += parse_amount(item.get("amount", "0"))

    # Expand recurring commitments into the period
    for item in recurring:
        amount = parse_amount(item.get("amount", "0"))
        freq_days = FREQUENCY_DAYS.get(item.get("frequency", "monthly"), 30)
        next_due = parse_date(item.get("next_due_date"))
        if not next_due:
            continue
        current = next_due
        while current <= period_end:
            if current >= period_start:
                total += amount
            current = current + timedelta(days=freq_days)

    return total * scenario_factor


def run_forecast(snapshot, num_months=4):
    """Run 3-scenario forecast with weekly (month 1) and monthly granularity.

    Returns dict with base/conservative/aggressive projections.
    """
    opening = parse_amount(snapshot.get("opening_cash", {}).get("amount", "0"))
    inflows = snapshot.get("expected_inflows", [])
    outflows = snapshot.get("committed_outflows", [])
    recurring = snapshot.get("recurring_commitments", [])
    scenarios_cfg = snapshot.get("scenarios", {})

    result = {}
    for scenario_name, defaults in DEFAULT_SCENARIOS.items():
        cfg = scenarios_cfg.get(scenario_name, {})
        in_factor = Decimal(str(cfg.get("inflow_factor", defaults["inflow_factor"])))
        out_factor = Decimal(str(cfg.get("outflow_factor", defaults["outflow_factor"])))

        cash = opening
        projections = []

        # Week-by-week for current month (4 weeks)
        t = today()
        month_start = t.replace(day=1)
        for w in range(4):
            w_start = month_start + timedelta(days=w * 7)
            w_end = w_start + timedelta(days=6)

            # Inflows this week
            week_in = Decimal("0")
            for item in inflows:
                if item.get("status") in ("cancelled",):
                    continue
                exp_date = parse_date(item.get("expected_date"))
                if exp_date and w_start <= exp_date <= w_end:
                    amount = parse_amount(item.get("amount", "0"))
                    prob = get_probability(item)
                    week_in += amount * prob * in_factor

            week_out = calculate_outflows_for_period(
                outflows, recurring, w_start, w_end, out_factor
            )

            cash = cash + week_in - week_out
            projections.append({
                "label": f"Week {w + 1} ({w_start.strftime('%m/%d')}–{w_end.strftime('%m/%d')})",
                "period_type": "weekly",
                "inflows": fmt(week_in),
                "outflows": fmt(week_out),
                "cash_position": fmt(cash),
            })

        # Monthly for months 2 through num_months
        for m in range(1, num_months):
            m_start = add_months(month_start, m)
            m_end = add_months(month_start, m + 1) - timedelta(days=1)

            # Inflows this month
            month_in = Decimal("0")
            for item in inflows:
                if item.get("status") in ("cancelled",):
                    continue
                exp_date = parse_date(item.get("expected_date"))
                if exp_date and m_start <= exp_date <= m_end:
                    amount = parse_amount(item.get("amount", "0"))
                    prob = get_probability(item)
                    month_in += amount * prob * in_factor

            month_out = calculate_outflows_for_period(
                outflows, recurring, m_start, m_end, out_factor
            )

            cash = cash + month_in - month_out
            projections.append({
                "label": m_start.strftime("%B %Y"),
                "period_type": "monthly",
                "inflows": fmt(month_in),
                "outflows": fmt(month_out),
                "cash_position": fmt(cash),
            })

        result[scenario_name] = {
            "projections": projections,
            "final_cash": fmt(cash),
        }

    return result


# ---------------------------------------------------------------------------
# Runway Calculator
# ---------------------------------------------------------------------------


def calculate_runway(snapshot):
    """Calculate burn rate, weighted income, and runway months."""
    opening = parse_amount(snapshot.get("opening_cash", {}).get("amount", "0"))
    outflows = snapshot.get("committed_outflows", [])
    recurring = snapshot.get("recurring_commitments", [])
    inflows = snapshot.get("expected_inflows", [])

    # Monthly burn from recurring (critical + important)
    burn_critical = Decimal("0")
    burn_important = Decimal("0")
    burn_optional = Decimal("0")
    for item in recurring:
        amount = parse_amount(item.get("amount", "0"))
        freq = item.get("frequency", "monthly")
        # Normalize to monthly
        if freq == "weekly":
            monthly = amount * Decimal("4.33")
        elif freq == "biweekly":
            monthly = amount * Decimal("2.17")
        elif freq == "quarterly":
            monthly = amount / Decimal("3")
        elif freq == "annual":
            monthly = amount / Decimal("12")
        else:
            monthly = amount

        ess = item.get("essentiality", "important")
        if ess == "critical":
            burn_critical += monthly
        elif ess == "important":
            burn_important += monthly
        else:
            burn_optional += monthly

    # Add one-time outflows averaged (upcoming only)
    upcoming_one_time = Decimal("0")
    for item in outflows:
        if item.get("status") in ("paid", "cancelled"):
            continue
        upcoming_one_time += parse_amount(item.get("amount", "0"))

    total_burn = burn_critical + burn_important + burn_optional + upcoming_one_time

    # Weighted monthly income
    weighted_income = Decimal("0")
    for item in inflows:
        if item.get("status") in ("cancelled", "received"):
            continue
        amount = parse_amount(item.get("amount", "0"))
        prob = get_probability(item)
        weighted_income += amount * prob

    net_burn = total_burn - weighted_income
    cash_flow_positive = net_burn <= 0

    # Runway calculations
    if net_burn > 0:
        runway_base = opening / net_burn
    else:
        runway_base = Decimal("-1")  # infinite

    # Conservative runway
    net_burn_conservative = total_burn * Decimal("1.1") - weighted_income * Decimal("0.7")
    if net_burn_conservative > 0:
        runway_conservative = opening / net_burn_conservative
    else:
        runway_conservative = Decimal("-1")

    # Aggressive runway
    net_burn_aggressive = total_burn * Decimal("0.9") - weighted_income * Decimal("1.3")
    if net_burn_aggressive > 0:
        runway_aggressive = opening / net_burn_aggressive
    else:
        runway_aggressive = Decimal("-1")

    # Zero-income runway (critical expenses only)
    if burn_critical > 0:
        zero_income_runway = opening / burn_critical
    else:
        zero_income_runway = Decimal("-1")

    return {
        "opening_cash": fmt(opening),
        "burn_critical": fmt(burn_critical),
        "burn_important": fmt(burn_important),
        "burn_optional": fmt(burn_optional),
        "monthly_burn_rate": fmt(total_burn),
        "weighted_monthly_income": fmt(weighted_income),
        "net_monthly_burn": fmt(net_burn),
        "cash_flow_positive": cash_flow_positive,
        "runway_base": float(runway_base.quantize(Decimal("0.1"))) if runway_base > 0 else None,
        "runway_conservative": float(runway_conservative.quantize(Decimal("0.1"))) if runway_conservative > 0 else None,
        "runway_aggressive": float(runway_aggressive.quantize(Decimal("0.1"))) if runway_aggressive > 0 else None,
        "zero_income_runway": float(zero_income_runway.quantize(Decimal("0.1"))) if zero_income_runway > 0 else None,
        "burn_no_optional": fmt(burn_critical + burn_important),
        "burn_critical_only": fmt(burn_critical),
    }


# ---------------------------------------------------------------------------
# Alert System
# ---------------------------------------------------------------------------


def check_alerts(snapshot, forecast=None, runway=None):
    """Check all alert triggers and return alerts list."""
    alerts = []
    t = today()
    opening = parse_amount(snapshot.get("opening_cash", {}).get("amount", "0"))
    inflows = snapshot.get("expected_inflows", [])
    outflows = snapshot.get("committed_outflows", [])

    # Runway alerts
    if runway:
        rc = runway.get("runway_conservative")
        if rc is not None:
            if rc < 3:
                alerts.append({
                    "type": "runway_warning",
                    "severity": "critical",
                    "message": f"Conservative runway is {rc} months — below 3-month critical threshold",
                    "action_recommended": "Activate survival mode: cut all optional expenses, chase all AR, consider bridge financing",
                    "triggered_at": t.isoformat(),
                })
            elif rc < 6:
                alerts.append({
                    "type": "runway_warning",
                    "severity": "warning",
                    "message": f"Conservative runway is {rc} months — below 6-month warning threshold",
                    "action_recommended": "Start cost optimization, accelerate collections, review pricing",
                    "triggered_at": t.isoformat(),
                })

    # Negative cash in any scenario
    if forecast:
        for scenario_name in ("conservative", "base", "aggressive"):
            scenario = forecast.get(scenario_name, {})
            for proj in scenario.get("projections", []):
                cash = parse_amount(proj.get("cash_position", "0"))
                if cash < 0:
                    alerts.append({
                        "type": "negative_cash",
                        "severity": "critical",
                        "message": f"Projected negative cash ({fmt(cash)}) in {scenario_name} scenario: {proj['label']}",
                        "action_recommended": "Immediate action required — defer non-critical outflows, accelerate collections",
                        "triggered_at": t.isoformat(),
                    })
                    break  # One alert per scenario

    # Collection urgent
    for item in inflows:
        if item.get("status") in ("cancelled", "received"):
            continue
        exp_date = parse_date(item.get("expected_date"))
        if exp_date and exp_date < t:
            days_overdue = (t - exp_date).days
            amount = parse_amount(item.get("amount", "0"))
            confidence = item.get("confidence", "medium")
            if days_overdue > 30:
                alerts.append({
                    "type": "collection_urgent",
                    "severity": "critical",
                    "message": f"{item.get('source', 'Unknown')} — {fmt(amount)} is {days_overdue} days overdue",
                    "action_recommended": f"Escalate collection for {item.get('source', 'Unknown')} immediately",
                    "triggered_at": t.isoformat(),
                })
            elif days_overdue > 7 and confidence == "high":
                alerts.append({
                    "type": "collection_urgent",
                    "severity": "warning",
                    "message": f"{item.get('source', 'Unknown')} — {fmt(amount)} is {days_overdue} days overdue (was high-confidence)",
                    "action_recommended": f"Follow up with {item.get('source', 'Unknown')} on overdue payment",
                    "triggered_at": t.isoformat(),
                })

    # Large outflow
    for item in outflows:
        if item.get("status") in ("paid", "cancelled"):
            continue
        amount = parse_amount(item.get("amount", "0"))
        if opening > 0 and amount / opening > Decimal("0.3"):
            pct = int(amount / opening * 100)
            alerts.append({
                "type": "large_outflow",
                "severity": "warning",
                "message": f"{item.get('payee', 'Unknown')} — {fmt(amount)} is {pct}% of cash on hand",
                "action_recommended": f"Ensure sufficient cash before {item.get('due_date', 'unknown date')} for {item.get('payee', 'Unknown')}",
                "triggered_at": t.isoformat(),
            })

    # Concentration risk
    total_weighted = Decimal("0")
    by_source = {}
    for item in inflows:
        if item.get("status") in ("cancelled", "received"):
            continue
        amount = parse_amount(item.get("amount", "0")) * get_probability(item)
        source = item.get("source", "Unknown")
        by_source[source] = by_source.get(source, Decimal("0")) + amount
        total_weighted += amount

    if total_weighted > 0:
        for source, amount in by_source.items():
            if amount / total_weighted > Decimal("0.5"):
                pct = int(amount / total_weighted * 100)
                alerts.append({
                    "type": "concentration_risk",
                    "severity": "warning",
                    "message": f"{source} represents {pct}% of expected inflows — high concentration risk",
                    "action_recommended": "Diversify client base — if this client delays or churns, impact is severe",
                    "triggered_at": t.isoformat(),
                })

    # Sort alerts
    alerts.sort(key=lambda a: (
        SEVERITY_ORDER.get(a["severity"], 9),
        TYPE_ORDER.get(a["type"], 9),
    ))

    return alerts


# ---------------------------------------------------------------------------
# Invoice Import (opc-invoice-manager integration)
# ---------------------------------------------------------------------------


def import_invoices(cashflow_dir, invoices_dir):
    """Import sent/overdue invoices from opc-invoice-manager as expected inflows."""
    index_path = os.path.join(invoices_dir, "INDEX.json")
    if not os.path.isfile(index_path):
        print("No INDEX.json found in invoices directory", file=sys.stderr)
        return {"imported": 0, "skipped": 0, "errors": []}

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    invoices = index_data.get("invoices", index_data if isinstance(index_data, list) else [])
    if isinstance(index_data, dict) and "entries" in index_data:
        invoices = index_data["entries"]

    # Load or create current snapshot
    snap_path, snapshot = get_latest_snapshot(cashflow_dir)
    if not snapshot:
        period = today().strftime("%Y-%m")
        snap_path = os.path.join(cashflow_dir, "snapshots", period, "snapshot.json")
        snapshot = {
            "snapshot_id": period,
            "period": period,
            "status": "draft",
            "opening_cash": {"amount": "0", "as_of_date": today().isoformat(), "source": "manual"},
            "expected_inflows": [],
            "committed_outflows": [],
            "recurring_commitments": [],
            "scenarios": {},
            "alerts": [],
            "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    existing_refs = {
        item.get("invoice_ref")
        for item in snapshot.get("expected_inflows", [])
        if item.get("invoice_ref")
    }

    imported = 0
    skipped = 0
    errors = []

    for inv in invoices:
        inv_id = inv.get("invoice_id", inv.get("invoice_number", ""))
        status = inv.get("status", "")

        # Skip non-actionable
        if status in ("paid", "void", "draft"):
            skipped += 1
            continue

        # Skip already imported
        if inv_id in existing_refs:
            skipped += 1
            continue

        # Determine amount
        amount = inv.get("outstanding_amount", inv.get("total_amount", "0"))
        due_date = inv.get("due_date", "")
        client = inv.get("client_name", inv.get("counterparty", "Unknown"))

        # Map status to confidence
        d = parse_date(due_date)
        if d and d < today():
            days_overdue = (today() - d).days
            if days_overdue > 60:
                confidence = "low"
                prob = "0.10"
            elif days_overdue > 30:
                confidence = "low"
                prob = "0.30"
            else:
                confidence = "medium"
                prob = "0.60"
        elif status == "partial":
            confidence = "high"
            prob = "0.80"
        else:
            confidence = "high"
            prob = "0.95"

        weighted = fmt(parse_amount(amount) * Decimal(prob))

        inflow = {
            "id": f"inv-import-{inv_id}",
            "source": client,
            "amount": str(amount),
            "expected_date": due_date or today().isoformat(),
            "confidence": confidence,
            "probability_factor": float(prob),
            "weighted_amount": weighted,
            "invoice_ref": inv_id,
            "status": "expected",
            "notes": f"Auto-imported from opc-invoice-manager (invoice status: {status})",
        }

        snapshot.setdefault("expected_inflows", []).append(inflow)
        imported += 1

    snapshot["invoice_import_date"] = today().isoformat()
    save_snapshot(snap_path, snapshot)

    return {"imported": imported, "skipped": skipped, "snapshot_path": snap_path}


# ---------------------------------------------------------------------------
# Index Builder
# ---------------------------------------------------------------------------


def build_index(cashflow_dir):
    """Build INDEX.json from all snapshots."""
    snapshots = find_snapshots(cashflow_dir)
    entries = []
    for path in snapshots:
        try:
            data = load_snapshot(path)
            opening = data.get("opening_cash", {}).get("amount", "0")
            summary = data.get("summary", {})
            entries.append({
                "snapshot_id": data.get("snapshot_id", ""),
                "period": data.get("period", ""),
                "status": data.get("status", "draft"),
                "opening_cash": opening,
                "projected_cash_conservative": summary.get("projected_cash_conservative", ""),
                "runway_conservative": summary.get("runway_months_conservative"),
                "alert_count": len(data.get("alerts", [])),
                "critical_alerts": sum(
                    1 for a in data.get("alerts", []) if a.get("severity") == "critical"
                ),
                "inflow_count": len(data.get("expected_inflows", [])),
                "outflow_count": len(data.get("committed_outflows", [])),
                "path": path,
            })
        except Exception as e:
            print(f"Warning: could not load {path}: {e}", file=sys.stderr)

    index = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "snapshot_count": len(entries),
        "snapshots": entries,
    }

    index_path = os.path.join(cashflow_dir, "INDEX.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return index


# ---------------------------------------------------------------------------
# Summary Generator
# ---------------------------------------------------------------------------


def generate_summary(snapshot):
    """Calculate and attach summary fields to snapshot."""
    inflows = snapshot.get("expected_inflows", [])
    outflows = snapshot.get("committed_outflows", [])

    total_raw = sum(parse_amount(i.get("amount", "0")) for i in inflows if i.get("status") != "cancelled")
    total_weighted = calculate_weighted_inflows(inflows, Decimal("1.0"))
    total_out = sum(
        parse_amount(o.get("amount", "0"))
        for o in outflows
        if o.get("status") not in ("paid", "cancelled")
    )

    opening = parse_amount(snapshot.get("opening_cash", {}).get("amount", "0"))

    runway_data = calculate_runway(snapshot)

    snapshot["summary"] = {
        "total_inflows_raw": fmt(total_raw),
        "total_inflows_weighted": fmt(total_weighted),
        "total_outflows": fmt(total_out),
        "projected_cash_base": fmt(opening + total_weighted - total_out),
        "projected_cash_conservative": fmt(
            opening + total_weighted * Decimal("0.7") - total_out * Decimal("1.1")
        ),
        "projected_cash_aggressive": fmt(
            opening + total_weighted * Decimal("1.3") - total_out * Decimal("0.9")
        ),
        "monthly_burn_rate": runway_data["monthly_burn_rate"],
        "weighted_monthly_income": runway_data["weighted_monthly_income"],
        "net_monthly_burn": runway_data["net_monthly_burn"],
        "runway_months": runway_data["runway_base"],
        "runway_months_conservative": runway_data["runway_conservative"],
        "cash_flow_positive": runway_data["cash_flow_positive"],
    }

    return snapshot["summary"]


# ---------------------------------------------------------------------------
# Human-Readable Formatters
# ---------------------------------------------------------------------------


def format_forecast_human(forecast, snapshot):
    """Format forecast as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("CASH FLOW FORECAST")
    lines.append("=" * 60)

    opening = snapshot.get("opening_cash", {})
    lines.append(f"Opening Cash: ${opening.get('amount', '0')} (as of {opening.get('as_of_date', 'N/A')})")
    lines.append("")

    for scenario in ("conservative", "base", "aggressive"):
        data = forecast.get(scenario, {})
        label = scenario.upper()
        if scenario == "conservative":
            label += " (USE THIS FOR DECISIONS)"
        lines.append(f"--- {label} ---")

        for proj in data.get("projections", []):
            cash = proj["cash_position"]
            marker = " <<<" if parse_amount(cash) < 0 else ""
            lines.append(
                f"  {proj['label']:30s}  In: ${proj['inflows']:>10s}  "
                f"Out: ${proj['outflows']:>10s}  Cash: ${cash:>10s}{marker}"
            )
        lines.append(f"  Final: ${data.get('final_cash', '0')}")
        lines.append("")

    return "\n".join(lines)


def format_runway_human(runway_data):
    """Format runway analysis as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("RUNWAY ANALYSIS")
    lines.append("=" * 60)
    lines.append(f"Cash on hand:          ${runway_data['opening_cash']}")
    lines.append(f"Monthly burn rate:     ${runway_data['monthly_burn_rate']}")
    lines.append(f"  Critical:            ${runway_data['burn_critical']}")
    lines.append(f"  Important:           ${runway_data['burn_important']}")
    lines.append(f"  Optional:            ${runway_data['burn_optional']}")
    lines.append(f"Weighted income:       ${runway_data['weighted_monthly_income']}")
    lines.append(f"Net monthly burn:      ${runway_data['net_monthly_burn']}")
    lines.append("")

    rb = runway_data['runway_base']
    rc = runway_data['runway_conservative']
    ra = runway_data['runway_aggressive']

    lines.append(f"Runway (base):          {rb if rb else 'unlimited'} months")
    lines.append(f"Runway (conservative):  {rc if rc else 'unlimited'} months  <-- USE THIS")
    lines.append(f"Runway (aggressive):    {ra if ra else 'unlimited'} months")

    if runway_data["cash_flow_positive"]:
        lines.append("")
        lines.append("Cash-flow POSITIVE. You're earning more than spending.")
        zi = runway_data["zero_income_runway"]
        if zi:
            lines.append(f"If all income stops: {zi} months on critical expenses only.")

    # Status
    lines.append("")
    if rc is not None:
        if rc < 3:
            lines.append("STATUS: CRITICAL — Conservative runway < 3 months")
        elif rc < 6:
            lines.append("STATUS: WARNING — Conservative runway < 6 months")
        else:
            lines.append("STATUS: HEALTHY — Conservative runway >= 6 months")
    else:
        lines.append("STATUS: HEALTHY — Cash-flow positive across scenarios")

    return "\n".join(lines)


def format_alerts_human(alerts):
    """Format alerts as human-readable text."""
    if not alerts:
        return "No active alerts. Cash position looks healthy."

    lines = []
    lines.append("=" * 60)
    lines.append("ALERTS")
    lines.append("=" * 60)

    icons = {"critical": "[!!!]", "warning": "[!!]", "info": "[i]"}
    for alert in alerts:
        icon = icons.get(alert["severity"], "[?]")
        lines.append(f"{icon} {alert['type'].upper()} ({alert['severity']})")
        lines.append(f"    {alert['message']}")
        lines.append(f"    -> {alert['action_recommended']}")
        lines.append("")

    return "\n".join(lines)


def format_dashboard_human(snapshot, forecast, runway_data, alerts):
    """Format dashboard as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("CASH POSITION DASHBOARD")
    lines.append(f"As of: {today().isoformat()}")
    lines.append("=" * 60)

    opening = snapshot.get("opening_cash", {}).get("amount", "0")
    summary = snapshot.get("summary", {})

    lines.append(f"Cash on hand:                ${opening}")
    lines.append(f"This month inflows (weighted): ${summary.get('total_inflows_weighted', '0')}")
    lines.append(f"This month outflows:           ${summary.get('total_outflows', '0')}")
    lines.append(f"Projected EOM (base):          ${summary.get('projected_cash_base', '0')}")
    lines.append(f"Projected EOM (conservative):  ${summary.get('projected_cash_conservative', '0')}")
    lines.append("")
    lines.append(f"Burn rate: ${runway_data['monthly_burn_rate']}/mo")

    rc = runway_data['runway_conservative']
    lines.append(f"Runway (conservative): {rc if rc else 'unlimited'} months")
    lines.append("")

    if alerts:
        lines.append("--- ALERTS ---")
        icons = {"critical": "[!!!]", "warning": "[!!]", "info": "[i]"}
        for alert in alerts[:5]:
            icon = icons.get(alert["severity"], "[?]")
            lines.append(f"  {icon} {alert['message']}")
            lines.append(f"      -> {alert['action_recommended']}")
        lines.append("")
    else:
        lines.append("No active alerts.")
        lines.append("")

    # Top actions
    actions = []
    for item in snapshot.get("expected_inflows", []):
        exp = parse_date(item.get("expected_date"))
        if exp and exp < today() and item.get("status") == "expected":
            days = (today() - exp).days
            actions.append(f"Chase {item['source']} — ${item['amount']} ({days} days overdue)")

    if actions:
        lines.append("--- TOP ACTIONS ---")
        for i, action in enumerate(actions[:3], 1):
            lines.append(f"  {i}. {action}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Cash Flow Tracker — Forecast, runway, and alerts for solo founders"
    )
    parser.add_argument(
        "cashflow_dir",
        nargs="?",
        default=".",
        help="Path to cashflow data directory (default: current dir)"
    )
    parser.add_argument("--index", action="store_true", help="Build/update INDEX.json")
    parser.add_argument("--forecast", action="store_true", help="Run 3-scenario forecast")
    parser.add_argument("--runway", action="store_true", help="Calculate runway and burn rate")
    parser.add_argument("--alerts", action="store_true", help="Check alert triggers")
    parser.add_argument("--dashboard", action="store_true", help="Generate dashboard summary")
    parser.add_argument("--import-invoices", metavar="INVOICES_DIR", help="Import from opc-invoice-manager")
    parser.add_argument("--json", action="store_true", default=True, help="JSON output (default)")
    parser.add_argument("--human", action="store_true", help="Human-readable output")
    parser.add_argument("--quiet", action="store_true", help="Exit code only (1 if critical)")

    args = parser.parse_args()
    cashflow_dir = os.path.abspath(args.cashflow_dir)

    has_critical = False

    # Import invoices
    if args.import_invoices:
        result = import_invoices(cashflow_dir, os.path.abspath(args.import_invoices))
        if args.quiet:
            sys.exit(0)
        if args.human:
            print(f"Imported {result['imported']} invoices, skipped {result['skipped']}")
        else:
            print(json.dumps(result, indent=2))
        return

    # Index
    if args.index:
        index = build_index(cashflow_dir)
        if args.quiet:
            sys.exit(0)
        if args.human:
            print(f"Index built: {index['snapshot_count']} snapshots")
            for s in index["snapshots"]:
                print(f"  {s['period']} — opening: ${s['opening_cash']}, alerts: {s['alert_count']}")
        else:
            print(json.dumps(index, indent=2))
        return

    # Load snapshot for other operations
    snap_path, snapshot = get_latest_snapshot(cashflow_dir)
    if not snapshot:
        print("No snapshot found. Create a snapshot first.", file=sys.stderr)
        sys.exit(1)

    # Generate summary
    generate_summary(snapshot)

    # Forecast
    if args.forecast:
        forecast = run_forecast(snapshot)
        runway_data = calculate_runway(snapshot)
        alerts = check_alerts(snapshot, forecast=forecast, runway=runway_data)
        snapshot["alerts"] = alerts
        save_snapshot(snap_path, snapshot)

        has_critical = any(a["severity"] == "critical" for a in alerts)

        if args.quiet:
            sys.exit(1 if has_critical else 0)
        if args.human:
            print(format_forecast_human(forecast, snapshot))
            print()
            print(format_alerts_human(alerts))
        else:
            print(json.dumps({
                "forecast": forecast,
                "alerts": alerts,
                "summary": snapshot.get("summary", {}),
            }, indent=2))

    # Runway
    elif args.runway:
        runway_data = calculate_runway(snapshot)
        forecast = run_forecast(snapshot)
        alerts = check_alerts(snapshot, forecast=forecast, runway=runway_data)
        snapshot["alerts"] = alerts
        save_snapshot(snap_path, snapshot)

        has_critical = any(a["severity"] == "critical" for a in alerts)

        if args.quiet:
            sys.exit(1 if has_critical else 0)
        if args.human:
            print(format_runway_human(runway_data))
        else:
            print(json.dumps({
                "runway": runway_data,
                "alerts": alerts,
            }, indent=2))

    # Alerts only
    elif args.alerts:
        forecast = run_forecast(snapshot)
        runway_data = calculate_runway(snapshot)
        alerts = check_alerts(snapshot, forecast=forecast, runway=runway_data)
        snapshot["alerts"] = alerts
        save_snapshot(snap_path, snapshot)

        has_critical = any(a["severity"] == "critical" for a in alerts)

        if args.quiet:
            sys.exit(1 if has_critical else 0)
        if args.human:
            print(format_alerts_human(alerts))
        else:
            print(json.dumps({"alerts": alerts}, indent=2))

    # Dashboard
    elif args.dashboard:
        forecast = run_forecast(snapshot)
        runway_data = calculate_runway(snapshot)
        alerts = check_alerts(snapshot, forecast=forecast, runway=runway_data)
        snapshot["alerts"] = alerts
        save_snapshot(snap_path, snapshot)

        has_critical = any(a["severity"] == "critical" for a in alerts)

        if args.quiet:
            sys.exit(1 if has_critical else 0)
        if args.human:
            print(format_dashboard_human(snapshot, forecast, runway_data, alerts))
        else:
            print(json.dumps({
                "dashboard": {
                    "opening_cash": snapshot.get("opening_cash", {}),
                    "summary": snapshot.get("summary", {}),
                    "runway": runway_data,
                    "alerts": alerts,
                },
            }, indent=2))

    else:
        # Default: show dashboard
        forecast = run_forecast(snapshot)
        runway_data = calculate_runway(snapshot)
        alerts = check_alerts(snapshot, forecast=forecast, runway=runway_data)
        has_critical = any(a["severity"] == "critical" for a in alerts)

        if args.quiet:
            sys.exit(1 if has_critical else 0)
        if args.human:
            print(format_dashboard_human(snapshot, forecast, runway_data, alerts))
        else:
            print(json.dumps({
                "summary": snapshot.get("summary", {}),
                "alerts": alerts,
            }, indent=2))

    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
