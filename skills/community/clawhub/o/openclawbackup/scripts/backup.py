#!/usr/bin/env python3
"""
backup.py — Run OpenClaw backup using built-in `openclaw backup create`.
Supports --verify flag and --dry-run.
"""

import argparse
import os
import subprocess
import sys

DEFAULT_HOME = os.path.expanduser("~")

def get_backup_dir():
    return os.environ.get("OPENCLAW_BACKUP_DIR") or os.path.expanduser(f"{DEFAULT_HOME}/openclaw_backups")


def ensure_backup_dir():
    os.makedirs(get_backup_dir(), exist_ok=True)


def run_backup(verify=False, dry_run=False):
    backup_dir = get_backup_dir()
    ensure_backup_dir()
    cmd = ["openclaw", "backup", "create", "--output", backup_dir]
    if verify:
        cmd.append("--verify")
    if dry_run:
        cmd.append("--dry-run")

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode == 0:
        # Find the created archive path from output
        for line in result.stdout.splitlines():
            if "openclaw-backup.tar.gz" in line or ".tar.gz" in line:
                print(f"✅ Backup created: {line.strip()}")
        return True
    else:
        print(f"❌ Backup failed (exit {result.returncode})")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run OpenClaw backup")
    parser.add_argument("--verify", action="store_true", help="Verify archive after writing")
    parser.add_argument("--dry-run", action="store_true", help="Preview backup plan without writing")
    args = parser.parse_args()

    if args.dry_run:
        print("Dry-run mode — no files will be written.")

    success = run_backup(verify=args.verify, dry_run=args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()