#!/usr/bin/env bash

set -euo pipefail

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$LIB_DIR/.." && pwd)"
CONFIG_FILE="${PET_ME_CONFIG_FILE:-$SKILL_DIR/config.json}"
COOLDOWN_SECONDS="${PET_ME_COOLDOWN_SECONDS:-43260}"
DEFAULT_CONTRACT="0xA99c4B08201F2913Db8D28e71d020c4298F29dBF"
DEFAULT_CHAIN_ID="8453"
DEFAULT_RPC_URL="https://mainnet.base.org"
BANKR_API_URL="${BANKR_API_URL:-https://api.bankr.bot}"
CORE_SUBGRAPH_URL="${CORE_SUBGRAPH_URL:-https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn}"
BANKR_WALLET_CACHE_FILE="${PET_ME_BANKR_WALLET_CACHE_FILE:-/tmp/pet-me-master-bankr-wallet.txt}"
BANKR_WALLET_CACHE_MAX_AGE="${PET_ME_BANKR_WALLET_CACHE_MAX_AGE:-21600}"

CAST_BIN="${CAST_BIN:-}"
if [ -z "$CAST_BIN" ] && command -v cast >/dev/null 2>&1; then
  CAST_BIN="$(command -v cast)"
fi
if [ -z "$CAST_BIN" ] && [ -x "$HOME/.foundry/bin/cast" ]; then
  CAST_BIN="$HOME/.foundry/bin/cast"
fi

err() {
  echo "ERROR: $*" >&2
  exit 1
}

warn() {
  echo "WARN: $*" >&2
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || err "Missing required binary: $bin"
}

require_read_tools() {
  [ -n "$CAST_BIN" ] || err "Missing required binary: cast"
  require_bin jq
}

require_tx_tools() {
  require_read_tools
  require_bin curl
}

load_config() {
  [ -f "$CONFIG_FILE" ] || err "Config not found: $CONFIG_FILE"

  CONTRACT_ADDRESS="$(jq -r '.contractAddress // empty' "$CONFIG_FILE")"
  RPC_URL="$(jq -r '.rpcUrl // empty' "$CONFIG_FILE")"
  CHAIN_ID="$(jq -r '.chainId // empty' "$CONFIG_FILE")"

  [ -n "$CONTRACT_ADDRESS" ] || CONTRACT_ADDRESS="$DEFAULT_CONTRACT"
  [ -n "$RPC_URL" ] || RPC_URL="$DEFAULT_RPC_URL"
  [ -n "$CHAIN_ID" ] || CHAIN_ID="$DEFAULT_CHAIN_ID"

  mapfile -t GOTCHI_IDS < <(jq -r '.gotchiIds[]? | tostring' "$CONFIG_FILE" 2>/dev/null | sed '/^$/d')
}

default_gotchi_id() {
  local wallet
  local first

  wallet="$(resolve_agent_wallet_address 2>/dev/null || true)"
  if [ -n "$wallet" ]; then
    first="$(discover_pettable_gotchi_ids "$wallet" 2>/dev/null | head -n1 || true)"
    if [ -n "$first" ]; then
      printf '%s\n' "$first"
      return 0
    fi
  fi

  load_config
  [ "${#GOTCHI_IDS[@]}" -gt 0 ] || err "No gotchiIds configured in $CONFIG_FILE"
  printf '%s\n' "${GOTCHI_IDS[0]}"
}

is_uint() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

is_eth_address() {
  [[ "$1" =~ ^0x[0-9a-fA-F]{40}$ ]]
}

to_lower() {
  printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]'
}

format_utc() {
  local ts="$1"
  if date -u -d "@$ts" "+%Y-%m-%d %H:%M UTC" >/dev/null 2>&1; then
    date -u -d "@$ts" "+%Y-%m-%d %H:%M UTC"
    return
  fi
  date -u -r "$ts" "+%Y-%m-%d %H:%M UTC"
}

