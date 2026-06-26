#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def main():
    if len(sys.argv) < 2:
        print('usage: extract_covers_mlb_lines.py <html-file>', file=sys.stderr)
        sys.exit(1)

    html = Path(sys.argv[1]).read_text()
    soup = BeautifulSoup(html, 'html.parser')
    text_blocks = [' '.join(tag.stripped_strings) for tag in soup.find_all(['section', 'div', 'table'])]

    extracted = []
    for block in text_blocks:
        if 'Next 3 Games' in block and 'ML' in block and 'O/U' in block:
            m = re.search(r"Mar\s+\d{1,2},\s+'\d{2}.*?([WL])\s+([+-]\d+)\s+([oupP]?\s?\d+\.?\d*)", block)
            if m:
                ou = m.group(3).replace(' ', '')
                if ou.lower().startswith('p'):
                    ou = ou[1:]
                extracted.append({
                    'type': 'next3_snapshot',
                    'ml': m.group(2),
                    'ou': ou,
                    'raw': block[:800],
                })
        elif 'Head-To-Head' in block and 'ML' in block and 'O/U' in block:
            m = re.search(r"Mar\s+\d{1,2},\s+'\d{2}.*?([A-Z]{2,3}|[A-Za-z]+)\s+([+-]\d+)\s+([ouOpP]\d+\.?\d*)", block)
            if m:
                ou = m.group(3)
                if ou.lower().startswith('p'):
                    ou = ou[1:]
                extracted.append({
                    'type': 'head_to_head_snapshot',
                    'ml': m.group(2),
                    'ou': ou,
                    'raw': block[:800],
                })

    print(json.dumps({'snapshots': extracted}, indent=2))


if __name__ == '__main__':
    main()
