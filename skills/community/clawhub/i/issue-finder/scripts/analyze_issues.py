#!/usr/bin/env python3
"""
GitHub Issue Analyzer - Analyze issues for contribution potential.

Usage:
    python analyze_issues.py --repo owner/repo --issue 123
    python analyze_issues.py --repo owner/repo --all --limit 20
    python analyze_issues.py --repo owner/repo --labels "good first issue,help wanted"
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


def run_gh_command(args: list[str]) -> dict[str, Any] | list[Any] | None:
    """Run a gh CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        return None


def analyze_issue_health(issue: dict[str, Any]) -> dict[str, Any]:
    """Analyze health indicators for a single issue."""
    created = datetime.fromisoformat(issue["createdAt"].replace("Z", "+00:00"))
    updated = datetime.fromisoformat(issue["updatedAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    age_days = (now - created).days
    time_since_update = (now - updated).days

    labels = [label["name"] for label in issue.get("labels", [])]

    return {
        "number": issue["number"],
        "title": issue["title"],
        "age_days": age_days,
        "time_since_update": time_since_update,
        "comment_count": issue.get("comments", 0),
        "labels": labels,
        "is_good_first_issue": "good first issue" in labels,
        "is_help_wanted": "help wanted" in labels,
        "has_bug_label": "bug" in labels,
        "has_enhancement_label": "enhancement" in labels,
        "health_score": calculate_health_score(age_days, time_since_update, issue.get("comments", 0)),
    }


def calculate_health_score(age_days: int, time_since_update: int, comments: int) -> int:
    """Calculate a health score for an issue (1-10)."""
    score = 10

    # Fresh issues are better
    if age_days > 365:
        score -= 3
    elif age_days > 180:
        score -= 2
    elif age_days > 90:
        score -= 1

    # Recent activity is good
    if time_since_update > 60:
        score -= 2
    elif time_since_update > 30:
        score -= 1

    # Some discussion is good
    if comments == 0:
        score -= 1
    elif comments > 10:
        score -= 1  # Too much discussion might indicate complexity

    return max(1, min(10, score))


def analyze_issue_complexity(issue: dict[str, Any]) -> str:
    """Estimate issue complexity based on labels and description."""
    labels = [label["name"] for label in issue.get("labels", [])]

    if "good first issue" in labels or "documentation" in labels:
        return "Tiny-Small"
    elif "help wanted" in labels and "bug" in labels:
        return "Small-Medium"
    elif "enhancement" in labels:
        return "Medium"
    elif "feature" in labels:
        return "Medium-Large"
    else:
        return "Unknown"


def generate_report(repo: str, issues: list[dict[str, Any]]) -> str:
    """Generate a markdown report from analyzed issues."""
    report_lines = [
        f"# Issue Analysis Report for {repo}",
        f"\nGenerated: {datetime.now(timezone.utc).isoformat()}",
        f"\n## Summary",
        f"\nTotal issues analyzed: {len(issues)}",
        "\n## Issues by Health Score\n",
        "| # | Title | Score | Complexity | Age (days) | Labels |",
        "|---|-------|-------|------------|------------|--------|",
    ]

    sorted_issues = sorted(issues, key=lambda x: x["health_score"], reverse=True)

    for issue in sorted_issues:
        labels_str = ", ".join(issue["labels"][:3])
        if len(issue["labels"]) > 3:
            labels_str += "..."
        report_lines.append(
            f"| #{issue['number']} | {issue['title'][:40]}... | "
            f"{issue['health_score']}/10 | {issue.get('complexity', 'Unknown')} | "
            f"{issue['age_days']} | {labels_str} |"
        )

    report_lines.extend([
        "\n## Recommendations\n",
        "### High Priority Issues\n",
    ])

    high_priority = [i for i in sorted_issues if i["health_score"] >= 7 and i["is_good_first_issue"]]
    for issue in high_priority[:5]:
        report_lines.append(f"- #{issue['number']}: {issue['title']}")

    if not high_priority:
        report_lines.append("No high priority issues found.")

    report_lines.extend([
        "\n### Good for Learning\n",
    ])

    learning_issues = [i for i in sorted_issues if i["is_help_wanted"] or i["is_good_first_issue"]]
    for issue in learning_issues[:5]:
        report_lines.append(f"- #{issue['number']}: {issue['title']}")

    if not learning_issues:
        report_lines.append("No beginner-friendly issues found.")

    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze GitHub issues for contribution potential")
    parser.add_argument("--repo", required=True, help="Repository in owner/repo format")
    parser.add_argument("--issue", type=int, help="Specific issue number to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all open issues")
    parser.add_argument("--limit", type=int, default=20, help="Limit number of issues to analyze")
    parser.add_argument("--labels", help="Filter by labels (comma-separated)")
    parser.add_argument("--output", help="Output file for report (default: stdout)")

    args = parser.parse_args()

    # Build gh command
    cmd_args = [
        "issue", "list",
        "--repo", args.repo,
        "--state", "open",
        "--limit", str(args.limit),
        "--json", "number,title,labels,createdAt,updatedAt,comments,state",
    ]

    if args.labels:
        for label in args.labels.split(","):
            cmd_args.extend(["--label", label.strip()])

    if args.issue:
        cmd_args = [
            "issue", "view",
            str(args.issue),
            "--repo", args.repo,
            "--json", "number,title,labels,createdAt,updatedAt,comments,state,body",
        ]
        issue_data = run_gh_command(cmd_args)
        if issue_data:
            analyzed = analyze_issue_health(issue_data)
            analyzed["complexity"] = analyze_issue_complexity(issue_data)
            issues = [analyzed]
        else:
            print("Failed to fetch issue", file=sys.stderr)
            sys.exit(1)
    else:
        issues_data = run_gh_command(cmd_args)
        if not issues_data:
            print("Failed to fetch issues", file=sys.stderr)
            sys.exit(1)

        issues = []
        for issue in issues_data:
            analyzed = analyze_issue_health(issue)
            analyzed["complexity"] = analyze_issue_complexity(issue)
            issues.append(analyzed)

    # Generate report
    report = generate_report(args.repo, issues)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()