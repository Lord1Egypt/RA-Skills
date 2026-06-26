#!/usr/bin/env bash
set -euo pipefail

MAIN_GATEWAY_HTTP="${MAIN_GATEWAY_HTTP:-http://192.168.88.11:18789}"
MAIN_GATEWAY_WS="${MAIN_GATEWAY_WS:-ws://192.168.88.11:18789}"
LOCAL_DEV_BIND="${LOCAL_DEV_BIND:-127.0.0.1}"
LOCAL_DEV_PORT="${LOCAL_DEV_PORT:-28789}"

cat <<EOF
# Mac local dev controller/gateway contract
# Keep this local-only. Do not publish it to the LAN.

MAIN_OPENCLAW_GATEWAY_HTTP=$MAIN_GATEWAY_HTTP
MAIN_OPENCLAW_GATEWAY_WS=$MAIN_GATEWAY_WS

MAC_DEV_GATEWAY_BIND=$LOCAL_DEV_BIND
MAC_DEV_GATEWAY_PORT=$LOCAL_DEV_PORT
MAC_DEV_GATEWAY_HTTP=http://$LOCAL_DEV_BIND:$LOCAL_DEV_PORT
MAC_DEV_GATEWAY_WS=ws://$LOCAL_DEV_BIND:$LOCAL_DEV_PORT

# Suggested tool/test ports
MAC_DEV_NGINX_PORT=8080
MAC_DEV_VITE_PORT=5173
MAC_DEV_BROWSERSYNC_PORT=3000
MAC_DEV_BROWSERSYNC_UI_PORT=3001

# Suggested runtime rule
# - production/shared gateway stays on the Ryzen
# - local dev controller stays loopback-only on the Mac
EOF
