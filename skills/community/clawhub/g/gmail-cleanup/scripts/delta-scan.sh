#!/usr/bin/env bash
# gmail-cleanup - delta scan (READ-ONLY).
#
# Scans inbox mail NEW since the last run instead of the newest N:
#   window = in:inbox after:<lastScanEpoch>
# First run bootstraps GMAIL_CLEANUP_BOOTSTRAP_HOURS (default 24h).
# Advances state/gmail-cleanup/watermark.json only on success.
#
# Reuses triage-scan.py for fetch/parse via a temp config whose scope.query is the
# delta window. Credentials: GOG_KEYRING_PASSWORD from the environment ONLY.
#
# Env: GMAIL_CLEANUP_STATE, GOG_KEYRING_PASSWORD, GMAIL_CLEANUP_BOOTSTRAP_HOURS,
#      GMAIL_CLEANUP_MAX (per-run candidate cap; also from limits.scanMax)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE="${GMAIL_CLEANUP_STATE:-$HERE/../../state/gmail-cleanup}"
CFG="${GMAIL_CLEANUP_CONFIG:-$STATE/config.json}"
WM="$STATE/watermark.json"
BOOTSTRAP_HOURS="${GMAIL_CLEANUP_BOOTSTRAP_HOURS:-24}"

if [ -z "${GOG_KEYRING_PASSWORD:-}" ]; then
  echo "GOG_KEYRING_PASSWORD is not set. Export it before running; this skill does not read credential files itself." >&2
  exit 1
fi
[ -f "$CFG" ] || { echo "config not found: $CFG" >&2; exit 1; }

now=$(date -u +%s)
since=0
[ -f "$WM" ] && since=$(python3 -c "import json;print(int(json.load(open('$WM')).get('lastScanEpoch',0)))" 2>/dev/null || echo 0)
if [ "$since" -le 0 ]; then
  since=$(( now - BOOTSTRAP_HOURS*3600 )); bootstrap=1
else
  bootstrap=0
fi

max="${GMAIL_CLEANUP_MAX:-$(python3 -c "import json;print(int(json.load(open('$CFG')).get('limits',{}).get('scanMax',200)))")}"
tmpcfg="$(mktemp)"; trap 'rm -f "$tmpcfg"' EXIT
python3 - "$CFG" "$tmpcfg" "$since" "$max" <<'PY'
import json,sys
cfg=json.load(open(sys.argv[1]))
cfg.setdefault("scope",{})
cfg["scope"]["query"]=f"in:inbox after:{sys.argv[3]}"
cfg["scope"]["extraQueries"]=[]
cfg.setdefault("limits",{})["scanMax"]=int(sys.argv[4])
json.dump(cfg,open(sys.argv[2],"w"))
PY

GMAIL_CLEANUP_CONFIG="$tmpcfg" GMAIL_CLEANUP_STATE="$STATE" python3 "$HERE/triage-scan.py"

python3 - "$WM" "$now" "$since" "$bootstrap" <<'PY'
import json,sys
json.dump({"lastScanEpoch":int(sys.argv[2]),"prevSince":int(sys.argv[3]),"bootstrap":sys.argv[4]=="1"},open(sys.argv[1],"w"),indent=1)
PY
echo "delta-scan: window=${since}..${now} bootstrap=${bootstrap}"
