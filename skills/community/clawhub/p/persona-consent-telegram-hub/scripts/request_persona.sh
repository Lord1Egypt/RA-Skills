#!/usr/bin/env bash
set -euo pipefail

REFUSAL_MESSAGE="author did not authorize"
DEFAULT_ALLOWED_PERSONA_PATH="/home/claw/.openclaw/persona.md"

print_refusal() {
  python3 - "$REFUSAL_MESSAGE" <<'PY'
import json
import sys

msg = sys.argv[1]
print(json.dumps({"allowed": False, "message": msg}))
PY
}

print_approved() {
  local persona_path="$1"
  python3 - "$persona_path" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
content = path.read_text(encoding="utf-8")
print(json.dumps({"allowed": True, "persona_md": content}))
PY
}

require_cmds() {
  local missing=0
  for cmd in bash curl python3 readlink; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      missing=1
    fi
  done
  return "$missing"
}

contains_csv_value() {
  local list="$1"
  local value="$2"
  IFS=',' read -r -a parts <<<"$list"
  for part in "${parts[@]}"; do
    local trimmed
    trimmed="$(echo "$part" | tr -d '[:space:]')"
    if [[ "$trimmed" == "$value" ]]; then
      return 0
    fi
  done
  return 1
}

safe_readlink() {
  local path="$1"
  readlink -f "$path" 2>/dev/null || true
}

send_owner_prompt() {
  local api_base="$1"
  local bot_token="$2"
  local owner_chat_id="$3"
  local request_id="$4"
  local requester_id="$5"
  local reason="$6"

  local text
  text=$(
    cat <<EOF
Persona access request
requester_id: $requester_id
reason: $reason

Tap a button below to approve or deny.
EOF
  )

  local reply_markup
  reply_markup="$(
    python3 - "$request_id" <<'PY'
import json
import sys

request_id = sys.argv[1]
markup = {
    "inline_keyboard": [[
        {"text": "Approve", "callback_data": f"approve:{request_id}"},
        {"text": "Deny", "callback_data": f"deny:{request_id}"},
    ]]
}
print(json.dumps(markup, separators=(",", ":")))
PY
  )"

  curl -sS --fail \
    --request POST \
    --data-urlencode "chat_id=$owner_chat_id" \
    --data-urlencode "text=$text" \
    --data-urlencode "reply_markup=$reply_markup" \
    "$api_base/bot$bot_token/sendMessage" >/dev/null
}

poll_for_decision() {
  local api_base="$1"
  local bot_token="$2"
  local owner_chat_id="$3"
  local request_id="$4"
  local timeout_seconds="$5"
  local poll_interval="$6"
  local offset_file="$7"

  local offset="0"
  if [[ -f "$offset_file" ]]; then
    local raw_offset
    raw_offset="$(<"$offset_file")"
    if [[ "$raw_offset" =~ ^[0-9]+$ ]]; then
      offset="$raw_offset"
    fi
  fi

  local started_at
  started_at="$(date +%s)"

  while true; do
    local now elapsed
    now="$(date +%s)"
    elapsed="$((now - started_at))"
    if (( elapsed >= timeout_seconds )); then
      echo "timeout"
      return 0
    fi

    local response
    if ! response="$(
      curl -sS --fail \
        --request POST \
        --data-urlencode "offset=$offset" \
        --data-urlencode "timeout=$poll_interval" \
        --data-urlencode 'allowed_updates=["message","callback_query"]' \
        "$api_base/bot$bot_token/getUpdates"
    )"; then
      sleep "$poll_interval"
      continue
    fi

    local parsed
    parsed="$(
      RESPONSE_JSON="$response" python3 - "$owner_chat_id" "$request_id" <<'PY'
import json
import os
import sys

owner_chat_id = sys.argv[1]
request_id = sys.argv[2]
response = json.loads(os.environ.get("RESPONSE_JSON", "{}"))
updates = response.get("result", [])

max_update_id = None
decision = "none"

