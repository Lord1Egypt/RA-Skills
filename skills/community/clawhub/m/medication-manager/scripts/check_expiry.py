#!/usr/bin/env python3
"""
Check medication expiry dates from markdown files.

Scans all .md files in the given directory for batch expiry dates
and reports warnings based on configurable thresholds.

Usage:
    python3 check_expiry.py /path/to/data/medications/

No database required — pure file scanning.
"""

import os
import re
import sys
from datetime import datetime, timedelta


def parse_markdown_table(filepath):
    """Extract batch rows from a markdown medication file."""
    batches = []
    in_batches = False
    header_found = False
    columns = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Detect Batches section
            if line.startswith('## Batches'):
                in_batches = True
                continue

            # Detect next section (exit batches)
            if in_batches and line.startswith('## ') and 'Batches' not in line:
                in_batches = False
                continue

            if not in_batches:
                continue

            # Parse header row
            if not header_found and line.startswith('|') and 'Batch' in line:
                columns = [c.strip() for c in line.strip('|').split('|')]
                header_found = True
                continue

            # Skip separator row
            if header_found and line.startswith('|') and '---' in line:
                continue

            # Parse data rows
            if header_found and line.startswith('|'):
                values = [c.strip() for c in line.strip('|').split('|')]
                if len(values) >= len(columns):
                    row = dict(zip(columns, values))
                    batches.append(row)

    return batches


def check_expiry(med_dir):
    """Scan all medication markdown files for expiry dates."""
    today = datetime.now().date()

    expired = []
    warning_7d = []
    warning_30d = []
    warning_90d = []

    med_files = [f for f in os.listdir(med_dir) if f.endswith('.md')]

    for filename in med_files:
        filepath = os.path.join(med_dir, filename)
        batches = parse_markdown_table(filepath)

        for batch in batches:
            expiry_str = batch.get('Expiry', '')
            status = batch.get('Status', '')

            # Skip already expired/depleted/discarded batches
            if status in ('expired', 'depleted', 'discarded'):
                continue

            # Parse expiry date (supports YYYY-MM-DD and YYYY-MM)
            try:
                if re.match(r'\d{4}-\d{2}-\d{2}', expiry_str):
                    expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
                elif re.match(r'\d{4}-\d{2}', expiry_str):
                    expiry = datetime.strptime(expiry_str, '%Y-%m').date()
                else:
                    continue
            except ValueError:
                continue

            days_left = (expiry - today).days
            batch_name = f"{filename.replace('.md', '')} [{batch.get('Batch No', '?')}]"
            entry = {
                'name': batch_name,
                'expiry': expiry_str,
                'days': days_left,
                'qty': batch.get('Qty', '?'),
                'unit': batch.get('Unit', ''),
            }

            if days_left < 0:
                expired.append(entry)
            elif days_left <= 7:
                warning_7d.append(entry)
            elif days_left <= 30:
                warning_30d.append(entry)
            elif days_left <= 90:
                warning_90d.append(entry)

    # Sort each category by days ascending
    for lst in [expired, warning_7d, warning_30d, warning_90d]:
        lst.sort(key=lambda x: x['days'])

    # Print results
    print(f"Scan date: {today.strftime('%Y-%m-%d')}")
    print(f"Files scanned: {len(med_files)}")
    print()

    print(f"=== ❌ 已过期 ({len(expired)}) ===")
    if expired:
        for e in expired:
            print(f"  {e['name']} | 过期: {e['expiry']} | 数量: {e['qty']}{e['unit']} | {-e['days']}天前过期")
    else:
        print("  无")

    print(f"\n=== ⚠️ 7 天内过期 ({len(warning_7d)}) ===")
    if warning_7d:
        for e in warning_7d:
            print(f"  {e['name']} | 过期: {e['expiry']} | 数量: {e['qty']}{e['unit']} | 剩余 {e['days']} 天")
    else:
        print("  无")

    print(f"\n=== ⚠️ 30 天内过期 ({len(warning_30d)}) ===")
    if warning_30d:
        for e in warning_30d:
            print(f"  {e['name']} | 过期: {e['expiry']} | 数量: {e['qty']}{e['unit']} | 剩余 {e['days']} 天")
    else:
        print("  无")

    print(f"\n=== 🔶 90 天内过期 ({len(warning_90d)}) ===")
    if warning_90d:
        for e in warning_90d:
            print(f"  {e['name']} | 过期: {e['expiry']} | 数量: {e['qty']}{e['unit']} | 剩余 {e['days']} 天")
    else:
        print("  无")

    # Summary
    total = len(expired) + len(warning_7d) + len(warning_30d) + len(warning_90d)
    print(f"\n--- Total items needing attention: {total} ---")

    return total


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 check_expiry.py /path/to/data/medications/")
        sys.exit(1)

    med_dir = sys.argv[1]
    if not os.path.isdir(med_dir):
        print(f"Error: {med_dir} is not a directory")
        sys.exit(1)

    check_expiry(med_dir)
