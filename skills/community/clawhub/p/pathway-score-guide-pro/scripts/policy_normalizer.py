#!/usr/bin/env python3
"""Normalize simple rule text into the policy schema.

This is intentionally conservative: it produces a starter YAML-like JSON object
for manual editing rather than pretending to perfectly parse school/unit rules.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys

KEYWORDS = {
    'hard_requirements': ['须', '必须', '应当', '条件', '资格', '不得'],
    'materials': ['材料', '提交', '附件', '证明', '推荐信', '公示'],
    'timeline': ['时间', '截止', '报名', '确认', '复试', '评审', '公示'],
}


def split_lines(text: str):
    return [line.strip() for line in text.splitlines() if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    args = ap.parse_args()
    text = pathlib.Path(args.input).read_text(encoding='utf-8')
    lines = split_lines(text)
    out = {
        'meta': {'document_title': pathlib.Path(args.input).name},
        'hard_requirements': [],
        'competitive_items': [],
        'materials': {'required': [], 'optional': []},
        'timeline': [],
        'risks': [],
        'notes': [],
    }
    for line in lines:
        if any(k in line for k in KEYWORDS['hard_requirements']):
            out['hard_requirements'].append({'item': line, 'satisfied': 'unknown', 'evidence': ''})
        elif any(k in line for k in KEYWORDS['materials']):
            out['materials']['required'].append(line)
        elif any(k in line for k in KEYWORDS['timeline']):
            out['timeline'].append({'stage': line[:20], 'deadline': '', 'note': line})
        else:
            out['notes'].append(line)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
