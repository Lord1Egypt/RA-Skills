#!/usr/bin/env python3
"""
health_check.py — Verify backup archive integrity and report status.
Uses `openclaw backup verify` + checks backup directory.
"""

import argparse
import glob
import os
import subprocess
import sys
from datetime import datetime

DEFAULT_HOME = os.path.expanduser("~")

def get_backup_dir():
    return os.environ.get("OPENCLAW_BACKUP_DIR") or os.path.expanduser(f"{DEFAULT_HOME}/openclaw_backups")


def find_latest_archive():
    backup_dir = get_backup_dir()
    pattern = os.path.join(backup_dir, "*openclaw-backup.tar.gz")
    archives = sorted(glob.glob(pattern), reverse=True)
    if not archives:
        return None
    return archives[0]


def verify_archive(archive_path):
    print(f"Verifying: {archive_path}")
    result = subprocess.run(
        ["openclaw", "backup", "verify", archive_path],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def check_backup_dir():
    backup_dir = get_backup_dir()
    pattern = os.path.join(backup_dir, "*openclaw-backup.tar.gz")
    archives = sorted(glob.glob(pattern), reverse=True)

    if not archives:
        print(f"❌ No backups found in {backup_dir}/")
        return False

    print(f"📁 Backup directory: {backup_dir}")
    print(f"   Total archives: {len(archives)}")
    print()

    # Show all archives with age
    now = datetime.now()
    print("Backups:")
    for i, arch in enumerate(archives[:10]):  # show last 10
        mtime = os.path.getmtime(arch)
        age = now - datetime.fromtimestamp(mtime)
        size_mb = os.path.getsize(arch) / (1024 * 1024)
        marker = " ← latest" if i == 0 else ""
        print(f"   {os.path.basename(arch)}  {size_mb:.1f} MB  {age.days}d old{marker}")

    if len(archives) > 10:
        print(f"   ... and {len(archives) - 10} more")

    return True


def main():
    parser = argparse.ArgumentParser(description="Check backup health")
    parser.add_argument("--archive", help="Specific archive to verify (default: latest)")
    args = parser.parse_args()

    # Check backup directory first
    if not check_backup_dir():
        sys.exit(1)

    print()

    # Verify the archive
    archive = args.archive or find_latest_archive()
    if not archive:
        print("No archive found to verify.")
        sys.exit(1)

    print()
    if verify_archive(archive):
        print("✅ Backup archive is valid")
        sys.exit(0)
    else:
        print("❌ Backup archive verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()