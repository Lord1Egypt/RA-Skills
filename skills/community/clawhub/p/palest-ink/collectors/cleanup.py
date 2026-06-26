#!/usr/bin/env python3
"""Palest Ink - Data Cleanup Tool

Removes oldest activity records when storage exceeds a threshold.
Always asks for user confirmation before deleting (unless --force).

Usage:
    python3 cleanup.py                   # Check size; clean if > 2 GB
    python3 cleanup.py --dry-run         # Show what would be deleted, no changes
    python3 cleanup.py --max-size 1.5    # Custom threshold in GB
    python3 cleanup.py --keep-days 60    # Always keep the most recent N days
    python3 cleanup.py --force           # Skip confirmation prompt (for skill use)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")
FLAG_FILE = os.path.join(PALEST_INK_DIR, "tmp", "cleanup_needed")

DEFAULT_MAX_SIZE_GB = 2.0
DEFAULT_KEEP_DAYS = 30
TARGET_RATIO = 0.70  # After cleanup, aim for 70% of max_size


def format_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_all_datafiles():
    """Return list of (date_str, filepath, size_bytes) sorted oldest-first."""
    files = []
    if not os.path.isdir(DATA_DIR):
        return files
    for year in sorted(os.listdir(DATA_DIR)):
        year_dir = os.path.join(DATA_DIR, year)
        if not os.path.isdir(year_dir) or not year.isdigit():
            continue
        for month in sorted(os.listdir(year_dir)):
            month_dir = os.path.join(year_dir, month)
            if not os.path.isdir(month_dir) or not month.isdigit():
                continue
            for fname in sorted(os.listdir(month_dir)):
                if not fname.endswith(".jsonl"):
                    continue
                day = fname.replace(".jsonl", "")
                date_str = f"{year}-{month}-{day}"
                fpath = os.path.join(month_dir, fname)
                size = os.path.getsize(fpath)
                files.append((date_str, fpath, size))
    return files


def count_records(filepath):
    try:
        with open(filepath, "r", errors="replace") as f:
            return sum(1 for line in f if line.strip())
    except OSError:
        return 0


def remove_empty_dirs(path):
    """Recursively remove empty directories up to DATA_DIR."""
    while path != DATA_DIR:
        try:
            if not os.listdir(path):
                os.rmdir(path)
            else:
                break
        except OSError:
            break
        path = os.path.dirname(path)


def clear_flag():
    try:
        os.unlink(FLAG_FILE)
    except OSError:
        pass


def main():
    parser = argparse.ArgumentParser(description="Palest Ink - Data Cleanup Tool")
    parser.add_argument("--max-size", type=float, default=DEFAULT_MAX_SIZE_GB,
                        metavar="GB", help=f"Size threshold in GB (default: {DEFAULT_MAX_SIZE_GB})")
    parser.add_argument("--keep-days", type=int, default=DEFAULT_KEEP_DAYS,
                        metavar="N", help=f"Always keep last N days (default: {DEFAULT_KEEP_DAYS})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be deleted without making changes")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompt")
    args = parser.parse_args()

    max_bytes = int(args.max_size * 1024 ** 3)
    target_bytes = int(max_bytes * TARGET_RATIO)
    keep_cutoff = (datetime.now() - timedelta(days=args.keep_days)).strftime("%Y-%m-%d")

    all_files = get_all_datafiles()
    if not all_files:
        print("No data files found.")
        return

    total_bytes = sum(s for _, _, s in all_files)
    total_records = None  # compute lazily only if needed

    print(f"Data directory : {DATA_DIR}")
    print(f"Current size   : {format_size(total_bytes)}")
    print(f"Threshold      : {format_size(max_bytes)}")
    print(f"Date range     : {all_files[0][0]}  →  {all_files[-1][0]}")
    print(f"Total files    : {len(all_files)}")
    print()

    if total_bytes <= max_bytes:
        print(f"Storage is within the {args.max_size} GB limit. No cleanup needed.")
        clear_flag()
        return

    overage = total_bytes - max_bytes
    print(f"⚠️  Exceeds limit by {format_size(overage)}. "
          f"Will delete oldest files until size ≤ {format_size(target_bytes)} "
          f"({int(TARGET_RATIO * 100)}% of threshold).")
    print()

    # Determine which files to delete (oldest first, never touch keep_cutoff window)
    to_delete = []
    freed = 0
    remaining = total_bytes

    for date_str, fpath, size in all_files:
        if remaining <= target_bytes:
            break
        if date_str >= keep_cutoff:
            # Reached the protected window — stop
            break
        to_delete.append((date_str, fpath, size))
        freed += size
        remaining -= size

    if not to_delete:
        print(f"Cannot free enough space without deleting files from the last "
              f"{args.keep_days} days (protected window: {keep_cutoff} → today).")
        print("Use --keep-days to reduce the protected window, or manually delete files.")
        return

    # Collect stats
    record_count = sum(count_records(fp) for _, fp, _ in to_delete)
    date_from = to_delete[0][0]
    date_to = to_delete[-1][0]

    print(f"Files to delete : {len(to_delete)}  ({date_from}  →  {date_to})")
    print(f"Records removed : {record_count:,}")
    print(f"Space freed     : {format_size(freed)}")
    print(f"Size after      : {format_size(remaining)}")
    print()

    if args.dry_run:
        print("Dry run — no files were deleted.")
        print("\nFiles that would be removed:")
        for date_str, fpath, size in to_delete:
            nrec = count_records(fpath)
            print(f"  {date_str}  {format_size(size):>10}  ({nrec} records)")
        return

    # Confirmation
    if not args.force:
        answer = input(
            f"Delete {len(to_delete)} files ({format_size(freed)}) "
            f"from {date_from} to {date_to}? [y/N] "
        ).strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted. No files were deleted.")
            return

    # Delete
    deleted_count = 0
    deleted_bytes = 0
    for date_str, fpath, size in to_delete:
        try:
            os.unlink(fpath)
            remove_empty_dirs(os.path.dirname(fpath))
            deleted_count += 1
            deleted_bytes += size
        except OSError as e:
            print(f"  Warning: could not delete {fpath}: {e}")

    clear_flag()
    print(f"\nDone. Deleted {deleted_count} files, freed {format_size(deleted_bytes)}.")
    print(f"Current data size: {format_size(remaining)}")


if __name__ == "__main__":
    main()
