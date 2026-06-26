#!/usr/bin/env python3
"""Log file analyzer — detects error patterns, aggregates by severity, flags anomalies.

Usage:
    analyze_logs.py <logfile> [--top N] [--severity LEVEL] [--json] [--since TIMESTAMP]
    analyze_logs.py --help

Examples:
    analyze_logs.py /var/log/syslog
    analyze_logs.py app.log --top 20 --severity ERROR
    analyze_logs.py server.log --json --since "2026-03-01"
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Common log patterns
SEVERITY_PATTERNS = {
    "FATAL": re.compile(r"\b(FATAL|CRITICAL|EMERG|PANIC)\b", re.IGNORECASE),
    "ERROR": re.compile(r"\b(ERROR|ERR|SEVERE|FAIL(ED|URE)?)\b", re.IGNORECASE),
    "WARN": re.compile(r"\b(WARN(ING)?|CAUTION)\b", re.IGNORECASE),
    "INFO": re.compile(r"\b(INFO|NOTICE)\b", re.IGNORECASE),
    "DEBUG": re.compile(r"\b(DEBUG|TRACE|VERBOSE)\b", re.IGNORECASE),
}

SEVERITY_ORDER = ["FATAL", "ERROR", "WARN", "INFO", "DEBUG", "UNKNOWN"]

TIMESTAMP_PATTERNS = [
    # ISO 8601
    re.compile(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})"),
    # Common syslog
    re.compile(r"([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"),
    # Nginx/Apache
    re.compile(r"\[(\d{2}/[A-Z][a-z]{2}/\d{4}:\d{2}:\d{2}:\d{2})"),
]

# Common error fingerprints to group
ERROR_FINGERPRINT_STRIP = re.compile(
    r"(0x[0-9a-fA-F]+|"           # hex addresses
    r"\d{10,}|"                     # long numbers (timestamps, IDs)
    r"pid[= ]\d+|"                  # process IDs
    r"port \d+|"                    # port numbers
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # IP addresses
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"  # UUIDs
)


def classify_severity(line: str) -> str:
    """Classify a log line by severity."""
    for level, pattern in SEVERITY_PATTERNS.items():
        if pattern.search(line):
            return level
    return "UNKNOWN"


def extract_timestamp(line: str) -> str | None:
    """Try to extract a timestamp string from a log line."""
    for pattern in TIMESTAMP_PATTERNS:
        m = pattern.search(line)
        if m:
            return m.group(1)
    return None


def fingerprint(line: str) -> str:
    """Create a normalized fingerprint for grouping similar errors."""
    # Remove timestamp-like prefix
    stripped = re.sub(r"^\S+\s+", "", line.strip())
    # Remove variable parts
    stripped = ERROR_FINGERPRINT_STRIP.sub("<VAR>", stripped)
    # Collapse whitespace
    stripped = re.sub(r"\s+", " ", stripped).strip()
    # Truncate for grouping
    return stripped[:200] if stripped else line[:200]


def analyze(filepath: str, top_n: int = 15, min_severity: str | None = None, since: str | None = None) -> dict:
    """Analyze a log file and return structured results."""
    severity_counts = Counter()
    error_groups = Counter()
    error_examples = {}
    total_lines = 0
    empty_lines = 0
    first_ts = None
    last_ts = None
    hourly_errors = defaultdict(int)

    severity_filter = None
    if min_severity:
        min_severity = min_severity.upper()
        if min_severity in SEVERITY_ORDER:
            severity_filter = set(SEVERITY_ORDER[: SEVERITY_ORDER.index(min_severity) + 1])

    since_str = since.strip() if since else None

    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    file_size = path.stat().st_size
    file_size_human = (
        f"{file_size / (1024*1024):.1f} MB" if file_size > 1024 * 1024
        else f"{file_size / 1024:.1f} KB" if file_size > 1024
        else f"{file_size} B"
    )

    with open(filepath, "r", errors="replace") as f:
        for line in f:
            total_lines += 1
            stripped = line.strip()
            if not stripped:
                empty_lines += 1
                continue

            ts = extract_timestamp(stripped)
            if ts:
                if first_ts is None:
                    first_ts = ts
                last_ts = ts

            # Filter by since
            if since_str and ts and ts < since_str:
                continue

            severity = classify_severity(stripped)
            severity_counts[severity] += 1

            if severity in ("FATAL", "ERROR", "WARN"):
                fp = fingerprint(stripped)
                error_groups[fp] += 1
                if fp not in error_examples:
                    error_examples[fp] = stripped[:500]

                # Track hourly distribution
                if ts:
                    hour_key = ts[:13] if len(ts) >= 13 else ts[:10]
                    hourly_errors[hour_key] += 1

    # Build top errors
    top_errors = []
    for fp, count in error_groups.most_common(top_n):
        top_errors.append({
            "count": count,
            "fingerprint": fp,
            "example": error_examples.get(fp, ""),
        })

    # Detect anomaly hours (errors > 2x average)
    anomaly_hours = []
    if hourly_errors:
        avg_errors = sum(hourly_errors.values()) / len(hourly_errors)
        threshold = max(avg_errors * 2, 5)
        for hour, count in sorted(hourly_errors.items()):
            if count > threshold:
                anomaly_hours.append({"hour": hour, "errors": count, "avg": round(avg_errors, 1)})

    result = {
        "file": filepath,
        "file_size": file_size_human,
        "total_lines": total_lines,
        "empty_lines": empty_lines,
        "time_range": {"first": first_ts, "last": last_ts},
        "severity_breakdown": {k: severity_counts.get(k, 0) for k in SEVERITY_ORDER},
        "top_errors": top_errors,
        "anomaly_hours": anomaly_hours,
    }

    if severity_filter:
        result["severity_filter"] = min_severity

    return result


def print_report(result: dict) -> None:
    """Print a human-readable report."""
    print(f"\n{'='*60}")
    print(f"  LOG ANALYSIS: {result['file']}")
    print(f"{'='*60}")
    print(f"  Size: {result['file_size']}  |  Lines: {result['total_lines']:,}  |  Empty: {result['empty_lines']:,}")

    tr = result["time_range"]
    if tr["first"]:
        print(f"  Time range: {tr['first']} → {tr['last']}")

    print(f"\n  SEVERITY BREAKDOWN:")
    for level in SEVERITY_ORDER:
        count = result["severity_breakdown"].get(level, 0)
        if count > 0:
            bar = "█" * min(count * 40 // max(result["total_lines"], 1), 40)
            pct = count * 100 / max(result["total_lines"], 1)
            print(f"    {level:8s}  {count:>8,}  ({pct:5.1f}%)  {bar}")

    if result["top_errors"]:
        print(f"\n  TOP ERROR PATTERNS (grouped):")
        for i, err in enumerate(result["top_errors"], 1):
            print(f"\n    #{i}  [{err['count']}x]")
            example = err["example"]
            if len(example) > 120:
                example = example[:117] + "..."
            print(f"       {example}")

    if result["anomaly_hours"]:
        print(f"\n  ANOMALY HOURS (>{2}x average error rate):")
        for a in result["anomaly_hours"]:
            print(f"    {a['hour']}  — {a['errors']} errors (avg: {a['avg']})")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files — detect errors, group patterns, flag anomalies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s /var/log/syslog\n"
               "  %(prog)s app.log --top 20 --severity ERROR\n"
               "  %(prog)s server.log --json --since '2026-03-01'\n",
    )
    parser.add_argument("logfile", help="Path to the log file to analyze")
    parser.add_argument("--top", type=int, default=15, help="Number of top error patterns to show (default: 15)")
    parser.add_argument("--severity", type=str, default=None, help="Minimum severity to include (FATAL, ERROR, WARN, INFO, DEBUG)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--since", type=str, default=None, help="Only analyze lines after this timestamp (e.g. '2026-03-01')")

    args = parser.parse_args()

    result = analyze(args.logfile, top_n=args.top, min_severity=args.severity, since=args.since)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
