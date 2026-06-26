#!/usr/bin/env bash
set -uo pipefail

# OpenClaw idle gateway shutdown watcher.
# Polls QQBot/user-bot session transcript files and stops the gateway after all
# active sessions have been idle continuously for IDLE_SECONDS.

IDLE_SECONDS="${IDLE_SECONDS:-120}"
POLL_SECONDS="${POLL_SECONDS:-10}"
SESSIONS_DIR="${SESSIONS_DIR:-$HOME/.openclaw/agents/main/sessions}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/idle-shutdown.log}"
OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S %z')" "$*" >> "$LOG_FILE"
}

gateway_is_running() {
  local output rc
  output="$($OPENCLAW_BIN gateway status 2>&1)"
  rc=$?

  # openclaw gateway status should normally return success. If it does not,
  # treat obvious stopped/unavailable output as stopped and anything else as
  # not safely stoppable this round.
  if printf '%s\n' "$output" | grep -Eiq '(^|[^a-z])(stopped|not running|inactive|dead|failed|offline)([^a-z]|$)'; then
    return 1
  fi

  if [ "$rc" -ne 0 ]; then
    log "gateway status failed (rc=$rc): ${output//$'\n'/ }"
    return 1
  fi

  return 0
}

session_files() {
  [ -d "$SESSIONS_DIR" ] || return 0

  # Prefer QQBot/channel session transcript files when names expose that.
  # If none match, fall back to all regular session files so the watcher still
  # works across OpenClaw transcript naming changes.
  local matches
  matches="$(find "$SESSIONS_DIR" -type f \
    \( -iname '*qqbot*' -o -iname '*channel*' -o -iname '*direct*' \) \
    -print 2>/dev/null | sort || true)"

  if [ -n "$matches" ]; then
    printf '%s\n' "$matches"
  else
    find "$SESSIONS_DIR" -type f -print 2>/dev/null | sort || true
  fi
}

newest_session_mtime() {
  local newest=0 file mtime
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    [ -f "$file" ] || continue
    mtime="$(stat -c '%Y' "$file" 2>/dev/null || echo 0)"
    if [ "${mtime:-0}" -gt "$newest" ]; then
      newest="$mtime"
    fi
  done < <(session_files)
  printf '%s\n' "$newest"
}

log "idle shutdown watcher started (idle=${IDLE_SECONDS}s poll=${POLL_SECONDS}s sessions=$SESSIONS_DIR)"

while true; do
  if ! gateway_is_running; then
    log "gateway already stopped or status unavailable; watcher exiting"
    exit 0
  fi

  newest_mtime="$(newest_session_mtime)"
  now="$(date +%s)"

  if [ "${newest_mtime:-0}" -le 0 ]; then
    log "no session transcript files found under $SESSIONS_DIR; waiting"
    sleep "$POLL_SECONDS"
    continue
  fi

  idle_for=$(( now - newest_mtime ))

  if [ "$idle_for" -ge "$IDLE_SECONDS" ]; then
    log "all detected sessions idle for ${idle_for}s (threshold ${IDLE_SECONDS}s); stopping gateway"
    if "$OPENCLAW_BIN" gateway stop >> "$LOG_FILE" 2>&1; then
      log "gateway stop completed"
      exit 0
    else
      rc=$?
      log "gateway stop failed (rc=$rc); retrying after ${POLL_SECONDS}s"
    fi
  fi

  sleep "$POLL_SECONDS"
done
