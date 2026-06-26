#!/usr/bin/env python3
"""
GA4 traffic source report with period-over-period comparison.
Optional DingTalk notification via DINGTALK_WEBHOOK (+ DINGTALK_SECRET if the bot uses signing).
"""
import os
import sys
import io
import json
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(SCRIPT_DIR, "ga-credentials.json")

CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
if os.path.isfile(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
else:
    _pid = os.environ.get("GA4_PROPERTY_ID")
    if not _pid:
        print(
            "Missing config.json and GA4_PROPERTY_ID. "
            "Copy config.json.example to config.json or set GA4_PROPERTY_ID.",
            file=sys.stderr,
        )
        sys.exit(1)
    config = {
        "property_id": _pid,
        "property_name": os.environ.get("GA4_PROPERTY_NAME", "GA4 Property"),
    }

PROPERTY_ID = f"properties/{config['property_id']}"
PROPERTY_NAME = config.get("property_name", "Unknown")

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension,
    OrderBy,
)

client = BetaAnalyticsDataClient()


def get_traffic_source_data(start_date: str, end_date: str):
    """Fetch traffic source rows for a GA4 date range."""

    request = RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[
            Dimension(name="sessionSource"),
            Dimension(name="sessionMedium"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
            Metric(name="averageSessionDuration"),
        ],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"))],
    )

    response = client.run_report(request)

    rows = {}
    for row in response.rows:
        source = row.dimension_values[0].value
        medium = row.dimension_values[1].value
        key = f"{source}|{medium}"

        rows[key] = {
            "source": source,
            "medium": medium,
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "views": int(row.metric_values[2].value),
            "engagement": float(row.metric_values[3].value) * 100,
            "duration": float(row.metric_values[4].value),
        }

    return rows


def compare_periods(current: dict, previous: dict) -> list:
    """Join two periods and compute deltas."""

    all_keys = set(current.keys()) | set(previous.keys())
    results = []

    for key in all_keys:
        curr = current.get(
            key,
            {
                "sessions": 0,
                "users": 0,
                "views": 0,
                "engagement": 0,
                "duration": 0,
                "source": "",
                "medium": "",
            },
        )
        prev = previous.get(
            key,
            {"sessions": 0, "users": 0, "views": 0, "engagement": 0, "duration": 0},
        )

        sessions_diff = curr["sessions"] - prev["sessions"]
        sessions_pct = (sessions_diff / prev["sessions"] * 100) if prev["sessions"] > 0 else None

        users_diff = curr["users"] - prev["users"]
        users_pct = (users_diff / prev["users"] * 100) if prev["users"] > 0 else None

        views_diff = curr["views"] - prev["views"]
        views_pct = (views_diff / prev["views"] * 100) if prev["views"] > 0 else None

        results.append(
            {
                "source": curr["source"] or prev["source"],
                "medium": curr["medium"] or prev["medium"],
                "sessions": curr["sessions"],
                "sessions_prev": prev["sessions"],
                "sessions_diff": sessions_diff,
                "sessions_pct": sessions_pct,
                "users": curr["users"],
                "users_prev": prev["users"],
                "users_diff": users_diff,
                "users_pct": users_pct,
                "views": curr["views"],
                "views_prev": prev["views"],
                "views_diff": views_diff,
                "views_pct": views_pct,
                "engagement": curr["engagement"],
                "duration": curr["duration"],
            }
        )

    results.sort(key=lambda x: x["sessions"], reverse=True)
    return results


def format_change(diff: int, pct: float) -> str:
    if pct is None:
        return "🆕" if diff > 0 else "❌"

    if diff > 0:
        return f"🔺 +{diff:,} (+{pct:.1f}%)"
    if diff < 0:
        return f"🔻 {diff:,} ({pct:.1f}%)"
    return "➡️ No change"


