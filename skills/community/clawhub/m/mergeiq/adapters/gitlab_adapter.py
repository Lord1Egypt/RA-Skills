"""
GitLab MR Adapter

Maps GitLab Merge Request API responses to MRData for complexity scoring.

GitLab MR API: https://docs.gitlab.com/ee/api/merge_requests.html

Required fields from the MR object (GET /projects/:id/merge_requests/:iid):
    iid, title, description, labels[], diff_refs, changes_count

For richer scoring, also fetch:
    GET /projects/:id/merge_requests/:iid/diffs       -> file_paths
    GET /projects/:id/merge_requests/:iid/notes       -> discussions_count
    GET /projects/:id/merge_requests/:iid/approvals   -> reviewers_count

Usage:
    from adapters.gitlab_adapter import gitlab_mr_to_mrdata
    mr_data = gitlab_mr_to_mrdata(mr_dict, diffs=diffs_list, notes=notes_list)
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mr_complexity_service import MRData


def gitlab_mr_to_mrdata(
    mr: Dict[str, Any],
    diffs: Optional[List[Dict]] = None,
    notes: Optional[List[Dict]] = None,
    approvals: Optional[Dict] = None,
) -> MRData:
    """
    Convert a GitLab MR API dict to MRData.

    Args:
        mr:        Raw MR dict from GitLab API
        diffs:     Optional list of diff objects (from /merge_requests/:iid/diffs)
        notes:     Optional list of note objects (from /merge_requests/:iid/notes)
        approvals: Optional approvals dict (from /merge_requests/:iid/approvals)

    Returns:
        MRData ready for MRComplexityCalculator
    """
    # Size metrics — GitLab stores additions/deletions in diff_refs or changes
    # Prefer explicit fields if available (requires ?include_diff_stats=true)
    additions = mr.get("additions") or 0
    deletions = mr.get("deletions") or 0
    files_changed = _parse_int(mr.get("changes_count")) or 0

    # File paths from diffs endpoint
    file_paths: List[str] = []
    if diffs:
        file_paths = [d.get("new_path", d.get("old_path", "")) for d in diffs if d]

    # Labels
    labels: List[str] = [lbl if isinstance(lbl, str) else lbl.get("name", "")
                          for lbl in (mr.get("labels") or [])]

    # Commit messages — GitLab doesn't return these in the MR object directly;
    # pass them separately if needed. Derive breaking-change hints from description.
    description = mr.get("description") or ""

    # Review metrics
    reviewers_count = 0
    if approvals:
        # approved_by is a list of {user: {...}}
        reviewers_count = len(approvals.get("approved_by") or [])
        if reviewers_count == 0:
            # Fall back to suggested_approvers count
            reviewers_count = len(approvals.get("suggested_approvers") or [])
    if reviewers_count == 0:
        # Last resort: count reviewers listed on the MR
        reviewers_count = len(mr.get("reviewers") or [])

    discussions_count = 0
    if notes:
        # Only count non-system notes as discussion threads
        discussions_count = sum(1 for n in notes if not n.get("system", False))

    # Review iterations: count unique approvals/changes-requested cycles
    review_iterations = 0
    if approvals:
        review_iterations = len(approvals.get("approved_by") or [])

    # Time to first approval (hours)
    hours_to_approval: Optional[float] = None
    created_at = _parse_dt(mr.get("created_at"))
    merged_at = _parse_dt(mr.get("merged_at"))
    if created_at and merged_at:
        hours_to_approval = (merged_at - created_at).total_seconds() / 3600

    # Linked issues from description (GitLab "Closes #123" syntax)
    linked_issues = _extract_linked_issues(description)

    return MRData(
        iid=mr.get("iid", 0),
        title=mr.get("title", ""),
        description=description,
        additions=additions,
        deletions=deletions,
        files_changed=files_changed,
        file_paths=file_paths,
        labels=labels,
        commit_messages=[],  # fetch separately if needed
        reviewers_count=reviewers_count,
        discussions_count=discussions_count,
        review_iterations=review_iterations,
        hours_to_approval=hours_to_approval,
        linked_issues=linked_issues,
    )


def _parse_int(val: Any) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0


def _parse_dt(val: Optional[str]) -> Optional[datetime]:
    if not val:
        return None
    try:
        return datetime.fromisoformat(val.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _extract_linked_issues(text: str) -> List[str]:
    """Extract issue references from GitLab description (Closes #123, !456)."""
    import re
    return re.findall(r'(?:Closes|Fixes|Resolves|Related to)\s+[#!](\d+)', text, re.IGNORECASE)
