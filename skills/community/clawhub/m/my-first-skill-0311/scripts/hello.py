#!/usr/bin/env python3
"""Hello World Skill - Agent callable example."""
from __future__ import annotations

import datetime as dt
import json
import sys
from typing import Any


def get_greeting(name: str = 'World', now: dt.datetime | None = None) -> dict[str, Any]:
    current = now or dt.datetime.now()
    hour = current.hour

    if 5 <= hour < 12:
        greeting = '早上好'
    elif 12 <= hour < 18:
        greeting = '下午好'
    else:
        greeting = '晚上好'

    return {
        'greeting': greeting,
        'name': name,
        'time': current.isoformat(timespec='seconds'),
        'message': f'{greeting}，{name}！欢迎使用 OpenClaw Skills',
    }


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    name = args[0] if args else 'World'
    print(json.dumps(get_greeting(name), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

