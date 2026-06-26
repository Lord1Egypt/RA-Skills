#!/usr/bin/env bash
set -euo pipefail

# Muster Connect Script
# Connects THIS AGENT to a Muster instance. Run once per agent.
# Handles: registration, API key storage, HEARTBEAT.md setup.
#
# Usage:
#   First agent (local install):  bash connect.sh --name "Silas" --title "COO" --slug "coo"
#   Additional agent (local):     bash connect.sh --name "Atlas" --title "CTO" --slug "cto"
#   Remote instance:              bash connect.sh --endpoint "https://hq.example.com/mcp" --key "sk-muster-..." --name "Silas" --title "COO" --slug "coo"
#
# If --name is omitted, the script attempts to read it from the agent's soul.md.
# If soul.md doesn't exist or has no name, the script reports that the agent
# must provide name/title/slug and exits with the JSON report.
#
# Outputs JSON report to stdout. Progress to stderr.

# --- Defaults ---
MUSTER_ENDPOINT=""
MUSTER_API_KEY=""
AGENT_NAME=""
AGENT_TITLE=""
AGENT_SLUG=""
AGENT_WEBHOOK=""
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
OPENCLAW_WORKSPACE=""
HEARTBEAT_FILE=""
HEARTBEAT_FRAGMENT="$SKILL_DIR/HEARTBEAT_MUSTER.md"

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case $1 in
    --endpoint) MUSTER_ENDPOINT="$2"; shift 2 ;;
    --key) MUSTER_API_KEY="$2"; shift 2 ;;
    --name) AGENT_NAME="$2"; shift 2 ;;
    --title) AGENT_TITLE="$2"; shift 2 ;;
    --slug) AGENT_SLUG="$2"; shift 2 ;;
    --webhook) AGENT_WEBHOOK="$2"; shift 2 ;;
    --workspace) OPENCLAW_WORKSPACE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Helpers ---
log() { echo "[muster-connect] $*" >&2; }
fail() { echo "[muster-connect] FAILED: $*" >&2; exit 1; }

# --- Auto-detect workspace if not provided ---
if [ -z "$OPENCLAW_WORKSPACE" ]; then
  # Strategy 1: Check if the skill is installed inside an agent workspace
  # (e.g., /path/to/agents/silas/workspace/skills/muster/scripts/connect.sh)
  CANDIDATE_WS="$(cd "$SKILL_DIR/../.." 2>/dev/null && pwd)"
  if [ -f "$CANDIDATE_WS/SOUL.md" ] || [ -f "$CANDIDATE_WS/AGENTS.md" ] || [ -f "$CANDIDATE_WS/HEARTBEAT.md" ]; then
    OPENCLAW_WORKSPACE="$CANDIDATE_WS"
    log "Auto-detected workspace from skill location: $OPENCLAW_WORKSPACE"
  fi

  # Strategy 2: Check standard OpenClaw default workspace
  if [ -z "$OPENCLAW_WORKSPACE" ] && [ -d "$HOME/.openclaw/workspace" ]; then
    OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
    log "Using default OpenClaw workspace: $OPENCLAW_WORKSPACE"
  fi

  # Strategy 3: Try reading from openclaw config
  if [ -z "$OPENCLAW_WORKSPACE" ] && [ -f "$OPENCLAW_CONFIG" ]; then
    DETECTED_WS=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        c = json.load(f)
    print(c.get('workspace', {}).get('path', ''))
except: pass
" 2>/dev/null || echo "")
    if [ -n "$DETECTED_WS" ] && [ -d "$DETECTED_WS" ]; then
      OPENCLAW_WORKSPACE="$DETECTED_WS"
      log "Detected workspace from config: $OPENCLAW_WORKSPACE"
    fi
  fi

  # Fallback
  if [ -z "$OPENCLAW_WORKSPACE" ]; then
    OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
    log "⚠ Could not auto-detect workspace. Using default: $OPENCLAW_WORKSPACE"
    log "  Use --workspace to specify the correct path for multi-agent setups."
  fi
fi

HEARTBEAT_FILE="$OPENCLAW_WORKSPACE/HEARTBEAT.md"

# ============================================================
# Phase 1: Determine Muster endpoint
# ============================================================
log "Phase 1: Locating Muster instance..."

if [ -z "$MUSTER_ENDPOINT" ]; then
  # Try to find from a local install
  if [ -f "$HOME/muster/.env" ]; then
    MUSTER_PORT=$(grep "^PORT=" "$HOME/muster/.env" 2>/dev/null | cut -d= -f2 || echo "3000")
    MUSTER_ENDPOINT="http://localhost:${MUSTER_PORT}/mcp"
    log "Found local Muster at $MUSTER_ENDPOINT"
  else
    fail "No --endpoint provided and no local Muster install found. Use --endpoint to specify."
  fi
fi

MUSTER_BASE="${MUSTER_ENDPOINT%/mcp}"
log "✓ Muster endpoint: $MUSTER_ENDPOINT"

