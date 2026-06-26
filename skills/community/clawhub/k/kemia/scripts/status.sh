#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# kemia status — Check connection, pending enrollment, and deploy state
#
# Usage: status.sh
# =============================================================================

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="${WORKSPACE}/skills/kemia"
CONFIG_FILE="${SKILL_DIR}/config.json"
STATE_FILE="${SKILL_DIR}/enrollment.json"

command -v jq >/dev/null 2>&1 || { echo "ERROR: jq is required."; exit 1; }

# ─── Case A: pending enrollment takes precedence ───────────────────────────
if [ -f "${STATE_FILE}" ]; then
  ENROLL_URL=$(jq -r '.enrollUrl // empty' "${STATE_FILE}")
  EXPIRES=$(jq -r '.expiresAt // empty' "${STATE_FILE}")
  echo "kemia Status"
  echo "════════════"
  echo "  State:       ⏳ PENDING CONFIRMATION"
  echo "  Link:        ${ENROLL_URL}"
  echo "  Expires:     ${EXPIRES}"
  echo ""
  echo "The user must open the link above and confirm in the browser."
  echo "Afterwards, run /kemia connect (no args) to complete."
  exit 0
fi

# ─── Case B: not connected ─────────────────────────────────────────────────
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "Status: NOT CONNECTED"
  echo "Run /kemia connect <kemia-url> to connect."
  exit 0
fi

# ─── Case C: verify connection ─────────────────────────────────────────────
BASE_URL=$(jq -r '.baseUrl' "${CONFIG_FILE}")
API_KEY=$(jq -r '.apiKey' "${CONFIG_FILE}")
INSTANCE_ID=$(jq -r '.instanceId' "${CONFIG_FILE}")
AGENT_ID=$(jq -r '.agentId // empty' "${CONFIG_FILE}")

echo "kemia Status"
echo "════════════"
echo "  Base URL:    ${BASE_URL}"
echo "  Instance ID: ${INSTANCE_ID}"

STATUS_RESPONSE=$(curl -sf -H "Authorization: Bearer ${API_KEY}" "${BASE_URL}/api/v1/status" 2>/dev/null) || {
  echo "  Connection:  ✗ UNREACHABLE"
  echo ""
  echo "Cannot reach kemia or API key is not accepted. Check URL/credentials."
  exit 1
}

INSTANCE_NAME=$(echo "${STATUS_RESPONSE}" | jq -r '.instanceName')
echo "  Instance:    ${INSTANCE_NAME}"
echo "  Connection:  ✓ OK"

if [ -n "${AGENT_ID}" ]; then
  echo "  Agent ID:    ${AGENT_ID}"

  DEPLOY_CODE=$(curl -s -o /tmp/kemia-status-deploy.json -w "%{http_code}" \
    -H "Authorization: Bearer ${API_KEY}" \
    "${BASE_URL}/api/v1/agents/${AGENT_ID}/deploy")

  if [ "${DEPLOY_CODE}" = "200" ]; then
    SNAP_NAME=$(jq -r '.snapshot.name' /tmp/kemia-status-deploy.json)
    SNAP_FILES=$(jq '.files | length' /tmp/kemia-status-deploy.json)
    echo "  Deploy:      ⚡ READY — '${SNAP_NAME}' (${SNAP_FILES} files)"
    echo ""
    echo "Run /import to apply the pending snapshot."
  else
    echo "  Deploy:      — no pending snapshot"
  fi
  rm -f /tmp/kemia-status-deploy.json
else
  echo "  Agent ID:    (none — run /kemia connect to export)"
fi
