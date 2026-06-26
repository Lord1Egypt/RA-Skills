#!/usr/bin/env python3
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def load_env(path: str) -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):]
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ[k] = v


def main() -> int:
    if len(sys.argv) < 3:
        print('usage: run_with_env.py <envfile> <script> [args...]', file=sys.stderr)
        return 2
    envfile = sys.argv[1]
    script = sys.argv[2]
    args = sys.argv[2:]
    load_env(envfile)
    sys.argv = args
    runpy.run_path(script, run_name='__main__')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
