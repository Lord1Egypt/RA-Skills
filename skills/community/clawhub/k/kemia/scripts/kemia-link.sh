#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# kemia-link — Generate a one-time login URL for the kemia web interface
#
# Usage: kemia-link.sh
# =============================================================================

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_FILE="${WORKSPACE}/skills/kemia/config.json"

command -v jq &>/dev/null || { echo "ERROR: jq is required."; exit 1; }

if [ ! -f "${CONFIG_FILE}" ]; then
  echo "ERROR: Not connected to kemia. Run /connect first."
  exit 1
fi

BASE_URL=$(jq -r '.baseUrl' "${CONFIG_FILE}")
API_KEY=$(jq -r '.apiKey' "${CONFIG_FILE}")

TOKEN_RESPONSE=$(curl -sf \
  -X POST \
  -H "Authorization: Bearer ${API_KEY}" \
  "${BASE_URL}/api/v1/auth-token") || {
  echo "ERROR: Failed to generate login URL. Check your connection with /kemia-status."
  exit 1
}

LOGIN_URL=$(echo "${TOKEN_RESPONSE}" | jq -r '.url')
EXPIRES=$(echo "${TOKEN_RESPONSE}" | jq -r '.expiresAt')

echo "Login URL (single-use, expires in 15 min):"
echo ""
echo "  ${LOGIN_URL}"
echo ""
echo "  Expires: ${EXPIRES}"