def generate_markdown_report(comparison_data: list, current_total: dict, previous_total: dict):
    """Build Markdown report body."""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_sessions_diff = current_total["sessions"] - previous_total["sessions"]
    total_sessions_pct = (
        (total_sessions_diff / previous_total["sessions"] * 100)
        if previous_total["sessions"] > 0
        else 0
    )

    total_users_diff = current_total["users"] - previous_total["users"]
    total_users_pct = (
        (total_users_diff / previous_total["users"] * 100) if previous_total["users"] > 0 else 0
    )

    growing = [d for d in comparison_data if d["sessions_diff"] > 0 and d["sessions_prev"] > 0]
    declining = [d for d in comparison_data if d["sessions_diff"] < 0 and d["sessions_prev"] > 0]
    new_channels = [d for d in comparison_data if d["sessions_prev"] == 0 and d["sessions"] > 0]
    lost_channels = [d for d in comparison_data if d["sessions"] == 0 and d["sessions_prev"] > 0]

    growing.sort(key=lambda x: x["sessions_pct"], reverse=True)
    declining.sort(key=lambda x: x["sessions_pct"])

    report = f"""# 📊 {PROPERTY_NAME} — traffic source report

**Current period**: `7daysAgo`–`yesterday`  
**Previous period**: `14daysAgo`–`8daysAgo`  
**Generated**: {now}

---

## 📈 Overview

| Metric | Current | Previous | Change |
|--------|---------|---------|--------|
| Sessions | {current_total['sessions']:,} | {previous_total['sessions']:,} | {format_change(total_sessions_diff, total_sessions_pct)} |
| Active users | {current_total['users']:,} | {previous_total['users']:,} | {format_change(total_users_diff, total_users_pct)} |
| Page views | {current_total['views']:,} | {previous_total['views']:,} | {format_change(current_total['views'] - previous_total['views'], (current_total['views'] - previous_total['views']) / previous_total['views'] * 100 if previous_total['views'] > 0 else 0)} |

---

## 🔍 Top sources (by sessionSource)

| Rank | Source | Sessions (current) | Sessions (prev) | Change |
|------|--------|-------------------|-------------------|--------|
"""

    source_stats = {}
    for d in comparison_data:
        src = d["source"]
        if src not in source_stats:
            source_stats[src] = {"sessions": 0, "sessions_prev": 0}
        source_stats[src]["sessions"] += d["sessions"]
        source_stats[src]["sessions_prev"] += d["sessions_prev"]

    sorted_sources = sorted(source_stats.items(), key=lambda x: x[1]["sessions"], reverse=True)

    for i, (source, stats) in enumerate(sorted_sources[:10], 1):
        diff = stats["sessions"] - stats["sessions_prev"]
        pct = (diff / stats["sessions_prev"] * 100) if stats["sessions_prev"] > 0 else None
        change_str = format_change(diff, pct)
        report += f"| {i} | {source} | {stats['sessions']:,} | {stats['sessions_prev']:,} | {change_str} |\n"

    report += """
---

## 🎯 Top source / medium pairs (detail)

| Rank | Source | Medium | Sessions (current) | Change |
|------|--------|--------|-------------------|--------|
"""

    for i, d in enumerate(comparison_data[:15], 1):
        change_str = format_change(d["sessions_diff"], d["sessions_pct"])
        report += f"| {i} | {d['source']} | {d['medium']} | {d['sessions']:,} | {change_str} |\n"

    report += """
---

## 💡 Highlights

### 📊 Trend
"""

    if total_sessions_diff > 0:
        report += f"✅ **Up**: total sessions **+{total_sessions_pct:.1f}%** (+{total_sessions_diff:,} vs prior window)\n\n"
    elif total_sessions_diff < 0:
        report += f"⚠️ **Down**: total sessions **{total_sessions_pct:.1f}%** ({total_sessions_diff:,} vs prior window)\n\n"
    else:
        report += "➡️ **Flat**: total sessions unchanged vs prior window\n\n"

    if growing:
        report += "### 🚀 Fastest growth (existing channels)\n\n"
        for i, d in enumerate(growing[:5], 1):
            report += f"{i}. **{d['source']} / {d['medium']}**: {d['sessions']:,} sessions 🔺 +{d['sessions_pct']:.1f}%\n"
        report += "\n"

    if declining:
        report += "### 📉 Largest declines (existing channels)\n\n"
        for i, d in enumerate(declining[:5], 1):
            report += f"{i}. **{d['source']} / {d['medium']}**: {d['sessions']:,} sessions 🔻 {abs(d['sessions_pct']):.1f}%\n"
        report += "\n"

    if new_channels:
        report += "### 🆕 New channels\n\n"
        for i, d in enumerate(new_channels[:5], 1):
            report += f"{i}. **{d['source']} / {d['medium']}**: {d['sessions']:,} sessions\n"
        report += "\n"

    if lost_channels:
        report += "### ❌ Churned channels\n\n"
        for i, d in enumerate(lost_channels[:5], 1):
            report += f"{i}. **{d['source']} / {d['medium']}**: had {d['sessions_prev']:,} sessions last period; **0** this period\n"
        report += "\n"

    report += "### 🎯 Suggestions\n\n"

    suggestions = []
    if growing:
        suggestions.append(
            f"✅ **Scale**: `{growing[0]['source']}` grew strongly — validate quality and consider more investment."
        )
    if declining and declining[0]["sessions_prev"] > 10:
        suggestions.append(
            f"⚠️ **Investigate**: `{declining[0]['source']}` dropped — check tracking, campaigns, or seasonality."
        )
    if new_channels:
        suggestions.append(f"🆕 **New sources**: {len(new_channels)} new channel(s) appeared — monitor for spam or mis-tagged traffic.")

    for i, s in enumerate(suggestions, 1):
        report += f"{i}. {s}\n"

    report += """
---

*Generated by Google Analytics skill*
"""
    return report


