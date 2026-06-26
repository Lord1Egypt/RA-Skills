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

# Chat ID for notifications — agent must inject at script generation time
CHAT_ID="INJECT_CHAT_ID"  # ← replace with Discord channel ID from inbound_meta.chat_id

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

# Post-poll actions (uncomment as needed)
# ON_COMPLETE_DOWNLOAD='<download command>'        # Category B1: Download artifact
# ON_COMPLETE_VERIFY=true                           # Category B2: Verify output file
# ON_COMPLETE_TRIGGER_AGENT="msg"                   # Category A2: Chain to next skill

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

# Category A1: Direct notification to user — no agent processing
notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

# Category A2: Trigger agent to execute next workflow step
trigger_agent() {
  local message="$1"
  openclaw agent --channel discord --message "$message" --deliver --timeout 600 2>/dev/null || {
    log "WARNING: agent trigger failed, falling back to direct message"
    notify_user "$message"
  }
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
  notify_user "❌ 任务失败：$*"
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
    log "TIMEOUT after $MAX_POLLS polls"
    save_progress "$POLL_COUNT" "timeout"
    notify_user "⏰ 任务超时（已达最大轮询次数 $MAX_POLLS）。"
    exit 1
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

  # ── Category B1: Download artifact (if configured) ────────────────────────
  if [[ "$PARSED" == "$STATUS_SUCCESS" ]]; then
    log "✅ Completion detected."
    touch "$DONE_FLAG"
    save_progress "$POLL_COUNT" "completed"

    # Uncomment and adapt for download:
    # if [[ -n "${ON_COMPLETE_DOWNLOAD:-}" ]]; then
    #   log "Downloading artifact..."
    #   eval "$ON_COMPLETE_DOWNLOAD" >> "$POLL_LOG" 2>&1 || log "WARNING: download failed"
    # fi

    # ── Category B2: Verify output ──────────────────────────────────────────
    # Uncomment and adapt:
    # if [[ "${ON_COMPLETE_VERIFY:-}" == "true" ]]; then
    #   [[ -s "$OUTPUT_PATH" ]] || { notify_user "⚠️ 产物文件为空"; exit 1; }
    # fi

    # ── Category A1: Notify user ────────────────────────────────────────────
    notify_user "✅ 任务完成！共 $POLL_COUNT 轮轮询。"

    # ── Category A2: Trigger agent for chaining ─────────────────────────────
    # Uncomment and adapt:
    # if [[ -n "${ON_COMPLETE_TRIGGER_AGENT:-}" ]]; then
    #   trigger_agent "$ON_COMPLETE_TRIGGER_AGENT"
    # fi

    exit 0
  fi

  # ── Failure ───────────────────────────────────────────────────────────────
  if [[ "$PARSED" == "$STATUS_FAILURE" ]]; then
    error_exit "Target task reported failure status: '$PARSED'"
  fi

  # ── Still in progress ────────────────────────────────────────────────────
  save_progress "$POLL_COUNT" "$PARSED"
  log "Still in_progress. Sleeping ${POLL_INTERVAL}s..."
  sleep "$POLL_INTERVAL"
done