format_duration() {
  local total="$1"
  if [ "$total" -lt 0 ]; then
    total=0
  fi
  local hours=$((total / 3600))
  local mins=$(((total % 3600) / 60))
  local secs=$((total % 60))
  printf "%dh %dm %ds" "$hours" "$mins" "$secs"
}

join_gotchi_ids() {
  local ids=("$@")
  local out=""
  local id
  for id in "${ids[@]}"; do
    if [ -z "$out" ]; then
      out="#$id"
    else
      out="$out, #$id"
    fi
  done
  printf '%s\n' "$out"
}

encode_interact_calldata() {
  local ids=("$@")
  [ "${#ids[@]}" -gt 0 ] || err "At least one gotchi ID is required"

  local selector="22c67519"
  local offset="0000000000000000000000000000000000000000000000000000000000000020"
  local length
  length="$(printf '%064x' "${#ids[@]}")"

  local payload=""
  local id
  for id in "${ids[@]}"; do
    is_uint "$id" || err "Invalid gotchi ID: $id"
    payload+="$(printf '%064x' "$id")"
  done

  printf '0x%s%s%s%s\n' "$selector" "$offset" "$length" "$payload"
}

resolve_bankr_api_key() {
  local key="${BANKR_API_KEY:-}"

  if [ -z "$key" ] && command -v systemctl >/dev/null 2>&1; then
    key="$(systemctl --user show-environment 2>/dev/null | sed -n 's/^BANKR_API_KEY=//p' | head -n1 || true)"
  fi

  if [ -z "$key" ] && [ -f "$HOME/.openclaw/skills/bankr/config.json" ]; then
    key="$(jq -r '.apiKey // empty' "$HOME/.openclaw/skills/bankr/config.json" 2>/dev/null || true)"
  fi

  if [ -z "$key" ] && [ -f "$HOME/.openclaw/workspace/skills/bankr/config.json" ]; then
    key="$(jq -r '.apiKey // empty' "$HOME/.openclaw/workspace/skills/bankr/config.json" 2>/dev/null || true)"
  fi

  case "$key" in
    ""|null|"your-api-key-here"|"YOUR_BANKR_API_KEY")
      err "BANKR_API_KEY is missing (env/systemd/bankr config)"
      ;;
  esac

  printf '%s\n' "$key"
}

