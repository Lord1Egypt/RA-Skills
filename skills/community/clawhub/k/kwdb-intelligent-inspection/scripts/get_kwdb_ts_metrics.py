#!/usr/bin/env python3
"""
KaiwuDB Time Series Metrics Processor

Process and extract inspection-relevant metrics from KaiwuDB's /ts/query API response.
The API returns a large JSON object with many metrics; this script filters and formats
only the metrics needed for inspection per references/report-template.md.

Usage:
    python3 get_kwdb_ts_metrics.py [--host HOST] [--port PORT] [--start TIME] [--end TIME]
                                    [--sample INTERVAL] [--metric NAME] [--json]

Options:
    --host           KaiwuDB admin host (default: localhost)
    --port           KaiwuDB admin port (default: 8080)
    --start          Start time (ISO format or unix timestamp in ns, default: 1 hour ago)
    --end            End time (ISO format or unix timestamp in ns, default: now)
    --sample         Sample interval in seconds (default: 60)
    --metric         Filter by specific metric name (e.g., sys.cpu.user.percent)
    --json           Output raw JSON data
"""

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class MetricMeta:
    """Display metadata for a time series metric."""
    display_name: str
    unit: str


@dataclass
class QueryParams:
    """Query parameters for /ts/query API."""
    downsampler: int
    source_aggregator: int
    derivative: int


@dataclass
class MetricInfo:
    """Complete metric definition: display metadata + query parameters."""
    display: MetricMeta
    query: QueryParams


# Metrics mapping: full metric name -> MetricInfo(display + query params)
#
# Query Enum Values:
#   Downsampler/SourceAggregator: 1=AVG, 2=SUM, 3=MAX, 4=MIN, 5=FIRST, 6=LAST, 7=VARIANCE
#   Derivative: 0=NONE, 1=DERIVATIVE, 2=NON_NEGATIVE_DERIVATIVE
#
# Query param conventions:
#   SUM metrics (cluster totals):     d:1, sa:2, der:0
#   AVG metrics (per-node average):   d:1, sa:1, der:0
#   MAX metrics (worst-case):         d:1, sa:3, der:0

Q_SUM = QueryParams(downsampler=1, source_aggregator=2, derivative=0)
Q_AVG = QueryParams(downsampler=1, source_aggregator=1, derivative=0)
Q_MAX = QueryParams(downsampler=1, source_aggregator=3, derivative=0)

METRICS_MAP: dict[str, MetricInfo] = {
    # Basic Indicators
    "cr.node.liveness.livenodes": MetricInfo(MetricMeta("Live Nodes", "nodes"), Q_AVG),
    "cr.node.sys.uptime": MetricInfo(MetricMeta("Uptime", "seconds"), Q_AVG),
    # System Resources
    "cr.node.sys.cpu.user.percent": MetricInfo(MetricMeta("CPU User", "%"), Q_SUM),
    "cr.node.sys.cpu.sys.percent": MetricInfo(MetricMeta("CPU Sys", "%"), Q_SUM),
    "cr.node.sys.cpu.combined.percent-normalized": MetricInfo(MetricMeta("CPU Combined", "%"), Q_SUM),
    "cr.store.capacity": MetricInfo(MetricMeta("Disk Total", "bytes"), Q_SUM),
    "cr.store.capacity.available": MetricInfo(MetricMeta("Disk Available", "bytes"), Q_SUM),
    "cr.store.capacity.used": MetricInfo(MetricMeta("Disk Used", "bytes"), Q_SUM),
    "cr.node.sys.rss": MetricInfo(MetricMeta("Memory RSS", "bytes"), Q_SUM),
    "cr.node.sys.go.allocbytes": MetricInfo(MetricMeta("Go Alloc", "bytes"), Q_SUM),
    "cr.node.sys.go.totalbytes": MetricInfo(MetricMeta("Go Total", "bytes"), Q_SUM),
    # Database Performance
    "cr.node.sql.insert.count": MetricInfo(MetricMeta("SQL Insert Count", "count"), Q_SUM),
    "cr.node.sql.update.count": MetricInfo(MetricMeta("SQL Update Count", "count"), Q_SUM),
    "cr.node.sql.delete.count": MetricInfo(MetricMeta("SQL Delete Count", "count"), Q_SUM),
    "cr.node.sql.select.count": MetricInfo(MetricMeta("SQL Select Count", "count"), Q_SUM),
    "cr.node.sql.query.count": MetricInfo(MetricMeta("SQL Query Count", "count"), Q_SUM),
    "cr.store.rebalancing.writespersecond": MetricInfo(MetricMeta("Rebalancing Writes/s", "ops/s"), Q_SUM),
    "cr.store.rebalancing.queriespersecond": MetricInfo(MetricMeta("Rebalancing Queries/s", "ops/s"), Q_SUM),
    "cr.node.exec.latency-p99": MetricInfo(MetricMeta("SQL Exec Latency", "ns"), Q_AVG),
    "cr.node.sql.service.latency-p99": MetricInfo(MetricMeta("SQL Service Latency", "ns"), Q_AVG),
    "cr.node.sql.distsql.exec.latency-p99": MetricInfo(MetricMeta("DistSQL Exec Latency", "ns"), Q_AVG),
    # Storage
    "cr.store.totalbytes": MetricInfo(MetricMeta("Total Bytes", "bytes"), Q_SUM),
    "cr.store.livebytes": MetricInfo(MetricMeta("Live Bytes", "bytes"), Q_SUM),
    # Cluster
    "cr.store.replicas": MetricInfo(MetricMeta("Replicas", "count"), Q_SUM),
    "cr.store.replicas.leaders": MetricInfo(MetricMeta("Raft Leaders", "count"), Q_SUM),
    "cr.store.replicas.leaseholders": MetricInfo(MetricMeta("Lease Holders", "count"), Q_SUM),
    "cr.store.ranges.unavailable": MetricInfo(MetricMeta("Unavailable Ranges", "count"), Q_MAX),
    "cr.store.ranges.underreplicated": MetricInfo(MetricMeta("Under-replicated Ranges", "count"), Q_MAX),
    "cr.store.ranges.overreplicated": MetricInfo(MetricMeta("Over-replicated Ranges", "count"), Q_MAX),
    "cr.store.raftlog.behind": MetricInfo(MetricMeta("Raftlog Behind", "count"), Q_MAX),
    "cr.store.raft.replica.consistent.latency-p99": MetricInfo(MetricMeta("Raft Consistent Latency", "ns"), Q_AVG),
    # Network
    "cr.node.clock-offset.meannanos": MetricInfo(MetricMeta("Clock Offset Mean", "ns"), Q_MAX),
}


