#!/usr/bin/env python3
"""gmail-cleanup - read-only triage scan (v4, hardened).

Pulls candidate inbox messages for the configured scope and emits a normalized
JSON file (state/gmail-cleanup/latest.json) for the agent to classify.
Performs NO mutations.

Credentials: read from the GOG_KEYRING_PASSWORD environment variable ONLY. This
script never reads credential files. The Workspace CLI is invoked as `gog` from
PATH; no executable override is honored.

Hardening:
  * retry + exponential backoff on Gmail `403 rateLimitExceeded` / quota errors
  * optional pacing between API requests (GMAIL_CLEANUP_PACE_MS, default 250ms)
  * malformed / partial responses are skipped, never fatal
  * emits a `skipped` count alongside `count`

Env: GMAIL_CLEANUP_STATE, GMAIL_CLEANUP_CONFIG, GOG_KEYRING_PASSWORD,
     GMAIL_CLEANUP_PACE_MS, GMAIL_CLEANUP_RETRIES
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

GOG = "gog"
STATE = os.environ.get(
    "GMAIL_CLEANUP_STATE",
    os.path.expanduser("~/.openclaw/workspace/state/gmail-cleanup"),
)
CFG = os.environ.get("GMAIL_CLEANUP_CONFIG", os.path.join(STATE, "config.json"))
PACE_MS = int(os.environ.get("GMAIL_CLEANUP_PACE_MS", "250"))
RETRIES = int(os.environ.get("GMAIL_CLEANUP_RETRIES", "4"))

RATE_HINTS = (
    "ratelimitexceeded",
    "quota exceeded",
    "too many requests",
    "user-rate limit",
    "429",
)

if not os.environ.get("GOG_KEYRING_PASSWORD"):
    sys.exit(
        "GOG_KEYRING_PASSWORD is not set. Export it before running; this skill "
        "intentionally does not read credential files itself."
    )

os.makedirs(STATE, exist_ok=True)
if not os.path.exists(CFG):
    sys.exit(f"config not found: {CFG} (copy templates/config.example.json)")

cfg = json.load(open(CFG))
acc = cfg["account"]
scope = cfg.get("scope", {})
scan_max = cfg.get("limits", {}).get("scanMax", 40)


class GogError(Exception):
    """Non-retryable gog failure (or retries exhausted)."""


def _is_rate_limited(blob):
    low = blob.lower()
    return any(h in low for h in RATE_HINTS)


def gog_json(args, retries=RETRIES):
    """Run `gog <args> -a <acc> -j` and return parsed JSON.

    Retries with exponential backoff on rate-limit responses; raises GogError on
    other failures or once retries are exhausted. May raise json.JSONDecodeError
    for a truncated/mangled body so the caller can skip that item.
    """
    delay = 2.0
    last = ""
    for attempt in range(retries + 1):
        r = subprocess.run([GOG, *args, "-a", acc, "-j"], capture_output=True, text=True)
        out, err = r.stdout, r.stderr
        if r.returncode == 0:
            return json.loads(out)
        blob = f"{err}\n{out}".strip()
        last = blob
        if _is_rate_limited(blob) and attempt < retries:
            time.sleep(delay)
            delay = min(delay * 2, 30)
            continue
        break
    raise GogError(last or "gog failed")


def header_map(payload):
    """Case-insensitive header lookup; tolerates missing/malformed entries."""
    out = {}
    for h in payload.get("headers") or []:
        if not isinstance(h, dict):
            continue
        name = h.get("name")
        if not name:
            continue
        out[str(name).lower()] = h.get("value", "")
    return out


queries = [scope.get("query", "in:inbox")] + list(scope.get("extraQueries", []))
seen, threads, search_errors = set(), [], []
for q in queries:
    try:
        res = gog_json(["gmail", "search", q, "--max", str(scan_max)])
    except (GogError, json.JSONDecodeError) as e:
        search_errors.append(f"{q}: {e}")
        continue
    for t in res.get("threads") or []:
        if not isinstance(t, dict):
            continue
        tid = t.get("id")
        if tid and tid not in seen:
            seen.add(tid)
            threads.append(t)
    time.sleep(PACE_MS / 1000.0)

if not threads and search_errors:
    sys.exit("gog search failed: " + "; ".join(search_errors))

candidates, skipped = [], 0
for t in threads:
    try:
        d = gog_json(["gmail", "get", t["id"]])
        payload = (d.get("message") or {}).get("payload") or {}
        hdrs = header_map(payload)
        norm = d.get("headers") or {}
        if not isinstance(norm, dict):
            norm = {}
        candidates.append({
            "id": t["id"],
            "date": t.get("date"),
            "internalDateIso": t.get("internalDateIso"),
            "from": t.get("from", ""),
            "subject": t.get("subject", ""),
            "labels": t.get("labels", []),
            "messageCount": t.get("messageCount", 1),
            "replyTo": norm.get("reply_to", ""),
            "listUnsubscribe": bool(hdrs.get("list-unsubscribe")),
            "precedence": hdrs.get("precedence", ""),
            "authResults": (hdrs.get("authentication-results", "") or "")[:400],
            "snippet": ((d.get("body") or "").strip())[:800],
        })
    except (GogError, json.JSONDecodeError, KeyError, TypeError, AttributeError):
        skipped += 1
        continue
    finally:
        time.sleep(PACE_MS / 1000.0)

out = {
    "generatedAt": datetime.now(timezone.utc).isoformat(),
    "account": acc,
    "queries": queries,
    "count": len(candidates),
    "skipped": skipped,
    "candidates": candidates,
}
with open(os.path.join(STATE, "latest.json"), "w") as f:
    json.dump(out, f, indent=2)
print(
    f"triage-scan: {len(candidates)} candidates ({skipped} skipped) "
    f"-> {os.path.join(STATE, 'latest.json')}"
)
