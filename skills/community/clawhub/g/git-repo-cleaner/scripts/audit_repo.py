#!/usr/bin/env python3
"""Git Repo Cleaner — audit and clean up Git repositories.

Find stale branches, large files, repo bloat, and generate cleanup scripts.
Pure Python stdlib — no external dependencies. Requires git CLI.

Usage:
    python3 audit_repo.py /path/to/repo
    python3 audit_repo.py /path/to/repo --check branches|large-files|stats|maintenance|all
    python3 audit_repo.py /path/to/repo --format json|markdown|text
    python3 audit_repo.py /path/to/repo --fix
"""

import sys
import os
import json
import subprocess
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta


def run_git(repo_path, *args, check=False):
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path)] + list(args),
            capture_output=True, text=True, timeout=30
        )
        if check and result.returncode != 0:
            return None
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def get_default_branch(repo_path):
    """Detect the default branch (main or master)."""
    # Check symbolic ref
    ref = run_git(repo_path, "symbolic-ref", "refs/remotes/origin/HEAD")
    if ref:
        return ref.split("/")[-1]

    # Fallback: check if main or master exists
    branches = run_git(repo_path, "branch", "--list", "main", "master")
    if branches:
        for b in branches.splitlines():
            name = b.strip().lstrip("* ")
            if name in ("main", "master"):
                return name

    return "main"


# ── Branch Audit ────────────────────────────────────────────────────────────

def audit_branches(repo_path, stale_days=30):
    """Find stale and merged branches."""
    default_branch = get_default_branch(repo_path)
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=stale_days)

    findings = {
        "default_branch": default_branch,
        "stale": [],
        "merged": [],
        "active": [],
        "total_branches": 0,
    }

    # Get all local branches with last commit date
    branch_output = run_git(
        repo_path, "for-each-ref",
        "--format=%(refname:short)|%(committerdate:iso8601)|%(authorname)|%(subject)",
        "refs/heads/"
    )
    if not branch_output:
        return findings

    for line in branch_output.splitlines():
        parts = line.split("|", 3)
        if len(parts) < 2:
            continue

        name = parts[0]
        date_str = parts[1].strip()
        author = parts[2] if len(parts) > 2 else "unknown"
        subject = parts[3] if len(parts) > 3 else ""

        findings["total_branches"] += 1

        if name == default_branch:
            continue

        # Parse date
        try:
            # Handle ISO format from git
            date_str_clean = re.sub(r'\s+[+-]\d{4}$', '', date_str)
            last_commit = datetime.strptime(date_str_clean, "%Y-%m-%d %H:%M:%S")
            last_commit = last_commit.replace(tzinfo=timezone.utc)
        except ValueError:
            last_commit = now

        days_old = (now - last_commit).days

        branch_info = {
            "name": name,
            "last_commit": date_str,
            "days_old": days_old,
            "author": author,
            "last_subject": subject,
        }

        # Check if merged
        merged_check = run_git(repo_path, "branch", "--merged", default_branch)
        is_merged = False
        if merged_check:
            merged_branches = [b.strip().lstrip("* ") for b in merged_check.splitlines()]
            is_merged = name in merged_branches

        if is_merged:
            branch_info["reason"] = "Already merged into " + default_branch
            findings["merged"].append(branch_info)
        elif days_old > stale_days:
            branch_info["reason"] = f"No commits in {days_old} days"
            findings["stale"].append(branch_info)
        else:
            findings["active"].append(branch_info)

    # Sort by age
    findings["stale"].sort(key=lambda x: x["days_old"], reverse=True)
    findings["merged"].sort(key=lambda x: x["days_old"], reverse=True)

    return findings


# ── Large Files ─────────────────────────────────────────────────────────────

