#!/usr/bin/env python3
"""Clean up old files from a user-specified inbound media folder."""

import os
import time
import argparse
from pathlib import Path

MAX_AGE_HOURS = 24


def cleanup(inbound_dir: str, max_age_hours: int = MAX_AGE_HOURS, dry_run: bool = False):
    inbound_dir = os.path.expanduser(inbound_dir)
    if not os.path.isdir(inbound_dir):
        print(f"Inbound directory not found: {inbound_dir}")
        return

    cutoff = time.time() - max_age_hours * 3600
    removed, kept = 0, 0

    for p in Path(inbound_dir).iterdir():
        if not p.is_file():
            continue
        if p.stat().st_mtime < cutoff:
            if dry_run:
                print(f"  [DRY] would remove {p.name}")
            else:
                p.unlink()
                print(f"  removed {p.name}")
            removed += 1
        else:
            kept += 1

    print(f"\nRemoved: {removed}, Kept: {kept} (threshold: {max_age_hours}h)")


if __name__ == "__main__":
    vault_dir = os.environ.get("IMAGE_VAULT_DIR", os.path.expanduser("~/.image-vault"))
    default_inbound = os.path.join(vault_dir, "inbound")

    p = argparse.ArgumentParser(description="Clean old inbound media files")
    p.add_argument("--dir", default=default_inbound, help="Inbound directory to clean (default: IMAGE_VAULT_DIR/inbound)")
    p.add_argument("--hours", type=int, default=MAX_AGE_HOURS, help="Max age in hours (default 24)")
    p.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
    args = p.parse_args()
    cleanup(inbound_dir=args.dir, max_age_hours=args.hours, dry_run=args.dry_run)
