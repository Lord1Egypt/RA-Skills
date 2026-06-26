#!/usr/bin/env python3
"""
补完计划 — 将搜索结果/补充资料格式化为 KG 标准章节，追加到笔记末尾。

Usage:
    type search_results.txt | python enrichment.py <note.md>
    python enrichment.py <note.md> --text "补充内容..."
    python enrichment.py <note.md> --stdout

Output: 默认追加回文件，--stdout 仅打印
"""
import re, sys, os


def parse_frontmatter(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    if not raw.startswith('---'):
        return {}, raw, 0
    # Find closing --- in raw directly to avoid lstrip offset bug
    close_idx = raw.find('\n---', 3)
    if close_idx == -1:
        return {}, raw, 0
    yaml_block = raw[3:close_idx].strip()
    fields = {}
    for line in yaml_block.split('\n'):
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    body_start = close_idx + 5
    return fields, raw[body_start:], body_start


def detect_type(fields: dict) -> str:
    raw_tags = fields.get('tags', '')
    m = re.match(r'\[?\s*(\S+?)\s*\]?', raw_tags)
    return m.group(1) if m else 'unknown'


def normalize_path(p: str) -> str:
    p = p.strip()
    m = re.match(r'^/([a-zA-Z])/(.*)', p)
    if m and os.name == 'nt':
        p = f"{m.group(1).upper()}:/{m.group(2)}"
    return os.path.abspath(p)


def dedup_lines(new: list[str], existing: str) -> list[str]:
    """Filter out lines that already exist in body."""
    return [l for l in new if l.strip() and l.strip() not in existing]


def format_concept(text: str, body: str) -> str:
    items = dedup_lines(text.strip().split('\n'), body)
    if not items:
        return ''
    out = []
    if '## 来源' not in body:
        out.append('\n## 来源\n')
    for item in items:
        out.append(f'- {item.strip()}')
    return '\n'.join(out)


def format_relation(text: str, body: str) -> str:
    if body.strip():
        return ''
    first = text.strip().split('\n')[0].strip()
    return first if first else ''


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(f"USAGE: python {__file__} <note.md> [--stdout] [--text ...]", file=sys.stderr)
        sys.exit(1)

    filepath = normalize_path(sys.argv[1])
    if not os.path.exists(filepath):
        print(f"ERROR: not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    to_stdout = '--stdout' in sys.argv
    explicit = None
    if '--text' in sys.argv:
        idx = sys.argv.index('--text')
        if idx + 1 < len(sys.argv):
            explicit = sys.argv[idx + 1]

    fields, body, _ = parse_frontmatter(filepath)
    ntype = detect_type(fields)

    if explicit:
        source = explicit
    elif not sys.stdin.isatty():
        source = sys.stdin.read()
    else:
        print("ERROR: pipe text or use --text", file=sys.stderr)
        sys.exit(1)

    if not source.strip():
        sys.exit(0)

    fmts = {'概念': format_concept, '关系': format_relation}
    fmter = fmts.get(ntype, format_concept)
    output = fmter(source, body)

    if not output.strip():
        print("SKIP: no new content", file=sys.stderr)
        sys.exit(0)

    if to_stdout:
        print(output)
    else:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write('\n' + output if '\n## ' not in output else output)
        print(f"DONE: appended to {filepath}", file=sys.stderr)


if __name__ == '__main__':
    main()
