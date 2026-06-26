#!/usr/bin/env python3
"""
GitHub Issues Fetcher for PMO Skill.
Reads open/closed issue counts and details from GitHub repos.
Returns structured data for portfolio analysis.

Usage:
    python github_fetch.py --owner my-org --repo my-project [--token-env GH_TOKEN]

Environment:
    GH_TOKEN: GitHub personal access token (or via --token flag)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional


def make_github_request(url: str, token: str) -> dict:
    """Make authenticated GitHub API request."""
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "pmo-skill/1.0")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"GitHub API error {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e


def fetch_repo_issues(owner: str, repo: str, token: str) -> dict:
    """
    Fetch all issues for a repo (open + closed).
    Returns structured data for PMO analysis.
    """
    base_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Fetch open issues
    open_url = f"{base_url}/issues?state=open&per_page=100"
    open_data = make_github_request(open_url, token)

    # Fetch closed issues (last 90 days for relevance)
    closed_url = f"{base_url}/issues?state=closed&per_page=100&sort=updated"
    closed_data = make_github_request(closed_url, token)

    # Filter out pull requests from both lists (GitHub API returns PRs in issues endpoint)
    open_issues = [i for i in open_data if "pull_request" not in i]
    closed_issues = [i for i in closed_data if "pull_request" not in i]

    open_count = len(open_issues)
    closed_count = len(closed_issues)
    total_count = open_count + closed_count

    progress = round(closed_count / total_count * 100, 1) if total_count > 0 else 0.0

    # Find last updated timestamp
    last_updated = None
    if open_issues:
        last_updated = max(i["updated_at"] for i in open_issues)
    if closed_issues:
        closed_latest = max(i["updated_at"] for i in closed_issues)
        last_updated = max(last_updated or "", closed_latest)

    # Build issue list with relevant fields
    def sanitize_issue(issue: dict) -> dict:
        return {
            "id": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "labels": [l["name"] for l in issue.get("labels", [])],
            "url": issue["html_url"],
            "created_at": issue["created_at"],
            "updated_at": issue["updated_at"],
            "assignees": [a["login"] for a in issue.get("assignees", [])],
        }

    issues = [sanitize_issue(i) for i in (open_issues + closed_issues)]

    result = {
        "project_name": f"{owner}/{repo}",
        "owner": owner,
        "repo": repo,
        "open_count": open_count,
        "closed_count": closed_count,
        "total_count": total_count,
        "progress_pct": progress,
        "last_updated": last_updated,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "issues": issues,
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub issues for PMO portfolio")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument(
        "--token-env",
        default="GH_TOKEN",
        help="Environment variable name for GitHub token (default: GH_TOKEN)",
    )
    parser.add_argument(
        "--token",
        dest="token_value",
        default=None,
        help="Direct token value (use sparingly — prefer --token-env)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "summary"],
        default="json",
        help="Output format: json (full) or summary (human-readable)",
    )

    args = parser.parse_args()

    # Resolve token
    if args.token_value:
        token = args.token_value
    else:
        token = os.environ.get(args.token_env)
        if not token:
            print(
                f"Error: {args.token_env} environment variable not set. "
                f"Set it or pass --token directly.",
                file=sys.stderr,
            )
            sys.exit(1)

    try:
        data = fetch_repo_issues(args.owner, args.repo, token)

        if args.format == "summary":
            print(f"Project: {data['project_name']}")
            print(f"Open:   {data['open_count']}")
            print(f"Closed: {data['closed_count']}")
            print(f"Progress: {data['progress_pct']}%")
            print(f"Last updated: {data['last_updated']}")
            print(f"\nIssues:")
            for issue in data["issues"]:
                labels = f" [{','.join(issue['labels'])}]" if issue["labels"] else ""
                print(f"  #{issue['id']} [{issue['state'].upper()}] {issue['title']}{labels}")
        else:
            print(json.dumps(data, indent=2))

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
