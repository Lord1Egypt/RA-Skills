#!/usr/bin/env bash
set -euo pipefail

CDP_PORT="${OPENCLAW_BROWSER_CDP_PORT:-18800}"
BROWSER_BIN="${OPENCLAW_BROWSER_BIN:-/usr/bin/chromium}"

echo "== Browser binary =="
command -v "$BROWSER_BIN" || true
"$BROWSER_BIN" --version || true

echo
echo "== OpenClaw browser status =="
openclaw browser status || true

echo
echo "== CDP probe =="
curl -s "http://127.0.0.1:${CDP_PORT}/json/version" || true

echo
echo "== Process check =="
ps -ef | grep -E "[c]hromium|[1]8800" || true

echo
echo "== Environment =="
printf 'HOME=%s\n' "$HOME"
printf 'XDG_RUNTIME_DIR=%s\n' "${XDG_RUNTIME_DIR-}"
printf 'DISPLAY=%s\n' "${DISPLAY-}"
printf 'WAYLAND_DISPLAY=%s\n' "${WAYLAND_DISPLAY-}"

echo
echo "== Hints =="
echo "Healthy enough when CDP JSON returns and browser status shows running: true."
