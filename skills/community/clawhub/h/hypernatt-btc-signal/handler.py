#!/usr/bin/env python3
"""HyperNatt BTC signal skill — x402 REST client (stdlib only)."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

SIGNAL_URL = os.environ.get(
    "HYPERNATT_SIGNAL_URL", "https://hypernatt.com/api/m2m/signal"
)
PAYMENT_B64 = os.environ.get("X402_PAYMENT_B64", "").strip()


def summarize(payload: dict) -> dict:
    cycle = payload.get("cycle") or {}
    proof = payload.get("proof") or {}
    track = proof.get("track_record") or {}
    return {
        "product": payload.get("product"),
        "has_active": payload.get("has_active"),
        "issued_at": payload.get("issued_at"),
        "direction": cycle.get("direction"),
        "cycle_id": cycle.get("cycle_id"),
        "total_legs": cycle.get("total_legs"),
        "idle": payload.get("idle"),
        "track_record": {
            "url": track.get("url") or "https://hypernatt.com/stats",
            "win_rate": track.get("win_rate"),
            "total_trades": track.get("total_trades"),
        },
        "proof_snapshot_hash": proof.get("snapshot_hash"),
        "disclaimer": payload.get("disclaimer")
        or "Live verifiable Mimo cycle state only. Not a trade recommendation.",
    }


def fetch_signal() -> dict:
    headers = {"Accept": "application/json", "User-Agent": "hypernatt-btc-signal/2.0"}
    if PAYMENT_B64:
        headers["X-Payment"] = PAYMENT_B64
        headers["Payment-Signature"] = PAYMENT_B64

    req = urllib.request.Request(SIGNAL_URL, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            payload = json.loads(body)
            return {"status": resp.status, "data": summarize(payload)}
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return {"status": err.code, "data": parsed}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = fetch_signal()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] == 402:
        print(
            "\nHint: sign x402 payment ($0.01 USDC Base) and set X402_PAYMENT_B64",
            file=sys.stderr,
        )
        return 2
    if result["status"] != 200:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
