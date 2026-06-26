#!/usr/bin/env python3
"""
cleanup_old_backups.py — Remove old backup archives from ~/openclaw_backups/.
Default: dry-run. Use --days to specify age threshold.
"""

import argparse
import glob
import os
import sys
from datetime import datetime, timedelta

DEFAULT_HOME = os.path.expanduser("~")

def get_backup_dir():
    home = os.environ.get("OPENCLAW_BACKUP_DIR") or os.path.expanduser(f"{DEFAULT_HOME}/openclaw_backups")
    return home


def find_archives(days=None):
    backup_dir = get_backup_dir()
    pattern = os.path.join(backup_dir, "*openclaw-backup.tar.gz")
    all_archives = sorted(glob.glob(pattern), reverse=True)
    if days is None:
        return all_archives
    cutoff = datetime.now() - timedelta(days=days)
    old = []
    for arch in all_archives:
        mtime = datetime.fromtimestamp(os.path.getmtime(arch))
        if mtime < cutoff:
            old.append(arch)
    return old


def main():
    parser = argparse.ArgumentParser(description="Cleanup old OpenClaw backups")
    parser.add_argument("--days", type=int, default=None,
                        help="Show backups older than N days (default: show all)")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Preview deletions (default: True)")
    parser.add_argument("--execute", action="store_true",
                        help="Actually delete (overrides dry-run)")
    args = parser.parse_args()

    dry_run = not args.execute

    backup_dir = get_backup_dir()
    all_archives = find_archives(None)
    to_delete = find_archives(args.days) if args.days else []

    if not all_archives:
        print(f"No backups found in {backup_dir}/")
        sys.exit(0)

    print(f"Backup directory: {backup_dir}")
    print(f"Total archives: {len(all_archives)}")

    if args.days:
        print(f"Filter: > {args.days} days old → {len(to_delete)} archive(s) would be affected")

    print()
    print("All backups:")
    now = datetime.now()
    for arch in all_archives:
        mtime = datetime.fromtimestamp(os.path.getmtime(arch))
        age = now - mtime
        size_mb = os.path.getsize(arch) / (1024 * 1024)
        in_delete = arch in to_delete
        marker = " ← TO DELETE" if in_delete else ""
        print(f"   {os.path.basename(arch)}  {size_mb:.1f} MB  {age.days}d old{marker}")

    print()

    if to_delete:
        if dry_run:
            print(f"🗑️  Run with --execute to delete {len(to_delete)} archive(s).")
        else:
            deleted = 0
            for arch in to_delete:
                os.remove(arch)
                deleted += 1
                print(f"   Deleted: {os.path.basename(arch)}")
            print(f"\nDeleted {deleted} archive(s).")
    else:
        if args.days:
            print(f"No archives older than {args.days} days.")


if __name__ == "__main__":
    main()