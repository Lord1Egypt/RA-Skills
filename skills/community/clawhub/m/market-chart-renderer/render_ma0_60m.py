#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from render_chart import render_chart  # noqa: E402


def main() -> int:
    result = render_chart(symbol='MA0', period='60', limit=120, output_stem='ma0_60m_market_chart_renderer')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
