#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="openclaw-mobile-gateway"
PORT="${GATEWAY_PORT:-4800}"

echo "[1] systemd status"
if sudo -n true >/dev/null 2>&1; then
  sudo systemctl --no-pager --full status "${SERVICE_NAME}" | sed -n '1,20p' || true
else
  systemctl --no-pager --full status "${SERVICE_NAME}" | sed -n '1,20p' || true
fi

echo
echo "[2] listening port"
ss -ltnp | grep -E ":${PORT}\b" || true

echo
echo "[3] health endpoint"
curl -sS -m 8 "http://127.0.0.1:${PORT}/health" || true
echo

echo "[4] quick actions endpoint"
curl -sS -m 8 "http://127.0.0.1:${PORT}/api/quick-actions" || true
echo

echo "[5] routing strategies endpoint"
curl -sS -m 8 "http://127.0.0.1:${PORT}/api/routing/strategies" || true
echo
