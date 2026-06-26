#!/usr/bin/env bash
set -euo pipefail
# load env if present
source "$(dirname "$0")/_env_loader.sh"

SESSION=${1:-debug}
PROXY_ARG="${2:-}"
REMOTE_PORT=${3:-${REMOTE_DEBUG_PORT:-9222}}
DISPLAY_VAL=${DISPLAY:-${VNC_DISPLAY:-:99}}
PROFILE_DIR=${CHROME_USER_DATA_DIR:-/tmp/${SESSION}_chrome_profile}
LOG=${TMP_LOG_DIR:-/tmp}/chrome_vnc_${SESSION}.log
mkdir -p "$PROFILE_DIR"
export DISPLAY="$DISPLAY_VAL"
# Build proxy flag if provided
PROXY_FLAG=''
# PROXY_ARG may be like --proxy=http://127.0.0.1:3128 or empty
if [[ -z "${PROXY_ARG}" && -n "${PROXY_URL:-}" ]]; then
  PROXY_ARG="--proxy=${PROXY_URL}"
fi
if [[ "$PROXY_ARG" =~ ^--proxy= ]]; then
  PROXY_FLAG="--proxy-server=${PROXY_ARG#--proxy=}"
fi
# Allow forcing chrome restart only if allowed
if [ "${ALLOW_CHROME_FORCE_RESTART:-false}" = "true" ]; then
  pkill -9 -f google-chrome || true
fi
# Start chrome with remote debugging
setsid nohup /usr/bin/google-chrome --user-data-dir="$PROFILE_DIR" "$PROXY_FLAG" --remote-debugging-port=""$REMOTE_PORT"" --no-first-run --no-default-browser-check --disable-extensions --disable-gpu --no-sandbox --window-size=1366,768 "${CHROME_EXTRA_FLAGS:-}" about:blank &> ""$LOG"" &
PID=$!
echo "$PID" > "${TMP_RUN_DIR:-/tmp}/chrome_vnc_${SESSION}.pid"
sleep 1
echo "Chrome started (pid=$PID) devtools at ws://127.0.0.1:$REMOTE_PORT - log: $LOG"