def audit_large_files(repo_path, min_size_kb=1024):
    """Find large files in current tree and history."""
    findings = {
        "current_tree": [],
        "history": [],
        "min_size_kb": min_size_kb,
    }

    # Large files in current tree
    ls_output = run_git(repo_path, "ls-files", "-z")
    if ls_output:
        for filepath in ls_output.split("\0"):
            if not filepath:
                continue
            full_path = Path(repo_path) / filepath
            try:
                size = full_path.stat().st_size
                if size >= min_size_kb * 1024:
                    findings["current_tree"].append({
                        "path": filepath,
                        "size_bytes": size,
                        "size_human": format_size(size),
                    })
            except OSError:
                pass

    findings["current_tree"].sort(key=lambda x: x["size_bytes"], reverse=True)

    # Large blobs in history (top 20)
    # Use rev-list with disk-usage for efficiency
    verify_output = run_git(
        repo_path, "rev-list", "--objects", "--all"
    )
    if verify_output:
        # Get largest objects
        cat_batch = run_git(
            repo_path, "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)",
            check=True
        )
        # Fallback: use verify-pack if available
        pack_dir = Path(repo_path) / ".git" / "objects" / "pack"
        if pack_dir.is_dir():
            for pack_idx in pack_dir.glob("*.idx"):
                pack_output = run_git(
                    repo_path, "verify-pack", "-v", str(pack_idx)
                )
                if pack_output:
                    blobs = []
                    for line in pack_output.splitlines():
                        parts = line.split()
                        if len(parts) >= 3 and parts[1] == "blob":
                            try:
                                size = int(parts[2])
                                if size >= min_size_kb * 1024:
                                    sha = parts[0]
                                    blobs.append({"sha": sha, "size": size})
                            except (ValueError, IndexError):
                                pass

                    blobs.sort(key=lambda x: x["size"], reverse=True)

                    for blob in blobs[:20]:
                        # Find the path for this blob
                        name_output = run_git(
                            repo_path, "rev-list", "--objects", "--all",
                        )
                        path = "unknown"
                        if name_output:
                            for obj_line in name_output.splitlines():
                                if obj_line.startswith(blob["sha"][:12]):
                                    parts = obj_line.split(None, 1)
                                    if len(parts) > 1:
                                        path = parts[1]
                                    break

                        findings["history"].append({
                            "sha": blob["sha"][:12],
                            "path": path,
                            "size_bytes": blob["size"],
                            "size_human": format_size(blob["size"]),
                        })
                break  # Only check first pack

    findings["history"].sort(key=lambda x: x["size_bytes"], reverse=True)
    findings["history"] = findings["history"][:20]

    return findings


# ── Repo Stats ──────────────────────────────────────────────────────────────

def audit_stats(repo_path):
    """Get repository size and object statistics."""
    stats = {
        "git_dir_size": 0,
        "git_dir_size_human": "0 B",
        "working_tree_size": 0,
        "working_tree_size_human": "0 B",
        "total_commits": 0,
        "total_branches": 0,
        "total_tags": 0,
        "total_contributors": 0,
        "first_commit": None,
        "latest_commit": None,
    }

    # .git directory size
    git_dir = Path(repo_path) / ".git"
    if git_dir.is_dir():
        total = 0
        for f in git_dir.rglob("*"):
            if f.is_file():
                try:
                    total += f.stat().st_size
                except OSError:
                    pass
        stats["git_dir_size"] = total
        stats["git_dir_size_human"] = format_size(total)

    # Commit count
    count = run_git(repo_path, "rev-list", "--count", "HEAD")
    if count:
        try:
            stats["total_commits"] = int(count)
        except ValueError:
            pass

    # Branch count
    branches = run_git(repo_path, "branch", "--list")
    if branches:
        stats["total_branches"] = len([b for b in branches.splitlines() if b.strip()])

    # Tag count
    tags = run_git(repo_path, "tag", "--list")
    if tags:
        stats["total_tags"] = len([t for t in tags.splitlines() if t.strip()])

    # Contributors
    shortlog = run_git(repo_path, "shortlog", "-sn", "HEAD")
    if shortlog:
        stats["total_contributors"] = len(shortlog.splitlines())

    # First and latest commit
    first = run_git(repo_path, "log", "--reverse", "--format=%ci", "-1")
    if first:
        stats["first_commit"] = first.strip()

    latest = run_git(repo_path, "log", "--format=%ci", "-1")
    if latest:
        stats["latest_commit"] = latest.strip()

    # Count objects
    count_output = run_git(repo_path, "count-objects", "-v")
    if count_output:
        for line in count_output.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().replace("-", "_").replace(" ", "_")
                try:
                    stats[f"objects_{key}"] = int(val.strip())
                except ValueError:
                    stats[f"objects_{key}"] = val.strip()

    return stats


