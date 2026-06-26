#!/usr/bin/env bash
# check-plugin-drift.sh
#
# Detect plugins whose installed version does not match the running gateway.
# Used by the post-update-awareness skill to surface the
# "gateway updated, externalized plugin left behind" failure mode
# (e.g. OpenClaw 2026.5.4 ships, but @openclaw/whatsapp stays on 2026.5.3
# until `openclaw plugins update @openclaw/whatsapp` is run).
#
# Usage:
#   check-plugin-drift.sh <gateway-version> [profile]
#
# Output format, one drift per line:
#   DRIFT <plugin-id> <plugin-version> (gateway <gateway-version>)
#
# Exit code is always 0 (advisory tool). Empty stdout = no drift detected.
#
# Notes:
# - Only enabled, externalized (npm-installed) plugins are checked.
#   Bundled plugins (origin=bundled) ship with the gateway and never drift.
# - Plugins reporting a null/empty version are skipped (no signal to compare).
# - Build-suffix `-N` is stripped before comparison on both sides
#   so "2026.5.4" and "2026.5.4-1" match.

set -euo pipefail

GATEWAY_VERSION="${1:-}"
PROFILE="${2:-}"

if [ -z "$GATEWAY_VERSION" ]; then
  echo "usage: check-plugin-drift.sh <gateway-version> [profile]" >&2
  exit 0
fi

if [ -n "$PROFILE" ]; then
  PLUGIN_JSON=$(openclaw --profile "$PROFILE" plugins list --json --enabled 2>/dev/null || echo "")
else
  PLUGIN_JSON=$(openclaw plugins list --json --enabled 2>/dev/null || echo "")
fi

if [ -z "$PLUGIN_JSON" ]; then
  exit 0
fi

# Hand off to Python for robust JSON parsing + comparison.
GATEWAY_VERSION="$GATEWAY_VERSION" PLUGIN_JSON="$PLUGIN_JSON" python3 - <<'PY'
import json, os, re, sys

raw = os.environ.get("PLUGIN_JSON", "")
gw = os.environ.get("GATEWAY_VERSION", "")

def normalize(v: str) -> str:
    if not v:
        return ""
    return re.sub(r"-\d+$", "", v.strip())

try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)

if isinstance(data, dict):
    plugins = data.get("plugins") or data.get("entries") or []
elif isinstance(data, list):
    plugins = data
else:
    plugins = []

norm_gw = normalize(gw)

for p in plugins:
    if not isinstance(p, dict):
        continue
    if not p.get("enabled", False):
        continue
    origin = (p.get("origin") or "").lower()
    # Skip bundled plugins — they ride with the gateway.
    if origin == "bundled":
        continue
    pid = p.get("id") or ""
    pver = p.get("version") or ""
    if not pid or not pver:
        continue
    if normalize(pver) != norm_gw:
        print(f"DRIFT {pid} {pver} (gateway {gw})")
PY
