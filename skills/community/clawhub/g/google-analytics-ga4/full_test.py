#!/usr/bin/env python3
"""Manual end-to-end checks against one GA4 property (set GA4_PROPERTY_ID)."""
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(SCRIPT_DIR, "ga-credentials.json")

_raw_id = os.environ.get("GA4_PROPERTY_ID")
if not _raw_id:
    print("Set GA4_PROPERTY_ID to your numeric GA4 property ID, then re-run.")
    sys.exit(1)

PROPERTY_ID = f"properties/{_raw_id}"

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Metric,
    Dimension,
    OrderBy,
)

client = BetaAnalyticsDataClient()

print("=" * 60)
print("Google Analytics manual integration test")
print("=" * 60)

print("\nRealtime — activeUsers")
print("-" * 40)
try:
    realtime_request = RunRealtimeReportRequest(
        property=PROPERTY_ID,
        metrics=[Metric(name="activeUsers")],
    )
    realtime_response = client.run_realtime_report(realtime_request)
    for row in realtime_response.rows:
        print(f"  activeUsers: {row.metric_values[0].value}")
    print("  OK")
except Exception as e:
    print(f"  Error: {e}")

print("\nYesterday — headline metrics")
print("-" * 40)
try:
    yesterday_request = RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date="yesterday", end_date="yesterday")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="engagementRate"),
        ],
    )
    response = client.run_report(yesterday_request)
    for row in response.rows:
        print(f"  activeUsers: {row.metric_values[0].value}")
        print(f"  sessions: {row.metric_values[1].value}")
        print(f"  screenPageViews: {row.metric_values[2].value}")
        print(f"  engagementRate: {float(row.metric_values[3].value)*100:.1f}%")
    print("  OK")
except Exception as e:
    print(f"  Error: {e}")

print("\nLast 7 days — activeUsers by date")
print("-" * 40)
try:
    trend_request = RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")],
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],
        order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))],
    )
    trend_response = client.run_report(trend_request)
    print(f"  {'date':<12} {'activeUsers':>12}")
    print(f"  {'-'*12} {'-'*12}")
    for row in trend_response.rows:
        date_str = row.dimension_values[0].value
        users = row.metric_values[0].value
        print(f"  {date_str:<12} {users:>12}")
    print("  OK")
except Exception as e:
    print(f"  Error: {e}")

print("\nCountries — top 5 by activeUsers")
print("-" * 40)
try:
    country_request = RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")],
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="activeUsers"))],
        limit=5,
    )
    country_response = client.run_report(country_request)
    print(f"  {'#':<4} {'country':<20} {'activeUsers':>12}")
    print(f"  {'-'*4} {'-'*20} {'-'*12}")
    for i, row in enumerate(country_response.rows, 1):
        country = row.dimension_values[0].value
        users = row.metric_values[0].value
        print(f"  {i:<4} {country:<20} {users:>12}")
    print("  OK")
except Exception as e:
    print(f"  Error: {e}")

print("\nDevice category — session mix")
print("-" * 40)
try:
    device_request = RunReportRequest(
        property=PROPERTY_ID,
        date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")],
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="sessions")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"))],
    )
    device_response = client.run_report(device_request)
    total = sum(int(row.metric_values[0].value) for row in device_response.rows)
    print(f"  {'deviceCategory':<16} {'sessions':>10} {'share':>10}")
    print(f"  {'-'*16} {'-'*10} {'-'*10}")
    for row in device_response.rows:
        device = row.dimension_values[0].value
        sessions = int(row.metric_values[0].value)
        pct = (sessions / total * 100) if total > 0 else 0
        print(f"  {device:<16} {sessions:>10} {pct:>9.1f}%")
    print("  OK")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 60)
print("Done")
print("=" * 60)
