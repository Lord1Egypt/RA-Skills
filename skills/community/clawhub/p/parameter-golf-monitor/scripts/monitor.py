#!/usr/bin/env python3
"""Parameter Golf PR Monitor — track competition leaderboard from GitHub PRs.

Usage:
    python monitor.py                      # one-shot leaderboard (valid only)
    python monitor.py --include-suspect    # include suspicious/non-standard submissions
    python monitor.py --watch 5            # poll every 5 minutes
    python monitor.py --merged             # show merged records only
    python monitor.py --all                # show both open and merged
    python monitor.py --json               # JSON output for piping
    python monitor.py --since 2026-03-19   # filter by date
    python monitor.py --me dexhunter       # highlight your PRs
    python monitor.py --top 10             # show only top N scored entries
    python monitor.py --records-only       # exclude non-record submissions
"""

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime

API_BASE = "https://api.github.com/repos/openai/parameter-golf"
BPB_PATTERN = re.compile(r"val_bpb[=:\s]*(\d+\.\d+)")
SCORE_IN_TITLE = re.compile(r"(\d+\.\d{3,})")

# Scores below this are almost certainly non-standard (val-only training, paid prefix, etc.)
# No legitimate standard training submission has achieved below 1.10 as of 2026-03-20.
SUSPECT_SCORE_THRESHOLD = 1.10

# Keywords in title/body that indicate non-standard training conditions
SUSPECT_KEYWORDS = [
    "val-only", "val_only", "validation-only", "validation only",
    "paid prefix", "paid-prefix",
    "train on val", "train on validation",
    "val-only training",
]


def fetch_prs(state="open", per_page=100):
    """Fetch PRs from GitHub API (unauthenticated, 60 req/hr)."""
    url = f"{API_BASE}/pulls?state={state}&per_page={per_page}&sort=created&direction=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "parameter-golf-monitor"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def extract_score(pr):
    """Extract val_bpb score from PR title or body."""
    title = pr.get("title", "")

    # Try explicit val_bpb pattern first
    m = BPB_PATTERN.search(title)
    if m:
        return float(m.group(1))

    # Try body
    body = pr.get("body", "") or ""
    m = BPB_PATTERN.search(body[:2000])
    if m:
        return float(m.group(1))

    # Fallback: any decimal in title that looks like a bpb score (1.xxx)
    for m in SCORE_IN_TITLE.finditer(title):
        val = float(m.group(1))
        if 1.0 < val < 2.0:
            return val

    return None


def is_suspect(pr, score, threshold=SUSPECT_SCORE_THRESHOLD):
    """Check if a submission likely uses non-standard training (val-only, paid prefix, etc.)."""
    # Score too low to be standard training
    if score is not None and score < threshold:
        return True

    # Only check title for suspect keywords (body may mention val-only as an aside)
    title = pr.get("title", "").lower()
    for keyword in SUSPECT_KEYWORDS:
        if keyword in title:
            return True

    return False


def classify_pr(pr):
    """Classify PR as record, non-record, or other."""
    title = pr.get("title", "").lower()
    labels = [l["name"].lower() for l in pr.get("labels", [])]

    if "non-record" in title or "non-record" in labels:
        return "non-record"
    if "record" in title or "record" in labels:
        return "record"
    return "other"


def format_leaderboard(prs, show_all_types=False, since=None, records_only=False,
                       include_suspect=False, suspect_threshold=SUSPECT_SCORE_THRESHOLD):
    """Format PRs into a sorted leaderboard."""
    entries = []
    suspect_count = 0

    for pr in prs:
        score = extract_score(pr)
        created = pr["created_at"][:10]

        if since and created < since:
            continue

        category = classify_pr(pr)
        if records_only and category == "non-record":
            continue
        if not show_all_types and not records_only and category == "other":
            continue

        suspect = is_suspect(pr, score, suspect_threshold)
        if suspect:
            suspect_count += 1
            if not include_suspect:
                continue

        state = pr.get("state", "open")
        merged = pr.get("merged_at") is not None
        status = "merged" if merged else state

        entries.append({
            "number": pr["number"],
            "title": pr["title"][:75],
            "score": score,
            "author": pr["user"]["login"],
            "date": created,
            "category": category,
            "status": status,
            "suspect": suspect,
        })

    # Sort: scored entries first (ascending bpb = better), then unscored
    entries.sort(key=lambda e: (e["score"] is None, e["score"] or 99))
    return entries, suspect_count


