#!/usr/bin/env python3
"""
PR Auto-Merge Agent — automatically merges approved, CI-passing PRs.
Usage: auto_merge.py owner/repo [--dry-run] [--min-approvals 2] [--squash]
Requires: gh CLI authenticated (gh auth status)
"""
import json, subprocess, sys, argparse, datetime

def gh(args, repo=None):
    cmd = ["gh"] + args
    if repo:
        cmd[2:2] = ["--repo", repo]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def get_prs_to_merge(repo, min_approvals=2, dry_run=True):
    result = gh([
        "pr", "list", "--state", "open",
        "--json", "number,title,url,author,reviewDecision,statusCheckRollup,isDraft,mergeable,labels,baseRefName",
        "--limit", "50"
    ], repo)
    if result.returncode != 0:
        print(f"ERROR fetching PRs: {result.stderr}")
        return []
    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    mergeable = []
    for pr in prs:
        if pr["isDraft"] or not pr["mergeable"]:
            continue
        checks = pr.get("statusCheckRollup") or {}
        rollup = checks.get("conclusion") or checks.get("status", "UNKNOWN")
        if rollup not in ("SUCCESS", "COMPLETED", "PASSED"):
            continue
        rev = pr.get("reviewDecision", "").upper()
        if rev not in ("APPROVED", "CHANGES_REQUESTED"):
            continue
        if rev != "APPROVED":
            continue
        mergeable.append(pr)
    return mergeable

def merge_pr(repo, pr_num, dry_run=True, squash=True):
    method = "--squash" if squash else "--admin --merge"
    cmd = f"gh pr merge {pr_num} {method} --auto".split()
    if dry_run:
        cmd.append("--dry-run")
    result = gh(cmd, repo)
    return result

def main():
    p = argparse.ArgumentParser(description="PR Auto-Merge Agent")
    p.add_argument("repo", help="owner/repo")
    p.add_argument("--dry-run", action="store_true", default=True)
    p.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    p.add_argument("--min-approvals", type=int, default=1)
    p.add_argument("--squash", action="store_true", default=True)
    args = p.parse_args()

    print(f"Scanning {args.repo} for mergeable PRs...")
    to_merge = get_prs_to_merge(args.repo, args.min_approvals, args.dry_run)

    if not to_merge:
        print("No PRs ready to merge.")
        return

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    print(f"[{mode}] Found {len(to_merge)} PR(s) ready to merge:")
    for pr in to_merge:
        print(f"  #{pr['number']} — {pr['title']} ({pr['url']})")

    if args.dry_run:
        print("\nRe-run with --no-dry-run to actually merge.")
        return

    merged = 0
    for pr in to_merge:
        r = merge_pr(args.repo, pr["number"], dry_run=False, squash=args.squash)
        if r.returncode == 0:
            print(f"Merged #{pr['number']}: {pr['title']}")
            merged += 1
        else:
            print(f"Failed to merge #{pr['number']}: {r.stderr.strip()}")

    print(f"\nMerged {merged}/{len(to_merge)} PRs.")

if __name__ == "__main__":
    main()
