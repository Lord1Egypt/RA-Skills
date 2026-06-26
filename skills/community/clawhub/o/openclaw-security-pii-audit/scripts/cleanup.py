#!/usr/bin/env python3
"""Cleanup audit logs older than retention period.

Usage:
    python cleanup.py                  # default 7-day retention
    python cleanup.py --days 30        # 30-day retention
    python cleanup.py --dry-run        # preview only
"""

import argparse
import json
import re
import shutil
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_AUDIT_DIR = str(Path(__file__).resolve().parent.parent / 'openclaw-security-audit')
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def prune_scan_cache(audit_path, max_age_seconds, dry_run=False):
    """Remove expired entries from .scan-cache.json.

    Uses FileLock for consistency with audit_worker.py's ScanCache.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from file_lock import FileLock

    cache_file = audit_path / '.scan-cache.json'
    if not cache_file.exists():
        return

    lock_path = str(cache_file) + '.lock'
    try:
        with FileLock(lock_path):
            data = json.loads(cache_file.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return

    now = time.time()
    before = len(data)
    data = {k: v for k, v in data.items() if (now - v) < max_age_seconds}
    pruned = before - len(data)

    if pruned == 0:
        print(f'Scan cache: {before} entries, 0 expired.')
        return

    if dry_run:
        print(f'[DRY-RUN] Scan cache: would prune {pruned}/{before} expired entries.')
    else:
        try:
            with FileLock(lock_path):
                cache_file.write_text(
                    json.dumps(data, ensure_ascii=False), encoding='utf-8')
        except OSError as exc:
            print(f'[WARN] Could not write scan cache: {exc}')
            return
        print(f'Scan cache: pruned {pruned}/{before} expired entries.')


def cleanup(audit_dir, days, dry_run=False):
    audit_path = Path(audit_dir)
    if not audit_path.exists():
        print(f'Audit directory not found: {audit_dir}')
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    removed = 0

    for entry in sorted(audit_path.iterdir()):
        if not entry.is_dir() or not DATE_PATTERN.match(entry.name):
            continue
        try:
            dir_date = datetime.strptime(entry.name, '%Y-%m-%d').replace(
                tzinfo=timezone.utc)
        except ValueError:
            continue

        if dir_date < cutoff:
            if dry_run:
                print(f'[DRY-RUN] Would remove: {entry}')
            else:
                shutil.rmtree(entry)
                print(f'[REMOVED] {entry}')
            removed += 1

    unit = 'directory' if removed == 1 else 'directories'
    prefix = 'would be ' if dry_run else ''
    print(f'Total: {removed} {unit} {prefix}removed.')

    # Also prune stale scan cache entries
    prune_scan_cache(audit_path, days * 86400, dry_run)


def main():
    parser = argparse.ArgumentParser(description='Cleanup old audit logs')
    parser.add_argument('--days', type=int, default=7,
                        help='Retention period in days (default: 7)')
    parser.add_argument('--audit-dir', default=DEFAULT_AUDIT_DIR,
                        help='Audit directory path')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be removed without deleting')
    args = parser.parse_args()

    cleanup(args.audit_dir, args.days, args.dry_run)


if __name__ == '__main__':
    main()
