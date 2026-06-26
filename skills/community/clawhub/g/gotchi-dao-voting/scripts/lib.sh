#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${GOTCHI_DAO_CONFIG_FILE:-$SCRIPT_DIR/../config.json}"

err() {
  echo "ERROR: $*" >&2
  exit 1
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || err "Missing required binary: $bin"
}

require_tools() {
  require_bin curl
  require_bin jq
}

normalize_wallet() {
  local wallet="$1"
  [[ "$wallet" =~ ^0x[0-9a-fA-F]{40}$ ]] || err "Invalid wallet address: $wallet"
  printf '%s\n' "$wallet"
}

normalize_proposal_id() {
  local proposal_id="$1"
  [[ "$proposal_id" =~ ^0x[0-9a-fA-F]{64}$ ]] || err "Invalid proposal ID: $proposal_id"
  printf '%s\n' "$proposal_id"
}

load_config() {
  [ -f "$CONFIG_FILE" ] || err "Config file not found: $CONFIG_FILE"

  WALLET="$(jq -r '.wallet // empty' "$CONFIG_FILE")"
  SPACE="$(jq -r '.space // empty' "$CONFIG_FILE")"
  SNAPSHOT_API="$(jq -r '.snapshotApiUrl // empty' "$CONFIG_FILE")"
  SEQUENCER="$(jq -r '.snapshotSequencer // empty' "$CONFIG_FILE")"

  [ -n "$WALLET" ] || err "Missing config.wallet"
  [ -n "$SPACE" ] || err "Missing config.space"
  [ -n "$SNAPSHOT_API" ] || err "Missing config.snapshotApiUrl"
  [ -n "$SEQUENCER" ] || err "Missing config.snapshotSequencer"

  normalize_wallet "$WALLET" >/dev/null
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

snapshot_query() {
  local query="$1"
  local variables_json="${2-}"
  local payload

  if [ -z "$variables_json" ]; then
    variables_json='{}'
  fi

  printf '%s' "$variables_json" | jq -e . >/dev/null 2>&1 || err "Invalid Snapshot variables JSON"

  payload="$(jq -n --arg query "$query" --argjson variables "$variables_json" '{query:$query,variables:$variables}')" || err "Failed to build Snapshot query payload"

  curl -sS -X POST "$SNAPSHOT_API" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

snapshot_has_errors() {
  local response="$1"
  printf '%s' "$response" | jq -e '.errors and (.errors | length > 0)' >/dev/null 2>&1
}

format_utc() {
  local ts="$1"
  date -u -d "@$ts" '+%Y-%m-%d %H:%M UTC' 2>/dev/null || echo "Unknown"
}
