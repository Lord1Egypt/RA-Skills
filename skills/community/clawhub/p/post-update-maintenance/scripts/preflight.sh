#!/usr/bin/env bash
# preflight.sh <profile>
#
# Verify the world is in a state where maintenance is safe to attempt.
# Refuses to proceed if anything looks off — that's the update-guard's job.
#
# Output:
#   OK preflight <state-dir> <backup-path>     - all good
#   BLOCKED <reason>                           - refuse to proceed
#
# Exit:
#   0 success
#   2 blocked

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_lib.sh
source "$SCRIPT_DIR/_lib.sh"

PROFILE="${1:-}"
if [ -z "$PROFILE" ]; then
  echo "usage: preflight.sh <profile>" >&2
  exit 2
fi

pum_require_awareness

# Gateway must be healthy BEFORE we touch anything.
if ! pum_gateway_healthy "$PROFILE"; then
  echo "BLOCKED gateway-unhealthy: refusing to start maintenance on an already-broken gateway" >&2
  echo "        (recovery from a broken gateway is the update-guard's responsibility, not this skill's)" >&2
  exit 2
fi

CFG="$(pum_config_path "$PROFILE")"
if [ ! -r "$CFG" ]; then
  echo "BLOCKED config-unreadable: $CFG" >&2
  exit 2
fi
if [ ! -w "$CFG" ]; then
  echo "BLOCKED config-not-writable: $CFG" >&2
  exit 2
fi

# Backup + snapshot.
BACKUP="$(pum_backup_config "$PROFILE")" || exit 2
STATE="$(pum_state_dir "$PROFILE")"
RUN="$(pum_run_id)"

# Channel snapshot (best-effort, missing channels tool shouldn't block).
openclaw --profile "$PROFILE" channels status --json > "$STATE/snapshots/channels-before.$RUN.json" 2>/dev/null \
  || echo '{}' > "$STATE/snapshots/channels-before.$RUN.json"

pum_log "$PROFILE" "preflight ok: backup=$BACKUP cfg=$CFG"
echo "OK preflight $STATE $BACKUP"
