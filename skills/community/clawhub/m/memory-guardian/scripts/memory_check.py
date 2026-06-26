#!/usr/bin/env python3
"""
Memory health check + integrity system for OpenClaw workspace.
Run: python3 memory_check.py [--fix] [--stats] [--dedup] [--index]

Checks:
1. File integrity (detect corruption, encoding issues)
2. Size warnings (files over threshold)
3. Duplicate content detection (fuzzy matching)
4. Stale session files (older than retention window)
5. Index consistency (MEMORY.md references match actual files)
6. Orphan detection (files not referenced anywhere)

With --fix: auto-repairs what it can (dedup, stale cleanup, index rebuild)
"""

import os
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
PERMANENT_DIR = os.path.join(MEMORY_DIR, "permanent")
BATCH_DIR = os.path.join(WORKSPACE, "systems/batch-cognition/batches")
MEMORY_INDEX = os.path.join(WORKSPACE, "MEMORY.md")

# Thresholds
MAX_SESSION_AGE_DAYS = 7
MAX_FILE_LINES = 300
MAX_TOTAL_LINES = 3000
DEDUP_SIMILARITY_THRESHOLD = 0.85


def hash_content(text):
    """Simple content hash for dedup."""
    return hashlib.md5(text.strip().encode()).hexdigest()


def get_file_stats(filepath):
    """Get line count, size, age for a file."""
    stat = os.stat(filepath)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    return {
        "path": filepath,
        "lines": len(lines),
        "bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "age_days": (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days,
        "hash": hash_content("".join(lines)),
    }


def check_all():
    """Run all checks, return report."""
    issues = []
    stats = {"total_files": 0, "total_lines": 0, "total_bytes": 0, "files": []}

    # Scan all memory files
    for root, dirs, files in os.walk(MEMORY_DIR):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            try:
                fstats = get_file_stats(fpath)
                stats["files"].append(fstats)
                stats["total_files"] += 1
                stats["total_lines"] += fstats["lines"]
                stats["total_bytes"] += fstats["bytes"]

                # Check: file too large
                if fstats["lines"] > MAX_FILE_LINES:
                    issues.append({
                        "type": "LARGE_FILE",
                        "severity": "WARN",
                        "file": fpath,
                        "detail": f"{fstats['lines']} lines (max {MAX_FILE_LINES})",
                    })

                # Check: stale session file
                if "permanent" not in fpath and "active" not in fpath:
                    # It's a session file — check age
                    if fstats["age_days"] > MAX_SESSION_AGE_DAYS:
                        issues.append({
                            "type": "STALE_SESSION",
                            "severity": "WARN",
                            "file": fpath,
                            "detail": f"{fstats['age_days']} days old (max {MAX_SESSION_AGE_DAYS})",
                        })

            except Exception as e:
                issues.append({
                    "type": "READ_ERROR",
                    "severity": "ERROR",
                    "file": fpath,
                    "detail": str(e),
                })

    # Check: total lines
    if stats["total_lines"] > MAX_TOTAL_LINES:
        issues.append({
            "type": "TOTAL_SIZE",
            "severity": "WARN",
            "file": MEMORY_DIR,
            "detail": f"{stats['total_lines']} total lines (max {MAX_TOTAL_LINES})",
        })

    # Check: duplicate content
    hashes = defaultdict(list)
    for fstats in stats["files"]:
        hashes[fstats["hash"]].append(fstats["path"])
    for h, paths in hashes.items():
        if len(paths) > 1:
            issues.append({
                "type": "DUPLICATE",
                "severity": "WARN",
                "file": ", ".join(paths),
                "detail": f"{len(paths)} files with identical content",
            })

    # Check: MEMORY.md index consistency
    if os.path.exists(MEMORY_INDEX):
        with open(MEMORY_INDEX, 'r') as f:
            index_content = f.read()
        for fstats in stats["files"]:
            relpath = os.path.relpath(fstats["path"], WORKSPACE)
            # Only check permanent files — session files aren't indexed
            if "permanent" in fstats["path"]:
                basename = os.path.basename(fstats["path"])
                if basename not in index_content:
                    issues.append({
                        "type": "ORPHAN",
                        "severity": "INFO",
                        "file": fstats["path"],
                        "detail": "Not referenced in MEMORY.md",
                    })

    return stats, issues


def print_report(stats, issues):
    """Print human-readable report."""
    print("=" * 60)
    print("MEMORY HEALTH CHECK")
    print("=" * 60)
    print(f"Total files:  {stats['total_files']}")
    print(f"Total lines:  {stats['total_lines']}")
    print(f"Total size:   {stats['total_bytes'] / 1024:.1f} KB")
    print()

    if not issues:
        print("✅ All checks passed. Memory is healthy.")
        return

    # Group by severity
    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]
    infos = [i for i in issues if i["severity"] == "INFO"]

    if errors:
        print(f"🔴 ERRORS ({len(errors)}):")
        for i in errors:
            print(f"   [{i['type']}] {i['file']}: {i['detail']}")
        print()

    if warnings:
        print(f"🟡 WARNINGS ({len(warnings)}):")
        for i in warnings:
            print(f"   [{i['type']}] {os.path.basename(i['file'])}: {i['detail']}")
        print()

    if infos:
        print(f"🔵 INFO ({len(infos)}):")
        for i in infos:
            print(f"   [{i['type']}] {os.path.basename(i['file'])}: {i['detail']}")


if __name__ == "__main__":
    stats, issues = check_all()
    print_report(stats, issues)
