#!/usr/bin/env python3
"""
check_github.py - Fetch releases for a GitHub repo via public API.

Usage:
    python3 check_github.py <owner> <repo> [--limit N]

Output: JSON array of releases, each with tag, name, body, published_at.
Exits with code 1 on error.
"""

import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime, timezone

DEFAULT_LIMIT = 10


def fetch_releases(owner: str, repo: str, limit: int = DEFAULT_LIMIT) -> list:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page={limit}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "changelog-watcher/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            retry_after = e.headers.get("Retry-After", "60")
            print(
                json.dumps({
                    "error": "rate_limited",
                    "message": f"GitHub API rate limit hit. Retry after {retry_after}s.",
                    "retry_after": int(retry_after),
                }),
                file=sys.stderr,
            )
            sys.exit(2)
        elif e.code == 404:
            print(
                json.dumps({
                    "error": "not_found",
                    "message": f"Repo {owner}/{repo} not found or has no releases.",
                }),
                file=sys.stderr,
            )
            sys.exit(3)
        else:
            print(
                json.dumps({"error": "http_error", "message": str(e)}),
                file=sys.stderr,
            )
            sys.exit(1)
    except urllib.error.URLError as e:
        print(
            json.dumps({"error": "network_error", "message": str(e.reason)}),
            file=sys.stderr,
        )
        sys.exit(1)

    releases = []
    for r in data:
        releases.append({
            "source": "github",
            "owner": owner,
            "repo": repo,
            "tag": r.get("tag_name", ""),
            "name": r.get("name", "") or r.get("tag_name", ""),
            "body": r.get("body", "") or "",
            "published_at": r.get("published_at", ""),
            "prerelease": r.get("prerelease", False),
            "draft": r.get("draft", False),
            "url": r.get("html_url", ""),
        })

    return releases


def main():
    if len(sys.argv) < 3:
        print("Usage: check_github.py <owner> <repo> [--limit N]", file=sys.stderr)
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    limit = DEFAULT_LIMIT

    for i, arg in enumerate(sys.argv[3:], start=3):
        if arg == "--limit" and i + 1 < len(sys.argv):
            try:
                limit = int(sys.argv[i + 1])
            except ValueError:
                print("--limit must be an integer", file=sys.stderr)
                sys.exit(1)

    releases = fetch_releases(owner, repo, limit)
    print(json.dumps(releases, indent=2))


if __name__ == "__main__":
    main()
