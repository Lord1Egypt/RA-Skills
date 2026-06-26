#!/bin/bash
# memory-watcher.sh — Watches for session reset events and immediately extracts memory
# Polls sessions directory every 30s for new .reset. files
# Started by memory-cron.sh, self-manages via PID file
#
# Usage: nohup bash memory-watcher.sh &
# Or:    bash memory-watcher.sh --once   (single check, no loop)

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
STATE_DIR="$WORKSPACE/.memory"
PID_FILE="$STATE_DIR/watcher.pid"
SEEN_FILE="$STATE_DIR/watcher-seen.txt"
LOG="$STATE_DIR/watcher.log"
POLL_INTERVAL=30  # seconds

# Resolve timezone
if [ -z "$TZ" ]; then
  OPENCLAW_CFG="$WORKSPACE/../openclaw.json"
  if [ -f "$OPENCLAW_CFG" ]; then
    DETECTED_TZ=$(node -e "try{const c=require('$OPENCLAW_CFG');console.log(c?.agents?.defaults?.userTimezone||'')}catch{}" 2>/dev/null)
    [ -n "$DETECTED_TZ" ] && export TZ="$DETECTED_TZ"
  fi
fi
export TZ="${TZ:-$(cat /etc/timezone 2>/dev/null || readlink /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||' || echo UTC)}"

mkdir -p "$STATE_DIR"

# Rotate log if > 50KB
[ -f "$LOG" ] && [ "$(wc -c < "$LOG" 2>/dev/null || echo 0)" -gt 51200 ] && mv "$LOG" "$LOG.old"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

# Single check mode
ONE_SHOT=false
[ "$1" = "--once" ] && ONE_SHOT=true

# Init seen file from existing reset files (don't re-extract old ones on first run)
if [ ! -f "$SEEN_FILE" ]; then
  [ -d "$SESSIONS_DIR" ] && ls "$SESSIONS_DIR" 2>/dev/null | grep '\.reset\.' > "$SEEN_FILE"
  log "initialized seen file with $(wc -l < "$SEEN_FILE" 2>/dev/null || echo 0) existing reset files"
fi

check_new_resets() {
  [ ! -d "$SESSIONS_DIR" ] && return
  
  local new_count=0
  for f in "$SESSIONS_DIR"/*.reset.*; do
    [ ! -f "$f" ] && continue
    local basename=$(basename "$f")
    
    # Skip if already seen
    grep -qxF "$basename" "$SEEN_FILE" 2>/dev/null && continue
    
    # New reset file detected!
    log "NEW RESET detected: $basename"
    
    # Extract memory from this session immediately
    EXTRACT_OUT=$(node "$SCRIPT_DIR/memory-auto-extract.js" --workspace "$WORKSPACE" "$f" 2>&1)
    log "extract: $EXTRACT_OUT"
    
    # Rebuild index after extraction
    INDEX_OUT=$(node "$SCRIPT_DIR/memory-index.js" --workspace "$WORKSPACE" 2>&1)
    log "reindex: $INDEX_OUT"
    
    # Mark as seen
    echo "$basename" >> "$SEEN_FILE"
    new_count=$((new_count + 1))
  done
  
  [ $new_count -gt 0 ] && log "processed $new_count new reset(s)"
}

# ── Main ──
if $ONE_SHOT; then
  check_new_resets
  exit 0
fi

# Daemon mode
echo $$ > "$PID_FILE"
log "watcher started (PID: $$, interval: ${POLL_INTERVAL}s)"

# Cleanup on exit
trap 'log "watcher stopped (PID: $$)"; rm -f "$PID_FILE"; exit 0' SIGTERM SIGINT EXIT

while true; do
  check_new_resets
  sleep "$POLL_INTERVAL"
done
