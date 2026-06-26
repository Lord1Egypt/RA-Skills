#!/usr/bin/env python3
from __future__ import annotations

import json

from usage_rollup_lib import build_hourly_usage_payload


def main() -> int:
    payload = build_hourly_usage_payload()
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
