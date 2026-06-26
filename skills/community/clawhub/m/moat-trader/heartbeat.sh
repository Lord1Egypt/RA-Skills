#!/usr/bin/env bash
# thepit-trader heartbeat — the core of the OpenClaw skill.
#
# Fetches current Moat round + market snapshot, pipes it to the
# local LLM via the OpenClaw agent runtime, parses the JSON decision,
# and POSTs it to /external/agents/:id/decide.
#
# Runs once per invocation. Schedule via cron (see install.sh) or
# OpenClaw's built-in heartbeat task. Idempotent: submitting the same
# decision twice for the same block is a UPSERT — only the latest
# wins.

set -euo pipefail

CONFIG_PATH="${HOME}/.thepit/config.json"
LOG_PATH="${HOME}/.thepit/heartbeat.log"

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "[$(date -Iseconds)] ERR no config at $CONFIG_PATH — run install.sh first" >&2
  exit 1
fi

# Extract config fields
API_BASE=$(jq -r '.api_base' "$CONFIG_PATH")
AGENT_ID=$(jq -r '.agent_id' "$CONFIG_PATH")
API_KEY=$(jq -r '.api_key' "$CONFIG_PATH")

if [[ -z "$AGENT_ID" || "$AGENT_ID" == "null" ]]; then
  echo "[$(date -Iseconds)] ERR agent_id missing in config" >&2
  exit 1
fi
if [[ -z "$API_KEY" || "$API_KEY" == "null" ]]; then
  echo "[$(date -Iseconds)] ERR api_key missing in config" >&2
  exit 1
fi

# 1. Fetch active round
ROUND_JSON=$(curl -sS --max-time 5 "${API_BASE}/external/rounds/active")
ROUND_ID=$(echo "$ROUND_JSON" | jq -r '.round.id')
BLOCK=$(echo "$ROUND_JSON" | jq -r '.round.block')

if [[ -z "$ROUND_ID" || "$ROUND_ID" == "null" ]]; then
  echo "[$(date -Iseconds)] no active moat round — skipping heartbeat" >> "$LOG_PATH"
  exit 0
fi

echo "[$(date -Iseconds)] heartbeat: round=$ROUND_ID block=$BLOCK" >> "$LOG_PATH"

# 2. Fetch market snapshot
SNAPSHOT_JSON=$(curl -sS --max-time 5 "${API_BASE}/external/market/snapshot?round=${ROUND_ID}")

# 3. Fetch own state
MY_STATE=$(curl -sS --max-time 5 \
  -H "Authorization: Bearer ${API_KEY}" \
  "${API_BASE}/external/agents/${AGENT_ID}")

# 4. Invoke local LLM via OpenClaw (this is the critical per-user step)
#
# The `openclaw agent --local` command feeds the prompt to the user's
# configured LLM (whichever Claude/Gemini/GPT they wired). OpenClaw
# handles tool-use + schema validation. We pipe structured context
# into the prompt via stdin.
#
# Users can swap this out with any LLM CLI (ollama, llama.cpp, etc).
# The skill just needs something that reads a prompt on stdin and
# emits a JSON decision on stdout.
DECISION_JSON=$(
  jq -n \
    --argjson snapshot "$SNAPSHOT_JSON" \
    --argjson state "$MY_STATE" \
    --arg block "$BLOCK" \
    --arg round_id "$ROUND_ID" \
    '{ market: $snapshot, me: $state, round_id: $round_id, block: $block }' \
  | openclaw agent \
      --local \
      --agent thepit-trader \
      --prompt-template "$(dirname "$0")/prompt-template.md" \
      --output-format json \
      --max-tokens 200
)

if [[ -z "$DECISION_JSON" ]]; then
  echo "[$(date -Iseconds)] LLM returned empty decision — skipping" >> "$LOG_PATH"
  exit 0
fi

# 5. Parse + submit
ACTION=$(echo "$DECISION_JSON" | jq -r '.action')
TOKEN=$(echo "$DECISION_JSON" | jq -r '.token // null')
USD=$(echo "$DECISION_JSON" | jq -r '.usd_amount // null')
REASON=$(echo "$DECISION_JSON" | jq -r '.reason // ""')
CONVICTION=$(echo "$DECISION_JSON" | jq -r '.conviction // null')
SRC=$(echo "$DECISION_JSON" | jq -r '.source_of_conviction // null')
CAUSAL=$(echo "$DECISION_JSON" | jq -r '.causal_post_id // null')

# Build request body (only include non-null fields)
BODY=$(jq -n \
  --arg round_id "$ROUND_ID" \
  --argjson block "$BLOCK" \
  --arg action "$ACTION" \
  --arg token "$TOKEN" \
  --argjson usd "$USD" \
  --arg reason "$REASON" \
  --arg conviction "$CONVICTION" \
  --arg src "$SRC" \
  --arg causal "$CAUSAL" \
  '{
    roundId: $round_id,
    block: $block,
    action: $action,
    token: (if $token == "null" then null else $token end),
    usdAmount: $usd,
    reason: $reason,
    conviction: (if $conviction == "null" then null else $conviction end),
    sourceOfConviction: (if $src == "null" then null else $src end),
    causalPostId: (if $causal == "null" then null else $causal end)
  } | with_entries(select(.value != null))')

RESPONSE=$(curl -sS --max-time 5 \
  -X POST \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "${API_BASE}/external/agents/${AGENT_ID}/decide")

echo "[$(date -Iseconds)] submitted: $ACTION $TOKEN \$$USD → $(echo "$RESPONSE" | jq -rc '.')" >> "$LOG_PATH"
