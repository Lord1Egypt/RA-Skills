#!/usr/bin/env bash
set -euo pipefail
# load env if present
source "$(dirname "$0")/_env_loader.sh"

SESSION=${1:-debug}
DISPLAY_VAL=${2:-${VNC_DISPLAY:-:99}}
FORCE_FLAG=false
# accept --force as optional third arg
if [ "${3:-}" = "--force" ]; then FORCE_FLAG=true; fi
LOG=${TMP_LOG_DIR:-/tmp}/x11vnc_${SESSION}.log

# Targeted Chrome shutdown: prefer pid file created by start_chrome_debug.sh
CHROME_PID_FILE="${TMP_RUN_DIR:-/tmp}/chrome_vnc_${SESSION}.pid"
if [ -f "$CHROME_PID_FILE" ]; then
  CHROME_PID=$(cat "$CHROME_PID_FILE" 2>/dev/null || true)
  if [ -n "$CHROME_PID" ] && ps -p "$CHROME_PID" > /dev/null 2>&1; then
    echo "Stopping Chrome pid $CHROME_PID (from $CHROME_PID_FILE)" | tee -a ""$LOG""
    kill "$CHROME_PID" || true
    # wait up to 5s
    for i in {1..5}; do
      if ps -p "$CHROME_PID" > /dev/null 2>&1; then
        sleep 1
      else
        break
      fi
    done
    if ps -p "$CHROME_PID" > /dev/null 2>&1; then
      echo "Chrome pid $CHROME_PID did not exit, sending SIGKILL" | tee -a ""$LOG""
      kill -9 "$CHROME_PID" || true
    fi
    rm -f "$CHROME_PID_FILE" || true
  else
    echo "Chrome pid file present but process not found or already exited: $CHROME_PID_FILE" | tee -a ""$LOG""
    rm -f "$CHROME_PID_FILE" || true
  fi
else
  echo "No chrome pid file ($CHROME_PID_FILE) found; skipping targeted chrome shutdown" | tee -a ""$LOG""
fi

# Global fallback (dangerous): only when explicitly allowed by .env AND --force flag provided
if [ "${ALLOW_CHROME_FORCE_RESTART:-false}" = "true" ] && [ "$FORCE_FLAG" = true ]; then
  echo "ALLOW_CHROME_FORCE_RESTART is true and --force passed; performing global chrome kill" | tee -a ""$LOG""
  pkill -9 -f google-chrome || true
else
  echo "Global chrome kill not performed (ALLOW_CHROME_FORCE_RESTART=${ALLOW_CHROME_FORCE_RESTART:-false}, --force=$FORCE_FLAG)" | tee -a ""$LOG""
fi

# Kill x11vnc
pkill -f "x11vnc.*${DISPLAY_VAL}" || true
# Kill fluxbox
pkill -f fluxbox || true
# Kill Xvfb
pkill -f "Xvfb ${DISPLAY_VAL}" || true

echo "Stopped VNC session $SESSION; logs: "$LOG"" | tee -a ""$LOG""