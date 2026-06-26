#!/usr/bin/env python3
"""
Meta Marketing API — Campaign Insights Exporter

Exports campaign, ad set, and ad-level performance data from your Meta ad account
using the official Marketing API Insights endpoint.

Requirements:
    pip install requests

Usage:
    python meta_campaign_insights.py --access-token YOUR_TOKEN --account-id act_123456789

    # Export last 30 days at campaign level to CSV
    python meta_campaign_insights.py -t YOUR_TOKEN -a act_123456789 --date-preset last_30d --level campaign -o campaigns.csv

    # Export specific date range at ad level with daily breakdown
    python meta_campaign_insights.py -t YOUR_TOKEN -a act_123456789 --since 2025-01-01 --until 2025-01-31 --level ad --time-increment 1 -o daily_ads.csv

    # Export with breakdowns by age and gender
    python meta_campaign_insights.py -t YOUR_TOKEN -a act_123456789 --level adset --breakdowns age,gender -o demo_breakdown.csv

    # Export with custom fields
    python meta_campaign_insights.py -t YOUR_TOKEN -a act_123456789 --fields impressions,clicks,spend,cpc,cpm,ctr,reach,frequency,actions,cost_per_action_type -o custom.csv

Reference:
    https://developers.facebook.com/docs/marketing-api/insights
    https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime

import requests

API_VERSION = "v25.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Most useful fields for campaign performance analysis
DEFAULT_FIELDS = [
    "campaign_id",
    "campaign_name",
    "adset_id",
    "adset_name",
    "ad_id",
    "ad_name",
    "objective",
    "optimization_goal",
    "impressions",
    "reach",
    "frequency",
    "clicks",
    "cpc",
    "cpm",
    "ctr",
    "spend",
    "actions",
    "cost_per_action_type",
    "conversions",
    "cost_per_conversion",
    "purchase_roas",
    "website_purchase_roas",
]

VALID_LEVELS = ["account", "campaign", "adset", "ad"]

VALID_DATE_PRESETS = [
    "today",
    "yesterday",
    "this_month",
    "last_month",
    "this_quarter",
    "maximum",
    "last_3d",
    "last_7d",
    "last_14d",
    "last_28d",
    "last_30d",
    "last_90d",
    "last_week_mon_sun",
    "last_week_sun_sat",
    "last_quarter",
    "last_year",
    "this_week_mon_today",
    "this_week_sun_today",
    "this_year",
]

VALID_BREAKDOWNS = [
    "age",
    "gender",
    "country",
    "region",
    "dma",
    "publisher_platform",
    "platform_position",
    "device_platform",
    "impression_device",
    "ad_format_asset",
    "body_asset",
    "image_asset",
    "video_asset",
    "title_asset",
    "description_asset",
    "link_url_asset",
    "product_id",
    "hourly_stats_aggregated_by_advertiser_time_zone",
    "hourly_stats_aggregated_by_audience_time_zone",
]


def fetch_insights(access_token, account_id, params):
    """Fetch insights from the Marketing API with pagination support."""
    url = f"{BASE_URL}/{account_id}/insights"
    params["access_token"] = access_token
    params["limit"] = params.get("limit", 500)

    all_data = []
    page = 0

    while url:
        page += 1
        try:
            response = requests.get(url, params=params if page == 1 else None)
            result = response.json()
        except Exception as e:
            print(f"\nError fetching data: {e}", file=sys.stderr)
            break

        if "error" in result:
            error = result["error"]
            error_code = error.get("code", "unknown")
            error_msg = error.get("message", "Unknown error")

            # Handle rate limiting
            if error_code == 613 or error_code == 17:
                print(
                    f"\nRate limited. Waiting 60 seconds before retrying...",
                    file=sys.stderr,
                )
                time.sleep(60)
                continue

            print(
                f"\nAPI Error (code {error_code}): {error_msg}",
                file=sys.stderr,
            )
            if error_code == 190:
                print(
                    "Your access token is invalid or expired. Generate a new one at:",
                    file=sys.stderr,
                )
                print(
                    "https://developers.facebook.com/tools/accesstoken/",
                    file=sys.stderr,
                )
            elif error_code == 200:
                print(
                    "Permission error. Ensure your token has ads_read permission.",
                    file=sys.stderr,
                )
            elif error_code == 3018:
                print(
                    "Date range too far back. Maximum is 37 months from today.",
                    file=sys.stderr,
                )
            break

        data = result.get("data", [])
        all_data.extend(data)
        print(f"\r  Fetched {len(all_data)} rows (page {page})...", end="", flush=True)

        # Handle pagination
        paging = result.get("paging", {})
        url = paging.get("next")
        # After first request, params are in the next URL
        params = None

    print()
    return all_data


def flatten_actions(row):
    """Flatten action-type fields into individual columns."""
    flat = {}
    for key, value in row.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            # This is an actions-type field (list of {action_type, value, ...})
            for action in value:
                action_type = action.get("action_type", "unknown")
                action_value = action.get("value", "")
                col_name = f"{key}:{action_type}"
                flat[col_name] = action_value
        elif isinstance(value, dict):
            # Nested dict — serialize to JSON
            flat[key] = json.dumps(value)
        else:
            flat[key] = value
    return flat


def export_to_csv(data, output_file, flatten=True):
    """Export insights data to CSV."""
    if not data:
        print("No data to export.", file=sys.stderr)
        return

    # Flatten action fields
    if flatten:
        data = [flatten_actions(row) for row in data]

    # Collect all unique column names
    all_columns = []
    seen = set()
    for row in data:
        for key in row.keys():
            if key not in seen:
                all_columns.append(key)
                seen.add(key)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Exported {len(data)} rows to {output_file}")


def export_to_json(data, output_file):
    """Export insights data to JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(data)} rows to {output_file}")


