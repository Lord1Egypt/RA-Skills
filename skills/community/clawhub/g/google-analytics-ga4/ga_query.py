#!/usr/bin/env python3
"""
Google Analytics Data API v1 CLI — realtime, historical, and metadata reports.
"""

import argparse
import json
import os
import sys
from typing import List, Optional, Dict, Any

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
        RunRealtimeReportRequest,
        MinuteRange,
        MetadataRequest,
    )
except ImportError:
    print("Error: install google-analytics-data")
    print("  pip install google-analytics-data")
    sys.exit(1)


class GoogleAnalyticsQuery:
    """Thin wrapper around BetaAnalyticsDataClient."""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Args:
            credentials_path: Path to the service account JSON key (optional if ADC is set).
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        self.client = BetaAnalyticsDataClient()

    def list_properties(self) -> List[Dict[str, str]]:
        """
        The Data API does not list properties; return guidance for locating a GA4 property ID.
        """
        return [{
            "note": "Property listing is not available via the Data API alone.",
            "instruction": "In GA4: Admin > Property settings — copy the numeric Property ID.",
            "format": "Property ID is numeric only, e.g. 123456789",
        }]

    def get_metadata(self, property_id: str) -> Dict[str, Any]:
        """
        Args:
            property_id: Numeric GA4 property ID.

        Returns:
            Dict of dimensions and metrics metadata.
        """
        request = MetadataRequest(property=f"properties/{property_id}")
        response = self.client.get_metadata(request)
        
        dimensions = []
        for dim in response.dimensions:
            dimensions.append({
                "name": dim.api_name,
                "description": dim.description,
                "category": dim.category
            })
        
        metrics = []
        for metric in response.metrics:
            metrics.append({
                "name": metric.api_name,
                "description": metric.description,
                "type": metric.type_.name,
                "category": metric.category
            })
        
        return {
            "dimensions": dimensions,
            "metrics": metrics
        }

    def query_realtime(
        self,
        property_id: str,
        metrics: List[str] = None,
        dimensions: List[str] = None,
        minute_range: str = "0-30"
    ) -> Dict[str, Any]:
        """
        Run a realtime report.
        """
        if metrics is None:
            metrics = ["activeUsers"]
        
        start_minutes, end_minutes = map(int, minute_range.split("-"))
        
        request = RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name=m) for m in metrics],
            dimensions=[Dimension(name=d) for d in dimensions] if dimensions else [],
            minute_ranges=[MinuteRange(
                start_minutes_ago=start_minutes,
                end_minutes_ago=end_minutes
            )]
        )
        
        response = self.client.run_realtime_report(request)
        
        result = self._parse_response(response, is_realtime=True)
        result["query_type"] = "realtime"
        result["minute_range"] = f"{start_minutes}-{end_minutes} minutes ago"
        
        return result

    def query_historical(
        self,
        property_id: str,
        start_date: str,
        end_date: str,
        metrics: List[str] = None,
        dimensions: List[str] = None,
        limit: int = 10000,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Run a standard (historical) report."""
        if metrics is None:
            metrics = ["activeUsers"]
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[Metric(name=m) for m in metrics],
            dimensions=[Dimension(name=d) for d in dimensions] if dimensions else [],
            limit=limit,
            offset=offset
        )
        
        response = self.client.run_report(request)
        
        result = self._parse_response(response, is_realtime=False)
        result["query_type"] = "historical"
        result["date_range"] = f"{start_date} to {end_date}"
        
        return result

    def _parse_response(self, response, is_realtime: bool = False) -> Dict[str, Any]:
        """Normalize API response rows and totals."""

        # Headers
        dimension_headers = [h.name for h in response.dimension_headers]
        metric_headers = [h.name for h in response.metric_headers]
        
        # Rows
        rows = []
        for row in response.rows:
            row_data = {}
            for i, dim_value in enumerate(row.dimension_values):
                if i < len(dimension_headers):
                    row_data[dimension_headers[i]] = dim_value.value
            for i, metric_value in enumerate(row.metric_values):
                if i < len(metric_headers):
                    row_data[metric_headers[i]] = metric_value.value
            rows.append(row_data)
        
        # Totals
        totals = {}
        if response.totals:
            for total_row in response.totals:
                for i, metric_value in enumerate(total_row.metric_values):
                    if i < len(metric_headers):
                        totals[metric_headers[i]] = metric_value.value
        
        return {
            "success": True,
            "dimension_headers": dimension_headers,
            "metric_headers": metric_headers,
            "rows": rows,
            "row_count": response.row_count,
            "totals": totals,
            "metadata": {
                "currency_code": getattr(response.metadata, 'currency_code', None) if response.metadata else None,
                "time_zone": getattr(response.metadata, 'time_zone', None) if response.metadata else None
            }
        }


def format_as_markdown_table(result: Dict[str, Any]) -> str:
    """Render a result dict as a Markdown table."""
    if not result.get("success"):
        return "❌ Query failed"
    
    lines = []
    
    query_type = result.get("query_type", "unknown")
    if query_type == "realtime":
        lines.append(f"### 📊 Realtime ({result.get('minute_range', '')})")
    elif query_type == "historical":
        lines.append(f"### 📈 Historical ({result.get('date_range', '')})")
    
    lines.append("")
    
    if result.get("totals"):
        lines.append("**Totals:**")
        for metric, value in result["totals"].items():
            lines.append(f"- {metric}: {value}")
        lines.append("")
    
    rows = result.get("rows", [])
    if not rows:
        lines.append("⚠️ No rows")
        return "\n".join(lines)

    headers = result.get("dimension_headers", []) + result.get("metric_headers", [])
    if not headers:
        lines.append("⚠️ No columns returned")
        return "\n".join(lines)
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    for row in rows[:50]:
        values = [str(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(values) + " |")
    
    if len(rows) > 50:
        lines.append(f"\n*... {len(rows) - 50} more rows*")
    
    lines.append(f"\n*{result.get('row_count', 0)} rows total*")
    
    return "\n".join(lines)


def format_metadata(metadata: Dict[str, Any]) -> str:
    """Pretty-print metadata for CLI markdown output."""
    lines = ["### 📋 Available dimensions and metrics\n"]

    lines.append("**Dimensions:**")
    dimensions = metadata.get("dimensions", [])[:30]
    for dim in dimensions:
        lines.append(f"- `{dim['name']}` - {dim['description'][:80]}...")
    if len(metadata.get("dimensions", [])) > 30:
        lines.append(f"\n*... {len(metadata['dimensions'])} dimensions total*")
    
    lines.append("")
    
    lines.append("**Metrics:**")
    metrics = metadata.get("metrics", [])[:30]
    for metric in metrics:
        lines.append(f"- `{metric['name']}` ({metric['type']}) - {metric['description'][:80]}...")
    if len(metadata.get("metrics", [])) > 30:
        lines.append(f"\n*... {len(metadata['metrics'])} metrics total*")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Google Analytics Data API CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ga_query.py --action realtime --property-id 123456789

  python ga_query.py --action historical \\
    --property-id 123456789 \\
    --start-date 7daysAgo \\
    --end-date yesterday \\
    --metrics activeUsers,sessions \\
    --dimensions country

  python ga_query.py --action metadata --property-id 123456789
        """,
    )
    
    parser.add_argument(
        "--action",
        choices=["realtime", "historical", "metadata", "list-properties"],
        required=True,
        help="Action to run",
    )
    
    parser.add_argument(
        "--property-id",
        help="Numeric GA4 property ID",
    )
    
    parser.add_argument(
        "--credentials",
        default="ga-credentials.json",
        help="Service account JSON path (default: ga-credentials.json)",
    )

    parser.add_argument(
        "--metrics",
        default="activeUsers",
        help="Comma-separated metrics (default: activeUsers)",
    )
    
    parser.add_argument(
        "--dimensions",
        help="Comma-separated dimensions",
    )
    
    parser.add_argument(
        "--minute-range",
        default="0-30",
        help="Realtime window: start-end minutes ago (default: 0-30)",
    )

    parser.add_argument(
        "--start-date",
        help="Historical start date (YYYY-MM-DD or relative)",
    )
    
    parser.add_argument(
        "--end-date",
        help="Historical end date",
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="Row limit (default: 10000)",
    )
    
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Row offset (default: 0)",
    )
    
    parser.add_argument(
        "--output",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    
    args = parser.parse_args()
    
    if args.action != "list-properties" and not args.property_id:
        print("Error: --property-id is required for this action")
        sys.exit(1)
    
    if args.action == "historical":
        if not args.start_date or not args.end_date:
            print("Error: --start-date and --end-date are required for historical reports")
            sys.exit(1)

    credentials_path = args.credentials
    if not os.path.isabs(credentials_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(script_dir, credentials_path)
        if os.path.exists(local_path):
            credentials_path = local_path
    
    if not os.path.exists(credentials_path) and not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(f"⚠️  Credentials file not found: {credentials_path}")
        print("Set GOOGLE_APPLICATION_CREDENTIALS or place ga-credentials.json next to this script.")
        print("")
    
    try:
        ga = GoogleAnalyticsQuery(credentials_path if os.path.exists(credentials_path) else None)
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        sys.exit(1)

    try:
        if args.action == "list-properties":
            result = ga.list_properties()
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif args.action == "metadata":
            metadata = ga.get_metadata(args.property_id)
            if args.output == "json":
                print(json.dumps(metadata, indent=2, ensure_ascii=False))
            else:
                print(format_metadata(metadata))
                
        elif args.action == "realtime":
            metrics = [m.strip() for m in args.metrics.split(",")]
            dimensions = [d.strip() for d in args.dimensions.split(",")] if args.dimensions else None
            
            result = ga.query_realtime(
                property_id=args.property_id,
                metrics=metrics,
                dimensions=dimensions,
                minute_range=args.minute_range
            )
            
            if args.output == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_as_markdown_table(result))
                
        elif args.action == "historical":
            metrics = [m.strip() for m in args.metrics.split(",")]
            dimensions = [d.strip() for d in args.dimensions.split(",")] if args.dimensions else None
            
            result = ga.query_historical(
                property_id=args.property_id,
                start_date=args.start_date,
                end_date=args.end_date,
                metrics=metrics,
                dimensions=dimensions,
                limit=args.limit,
                offset=args.offset
            )
            
            if args.output == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(format_as_markdown_table(result))
    
    except Exception as e:
        print(f"❌ Query failed: {e}")
        if os.environ.get("DEBUG"):
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
