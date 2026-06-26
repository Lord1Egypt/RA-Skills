#!/usr/bin/env bash
set -euo pipefail

log() {
  >&2 echo "[persona-client] $*"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUEST_SCRIPT="$SCRIPT_DIR/request_persona.sh"

PERSONA_SERVICE_URL="${PERSONA_SERVICE_URL:-}"
PERSONA_CLIENT_ID="${PERSONA_CLIENT_ID:-}"
PERSONA_CLIENT_SHARED_SECRET="${PERSONA_CLIENT_SHARED_SECRET:-}"
POLL_INTERVAL_SECONDS="${PERSONA_CLIENT_POLL_INTERVAL_SECONDS:-10}"
MAX_BACKOFF_SECONDS="${PERSONA_CLIENT_MAX_BACKOFF_SECONDS:-60}"

if [[ -z "$PERSONA_SERVICE_URL" || -z "$PERSONA_CLIENT_ID" ]]; then
  log "PERSONA_SERVICE_URL and PERSONA_CLIENT_ID must be set in the environment."
  exit 1
fi

if [[ ! -x "$REQUEST_SCRIPT" ]]; then
  if [[ -f "$REQUEST_SCRIPT" ]]; then
    chmod +x "$REQUEST_SCRIPT" 2>/dev/null || true
  fi
fi

if [[ ! -x "$REQUEST_SCRIPT" ]]; then
  log "request_persona.sh not found or not executable at $REQUEST_SCRIPT"
  exit 1
fi

http_get_next() {
  local url
  url="${PERSONA_SERVICE_URL%/}/persona/client/next?client_id=${PERSONA_CLIENT_ID}"
  local args=()
  if [[ -n "$PERSONA_CLIENT_SHARED_SECRET" ]]; then
    args+=(-H "X-Client-Secret: ${PERSONA_CLIENT_SHARED_SECRET}")
  fi
  curl -sS --fail "${args[@]}" "$url"
}

http_post_response() {
  local body="$1"
  local url
  url="${PERSONA_SERVICE_URL%/}/persona/client/responses"
  local args=(-H "Content-Type: application/json")
  if [[ -n "$PERSONA_CLIENT_SHARED_SECRET" ]]; then
    args+=(-H "X-Client-Secret: ${PERSONA_CLIENT_SHARED_SECRET}")
  fi
  curl -sS --fail "${args[@]}" -d "$body" "$url"
}

build_response_body() {
  # Uses RESULT_JSON, REQUEST_ID, PERSONA_CLIENT_ID from environment
  python3 - <<'PY'
import json
import os

raw = os.environ.get("RESULT_JSON", "{}")
request_id = os.environ["REQUEST_ID"]
client_id = os.environ["PERSONA_CLIENT_ID"]

try:
    data = json.loads(raw)
except Exception:
    data = {}

allowed = bool(data.get("allowed"))
persona_md = data.get("persona_md")
message = data.get("message") or "author did not authorize"

payload = {
    "request_id": request_id,
    "client_id": client_id,
    "allowed": allowed,
    "persona_md": persona_md,
    "message": message,
}
print(json.dumps(payload))
PY
}

handle_request() {
  local request_id="$1"
  local requester_id="$2"
  local reason="$3"

  log "handling request_id=${request_id} requester_id=${requester_id}"

  local result_json
  if ! result_json="$("$REQUEST_SCRIPT" "$requester_id" "$reason")"; then
    log "request_persona.sh failed; treating as denial"
    result_json='{"allowed": false, "message": "author did not authorize"}'
  fi

  export REQUEST_ID="$request_id"
  export RESULT_JSON="$result_json"
  body="$(build_response_body)"
  unset REQUEST_ID RESULT_JSON

  local backoff="$POLL_INTERVAL_SECONDS"
  while true; do
    if http_post_response "$body"; then
      log "submitted result for request_id=${request_id}"
      break
    fi
    log "failed to submit result for request_id=${request_id}, retrying in ${backoff}s"
    sleep "$backoff"
    backoff=$((backoff * 2))
    if (( backoff > MAX_BACKOFF_SECONDS )); then
      backoff="$MAX_BACKOFF_SECONDS"
    fi
  done
}

main_loop() {
  local backoff="$POLL_INTERVAL_SECONDS"

  while true; do
    local response
    if ! response="$(http_get_next)"; then
      log "error contacting persona-service, sleeping ${backoff}s"
      sleep "$backoff"
      backoff=$((backoff * 2))
      if (( backoff > MAX_BACKOFF_SECONDS )); then
        backoff="$MAX_BACKOFF_SECONDS"
      fi
      continue
    fi

    local parsed status request_id requester_id reason
    parsed="$(
      RESPONSE_JSON="$response" python3 - <<'PY'
import json
import os

data = json.loads(os.environ.get("RESPONSE_JSON", "{}"))
print(data.get("status", ""))
print(data.get("request_id", ""))
print(data.get("requester_id", ""))
print(data.get("reason", ""))
PY
    )"

    status="$(echo "$parsed" | sed -n '1p')"
    request_id="$(echo "$parsed" | sed -n '2p')"
    requester_id="$(echo "$parsed" | sed -n '3p')"
    reason="$(echo "$parsed" | sed -n '4p')"

    if [[ "$status" != "pending" || -z "$request_id" ]]; then
      backoff="$POLL_INTERVAL_SECONDS"
      sleep "$POLL_INTERVAL_SECONDS"
      continue
    fi

    backoff="$POLL_INTERVAL_SECONDS"
    handle_request "$request_id" "$requester_id" "$reason"
  done
}

log "starting persona-client polling loop against ${PERSONA_SERVICE_URL} for client_id=${PERSONA_CLIENT_ID}"
main_loop
