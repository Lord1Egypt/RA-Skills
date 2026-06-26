#!/usr/bin/env bash

# Shared helpers for gotchi-pocket scripts.

set -euo pipefail

AAVEGOTCHI_DIAMOND="${AAVEGOTCHI_DIAMOND:-0xA99c4B08201F2913Db8D28e71d020c4298F29dBF}"
BASE_RPC_URL="${BASE_MAINNET_RPC:-https://mainnet.base.org}"
BANKR_API_URL="${BANKR_API_URL:-https://api.bankr.bot}"
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

require_bins() {
  local bin
  [ -n "$CAST_BIN" ] || err "Missing required binary: cast (or ~/.foundry/bin/cast)"

  for bin in jq curl python3; do
    command -v "$bin" >/dev/null 2>&1 || err "Missing required binary: $bin"
  done
}

to_lower() {
  printf "%s" "$1" | tr "[:upper:]" "[:lower:]"
}

is_valid_address() {
  [[ "$1" =~ ^0x[0-9a-fA-F]{40}$ ]]
}

resolve_token_address() {
  local token="${1:-}"
  [ -n "$token" ] || err "Token is required"

  case "$(to_lower "$token")" in
    ghst)
      echo "0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB"
      ;;
    fud)
      echo "0x2028b4043e6722ea164946c82fe806c4a43a0ff4"
      ;;
    fomo)
      echo "0xa32137bfb57d2b6a9fd2956ba4b54741a6d54b58"
      ;;
    alpha)
      echo "0x15e7cac885e3730ce6389447bc0f7ac032f31947"
      ;;
    kek)
      echo "0xe52b9170ff4ece4c35e796ffd74b57dec68ca0e5"
      ;;
    usdc)
      echo "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
      ;;
    weth)
      echo "0x4200000000000000000000000000000000000006"
      ;;
    dai)
      echo "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"
      ;;
    0x*)
      is_valid_address "$token" || err "Invalid token address: $token"
      echo "$token"
      ;;
    *)
      err "Unsupported token alias: $token"
      ;;
  esac
}

resolve_bankr_api_key() {
  local key="${BANKR_API_KEY:-}"

  if [ -z "$key" ] && command -v systemctl >/dev/null 2>&1; then
    key="$(systemctl --user show-environment 2>/dev/null | sed -n "s/^BANKR_API_KEY=//p" | head -n1 || true)"
  fi

  if [ -z "$key" ] && [ -f "$HOME/.openclaw/skills/bankr/config.json" ]; then
    key="$(jq -r '.apiKey // empty' "$HOME/.openclaw/skills/bankr/config.json" 2>/dev/null || true)"
  fi

  if [ -z "$key" ] && [ -f "$HOME/.openclaw/workspace/skills/bankr/config.json" ]; then
    key="$(jq -r '.apiKey // empty' "$HOME/.openclaw/workspace/skills/bankr/config.json" 2>/dev/null || true)"
  fi

  [ -n "$key" ] || err "BANKR_API_KEY not found in env, systemd, or Bankr config"
  echo "$key"
}

parse_gotchi_struct() {
  local gotchi_id="$1"
  local raw

  raw="$("$CAST_BIN" call "$AAVEGOTCHI_DIAMOND" "getAavegotchi(uint256)" "$gotchi_id" --rpc-url "$BASE_RPC_URL")" || err "Failed to fetch gotchi struct"

  "$CAST_BIN" decode-abi \
    "getAavegotchi(uint256)((uint256,string,address,uint256,uint256,int16[6],int16[6],uint16[16],address,address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,bool))" \
    "$raw"
}

get_gotchi_owner() {
  local gotchi_id="$1"
  "$CAST_BIN" call "$AAVEGOTCHI_DIAMOND" "ownerOf(uint256)(address)" "$gotchi_id" --rpc-url "$BASE_RPC_URL"
}

get_gotchi_pocket() {
  local gotchi_id="$1"
  local decoded
  local addresses
  local pocket

  decoded="$(parse_gotchi_struct "$gotchi_id")"
  addresses="$(printf "%s\n" "$decoded" | grep -oE '0x[0-9a-fA-F]{40}' || true)"
  pocket="$(printf "%s\n" "$addresses" | sed -n '3p')"

  [ -n "$pocket" ] || err "Unable to resolve pocket address for gotchi #$gotchi_id"
  echo "$pocket"
}

get_token_decimals() {
  local token_address="$1"
  "$CAST_BIN" call "$token_address" "decimals()(uint8)" --rpc-url "$BASE_RPC_URL" 2>/dev/null || err "Unable to read token decimals"
}

