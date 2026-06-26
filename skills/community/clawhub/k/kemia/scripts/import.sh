#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# kemia import — Import deploy-ready snapshot into OpenClaw workspace
#
# Usage: import.sh [agent-id]
#
# Reads config.json for API credentials, fetches the deploy-ready snapshot,
# and writes files back to the OpenClaw workspace root.
# =============================================================================

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="${WORKSPACE}/skills/kemia"
CONFIG_FILE="${SKILL_DIR}/config.json"

# Require jq
command -v jq &>/dev/null || { echo "ERROR: jq is required."; exit 1; }

# Load config
if [ ! -f "${CONFIG_FILE}" ]; then
  echo "ERROR: Not connected to kemia. Run /connect first."
  exit 1
fi

BASE_URL=$(jq -r '.baseUrl' "${CONFIG_FILE}")
API_KEY=$(jq -r '.apiKey' "${CONFIG_FILE}")
AGENT_ID="${1:-$(jq -r '.agentId // empty' "${CONFIG_FILE}")}"

if [ -z "${AGENT_ID}" ]; then
  echo "ERROR: No agent ID specified and none saved in config."
  echo "Usage: import.sh <agent-id>"
  exit 1
fi

# ---- Fetch deploy-ready snapshot ----
echo "Checking for deploy-ready snapshot (agent: ${AGENT_ID})..."

HTTP_CODE=$(curl -s -o /tmp/kemia-deploy-response.json -w "%{http_code}" \
  -H "Authorization: Bearer ${API_KEY}" \
  "${BASE_URL}/api/v1/agents/${AGENT_ID}/deploy")

if [ "${HTTP_CODE}" = "404" ]; then
  echo "No deploy-ready snapshot found."
  echo "Mark a snapshot as 'deploy ready' in the kemia web interface first."
  exit 0
fi

if [ "${HTTP_CODE}" != "200" ]; then
  echo "ERROR: API returned HTTP ${HTTP_CODE}"
  cat /tmp/kemia-deploy-response.json 2>/dev/null
  exit 1
fi

RESPONSE=$(cat /tmp/kemia-deploy-response.json)
rm -f /tmp/kemia-deploy-response.json

SNAPSHOT_NAME=$(echo "${RESPONSE}" | jq -r '.snapshot.name')
SNAPSHOT_ID=$(echo "${RESPONSE}" | jq -r '.snapshot.id')
FILE_COUNT=$(echo "${RESPONSE}" | jq '.files | length')

echo "✓ Found snapshot '${SNAPSHOT_NAME}' with ${FILE_COUNT} files."

# ---- Backup current files ----
BACKUP_DIR="${WORKSPACE}/.kemia-backup/$(date +%Y%m%d-%H%M%S)"
mkdir -p "${BACKUP_DIR}"

echo "Backing up current files to ${BACKUP_DIR}..."
echo "${RESPONSE}" | jq -r '.files[].filename' | while read -r filename; do
  if [ -f "${WORKSPACE}/${filename}" ]; then
    cp "${WORKSPACE}/${filename}" "${BACKUP_DIR}/${filename}"
    echo "  ↪ ${filename}"
  fi
done

# ---- Write imported files ----
echo "Importing files to workspace..."

echo "${RESPONSE}" | jq -c '.files[]' | while read -r file; do
  FILENAME=$(echo "${file}" | jq -r '.filename')
  echo "${file}" | jq -r '.content' > "${WORKSPACE}/${FILENAME}"
  echo "  ✓ ${FILENAME}"
done

echo ""
echo "Import complete!"
echo "  Snapshot: ${SNAPSHOT_NAME} (${SNAPSHOT_ID})"
echo "  Files:    ${FILE_COUNT}"
echo "  Backup:   ${BACKUP_DIR}"
echo ""
echo "Restart your OpenClaw agent to apply the new config."
