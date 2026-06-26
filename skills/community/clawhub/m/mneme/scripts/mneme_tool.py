#!/usr/bin/env python3
# Copyright 2026 Casper Kwok
# Licensed under the Apache License, Version 2.0 (see ../LICENSE).
"""Mneme tool: spine projection / lint health-check / collision-free id allocation. Zero deps.

Solves the two review findings of Mneme v0.1:
- ID collision (P2): `new-id PREFIX` allocates deterministically (scan max+1); `lint` detects dups.
- seen/state rot (P1): `lint` flags `live` cells whose `seen` is older than DECAY_DAYS, and
  checks supersede link symmetry / dangling links — wire it into a pre-commit hook so lifecycle
  metadata can't silently rot (a probabilistic reader won't do the bookkeeping; let a machine).

Usage:
    python mneme_tool.py spine  [file]
    python mneme_tool.py lint   [file]      # exit code 1 on errors (for hooks)
    python mneme_tool.py new-id DEC [file]
If [file] omitted, uses the first *.mneme in the current directory.
"""
import datetime as _dt
import glob
import os
import re
import sys

DECAY_DAYS = 45          # live cell with seen older than this → lint flags "verify or mark stale"
WORK_STATES = ('live', 'stale')
REQUIRED = ('gist', 'state', 'since', 'seen')
REL_INVERSE = {'supersedes': 'superseded-by', 'superseded-by': 'supersedes'}


def parse(path):
    cells, cur = [], None
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if line.startswith('#'):
            continue
        if line.startswith('@'):
            if cur:
                cells.append(cur)
            m = re.match(r'@\s+(\S+)\s+(\S+)', line)
            cur = {'id': m.group(1) if m else line[1:].strip(),
                   'topic': m.group(2) if m else '', 'links': [], 'line': line}
            continue
        if cur is None:
            continue
        if line.startswith('>') or not line.strip():
            continue
        toks = line.split()
        i = 0
        while i < len(toks) - 1:
            k = toks[i]
            if k in ('state', 'conf', 'since', 'seen'):
                cur[k] = toks[i + 1]; i += 2; continue
            if k == 'gist' or k == 'cue':
                cur[k] = line.split(None, 1)[1]; break
            if k == 'link':
                if len(toks) >= 3:
                    cur['links'].append((toks[1], toks[2]))
                break
            i += 1
    if cur:
        cells.append(cur)
    return cells


def _default_file():
    hits = sorted(glob.glob('*.mneme')) or sorted(glob.glob('**/*.mneme', recursive=True))
    return hits[0] if hits else 'project.mneme'


def cmd_spine(path):
    for c in parse(path):
        if c.get('state') in WORK_STATES:
            print(f"{c['id']:<14} {c.get('state',''):<6} {c.get('gist','')}  [{c.get('topic','')}]")


def cmd_new_id(prefix, path):
    nums = [int(m.group(1)) for c in parse(path)
            if (m := re.match(rf'{re.escape(prefix)}-(\d+)$', c['id']))]
    print(f"{prefix}-{(max(nums) + 1 if nums else 1):04d}")


def cmd_lint(path):
    cells = parse(path)
    by_id, errors, warns = {}, [], []
    today = _dt.date.today()

    for c in cells:
        cid = c['id']
        if cid in by_id:
            errors.append(f"duplicate id: {cid}")
        by_id[cid] = c
        for f in REQUIRED:
            if f not in c:
                errors.append(f"{cid} missing required field: {f}")
        if c.get('state') == 'superseded' and not any(r == 'superseded-by' for r, _ in c['links']):
            warns.append(f"{cid} is superseded but has no superseded-by link")

    for c in cells:
        cid = c['id']
        seen = c.get('seen')
        if seen:
            try:
                age = (today - _dt.date.fromisoformat(seen)).days
                if c.get('state') == 'live' and age > DECAY_DAYS:
                    warns.append(f"{cid} live but seen {age}d ago → verify or mark stale")
            except ValueError:
                errors.append(f"{cid} invalid seen date: {seen}")
        for rel, tgt in c['links']:
            if tgt not in by_id:
                warns.append(f"{cid} link {rel} {tgt} → target not found")
            elif rel in REL_INVERSE:
                inv = REL_INVERSE[rel]
                if not any(r == inv and t == cid for r, t in by_id[tgt]['links']):
                    warns.append(f"{cid} {rel} {tgt}, but {tgt} lacks reverse {inv} {cid} (asymmetric)")

    for w in warns:
        print(f"  WARN {w}")
    for e in errors:
        print(f"  ERR  {e}")
    print(f"\nlint: {len(cells)} cells, {len(errors)} error, {len(warns)} warn")
    return 1 if errors else 0


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else 'lint'
    if cmd == 'new-id':
        cmd_new_id(args[1], args[2] if len(args) > 2 else _default_file())
    elif cmd == 'spine':
        cmd_spine(args[1] if len(args) > 1 else _default_file())
    elif cmd == 'lint':
        sys.exit(cmd_lint(args[1] if len(args) > 1 else _default_file()))
    else:
        print(__doc__); sys.exit(2)


if __name__ == '__main__':
    main()
