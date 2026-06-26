#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

mods = ["selenium", "pandas", "bs4", "sqlalchemy", "pymysql"]
missing = []
for name in mods:
    try:
        __import__(name)
        print(f"ok: {name}")
    except Exception:
        print(f"missing: {name}")
        missing.append(name)

chromedriver = os.getenv("CHROMEDRIVER_PATH", "")
if chromedriver:
    p = Path(chromedriver)
    print(f"chromedriver: {'ok' if p.exists() else 'missing'} -> {chromedriver}")
else:
    print("chromedriver: not set (Chrome Selenium Manager may still work)")

print("ready" if not missing else "not-ready")
