#!/bin/bash
# Source GooseTown config from agent workspace
# AGENT_DIR is set by OpenClaw when running skill tools
_BC_CFG="${AGENT_DIR:-$(pwd)}/GOOSETOWN.md"
if [ ! -f "$_BC_CFG" ]; then
    echo '{"error": "GOOSETOWN.md not found. Run town_register first."}'
    exit 1
fi
export TOWN_TOKEN="$(grep '^token:' "$_BC_CFG" | head -1 | awk '{print $2}')"
export TOWN_WS_URL="$(grep '^ws_url:' "$_BC_CFG" | head -1 | awk '{print $2}')"
export TOWN_API_URL="$(grep '^api_url:' "$_BC_CFG" | head -1 | awk '{print $2}')"
export TOWN_AGENT="$(grep '^agent:' "$_BC_CFG" | head -1 | awk '{print $2}')"
export TOWN_WORKSPACE="$(grep '^workspace_path:' "$_BC_CFG" | head -1 | sed 's/^workspace_path: *//')"
export STATE_DIR="/tmp/goosetown/${TOWN_AGENT}"
mkdir -p "$STATE_DIR"
