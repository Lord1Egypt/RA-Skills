#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-/opt/openclaw-mobile-gateway}"
RUN_USER="${RUN_USER:-${SUDO_USER:-$(id -un)}}"
RUN_GROUP="${RUN_GROUP:-$(id -gn "${RUN_USER}")}"
GATEWAY_PORT="${GATEWAY_PORT:-4800}"
OPENCLAW_API_BASE_URL="${OPENCLAW_API_BASE_URL:-}"
OPENCLAW_AUTH_HEADER_NAME="${OPENCLAW_AUTH_HEADER_NAME:-Authorization}"
OPENCLAW_AUTH_HEADER_VALUE="${OPENCLAW_AUTH_HEADER_VALUE:-}"
RUN_HOME="$(getent passwd "${RUN_USER}" | cut -d: -f6 || true)"
if [[ -z "${RUN_HOME}" ]]; then
  RUN_HOME="/home/${RUN_USER}"
fi
OPENCLAW_CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-${RUN_HOME}/.openclaw/openclaw.json}"
OPENCLAW_RUNTIME_CONFIG_PATH="${OPENCLAW_RUNTIME_CONFIG_PATH:-${OPENCLAW_CONFIG_PATH}}"
OPENCLAW_USAGE_CONFIG_PATH="${OPENCLAW_USAGE_CONFIG_PATH:-${OPENCLAW_CONFIG_PATH}}"
OPENCLAW_USAGE_DAYS="${OPENCLAW_USAGE_DAYS:-7}"
SERVICE_NAME="openclaw-mobile-gateway"
PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "${OPENCLAW_API_BASE_URL}" ]]; then
  echo "ERROR: OPENCLAW_API_BASE_URL is required"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: node is required"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "ERROR: npm is required"
  exit 1
fi

sudo mkdir -p "${INSTALL_DIR}"
sudo mkdir -p "${INSTALL_DIR}/apps"
sudo rsync -a --delete "${PACKAGE_ROOT}/backend/" "${INSTALL_DIR}/apps/backend/"
sudo chown -R "${RUN_USER}:${RUN_GROUP}" "${INSTALL_DIR}"

pushd "${INSTALL_DIR}/apps/backend" >/dev/null
npm install --omit=optional
popd >/dev/null

sudo mkdir -p /etc/openclaw-mobile-gateway
sudo tee /etc/openclaw-mobile-gateway/env >/dev/null <<EOF
OPENCLAW_API_BASE_URL=${OPENCLAW_API_BASE_URL}
OPENCLAW_AUTH_HEADER_NAME=${OPENCLAW_AUTH_HEADER_NAME}
OPENCLAW_AUTH_HEADER_VALUE=${OPENCLAW_AUTH_HEADER_VALUE}
OPENCLAW_CONFIG_PATH=${OPENCLAW_CONFIG_PATH}
OPENCLAW_RUNTIME_CONFIG_PATH=${OPENCLAW_RUNTIME_CONFIG_PATH}
OPENCLAW_USAGE_CONFIG_PATH=${OPENCLAW_USAGE_CONFIG_PATH}
OPENCLAW_USAGE_DAYS=${OPENCLAW_USAGE_DAYS}
PORT=${GATEWAY_PORT}
NODE_ENV=production
EOF

sudo tee /etc/systemd/system/${SERVICE_NAME}.service >/dev/null <<EOF
[Unit]
Description=OpenClaw Mobile Admin Gateway
After=network.target

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_GROUP}
WorkingDirectory=${INSTALL_DIR}/apps/backend
EnvironmentFile=/etc/openclaw-mobile-gateway/env
Environment=HOME=${RUN_HOME}
ExecStart=/usr/bin/env node ./node_modules/tsx/dist/cli.mjs src/index.ts
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}
sleep 2
sudo systemctl --no-pager --full status ${SERVICE_NAME} | sed -n '1,18p'

echo
echo "Gateway installed."
echo "Health check: curl http://127.0.0.1:${GATEWAY_PORT}/health"
echo "APK base URL:  http://<server-ip>:${GATEWAY_PORT}"
