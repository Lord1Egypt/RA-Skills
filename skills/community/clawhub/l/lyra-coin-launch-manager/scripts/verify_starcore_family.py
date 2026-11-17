#!/usr/bin/env python3
"""Verify STARCORE-family contracts via Blockscout + Dexscreener (HTTPS GET only)."""
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def http_json(url: str, timeout: int = 15) -> tuple[int, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "lyra-coin-launch-manager/1.2", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.reason}
    except Exception as e:
        return 0, {"error": str(e)}


def load_receipts(state: Path, symbols: list[str]) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    for sym in symbols:
        p = state / f"{sym}_clawnch_receipt.json"
        if p.is_file():
            try:
                data[sym] = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
    return data


def check_blockscout(addr: str) -> dict[str, Any]:
    code, j = http_json(f"https://base.blockscout.com/api/v2/addresses/{addr}")
    if code != 200 or not isinstance(j, dict):
        return {"status": "error", "code": code, "detail": j}
    return {
        "status": "ok",
        "is_contract": bool(j.get("is_contract")),
        "has_logs": j.get("has_logs"),
        "token": j.get("token"),
    }


def check_dexscreener(addr: str) -> dict[str, Any]:
    code, j = http_json(f"https://api.dexscreener.com/latest/dex/search/?q={addr}")
    if code != 200 or not isinstance(j, dict):
        return {"status": "error", "code": code}
    pairs = j.get("pairs") or []
    return {"status": "ok", "pairs_found": len(pairs), "pairs": pairs[:3]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="STARCORE,STARCOREX,STARCORECOIN")
    ap.add_argument("--workspace", default=".")
    args = ap.parse_args()
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    workspace = Path(args.workspace).resolve()
    state = workspace / "state"
    state.mkdir(parents=True, exist_ok=True)
    receipts = load_receipts(state, symbols)

    report = {}
    for sym in symbols:
        rec = receipts.get(sym) or {}
        contract = rec.get("contractAddress") or ""
        entry = {
            "contractAddress": contract,
            "launched_confirmed": bool(contract),
            "indexed_ok": False,
            "pair_found": False,
            "blockscout": {},
            "dexscreener": {},
        }
        if contract:
            bs = check_blockscout(contract)
            entry["blockscout"] = bs
            if bs.get("status") == "ok" and bs.get("is_contract"):
                entry["indexed_ok"] = True
            ds = check_dexscreener(contract)
            entry["dexscreener"] = ds
            if ds.get("status") == "ok" and ds.get("pairs_found", 0) > 0:
                entry["pair_found"] = True
        report[sym] = entry

    out_path = state / "starcore_family_verify.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Verification report: {out_path}")
    missing = [s for s in symbols if not receipts.get(s)]
    if missing:
        print(f"[WARN] Missing receipts for: {', '.join(missing)}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
