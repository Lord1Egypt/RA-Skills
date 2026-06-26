#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="openclaw-mobile-gateway"
INSTALL_DIR="${INSTALL_DIR:-/opt/openclaw-mobile-gateway}"

sudo systemctl stop "${SERVICE_NAME}" 2>/dev/null || true
sudo systemctl disable "${SERVICE_NAME}" 2>/dev/null || true
sudo rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
sudo systemctl daemon-reload
sudo rm -rf /etc/openclaw-mobile-gateway
sudo rm -rf "${INSTALL_DIR}"

echo "Uninstalled ${SERVICE_NAME}."
