#!/usr/bin/env bash
set -euo pipefail

# OpenClaw Safe Change Runner (hardened)
# Usage:
#   safe-change.sh --main-script ./edit-main.sh [--secondary-script ./edit-secondary.sh]

MAIN_CFG="${MAIN_CFG:-$HOME/.openclaw/openclaw.json}"
SECONDARY_CFG="${SECONDARY_CFG:-$HOME/.openclaw-secondary/openclaw.json}"
SECONDARY_HOME="${SECONDARY_HOME:-$HOME/.openclaw-secondary}"
SECONDARY_URL="${SECONDARY_URL:-ws://127.0.0.1:18889}"
SECONDARY_TOKEN="${SECONDARY_TOKEN:-}"

MAIN_SCRIPT=""
SECONDARY_SCRIPT=""

usage() {
  cat <<'USAGE'
Usage:
  safe-change.sh --main-script <path> [--secondary-script <path>]

Notes:
  - Use script-file mode to avoid inline command injection patterns.
  - Provide SECONDARY_TOKEN via environment variable when secondary validation is enabled.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --main-script) MAIN_SCRIPT="$2"; shift 2 ;;
    --secondary-script) SECONDARY_SCRIPT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 2 ;;
  esac
done

if [[ -z "$MAIN_SCRIPT" ]]; then
  echo "ERROR: --main-script is required"
  usage
  exit 2
fi

if [[ ! -f "$MAIN_SCRIPT" ]]; then
  echo "ERROR: main script not found: $MAIN_SCRIPT"
  exit 2
fi

if [[ -n "$SECONDARY_SCRIPT" && ! -f "$SECONDARY_SCRIPT" ]]; then
  echo "ERROR: secondary script not found: $SECONDARY_SCRIPT"
  exit 2
fi

TS=$(date +%Y%m%d-%H%M%S)
MAIN_BAK="${MAIN_CFG}.bak.safe-${TS}"
SECONDARY_BAK="${SECONDARY_CFG}.bak.safe-${TS}"

cp "$MAIN_CFG" "$MAIN_BAK"
[[ -f "$SECONDARY_CFG" ]] && cp "$SECONDARY_CFG" "$SECONDARY_BAK" || true

echo "[1/5] backups created"

echo "[2/5] apply main change via script"
bash "$MAIN_SCRIPT"

if [[ -n "$SECONDARY_SCRIPT" ]]; then
  echo "[2b/5] apply secondary change via script"
  bash "$SECONDARY_SCRIPT"
fi

rollback() {
  echo "[rollback] restoring backups..."
  cp "$MAIN_BAK" "$MAIN_CFG" || true
  if [[ -f "$SECONDARY_BAK" ]]; then cp "$SECONDARY_BAK" "$SECONDARY_CFG" || true; fi
  openclaw gateway restart >/dev/null 2>&1 || true
  if command -v launchctl >/dev/null 2>&1; then
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway.secondary" >/dev/null 2>&1 || true
  fi
  echo "[rollback] done"
}

echo "[3/5] validate main"
if ! openclaw status --deep >/dev/null 2>&1; then
  echo "[error] main validation failed"
  rollback
  exit 1
fi

echo "[4/5] validate secondary (if exists)"
if [[ -f "$SECONDARY_CFG" ]]; then
  if [[ -z "$SECONDARY_TOKEN" ]]; then
    echo "[error] SECONDARY_TOKEN env var is required when secondary instance is enabled"
    rollback
    exit 1
  fi
  if ! OPENCLAW_HOME="$SECONDARY_HOME" openclaw gateway health --url "$SECONDARY_URL" --token "$SECONDARY_TOKEN" >/dev/null 2>&1; then
    echo "[error] secondary validation failed"
    rollback
    exit 1
  fi
fi

echo "[5/5] success: changes applied safely"
echo "main backup: $MAIN_BAK"
[[ -f "$SECONDARY_BAK" ]] && echo "secondary backup: $SECONDARY_BAK" || true
