#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_SRC="$ROOT_DIR/templates/openclaw-watchdog.service"
TIMER_SRC="$ROOT_DIR/templates/openclaw-watchdog.timer"
TARGET_DIR="${1:-/etc/systemd/system}"

install -m 0644 "$SERVICE_SRC" "$TARGET_DIR/openclaw-watchdog.service"
install -m 0644 "$TIMER_SRC" "$TARGET_DIR/openclaw-watchdog.timer"

cat <<EOF
Installed:
  $TARGET_DIR/openclaw-watchdog.service
  $TARGET_DIR/openclaw-watchdog.timer

Next steps:
  sudo systemctl daemon-reload
  sudo systemctl enable --now openclaw-watchdog.timer
EOF
