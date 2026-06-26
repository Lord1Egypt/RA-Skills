"""
GitHub PR Adapter

Maps GitHub Pull Request API responses to MRData for complexity scoring.

GitHub PR API: https://docs.github.com/en/rest/pulls/pulls

Required field from the PR object (GET /repos/:owner/:repo/pulls/:number):
    number, title, body, additions, deletions, changed_files,
    requested_reviewers[], labels[]

For richer scoring, also fetch:
    GET /repos/:owner/:repo/pulls/:number/files    -> file_paths
    GET /repos/:owner/:repo/pulls/:number/commits  -> commit_messages
    GET /repos/:owner/:repo/pulls/:number/reviews  -> reviewers_count, review_iterations

Usage:
    from adapters.github_adapter import github_pr_to_mrdata
    mr_data = github_pr_to_mrdata(pr_dict, files=files_list, reviews=reviews_list)
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional

import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mr_complexity_service import MRData


def github_pr_to_mrdata(
    pr: Dict[str, Any],
    files: Optional[List[Dict]] = None,
    commits: Optional[List[Dict]] = None,
    reviews: Optional[List[Dict]] = None,
    review_comments: Optional[List[Dict]] = None,
) -> MRData:
    """
    Convert a GitHub PR API dict to MRData.

    Args:
        pr:              Raw PR dict from GitHub REST API
        files:           Optional list of file objects (from /pulls/:number/files)
                         Each item: {filename, additions, deletions, status, patch}
        commits:         Optional list of commit objects (from /pulls/:number/commits)
                         Each item: {commit: {message: str}}
        reviews:         Optional list of review objects (from /pulls/:number/reviews)
                         Each item: {state: APPROVED|CHANGES_REQUESTED|COMMENTED, user: {...}}
        review_comments: Optional list of inline comment objects
                         (from /pulls/:number/comments)

    Returns:
        MRData ready for MRComplexityCalculator
    """
    # Size metrics — GitHub provides these directly on the PR object
    additions: int = pr.get("additions") or 0
    deletions: int = pr.get("deletions") or 0
    files_changed: int = pr.get("changed_files") or 0

    # File paths from files endpoint
    file_paths: List[str] = []
    if files:
        file_paths = [f.get("filename", "") for f in files if f]

    # Labels
    labels: List[str] = [lbl.get("name", "") for lbl in (pr.get("labels") or [])]

    # Commit messages from commits endpoint
    commit_messages: List[str] = []
    if commits:
        commit_messages = [
            c.get("commit", {}).get("message", "").split("\n")[0]  # first line only
            for c in commits
            if c.get("commit", {}).get("message")
        ]

    description = pr.get("body") or ""

    # Review metrics
    # Unique reviewers who left any review (approved, requested changes, commented)
    reviewers_count = 0
    review_iterations = 0
    if reviews:
        unique_reviewers = {r["user"]["login"] for r in reviews if r.get("user")}
        reviewers_count = len(unique_reviewers)
        # Count approval rounds: how many APPROVED + CHANGES_REQUESTED reviews
        substantive = [r for r in reviews if r.get("state") in ("APPROVED", "CHANGES_REQUESTED")]
        review_iterations = len(substantive)
    else:
        # Fall back to requested_reviewers count on the PR object
        reviewers_count = len(pr.get("requested_reviewers") or [])

    # Discussion count: inline review comments + PR-level comments
    discussions_count = pr.get("review_comments", 0) + pr.get("comments", 0)
    if review_comments:
        # Use actual fetched comments if available (more accurate)
        discussions_count = len(review_comments)

    # Time to merge (hours) — proxy for time-to-approval
    hours_to_approval: Optional[float] = None
    created_at = _parse_dt(pr.get("created_at"))
    merged_at = _parse_dt(pr.get("merged_at"))
    if created_at and merged_at:
        hours_to_approval = (merged_at - created_at).total_seconds() / 3600

    # Linked issues from body (GitHub "Closes #123", "Fixes #456")
    linked_issues = _extract_linked_issues(description)

    return MRData(
        iid=pr.get("number", 0),
        title=pr.get("title", ""),
        description=description,
        additions=additions,
        deletions=deletions,
        files_changed=files_changed,
        file_paths=file_paths,
        labels=labels,
        commit_messages=commit_messages,
        reviewers_count=reviewers_count,
        discussions_count=discussions_count,
        review_iterations=review_iterations,
        hours_to_approval=hours_to_approval,
        linked_issues=linked_issues,
    )


def _parse_dt(val: Optional[str]) -> Optional[datetime]:
    if not val:
        return None
    try:
        return datetime.fromisoformat(val.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _extract_linked_issues(text: str) -> List[str]:
    """Extract issue references from GitHub PR body (Closes #123, Fixes #456)."""
    return re.findall(
        r'(?:Closes|Fixes|Resolves|Related to)\s+#(\d+)',
        text,
        re.IGNORECASE
    )
