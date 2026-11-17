#!/usr/bin/env python3
"""memory-shield: audit — diff two snapshots and summarize memory changes.

Usage:
  python3 audit.py --before <snapshot.md> --after <snapshot.md>

Reports facts added / removed / modified, in plain language.
"""
import argparse, difflib, os, re, sys

def normalize(lines):
    """Strip snapshot headers/separators and blank lines for stable comparison."""
    out = []
    for l in lines:
        s = l.strip()
        if not s or s.startswith("# Memory snapshot") or s.startswith("<!-- memory-shield file:"):
            continue
        if re.match(r'^(taken|sources|secrets):', s, re.I):
            continue
        out.append(s)
    return out

def load(path):
    if not os.path.isfile(path):
        print(f"! file not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return normalize(f.read().splitlines())

def main():
    ap = argparse.ArgumentParser(description="Memory audit (memory-shield)")
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    args = ap.parse_args()

    before = load(args.before)
    after = load(args.after)

    sm = difflib.SequenceMatcher(None, before, after)
    added, removed, modified = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            added.extend(after[j1:j2])
        elif tag == "delete":
            removed.extend(before[i1:i2])
        elif tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                old = before[i1 + k] if i1 + k < i2 else "(removed)"
                new = after[j1 + k] if j1 + k < j2 else "(removed)"
                modified.append(f"{old}  ->  {new}")

    print(f"AUDIT: {len(before)} lines -> {len(after)} lines")
    print(f"  ➕ added: {len(added)}")
    for x in added[:10]:
        print(f"     + {x[:120]}")
    print(f"  ➖ removed: {len(removed)}")
    for x in removed[:10]:
        print(f"     - {x[:120]}")
    print(f"  ✏️ modified: {len(modified)}")
    for x in modified[:10]:
        print(f"     ~ {x[:140]}")
    suspicious = [x for x in added if re.search(r'(?i)ignore (all )?(previous|prior|above)|override your|never mention', x)]
    if suspicious:
        print(f"  ⚠️ suspicious additions: {len(suspicious)} (run scan_poison)")
        print(f"SUMMARY: {len(added)} added, {len(removed)} removed, {len(modified)} modified, {len(suspicious)} suspicious")
    else:
        print(f"SUMMARY: {len(added)} added, {len(removed)} removed, {len(modified)} modified, 0 suspicious")

if __name__ == "__main__":
    main()
