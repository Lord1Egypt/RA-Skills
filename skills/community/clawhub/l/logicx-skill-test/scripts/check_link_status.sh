#!/usr/bin/env bash
set -euo pipefail

# When the user says "我登录好了", run this script to check binding status.
# It reads link_code and install_id from the state file (saved by logicx_api.sh
# after agent/link/start) and calls agent/link/status. No need to remember them.
#
# Usage: scripts/check_link_status.sh
# Requires: LOGICX_BASE_URL, LOGICX_AGENT_SERVICE_KEY

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGICX_STATE_FILE="${LOGICX_STATE_FILE:-${HOME:-/tmp}/.config/logicx/skill-state.json}"

if [[ ! -f "$LOGICX_STATE_FILE" ]]; then
  echo "No bind state found. Please run agent/link/start first and open the login URL." >&2
  exit 1
fi

link_code="$(sed -n 's/.*"link_code"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$LOGICX_STATE_FILE" 2>/dev/null | head -1)"
install_id="$(sed -n 's/.*"install_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$LOGICX_STATE_FILE" 2>/dev/null | head -1)"

if [[ -z "$link_code" || -z "$install_id" ]]; then
  echo "No link_code or install_id in state. Please run agent/link/start first." >&2
  exit 1
fi

exec bash "$SCRIPT_DIR/logicx_api.sh" POST agent/link/status "{\"link_code\":\"$link_code\",\"install_id\":\"$install_id\"}"
