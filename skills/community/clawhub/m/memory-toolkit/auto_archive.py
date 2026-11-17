#!/usr/bin/env python3
"""
Auto-Archive — Moves daily notes older than N days to archive subdirectories.

Organizes archived files by month (e.g. archive/2026-07/2026-07-11.md).
Preserves all other memory files (ontology, scores, json, non-daily notes).

Usage:
    python3 auto_archive.py                # Archive notes > 21 days (default)
    python3 auto_archive.py --days 30      # Custom threshold
    python3 auto_archive.py --dry-run      # Preview without moving
    python3 auto_archive.py --verbose      # Show each file moved
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace")).resolve()
MEMORY_DIR = WORKSPACE / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"


def validate_paths() -> None:
    """Re-validate that the memory/archive paths stay inside WORKSPACE.

    Called after every reassignment of WORKSPACE/MEMORY_DIR/ARCHIVE_DIR — in
    particular after --workspace is parsed. Checking only at import time left a
    gap: --workspace re-bound the globals further down the flow without
    re-running the guard (intent/code divergence).
    """
    if not MEMORY_DIR.resolve().is_relative_to(WORKSPACE):
        raise RuntimeError(f"Security: MEMORY_DIR escapes workspace: {MEMORY_DIR}")
    if not ARCHIVE_DIR.resolve().is_relative_to(WORKSPACE):
        raise RuntimeError(f"Security: ARCHIVE_DIR escapes workspace: {ARCHIVE_DIR}")


validate_paths()

# Daily note pattern: YYYY-MM-DD optionally followed by -suffix
DAILY_NOTE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-.+)?\.md$")


def find_archivable_notes(threshold_days: int):
    """Find daily notes older than threshold_days."""
    cutoff = datetime.now() - timedelta(days=threshold_days)
    candidates = []

    if not MEMORY_DIR.exists():
        return candidates

    for entry in MEMORY_DIR.iterdir():
        if entry.is_symlink() or not entry.is_file():
            continue
        match = DAILY_NOTE_RE.match(entry.name)
        if not match:
            continue

        # Use file modification time for age calculation
        mtime = datetime.fromtimestamp(entry.stat().st_mtime)
        if mtime < cutoff:
            # Extract the date portion for month grouping
            date_str = match.group(1)
            candidates.append((entry, date_str, mtime))

    # Sort oldest first
    candidates.sort(key=lambda x: x[2])
    return candidates


def archive_note(file_path: Path, date_str: str, verbose: bool = False) -> bool:
    """Move a note to archive/YYYY-MM/ subdirectory."""
    try:
        # Parse date to get year-month
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month_dir = ARCHIVE_DIR / f"{dt.year}-{dt.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)

        dest = month_dir / file_path.name

        # Don't overwrite if already archived (can happen with re-runs)
        if dest.exists():
            if verbose:
                print(f"  ⏭️  Already archived: {file_path.name} → {month_dir.name}/")
            return False

        shutil.move(str(file_path), str(dest))
        if verbose:
            print(f"  📦 {file_path.name} → archive/{month_dir.name}/")
        return True

    except Exception as e:
        print(f"  ❌ Error archiving {file_path.name}: {e}", file=sys.stderr)
        return False


def run_archive(threshold_days: int, dry_run: bool = False, verbose: bool = False, force: bool = False):
    """Main archive routine."""
    candidates = find_archivable_notes(threshold_days)

    if not candidates:
        print(f"✅ No notes older than {threshold_days} days to archive.")
        return {"archived": 0, "skipped": 0, "errors": 0, "candidates": []}

    print(f"Found {len(candidates)} notes older than {threshold_days} days.")

    if dry_run:
        print("\n🔍 Dry run — no files moved:")
        for f, date_str, mtime in candidates:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            month_dir = f"{dt.year}-{dt.month:02d}"
            print(f"  Would move: {f.name} → archive/{month_dir}/{f.name}")
        return {"archived": 0, "skipped": 0, "errors": 0, "candidates": [c[1] for c in candidates]}

    # Bulk safety: require confirmation if more than 10 files will be moved
    if len(candidates) > 10 and not force:
        print(f"\n⚠️  {len(candidates)} files will be moved to archive.")
        print("   Files to be moved:")
        for f, date_str, mtime in candidates[:20]:
            print(f"    {f.name}")
        if len(candidates) > 20:
            print(f"    ... and {len(candidates) - 20} more")
        if not sys.stdin.isatty():
            print("❌ Non-interactive mode with >10 files. Use --force to proceed without confirmation.")
            return {"archived": 0, "skipped": 0, "errors": 0, "candidates": []}
        response = input(f"\nMove {len(candidates)} files? (y/n): ").strip().lower()
        if response not in ("y", "yes"):
            print("Aborted. No files moved.")
            return {"archived": 0, "skipped": 0, "errors": 0, "candidates": []}

    archived = 0
    skipped = 0
    errors = 0
    archived_names = []

    for f, date_str, mtime in candidates:
        result = archive_note(f, date_str, verbose=verbose)
        if result:
            archived += 1
            archived_names.append(f.name)
        else:
            skipped += 1

    print(f"\n📊 Archive complete: {archived} moved, {skipped} skipped, {errors} errors.")
    return {"archived": archived, "skipped": skipped, "errors": errors, "candidates": archived_names}


def main():
    parser = argparse.ArgumentParser(description="Auto-archive daily notes older than N days")
    parser.add_argument("--days", type=int, default=21, help="Age threshold in days (default: 21)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show each file moved")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt for bulk moves (>10 files)")
    parser.add_argument("--workspace", type=str, default=None, help="Override workspace path")
    args = parser.parse_args()

    global WORKSPACE, MEMORY_DIR, ARCHIVE_DIR
    if args.workspace:
        WORKSPACE = Path(args.workspace).resolve()
        MEMORY_DIR = WORKSPACE / "memory"
        ARCHIVE_DIR = MEMORY_DIR / "archive"
        # Re-run the confinement guard: the import-time check no longer covers
        # the overridden values.
        validate_paths()

    result = run_archive(args.days, dry_run=args.dry_run, verbose=args.verbose, force=args.force)
    sys.exit(0 if result["errors"] == 0 else 1)


if __name__ == "__main__":
    main()