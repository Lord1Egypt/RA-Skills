#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

BRIDGE_SRC="$SKILL_DIR/scripts/knods_iris_bridge.py"
BRIDGE_DST="$OPENCLAW_HOME/scripts/knods_iris_bridge.py"
ENV_FILE="$OPENCLAW_HOME/.env"
SERVICE_NAME="knods-iris-bridge.service"
SERVICE_PATH="$SYSTEMD_USER_DIR/$SERVICE_NAME"

OPENCLAW_BIN_DETECTED="$(command -v openclaw || true)"
if [[ -z "$OPENCLAW_BIN_DETECTED" ]]; then
  OPENCLAW_BIN_DETECTED="$HOME/.npm-global/bin/openclaw"
fi

mkdir -p "$OPENCLAW_HOME/scripts" "$SYSTEMD_USER_DIR"
install -m 0755 "$BRIDGE_SRC" "$BRIDGE_DST"

cat >"$SERVICE_PATH" <<EOF
[Unit]
Description=Knods Iris Bridge (OpenClaw)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$HOME
EnvironmentFile=$ENV_FILE
Environment=PYTHONUNBUFFERED=1
Environment=PATH=$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
Environment=OPENCLAW_BIN=$OPENCLAW_BIN_DETECTED
ExecStart=/usr/bin/python3 $BRIDGE_DST
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now "$SERVICE_NAME"

echo "Installed bridge script: $BRIDGE_DST"
echo "Installed service unit:  $SERVICE_PATH"
echo "Service status:"
systemctl --user --no-pager --full status "$SERVICE_NAME" | sed -n '1,20p'
echo
echo "Required env in $ENV_FILE:"
echo "  KNODS_BASE_URL=..."
echo "Optional when URL has no token:"
echo "  KNODS_GATEWAY_TOKEN=gw_..."
echo "Optional agent override:"
echo "  OPENCLAW_AGENT_ID=iris"
