#!/usr/bin/env python3
"""Classify which model endpoints an OpenClaw agent is configured to use, and
which ones actually served recent turns.

Evidence level: CLAIMED. This reads local config and the public NEAR endpoint
catalog. It proves nothing cryptographically — see SKILL.md.

Usage:
  check.py              classify the configured model chain
  check.py --served     what actually served recent turns (from gateway logs)
  check.py --json       machine-readable output
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ENDPOINTS_URL = "https://completions.near.ai/endpoints"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "nearai-verify"
CACHE_TTL = 86400  # the TEE fleet changes rarely; a day is plenty

CONFIG = Path(os.environ.get("OPENCLAW_CONFIG_PATH", Path.home() / ".openclaw" / "openclaw.json"))
LOG_DIR = Path("/tmp/openclaw")

# state -> (icon, label, private?)
STATES = {
    "tee_direct": ("[TEE]", "TEE-direct", True),
    "tee_gateway": ("[tee]", "TEE via gateway", True),
    "near_proxied": ("[!!]", "NEAR-proxied, NOT private", False),
    "not_near": ("[XX]", "not NEAR, not private", False),
    "unknown": ("[??]", "unknown", False),
}


def load_tee_catalog() -> dict[str, str]:
    """Map model id -> TEE hostname. Cached; falls back to stale cache offline."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / "endpoints.json"
    if cached.exists() and time.time() - cached.stat().st_mtime < CACHE_TTL:
        return json.loads(cached.read_text())
    try:
        with urllib.request.urlopen(ENDPOINTS_URL, timeout=15) as r:
            data = json.loads(r.read())
        out = {m: e["domain"] for e in data.get("endpoints", []) for m in e.get("models", [])}
        cached.write_text(json.dumps(out))
        return out
    except Exception:
        if cached.exists():
            return json.loads(cached.read_text())  # stale beats nothing
        return {}


def classify(base_url: str | None, bare_model: str, tee: dict[str, str]) -> str:
    if not base_url:
        return "not_near"  # built-in provider (openai, anthropic, ...)
    host = re.sub(r"^https?://", "", base_url).split("/")[0]
    if host.endswith(".completions.near.ai"):
        return "tee_direct"
    if host in ("cloud-api.near.ai", "api.near.ai"):
        return "tee_gateway" if bare_model in tee else "near_proxied"
    return "not_near"


def resolve(model_ref: str, cfg: dict, tee: dict[str, str]) -> dict:
    """model_ref is 'provider/model' where model may itself contain slashes."""
    provider, _, bare = model_ref.partition("/")
    pcfg = cfg.get("models", {}).get("providers", {}).get(provider, {})
    base = pcfg.get("baseUrl")
    for entry in pcfg.get("models", []):  # per-model baseUrl wins
        if entry.get("id") == bare and entry.get("baseUrl"):
            base = entry["baseUrl"]
            break
    state = classify(base, bare, tee)
    return {
        "ref": model_ref,
        "endpoint": re.sub(r"^https?://", "", base).split("/")[0] if base else "provider default",
        "state": state,
    }


def read_config() -> dict:
    if not CONFIG.exists():
        sys.exit(f"No OpenClaw config at {CONFIG}")
    return json.loads(CONFIG.read_text())


def cmd_config(as_json: bool) -> int:
    cfg = read_config()
    tee = load_tee_catalog()
    model = cfg.get("agents", {}).get("defaults", {}).get("model", {})
    chain = [("primary", model.get("primary"))]
    chain += [(f"fallback#{i}", m) for i, m in enumerate(model.get("fallbacks", []), 1)]
    chain = [(role, ref) for role, ref in chain if ref]

    rows = [dict(role=role, **resolve(ref, cfg, tee)) for role, ref in chain]
    leaks = [r for r in rows if not STATES[r["state"]][2]]

    if as_json:
        print(json.dumps({"level": "claimed", "chain": rows,
                          "chain_leaves_tee": bool(leaks)}, indent=2))
        return 0

    print("NEAR AI verification - level: CLAIMED")
    print("(read from local config; nothing cryptographically verified)\n")
    if not tee:
        print("  ! endpoint catalog unavailable and no cache - results may be wrong\n")
    width = max(len(r["ref"]) for r in rows)
    for r in rows:
        icon, label, _ = STATES[r["state"]]
        print(f"  {r['role']:<11} {icon:<5} {label:<26} {r['ref']:<{width}}  {r['endpoint']}")

    print()
    if leaks:
        first = leaks[0]
        print(f"  WARNING: chain leaves the TEE at {first['role']} ({first['ref']}).")
        print("  A failover sends your prompt outside the enclave.")
    else:
        print("  Every model in the chain is a NEAR TEE endpoint.")
    print("\n  This does not prove the endpoint is genuine TEE hardware.")
    print("  That needs an attestation check - not yet implemented (see SKILL.md).")
    return 1 if leaks else 0


def cmd_served(as_json: bool, limit: int) -> int:
    cfg = read_config()
    tee = load_tee_catalog()
    logs = sorted(LOG_DIR.glob("openclaw-*.log"))
    if not logs:
        sys.exit(f"No gateway logs in {LOG_DIR}")

    pat = re.compile(r"\[model-fetch\] start provider=(\S+) \S+ model=(\S+) \S+ url=(\S+)")
    seen: list[dict] = []
    for line in reversed(logs[-1].read_text(errors="replace").splitlines()):
        try:
            msg = json.loads(line).get("message", "")
        except Exception:
            continue
        m = pat.search(msg)
        if not m:
            continue
        provider, bare, url = m.groups()
        seen.append({
            "ref": f"{provider}/{bare}",
            "endpoint": re.sub(r"^https?://", "", url).split("/")[0],
            "state": classify(url, bare, tee),
            "time": json.loads(line).get("time", "")[11:19],
        })
        if len(seen) >= limit:
            break

    if as_json:
        print(json.dumps({"level": "claimed", "served": seen}, indent=2))
        return 0

    if not seen:
        print("No model calls found in today's log.")
        return 0
    print(f"Last {len(seen)} turns actually served - level: CLAIMED\n")
    for s in seen:
        icon, label, _ = STATES[s["state"]]
        print(f"  {s['time']}  {icon:<5} {label:<26} {s['ref']}  {s['endpoint']}")
    outside = [s for s in seen if not STATES[s["state"]][2]]
    print()
    print(f"  WARNING: {len(outside)} of {len(seen)} turns ran outside a TEE."
          if outside else "  All recent turns ran on NEAR TEE endpoints.")
    return 1 if outside else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Check which endpoints an OpenClaw agent uses.")
    ap.add_argument("--served", action="store_true", help="what actually served recent turns")
    ap.add_argument("--limit", type=int, default=10, help="turns to show with --served")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    return cmd_served(a.json, a.limit) if a.served else cmd_config(a.json)


if __name__ == "__main__":
    sys.exit(main())
