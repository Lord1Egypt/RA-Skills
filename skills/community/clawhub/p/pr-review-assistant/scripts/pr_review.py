#!/usr/bin/env python3
"""Collect PR/diff data for AI-powered code review."""

import subprocess
import argparse
import json
import sys

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.stdout.strip(), r.returncode

def get_diff(base="main", staged=False):
    if staged:
        diff, _ = run(["git", "diff", "--staged"])
    else:
        diff, _ = run(["git", "diff", f"{base}...HEAD"])
    return diff

def get_pr_diff(pr_number):
    diff, rc = run(["gh", "pr", "diff", str(pr_number)])
    if rc != 0:
        print(f"Error: could not fetch PR #{pr_number}. Is `gh` authenticated?", file=sys.stderr)
        sys.exit(1)
    return diff

def get_changed_files(base="main"):
    out, _ = run(["git", "diff", "--name-only", f"{base}...HEAD"])
    return out.split("\n") if out else []

def parse_diff_stats(diff):
    additions = diff.count("\n+") - diff.count("\n+++")
    deletions = diff.count("\n-") - diff.count("\n---")
    files = [l.split(" b/", 1)[1] for l in diff.split("\n") if l.startswith("diff --git")]
    return {"files_changed": len(files), "additions": additions, "deletions": deletions, "files": files}

def main():
    p = argparse.ArgumentParser(description="Collect diff data for PR review")
    p.add_argument("--pr", type=int, help="GitHub PR number")
    p.add_argument("--base", default="main", help="Base branch")
    p.add_argument("--staged", action="store_true", help="Review staged changes")
    p.add_argument("--focus", help="Comma-separated focus areas")
    p.add_argument("--format", default="markdown", choices=["markdown", "json", "github-comment"])
    p.add_argument("--max-files", type=int, default=50)
    args = p.parse_args()

    if args.pr:
        diff = get_pr_diff(args.pr)
    else:
        diff = get_diff(args.base, args.staged)

    if not diff:
        print("No changes found.")
        return

    stats = parse_diff_stats(diff)

    if stats["files_changed"] > args.max_files:
        print(f"Warning: {stats['files_changed']} files changed (limit: {args.max_files}). Truncating.")
        diff_lines = diff.split("\ndiff --git")
        diff = "\ndiff --git".join(diff_lines[:args.max_files + 1])

    review_data = {
        "stats": stats,
        "focus": args.focus.split(",") if args.focus else ["correctness", "security", "performance", "maintainability", "testing", "best-practices"],
        "diff": diff,
    }

    if args.format == "json":
        print(json.dumps(review_data, indent=2))
    else:
        print(f"## PR Review Data\n")
        print(f"- **Files changed:** {stats['files_changed']}")
        print(f"- **Additions:** +{stats['additions']}")
        print(f"- **Deletions:** -{stats['deletions']}")
        print(f"- **Focus areas:** {', '.join(review_data['focus'])}")
        print(f"\n### Changed Files\n")
        for f in stats["files"][:args.max_files]:
            print(f"- {f}")
        print(f"\n### Diff\n```diff\n{diff[:50000]}\n```")

if __name__ == "__main__":
    main()
