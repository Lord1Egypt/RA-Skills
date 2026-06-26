#!/usr/bin/env bash

SUBGRAPH_URL="https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn"

die() {
  echo "ERROR: $*" >&2
  exit 1
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || die "Missing required binary: $bin"
}

validate_gotchi_id() {
  local gotchi_id="$1"
  [[ "$gotchi_id" =~ ^[0-9]+$ ]] || die "Invalid gotchi ID: $gotchi_id"
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

  [ -n "$key" ] || die "BANKR_API_KEY missing (env/systemd/bankr config)"
  printf '%s\n' "$key"
}

fetch_gotchi_subgraph_json() {
  local gotchi_id="$1"
  local payload response

  require_bin curl
  require_bin jq
  validate_gotchi_id "$gotchi_id"

  payload="$(jq -n --arg id "$gotchi_id" '{
    query: "query($id: String!) { aavegotchi(id: $id) { id name equippedWearables } }",
    variables: { id: $id }
  }')"

  response="$(curl -sS "$SUBGRAPH_URL" -H 'content-type: application/json' --data "$payload")"

  if ! echo "$response" | jq -e . >/dev/null 2>&1; then
    die "Subgraph returned non-JSON response"
  fi

  if echo "$response" | jq -e '.errors and (.errors | length > 0)' >/dev/null 2>&1; then
    echo "$response" | jq '.errors' >&2
    die "Subgraph query returned errors"
  fi

  local gotchi_json
  gotchi_json="$(echo "$response" | jq -c '.data.aavegotchi // null')"

  [ "$gotchi_json" != "null" ] || die "Gotchi #$gotchi_id not found"

  printf '%s\n' "$gotchi_json"
}

fetch_current_wearables() {
  local gotchi_id="$1"
  local gotchi_json wearables

  gotchi_json="$(fetch_gotchi_subgraph_json "$gotchi_id")"

  wearables="$(echo "$gotchi_json" | jq -c '(.equippedWearables // []) as $w | ($w + [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])[0:16]')"

  if ! echo "$wearables" | jq -e 'type == "array" and length == 16 and all(.[]; (type == "number") and (. >= 0) and (. <= 65535))' >/dev/null 2>&1; then
    die "Invalid equippedWearables shape from subgraph"
  fi

  printf '%s\n' "$wearables"
}
