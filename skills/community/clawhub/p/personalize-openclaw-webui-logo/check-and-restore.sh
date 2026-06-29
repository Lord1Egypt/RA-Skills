#!/usr/bin/env bash
# check-and-restore.sh — verify the active favicon matches the last applied state;
# if not, re-apply the recorded set. Cheap: one sha256 of one PNG.
#
# Invoked by the gateway:startup hook (hooks/logo-guard/handler.js) on every
# openclaw gateway start. Also runnable by hand for debugging.
#
# Runtime state (stamp + log) is read from / written to:
#   ${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo/
#
# Exit codes:
#   0  — in sync (no-op) OR successfully re-applied
#   2  — no stamp file yet (apply-logo.sh has never been run)
#   3  — could not locate control-ui dist
#   4  — re-apply attempted but failed
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}/state/personalize-openclaw-webui-logo"
STAMP="$STATE_DIR/applied-state"
LOG="$STATE_DIR/logo-guard.log"

mkdir -p "$STATE_DIR" 2>/dev/null || true
chmod 700 "$STATE_DIR" 2>/dev/null || true

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }

if [ ! -f "$STAMP" ]; then
  log "no stamp at $STAMP — skip (apply-logo.sh has never been run)"
  exit 2
fi

SET=""; EXPECTED_HASH=""
while IFS='=' read -r k v; do
  case "$k" in
    set) SET="$v" ;;
    favicon32_sha256) EXPECTED_HASH="$v" ;;
  esac
done < "$STAMP"

if [ -z "$SET" ] || [ -z "$EXPECTED_HASH" ]; then
  log "stamp malformed (set='$SET' hash='$EXPECTED_HASH') — bailing"
  exit 2
fi

find_ui_dir() {
  if [ -n "${OPENCLAW_UI_DIR:-}" ]; then echo "$OPENCLAW_UI_DIR"; return 0; fi
  if command -v npm >/dev/null 2>&1; then
    local nr; nr="$(npm root -g 2>/dev/null || true)"
    [ -n "$nr" ] && [ -d "$nr/openclaw/dist/control-ui" ] && { echo "$nr/openclaw/dist/control-ui"; return 0; }
  fi
  local candidates=(
    "$HOME/.npm-global/lib/node_modules/openclaw/dist/control-ui"
    "$HOME/.local/lib/node_modules/openclaw/dist/control-ui"
    "/usr/local/lib/node_modules/openclaw/dist/control-ui"
    "/opt/homebrew/lib/node_modules/openclaw/dist/control-ui"
    "/usr/lib/node_modules/openclaw/dist/control-ui"
  )
  # Windows (Git Bash / MSYS / WSL)
  [ -n "${APPDATA:-}" ] && candidates+=("$APPDATA/npm/node_modules/openclaw/dist/control-ui")
  [ -n "${USERPROFILE:-}" ] && candidates+=("$USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/dist/control-ui")
  local c
  for c in "${candidates[@]}"; do
    [ -d "$c" ] && { ( cd "$c" && pwd -P ); return 0; }
  done
  return 1
}

UI="$(find_ui_dir || true)"
if [ -z "$UI" ] || [ ! -f "$UI/favicon-32.png" ]; then
  log "dist not found or favicon-32.png missing (UI='$UI')"
  exit 3
fi

if command -v sha256sum >/dev/null 2>&1; then
  CURRENT_HASH="$(sha256sum "$UI/favicon-32.png" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  CURRENT_HASH="$(shasum -a 256 "$UI/favicon-32.png" | awk '{print $1}')"
else
  log "no sha256 tool — bailing"
  exit 3
fi

if [ "$CURRENT_HASH" = "$EXPECTED_HASH" ]; then
  log "in sync (set=$SET hash=${CURRENT_HASH:0:12}…) — no-op"
  exit 0
fi

log "DRIFT detected: expected ${EXPECTED_HASH:0:12}… got ${CURRENT_HASH:0:12}… — re-applying set '$SET'"
if bash "$SKILL_DIR/apply-logo.sh" "$SET" >> "$LOG" 2>&1; then
  log "re-apply OK"
  exit 0
else
  rc=$?
  log "re-apply FAILED (exit $rc)"
  exit 4
fi
