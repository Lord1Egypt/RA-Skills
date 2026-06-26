#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${GOTCHI_CHANNELING_CONFIG_FILE:-$SCRIPT_DIR/../config.json}"

DEFAULT_REALM_DIAMOND="0x4B0040c3646D3c44B8a28Ad7055cfCF536c05372"
DEFAULT_RPC_URL="https://mainnet.base.org"
DEFAULT_CHAIN_ID="8453"

err() {
  echo "ERROR: $*" >&2
  exit 1
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || err "Missing required binary: $bin"
}

require_numeric() {
  local value="$1"
  local label="$2"
  [[ "$value" =~ ^[0-9]+$ ]] || err "Invalid $label: $value"
}

load_config() {
  [ -f "$CONFIG_FILE" ] || err "Config file not found: $CONFIG_FILE"

  REALM_DIAMOND="$(jq -r '.realmDiamond // empty' "$CONFIG_FILE")"
  RPC_URL="$(jq -r '.rpcUrl // empty' "$CONFIG_FILE")"
  CHAIN_ID="$(jq -r '.chainId // empty' "$CONFIG_FILE")"

  [ -n "$REALM_DIAMOND" ] || REALM_DIAMOND="$DEFAULT_REALM_DIAMOND"
  [ -n "$RPC_URL" ] || RPC_URL="$DEFAULT_RPC_URL"
  [ -n "$CHAIN_ID" ] || CHAIN_ID="$DEFAULT_CHAIN_ID"

  if [ -n "${BASE_MAINNET_RPC:-}" ]; then
    RPC_URL="$BASE_MAINNET_RPC"
  fi

  [[ "$REALM_DIAMOND" =~ ^0x[0-9a-fA-F]{40}$ ]] || err "Invalid realmDiamond in config"
  require_numeric "$CHAIN_ID" "chainId"
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

  [ -n "$key" ] || err "BANKR_API_KEY missing (env/systemd/bankr config)"
  printf '%s\n' "$key"
}

format_wait() {
  local seconds="$1"
  local hours mins
  hours=$((seconds / 3600))
  mins=$(((seconds % 3600) / 60))
  printf '%sh %sm' "$hours" "$mins"
}