# ── Maintenance Audit ───────────────────────────────────────────────────────

def audit_maintenance(repo_path):
    """Check for common maintenance issues."""
    findings = {
        "missing_gitignore": [],
        "should_be_ignored": [],
        "needs_gc": False,
        "gc_recommendation": None,
    }

    # Check for common patterns that should be in .gitignore
    common_ignores = {
        "node_modules": "Node.js dependencies",
        "__pycache__": "Python bytecode cache",
        ".env": "Environment variables (may contain secrets)",
        ".DS_Store": "macOS folder metadata",
        "Thumbs.db": "Windows thumbnail cache",
        "*.pyc": "Python compiled files",
        "dist": "Build output",
        "build": "Build output",
        ".idea": "JetBrains IDE config",
        ".vscode": "VS Code config",
        "*.log": "Log files",
        "coverage": "Test coverage reports",
        ".pytest_cache": "Pytest cache",
    }

    gitignore_path = Path(repo_path) / ".gitignore"
    gitignore_content = ""
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()

    for pattern, description in common_ignores.items():
        # Check if tracked
        tracked = run_git(repo_path, "ls-files", pattern)
        if tracked:
            findings["should_be_ignored"].append({
                "pattern": pattern,
                "description": description,
                "tracked_files": len(tracked.splitlines()),
            })
        elif pattern not in gitignore_content and not gitignore_path.exists():
            findings["missing_gitignore"].append({
                "pattern": pattern,
                "description": description,
            })

    # Check if gc would help
    count_output = run_git(repo_path, "count-objects", "-v")
    if count_output:
        loose = 0
        for line in count_output.splitlines():
            if line.startswith("count:"):
                try:
                    loose = int(line.split(":")[1].strip())
                except ValueError:
                    pass
        if loose > 1000:
            findings["needs_gc"] = True
            findings["gc_recommendation"] = f"{loose} loose objects — run `git gc`"

    return findings


# ── Cleanup Script ──────────────────────────────────────────────────────────

def generate_cleanup_script(repo_path, branch_findings, force_delete=False):
    """Generate a cleanup shell script."""
    lines = ["#!/bin/bash", f'# Git Repo Cleanup Script for {repo_path}',
             f'# Generated: {datetime.now().isoformat()}', "",
             'set -e', ""]

    delete_flag = "-D" if force_delete else "-d"

    if branch_findings.get("merged"):
        lines.append("# === Delete merged branches ===")
        for b in branch_findings["merged"]:
            lines.append(f'echo "Deleting merged branch: {b["name"]}"')
            lines.append(f'git branch {delete_flag} "{b["name"]}"')
        lines.append("")

    if branch_findings.get("stale"):
        lines.append("# === Delete stale branches (review carefully!) ===")
        for b in branch_findings["stale"]:
            lines.append(f'# Stale {b["days_old"]} days, last: {b["last_subject"][:50]}')
            if force_delete:
                lines.append(f'git branch -D "{b["name"]}"')
            else:
                lines.append(f'# git branch -D "{b["name"]}"  # Uncomment after review')
        lines.append("")

    lines.append("# === Optimize repo ===")
    lines.append("git gc --aggressive --prune=now")
    lines.append("")
    lines.append('echo "Cleanup complete!"')

    return "\n".join(lines)


