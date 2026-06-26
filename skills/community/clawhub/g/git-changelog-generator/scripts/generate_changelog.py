#!/usr/bin/env python3
"""Generate structured changelogs from git history."""

import subprocess
import re
import json
import argparse
from datetime import datetime
from collections import defaultdict

COMMIT_TYPES = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "refactor": "Code Refactoring",
    "docs": "Documentation",
    "test": "Tests",
    "perf": "Performance",
    "ci": "CI/CD",
    "chore": "Maintenance",
    "style": "Style",
    "build": "Build",
}

def git(cmd, repo="."):
    result = subprocess.run(
        ["git", "-C", repo] + cmd,
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()

def get_last_tag(repo):
    return git(["describe", "--tags", "--abbrev=0"], repo) or None

def get_commits(repo, from_ref=None, to_ref="HEAD", last=None, since=None):
    cmd = ["log", "--format=%H|%s|%an|%aI"]
    if last:
        cmd.append(f"-{last}")
    elif since:
        cmd.append(f"--since={since}")
    elif from_ref:
        cmd.append(f"{from_ref}..{to_ref}")
    else:
        cmd.append(to_ref)

    output = git(cmd, repo)
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0][:8],
                "message": parts[1],
                "author": parts[2],
                "date": parts[3][:10],
            })
    return commits

def categorize(commits):
    groups = defaultdict(list)
    breaking = []

    for c in commits:
        msg = c["message"]
        if "BREAKING CHANGE" in msg or msg.startswith("!"):
            breaking.append(c)

        matched = False
        for prefix, label in COMMIT_TYPES.items():
            pattern = rf'^{prefix}(?:\(.+?\))?!?:\s*(.+)'
            m = re.match(pattern, msg)
            if m:
                c["clean_message"] = m.group(1)
                scope_m = re.search(rf'^{prefix}\((.+?)\)', msg)
                c["scope"] = scope_m.group(1) if scope_m else None
                groups[label].append(c)
                matched = True
                break

        if not matched:
            c["clean_message"] = msg
            c["scope"] = None
            groups["Other Changes"].append(c)

    return dict(groups), breaking

def format_markdown(groups, breaking, args):
    lines = []
    version = args.to if args.to != "HEAD" else "Unreleased"
    lines.append(f"# {version} ({datetime.now().strftime('%Y-%m-%d')})\n")

    if breaking:
        lines.append("## Breaking Changes\n")
        for c in breaking:
            lines.append(f"- {c['clean_message']}")
            if args.include_hashes:
                lines[-1] += f" ({c['hash']})"
        lines.append("")

    order = list(COMMIT_TYPES.values()) + ["Other Changes"]
    for category in order:
        if category not in groups:
            continue
        lines.append(f"## {category}\n")
        for c in groups[category]:
            prefix = f"**{c['scope']}**: " if c.get("scope") else ""
            entry = f"- {prefix}{c['clean_message']}"
            if args.include_authors:
                entry += f" (@{c['author']})"
            if args.include_hashes:
                entry += f" ({c['hash']})"
            lines.append(entry)
        lines.append("")

    return "\n".join(lines)

def format_json(groups, breaking, args):
    return json.dumps({"version": args.to, "date": datetime.now().isoformat(),
                        "breaking_changes": breaking, "categories": groups}, indent=2, default=str)

def main():
    p = argparse.ArgumentParser(description="Generate changelog from git history")
    p.add_argument("--from", dest="from_ref", help="Start tag/commit")
    p.add_argument("--to", default="HEAD", help="End tag/commit")
    p.add_argument("--last", type=int, help="Last N commits")
    p.add_argument("--since", help="Start date (YYYY-MM-DD)")
    p.add_argument("--format", default="markdown", choices=["markdown", "keepachangelog", "github-release", "json"])
    p.add_argument("--output", help="Output file path")
    p.add_argument("--repo", default=".", help="Repository path")
    p.add_argument("--include-authors", action="store_true")
    p.add_argument("--include-hashes", action="store_true")
    p.add_argument("--group-by", default="type", choices=["type", "scope"])
    args = p.parse_args()

    from_ref = args.from_ref or get_last_tag(args.repo)
    commits = get_commits(args.repo, from_ref, args.to, args.last, args.since)

    if not commits:
        print("No commits found in the specified range.")
        return

    groups, breaking = categorize(commits)

    if args.format == "json":
        output = format_json(groups, breaking, args)
    else:
        output = format_markdown(groups, breaking, args)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Changelog written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
