#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"
SECRET="${SECRET:-dev-bridge-secret}"
CHAT_ID="${CHAT_ID:-mock-group-001}"
CHAT_NAME="${CHAT_NAME:-Ops Group}"
SIDEcar_ID="${SIDECAR_ID:-winbox-01}"
TEXT="${TEXT:-/mail someone@example.com}"

TS="$(date +%s)"
EVENT_ID="evt_smoke_$(date +%s)"
MSG_ID="msg_smoke_$(date +%s)"

curl -sS -X POST "${BASE_URL}/api/v1/sidecar/events" \
  -H "Authorization: Bearer ${SECRET}" \
  -H "x-bridge-ts: ${TS}" \
  -H "content-type: application/json" \
  -d "{
    \"eventId\": \"${EVENT_ID}\",
    \"source\": \"windows-sidecar\",
    \"sidecarId\": \"${SIDEcar_ID}\",
    \"platform\": \"wechat-desktop\",
    \"chatType\": \"group\",
    \"chatId\": \"${CHAT_ID}\",
    \"chatName\": \"${CHAT_NAME}\",
    \"senderDisplayName\": \"Smoke\",
    \"messageId\": \"${MSG_ID}\",
    \"messageText\": \"${TEXT}\",
    \"messageTime\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"observedAt\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
  }"

