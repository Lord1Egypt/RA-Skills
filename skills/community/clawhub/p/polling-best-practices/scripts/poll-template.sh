#!/bin/bash
# ==========================================
# Generic Polling Script Template
# ==========================================
# Copy this file to your task's temp directory and adapt it.
# See SKILL.md for the full best-practices guide.
#
# Required: set all variables in the "─── Config ───" section before running.
# All paths are relative to the script's working directory.

set -euo pipefail

# ─── Config (adapt these for each task) ───────────────────────────────────────

# Poll command — must return within seconds and produce parseable output
POLL_COMMAND='echo "Replace this with the actual status check command"'

# Output parsing: extract a value from POLL_COMMAND output
#   e.g., for JSON output '{"status": "completed"}', use:
#     jq -r '.status' <<< "$OUTPUT"
#   e.g., for plain text, use:
#     grep -o 'status: [a-z]*' | awk '{print $2}'
PARSE_OUTPUT='jq -r ".status" <<< "$OUTPUT"'

# Match values
STATUS_SUCCESS='completed'
STATUS_FAILURE='failed'

# Polling parameters
POLL_INTERVAL=300      # seconds (5 minutes)
MAX_POLLS=8            # 8 × 5min = 40 minutes max
DONE_FLAG='done.flag'
PROGRESS_FILE='progress.json'
POLL_LOG='poll.log'
ERROR_LOG='error.log'
TASK_JSON='task.json'

# ─── Helpers ───────────────────────────────────────────────────────────────────

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$POLL_LOG"
}

save_progress() {
  local count="${1:-0}"
  local last_result="${2:-}"
  cat > "$PROGRESS_FILE" <<EOF
{
  "poll_count": $count,
  "last_poll_at": "$(date -Iseconds)",
  "last_poll_result": "$last_result"
}
EOF
}

error_exit() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" >> "$ERROR_LOG"
  log "ERROR: $*"
  exit 1
}

# ─── Init ──────────────────────────────────────────────────────────────────────

if [[ ! -f "$TASK_JSON" ]]; then
  error_exit "task.json not found. Run from the task's temp directory."
fi

if [[ -f "$DONE_FLAG" ]]; then
  echo "done.flag found — task already marked complete. Exiting."
  exit 0
fi

POLL_COUNT=0
if [[ -f "$PROGRESS_FILE" ]]; then
  POLL_COUNT=$(grep '"poll_count"' "$PROGRESS_FILE" | sed 's/[^0-9]//g') || POLL_COUNT=0
  log "Resuming from poll count: $POLL_COUNT"
fi

log "Starting poll loop — every ${POLL_INTERVAL}s, max ${MAX_POLLS} polls"
log "Success marker: '$STATUS_SUCCESS' | Failure marker: '$STATUS_FAILURE'"

# ─── Main Loop ────────────────────────────────────────────────────────────────

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))

  if [[ $POLL_COUNT -gt $MAX_POLLS ]]; then
    error_exit "Timeout: reached max polls ($MAX_POLLS). Status may still be in_progress."
  fi

  log "[Poll $POLL_COUNT/$MAX_POLLS] Running: $POLL_COMMAND"
  OUTPUT=$(eval "$POLL_COMMAND" 2>&1) || {
    log "Command failed: $OUTPUT"
    save_progress "$POLL_COUNT" "command_failed"
    sleep "$POLL_INTERVAL"
    continue
  }

  log "Output: ${OUTPUT:0:200}"

  PARSED=$(eval "$PARSE_OUTPUT" <<< "$OUTPUT" 2>/dev/null) || PARSED="parse_error"
  log "Parsed status: '$PARSED'"

  if [[ "$PARSED" == "$STATUS_SUCCESS" ]]; then
    log "✅ Completion detected. Marking done."
    touch "$DONE_FLAG"
    save_progress "$POLL_COUNT" "completed"
    exit 0
  fi

  if [[ "$PARSED" == "$STATUS_FAILURE" ]]; then
    error_exit "Target task reported failure status: '$PARSED'"
  fi

  save_progress "$POLL_COUNT" "$PARSED"
  log "Still in_progress. Sleeping ${POLL_INTERVAL}s..."
  sleep "$POLL_INTERVAL"
done
