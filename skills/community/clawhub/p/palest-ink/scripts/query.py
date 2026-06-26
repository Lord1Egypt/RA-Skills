#!/usr/bin/env python3
"""Palest Ink - Activity Query Tool

Search and filter activity records. Designed to be called by Claude Code skill.

Usage:
    python3 query.py --date today --summary
    python3 query.py --date 2026-03-03 --type git_commit --search "plugin"
    python3 query.py --from 2026-03-01 --to 2026-03-03 --type web_visit --search "homebrew"
    python3 query.py --date today --type web_visit --search-content "人效"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Shanghai")


def ts_to_local_str(ts_str):
    """Convert UTC ISO timestamp to local time string (YYYY-MM-DD HH:MM:SS)."""
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts_str[:19].replace("T", " ")

DATA_DIR = os.path.expanduser("~/.palest-ink/data")

ACTIVITY_TYPES = {
    "git_commit", "git_push", "git_pull", "git_checkout",
    "web_visit", "shell_command", "vscode_edit",
    "app_focus", "file_change",
}

TYPE_LABELS = {
    "git_commit": "Git Commit",
    "git_push": "Git Push",
    "git_pull": "Git Pull",
    "git_checkout": "Git Checkout",
    "web_visit": "Web Visit",
    "shell_command": "Shell Command",
    "vscode_edit": "VS Code Edit",
    "app_focus": "App Focus",
    "file_change": "File Change",
}


def parse_date(s):
    """Parse a date string, supporting 'today', 'yesterday', and ISO format."""
    s = s.strip().lower()
    today = datetime.now().date()
    if s == "today":
        return today
    elif s == "yesterday":
        return today - timedelta(days=1)
    else:
        return datetime.strptime(s, "%Y-%m-%d").date()


def get_datafiles(date_from, date_to):
    """Get list of JSONL data file paths for the date range."""
    files = []
    d = date_from
    while d <= date_to:
        path = os.path.join(DATA_DIR, d.strftime("%Y"), d.strftime("%m"), f"{d.strftime('%d')}.jsonl")
        if os.path.exists(path):
            files.append(path)
        d += timedelta(days=1)
    return files


def load_records(files, type_filter=None):
    """Load all records from the given files, optionally filtering by type."""
    records = []
    for filepath in files:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if type_filter and record.get("type") != type_filter:
                    continue
                records.append(record)
    return records


def search_records(records, term, search_content=False):
    """Filter records matching search term across all data fields."""
    term_lower = term.lower()
    matched = []
    for record in records:
        data = record.get("data", {})
        # Search in all string values of data
        searchable = []
        for key, val in data.items():
            if isinstance(val, str):
                searchable.append(val)
            elif isinstance(val, list):
                searchable.extend(str(v) for v in val)
        # Also search in content_summary and content_keywords if search_content
        if search_content:
            summary = data.get("content_summary", "")
            keywords = data.get("content_keywords", [])
            searchable.append(summary)
            searchable.extend(keywords)

        text = " ".join(searchable).lower()
        if term_lower in text:
            matched.append(record)
    return matched


def format_record_text(record):
    """Format a single record for text output."""
    ts = ts_to_local_str(record.get("ts", ""))
    rtype = record.get("type", "unknown")
    data = record.get("data", {})
    label = TYPE_LABELS.get(rtype, rtype)

    if rtype == "git_commit":
        repo = os.path.basename(data.get("repo", ""))
        msg = data.get("message", "")
        files = data.get("files_changed", [])
        ins = data.get("insertions", 0)
        dels = data.get("deletions", 0)
        return f"[{ts}] {label}: {repo} - {msg} ({len(files)} files, +{ins}/-{dels})"

    elif rtype == "git_push":
        repo = os.path.basename(data.get("repo", ""))
        branch = data.get("branch", "")
        return f"[{ts}] {label}: {repo} ({branch}) -> {data.get('remote', '')}"

    elif rtype == "git_pull":
        repo = os.path.basename(data.get("repo", ""))
        branch = data.get("branch", "")
        return f"[{ts}] {label}: {repo} ({branch})"

    elif rtype == "git_checkout":
        repo = os.path.basename(data.get("repo", ""))
        return f"[{ts}] {label}: {repo} ({data.get('from_ref', '')} -> {data.get('to_branch', '')})"

    elif rtype == "web_visit":
        title = data.get("title", "")[:60]
        url = data.get("url", "")
        duration = data.get("visit_duration_seconds", 0)
        browser = data.get("browser", "")
        content_summary = data.get("content_summary", "")[:100]
        line = f"[{ts}] {label} ({browser}): {title}\n         URL: {url}"
        if duration > 0:
            line += f" ({duration}s)"
        if content_summary:
            line += f"\n         Summary: {content_summary}..."
        return line

    elif rtype == "shell_command":
        cmd = data.get("command", "")[:120]
        return f"[{ts}] {label}: {cmd}"

    elif rtype == "vscode_edit":
        filepath = data.get("file_path", "")
        lang = data.get("language", "")
        return f"[{ts}] {label}: {filepath} ({lang})"

    elif rtype == "app_focus":
        app = data.get("app_name", "")
        window = data.get("window_title", "")
        dur = data.get("duration_seconds", 0)
        suffix = f" — {window[:60]}" if window else ""
        return f"[{ts}] {label}: {app}{suffix} ({dur}s)"

    elif rtype == "file_change":
        path = data.get("path", "")
        lang = data.get("language", "")
        workspace = os.path.basename(data.get("workspace", ""))
        suffix = f" in {workspace}" if workspace else ""
        return f"[{ts}] {label}: {path} ({lang}){suffix}"

    else:
        return f"[{ts}] {label}: {json.dumps(data, ensure_ascii=False)[:100]}"


def print_summary(records):
    """Print a summary of records by type."""
    counts = {}
    for r in records:
        rtype = r.get("type", "unknown")
        counts[rtype] = counts.get(rtype, 0) + 1

    total = len(records)
    print(f"Total activities: {total}")
    print("-" * 40)
    for rtype, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        label = TYPE_LABELS.get(rtype, rtype)
        print(f"  {label}: {count}")

    # Additional stats for git
    git_commits = [r for r in records if r.get("type") == "git_commit"]
    if git_commits:
        repos = set(r.get("data", {}).get("repo", "") for r in git_commits)
        total_ins = sum(r.get("data", {}).get("insertions", 0) for r in git_commits)
        total_del = sum(r.get("data", {}).get("deletions", 0) for r in git_commits)
        print(f"\nGit: {len(git_commits)} commits across {len(repos)} repos (+{total_ins}/-{total_del})")

    # Web stats
    web_visits = [r for r in records if r.get("type") == "web_visit"]
    if web_visits:
        domains = set()
        for r in web_visits:
            url = r.get("data", {}).get("url", "")
            try:
                from urllib.parse import urlparse
                domains.add(urlparse(url).netloc)
            except Exception:
                pass
        print(f"Web: {len(web_visits)} page visits across {len(domains)} domains")


def main():
    parser = argparse.ArgumentParser(description="Palest Ink - Query activities")
    parser.add_argument("--date", help="Date to query (YYYY-MM-DD, 'today', 'yesterday')")
    parser.add_argument("--from", dest="date_from", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", help="End date (YYYY-MM-DD)")
    parser.add_argument("--type", dest="activity_type", help="Filter by activity type")
    parser.add_argument("--search", help="Search term across all fields")
    parser.add_argument("--search-content", help="Search term including web page content summaries")
    parser.add_argument("--summary", action="store_true", help="Show summary instead of records")
    parser.add_argument("--limit", type=int, default=50, help="Max records to show (default: 50)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Determine date range
    if args.date:
        date_from = date_to = parse_date(args.date)
    elif args.date_from and args.date_to:
        date_from = parse_date(args.date_from)
        date_to = parse_date(args.date_to)
    else:
        date_from = date_to = datetime.now().date()

    # Find data files
    files = get_datafiles(date_from, date_to)
    if not files:
        print(f"No data found for {date_from} to {date_to}")
        sys.exit(0)

    # Load records
    records = load_records(files, type_filter=args.activity_type)

    # Apply search
    if args.search:
        records = search_records(records, args.search)
    if args.search_content:
        records = search_records(records, args.search_content, search_content=True)

    # Sort by timestamp
    records.sort(key=lambda r: r.get("ts", ""))

    # Output
    if args.summary:
        print_summary(records)
    elif args.format == "json":
        output = records[:args.limit]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        for record in records[:args.limit]:
            print(format_record_text(record))
            print()

        if len(records) > args.limit:
            print(f"... and {len(records) - args.limit} more records (use --limit to see more)")


if __name__ == "__main__":
    main()
