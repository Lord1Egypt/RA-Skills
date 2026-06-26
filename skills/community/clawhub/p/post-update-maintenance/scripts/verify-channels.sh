#!/usr/bin/env bash
# verify-channels.sh <profile>
#
# Diff the pre-flight channel snapshot against current state. Reports:
#   OK_HEALTHY    <channel-id>           - healthy before and after
#   RECOVERED     <channel-id>           - unhealthy before, healthy now
#   BROKE         <channel-id> <reason>  - healthy before, unhealthy now (bad)
#   STILL_BROKEN  <channel-id> <reason>  - unhealthy before, unhealthy now
#
# Exit:
#   0 always (advisory). The caller decides how loud to be about BROKE lines.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_lib.sh
source "$SCRIPT_DIR/_lib.sh"

PROFILE="${1:-}"
if [ -z "$PROFILE" ]; then
  echo "usage: verify-channels.sh <profile>" >&2
  exit 2
fi

STATE="$(pum_state_dir "$PROFILE")"
RUN="$(pum_run_id)"

# Capture the after-snapshot.
AFTER="$STATE/snapshots/channels-after.$RUN.json"
openclaw --profile "$PROFILE" channels status --json > "$AFTER" 2>/dev/null \
  || echo '{}' > "$AFTER"

# Pick the most recent before-snapshot.
BEFORE="$(ls -t "$STATE/snapshots"/channels-before.*.json 2>/dev/null | head -1)"
if [ -z "$BEFORE" ] || [ ! -r "$BEFORE" ]; then
  echo "BLOCKED no-pre-snapshot: run preflight.sh first" >&2
  exit 2
fi

BEFORE="$BEFORE" AFTER="$AFTER" python3 <<'PY'
import json, os, sys

def load(p):
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return {}

def channels(d):
    # Try several plausible shapes; default to a flat list of objects with
    # id/health fields.
    if isinstance(d, dict):
        if isinstance(d.get("channels"), list):
            return d["channels"]
        if isinstance(d.get("data"), list):
            return d["data"]
        # Dict keyed by id.
        out = []
        for k, v in d.items():
            if isinstance(v, dict):
                v = dict(v)
                v.setdefault("id", k)
                out.append(v)
        return out
    if isinstance(d, list):
        return d
    return []

def is_healthy(c):
    h = (c.get("health") or "").lower()
    s = (c.get("status") or "").lower()
    conn = (c.get("connected") if c.get("connected") is not None else (c.get("connectionStatus") or "")).__str__().lower()
    if h:
        return h in ("healthy", "ok", "running")
    if conn in ("true", "connected"):
        return True
    if s in ("connected", "running", "healthy", "ok"):
        return True
    return False

def reason(c):
    return (c.get("error") or c.get("statusText") or c.get("status") or "no-reason").strip()

before = {c.get("id") or c.get("name"): c for c in channels(load(os.environ["BEFORE"])) if c.get("id") or c.get("name")}
after  = {c.get("id") or c.get("name"): c for c in channels(load(os.environ["AFTER"]))  if c.get("id") or c.get("name")}

all_ids = sorted(set(before) | set(after))
for cid in all_ids:
    b = before.get(cid)
    a = after.get(cid)
    b_ok = bool(b and is_healthy(b))
    a_ok = bool(a and is_healthy(a))
    if not a:
        # Disappeared after — treat as broken.
        print(f"BROKE {cid} channel-disappeared")
        continue
    if b_ok and a_ok:
        print(f"OK_HEALTHY {cid}")
    elif not b_ok and a_ok:
        print(f"RECOVERED {cid}")
    elif b_ok and not a_ok:
        print(f"BROKE {cid} {reason(a)}")
    else:
        print(f"STILL_BROKEN {cid} {reason(a)}")
PY
