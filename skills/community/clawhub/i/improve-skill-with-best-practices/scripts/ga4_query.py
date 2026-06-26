#!/usr/bin/env python3
"""Google Analytics 4 Data API query tool.

Usage:
    python ga4_query.py --property-id 123456789 --preset traffic_overview \
        --start-date 2025-01-01 --end-date 2025-03-01

    python ga4_query.py --property-id 123456789 --preset top_pages --limit 50

    python ga4_query.py --property-id 123456789 \
        --dimensions pagePath,deviceCategory \
        --metrics sessions,bounceRate \
        --start-date 30daysAgo --end-date yesterday \
        --order-by="-sessions"

Reads .env from: .skills-data/google-analytics-and-search-improve/.env
Env vars: GA4_PROPERTY_ID
"""

import argparse
import json
import os
import sys

from utils import require_google_credentials

# Auto-discover credentials before importing Google client libs
# (BetaAnalyticsDataClient reads GOOGLE_APPLICATION_CREDENTIALS on init)
require_google_credentials()

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    MetricType,
    OrderBy,
    RunReportRequest,
)


PRESETS = {
    "traffic_overview": {
        "dimensions": ["date"],
        "metrics": ["sessions", "totalUsers", "newUsers", "screenPageViews",
                     "bounceRate", "averageSessionDuration", "engagementRate"],
        "order_by": "date",
    },
    "top_pages": {
        "dimensions": ["pagePath", "pageTitle"],
        "metrics": ["screenPageViews", "sessions", "totalUsers",
                     "bounceRate", "averageSessionDuration", "engagementRate"],
        "order_by": "-screenPageViews",
    },
    "user_acquisition": {
        "dimensions": ["sessionDefaultChannelGroup", "sessionSource", "sessionMedium"],
        "metrics": ["sessions", "totalUsers", "newUsers",
                     "bounceRate", "engagementRate", "conversions"],
        "order_by": "-sessions",
    },
    "device_breakdown": {
        "dimensions": ["deviceCategory", "operatingSystem", "browser"],
        "metrics": ["sessions", "totalUsers", "bounceRate",
                     "averageSessionDuration", "engagementRate"],
        "order_by": "-sessions",
    },
    "geo_distribution": {
        "dimensions": ["country", "city"],
        "metrics": ["sessions", "totalUsers", "bounceRate", "engagementRate"],
        "order_by": "-sessions",
    },
    "landing_pages": {
        "dimensions": ["landingPage"],
        "metrics": ["sessions", "totalUsers", "bounceRate",
                     "averageSessionDuration", "engagementRate", "conversions"],
        "order_by": "-sessions",
    },
    "user_behavior": {
        "dimensions": ["pagePath"],
        "metrics": ["screenPageViews", "engagedSessions", "engagementRate",
                     "averageSessionDuration", "eventCount"],
        "order_by": "-screenPageViews",
    },
    "conversion_events": {
        "dimensions": ["eventName", "date"],
        "metrics": ["eventCount", "totalUsers", "conversions"],
        "order_by": "-eventCount",
    },
    # ── User Persona Presets ──────────────────────────────────
    "demographics_age": {
        "dimensions": ["userAgeBracket"],
        "metrics": ["totalUsers", "sessions", "bounceRate",
                     "engagementRate", "averageSessionDuration", "conversions"],
        "order_by": "-totalUsers",
    },
    "demographics_gender": {
        "dimensions": ["userGender"],
        "metrics": ["totalUsers", "sessions", "bounceRate",
                     "engagementRate", "averageSessionDuration", "conversions"],
        "order_by": "-totalUsers",
    },
    "demographics_geo": {
        "dimensions": ["country", "city"],
        "metrics": ["totalUsers", "sessions", "bounceRate",
                     "engagementRate", "conversions"],
        "order_by": "-totalUsers",
    },
    "demographics_language": {
        "dimensions": ["language"],
        "metrics": ["totalUsers", "sessions", "bounceRate",
                     "engagementRate"],
        "order_by": "-totalUsers",
    },
    "demographics_interests": {
        "dimensions": ["brandingInterest"],
        "metrics": ["totalUsers", "sessions", "bounceRate",
                     "engagementRate", "conversions"],
        "order_by": "-totalUsers",
    },
    "new_vs_returning": {
        "dimensions": ["newVsReturning"],
        "metrics": ["totalUsers", "sessions", "sessionsPerUser",
                     "bounceRate", "engagementRate", "averageSessionDuration",
                     "screenPageViewsPerSession", "conversions"],
        "order_by": "-totalUsers",
    },
}