def print_table(entries, highlight_user=None, top_n=None, suspect_count=0):
    """Print a formatted leaderboard table."""
    if not entries:
        print("No matching PRs found.")
        return

    print()
    header = f"{'Rank':>4}  {'val_bpb':>8}  {'PR':>5}  {'Status':<8}  {'Author':<18}  {'Date':<10}  Title"
    print(header)
    print("-" * len(header) + "-" * 30)

    rank = 0
    shown = 0
    user_entry = None
    user_rank = None

    for e in entries:
        if e["score"] is not None:
            rank += 1
            score_str = f"{e['score']:.5f}"
            rank_str = f"{rank}"
        else:
            score_str = "    ?   "
            rank_str = " -"

        is_me = highlight_user and e["author"].lower() == highlight_user.lower()
        if is_me:
            user_entry = e
            user_rank = rank if e["score"] is not None else None

        # Apply --top filter (but always show highlighted user)
        if top_n and shown >= top_n and not is_me:
            if e["score"] is not None:
                continue
            else:
                break

        status_str = e["status"]
        if e["category"] == "non-record":
            status_str = "non-rec"

        marker = " <--" if is_me else ""
        suspect_marker = " [!]" if e.get("suspect") else ""
        print(
            f"{rank_str:>4}  {score_str:>8}  #{e['number']:<4}  {status_str:<8}  "
            f"{e['author']:<18}  {e['date']}  {e['title']}{marker}{suspect_marker}"
        )
        shown += 1

    # Summary
    scored = [e for e in entries if e["score"] is not None]
    if scored:
        best = min(scored, key=lambda e: e["score"])
        print(f"\nBest: val_bpb={best['score']:.5f} (#{best['number']} by {best['author']})")
        print(f"Total: {len(entries)} PRs, {len(scored)} with scores")

    if suspect_count > 0:
        has_suspect_in_list = any(e.get("suspect") for e in entries)
        if has_suspect_in_list:
            print(f"[!] = suspect (non-standard training, val-only, or score < {SUSPECT_SCORE_THRESHOLD})")
        else:
            print(f"({suspect_count} suspect submission{'s' if suspect_count != 1 else ''} hidden — use --include-suspect to show)")

    if user_entry and user_rank:
        gap = user_entry["score"] - best["score"]
        print(f"\nYou ({highlight_user}): rank #{user_rank}, val_bpb={user_entry['score']:.5f}, gap to #1: {gap:+.5f}")


def print_json(entries):
    """Print entries as JSON."""
    print(json.dumps(entries, indent=2))


def run_once(args):
    """Single fetch and display."""
    all_prs = []

    if args.merged or args.all:
        closed = fetch_prs(state="closed", per_page=100)
        merged = [pr for pr in closed if pr.get("merged_at")]
        all_prs.extend(merged)

    if not args.merged or args.all:
        open_prs = fetch_prs(state="open", per_page=100)
        all_prs.extend(open_prs)

    entries, suspect_count = format_leaderboard(
        all_prs,
        show_all_types=args.all,
        since=args.since,
        records_only=args.records_only,
        include_suspect=args.include_suspect,
        suspect_threshold=args.suspect_threshold,
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if args.json:
        print_json(entries)
    else:
        mode = "open+merged" if args.all else ("merged" if args.merged else "open")
        print(f"[{timestamp}] Parameter Golf Leaderboard ({mode} PRs)")
        print_table(entries, highlight_user=args.me, top_n=args.top,
                    suspect_count=suspect_count)


def main():
    parser = argparse.ArgumentParser(
        description="Parameter Golf PR Monitor — track the openai/parameter-golf competition leaderboard"
    )
    parser.add_argument("--watch", type=int, metavar="MIN", help="Poll every N minutes")
    parser.add_argument("--merged", action="store_true", help="Show merged PRs only")
    parser.add_argument("--all", action="store_true", help="Show both open and merged")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--since", type=str, help="Filter PRs created after date (YYYY-MM-DD)")
    parser.add_argument("--me", type=str, metavar="USER", help="Highlight your GitHub username (e.g. --me dexhunter)")
    parser.add_argument("--top", type=int, metavar="N", help="Show only top N scored entries")
    parser.add_argument("--records-only", action="store_true", help="Exclude non-record submissions")
    parser.add_argument("--include-suspect", action="store_true",
                        help="Include suspect submissions (val-only, paid prefix, or score below threshold)")
    parser.add_argument("--suspect-threshold", type=float, default=SUSPECT_SCORE_THRESHOLD, metavar="BPB",
                        help=f"Score below this is flagged as suspect (default: {SUSPECT_SCORE_THRESHOLD})")
    args = parser.parse_args()

    if args.watch:
        print(f"Watching Parameter Golf PRs every {args.watch} minutes (Ctrl+C to stop)\n")
        while True:
            try:
                run_once(args)
                print(f"\n--- Next refresh in {args.watch} min ---\n")
                time.sleep(args.watch * 60)
            except KeyboardInterrupt:
                print("\nStopped.")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e} (retrying in {args.watch} min)")
                time.sleep(args.watch * 60)
    else:
        run_once(args)


if __name__ == "__main__":
    main()
