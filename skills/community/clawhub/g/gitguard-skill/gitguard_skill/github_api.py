"""
Minimal GitHub REST API v3 client for PR/issue triage.

Only reads data the authenticated user (or public API for public repos)
already has access to. No write operations are performed by this module.
A personal access token is optional -- without one, requests fall back to
unauthenticated calls which are rate-limited by GitHub (60/hour) but work
fine for occasional checks on public repos.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

from .models import IssueInfo, PullRequestInfo

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

API_BASE = "https://api.github.com"


def _headers() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _days_since(iso_date: str) -> int:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def get_open_pull_requests(owner: str, repo: str, stale_days: int = 14,
                            timeout: float = 8.0) -> list[PullRequestInfo]:
    if not HAS_REQUESTS:
        return []
    try:
        r = requests.get(
            f"{API_BASE}/repos/{owner}/{repo}/pulls",
            params={"state": "open", "per_page": 50},
            headers=_headers(), timeout=timeout,
        )
        if r.status_code != 200:
            return []
        data = r.json()
    except requests.RequestException:
        return []

    results = []
    for pr in data:
        days_open = _days_since(pr["created_at"])
        results.append(PullRequestInfo(
            number=pr["number"],
            title=pr["title"],
            author=pr.get("user", {}).get("login", "unknown"),
            days_open=days_open,
            is_stale=days_open >= stale_days,
            review_status="draft" if pr.get("draft") else "open",
            url=pr["html_url"],
        ))
    return results


def get_open_issues(owner: str, repo: str, stale_days: int = 30,
                     timeout: float = 8.0) -> list[IssueInfo]:
    if not HAS_REQUESTS:
        return []
    try:
        r = requests.get(
            f"{API_BASE}/repos/{owner}/{repo}/issues",
            params={"state": "open", "per_page": 50},
            headers=_headers(), timeout=timeout,
        )
        if r.status_code != 200:
            return []
        data = r.json()
    except requests.RequestException:
        return []

    results = []
    for issue in data:
        if "pull_request" in issue:
            continue  # GitHub's issues endpoint also returns PRs; skip them
        days_open = _days_since(issue["created_at"])
        results.append(IssueInfo(
            number=issue["number"],
            title=issue["title"],
            labels=[l["name"] for l in issue.get("labels", [])],
            days_open=days_open,
            is_stale=days_open >= stale_days,
            url=issue["html_url"],
        ))
    return results
