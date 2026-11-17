#!/usr/bin/env python3
"""Instant escalation responder for `jevw run --escalate-cmd`.

Reads ONE escalation payload JSON on stdin, prints ONE decision JSON line.
- done_verify: ack DONE directly — the loop's own keyword gate is the judge
  (no LLM call; answering can never bypass that gate).
- everything else: ONE call to any OpenAI-compatible chat endpoint — the
  model layer is provider-agnostic (tested build: Xiaomi MiMo 2.6 flash).
  Configure via JEZW_ESCALER_URL / JEZW_ESCALER_MODEL / JEZW_ESCALER_API_KEY
  (keys are never printed). Any failure
  falls back to WAIT — this script must not crash the loop.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

# Provider-agnostic: the defaults are merely the tested build (Xiaomi MiMo 2.6 flash).
URL = os.environ.get("JEZW_ESCALER_URL", "https://token-plan-cn.xiaomimimo.com/v1/chat/completions")
MODEL = os.environ.get("JEZW_ESCALER_MODEL", "mimo-v2.6-flash")
OPS = {"CLICK", "TYPE_TEXT", "SELECT", "SCROLL_UP", "SCROLL_DOWN", "WAIT", "DONE", "BLOCKED"}
WAIT = {"op": "WAIT", "target": None, "confidence": 0.5, "value": None}


def fallback(reason: str) -> dict:
    return dict(WAIT, value=None) | {}


def chat(system: str, user: str) -> str:
    key = os.environ.get("JEZW_ESCALER_API_KEY")
    if not key:
        raise RuntimeError("JEZW_ESCALER_API_KEY missing")
    body = json.dumps({
        "model": MODEL, "temperature": 0,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]


def decide(payload: dict) -> dict:
    if payload.get("reason") == "done_verify":
        return {"op": "DONE", "target": None, "confidence": 0.95, "value": None}
    rows = payload.get("rows") or []
    table = "\n".join(
        f"{r.get('idx')} | {r.get('role')} | {(r.get('name') or r.get('value') or '')[:60]} | {','.join(r.get('ops') or [])}"
        for r in rows)
    hist = payload.get("history") or []
    tail = "\n".join(
        f"c{h.get('cycle')}: {h.get('op')} target={h.get('target')} src={h.get('source')} "
        f"res={h.get('result')} detail={str(h.get('detail'))[:60]}"
        for h in hist[-6:])
    system = (
        "You are the escalation judge of a browser-automation loop. Reply with ONLY one JSON object, "
        "no prose, no fences: {\"op\": ..., \"target\": ..., \"confidence\": <0..1>, \"value\": null}. "
        f"op must be one of {sorted(OPS)}. target must be an integer index from the table or null "
        "(null is required for WAIT/DONE/BLOCKED/SCROLL_*). Rules: while an answer is still generating, "
        "WAIT; when the goal is clearly met, DONE; when the last actions errored, prefer a different "
        "row or WAIT over repeating them; never invent indices.")
    user = (f"goal: {payload.get('goal')}\nreason for escalation: {payload.get('reason')}\n"
            f"state: {payload.get('state_sig')}\nelement table:\n{table}\nrecent history:\n{tail}")
    raw = chat(system, user)
    start, end = raw.find("{"), raw.rfind("}")
    d = json.loads(raw[start:end + 1])
    if d.get("op") not in OPS:
        raise ValueError(f"bad op {d.get('op')}")
    if d["op"] in ("WAIT", "DONE", "BLOCKED", "SCROLL_UP", "SCROLL_DOWN"):
        d["target"] = None
    elif d.get("target") is not None:
        d["target"] = int(d["target"])
    d.setdefault("confidence", 0.7)
    d.setdefault("value", None)
    return d


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        d = decide(payload)
    except Exception as e:  # noqa: BLE001 — never crash the loop
        print(f"jevw-escaler fallback: {e}", file=sys.stderr)
        d = dict(WAIT)
    print(json.dumps({k: d.get(k) for k in ("op", "target", "confidence", "value")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
