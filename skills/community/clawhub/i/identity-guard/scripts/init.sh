#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../identities.json"
TEMPLATE_FILE="${SCRIPT_DIR}/../identities.template.json"

prompt() {
  local label="$1"
  local value=""
  read -r -p "${label}: " value
  echo "${value}"
}

CHANNEL="$(prompt "Channel (e.g., feishu, telegram)")"
SENDER_ID="$(prompt "Your sender_id")"

if [[ -z "${CHANNEL}" || -z "${SENDER_ID}" ]]; then
  echo "Both channel and sender_id are required." >&2
  echo "Tip: run ./scripts/whoami.sh or ask the bot with /whoami to get your sender_id." >&2
  exit 1
fi

if [[ -f "${CONFIG_FILE}" ]]; then
  cp "${CONFIG_FILE}" "${CONFIG_FILE}.bak.$(date +%Y%m%d-%H%M%S)"
elif [[ -f "${TEMPLATE_FILE}" ]]; then
  cp "${TEMPLATE_FILE}" "${CONFIG_FILE}"
else
  echo "Error: Template file not found: ${TEMPLATE_FILE}" >&2
  exit 1
fi

if grep -q "\"${CHANNEL}\"" "${CONFIG_FILE}"; then
  sed -i.bak -E "/\"${CHANNEL}\"/,/\"allowlist\"/ s/\"master_id\": \"[^\"]*\"/\"master_id\": \"${SENDER_ID}\"/" "${CONFIG_FILE}"
  rm -f "${CONFIG_FILE}.bak"
else
  TMP_FILE="$(mktemp)"
  awk -v channel="${CHANNEL}" -v sender="${SENDER_ID}" '
    /"channels": \{/ {
      print
      print "    \"" channel "\": {"
      print "      \"master_id\": \"" sender "\","
      print "      \"allowlist\": []"
      print "    },"
      next
    }
    { print }
  ' "${CONFIG_FILE}" > "${TMP_FILE}"
  mv "${TMP_FILE}" "${CONFIG_FILE}"
fi

echo "Updated ${CONFIG_FILE}"