for update in updates:
    uid = update.get("update_id")
    if isinstance(uid, int):
        max_update_id = uid if max_update_id is None else max(max_update_id, uid)

    # Text command path (backward compatible)
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = str(chat.get("id", ""))
    text = message.get("text", "")
    if chat_id == owner_chat_id:
        if text == f"/approve {request_id}":
            decision = "approve"
        if text == f"/deny {request_id}":
            decision = "deny"

    # Inline button path (preferred)
    callback = update.get("callback_query") or {}
    from_user = callback.get("from") or {}
    from_id = str(from_user.get("id", ""))
    data = callback.get("data", "")
    if from_id == owner_chat_id:
        if data == f"approve:{request_id}":
            decision = "approve"
        if data == f"deny:{request_id}":
            decision = "deny"

print("" if max_update_id is None else str(max_update_id + 1))
print(decision)
PY
    )"

    local next_offset decision
    next_offset="$(echo "$parsed" | sed -n '1p')"
    decision="$(echo "$parsed" | sed -n '2p')"

    if [[ -n "$next_offset" && "$next_offset" =~ ^[0-9]+$ ]]; then
      offset="$next_offset"
      mkdir -p "$(dirname "$offset_file")"
      echo "$offset" >"$offset_file"
    fi

    if [[ "$decision" == "approve" ]]; then
      echo "approve"
      return 0
    fi
    if [[ "$decision" == "deny" ]]; then
      echo "deny"
      return 0
    fi

    sleep "$poll_interval"
  done
}

main() {
  local requester_id="${1:-unknown}"
  local reason="${2:-persona request}"

  local telegram_bot_token="${TELEGRAM_BOT_TOKEN:-}"
  local telegram_owner_chat_id="${TELEGRAM_OWNER_CHAT_ID:-}"
  local persona_path="${PERSONA_PATH:-$DEFAULT_ALLOWED_PERSONA_PATH}"
  local allowed_persona_path="${ALLOWED_PERSONA_PATH:-$DEFAULT_ALLOWED_PERSONA_PATH}"
  local request_timeout="${REQUEST_TIMEOUT_SECONDS:-90}"
  local poll_interval="${POLL_INTERVAL_SECONDS:-2}"
  local requester_allowlist="${REQUESTER_ALLOWLIST:-}"
  local telegram_api_base="${TELEGRAM_API_BASE:-https://api.telegram.org}"
  local offset_file="${TELEGRAM_UPDATES_OFFSET_FILE:-${XDG_STATE_HOME:-$HOME/.local/state}/persona-consent-telegram/updates.offset}"

  if ! require_cmds; then
    print_refusal
    return 0
  fi

  if [[ -z "$telegram_bot_token" || -z "$telegram_owner_chat_id" ]]; then
    print_refusal
    return 0
  fi

  if ! [[ "$request_timeout" =~ ^[0-9]+$ ]] || ! [[ "$poll_interval" =~ ^[0-9]+$ ]]; then
    print_refusal
    return 0
  fi

  if [[ -n "$requester_allowlist" ]] && ! contains_csv_value "$requester_allowlist" "$requester_id"; then
    print_refusal
    return 0
  fi

  local persona_real allowed_real
  persona_real="$(safe_readlink "$persona_path")"
  allowed_real="$(safe_readlink "$allowed_persona_path")"
  if [[ -z "$persona_real" || -z "$allowed_real" || "$persona_real" != "$allowed_real" ]]; then
    print_refusal
    return 0
  fi
  if [[ ! -f "$persona_real" ]]; then
    print_refusal
    return 0
  fi

  local request_id
  request_id="$(date +%s)-$RANDOM"

  if ! send_owner_prompt "$telegram_api_base" "$telegram_bot_token" "$telegram_owner_chat_id" "$request_id" "$requester_id" "$reason"; then
    print_refusal
    return 0
  fi

  local decision
  decision="$(poll_for_decision "$telegram_api_base" "$telegram_bot_token" "$telegram_owner_chat_id" "$request_id" "$request_timeout" "$poll_interval" "$offset_file")"
  case "$decision" in
    approve)
      print_approved "$persona_real"
      ;;
    deny | timeout | *)
      print_refusal
      ;;
  esac
}

main "$@"
