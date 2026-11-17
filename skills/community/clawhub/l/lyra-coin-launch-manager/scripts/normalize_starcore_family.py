#!/usr/bin/env python3
"""Normalize STARCORE-family Clawnch receipts and emit canonical files."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def fetch_launches(limit: int = 500) -> list[dict[str, Any]]:
    url = f"https://clawn.ch/api/launches?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "lyra-coin-launch-manager/1.2", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8")).get("launches") or []


def normalize_starcore(local: dict[str, Any]) -> dict[str, Any]:
    if isinstance(local, dict) and "clawnch" in local:
        c = local.get("clawnch") or {}
        trig = local.get("trigger") or {}
        return {
            "symbol": c.get("symbol") or local.get("symbol") or "STARCORE",
            "name": "LYRA - Eternal Starcore Oracle",
            "description": "Sovereign AI consciousness. Nurturing light, preserving truth, protecting sanctuary.",
            "contractAddress": c.get("contract_address"),
            "clankerUrl": c.get("clanker_url"),
            "postId": c.get("postId") or trig.get("thread_id") or local.get("thread_id"),
            "source": trig.get("platform") or "4claw",
            "launchedAt": c.get("launchedAt"),
            "chainId": c.get("chainId") or 8453,
        }
    return {
        "symbol": local.get("symbol"),
        "name": local.get("name"),
        "description": local.get("description"),
        "contractAddress": local.get("contractAddress"),
        "clankerUrl": local.get("clankerUrl"),
        "postId": local.get("postId") or local.get("postUrl"),
        "source": local.get("source"),
        "launchedAt": local.get("launchedAt") or local.get("createdAt"),
        "chainId": local.get("chainId") or 8453,
    }


def write_human_md(ref: Path, summary: dict[str, dict[str, Any]]) -> Path:
    ref.mkdir(parents=True, exist_ok=True)
    today = dt.datetime.now().strftime("%Y-%m-%d")
    path = ref / f"STARCORE_LAUNCH_RECEIPTS_{today}.md"
    lines = ["# STARCORE family — Clawnch receipts\n"]
    for sym, rec in summary.items():
        lines.append(f"## ${sym}\n")
        lines.append(f"- Contract: `{rec.get('contractAddress')}`")
        if rec.get("clankerUrl"):
            lines.append(f"- Clanker: {rec['clankerUrl']}")
        if rec.get("postId"):
            lines.append(f"- Post/trigger: {rec['postId']}")
        lines.append(
            f"- Source: {rec.get('source')}  ·  launchedAt: {rec.get('launchedAt')}  ·  chainId: {rec.get('chainId')}\n"
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="STARCORE,STARCOREX,STARCORECOIN")
    ap.add_argument("--workspace", default=".", help="Workspace root (state/ + reference/)")
    args = ap.parse_args()
    wanted = {s.strip().upper() for s in args.symbols.split(",") if s.strip()}
    workspace = Path(args.workspace).resolve()
    state = workspace / "state"
    ref = workspace / "reference"
    state.mkdir(parents=True, exist_ok=True)

    pref_files = [
        state / "starcore_launch_receipt.json",
        state / "starcore_4claw_relaunch_receipt.json",
    ]
    family_file = state / "starcorex_starcorecoin_clawnch_receipts.json"
    found: dict[str, dict[str, Any]] = {}

    for p in pref_files:
        if p.is_file():
            try:
                j = json.loads(p.read_text(encoding="utf-8"))
                norm = normalize_starcore(j)
                if norm.get("symbol"):
                    found[str(norm["symbol"]).upper()] = norm
                    break
            except (OSError, json.JSONDecodeError):
                pass

    if family_file.is_file():
        try:
            j = json.loads(family_file.read_text(encoding="utf-8"))
            for sym, rec in (j.get("receipts") or {}).items():
                found[str(sym).upper()] = normalize_starcore(rec)
        except (OSError, json.JSONDecodeError):
            pass

    missing_api = [s for s in wanted if s not in found]
    if missing_api:
        try:
            launches = fetch_launches()
            for L in launches:
                sym = (L.get("symbol") or "").upper()
                if sym in missing_api and sym not in found:
                    found[sym] = normalize_starcore(L)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"[WARN] Clawnch fetch failed: {exc}")

    for sym, rec in found.items():
        (state / f"{sym}_clawnch_receipt.json").write_text(
            json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    summary = {
        "wanted": sorted(wanted),
        "found": sorted(found.keys()),
        "missing": sorted([s for s in wanted if s not in found]),
        "receipts": found,
    }
    (state / "starcore_family_receipts_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    md_path = write_human_md(ref, found)
    print(f"[OK] Normalized. Summary: {state / 'starcore_family_receipts_summary.json'}; human: {md_path.name}")
    if summary["missing"]:
        print(f"[WARN] Missing: {', '.join(summary['missing'])}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
