from init_db import init_db, get_db
from logic import (
    calculate_burn_rate, predict_blackout, check_outages,
    check_budget, comparison_insights, is_onboarded,
)
from datetime import datetime, timedelta


def check_status():
    remaining = predict_blackout()

    with get_db() as conn:
        last_reading = conn.execute(
            "SELECT balance, timestamp FROM readings ORDER BY id DESC LIMIT 1"
        ).fetchone()

    alerts = []

    if remaining is not None and remaining < 24:
        eta = (datetime.now() + timedelta(hours=remaining)).strftime("%I:%M %p")
        alerts.append({
            "type": "LOW_BALANCE_WARNING",
            "message": f"Niaje! You only have {remaining:.1f} hours of power left based on your current usage. "
                       f"You'll likely run out by {eta}. Top up soon!",
        })

    if last_reading:
        last_time = datetime.strptime(last_reading[1], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_time).total_seconds() > 48 * 3600:
            alerts.append({
                "type": "SPOT_CHECK_REQUEST",
                "message": "Niaje! I haven't had a meter reading in a while. "
                           "Can you press 20# and tell me what the units say? It helps me stay accurate.",
            })

    # Only check outages if user has set their area
    if is_onboarded():
        outage_msg = check_outages()
        if outage_msg and "No planned outages" not in outage_msg:
            alerts.append({"type": "PLANNED_OUTAGE", "message": outage_msg})

    budget_msg = check_budget()
    if budget_msg and ("⚠️" in budget_msg or "🚨" in budget_msg):
        alerts.append({"type": "BUDGET_WARNING", "message": budget_msg})

    return alerts


def weekly_summary():
    """Generate a weekly consumption and spend summary."""
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        c = conn.cursor()
        units_bought, amount_spent, purchase_count = c.execute(
            "SELECT COALESCE(SUM(units),0), COALESCE(SUM(amount),0), COUNT(*) "
            "FROM purchases WHERE timestamp >= ?",
            (week_ago,),
        ).fetchone()
        readings = c.execute(
            "SELECT timestamp, balance FROM readings WHERE timestamp >= ? ORDER BY timestamp ASC",
            (week_ago,),
        ).fetchall()

    units_consumed = None
    if len(readings) >= 2:
        units_consumed = (readings[0][1] + units_bought) - readings[-1][1]
        if units_consumed < 0:
            units_consumed = None  # purchase timing skew — fall back to burn rate

    burn_rate = calculate_burn_rate()

    lines = ["📊 *Weekly KPLC Summary*", ""]
    lines.append(f"Top-ups: {purchase_count} purchases, {units_bought:.1f} units (KES {amount_spent:,.0f})")

    if units_consumed is not None and units_consumed > 0:
        lines.append(f"Consumed: ~{units_consumed:.1f} units this week")
        projected_monthly = units_consumed * (30 / 7)
        monthly_cost = (amount_spent / units_bought * projected_monthly) if units_bought > 0 else 0
        lines.append(f"Projected monthly: ~{projected_monthly:.0f} units (~KES {monthly_cost:,.0f})")
    elif burn_rate:
        lines.append(f"Est. weekly consumption: ~{burn_rate * 24 * 7:.1f} units (from burn rate)")

    remaining = predict_blackout()
    if remaining:
        lines.append(f"Current runway: ~{remaining:.0f} hours")

    insights = comparison_insights()
    if insights:
        lines.append("")
        lines.append(insights)

    return {"type": "WEEKLY_SUMMARY", "message": "\n".join(lines)}


if __name__ == "__main__":
    init_db()
    for alert in check_status():
        print(f"[{alert['type']}] {alert['message']}")
    summary = weekly_summary()
    print(f"\n[{summary['type']}]\n{summary['message']}")
