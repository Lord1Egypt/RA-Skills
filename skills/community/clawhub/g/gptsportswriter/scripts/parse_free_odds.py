#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


def extract_candidates(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = []
    pattern = re.compile(r'(?P<away>[A-Za-z0-9 .&\-]+)\s+(?:at|vs\.?|@)\s+(?P<home>[A-Za-z0-9 .&\-]+)', re.I)
    for line in lines:
        m = pattern.search(line)
        if m:
            out.append({
                "event": f"{m.group('away').strip()} at {m.group('home').strip()}",
                "raw": line,
            })
    return out


def main():
    ap = argparse.ArgumentParser(description="Parse rough public-odds text into event candidates")
    ap.add_argument("file", nargs="?", help="Input text file; stdin if omitted")
    args = ap.parse_args()

    if args.file:
        text = Path(args.file).read_text()
    else:
        text = sys.stdin.read()

    print(json.dumps({"events": extract_candidates(text)}, indent=2))


if __name__ == "__main__":
    main()
