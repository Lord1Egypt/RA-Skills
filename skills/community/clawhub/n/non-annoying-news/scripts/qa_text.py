#!/usr/bin/env python3
import re
import sys
from pathlib import Path

BANNED = [
    r'\bTODO\b', r'\bPLACEHOLDER\b', r'\bQA\b', r'\bqueue\b', r'\bfallback\b',
    r'\bprototype\b', r'\blorem\b', r'\binteresting\b', r'potentially relevant',
    r'worth watching', r'food for thought', r'click here', r'as an AI',
]
FILLER_HEADINGS = [
    r'>\s*(Glossary|Terms|Notes|Misc|Filler|Scratchpad)\s*<',
    r'>\s*(Stichwort|Kurzfakt|Belegarten|Sandbox)\s*<',
]
PRIVATE_PATTERNS = [
    r'/Users/[^\s<]+', r'~/.openclaw/[^\s<]+', r'channel:[A-Z0-9]+',
    r'\bslack\b.*\b(channel|id)\b', r'\btelegram\b.*\b(chat|id)\b',
    r'\bsignal\b.*\b(chat|id)\b',
]


def visible_text(raw: str) -> str:
    raw = re.sub(r'<script[\s\S]*?</script>', ' ', raw, flags=re.I)
    raw = re.sub(r'<style[\s\S]*?</style>', ' ', raw, flags=re.I)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', raw).strip()


def main(paths):
    failed = False
    for path in paths:
        p = Path(path)
        text = p.read_text(errors='ignore')
        flat = visible_text(text)
        print(f'== {p} ==')
        checks = [
            ('banned/process/filler', BANNED, flat),
            ('filler headings', FILLER_HEADINGS, text),
            ('private/portable-risk', PRIVATE_PATTERNS, flat),
        ]
        for label, patterns, hay in checks:
            hits = []
            for pat in patterns:
                if re.search(pat, hay, flags=re.I):
                    hits.append(pat)
            if hits:
                failed = True
                print(f'FAIL {label}: ' + ', '.join(hits))
            else:
                print(f'ok {label}')
        words = len(flat.split())
        print(f'visible_words={words}')
    return 1 if failed else 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: qa_text.py <html-or-text> [...]', file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
