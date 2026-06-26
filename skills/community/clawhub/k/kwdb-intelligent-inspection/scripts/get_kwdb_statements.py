#!/usr/bin/env python3
"""
KaiwuDB Statements API Client

Fetch and parse SQL statement statistics from KaiwuDB's /_status/statements API.
This API returns aggregated statement statistics collected over a time window
controlled by the cluster setting 'sql.stats.aggregation.interval' (default: 1 hour).

Usage:
    python3 get_kwdb_statements.py [--host HOST] [--port PORT] [--limit N] [--min-latency-ms MS]

Options:
    --host           KaiwuDB admin host (default: localhost)
    --port           KaiwuDB admin port (default: 8080)
    --limit N        Limit output to top N slowest statements (default: 10)
    --min-latency-ms Minimum service latency in ms to filter (default: 0, show all)
    --sort-by        Sort by: service_lat, run_lat, plan_lat, count (default: service_lat)
    --json           Output raw JSON data
"""

import argparse
import json
import subprocess
import sys
from typing import Any


def fetch_statements(host: str, port: int) -> dict:
    """Fetch statements from KaiwuDB _status/statements API."""
    curl_cmd = [
        "curl",
        "-s",
        "--insecure",
        f"http://{host}:{port}/_status/statements"
    ]
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: Failed to fetch statements: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def parse_statements(data: dict) -> list[dict[str, Any]]:
    """Parse and flatten statement data for easier processing."""
    statements = []
    for item in data.get("statements", []):
        key = item.get("key", {})
        stats = item.get("stats", {})

        stmt = {
            "query": key.get("keyData", {}).get("query", ""),
            "app": key.get("keyData", {}).get("app", ""),
            "user": key.get("keyData", {}).get("user", ""),
            "database": key.get("keyData", {}).get("database", ""),
            "node_id": key.get("nodeId", 0),
            "dist_sql": key.get("keyData", {}).get("distSQL", False),
            "failed": key.get("keyData", {}).get("failed", False),
            "implicit_txn": key.get("keyData", {}).get("implicitTxn", False),
            "count": int(stats.get("count", 0)),
            "first_attempt_count": int(stats.get("firstAttemptCount", 0)),
            "max_retries": int(stats.get("maxRetries", 0)),
            "bytes_read": int(stats.get("bytesRead", 0)),
            "rows_read": int(stats.get("rowsRead", 0)),
            "failed_count": int(stats.get("failedCount", 0)),
            # Latencies in seconds (mean)
            "parse_latency_s": stats.get("parseLat", {}).get("mean", 0),
            "plan_latency_s": stats.get("planLat", {}).get("mean", 0),
            "run_latency_s": stats.get("runLat", {}).get("mean", 0),
            "service_latency_s": stats.get("serviceLat", {}).get("mean", 0),
            "overhead_latency_s": stats.get("overheadLat", {}).get("mean", 0),
            # Derived latencies in ms
            "service_latency_ms": stats.get("serviceLat", {}).get("mean", 0) * 1000,
            "run_latency_ms": stats.get("runLat", {}).get("mean", 0) * 1000,
            "plan_latency_ms": stats.get("planLat", {}).get("mean", 0) * 1000,
            "parse_latency_ms": stats.get("parseLat", {}).get("mean", 0) * 1000,
            # Rows
            "num_rows_mean": stats.get("numRows", {}).get("mean", 0),
            # Last error
            "last_err": stats.get("sensitiveInfo", {}).get("lastErr", ""),
        }
        statements.append(stmt)
    return statements


def filter_and_sort(statements: list[dict], min_latency_ms: float, sort_by: str) -> list[dict]:
    """Filter statements by minimum latency and sort."""
    filtered = [s for s in statements if s["service_latency_ms"] >= min_latency_ms]

    sort_key_map = {
        "service_lat": "service_latency_ms",
        "run_lat": "run_latency_ms",
        "plan_lat": "plan_latency_ms",
        "count": "count",
    }
    sort_key = sort_key_map.get(sort_by, "service_latency_ms")
    filtered.sort(key=lambda x: x[sort_key], reverse=True)

    return filtered


def format_statement(stmt: dict, index: int) -> str:
    """Format a single statement for display."""
    lines = [
        f"{'='*80}",
        f"[{index + 1}] Slow Statement",
        f"{'='*80}",
        f"Query: {stmt['query'][:200]}{'...' if len(stmt['query']) > 200 else ''}",
        f"App: {stmt['app']}",
        f"User: {stmt['user']} | Database: {stmt['database']}",
        f"Node ID: {stmt['node_id']}",
        f"",
        f"Latency (ms):",
        f"  - Service: {stmt['service_latency_ms']:.3f}",
        f"  - Run:     {stmt['run_latency_ms']:.3f}",
        f"  - Plan:    {stmt['plan_latency_ms']:.3f}",
        f"  - Parse:   {stmt['parse_latency_ms']:.3f}",
        f"",
        f"Execution:",
        f"  - Count: {stmt['count']}",
        f"  - First Attempts: {stmt['first_attempt_count']}",
        f"  - Max Retries: {stmt['max_retries']}",
        f"  - Failed Count: {stmt['failed_count']}",
        f"",
        f"Data:",
        f"  - Rows Read (avg): {stmt['num_rows_mean']:.1f}",
        f"  - Bytes Read: {stmt['bytes_read']}",
        f"  - Rows Read (total): {stmt['rows_read']}",
        f"",
        f"Flags: DistSQL={stmt['dist_sql']} | Failed={stmt['failed']} | ImplicitTxn={stmt['implicit_txn']}",
    ]

    if stmt["last_err"]:
        lines.append(f"Last Error: {stmt['last_err']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze slow SQL statements from KaiwuDB"
    )
    parser.add_argument("--host", default="localhost", help="KaiwuDB admin host")
    parser.add_argument("--port", type=int, default=8080, help="KaiwuDB admin port")
    parser.add_argument("--limit", type=int, default=10, help="Number of statements to show")
    parser.add_argument(
        "--min-latency-ms",
        type=float,
        default=0,
        help="Minimum service latency (ms) to include in results"
    )
    parser.add_argument(
        "--sort-by",
        choices=["service_lat", "run_lat", "plan_lat", "count"],
        default="service_lat",
        help="Sort criteria (default: service_lat)"
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    data = fetch_statements(args.host, args.port)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    statements = parse_statements(data)
    filtered = filter_and_sort(statements, args.min_latency_ms, args.sort_by)

    last_reset = data.get("lastReset", "unknown")
    internal_prefix = data.get("internalAppNamePrefix", "")

    print(f"KaiwuDB Statements Summary")
    print(f"{'='*80}")
    print(f"Last Reset: {last_reset}")
    print(f"Internal App Prefix: {internal_prefix}")
    print(f"Total Statements: {len(statements)}")
    print(f"Showing: {min(args.limit, len(filtered))} of {len(filtered)} statements "
          f"(sorted by {args.sort_by}, min_latency={args.min_latency_ms}ms)")
    print()

    for i, stmt in enumerate(filtered[:args.limit]):
        print(format_statement(stmt, i))
        print()


if __name__ == "__main__":
    main()
