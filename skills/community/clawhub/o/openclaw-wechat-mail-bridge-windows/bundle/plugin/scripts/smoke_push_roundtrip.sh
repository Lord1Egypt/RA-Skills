#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"
SECRET="${SECRET:-dev-bridge-secret}"
CHAT_ID="${CHAT_ID:-mock-group-001}"
CHAT_NAME="${CHAT_NAME:-Ops Group}"
SIDECAR_ID="${SIDECAR_ID:-smoke-sidecar}"
EMAIL="${EMAIL:-someone@example.com}"
WAIT_SEC="${WAIT_SEC:-60}"

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
  node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const j=JSON.parse(s);const parts='${path}'.split('.');let v=j;for(const p of parts){if(!p){continue;}if(/^[0-9]+$/.test(p)){v=v?.[Number(p)];}else{v=v?.[p];}}if(v===undefined||v===null){process.exit(1);}process.stdout.write(String(v));});"
}

echo "[1/6] post /watch event"
WATCH_RES="$(
  post_json "/api/v1/sidecar/events" "$(cat <<JSON
{
  "eventId":"evt_watch_smoke_$(date +%s)",
  "source":"windows-sidecar",
  "sidecarId":"${SIDECAR_ID}",
  "platform":"wechat-desktop",
  "chatType":"group",
  "chatId":"${CHAT_ID}",
  "chatName":"${CHAT_NAME}",
  "senderDisplayName":"Smoke",
  "messageId":"msg_watch_smoke_$(date +%s)",
  "messageText":"/watch ${EMAIL} ${WAIT_SEC}",
  "messageTime":"$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "observedAt":"$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON
)"
)"
echo "${WATCH_RES}"
WATCH_JOB_ID="$(printf '%s' "${WATCH_RES}" | parse_json_path "result.jobId")"
WATCH_CMD_ID="$(printf '%s' "${WATCH_RES}" | parse_json_path "result.commandId")"

echo "[2/6] claim + ack watch-start command"
CLAIM1_RES="$(post_json "/api/v1/sidecar/commands/claim" "{\"sidecarId\":\"${SIDECAR_ID}\",\"limit\":5}")"
echo "${CLAIM1_RES}"
ACK1_RES="$(post_json "/api/v1/sidecar/commands/${WATCH_CMD_ID}/ack" "{\"sidecarId\":\"${SIDECAR_ID}\",\"status\":\"sent\"}")"
echo "${ACK1_RES}"

echo "[3/6] post webhook payload"
WEBHOOK_RES="$(
  post_json "/api/v1/bhmailer/webhook" "$(cat <<JSON
{
  "matchedEmail":"${EMAIL}",
  "subject":"OTP code",
  "from":"no-reply@example.com",
  "receivedAt":"$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "bodyPreview":"Your verification code is 123456",
  "extractedFields":{"code":"123456"}
}
JSON
)"
)"
echo "${WEBHOOK_RES}"
WEBHOOK_CMD_ID="$(printf '%s' "${WEBHOOK_RES}" | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const j=JSON.parse(s);const ids=Array.isArray(j.commandIds)?j.commandIds:[];if(ids.length===0){process.exit(1);}process.stdout.write(String(ids[0]));});")"

echo "[4/6] claim + ack webhook reply command"
CLAIM2_RES="$(post_json "/api/v1/sidecar/commands/claim" "{\"sidecarId\":\"${SIDECAR_ID}\",\"limit\":5}")"
echo "${CLAIM2_RES}"
ACK2_RES="$(post_json "/api/v1/sidecar/commands/${WEBHOOK_CMD_ID}/ack" "{\"sidecarId\":\"${SIDECAR_ID}\",\"status\":\"sent\"}")"
echo "${ACK2_RES}"

echo "[5/6] verify no active watch remains"
WATCH_LIST_RES="$(post_json "/api/v1/admin/watch/list" "{\"limit\":20}")"
echo "${WATCH_LIST_RES}"

echo "[6/6] verify job list/receipts"
JOBS_RES="$(post_json "/api/v1/admin/jobs/list" "{\"limit\":20}")"
echo "${JOBS_RES}"
RCPT_RES="$(post_json "/api/v1/admin/receipts/list" "{\"limit\":20}")"
echo "${RCPT_RES}"

echo "smoke push roundtrip completed: jobId=${WATCH_JOB_ID} startCmd=${WATCH_CMD_ID} webhookCmd=${WEBHOOK_CMD_ID}"
