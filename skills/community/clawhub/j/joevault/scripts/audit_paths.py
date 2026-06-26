#!/usr/bin/env python3
import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def iso(ts: float | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def windowsish(path: str) -> str:
    p = path.replace('/', '\\')
    if p.startswith('\\mnt\\'):
        parts = p.split('\\')
        if len(parts) >= 5:
            drive = parts[2].upper().rstrip(':')
            return f'{drive}:\\' + '\\'.join(parts[4:])
    return p


def latest_files(root: Path, limit: int = 10) -> list[dict]:
    items: list[tuple[float, str]] = []
    if not root.exists():
        return []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', '__pycache__'}]
        for name in files:
            fp = Path(base) / name
            try:
                mtime = fp.stat().st_mtime
            except OSError:
                continue
            items.append((mtime, str(fp)))
    items.sort(reverse=True)
    return [{'path': p, 'modified_at': iso(ts)} for ts, p in items[:limit]]


def path_size_bytes(root: Path) -> int:
    if not root.exists():
        return 0
    if root.is_file():
        return root.stat().st_size
    total = 0
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', '__pycache__'}]
        for name in files:
            fp = Path(base) / name
            try:
                total += fp.stat().st_size
            except OSError:
                pass
    return total


def summarize_path(path: Path, recent_limit: int) -> dict:
    if not path.exists() and not path.is_symlink():
        return {'path': str(path), 'exists': False}
    try:
        stat = path.lstat()
        mtime = stat.st_mtime
    except OSError:
        mtime = None
    info = {
        'path': str(path),
        'exists': path.exists() or path.is_symlink(),
        'is_dir': path.is_dir(),
        'is_file': path.is_file(),
        'is_symlink': path.is_symlink(),
        'symlink_target': str(path.resolve()) if path.is_symlink() else None,
        'modified_at': iso(mtime),
    }
    if path.exists():
        info['size_bytes'] = path_size_bytes(path)
        if path.is_dir():
            info['latest_files'] = latest_files(path, recent_limit)
    return info


def scan_refs(search_roots: Iterable[Path], patterns: list[re.Pattern[str]]) -> list[dict]:
    hits: list[dict] = []
    for root in search_roots:
        if not root.exists():
            continue
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next', '__pycache__'}]
            for name in files:
                fp = Path(base) / name
                try:
                    text = fp.read_text(encoding='utf-8', errors='ignore')
                except OSError:
                    continue
                matched = [p.pattern for p in patterns if p.search(text)]
                if matched:
                    hits.append({'file': str(fp), 'patterns': matched})
    return hits


def main() -> None:
    ap = argparse.ArgumentParser(description='Audit active and stale paths before quarantine.')
    ap.add_argument('--current-root', required=True)
    ap.add_argument('--stale-root', required=True)
    ap.add_argument('--candidate', action='append', required=True, help='Relative path to inspect under both roots')
    ap.add_argument('--search-root', action='append', default=[], help='Root to scan for stale path references')
    ap.add_argument('--recent-limit', type=int, default=10)
    args = ap.parse_args()

    current_root = Path(args.current_root)
    stale_root = Path(args.stale_root)
    stale_strings = [
        re.escape(str(stale_root)),
        re.escape(windowsish(str(stale_root))),
        re.escape(str(stale_root).replace('/mnt/c/', 'C:/').replace('/', '\\')),
    ]
    patterns = [re.compile(s) for s in dict.fromkeys(stale_strings)]

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'current_root': str(current_root),
        'stale_root': str(stale_root),
        'candidates': [],
        'reference_hits': scan_refs([Path(p) for p in args.search_root], patterns),
    }

    for rel in args.candidate:
        report['candidates'].append({
            'relative_path': rel,
            'current': summarize_path(current_root / rel, args.recent_limit),
            'stale': summarize_path(stale_root / rel, args.recent_limit),
        })

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