def build_client():
    return BetaAnalyticsDataClient()


def build_order_by(field_name, dimension_names):
    descending = field_name.startswith("-")
    name = field_name.lstrip("-")
    if name in dimension_names:
        return OrderBy(
            dimension=OrderBy.DimensionOrderBy(dimension_name=name),
            desc=descending,
        )
    return OrderBy(
        metric=OrderBy.MetricOrderBy(metric_name=name),
        desc=descending,
    )


def run_report(client, property_id, dimensions, metrics, start_date, end_date,
               limit=1000, order_by_field=None):
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=limit,
    )
    if order_by_field:
        request.order_bys = [build_order_by(order_by_field, dimensions)]

    return client.run_report(request)


def response_to_dict(response):
    dim_headers = [h.name for h in response.dimension_headers]
    metric_headers = [h.name for h in response.metric_headers]
    metric_types = [MetricType(h.type_).name for h in response.metric_headers]

    rows = []
    for row in response.rows:
        row_data = {}
        for i, dv in enumerate(row.dimension_values):
            row_data[dim_headers[i]] = dv.value
        for i, mv in enumerate(row.metric_values):
            val = mv.value
            if metric_types[i] in ("TYPE_INTEGER", "TYPE_FLOAT", "TYPE_SECONDS", "TYPE_CURRENCY"):
                try:
                    val = float(val)
                    if val == int(val):
                        val = int(val)
                except ValueError:
                    pass
            row_data[metric_headers[i]] = val
        rows.append(row_data)

    return {
        "row_count": response.row_count,
        "dimensions": dim_headers,
        "metrics": metric_headers,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser(description="GA4 Data API query tool")
    parser.add_argument("--property-id", default=os.environ.get("GA4_PROPERTY_ID"),
                        help="GA4 property ID (or set GA4_PROPERTY_ID env)")
    parser.add_argument("--preset", choices=list(PRESETS.keys()),
                        help="Use a predefined query template")
    parser.add_argument("--dimensions", help="Comma-separated dimension names")
    parser.add_argument("--metrics", help="Comma-separated metric names")
    parser.add_argument("--start-date", default="28daysAgo")
    parser.add_argument("--end-date", default="yesterday")
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--order-by",
                        help='Metric to order by (prefix with - for desc; quote in shell: --order-by="-sessions")')
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    if not args.property_id:
        print("Error: --property-id required or set GA4_PROPERTY_ID", file=sys.stderr)
        sys.exit(1)

    if args.preset:
        preset = PRESETS[args.preset]
        dimensions = preset["dimensions"]
        metrics = preset["metrics"]
        order_by = args.order_by or preset.get("order_by")
    elif args.dimensions and args.metrics:
        dimensions = [d.strip() for d in args.dimensions.split(",")]
        metrics = [m.strip() for m in args.metrics.split(",")]
        order_by = args.order_by
    else:
        print("Error: provide --preset or both --dimensions and --metrics", file=sys.stderr)
        sys.exit(1)

    client = build_client()
    response = run_report(
        client, args.property_id, dimensions, metrics,
        args.start_date, args.end_date, args.limit, order_by
    )

    result = response_to_dict(response)
    result["query"] = {
        "property_id": args.property_id,
        "preset": args.preset,
        "date_range": {"start": args.start_date, "end": args.end_date},
        "dimensions": dimensions,
        "metrics": metrics,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
