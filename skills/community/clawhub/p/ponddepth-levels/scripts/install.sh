#!/usr/bin/env bash
set -euo pipefail

WS="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
DIST="${OPENCLAW_UI_ASSETS_DIR:-/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/assets}"
EXT_DIR="$WS/.openclaw/extensions/ponddepth"

if [[ ! -d "$EXT_DIR" ]]; then
  echo "ERROR: missing ponddepth plugin at $EXT_DIR" >&2
  exit 1
fi

mkdir -p "$DIST/ponddepth-icons"

# Backup
TS=$(date +%Y%m%d-%H%M%S)
mkdir -p "$WS/_deleted/ponddepth-install-backups/$TS"

if [[ -f "$DIST/ponddepth-badge.js" ]]; then
  cp -f "$DIST/ponddepth-badge.js" "$WS/_deleted/ponddepth-install-backups/$TS/ponddepth-badge.js"
fi

# Copy assets (PNG preferred; fallback to base64-text assets for ClawHub web uploader)
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if compgen -G "$BASE_DIR/assets/icons_bin/*.png" > /dev/null; then
  cp -f "$BASE_DIR/assets/icons_bin/"*.png "$DIST/ponddepth-icons/"
elif compgen -G "$BASE_DIR/assets/icons_b64/*.png.txt" > /dev/null; then
  for b64 in "$BASE_DIR"/assets/icons_b64/*.png.txt; do
    out="$DIST/ponddepth-icons/$(basename "$b64" .txt)"
    cat "$b64" | base64 -d > "$out"
  done
else
  echo "WARN: no icons found in skill assets (icons_bin/icons_b64)" >&2
fi

# Copy badge script
cp -f "$(cd "$(dirname "$0")/.." && pwd)/assets/ponddepth-badge.js" "$DIST/ponddepth-badge.js"

# Copy plugin extension (so Control UI can query /ponddepth/api if enabled)
mkdir -p "$WS/.openclaw/extensions/ponddepth"
cp -f "$EXT_DIR/openclaw.plugin.json" "$WS/.openclaw/extensions/ponddepth/openclaw.plugin.json"
cp -f "$EXT_DIR/index.ts" "$WS/.openclaw/extensions/ponddepth/index.ts"

# Install packaged helper tasks into the user's workspace (idempotent)
TASKS_DIR="$WS/tasks"
mkdir -p "$TASKS_DIR"
# (BASE_DIR already set above)

cp -f "$BASE_DIR/tasks/companion_metrics.py" "$TASKS_DIR/ponddepth_companion_metrics.py"
cp -f "$BASE_DIR/tasks/clawhub_status.py" "$TASKS_DIR/ponddepth_clawhub_status.py"

chmod +x "$TASKS_DIR/ponddepth_companion_metrics.py" "$TASKS_DIR/ponddepth_clawhub_status.py" || true

# Best-effort: create/update crons (B2 UX relies on clawhub-status.json)
if command -v openclaw >/dev/null 2>&1; then
  # 1) ClawHub status refresh (every 10 minutes)
  if command -v jq >/dev/null 2>&1; then
    EXIST_ID=$(openclaw cron list --json | jq -r '.jobs[]|select(.name=="PondDepth ClawHub status (10m)")|.id' | head -n 1)
  else
    EXIST_ID=""
  fi

  if [[ -n "${EXIST_ID:-}" && "${EXIST_ID}" != "null" ]]; then
    openclaw cron edit "$EXIST_ID" --every 10m --name "PondDepth ClawHub status (10m)" --description "Writes /ui/assets/clawhub-status.json for PondDepth B2 UX" --message "请运行命令并输出stdout：python3 $TASKS_DIR/ponddepth_clawhub_status.py" --model gpt-4o-mini --thinking minimal --timeout-seconds 60 --session isolated --no-deliver >/dev/null
  else
    openclaw cron add --every 10m --name "PondDepth ClawHub status (10m)" --description "Writes /ui/assets/clawhub-status.json for PondDepth B2 UX" --message "请运行命令并输出stdout：python3 $TASKS_DIR/ponddepth_clawhub_status.py" --model gpt-4o-mini --thinking minimal --timeout-seconds 60 --session isolated --no-deliver >/dev/null
  fi

  # 2) Companion metrics refresh (hourly)
  if command -v jq >/dev/null 2>&1; then
    EXIST_ID2=$(openclaw cron list --json | jq -r '.jobs[]|select(.name=="PondDepth companion metrics (hourly)")|.id' | head -n 1)
  else
    EXIST_ID2=""
  fi

  if [[ -n "${EXIST_ID2:-}" && "${EXIST_ID2}" != "null" ]]; then
    openclaw cron edit "$EXIST_ID2" --cron "0 0 * * * *" --tz UTC --name "PondDepth companion metrics (hourly)" --description "Generate /ui/assets/companion-metrics.json (XP/level)" --message "请运行命令并输出stdout：python3 $TASKS_DIR/ponddepth_companion_metrics.py --tz Asia/Shanghai" --model gpt-4o-mini --thinking minimal --timeout-seconds 120 --session isolated --no-deliver >/dev/null
  else
    openclaw cron add --cron "0 0 * * * *" --tz UTC --name "PondDepth companion metrics (hourly)" --description "Generate /ui/assets/companion-metrics.json (XP/level)" --message "请运行命令并输出stdout：python3 $TASKS_DIR/ponddepth_companion_metrics.py --tz Asia/Shanghai" --model gpt-4o-mini --thinking minimal --timeout-seconds 120 --session isolated --no-deliver >/dev/null
  fi
fi

echo "OK: installed PondDepth assets + helper tasks. If Control UI is open, hard refresh the page."