submit_bankr_tx() {
  local to_addr="$1"
  local calldata="$2"
  local description="$3"
  local api_key
  api_key="$(resolve_bankr_api_key)"

  local payload
  payload="$(jq -n \
    --arg to "$to_addr" \
    --arg chainId "$CHAIN_ID" \
    --arg data "$calldata" \
    --arg description "$description" \
    '{transaction:{to:$to,chainId:($chainId|tonumber),value:"0",data:$data},description:$description,waitForConfirmation:true}')"

  curl -sS -X POST "$BANKR_API_URL/agent/submit" \
    -H "X-API-Key: $api_key" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

bankr_is_success() {
  local response="$1"
  [ "$(printf '%s' "$response" | jq -r '.success // false' 2>/dev/null || echo false)" = "true" ]
}

bankr_tx_hash() {
  local response="$1"
  printf '%s' "$response" | jq -r '.transactionHash // .txHash // .hash // empty' 2>/dev/null || true
}

bankr_error() {
  local response="$1"
  printf '%s' "$response" | jq -r '.error // .message // .details // "Unknown error"' 2>/dev/null || echo "Unknown error"
}

get_bankr_wallet_address() {
  local api_key
  local job_response
  local job_id
  local result
  local status
  local response_text
  local wallet
  local i

  api_key="$(resolve_bankr_api_key)"

  job_response="$(curl -sS -X POST "$BANKR_API_URL/agent/prompt" \
    -H "X-API-Key: $api_key" \
    -H "Content-Type: application/json" \
    -d '{"prompt":"What is my Base wallet address? Respond with only the address."}')"

  job_id="$(printf '%s' "$job_response" | jq -r '.jobId // empty' 2>/dev/null || true)"
  [ -n "$job_id" ] || err "Could not start Bankr wallet lookup"

  for i in $(seq 1 20); do
    result="$(curl -sS "$BANKR_API_URL/agent/job/$job_id" -H "X-API-Key: $api_key" || true)"
    status="$(printf '%s' "$result" | jq -r '.status // "unknown"' 2>/dev/null || echo unknown)"
    if [ "$status" = "completed" ] || [ "$status" = "failed" ] || [ "$status" = "cancelled" ]; then
      break
    fi
    sleep 2
  done

  status="$(printf '%s' "$result" | jq -r '.status // "unknown"' 2>/dev/null || echo unknown)"
  [ "$status" = "completed" ] || err "Bankr wallet lookup failed (status=$status)"

  response_text="$(printf '%s' "$result" | jq -r '.response // .result // .output // empty' 2>/dev/null || true)"
  wallet="$(printf '%s' "$response_text" | grep -Eo '0x[a-fA-F0-9]{40}' | head -n1 || true)"
  [ -n "$wallet" ] || err "Could not parse Bankr wallet address"

  printf '%s\n' "$wallet"
}

resolve_agent_wallet_address() {
  local wallet="${PET_ME_WALLET_ADDRESS:-${BANKR_WALLET_ADDRESS:-}}"

  if [ -z "$wallet" ] && [ -f "$CONFIG_FILE" ]; then
    wallet="$(jq -r '.walletAddress // .wallet // .bankrWallet // empty' "$CONFIG_FILE" 2>/dev/null || true)"
  fi

  if [ -z "$wallet" ] && [ -f "$BANKR_WALLET_CACHE_FILE" ]; then
    local age
    age="$(( $(date +%s) - $(stat -c %Y "$BANKR_WALLET_CACHE_FILE" 2>/dev/null || echo 0) ))"
    if [ "$age" -ge 0 ] && [ "$age" -le "$BANKR_WALLET_CACHE_MAX_AGE" ]; then
      wallet="$(head -n1 "$BANKR_WALLET_CACHE_FILE" | tr -d '[:space:]')"
    fi
  fi

  if [ -z "$wallet" ]; then
    wallet="$(get_bankr_wallet_address 2>/dev/null || true)"
    if [ -n "$wallet" ]; then
      mkdir -p "$(dirname "$BANKR_WALLET_CACHE_FILE")"
      printf '%s\n' "$wallet" > "$BANKR_WALLET_CACHE_FILE"
    fi
  fi

  if ! is_eth_address "$wallet"; then
    return 1
  fi

  printf '%s\n' "$(to_lower "$wallet")"
}

discover_owned_gotchi_ids() {
  local wallet="$1"
  local out

  is_eth_address "$wallet" || err "Invalid wallet address for owner discovery: $wallet"

  out="$("$CAST_BIN" call "$CONTRACT_ADDRESS" 'tokenIdsOfOwner(address)(uint32[])' "$wallet" --rpc-url "$RPC_URL" --json 2>/dev/null || true)"
  [ -n "$out" ] || return 0

  printf '%s' "$out" | jq -r '.[0][]? | tostring' 2>/dev/null | sed '/^$/d' || true
}

discover_delegated_gotchi_ids() {
  local wallet="$1"
  local wallet_lower
  local payload
  local resp

  is_eth_address "$wallet" || err "Invalid wallet address for delegated discovery: $wallet"
  wallet_lower="$(to_lower "$wallet")"

  payload="$(jq -n --arg wallet "$wallet_lower" '{query:"query($wallet:Bytes!){ gotchiLendings(first:1000, where:{or:[{borrower:$wallet, cancelled:false, completed:false, timeAgreed_gt:\"0\"},{thirdPartyAddress:$wallet, cancelled:false, completed:false, timeAgreed_gt:\"0\"}]}){ gotchiTokenId } }",variables:{wallet:$wallet}}')"

  resp="$(curl -sS "$CORE_SUBGRAPH_URL" -H 'content-type: application/json' -d "$payload" 2>/dev/null || true)"
  [ -n "$resp" ] || return 0

  if printf '%s' "$resp" | jq -e '.errors' >/dev/null 2>&1; then
    warn "Delegated gotchi query returned errors from core subgraph"
    return 0
  fi

  printf '%s' "$resp" | jq -r '.data.gotchiLendings[]?.gotchiTokenId // empty' 2>/dev/null | sed '/^$/d' || true
}

discover_pettable_gotchi_ids() {
  local wallet="${1:-}"
  local -a owned_ids=()
  local -a delegated_ids=()
  local -a config_ids=()

  load_config

  if [ -z "$wallet" ]; then
    wallet="$(resolve_agent_wallet_address 2>/dev/null || true)"
  fi

  [ -n "$wallet" ] || err "Could not resolve agent wallet address (set PET_ME_WALLET_ADDRESS or config.walletAddress)"

  mapfile -t owned_ids < <(discover_owned_gotchi_ids "$wallet")
  mapfile -t delegated_ids < <(discover_delegated_gotchi_ids "$wallet")
  config_ids=("${GOTCHI_IDS[@]}")

  printf '%s\n' "${owned_ids[@]}" "${delegated_ids[@]}" "${config_ids[@]}" | awk '/^[0-9]+$/{if(!seen[$1]++) print $1}'
}

resolve_reminder_chat_id() {
  local chat_id="${PET_ME_TELEGRAM_CHAT_ID:-${TELEGRAM_CHAT_ID:-}}"

  if [ -z "$chat_id" ] && [ -f "$CONFIG_FILE" ]; then
    chat_id="$(jq -r '.reminder.telegramChatId // .telegramChatId // empty' "$CONFIG_FILE" 2>/dev/null || true)"
  fi

  case "$chat_id" in
    ""|null)
      return 1
      ;;
  esac

  printf '%s\n' "$chat_id"
}

resolve_telegram_bot_token() {
  local token="${TELEGRAM_BOT_TOKEN:-}"

  if [ -z "$token" ] && command -v systemctl >/dev/null 2>&1; then
    token="$(systemctl --user show-environment 2>/dev/null | sed -n 's/^TELEGRAM_BOT_TOKEN=//p' | head -n1 || true)"
  fi

  if [ -z "$token" ] && [ -f "$HOME/.openclaw/openclaw.json" ]; then
    token="$(jq -r '.. | .botToken? // empty' "$HOME/.openclaw/openclaw.json" 2>/dev/null | head -n1 || true)"
  fi

  case "$token" in
    ""|null)
      return 1
      ;;
  esac

  printf '%s\n' "$token"
}

send_telegram_message() {
  local chat_id="$1"
  local message="$2"

  local token
  token="$(resolve_telegram_bot_token || true)"
  [ -n "$token" ] || return 1

  local response
  response="$(curl -sS -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    --data-urlencode "chat_id=${chat_id}" \
    --data-urlencode "text=${message}" \
    --data-urlencode "disable_web_page_preview=true" \
    --data-urlencode "disable_notification=false" 2>/dev/null || true)"

  [ "$(printf '%s' "$response" | jq -r '.ok // false' 2>/dev/null || echo false)" = "true" ]
}

is_daily_reminder_enabled() {
  local raw
  raw="$(jq -r '.dailyReminder // .reminder.enabled // true' "$CONFIG_FILE" 2>/dev/null || echo true)"
  raw="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"

  case "$raw" in
    false|0|no|off)
      return 1
      ;;
    *)
      return 0
      ;;
  esac
}

resolve_fallback_delay_hours() {
  local raw="${PET_ME_FALLBACK_DELAY_HOURS:-}"
  if [ -z "$raw" ]; then
    raw="$(jq -r '.fallbackDelayHours // .reminder.fallbackDelayHours // 1' "$CONFIG_FILE" 2>/dev/null || echo 1)"
  fi

  raw="${raw%%.*}"
  if ! is_uint "$raw" || [ "$raw" -le 0 ]; then
    raw="1"
  fi

  printf '%s\n' "$raw"
}
