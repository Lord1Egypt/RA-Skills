#!/usr/bin/env python3
import json
import re
import sys


def variants(username: str):
    u = username.strip()
    out = []
    seen = set()

    def add(x):
        if x and x not in seen:
            seen.add(x)
            out.append(x)

    add(u)
    add(u.lower())

    collapsed = re.sub(r'[_.-]+', '', u)
    add(collapsed)

    if '_' in u or '.' in u or '-' in u:
        parts = re.split(r'[_.-]+', u)
        if len(parts) > 1:
            add('.'.join(parts))
            add('-'.join(parts))
            add('_'.join(parts))

    trimmed = re.sub(r'\d+$', '', u)
    if trimmed and trimmed != u:
        add(trimmed)
        add(trimmed.lower())

    return out[:8]


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: generate_variants.py <username>"}))
        return
    print(json.dumps({"input": sys.argv[1], "variants": variants(sys.argv[1])}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
