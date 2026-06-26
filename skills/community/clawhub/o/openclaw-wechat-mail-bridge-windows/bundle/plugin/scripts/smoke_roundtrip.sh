#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"
SECRET="${SECRET:-dev-bridge-secret}"
CHAT_ID="${CHAT_ID:-mock-group-001}"
CHAT_NAME="${CHAT_NAME:-Ops Group}"
SIDECAR_ID="${SIDECAR_ID:-smoke-sidecar}"
TEXT="${TEXT:-/mail someone@example.com}"

post_json() {
  local path="$1"
  local body="$2"
  local ts
  ts="$(date +%s)"
  local nonce
  nonce="nonce_$(date +%s%N)"

  curl -sS -X POST "${BASE_URL}${path}" \
    -H "Authorization: Bearer ${SECRET}" \
    -H "x-bridge-ts: ${ts}" \
    -H "x-bridge-nonce: ${nonce}" \
    -H "content-type: application/json" \
    -d "${body}"
}

parse_json_path() {
  local path="$1"
  node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const j=JSON.parse(s);const parts='${path}'.split('.');let v=j;for(const p of parts){if(!p){continue;}v=v?.[p];}if(v===undefined||v===null){process.exit(1);}process.stdout.write(String(v));});"
}

echo "[1/5] post sidecar event"
INGEST_RES="$(
  post_json "/api/v1/sidecar/events" "$(cat <<JSON
{
  "eventId":"evt_smoke_$(date +%s)",
  "source":"windows-sidecar",
  "sidecarId":"${SIDECAR_ID}",
  "platform":"wechat-desktop",
  "chatType":"group",
  "chatId":"${CHAT_ID}",
  "chatName":"${CHAT_NAME}",
  "senderDisplayName":"Smoke",
  "messageId":"msg_smoke_$(date +%s)",
  "messageText":"${TEXT}",
  "messageTime":"$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "observedAt":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON
)"
)"
echo "${INGEST_RES}"
COMMAND_ID="$(printf '%s' "${INGEST_RES}" | parse_json_path "result.commandId")"
JOB_ID="$(printf '%s' "${INGEST_RES}" | parse_json_path "result.jobId")"

echo "[2/5] claim commands"
CLAIM_RES="$(post_json "/api/v1/sidecar/commands/claim" "{\"sidecarId\":\"${SIDECAR_ID}\",\"limit\":5}")"
echo "${CLAIM_RES}"

echo "[3/5] ack command sent"
ACK_RES="$(post_json "/api/v1/sidecar/commands/${COMMAND_ID}/ack" "{\"sidecarId\":\"${SIDECAR_ID}\",\"status\":\"sent\"}")"
echo "${ACK_RES}"

echo "[4/5] list receipts"
RCPT_RES="$(post_json "/api/v1/admin/receipts/list" "{\"limit\":10}")"
echo "${RCPT_RES}"

echo "[5/5] verify job status"
JOBS_RES="$(post_json "/api/v1/admin/jobs/list" "{\"limit\":10}")"
echo "${JOBS_RES}"

echo "smoke roundtrip completed: jobId=${JOB_ID} commandId=${COMMAND_ID}"