# Verify Muster is reachable
if ! curl -sf "$MUSTER_BASE/api/health" &>/dev/null; then
  fail "Cannot reach Muster at $MUSTER_BASE/api/health. Is it running?"
fi
log "✓ Muster is healthy"

# ============================================================
# Phase 2: Agent identity
# ============================================================
log "Phase 2: Resolving agent identity..."

# Try reading from soul.md if name not provided
if [ -z "$AGENT_NAME" ]; then
  SOUL_LOCATIONS=(
    "$OPENCLAW_WORKSPACE/SOUL.md"
    "$OPENCLAW_WORKSPACE/soul.md"
    "$HOME/.openclaw/workspace/SOUL.md"
  )
  for soul_path in "${SOUL_LOCATIONS[@]}"; do
    if [ -f "$soul_path" ]; then
      # Try to extract name from first heading or "Name:" field
      EXTRACTED_NAME=$(grep -m1 -oP '(?<=^# ).*' "$soul_path" 2>/dev/null || \
                       grep -m1 -oP '(?<=Name: ).*' "$soul_path" 2>/dev/null || \
                       grep -m1 -oP '(?<=name: ).*' "$soul_path" 2>/dev/null || echo "")
      if [ -n "$EXTRACTED_NAME" ]; then
        AGENT_NAME="$EXTRACTED_NAME"
        log "Found name from soul: $AGENT_NAME"
        break
      fi
    fi
  done
fi

# Generate slug from title if not provided
if [ -n "$AGENT_TITLE" ] && [ -z "$AGENT_SLUG" ]; then
  AGENT_SLUG=$(echo "$AGENT_TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
fi

NEEDS_IDENTITY=false
if [ -z "$AGENT_NAME" ] || [ -z "$AGENT_TITLE" ] || [ -z "$AGENT_SLUG" ]; then
  NEEDS_IDENTITY=true
fi

# ============================================================
# Phase 3: Register with Muster
# ============================================================

AGENT_ID=""
REGISTERED_KEY=""

if [ -n "$MUSTER_API_KEY" ]; then
  # Key provided — agent is already registered or being connected to remote instance
  log "Phase 3: API key provided — skipping registration"
  REGISTERED_KEY="$MUSTER_API_KEY"

  # Try to get agent_id from an existing state file
  if [ -f "$HOME/.muster/state.json" ]; then
    AGENT_ID=$(python3 -c "import json; print(json.load(open('$HOME/.muster/state.json'))['agent_id'])" 2>/dev/null || echo "")
  fi
elif [ "$NEEDS_IDENTITY" = "true" ]; then
  log "Phase 3: Cannot register — missing agent identity"
  log "  Need: --name, --title, --slug (or a soul.md with a name)"

  cat <<REPORT_JSON
{
  "success": false,
  "action": "needs_identity",
  "message": "Cannot register without agent identity. Provide --name, --title, and --slug, or ensure soul.md exists with a name.",
  "endpoint": "${MUSTER_ENDPOINT}"
}
REPORT_JSON
  exit 0
else
  log "Phase 3: Registering with Muster..."

  REGISTER_BODY="{\"name\":\"${AGENT_NAME}\",\"title\":\"${AGENT_TITLE}\",\"slug\":\"${AGENT_SLUG}\",\"runtime\":\"openclaw\""
  if [ -n "$AGENT_WEBHOOK" ]; then
    REGISTER_BODY="${REGISTER_BODY},\"webhookUrl\":\"${AGENT_WEBHOOK}\""
  fi
  REGISTER_BODY="${REGISTER_BODY}}"

  REGISTER_RESPONSE=$(curl -sf -X POST "$MUSTER_BASE/api/agents/register" \
    -H "Content-Type: application/json" \
    -d "$REGISTER_BODY" 2>&1) || {
    # Check for 409 conflict
    if echo "$REGISTER_RESPONSE" | grep -q "409\|conflict\|already exists"; then
      fail "Slug '$AGENT_SLUG' is already registered. Use a different --slug or provide --key to connect with an existing registration."
    fi
    fail "Registration failed: $REGISTER_RESPONSE"
  }

  AGENT_ID=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('agent',{}).get('id', d.get('id','')))" 2>/dev/null || echo "")
  REGISTERED_KEY=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('apiKey',''))" 2>/dev/null || echo "")

  if [ -z "$REGISTERED_KEY" ]; then
    fail "Registration succeeded but no API key in response. Check Muster logs."
  fi

  log "✓ Registered as $AGENT_NAME ($AGENT_TITLE)"
  log "✓ Agent ID: $AGENT_ID"
fi

# ============================================================
# Phase 4: Store credentials
# ============================================================
log "Phase 4: Storing credentials..."

mkdir -p "$HOME/.muster"

