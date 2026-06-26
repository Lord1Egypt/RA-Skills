#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
INDEX_DIR = ROOT / 'memory' / 'index'
REPORT_PATH = ROOT / 'memory' / 'reports' / 'phase2-dual-path-report-2026-03-28.md'


def main() -> int:
    thin_bytes = (INDEX_DIR / 'thin-index.json').stat().st_size
    packed_bytes = (INDEX_DIR / 'retrieval-view-packed.json').stat().st_size
    hot_bytes = (INDEX_DIR / 'retrieval-view-hot.json').stat().st_size

    thin_to_packed_pct = round(((thin_bytes - packed_bytes) / thin_bytes) * 100, 2) if thin_bytes else 0.0
    thin_to_hot_pct = round(((thin_bytes - hot_bytes) / thin_bytes) * 100, 2) if thin_bytes else 0.0

    lines = [
        '# Phase2 Dual-Path Retrieval Report · 2026-03-28',
        '',
        '## Recommended Strategy',
        '- fast_path: retrieval-view-hot.json',
        '- fallback_path: retrieval-view-packed.json',
        '- source_of_truth: thin-index.json',
        '',
        '## Size Metrics',
        f'- thin_index_bytes: {thin_bytes}',
        f'- packed_bytes: {packed_bytes}',
        f'- hot_only_bytes: {hot_bytes}',
        f'- thin_to_packed_reduction_pct: {thin_to_packed_pct}',
        f'- thin_to_hot_reduction_pct: {thin_to_hot_pct}',
        '',
        '## Decision',
        '- hot-only keeps core query coverage and is suitable for fast path',
        '- packed view preserves broader coverage and is suitable for fallback path',
        '- thin-index remains debugging/reference source',
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT_PATH),
        'fast_path': 'retrieval-view-hot.json',
        'fallback_path': 'retrieval-view-packed.json',
        'thin_to_hot_reduction_pct': thin_to_hot_pct,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
