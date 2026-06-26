#!/usr/bin/env bash
# clean-stale-config.sh <profile> [--apply] [--entries id1,id2,...]
#
# Remove stale plugins.entries.<id> nodes from openclaw.json.
# Default mode is dry-run: prints the JSON patch, no mutation.
#
# With --apply:
#   1. backup openclaw.json (fresh snapshot)
#   2. apply patch atomically (<file>.tmp then mv)
#   3. openclaw gateway restart
#   4. wait up to 60s for Runtime: running
#   5. on unhealthy -> restore backup, restart, exit 3 RESTORE
#
# --entries lets the caller opt into a subset. Without it, all detected stale
# entries are targeted.
#
# Output:
#   one JSON patch op per stale entry (always)
#   OK cleaned <count> entries, gateway healthy
#   NOTHING_TO_DO
#   RESTORE <reason>
#
# Exit:
#   0 success or nothing-to-do
#   2 BLOCKED preconditions
#   3 RESTORE happened

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_lib.sh
source "$SCRIPT_DIR/_lib.sh"

PROFILE=""
APPLY=0
ENTRIES_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --entries) ENTRIES_ARG="${2:-}"; shift ;;
    --help|-h)
      sed -n '1,28p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      if [ -z "$PROFILE" ]; then
        PROFILE="$1"
      else
        echo "usage: clean-stale-config.sh <profile> [--apply] [--entries id1,id2,...]" >&2
        exit 2
      fi
      ;;
  esac
  shift
done

if [ -z "$PROFILE" ]; then
  echo "usage: clean-stale-config.sh <profile> [--apply] [--entries id1,id2,...]" >&2
  exit 2
fi

CFG="$(pum_config_path "$PROFILE")"
if [ ! -r "$CFG" ]; then
  echo "BLOCKED config-unreadable: $CFG" >&2
  exit 2
fi

# Detect stale entries (full set).
mapfile -t DETECTED < <(bash "$SCRIPT_DIR/detect-stale-config.sh" "$PROFILE" | awk '/^STALE plugins\.entries\./ { sub("^STALE plugins\\.entries\\.", "", $0); print $0 }')

# Build the target set: --entries overrides, otherwise use everything detected.
if [ -n "$ENTRIES_ARG" ]; then
  IFS=',' read -r -a TARGETS <<< "$ENTRIES_ARG"
else
  TARGETS=("${DETECTED[@]}")
fi

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "NOTHING_TO_DO"
  exit 0
fi

# Print the patch (always, even on dry-run).
echo "# JSON patch (RFC 6902) targeting $CFG"
echo "["
FIRST=1
for id in "${TARGETS[@]}"; do
  if [ "$FIRST" -eq 1 ]; then FIRST=0; else echo ","; fi
  printf '  { "op": "remove", "path": "/plugins/entries/%s" }' "$id"
done
echo
echo "]"

if [ "$APPLY" -ne 1 ]; then
  echo "# dry-run: pass --apply to write changes"
  exit 0
fi

# ---- apply -------------------------------------------------------------------

BACKUP="$(pum_backup_config "$PROFILE")" || {
  echo "BLOCKED backup-failed" >&2
  exit 2
}
pum_log "$PROFILE" "clean-stale-config: applying for ${#TARGETS[@]} entries; backup=$BACKUP"

# Use jq if available, else Python.
TMP="$CFG.pum.tmp.$$"
TARGETS_JSON="$(printf '%s\n' "${TARGETS[@]}" | python3 -c 'import sys, json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))')"

if command -v jq >/dev/null 2>&1; then
  if ! jq --argjson keys "$TARGETS_JSON" \
       '(.plugins.entries // {}) as $e | .plugins.entries = (reduce $keys[] as $k ($e; del(.[$k])))' \
       "$CFG" > "$TMP"; then
    rm -f "$TMP"
    echo "BLOCKED jq-failed" >&2
    exit 2
  fi
else
  if ! TARGETS_JSON="$TARGETS_JSON" python3 - "$CFG" "$TMP" <<'PY'
import json, os, sys
src, dst = sys.argv[1], sys.argv[2]
targets = json.loads(os.environ["TARGETS_JSON"])
with open(src) as f:
    data = json.load(f)
entries = data.get("plugins", {}).get("entries", {})
for k in targets:
    entries.pop(k, None)
data.setdefault("plugins", {})["entries"] = entries
with open(dst, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
PY
  then
    rm -f "$TMP"
    echo "BLOCKED python-fallback-failed" >&2
    exit 2
  fi
fi

# Atomic move.
mv "$TMP" "$CFG"
pum_log "$PROFILE" "clean-stale-config: patch written to $CFG, restarting gateway"

openclaw --profile "$PROFILE" gateway restart >>"$(pum_state_dir "$PROFILE")/runs/$(pum_run_id).log" 2>&1 || true

if pum_wait_healthy "$PROFILE" 60; then
  echo "OK cleaned ${#TARGETS[@]} entries, gateway healthy"
  pum_log "$PROFILE" "clean-stale-config: ok"
  exit 0
fi

# Unhealthy → restore.
pum_log "$PROFILE" "clean-stale-config: gateway unhealthy, restoring backup"
if pum_restore_config "$PROFILE" "$BACKUP"; then
  echo "RESTORE gateway-unhealthy-after-config-clean: restored config backup, gateway healthy on previous config" >&2
  exit 3
fi
echo "RESTORE FAILED gateway-still-unhealthy-after-restore: manual intervention needed" >&2
exit 3
