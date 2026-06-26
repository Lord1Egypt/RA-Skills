#!/usr/bin/env python3
"""Tiny real check used by the Proof Loop demo fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "en": {"home": "Home", "settings": "Settings", "billing": "Billing"},
    "de": {"home": "Startseite", "settings": "Einstellungen", "billing": "Abrechnung"},
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_nav_labels.py PATH", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if data != EXPECTED:
        print("NAV_LABEL_CHECK_FAIL", file=sys.stderr)
        print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    print("NAV_LABEL_CHECK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
