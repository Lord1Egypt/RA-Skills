#!/usr/bin/env python3
"""Git repository statistics analyzer.

Produces contributor stats, commit frequency, file-type breakdown,
LOC counts, and activity trends from any local git repo.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta


def run_git(args, cwd=None):
    """Run a git command and return stdout lines."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60,
        )
        if result.returncode != 0:
            return []
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def get_repo_root(path):
    """Find the git repo root from a path."""
    lines = run_git(["rev-parse", "--show-toplevel"], cwd=path)
    return lines[0] if lines else None


def get_commit_log(cwd, since=None, until=None, branch=None):
    """Get commit log as list of (hash, author, email, date_iso, subject)."""
    args = ["log", "--format=%H|%aN|%aE|%aI|%s", "--no-merges"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    if branch:
        args.append(branch)
    lines = run_git(args, cwd=cwd)
    commits = []
    for line in lines:
        parts = line.split("|", 4)
        if len(parts) == 5:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "email": parts[2],
                "date": parts[3],
                "subject": parts[4],
            })
    return commits


def get_contributor_stats(cwd, branch=None):
    """Get per-author commit counts."""
    args = ["shortlog", "-sne", "--no-merges"]
    if branch:
        args.append(branch)
    else:
        args.append("HEAD")
    lines = run_git(args, cwd=cwd)
    contributors = []
    for line in lines:
        match = re.match(r"\s*(\d+)\s+(.+?)\s+<(.+?)>", line)
        if match:
            contributors.append({
                "commits": int(match.group(1)),
                "name": match.group(2),
                "email": match.group(3),
            })
    return sorted(contributors, key=lambda c: c["commits"], reverse=True)


def get_file_type_breakdown(cwd):
    """Count files by extension in the repo."""
    lines = run_git(["ls-files"], cwd=cwd)
    ext_counts = Counter()
    for f in lines:
        if f:
            ext = os.path.splitext(f)[1].lower() or "(no ext)"
            ext_counts[ext] += 1
    return dict(ext_counts.most_common(25))


def get_loc_stats(cwd):
    """Count lines of code for tracked files (top 10 extensions)."""
    lines = run_git(["ls-files"], cwd=cwd)
    ext_loc = defaultdict(int)
    total_files = 0
    total_lines = 0
    for f in lines:
        if not f:
            continue
        filepath = os.path.join(cwd, f)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(f)[1].lower() or "(no ext)"
        try:
            with open(filepath, "r", errors="ignore") as fh:
                count = sum(1 for _ in fh)
                ext_loc[ext] += count
                total_lines += count
                total_files += 1
        except (OSError, UnicodeDecodeError):
            pass
    top = dict(sorted(ext_loc.items(), key=lambda x: x[1], reverse=True)[:15])
    return {"total_files": total_files, "total_lines": total_lines, "by_extension": top}


def get_activity_by_day(commits):
    """Group commit counts by day of week."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = Counter()
    for c in commits:
        try:
            dt = datetime.fromisoformat(c["date"])
            day_counts[days[dt.weekday()]] += 1
        except (ValueError, IndexError):
            pass
    return {d: day_counts.get(d, 0) for d in days}


def get_activity_by_hour(commits):
    """Group commit counts by hour of day."""
    hour_counts = Counter()
    for c in commits:
        try:
            dt = datetime.fromisoformat(c["date"])
            hour_counts[dt.hour] += 1
        except ValueError:
            pass
    return {f"{h:02d}:00": hour_counts.get(h, 0) for h in range(24)}


def get_monthly_trend(commits, months=12):
    """Commit count per month for the last N months."""
    now = datetime.now()
    buckets = {}
    for i in range(months):
        d = now - timedelta(days=30 * i)
        key = d.strftime("%Y-%m")
        buckets[key] = 0
    for c in commits:
        try:
            dt = datetime.fromisoformat(c["date"])
            key = dt.strftime("%Y-%m")
            if key in buckets:
                buckets[key] += 1
        except ValueError:
            pass
    return dict(sorted(buckets.items()))


def format_text(stats):
    """Format stats as human-readable text."""
    lines = []
    lines.append(f"=== Git Repository Statistics ===")
    lines.append(f"Repository: {stats['repo_path']}")
    lines.append(f"Total commits (non-merge): {stats['total_commits']}")
    lines.append("")

    lines.append("--- Top Contributors ---")
    for i, c in enumerate(stats["contributors"][:15], 1):
        lines.append(f"  {i:>3}. {c['name']} <{c['email']}> — {c['commits']} commits")
    lines.append("")

    lines.append("--- Lines of Code ---")
    loc = stats["loc"]
    lines.append(f"  Total files: {loc['total_files']}")
    lines.append(f"  Total lines: {loc['total_lines']:,}")
    for ext, count in loc["by_extension"].items():
        lines.append(f"    {ext:>12}: {count:>8,} lines")
    lines.append("")

    lines.append("--- File Types ---")
    for ext, count in stats["file_types"].items():
        lines.append(f"    {ext:>12}: {count:>5} files")
    lines.append("")

    lines.append("--- Activity by Day of Week ---")
    for day, count in stats["activity_by_day"].items():
        bar = "█" * min(count, 50)
        lines.append(f"  {day:>10}: {count:>4}  {bar}")
    lines.append("")

    lines.append("--- Activity by Hour ---")
    for hour, count in stats["activity_by_hour"].items():
        bar = "█" * min(count, 50)
        lines.append(f"  {hour}: {count:>4}  {bar}")
    lines.append("")

    lines.append("--- Monthly Trend ---")
    for month, count in stats["monthly_trend"].items():
        bar = "█" * min(count, 50)
        lines.append(f"  {month}: {count:>4}  {bar}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze git repository statistics: contributors, LOC, activity, trends."
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)",
    )
    parser.add_argument("--branch", default=None, help="Analyze specific branch")
    parser.add_argument("--since", default=None, help="Only commits after date (e.g. 2025-01-01)")
    parser.add_argument("--until", default=None, help="Only commits before date")
    parser.add_argument("--months", type=int, default=12, help="Monthly trend window (default: 12)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-loc", action="store_true", help="Skip LOC counting (faster)")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
    root = get_repo_root(repo_path)
    if not root:
        print(f"Error: '{repo_path}' is not inside a git repository.", file=sys.stderr)
        sys.exit(1)

    commits = get_commit_log(root, since=args.since, until=args.until, branch=args.branch)
    contributors = get_contributor_stats(root, branch=args.branch)
    file_types = get_file_type_breakdown(root)
    loc = get_loc_stats(root) if not args.no_loc else {"total_files": 0, "total_lines": 0, "by_extension": {}}
    activity_day = get_activity_by_day(commits)
    activity_hour = get_activity_by_hour(commits)
    monthly = get_monthly_trend(commits, months=args.months)

    stats = {
        "repo_path": root,
        "total_commits": len(commits),
        "contributors": contributors,
        "file_types": file_types,
        "loc": loc,
        "activity_by_day": activity_day,
        "activity_by_hour": activity_hour,
        "monthly_trend": monthly,
    }

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(format_text(stats))


if __name__ == "__main__":
    main()
