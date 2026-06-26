#!/usr/bin/env bash
set -euo pipefail

CDP_PORT="${OPENCLAW_BROWSER_CDP_PORT:-18800}"
USER_DATA_DIR="${OPENCLAW_BROWSER_USER_DATA_DIR:-$HOME/.openclaw/browser/openclaw/user-data}"
LOG_FILE="${OPENCLAW_BROWSER_LOG:-/tmp/openclaw-browser.log}"
BROWSER_BIN="${OPENCLAW_BROWSER_BIN:-/usr/bin/chromium}"

if [[ ! -x "$BROWSER_BIN" ]]; then
  echo "Browser binary not found or not executable: $BROWSER_BIN" >&2
  exit 1
fi

mkdir -p "$USER_DATA_DIR"

if command -v pkill >/dev/null 2>&1; then
  pkill -f "${BROWSER_BIN}.*--remote-debugging-port=${CDP_PORT}" >/dev/null 2>&1 || true
fi

"$BROWSER_BIN" \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --no-first-run \
  --remote-debugging-port="$CDP_PORT" \
  --user-data-dir="$USER_DATA_DIR" \
  about:blank >"$LOG_FILE" 2>&1 &

sleep 2

echo "CDP probe:"
curl -s "http://127.0.0.1:${CDP_PORT}/json/version" || true

echo
echo "OpenClaw browser status:"
openclaw browser status || true

echo
echo "Log file: $LOG_FILE"