get_token_symbol() {
  local token_address="$1"
  local symbol

  symbol="$("$CAST_BIN" call "$token_address" "symbol()(string)" --rpc-url "$BASE_RPC_URL" 2>/dev/null || true)"
  symbol="${symbol//\"/}"

  if [ -z "$symbol" ]; then
    symbol="TOKEN"
  fi

  echo "$symbol"
}

balance_of_raw() {
  local token_address="$1"
  local wallet_address="$2"
  "$CAST_BIN" call "$token_address" "balanceOf(address)(uint256)" "$wallet_address" --rpc-url "$BASE_RPC_URL" | awk '{print $1}'
}

amount_to_raw() {
  local amount="$1"
  local decimals="$2"

  python3 - "$amount" "$decimals" <<'PY'
from decimal import Decimal, InvalidOperation, ROUND_DOWN, getcontext
import sys

amount = sys.argv[1].strip()
decimals = int(sys.argv[2])

if decimals < 0 or decimals > 36:
    raise SystemExit("Invalid decimals")

getcontext().prec = 100

try:
    value = Decimal(amount)
except InvalidOperation:
    raise SystemExit("Invalid amount")

if value < 0:
    raise SystemExit("Amount cannot be negative")

scaled = (value * (Decimal(10) ** decimals)).to_integral_value(rounding=ROUND_DOWN)
print(int(scaled))
PY
}

raw_to_units() {
  local raw="$1"
  local decimals="$2"

  python3 - "$raw" "$decimals" <<'PY'
from decimal import Decimal, getcontext
import sys

raw = Decimal(sys.argv[1])
decimals = int(sys.argv[2])

getcontext().prec = 100
units = raw / (Decimal(10) ** decimals)

if units == units.to_integral():
    print(int(units))
else:
    print(format(units.normalize(), "f"))
PY
}

is_less_than_bigint() {
  local left="${1#0}"
  local right="${2#0}"

  [ -n "$left" ] || left="0"
  [ -n "$right" ] || right="0"

  if [ ${#left} -lt ${#right} ]; then
    return 0
  fi

  if [ ${#left} -gt ${#right} ]; then
    return 1
  fi

  [[ "$left" < "$right" ]]
}

submit_bankr_tx() {
  local to_address="$1"
  local calldata="$2"
  local description="$3"
  local api_key
  local payload

  api_key="$(resolve_bankr_api_key)"

  payload="$(jq -n \
    --arg to "$to_address" \
    --arg data "$calldata" \
    --arg description "$description" \
    '{transaction:{to:$to,chainId:8453,value:"0",data:$data},description:$description,waitForConfirmation:true}')"

  curl -s -X POST "$BANKR_API_URL/agent/submit" \
    -H "X-API-Key: $api_key" \
    -H "Content-Type: application/json" \
    -d "$payload"
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

  job_response="$(curl -s -X POST "$BANKR_API_URL/agent/prompt" \
    -H "X-API-Key: $api_key" \
    -H "Content-Type: application/json" \
    -d '{"prompt":"What is my Base wallet address?"}')"

  job_id="$(printf "%s" "$job_response" | jq -r '.jobId // empty')"
  [ -n "$job_id" ] || err "Could not start Bankr wallet lookup"

  for i in $(seq 1 20); do
    result="$(curl -s "$BANKR_API_URL/agent/job/$job_id" -H "X-API-Key: $api_key")"
    status="$(printf "%s" "$result" | jq -r '.status // "unknown"')"
    if [ "$status" = "completed" ] || [ "$status" = "failed" ] || [ "$status" = "cancelled" ]; then
      break
    fi
    sleep 2
  done

  status="$(printf "%s" "$result" | jq -r '.status // "unknown"')"
  [ "$status" = "completed" ] || err "Bankr wallet lookup failed (status=$status)"

  response_text="$(printf "%s" "$result" | jq -r '.response // .result // .output // empty')"
  wallet="$(printf "%s" "$response_text" | grep -Eo '0x[a-fA-F0-9]{40}' | head -n1 || true)"

  [ -n "$wallet" ] || err "Could not parse Bankr wallet address"
  echo "$wallet"
}

ensure_bankr_controls_gotchi() {
  local gotchi_id="$1"
  local owner
  local bankr_wallet

  if [ "${SKIP_BANKR_OWNER_CHECK:-0}" = "1" ]; then
    return
  fi

  owner="$(get_gotchi_owner "$gotchi_id")"
  bankr_wallet="$(get_bankr_wallet_address)"

  if [ "$(to_lower "$owner")" != "$(to_lower "$bankr_wallet")" ]; then
    err "Bankr wallet $bankr_wallet does not own gotchi #$gotchi_id (owner: $owner)"
  fi
}
