#!/usr/bin/env bash
# sync-drifted-plugins.sh <profile> [--apply] [--yes]
#
# Sync externalized plugins that drifted behind the gateway version.
# Default mode is dry-run: prints the commands it would run, no mutation.
#
# With --apply:
#   1. backup openclaw.json (fresh snapshot)
#   2. for each drift: openclaw plugins update <id>
#   3. openclaw gateway restart
#   4. wait up to 60s for Runtime: running
#   5. on unhealthy -> restore backup, restart, exit 3 RESTORE
#
# With --yes: skip the per-plugin prompt placeholder (the calling agent owns
# the actual UX prompt — this flag just signals "no per-plugin gate needed").
#
# Output: one line per action, terminated by either:
#   OK synced <count> drifted plugins, gateway healthy
#   RESTORE <reason>
#   NOTHING_TO_DO
#
# Exit codes:
#   0 success (synced or nothing to do)
#   2 BLOCKED preconditions
#   3 RESTORE happened
#   4 sync attempted but one or more plugin updates failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_lib.sh
source "$SCRIPT_DIR/_lib.sh"

PROFILE=""
APPLY=0
YES=0
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --yes)   YES=1 ;;
    --help|-h)
      sed -n '1,30p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      if [ -z "$PROFILE" ]; then
        PROFILE="$1"
      else
        echo "usage: sync-drifted-plugins.sh <profile> [--apply] [--yes]" >&2
        exit 2
      fi
      ;;
  esac
  shift
done

if [ -z "$PROFILE" ]; then
  echo "usage: sync-drifted-plugins.sh <profile> [--apply] [--yes]" >&2
  exit 2
fi

pum_require_awareness

# Collect drift lines.
DRIFT_OUTPUT="$(bash "$SCRIPT_DIR/detect-drift.sh" "$PROFILE")"

if [ -z "$DRIFT_OUTPUT" ]; then
  echo "NOTHING_TO_DO"
  exit 0
fi

# Parse drift lines into plugin ids.
mapfile -t PLUGINS < <(echo "$DRIFT_OUTPUT" | awk '/^DRIFT / { print $2 }')

if [ ${#PLUGINS[@]} -eq 0 ]; then
  echo "NOTHING_TO_DO"
  exit 0
fi

# ---- dry-run -----------------------------------------------------------------

if [ "$APPLY" -ne 1 ]; then
  echo "# dry-run: the following commands would run with --apply"
  for p in "${PLUGINS[@]}"; do
    echo "openclaw --profile $PROFILE plugins update $p"
  done
  echo "openclaw --profile $PROFILE gateway restart"
  echo "# (pass --apply to actually run)"
  exit 0
fi

# ---- apply -------------------------------------------------------------------

BACKUP="$(pum_backup_config "$PROFILE")" || {
  echo "BLOCKED backup-failed" >&2
  exit 2
}
pum_log "$PROFILE" "sync-drifted: applying for ${#PLUGINS[@]} plugin(s); backup=$BACKUP"

FAILED=()
SUCCEEDED=()

for p in "${PLUGINS[@]}"; do
  pum_log "$PROFILE" "sync-drifted: openclaw plugins update $p (start)"
  if openclaw --profile "$PROFILE" plugins update "$p" >>"$(pum_state_dir "$PROFILE")/runs/$(pum_run_id).log" 2>&1; then
    SUCCEEDED+=("$p")
    pum_log "$PROFILE" "sync-drifted: $p ok"
  else
    FAILED+=("$p")
    pum_log "$PROFILE" "sync-drifted: $p FAILED"
  fi
done

# If nothing succeeded, don't bother restarting.
if [ ${#SUCCEEDED[@]} -eq 0 ]; then
  echo "no plugins updated successfully (${#FAILED[@]} failed)"
  pum_log "$PROFILE" "sync-drifted: all failed, skipping restart"
  exit 4
fi

# Restart and wait.
pum_log "$PROFILE" "sync-drifted: restarting gateway"
openclaw --profile "$PROFILE" gateway restart >>"$(pum_state_dir "$PROFILE")/runs/$(pum_run_id).log" 2>&1 || true

if pum_wait_healthy "$PROFILE" 60; then
  if [ ${#FAILED[@]} -gt 0 ]; then
    echo "OK synced ${#SUCCEEDED[@]} drifted plugins, gateway healthy (${#FAILED[@]} failed: ${FAILED[*]})"
    pum_log "$PROFILE" "sync-drifted: partial success (${#FAILED[@]} failed)"
    exit 4
  fi
  echo "OK synced ${#SUCCEEDED[@]} drifted plugins, gateway healthy"
  pum_log "$PROFILE" "sync-drifted: all ok"
  exit 0
fi

# Unhealthy → restore.
pum_log "$PROFILE" "sync-drifted: gateway unhealthy after restart, restoring backup"
if pum_restore_config "$PROFILE" "$BACKUP"; then
  echo "RESTORE gateway-unhealthy-after-sync: restored config backup, gateway healthy on previous config" >&2
  exit 3
fi
echo "RESTORE FAILED gateway-still-unhealthy-after-restore: manual intervention needed" >&2
exit 3
