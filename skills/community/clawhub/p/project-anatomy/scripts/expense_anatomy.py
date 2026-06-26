#!/usr/bin/env python3
"""
Expense Anatomy Scanner
Specialized variant for reimbursement directories.
Parses structured info from filenames (date, merchant, amount, sequence).

Usage:
    python3 expense_anatomy.py <expense-dir> [--output <path>]
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict


def parse_expense_filename(fname: str) -> dict:
    """Parse structured info from expense filename patterns."""
    info = {'raw': fname, 'type': None, 'date': None,
            'merchant': None, 'amount': None, 'seq': None}

    # PDF pattern: 20260506新镇江上海小笼馆_22.60元_001.pdf
    pdf_match = re.match(
        r'(\d{8})(.+?)(?:配送费)?_(\d+\.?\d*)元_(\d+)\.pdf', fname)
    if pdf_match:
        info['type'] = 'invoice'
        info['date'] = pdf_match.group(1)
        info['merchant'] = pdf_match.group(2).rstrip('_')
        info['amount'] = float(pdf_match.group(3))
        info['seq'] = pdf_match.group(4)
        if '配送费' in fname:
            info['subtype'] = 'delivery_fee'
        else:
            info['subtype'] = 'meal'
        return info

    # JPG pattern: 0506新镇江上海小笼馆_001.jpg
    jpg_match = re.match(r'(\d{4})(.+?)_(\d+)\.jpg', fname)
    if jpg_match:
        info['type'] = 'screenshot'
        info['date'] = '2026' + jpg_match.group(1)
        info['merchant'] = jpg_match.group(2)
        info['seq'] = jpg_match.group(3)
        return info

    # Excel
    if fname.endswith(('.xlsx', '.xls')):
        info['type'] = 'workbook'
        return info

    info['type'] = 'other'
    return info


def scan_expense_dir(root: Path) -> dict:
    """Scan expense directory and categorize files."""
    results = {
        'invoices': [],
        'screenshots': [],
        'workbooks': [],
        'others': [],
        'by_seq': defaultdict(list),
        'by_date': defaultdict(list),
    }

    for item in sorted(root.iterdir()):
        if item.is_dir():
            continue
        info = parse_expense_filename(item.name)
        info['size_kb'] = item.stat().st_size / 1024

        if info['type'] == 'invoice':
            results['invoices'].append(info)
        elif info['type'] == 'screenshot':
            results['screenshots'].append(info)
        elif info['type'] == 'workbook':
            results['workbooks'].append(info)
        else:
            results['others'].append(info)

        if info.get('seq'):
            results['by_seq'][info['seq']].append(info)
        if info.get('date'):
            results['by_date'][info['date']].append(info)

    return results


def generate_expense_anatomy(results: dict, dir_name: str) -> str:
    """Generate expense anatomy markdown."""
    lines = [
        f'# Expense Anatomy: {dir_name}',
        '',
        f'> {len(results["invoices"])} invoices, '
        f'{len(results["screenshots"])} screenshots, '
        f'{len(results["workbooks"])} workbooks',
        '',
    ]

    # Summary by sequence (each meal)
    lines.append('## By Meal (sequence)')
    lines.append('')
    for seq in sorted(results['by_seq'].keys()):
        items = results['by_seq'][seq]
        merchant = next((i['merchant'] for i in items if i.get('merchant')), '?')
        date = next((i['date'] for i in items if i.get('date')), '?')
        total = sum(i.get('amount', 0) for i in items if i.get('amount'))
        has_screenshot = any(i['type'] == 'screenshot' for i in items)
        has_invoice = any(i['type'] == 'invoice' for i in items)
        status = '✅' if (has_screenshot and has_invoice) else '⚠️'
        parts = []
        if has_screenshot:
            parts.append('截图')
        if has_invoice:
            inv_count = sum(1 for i in items if i['type'] == 'invoice')
            parts.append(f'{inv_count}张发票')
        lines.append(
            f'- {status} #{seq} {date[4:6]}/{date[6:8]} '
            f'{merchant} ¥{total:.2f} ({", ".join(parts)})'
        )
    lines.append('')

    # Summary by date
    lines.append('## By Date')
    lines.append('')
    for date in sorted(results['by_date'].keys()):
        items = results['by_date'][date]
        total = sum(i.get('amount', 0) for i in items if i.get('amount'))
        count = len(set(i.get('seq') for i in items if i.get('seq')))
        lines.append(f'- {date[4:6]}/{date[6:8]}: {count} meals, ¥{total:.2f}')
    lines.append('')

    # Missing items check
    lines.append('## Completeness Check')
    lines.append('')
    for seq in sorted(results['by_seq'].keys()):
        items = results['by_seq'][seq]
        has_screenshot = any(i['type'] == 'screenshot' for i in items)
        has_invoice = any(i['type'] == 'invoice' for i in items)
        if not has_screenshot:
            merchant = next((i['merchant'] for i in items), '?')
            lines.append(f'- ⚠️ #{seq} {merchant}: 缺截图')
        if not has_invoice:
            merchant = next((i['merchant'] for i in items), '?')
            lines.append(f'- ⚠️ #{seq} {merchant}: 缺发票')

    if not any('⚠️' in l for l in lines[-10:]):
        lines.append('- ✅ All meals have both screenshots and invoices')
    lines.append('')

    return '\n'.join(lines)


def scan_downloads():
    """Check ~/Downloads for unreimbursed expense files (PDF/JPG from today)."""
    dl = Path.home() / 'Downloads'
    if not dl.is_dir():
        return None
    from datetime import datetime, timedelta
    today = datetime.now().strftime('%Y%m%d')
    recent = []
    for f in dl.iterdir():
        if f.is_dir():
            continue
        fname = f.name
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if (fname.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')) and
                today in fname):
            recent.append((fname, mtime, f.stat().st_size / 1024))
        elif mtime > datetime.now() - timedelta(hours=24):
            if fname.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                recent.append((fname, mtime, f.stat().st_size / 1024))
    return recent if recent else None


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Expense directory anatomy')
    parser.add_argument('expense_dir', help='Expense directory path')
    parser.add_argument('--output', '-o', help='Output path')
    parser.add_argument('--scan-downloads', '-d', action='store_true',
                        help='Also scan ~/Downloads for unreimbursed files')
    args = parser.parse_args()

    expense_dir = Path(args.expense_dir).resolve()
    if not expense_dir.is_dir():
        print(f"Error: {expense_dir} not a directory", file=sys.stderr)
        sys.exit(1)

    results = scan_expense_dir(expense_dir)
    content = generate_expense_anatomy(results, expense_dir.name)

    # Downloads scan
    dl_files = None
    if args.scan_downloads:
        dl_files = scan_downloads()
        if dl_files:
            content += '\n## ⚠️ Downloads 待归档\n\n'
            for fname, mtime, size in dl_files:
                content += f'- `{fname}` ({size:.0f}KB) — {mtime.strftime("%m/%d %H:%M")}\n'

    output_path = Path(args.output) if args.output else expense_dir / '.anatomy.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Done! → {output_path}")
    print(f"  {len(results['invoices'])} invoices, "
          f"{len(results['screenshots'])} screenshots")
    print(f"  {len(results['by_seq'])} meals across "
          f"{len(results['by_date'])} days")
    if args.scan_downloads and dl_files:
        print(f"  ⚠️ Downloads 有 {len(dl_files)} 个未归档文件")


if __name__ == '__main__':
    main()
