#!/usr/bin/env python3
"""
Hong Kong MTR Next Train Sync Stations Script
Version: 1.0.0
Created: 2026-03-18

Changelog:
v1.0.0 - 2026-03-18 (Initial version)
- Sync MTR lines & stations CSV to local skill directory.
"""

import os
from urllib.request import Request, urlopen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(BASE_DIR, "mtr_lines_and_stations.csv")
SRC_URL = "https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv"


def sync():
    req = Request(SRC_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as r:
        data = r.read()
    with open(OUT_CSV, "wb") as f:
        f.write(data)
    print(f"Synced: {OUT_CSV}")


if __name__ == "__main__":
    sync()