def build_ts_query(host: str, port: int, start_ns: int, end_ns: int, sample_ns: int,
                   metric_filter: list[str] | None = None) -> dict:
    """Build and execute /ts/query API request."""

    queries = []
    metrics_to_query = metric_filter if metric_filter else list(METRICS_MAP.keys())

    for name in metrics_to_query:
        info = METRICS_MAP[name]  # Validated in main() before this call
        queries.append({
            "name": name,
            "downsampler": info.query.downsampler,
            "source_aggregator": info.query.source_aggregator,
            "derivative": info.query.derivative,
        })

    payload = {
        "start_nanos": start_ns,
        "end_nanos": end_ns,
        "sample_nanos": sample_ns,
        "queries": queries
    }

    curl_cmd = [
        "curl", "-s", "--insecure", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
        f"http://{host}:{port}/ts/query"
    ]

    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        print("Error: Connection to KaiwuDB timed out (30s)", file=sys.stderr)
        sys.exit(1)
    if result.returncode != 0:
        print(f"Error: Failed to fetch metrics: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def parse_metrics(data: dict) -> list[dict[str, Any]]:
    """Parse /ts/query response and extract latest values for each metric."""
    results = []

    for r in data.get("results", []):
        full_name = r.get("query", {}).get("name", "")
        sources = r.get("query", {}).get("sources", [])
        datapoints = r.get("datapoints", [])
        info = METRICS_MAP.get(full_name, MetricInfo(MetricMeta(full_name, ""), Q_SUM))

        result = {
            "name": full_name,
            "display_name": info.display.display_name,
            "unit": info.display.unit,
            "sources": sources,
        }

        if datapoints:
            latest = datapoints[-1]
            result.update({
                # TODO: display datapoints_count to show data completeness (e.g., expected 720 pts vs actual 713 pts)
                "datapoints_count": len(datapoints),
                # TODO: display timestamp to show when latest value was collected
                "timestamp": int(latest.get("timestampNanos", 0)) // 1_000_000,
                "latest_value": latest.get("value", 0),
                "min": min(dp.get("value", 0) for dp in datapoints),
                "max": max(dp.get("value", 0) for dp in datapoints),
                "avg": sum(dp.get("value", 0) for dp in datapoints) / len(datapoints),
            })
        else:
            result.update({
                # TODO: display datapoints_count to show data completeness
                "datapoints_count": 0,
                # TODO: display timestamp to show when latest value was collected
                "timestamp": None,
                "latest_value": None,
                "min": None,
                "max": None,
                "avg": None,
            })

        results.append(result)

    return results


def format_metrics_table(metrics: list[dict]) -> str:
    """Format metrics as a table."""
    if not metrics:
        return "No metrics data available."

    # Unit formatters: unit_name -> (formatter_fn, suffix_or_none)
    # suffix_or_none: if not None, append to formatted value (e.g., "ms", "%")
    UNIT_FORMATTERS = {
        "bytes": (format_bytes, None),
        "%": (lambda v: f"{v:.4f}", "%"),
        "ms": (lambda v: f"{v:.3f}", "ms"),
        "ns": (lambda v: f"{v/1_000_000:.3f}", "ms"),  # nanoseconds -> milliseconds
        "seconds": (format_duration, None),
        "count": (lambda v: str(int(v)), None),
        "nodes": (lambda v: str(int(v)), None),
        "ops/s": (lambda v: f"{v:.2f}", "/s"),
    }

    def format_value(value, unit, col_width=18):
        if value is None:
            return "NAN"
        if unit not in UNIT_FORMATTERS:
            s = str(value)
        else:
            formatter, suffix = UNIT_FORMATTERS[unit]
            s = f"{formatter(value)}{suffix}" if suffix else formatter(value)
        # Truncate only if exceeds column width
        if len(s) > col_width:
            return s[:col_width-3] + "..."
        return s

    # Determine column widths
    name_width = max(len(m["display_name"]) for m in metrics) + 2
    val_width = 18
    min_width = 15
    max_width = 15
    avg_width = 15

    lines = []
    header = (f"{'Metric':<{name_width}}"
              f"{'Latest':>{val_width}}"
              f"{'Min':>{min_width}}"
              f"{'Max':>{max_width}}"
              f"{'Avg':>{avg_width}}"
              f"  Sources")
    lines.append(header)
    lines.append("-" * len(header))

    for m in sorted(metrics, key=lambda x: x["display_name"]):
        value_str = format_value(m["latest_value"], m["unit"], val_width)
        min_str = format_value(m["min"], m["unit"], min_width)
        max_str = format_value(m["max"], m["unit"], max_width)
        avg_str = format_value(m["avg"], m["unit"], avg_width)

        lines.append(
            f"{m['display_name']:<{name_width}}"
            f"{value_str:>{val_width}}"
            f"{min_str:>{min_width}}"
            f"{max_str:>{max_width}}"
            f"{avg_str:>{avg_width}}"
            f"  {','.join(m['sources']) if m['sources'] else 'N/A'}"
        )

    return "\n".join(lines)


def format_bytes(num: float) -> str:
    """Format bytes as human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num) < 1024.0:
            return f"{num:.2f}{unit}"
        num /= 1024.0
    return f"{num:.2f}PB"


def _parse_iso_to_ns(iso_str: str) -> float:
    """Parse ISO 8601 datetime string to unix timestamp in nanoseconds."""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp() * 1_000_000_000


def format_duration(seconds: float) -> str:
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    elif seconds < 86400:
        return f"{seconds/3600:.1f}h"
    else:
        return f"{seconds/86400:.1f}d"


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and process time series metrics from KaiwuDB"
    )
    parser.add_argument("--host", default="localhost", help="KaiwuDB admin host")
    parser.add_argument("--port", type=int, default=8080, help="KaiwuDB admin port")
    parser.add_argument("--start", help="Start time (ISO 8601 format or unix timestamp in ns). Examples: '2026-04-28T10:00:00', '2026-04-28T10:00:00Z', '1745846400000000000'")
    parser.add_argument("--end", help="End time (ISO 8601 format or unix timestamp in ns). Examples: '2026-04-28T11:00:00', '2026-04-28T11:00:00Z', '1745850000000000000'")
    parser.add_argument("--sample", type=int, default=60, help="Sample interval in seconds")
    parser.add_argument("--metric", action="append", help="Filter by metric name (can repeat)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    # Validate metric filter
    if args.metric:
        for m in args.metric:
            if m not in METRICS_MAP:
                print(f"Error: Unknown metric: {m}", file=sys.stderr)
                sys.exit(1)

    # Calculate time range
    now_ns = int(time.time_ns())  # Use time_ns() for integer precision
    hour_ns = 3600 * 1_000_000_000

    if args.start:
        try:
            start_ns = int(args.start)
        except ValueError:
            try:
                start_ns = int(_parse_iso_to_ns(args.start))
            except ValueError as e:
                print(f"Error: Invalid --start format: {args.start}. Use ISO 8601 (e.g., '2026-04-28T10:00:00') or unix timestamp in ns", file=sys.stderr)
                sys.exit(1)
    else:
        start_ns = now_ns - hour_ns

    if args.end:
        try:
            end_ns = int(args.end)
        except ValueError:
            try:
                end_ns = int(_parse_iso_to_ns(args.end))
            except ValueError as e:
                print(f"Error: Invalid --end format: {args.end}. Use ISO 8601 (e.g., '2026-04-28T10:00:00') or unix timestamp in ns", file=sys.stderr)
                sys.exit(1)
    else:
        end_ns = now_ns

    sample_ns = args.sample * 1_000_000_000

    data = build_ts_query(args.host, args.port, start_ns, end_ns, sample_ns,
                          args.metric)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    metrics = parse_metrics(data)

    print(f"KaiwuDB Time Series Metrics")
    print(f"{'='*80}")
    print(f"Host: {args.host}:{args.port}")
    print(f"Time Range: {start_ns} - {end_ns} ({args.sample}s intervals)")
    print(f"Metrics Retrieved: {len(metrics)}")
    print()
    print(format_metrics_table(metrics))


if __name__ == "__main__":
    main()
