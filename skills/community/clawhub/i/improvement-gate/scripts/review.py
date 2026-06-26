#!/usr/bin/env python3
"""CLI for completing pending human reviews.

Usage:
  python3 review.py --state-root /path/to/state --list
  python3 review.py --state-root /path/to/state --complete REQ_ID --decision approve
  python3 review.py --state-root /path/to/state --complete REQ_ID --decision reject --reason "..."
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import read_json, utc_now_iso, write_json
from lib.state_machine import DEFAULT_STATE_ROOT, ensure_tree


def _reviews_dir(state_root: Path) -> Path:
    return state_root / "state" / "reviews"


def list_pending(state_root: Path) -> list[dict]:
    """Return all pending review requests from the state directory."""
    reviews_dir = _reviews_dir(state_root)
    if not reviews_dir.exists():
        return []
    pending = []
    for path in sorted(reviews_dir.glob("review-*.json")):
        data = read_json(path)
        if data.get("status") == "pending":
            data["_path"] = str(path)
            pending.append(data)
    return pending


def complete_review(
    state_root: Path,
    request_id: str,
    decision: str,
    reviewer: str = "cli-user",
    reason: str = "",
) -> dict:
    """Mark a pending review as completed.

    Args:
        state_root: Root of the state directory.
        request_id: The review request ID (e.g. review-cand-001).
        decision: One of 'approve' or 'reject'.
        reviewer: Who completed the review.
        reason: Optional reason (especially for rejections).

    Returns:
        The updated review request dict.

    Raises:
        FileNotFoundError: If the review request file doesn't exist.
        ValueError: If the review is already completed or decision is invalid.
    """
    if decision not in ("approve", "reject"):
        raise ValueError(f"Decision must be 'approve' or 'reject', got: {decision!r}")

    reviews_dir = _reviews_dir(state_root)
    review_path = reviews_dir / f"{request_id}.json"
    if not review_path.exists():
        raise FileNotFoundError(f"Review request not found: {review_path}")

    data = read_json(review_path)
    if data.get("status") == "completed":
        raise ValueError(f"Review {request_id} is already completed (decision: {data.get('decision')})")

    data["status"] = "completed"
    data["decision"] = decision
    data["reviewer"] = reviewer
    data["comments"] = reason
    data["completed_at"] = utc_now_iso()
    write_json(review_path, data)
    return data


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="CLI for completing pending human reviews",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--state-root", default=str(DEFAULT_STATE_ROOT), help="State directory root")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true", dest="list_pending", help="List pending reviews")
    group.add_argument("--complete", metavar="REQ_ID", help="Complete a pending review")

    parser.add_argument("--decision", choices=["approve", "reject"], help="Review decision (required with --complete)")
    parser.add_argument("--reason", default="", help="Reason for decision")
    parser.add_argument("--reviewer", default="cli-user", help="Reviewer name/id")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    state_root = Path(args.state_root).expanduser().resolve()
    ensure_tree(state_root)

    if args.list_pending:
        pending = list_pending(state_root)
        if not pending:
            print("No pending reviews.")
            return 0
        print(f"Pending reviews ({len(pending)}):\n")
        for review in pending:
            print(f"  ID:       {review.get('request_id', '?')}")
            print(f"  Category: {review.get('category', '?')}")
            print(f"  Risk:     {review.get('risk_level', '?')}")
            print(f"  Title:    {review.get('title', '(no title)')}")
            if review.get("description"):
                print(f"  Desc:     {review['description'][:80]}")
            print(f"  Since:    {review.get('requested_at', '?')}")
            print()
        return 0

    if args.complete:
        if not args.decision:
            print("ERROR: --decision is required with --complete", file=sys.stderr)
            return 1
        try:
            result = complete_review(
                state_root,
                args.complete,
                args.decision,
                reviewer=args.reviewer,
                reason=args.reason,
            )
            print(f"Review {args.complete} completed: {result['decision']}")
            return 0
        except (FileNotFoundError, ValueError) as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