def print_summary(data):
    """Print a quick summary of the exported data."""
    if not data:
        return

    total_spend = sum(float(row.get("spend", 0)) for row in data)
    total_impressions = sum(int(row.get("impressions", 0)) for row in data)
    total_clicks = sum(int(row.get("clicks", 0)) for row in data)
    total_reach = sum(int(row.get("reach", 0)) for row in data)

    print("\n--- Quick Summary ---")
    print(f"  Total rows:        {len(data)}")
    print(f"  Total spend:       {total_spend:,.2f}")
    print(f"  Total impressions: {total_impressions:,}")
    print(f"  Total clicks:      {total_clicks:,}")
    print(f"  Total reach:       {total_reach:,}")
    if total_impressions > 0:
        print(f"  Overall CTR:       {(total_clicks / total_impressions * 100):.2f}%")
        print(f"  Overall CPM:       {(total_spend / total_impressions * 1000):.2f}")
    if total_clicks > 0:
        print(f"  Overall CPC:       {(total_spend / total_clicks):.2f}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Export Meta Ads campaign insights to CSV/JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Last 30 days, campaign level
  %(prog)s -t TOKEN -a act_123 --date-preset last_30d --level campaign -o campaigns.csv

  # Custom date range, daily breakdown, ad level
  %(prog)s -t TOKEN -a act_123 --since 2025-01-01 --until 2025-01-31 --level ad --time-increment 1 -o daily.csv

  # With demographic breakdowns
  %(prog)s -t TOKEN -a act_123 --level adset --breakdowns age,gender -o demo.csv

  # JSON output
  %(prog)s -t TOKEN -a act_123 --format json -o data.json

Get your access token at: https://developers.facebook.com/tools/accesstoken/
Docs: https://developers.facebook.com/docs/marketing-api/insights
        """,
    )
    parser.add_argument(
        "-t",
        "--access-token",
        required=True,
        help="Meta Marketing API access token (with ads_read permission)",
    )
    parser.add_argument(
        "-a",
        "--account-id",
        required=True,
        help="Ad account ID (format: act_123456789)",
    )
    parser.add_argument(
        "--level",
        choices=VALID_LEVELS,
        default="campaign",
        help="Aggregation level (default: campaign)",
    )
    parser.add_argument(
        "--fields",
        help=f"Comma-separated fields to retrieve. Default: key performance fields",
    )
    parser.add_argument(
        "--date-preset",
        choices=VALID_DATE_PRESETS,
        help="Predefined date range (e.g., last_7d, last_30d, this_month)",
    )
    parser.add_argument(
        "--since", help="Start date YYYY-MM-DD (use with --until)"
    )
    parser.add_argument(
        "--until", help="End date YYYY-MM-DD (use with --since)"
    )
    parser.add_argument(
        "--time-increment",
        help="Break results into N-day increments (1=daily, 7=weekly) or 'monthly'",
    )
    parser.add_argument(
        "--breakdowns",
        help=f"Comma-separated breakdowns: {', '.join(VALID_BREAKDOWNS[:8])}...",
    )
    parser.add_argument(
        "--filtering",
        help='JSON filtering array, e.g., \'[{"field":"ad.effective_status","operator":"IN","value":["ACTIVE"]}]\'',
    )
    parser.add_argument(
        "--sort",
        help='Sort field with direction, e.g., "spend_descending" or "impressions_ascending"',
    )
    parser.add_argument(
        "--action-attribution-windows",
        help="Attribution windows, e.g., 1d_click,7d_click,1d_view",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="meta_insights_export.csv",
        help="Output file path (default: meta_insights_export.csv)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Skip the summary output",
    )
    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="Don't flatten action fields into separate columns (CSV only)",
    )
    parser.add_argument(
        "--use-unified-attribution",
        action="store_true",
        help="Use ad-set-level attribution settings (matches Ads Manager behavior)",
    )

    args = parser.parse_args()

    # Validate account ID format
    if not args.account_id.startswith("act_"):
        print(
            "Warning: Account ID should start with 'act_'. Prepending it.",
            file=sys.stderr,
        )
        args.account_id = f"act_{args.account_id}"

    # Build fields list
    if args.fields:
        fields = args.fields
    else:
        # Filter default fields based on level
        level_fields = {
            "account": [
                "account_id",
                "account_name",
                "impressions",
                "reach",
                "frequency",
                "clicks",
                "cpc",
                "cpm",
                "ctr",
                "spend",
                "actions",
                "cost_per_action_type",
                "purchase_roas",
            ],
            "campaign": [
                "campaign_id",
                "campaign_name",
                "objective",
                "impressions",
                "reach",
                "frequency",
                "clicks",
                "cpc",
                "cpm",
                "ctr",
                "spend",
                "actions",
                "cost_per_action_type",
                "purchase_roas",
            ],
            "adset": [
                "campaign_name",
                "adset_id",
                "adset_name",
                "optimization_goal",
                "impressions",
                "reach",
                "frequency",
                "clicks",
                "cpc",
                "cpm",
                "ctr",
                "spend",
                "actions",
                "cost_per_action_type",
                "purchase_roas",
            ],
            "ad": [
                "campaign_name",
                "adset_name",
                "ad_id",
                "ad_name",
                "impressions",
                "reach",
                "frequency",
                "clicks",
                "cpc",
                "cpm",
                "ctr",
                "spend",
                "actions",
                "cost_per_action_type",
                "purchase_roas",
            ],
        }
        fields = ",".join(level_fields.get(args.level, DEFAULT_FIELDS))

    # Build API params
    params = {
        "fields": fields,
        "level": args.level,
    }

    # Date range
    if args.since and args.until:
        params["time_range"] = json.dumps(
            {"since": args.since, "until": args.until}
        )
    elif args.date_preset:
        params["date_preset"] = args.date_preset
    else:
        params["date_preset"] = "last_30d"

    # Optional params
    if args.time_increment:
        params["time_increment"] = args.time_increment

    if args.breakdowns:
        params["breakdowns"] = args.breakdowns

    if args.filtering:
        params["filtering"] = args.filtering

    if args.sort:
        params["sort"] = json.dumps([args.sort])

    if args.action_attribution_windows:
        params["action_attribution_windows"] = json.dumps(
            args.action_attribution_windows.split(",")
        )

    if args.use_unified_attribution:
        params["use_unified_attribution_setting"] = "true"

    # Log what we're doing
    print(f"Meta Campaign Insights Export")
    print(f"  Account:    {args.account_id}")
    print(f"  Level:      {args.level}")
    print(f"  Date range: {args.date_preset or f'{args.since} to {args.until}'}")
    if args.breakdowns:
        print(f"  Breakdowns: {args.breakdowns}")
    if args.time_increment:
        print(f"  Increment:  {args.time_increment}")
    print(f"  Output:     {args.output} ({args.format})")
    print()

    # Fetch data
    print("Fetching insights from Meta API...")
    data = fetch_insights(args.access_token, args.account_id, params)

    if not data:
        print("No data returned. Check your account ID, date range, and permissions.")
        sys.exit(1)

    # Export
    if args.format == "json":
        export_to_json(data, args.output)
    else:
        export_to_csv(data, args.output, flatten=not args.no_flatten)

    # Summary
    if not args.no_summary:
        print_summary(data)


if __name__ == "__main__":
    main()
