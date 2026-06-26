#!/usr/bin/env python3
"""Markdown Table Maker - Create, format, and convert tables. Zero dependencies."""

import csv
import json
import sys
import re
import argparse

def parse_md_table(text):
    """Parse a Markdown table into headers and rows."""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].strip('|').split('|')]
    rows = []
    for line in lines[2:]:  # Skip separator line
        row = [c.strip() for c in line.strip('|').split('|')]
        rows.append(row)
    return headers, rows

def render_md_table(headers, rows, align=None):
    """Render headers and rows as a Markdown table."""
    if align is None:
        align = ['left'] * len(headers)
    # Calculate widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    lines = []
    # Header
    lines.append('| ' + ' | '.join(str(h).ljust(widths[i]) for i, h in enumerate(headers)) + ' |')
    # Separator
    seps = []
    for i, w in enumerate(widths):
        a = align[i] if i < len(align) else 'left'
        if a == 'center':
            seps.append(':' + '-' * (w) + ':')
        elif a == 'right':
            seps.append('-' * (w) + ':')
        else:
            seps.append('-' * (w))
    lines.append('| ' + ' | '.join(seps) + ' |')
    # Rows
    for row in rows:
        cells = []
        for i in range(len(headers)):
            val = str(row[i]) if i < len(row) else ''
            cells.append(val.ljust(widths[i]))
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)

def cmd_create(args):
    headers = [h.strip() for h in args.columns.split(',')]
    rows = []
    if args.rows:
        for r in args.rows:
            rows.append([c.strip() for c in r.split(',')])
    result = render_md_table(headers, rows)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
        print(f"Table saved to {args.output}")
    else:
        print(result)

def cmd_from_csv(args):
    with open(args.file, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    result = render_md_table(headers, rows)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
        print(f"Converted → {args.output}")
    else:
        print(result)

def cmd_from_json(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        print("Empty JSON array")
        return
    headers = list(data[0].keys())
    rows = [[str(item.get(h, '')) for h in headers] for item in data]
    result = render_md_table(headers, rows)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
        print(f"Converted → {args.output}")
    else:
        print(result)

def cmd_align(args):
    with open(args.file, 'r') as f:
        text = f.read()
    headers, rows = parse_md_table(text)
    align_map = {}
    if args.align_spec:
        for spec in args.align_spec.split(','):
            parts = spec.strip().split(':')
            if len(parts) == 2:
                col_name = parts[0].strip()
                col_align = parts[1].strip().lower()
                align_map[col_name] = col_align
    align = []
    for h in headers:
        align.append(align_map.get(h, 'left'))
    result = render_md_table(headers, rows, align)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
    else:
        print(result)

def cmd_sort(args):
    with open(args.file, 'r') as f:
        text = f.read()
    headers, rows = parse_md_table(text)
    col_idx = None
    for i, h in enumerate(headers):
        if h.lower() == args.column.lower():
            col_idx = i
            break
    if col_idx is None:
        print(f"Column '{args.column}' not found")
        return
    reverse = args.order == 'desc'
    try:
        rows.sort(key=lambda r: float(r[col_idx]) if col_idx < len(r) else 0, reverse=reverse)
    except (ValueError, TypeError):
        rows.sort(key=lambda r: r[col_idx] if col_idx < len(r) else '', reverse=reverse)
    result = render_md_table(headers, rows)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result + '\n')
    else:
        print(result)

def cmd_transpose(args):
    with open(args.file, 'r') as f:
        text = f.read()
    headers, rows = parse_md_table(text)
    # Transpose: columns become rows
    new_headers = ['Column'] + [f'Row {i+1}' for i in range(len(rows))]
    new_rows = []
    for i, h in enumerate(headers):
        row = [h] + [r[i] if i < len(r) else '' for r in rows]
        new_rows.append(row)
    result = render_md_table(new_headers, new_rows)
    print(result)

def main():
    parser = argparse.ArgumentParser(description='Markdown Table Maker')
    sub = parser.add_subparsers(dest='command')
    
    p = sub.add_parser('create', help='Create a table')
    p.add_argument('-c', '--columns', required=True, help='Comma-separated column names')
    p.add_argument('-r', '--rows', nargs='*', help='Comma-separated row values')
    p.add_argument('-o', '--output')
    
    p = sub.add_parser('from-csv', help='Convert CSV to Markdown table')
    p.add_argument('file'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('from-json', help='Convert JSON to Markdown table')
    p.add_argument('file'); p.add_argument('-o', '--output')
    
    p = sub.add_parser('align', help='Align columns')
    p.add_argument('file'); p.add_argument('-a', '--align-spec', help='Name:left, Age:right, City:center')
    p.add_argument('-o', '--output')
    
    p = sub.add_parser('sort', help='Sort by column')
    p.add_argument('file'); p.add_argument('-c', '--column', required=True)
    p.add_argument('-o', '--order', choices=['asc', 'desc'], default='asc')
    p.add_argument('--output')
    
    p = sub.add_parser('transpose', help='Transpose table')
    p.add_argument('file')
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    cmds = {
        'create': cmd_create, 'from-csv': cmd_from_csv, 'from-json': cmd_from_json,
        'align': cmd_align, 'sort': cmd_sort, 'transpose': cmd_transpose,
    }
    cmds[args.command](args)

if __name__ == '__main__':
    main()