def send_to_dingtalk(markdown_content: str) -> bool:
    """Post Markdown to DingTalk if DINGTALK_WEBHOOK is set."""
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse

    try:
        import requests
    except ImportError:
        print("Install requests to use DingTalk: pip install requests", file=sys.stderr)
        return False

    webhook = os.environ.get("DINGTALK_WEBHOOK", "").strip()
    secret = os.environ.get("DINGTALK_SECRET", "").strip()

    if not webhook:
        print("DINGTALK_WEBHOOK not set; skipping DingTalk notification.")
        return False

    if secret:
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode("utf-8")
        string_to_sign = f"{timestamp}\n{secret}"
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = f"{webhook}&timestamp={timestamp}&sign={sign}"
    else:
        url = webhook

    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"{PROPERTY_NAME} — traffic source report",
            "text": markdown_content,
        },
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)
    try:
        result = response.json()
    except Exception:
        return False
    return result.get("errcode", -1) == 0


def main():
    print("=" * 60)
    print(f"📊 {PROPERTY_NAME} — traffic source report (period comparison)")
    print("=" * 60)

    print("\n🔍 Querying current window (7daysAgo–yesterday)...")
    current_data = get_traffic_source_data("7daysAgo", "yesterday")
    print(f"✅ Rows (source/medium combos): {len(current_data)}")

    print("\n🔍 Querying prior window (14daysAgo–8daysAgo)...")
    previous_data = get_traffic_source_data("14daysAgo", "8daysAgo")
    print(f"✅ Rows (source/medium combos): {len(previous_data)}")

    print("\n📊 Comparing periods...")
    comparison_data = compare_periods(current_data, previous_data)

    current_total = {
        "sessions": sum(d["sessions"] for d in current_data.values()),
        "users": sum(d["users"] for d in current_data.values()),
        "views": sum(d["views"] for d in current_data.values()),
    }

    previous_total = {
        "sessions": sum(d["sessions"] for d in previous_data.values()),
        "users": sum(d["users"] for d in previous_data.values()),
        "views": sum(d["views"] for d in previous_data.values()),
    }

    print("\n📝 Building Markdown...")
    report = generate_markdown_report(comparison_data, current_total, previous_total)

    report_file = os.path.join(SCRIPT_DIR, "traffic_source_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"💾 Saved: {report_file}")

    print("\n📤 DingTalk...")
    if send_to_dingtalk(report):
        print("✅ DingTalk delivered.")
    else:
        print("⚠️ DingTalk skipped or failed (check env vars and logs).")

    print("\n" + "=" * 60)
    print("📋 Summary")

    total_diff = current_total["sessions"] - previous_total["sessions"]
    total_pct = (total_diff / previous_total["sessions"] * 100) if previous_total["sessions"] > 0 else 0

    print(f"\nSessions: {format_change(total_diff, total_pct)}")

    growing = [d for d in comparison_data if d["sessions_diff"] > 0 and d["sessions_prev"] > 0]
    if growing:
        growing.sort(key=lambda x: x["sessions_pct"], reverse=True)
        print(f"\n🚀 Top growth: {growing[0]['source']} / {growing[0]['medium']} 🔺 +{growing[0]['sessions_pct']:.1f}%")

    declining = [d for d in comparison_data if d["sessions_diff"] < 0 and d["sessions_prev"] > 0]
    if declining:
        declining.sort(key=lambda x: x["sessions_pct"])
        print(
            f"📉 Largest drop: {declining[0]['source']} / {declining[0]['medium']} "
            f"🔻 {abs(declining[0]['sessions_pct']):.1f}%"
        )

    print("\n" + "=" * 60)
    print("✅ Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
