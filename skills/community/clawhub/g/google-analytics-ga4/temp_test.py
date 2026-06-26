#!/usr/bin/env python3
"""Minimal one-shot report (set GA4_PROPERTY_ID)."""
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(SCRIPT_DIR, "ga-credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

print(f"Credentials path: {creds_path}")
print(f"File exists: {os.path.exists(creds_path)}")

ga4_property_id = os.environ.get("GA4_PROPERTY_ID")
if not ga4_property_id:
    print("Set GA4_PROPERTY_ID to your numeric GA4 property ID.")
    sys.exit(1)

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest,
        DateRange,
        Metric,
    )

    client = BetaAnalyticsDataClient()
    property_id = f"properties/{ga4_property_id}"
    print(f"Querying {property_id}")

    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(start_date="7daysAgo", end_date="yesterday")],
        metrics=[Metric(name="activeUsers")],
    )

    response = client.run_report(request)
    print("OK — activeUsers (aggregated window):")
    for row in response.rows:
        print(f"  {row.metric_values[0].value}")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
