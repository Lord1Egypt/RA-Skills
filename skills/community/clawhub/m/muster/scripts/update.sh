#!/usr/bin/env bash
set -euo pipefail

# Muster Update Script
# Pulls latest, rebuilds, migrates, restarts. Auto-rolls back on failure.
# Stops without updating for major version bumps (agent handles that decision).
#
# Supports both launchd (macOS) and pm2 (Linux/fallback) service modes.
# Auto-detects which is in use.
#
# Usage: bash update.sh [--install-dir DIR]
#
# Outputs JSON report to stdout. Progress to stderr.

INSTALL_DIR="${INSTALL_DIR:-$HOME/muster}"

while [[ $# -gt 0 ]]; do
  case $1 in --install-dir) INSTALL_DIR="$2"; shift 2 ;; *) echo "Unknown: $1" >&2; exit 1 ;; esac
done

log() { echo "[muster-update] $*" >&2; }
fail() { echo "[muster-update] FAILED: $*" >&2; exit 1; }

wait_for_healthy() {
  local url="$1" max="${2:-30}" i=0
  while [ $i -lt $max ]; do curl -sf "$url" &>/dev/null && return 0; sleep 2; i=$((i+1)); done; return 1
}

# Auto-detect service mode
detect_service_mode() {
  local LABEL="com.bai.muster"
  if launchctl list "$LABEL" &>/dev/null 2>&1; then
    echo "launchd"
  elif command -v pm2 &>/dev/null && pm2 describe muster &>/dev/null 2>&1; then
    echo "pm2"
  else
    echo "unknown"
  fi
}

restart_service() {
  local mode="$1"
  if [ "$mode" = "launchd" ]; then
    launchctl kickstart -k "gui/$(id -u)/com.bai.muster" 2>/dev/null || {
      log "⚠ launchctl kickstart failed — trying stop/start..."
      launchctl kickstart "gui/$(id -u)/com.bai.muster" 2>/dev/null || true
    }
  elif [ "$mode" = "pm2" ]; then
    pm2 restart muster
  else
    fail "No known service manager found. Restart Muster manually."
  fi
}

cd "$INSTALL_DIR" || fail "Install directory not found: $INSTALL_DIR"

SERVICE_MODE=$(detect_service_mode)
log "Detected service mode: $SERVICE_MODE"

CURRENT_VERSION=$(node -e "console.log(require('./package.json').version)" 2>/dev/null || echo "unknown")
CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
MUSTER_PORT=$(grep "^PORT=" .env 2>/dev/null | cut -d= -f2 || echo "3000")
log "Current: $CURRENT_VERSION (${CURRENT_COMMIT:0:8})"

git fetch origin main --quiet
REMOTE_VERSION=$(git show origin/main:package.json | node -e "const d=require('fs').readFileSync('/dev/stdin','utf8');console.log(JSON.parse(d).version)" 2>/dev/null || echo "unknown")

# Major version check
CURRENT_MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
REMOTE_MAJOR=$(echo "$REMOTE_VERSION" | cut -d. -f1)
if [ "$REMOTE_MAJOR" != "$CURRENT_MAJOR" ] && [ "$REMOTE_VERSION" != "unknown" ]; then
  cat <<REPORT_JSON
{"success":false,"action":"major_version_detected","current_version":"${CURRENT_VERSION}","available_version":"${REMOTE_VERSION}","message":"Major version update (v${CURRENT_MAJOR}→v${REMOTE_MAJOR}). Do not auto-update. Read UPDATE.md and get human confirmation."}
REPORT_JSON
  exit 0
fi

if [ "$REMOTE_VERSION" = "$CURRENT_VERSION" ]; then
  cat <<REPORT_JSON
{"success":true,"action":"already_current","current_version":"${CURRENT_VERSION}"}
REPORT_JSON
  exit 0
fi

log "Updating: $CURRENT_VERSION → $REMOTE_VERSION"
git pull origin main
npm install --silent
npm run build
npx drizzle-kit migrate
restart_service "$SERVICE_MODE"

if wait_for_healthy "http://localhost:${MUSTER_PORT}/api/health" 30; then
  NEW_VERSION=$(node -e "console.log(require('./package.json').version)" 2>/dev/null || echo "unknown")
  log "✓ Updated: $CURRENT_VERSION → $NEW_VERSION"
  cat <<REPORT_JSON
{"success":true,"action":"updated","previous_version":"${CURRENT_VERSION}","new_version":"${NEW_VERSION}","service_mode":"${SERVICE_MODE}"}
REPORT_JSON
else
  log "⚠ Health check failed. Rolling back..."
  git checkout "$CURRENT_COMMIT"
  npm install --silent
  npm run build
  restart_service "$SERVICE_MODE"
  ROLLBACK_OK=false
  wait_for_healthy "http://localhost:${MUSTER_PORT}/api/health" 30 && ROLLBACK_OK=true
  cat <<REPORT_JSON
{"success":false,"action":"rollback","current_version":"${CURRENT_VERSION}","attempted_version":"${REMOTE_VERSION}","rollback_healthy":${ROLLBACK_OK},"service_mode":"${SERVICE_MODE}"}
REPORT_JSON
fi