# ── Helpers ─────────────────────────────────────────────────────────────────

def format_size(size_bytes):
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ── Formatters ──────────────────────────────────────────────────────────────

def format_text(audit_result):
    """Format audit result as text."""
    lines = []
    r = audit_result

    lines.append(f"\n{'='*60}")
    lines.append(f"  Git Repo Audit: {r['repo_path']}")
    lines.append(f"{'='*60}")

    if "stats" in r:
        s = r["stats"]
        lines.append(f"\n  [STATS]")
        lines.append(f"  .git size:      {s['git_dir_size_human']}")
        lines.append(f"  Commits:        {s['total_commits']}")
        lines.append(f"  Branches:       {s['total_branches']}")
        lines.append(f"  Tags:           {s['total_tags']}")
        lines.append(f"  Contributors:   {s['total_contributors']}")
        if s.get("first_commit"):
            lines.append(f"  First commit:   {s['first_commit']}")

    if "branches" in r:
        b = r["branches"]
        lines.append(f"\n  [BRANCHES] (default: {b['default_branch']})")
        lines.append(f"  Total: {b['total_branches']} | "
                     f"Active: {len(b['active'])} | "
                     f"Stale: {len(b['stale'])} | "
                     f"Merged: {len(b['merged'])}")

        if b["merged"]:
            lines.append(f"\n  Merged (safe to delete):")
            for br in b["merged"][:10]:
                lines.append(f"    [-] {br['name']} ({br['days_old']}d old)")

        if b["stale"]:
            lines.append(f"\n  Stale (no recent commits):")
            for br in b["stale"][:10]:
                lines.append(f"    [!] {br['name']} ({br['days_old']}d old) — {br['author']}")

    if "large_files" in r:
        lf = r["large_files"]
        if lf["current_tree"]:
            lines.append(f"\n  [LARGE FILES] (current tree, >{lf['min_size_kb']}KB)")
            for f in lf["current_tree"][:10]:
                lines.append(f"    [!] {f['size_human']:>10}  {f['path']}")

        if lf["history"]:
            lines.append(f"\n  [LARGE BLOBS] (in git history)")
            for f in lf["history"][:10]:
                lines.append(f"    [!] {f['size_human']:>10}  {f['path']} ({f['sha']})")

    if "maintenance" in r:
        m = r["maintenance"]
        if m["should_be_ignored"]:
            lines.append(f"\n  [MAINTENANCE] Files that should be gitignored:")
            for f in m["should_be_ignored"]:
                lines.append(f"    [!] {f['pattern']} — {f['description']} ({f['tracked_files']} files)")

        if m["needs_gc"]:
            lines.append(f"\n  [GC] {m['gc_recommendation']}")

    # Summary
    issues = 0
    if "branches" in r:
        issues += len(r["branches"]["stale"]) + len(r["branches"]["merged"])
    if "large_files" in r:
        issues += len(r["large_files"]["current_tree"])
    if "maintenance" in r:
        issues += len(r["maintenance"]["should_be_ignored"])

    lines.append(f"\n  {'='*58}")
    lines.append(f"  Total issues: {issues}")
    if issues > 0:
        lines.append(f"  Run with --fix to generate cleanup script")
    else:
        lines.append(f"  Repo is clean!")
    lines.append("")

    return "\n".join(lines)


def format_json(audit_result):
    """Format as JSON."""
    return json.dumps(audit_result, indent=2, default=str)


