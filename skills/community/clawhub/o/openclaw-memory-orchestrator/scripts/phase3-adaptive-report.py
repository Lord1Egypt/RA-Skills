#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import os

ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
REPORT = ROOT / 'memory' / 'reports' / 'phase3-adaptive-report-2026-03-28.md'
INDEX = ROOT / 'memory' / 'index'


def main():
    thin = (INDEX / 'thin-index.json').stat().st_size
    hot = (INDEX / 'retrieval-view-hot.json').stat().st_size
    packed = (INDEX / 'retrieval-view-packed.json').stat().st_size
    lines = [
        '# Phase3 Adaptive Retrieval Report · 2026-03-28',
        '',
        f'- thin_index_bytes: {thin}',
        f'- hot_only_bytes: {hot}',
        f'- packed_bytes: {packed}',
        '- router_mode: query-aware adaptive',
        '- miss_recovery: hot -> packed -> thin',
        '- production_policy: adaptive hot-first with recovery fallback',
    ]
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({
        'report': str(REPORT),
        'thin_index_bytes': thin,
        'hot_only_bytes': hot,
        'packed_bytes': packed,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
