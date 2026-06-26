#!/usr/bin/env python3
"""Generate changelogs from git history with conventional commit support.

Usage:
    changelog_gen.py [--repo PATH] [--since TAG_OR_DATE] [--until TAG_OR_DATE] [--format md|json] [--group]
    changelog_gen.py --help

Examples:
    changelog_gen.py
    changelog_gen.py --repo /path/to/repo --since v1.0.0 --group
    changelog_gen.py --since "2026-01-01" --format json
    changelog_gen.py --since v1.0.0 --until v2.0.0
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime


CONVENTIONAL_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"           # type: feat, fix, docs, etc.
    r"(?:\((?P<scope>[^)]+)\))?"   # optional scope: (api), (ui)
    r"(?P<breaking>!)?"            # optional breaking: !
    r":\s*"                         # colon separator
    r"(?P<description>.+)$",       # description
    re.IGNORECASE,
)

TYPE_LABELS = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "docs": "Documentation",
    "style": "Styles",
    "refactor": "Refactoring",
    "perf": "Performance",
    "test": "Tests",
    "build": "Build",
    "ci": "CI/CD",
    "chore": "Chores",
    "revert": "Reverts",
}

TYPE_ORDER = list(TYPE_LABELS.keys())


@dataclass
class Commit:
    hash: str
    short_hash: str
    author: str
    date: str
    subject: str
    commit_type: str | None = None
    scope: str | None = None
    description: str | None = None
    breaking: bool = False
    body: str = ""


def run_git(args: list[str], cwd: str | None = None) -> str:
    """Run a git command and return stdout."""
    cmd = ["git"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=30)
        if result.returncode != 0:
            error_msg = result.stderr.strip() or f"git command failed with exit code {result.returncode}"
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
        return result.stdout.strip()
    except FileNotFoundError:
        print("Error: git not found in PATH", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: git command timed out", file=sys.stderr)
        sys.exit(1)


def parse_commit(raw: str) -> Commit | None:
    """Parse a git log entry into a Commit object."""
    lines = raw.strip().split("\n")
    if len(lines) < 4:
        return None

    commit_hash = lines[0]
    short_hash = lines[1]
    author = lines[2]
    date = lines[3]
    subject = lines[4] if len(lines) > 4 else ""
    body = "\n".join(lines[5:]).strip() if len(lines) > 5 else ""

    commit = Commit(
        hash=commit_hash,
        short_hash=short_hash,
        author=author,
        date=date,
        subject=subject,
        body=body,
    )

    # Parse conventional commit
    match = CONVENTIONAL_PATTERN.match(subject)
    if match:
        commit.commit_type = match.group("type").lower()
        commit.scope = match.group("scope")
        commit.description = match.group("description").strip()
        commit.breaking = bool(match.group("breaking"))

    # Check body for BREAKING CHANGE
    if "BREAKING CHANGE" in body or "BREAKING-CHANGE" in body:
        commit.breaking = True

    return commit


def get_commits(repo: str, since: str | None = None, until: str | None = None) -> list[Commit]:
    """Get commits from git log."""
    # Format: hash, short_hash, author, date, subject, body (separated by record separator)
    log_format = "%H%n%h%n%an%n%Y-%m-%d%n%s%n%b%x1e"

    args = ["log", f"--format={log_format}"]

    if since and until:
        args.append(f"{since}..{until}")
    elif since:
        args.append(f"{since}..HEAD")

    raw = run_git(args, cwd=repo)
    if not raw:
        return []

    entries = raw.split("\x1e")
    commits = []
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        commit = parse_commit(entry)
        if commit:
            commits.append(commit)

    return commits


def group_commits(commits: list[Commit]) -> dict[str, list[Commit]]:
    """Group commits by conventional commit type."""
    groups = defaultdict(list)
    for commit in commits:
        if commit.commit_type:
            groups[commit.commit_type].append(commit)
        else:
            groups["other"].append(commit)
    return dict(groups)


def format_markdown(commits: list[Commit], grouped: bool = False, since: str | None = None, until: str | None = None) -> str:
    """Format commits as a markdown changelog."""
    lines = []

    # Header
    today = datetime.now().strftime("%Y-%m-%d")
    title = "Changelog"
    if until:
        title = f"{until}"
    elif since:
        title = f"Changes since {since}"
    lines.append(f"# {title}")
    lines.append(f"*Generated {today}*\n")

    # Breaking changes first
    breaking = [c for c in commits if c.breaking]
    if breaking:
        lines.append("## BREAKING CHANGES\n")
        for c in breaking:
            desc = c.description or c.subject
            scope = f"**{c.scope}:** " if c.scope else ""
            lines.append(f"- {scope}{desc} ({c.short_hash})")
        lines.append("")

    if grouped:
        groups = group_commits(commits)
        # Sort by TYPE_ORDER
        for type_key in TYPE_ORDER + ["other"]:
            if type_key not in groups:
                continue
            label = TYPE_LABELS.get(type_key, "Other")
            lines.append(f"## {label}\n")
            for c in groups[type_key]:
                desc = c.description or c.subject
                scope = f"**{c.scope}:** " if c.scope else ""
                lines.append(f"- {scope}{desc} ({c.short_hash})")
            lines.append("")
    else:
        lines.append("## Commits\n")
        for c in commits:
            prefix = ""
            if c.commit_type:
                prefix = f"**{c.commit_type}:** "
                if c.scope:
                    prefix = f"**{c.commit_type}({c.scope}):** "
            desc = c.description or c.subject
            lines.append(f"- {prefix}{desc} ({c.short_hash}) — {c.author}, {c.date}")
        lines.append("")

    # Stats
    lines.append(f"---\n*{len(commits)} commits")
    authors = set(c.author for c in commits)
    lines.append(f"from {len(authors)} contributor(s)*")

    return "\n".join(lines)


def format_json(commits: list[Commit], grouped: bool = False) -> str:
    """Format commits as JSON."""
    data = {
        "generated": datetime.now().isoformat(),
        "total_commits": len(commits),
        "authors": sorted(set(c.author for c in commits)),
        "breaking_changes": [asdict(c) for c in commits if c.breaking],
    }
    if grouped:
        groups = group_commits(commits)
        data["groups"] = {k: [asdict(c) for c in v] for k, v in groups.items()}
    else:
        data["commits"] = [asdict(c) for c in commits]

    return json.dumps(data, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Generate changelogs from git commit history with conventional commit support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  %(prog)s\n"
               "  %(prog)s --repo /path/to/repo --since v1.0.0 --group\n"
               "  %(prog)s --since '2026-01-01' --format json\n"
               "  %(prog)s --since v1.0.0 --until v2.0.0\n",
    )
    parser.add_argument("--repo", type=str, default=".", help="Path to git repository (default: current directory)")
    parser.add_argument("--since", type=str, default=None, help="Start point — tag name or commit ref (e.g. v1.0.0)")
    parser.add_argument("--until", type=str, default=None, help="End point — tag name or commit ref")
    parser.add_argument("--format", type=str, choices=["md", "json"], default="md", help="Output format (default: md)")
    parser.add_argument("--group", action="store_true", help="Group commits by conventional commit type")
    parser.add_argument("--output", "-o", type=str, default=None, help="Write output to file instead of stdout")

    args = parser.parse_args()

    # Verify it's a git repo
    repo = os.path.abspath(args.repo)
    run_git(["rev-parse", "--git-dir"], cwd=repo)

    commits = get_commits(repo, since=args.since, until=args.until)

    if not commits:
        print("No commits found in the specified range.", file=sys.stderr)
        sys.exit(0)

    if args.format == "json":
        output = format_json(commits, grouped=args.group)
    else:
        output = format_markdown(commits, grouped=args.group, since=args.since, until=args.until)

    if args.output:
        Path_obj = __import__("pathlib").Path(args.output)
        Path_obj.write_text(output)
        print(f"Changelog written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