def format_markdown(audit_result):
    """Format as Markdown report."""
    r = audit_result
    lines = [f"# Git Repo Audit: {Path(r['repo_path']).name}", ""]

    if "stats" in r:
        s = r["stats"]
        lines.append("## Repository Stats")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| .git size | {s['git_dir_size_human']} |")
        lines.append(f"| Commits | {s['total_commits']} |")
        lines.append(f"| Branches | {s['total_branches']} |")
        lines.append(f"| Tags | {s['total_tags']} |")
        lines.append(f"| Contributors | {s['total_contributors']} |")
        lines.append("")

    if "branches" in r:
        b = r["branches"]
        if b["merged"]:
            lines.append("## Merged Branches (safe to delete)")
            lines.append("")
            lines.append("| Branch | Age | Last Commit |")
            lines.append("|--------|-----|-------------|")
            for br in b["merged"]:
                lines.append(f"| `{br['name']}` | {br['days_old']}d | {br['last_subject'][:40]} |")
            lines.append("")

        if b["stale"]:
            lines.append("## Stale Branches")
            lines.append("")
            lines.append("| Branch | Age | Author | Last Commit |")
            lines.append("|--------|-----|--------|-------------|")
            for br in b["stale"]:
                lines.append(f"| `{br['name']}` | {br['days_old']}d | {br['author']} | {br['last_subject'][:30]} |")
            lines.append("")

    if "large_files" in r and r["large_files"]["current_tree"]:
        lines.append("## Large Files")
        lines.append("")
        lines.append("| File | Size |")
        lines.append("|------|------|")
        for f in r["large_files"]["current_tree"][:20]:
            lines.append(f"| `{f['path']}` | {f['size_human']} |")
        lines.append("")

    if "maintenance" in r and r["maintenance"]["should_be_ignored"]:
        lines.append("## Maintenance Issues")
        lines.append("")
        for f in r["maintenance"]["should_be_ignored"]:
            lines.append(f"- **{f['pattern']}** — {f['description']} ({f['tracked_files']} tracked files)")
        lines.append("")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Git Repo Cleaner — audit repositories for bloat, stale branches, and maintenance issues"
    )
    parser.add_argument("repo_path", help="Path to git repository")
    parser.add_argument("--check", "-c",
                       choices=["all", "branches", "large-files", "stats", "maintenance"],
                       default="all", help="Which checks to run (default: all)")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"],
                       default="text", help="Output format (default: text)")
    parser.add_argument("--stale-days", type=int, default=30,
                       help="Days without commits to consider branch stale (default: 30)")
    parser.add_argument("--min-size", type=int, default=1024,
                       help="Minimum file size in KB to flag (default: 1024 = 1MB)")
    parser.add_argument("--fix", action="store_true",
                       help="Generate cleanup script (printed to stdout, not executed)")
    parser.add_argument("--force-delete", action="store_true",
                       help="Use git branch -D instead of -d in cleanup script")

    args = parser.parse_args()

    # Validate repo
    repo = Path(args.repo_path)
    if not (repo / ".git").is_dir():
        print(f"Error: {args.repo_path} is not a git repository", file=sys.stderr)
        sys.exit(1)

    result = {"repo_path": str(repo.resolve())}

    checks = args.check
    if checks == "all":
        checks_to_run = ["stats", "branches", "large-files", "maintenance"]
    else:
        checks_to_run = [checks]

    for check in checks_to_run:
        if check == "stats":
            result["stats"] = audit_stats(repo)
        elif check == "branches":
            result["branches"] = audit_branches(repo, args.stale_days)
        elif check == "large-files":
            result["large_files"] = audit_large_files(repo, args.min_size)
        elif check == "maintenance":
            result["maintenance"] = audit_maintenance(repo)

    # Generate cleanup script if requested
    if args.fix and "branches" in result:
        script = generate_cleanup_script(repo, result["branches"], args.force_delete)
        print(script)
        return

    # Output
    formatters = {"text": format_text, "json": format_json, "markdown": format_markdown}
    print(formatters[args.format](result))

    # Exit code: 0 = clean, 1 = has issues
    issues = 0
    if "branches" in result:
        issues += len(result["branches"].get("stale", [])) + len(result["branches"].get("merged", []))
    if "large_files" in result:
        issues += len(result["large_files"].get("current_tree", []))
    if "maintenance" in result:
        issues += len(result["maintenance"].get("should_be_ignored", []))

    sys.exit(1 if issues > 0 else 0)


if __name__ == "__main__":
    main()
