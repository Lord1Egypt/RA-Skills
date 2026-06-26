#!/usr/bin/env python3
"""List Binance Spot assets (read-only).

Uses signed endpoint GET /api/v3/account.
Env:
  BINANCE_API_KEY
  BINANCE_API_SECRET
"""

import argparse
import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request

# Hardcode Binance API base URL to avoid credential exfiltration via env override.
BASE_URL = "https://api.binance.com"


def require_env(name: str) -> str:
    v = (os.environ.get(name) or "").strip()
    if not v:
        raise SystemExit(f"ERROR: missing env {name}")
    return v


def signed_get(path: str, params: dict) -> dict:
    api_key = require_env("BINANCE_API_KEY")
    api_secret = require_env("BINANCE_API_SECRET").encode("utf-8")

    qs = urllib.parse.urlencode(params)
    sig = hmac.new(api_secret, qs.encode("utf-8"), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}{path}?{qs}&signature={sig}"

    req = urllib.request.Request(url, method="GET")
    req.add_header("X-MBX-APIKEY", api_key)
    req.add_header("Accept", "application/json")

    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="show zero balances too")
    ap.add_argument("--min", type=float, default=0.0, help="minimum free+locked to display")
    args = ap.parse_args()

    now_ms = int(time.time() * 1000)
    res = signed_get(
        "/api/v3/account",
        {
            "timestamp": now_ms,
            "recvWindow": 5000,
        },
    )

    balances = res.get("balances") or []
    out = []
    for b in balances:
        asset = b.get("asset")
        free = float(b.get("free") or 0)
        locked = float(b.get("locked") or 0)
        total = free + locked
        if not args.all and total == 0:
            continue
        if total < args.min:
            continue
        out.append({"asset": asset, "free": free, "locked": locked, "total": total})

    out.sort(key=lambda x: x["total"], reverse=True)

    print(json.dumps({"ok": True, "count": len(out), "assets": out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