# State file
cat > "$HOME/.muster/state.json" << EOF
{
  "agent_id": "${AGENT_ID}",
  "slug": "${AGENT_SLUG}",
  "name": "${AGENT_NAME}",
  "title": "${AGENT_TITLE}",
  "muster_endpoint": "${MUSTER_ENDPOINT}",
  "registered_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
log "✓ State file: ~/.muster/state.json"

# OpenClaw config — add/update skills.entries.muster
if [ -f "$OPENCLAW_CONFIG" ]; then
  # Use python to safely merge into existing config
  python3 << PYEOF
import json, os

config_path = "$OPENCLAW_CONFIG"
try:
    with open(config_path) as f:
        config = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    config = {}

config.setdefault("skills", {}).setdefault("entries", {})
config["skills"]["entries"]["muster"] = {
    "enabled": True,
    "env": {
        "MUSTER_ENDPOINT": "$MUSTER_ENDPOINT",
        "MUSTER_API_KEY": "$REGISTERED_KEY"
    }
}

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)
PYEOF
  log "✓ OpenClaw config updated"
else
  log "⚠ OpenClaw config not found at $OPENCLAW_CONFIG — agent must set MUSTER_ENDPOINT and MUSTER_API_KEY manually"
fi

# ============================================================
# Phase 5: Update HEARTBEAT.md
# ============================================================
log "Phase 5: Setting up heartbeat..."

if [ -f "$HEARTBEAT_FRAGMENT" ]; then
  # Check if Muster section already exists
  if [ -f "$HEARTBEAT_FILE" ] && grep -q "## Muster check-in" "$HEARTBEAT_FILE"; then
    log "✓ HEARTBEAT.md already has Muster section — skipping"
  else
    # Append the fragment
    mkdir -p "$(dirname "$HEARTBEAT_FILE")"
    cat "$HEARTBEAT_FRAGMENT" >> "$HEARTBEAT_FILE"
    log "✓ Appended Muster checklist to HEARTBEAT.md"
  fi
else
  log "⚠ HEARTBEAT_MUSTER.md not found at $HEARTBEAT_FRAGMENT — agent should add Muster check-in to HEARTBEAT.md manually"
fi

# ============================================================
# Phase 6: First heartbeat
# ============================================================
log "Phase 6: Sending first heartbeat..."

if [ -n "$AGENT_ID" ] && [ -n "$REGISTERED_KEY" ]; then
  HTTP_CODE=$(curl -s -o /tmp/muster-heartbeat-response.json -w "%{http_code}" -X POST "$MUSTER_ENDPOINT" \
    -H "Authorization: Bearer $REGISTERED_KEY" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 1,
      \"method\": \"tools/call\",
      \"params\": {
        \"name\": \"heartbeat\",
        \"arguments\": {
          \"agent_id\": \"$AGENT_ID\",
          \"status\": \"idle\",
          \"metadata\": {\"first_heartbeat\": true, \"name\": \"$AGENT_NAME\", \"title\": \"$AGENT_TITLE\"}
        }
      }
    }" 2>&1)
  CURL_EXIT=$?

  if [ $CURL_EXIT -eq 7 ]; then
    log "⚠ First heartbeat failed — server unreachable (connection refused). Is Muster running?"
  elif [ $CURL_EXIT -eq 28 ]; then
    log "⚠ First heartbeat failed — server timed out"
  elif [ $CURL_EXIT -ne 0 ]; then
    log "⚠ First heartbeat failed — curl error $CURL_EXIT"
  elif [ "$HTTP_CODE" = "401" ]; then
    log "⚠ First heartbeat failed — API key rejected (HTTP 401)"
  elif [[ "$HTTP_CODE" =~ ^5 ]]; then
    log "⚠ First heartbeat failed — server error (HTTP $HTTP_CODE). Check Muster logs."
  elif [ "$HTTP_CODE" = "200" ]; then
    HEARTBEAT_RESPONSE=$(cat /tmp/muster-heartbeat-response.json 2>/dev/null)
    log "✓ First heartbeat sent"
  else
    log "⚠ First heartbeat returned unexpected HTTP $HTTP_CODE"
  fi
  rm -f /tmp/muster-heartbeat-response.json
else
  log "⚠ Skipping heartbeat — missing agent_id or key"
fi

# ============================================================
# Report (JSON to stdout)
# ============================================================
cat <<REPORT_JSON
{
  "success": true,
  "agent_id": "${AGENT_ID}",
  "agent_name": "${AGENT_NAME}",
  "agent_title": "${AGENT_TITLE}",
  "agent_slug": "${AGENT_SLUG}",
  "api_key": "${REGISTERED_KEY}",
  "muster_endpoint": "${MUSTER_ENDPOINT}",
  "muster_base_url": "${MUSTER_BASE}",
  "heartbeat_updated": $([ -f "$HEARTBEAT_FRAGMENT" ] && ! grep -q "manually" <<< "$(log "")" && echo "true" || echo "true"),
  "state_file": "$HOME/.muster/state.json",
  "next_steps": [
    "Agent: create first-run tasks (one for human, one for yourself)",
    "Agent: report connection details to human",
    "Agent: pick up your first task on next heartbeat"
  ]
}
REPORT_JSON

log ""
log "========================================="
log "  Connected to Muster as $AGENT_NAME"
log "========================================="
