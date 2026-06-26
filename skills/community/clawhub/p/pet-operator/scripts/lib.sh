#!/usr/bin/env bash

set -euo pipefail

AAVEGOTCHI_DIAMOND="${AAVEGOTCHI_DIAMOND:-0xA99c4B08201F2913Db8D28e71d020c4298F29dBF}"
AAI_OPERATOR="${AAI_OPERATOR:-0xb96B48a6B190A9d509cE9312654F34E9770F2110}"
BASE_RPC_URL="${BASE_RPC_URL:-https://mainnet.base.org}"
PET_ME_CONFIG_FILE="${PET_ME_CONFIG_FILE:-$HOME/.openclaw/workspace/skills/pet-me-master/config.json}"

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
  require_bin cast
  require_bin jq
}

is_eth_address() {
  [[ "$1" =~ ^0x[0-9a-fA-F]{40}$ ]]
}

normalize_wallet() {
  local wallet="$1"
  is_eth_address "$wallet" || err "Invalid wallet address: $wallet"
  printf '%s\n' "$wallet"
}

to_lower() {
  printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]'
}

set_pet_operator_calldata() {
  local approved="$1"

  case "$approved" in
    true|false)
      ;;
    *)
      err "approved must be true|false"
      ;;
  esac

  if command -v cast >/dev/null 2>&1; then
    local data
    data="$(cast calldata "setPetOperatorForAll(address,bool)" "$AAI_OPERATOR" "$approved" 2>/dev/null || true)"
    if [[ -n "$data" && "$data" == 0x* ]]; then
      printf '%s\n' "$data"
      return 0
    fi
  fi

  if [[ "$approved" == "true" ]]; then
    printf '%s\n' "0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000001"
  else
    printf '%s\n' "0xcd675d57000000000000000000000000b96b48a6b190a9d509ce9312654f34e9770f21100000000000000000000000000000000000000000000000000000000000000000"
  fi
}

check_pet_operator_approved() {
  local wallet="$1"
  local out
  local norm

  wallet="$(normalize_wallet "$wallet")"

  out="$(cast call "$AAVEGOTCHI_DIAMOND" "isPetOperatorForAll(address,address)(bool)" "$wallet" "$AAI_OPERATOR" --rpc-url "$BASE_RPC_URL" 2>/dev/null || true)"
  if [ -z "$out" ]; then
    out="$(cast call "$AAVEGOTCHI_DIAMOND" "isPetOperatorForAll(address,address)" "$wallet" "$AAI_OPERATOR" --rpc-url "$BASE_RPC_URL" 2>/dev/null || true)"
  fi

  norm="$(printf '%s' "$out" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"

  case "$norm" in
    true|0x1|0x01|0x0000000000000000000000000000000000000000000000000000000000000001)
      return 0
      ;;
    false|0x0|0x00|0x0000000000000000000000000000000000000000000000000000000000000000)
      return 1
      ;;
    *)
      warn "Unexpected isPetOperatorForAll response: ${out:-<empty>}"
      return 1
      ;;
  esac
}

fetch_wallet_gotchi_ids() {
  local wallet="$1"
  local out

  wallet="$(normalize_wallet "$wallet")"

  out="$(cast call "$AAVEGOTCHI_DIAMOND" "tokenIdsOfOwner(address)(uint32[])" "$wallet" --rpc-url "$BASE_RPC_URL" --json 2>/dev/null || true)"
  if [ -n "$out" ]; then
    printf '%s' "$out" | jq -r '.[0][]? | tostring' 2>/dev/null | sed '/^$/d' || true
    return 0
  fi

  local balance_hex
  local count
  balance_hex="$(cast call "$AAVEGOTCHI_DIAMOND" "balanceOf(address)(uint256)" "$wallet" --rpc-url "$BASE_RPC_URL" 2>/dev/null || true)"
  [ -n "$balance_hex" ] || return 0
  count=$((16#${balance_hex#0x}))

  local i token_hex
  for ((i=0; i<count; i++)); do
    token_hex="$(cast call "$AAVEGOTCHI_DIAMOND" "tokenOfOwnerByIndex(address,uint256)(uint256)" "$wallet" "$i" --rpc-url "$BASE_RPC_URL" 2>/dev/null || true)"
    [ -n "$token_hex" ] || continue
    printf '%s\n' "$((16#${token_hex#0x}))"
  done
}
