#!/usr/bin/env python3
"""Pull canonical launch receipts from Clawnch (HTTPS GET only).

Writes:
- <out>/<SYMBOL>_clawnch_receipt.json
- <out>/clawnch_receipts_summary.json

Usage:
  python pull_clawnch_receipts.py --symbols STARCORE,STARCOREX --out state
"""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

CLAUNCH_URL = "https://clawn.ch/api/launches?limit=500"


def fetch_launches(limit: int = 500) -> list[dict[str, Any]]:
    url = f"https://clawn.ch/api/launches?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "lyra-coin-launch-manager/1.2", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        j = json.loads(resp.read().decode("utf-8"))
    return j.get("launches") or []


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull Clawnch launch receipts (no credentials)")
    ap.add_argument("--symbols", required=True, help="Comma-separated symbols")
    ap.add_argument("--out", default="state", help="Output directory (created if missing)")
    args = ap.parse_args()

    wanted = {s.strip().upper() for s in args.symbols.split(",") if s.strip()}
    if not wanted:
        print("No symbols provided")
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        launches = fetch_launches()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[ERR] Clawnch fetch failed: {exc}")
        return 1

    found: dict[str, dict[str, Any]] = {}
    for L in launches:
        sym = (L.get("symbol") or "").upper()
        if sym in wanted and sym not in found:
            found[sym] = L

    summary = {
        "wanted": sorted(wanted),
        "found": sorted(found.keys()),
        "missing": sorted([s for s in wanted if s not in found]),
        "receipts": found,
        "source": CLAUNCH_URL,
    }

    for sym, rec in found.items():
        (out_dir / f"{sym}_clawnch_receipt.json").write_text(
            json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    (out_dir / "clawnch_receipts_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if summary["missing"]:
        print(f"[WARN] Missing: {', '.join(summary['missing'])}")
        return 2

    print(f"[OK] Receipts written for: {', '.join(sorted(found.keys()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
