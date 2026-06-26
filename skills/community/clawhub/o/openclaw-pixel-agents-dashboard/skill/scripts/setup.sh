#!/usr/bin/env bash
# pixel-agents auto-config — discovers the local OpenClaw environment
# and generates dashboard.config.json for zero-config setup.
#
# Usage: bash setup.sh [--port PORT] [--gateway-url URL]
#
# Discovers:
#   - Agent directories in ~/.openclaw/agents/
#   - Gateway port from openclaw.json or running process
#   - Active sessions per agent
#
# Generates dashboard.config.json in the project root.

set -euo pipefail

# ── Defaults ────────────────────────────────────────────────

PORT="${PIXEL_AGENTS_PORT:-5070}"
GATEWAY_URL=""
AGENTS_DIR=""
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# ── Parse args ──────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --gateway-url) GATEWAY_URL="$2"; shift 2 ;;
    --agents-dir) AGENTS_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ── Discovery ───────────────────────────────────────────────

echo "🔍 Discovering OpenClaw environment..."

# Find agents directory
if [[ -z "$AGENTS_DIR" ]]; then
  if [[ -d "$HOME/.openclaw/agents" ]]; then
    AGENTS_DIR="$HOME/.openclaw/agents"
  else
    echo "   ⚠ No agents directory found at ~/.openclaw/agents/"
    echo "   Set --agents-dir or create the directory first."
    AGENTS_DIR="~/.openclaw/agents"
  fi
fi
echo "   Agents dir: $AGENTS_DIR"

# Discover gateway URL
if [[ -z "$GATEWAY_URL" ]]; then
  # Try openclaw.json
  OC_CONFIG="$HOME/.openclaw/openclaw.json"
  if [[ -f "$OC_CONFIG" ]]; then
    GW_PORT=$(python3 -c "
import json
try:
    c = json.load(open('$OC_CONFIG'))
    print(c.get('gateway',{}).get('port', 18789))
except:
    print(18789)
" 2>/dev/null || echo "18789")
    GATEWAY_URL="http://localhost:$GW_PORT"
  else
    GATEWAY_URL="http://localhost:18789"
  fi
fi
echo "   Gateway: $GATEWAY_URL"

# Check gateway reachability
if curl -s --connect-timeout 3 "$GATEWAY_URL/v1/models" >/dev/null 2>&1; then
  echo "   ✓ Gateway reachable"
  GW_OK=true
else
  echo "   ✗ Gateway not reachable (will still generate config)"
  GW_OK=false
fi

# Discover agents
echo ""
echo "🤖 Discovering agents..."

AGENTS_JSON="["
FIRST=true
PALETTE=0
EMOJIS=("🤖" "🔧" "🔍" "🔩" "☀️" "🧪")
EMOJI_IDX=0

if [[ -d "$AGENTS_DIR" ]]; then
  for agent_dir in "$AGENTS_DIR"/*/; do
    [[ -d "$agent_dir" ]] || continue
    agent_id=$(basename "$agent_dir")

    # Count active sessions
    sessions_dir="$agent_dir/sessions"
    session_count=0
    if [[ -d "$sessions_dir" ]]; then
      session_count=$(find "$sessions_dir" -name "*.jsonl" -mmin -60 2>/dev/null | wc -l)
    fi

    # Capitalize name
    agent_name="$(echo "${agent_id:0:1}" | tr '[:lower:]' '[:upper:]')${agent_id:1}"

    # First agent is always-present (usually 'main')
    always_present="false"
    if [[ "$agent_id" == "main" ]]; then
      always_present="true"
    fi

    emoji="${EMOJIS[$EMOJI_IDX % ${#EMOJIS[@]}]}"

    if [[ "$FIRST" == "true" ]]; then
      FIRST=false
    else
      AGENTS_JSON+=","
    fi

    AGENTS_JSON+="
    {
      \"id\": \"$agent_id\",
      \"name\": \"$agent_name\",
      \"emoji\": \"$emoji\",
      \"palette\": $PALETTE,
      \"alwaysPresent\": $always_present
    }"

    status=""
    if [[ $session_count -gt 0 ]]; then
      status=" ($session_count active sessions)"
    fi
    echo "   ${emoji} ${agent_name} (${agent_id})${status}"

    PALETTE=$(( (PALETTE + 1) % 6 ))
    EMOJI_IDX=$((EMOJI_IDX + 1))
  done
fi

AGENTS_JSON+="
  ]"

if [[ "$FIRST" == "true" ]]; then
  echo "   ⚠ No agents found. Add them manually to the config."
  AGENTS_JSON='[
    {
      "id": "main",
      "name": "Main",
      "emoji": "🤖",
      "palette": 0,
      "alwaysPresent": true
    }
  ]'
fi

# ── Generate Config ─────────────────────────────────────────

CONFIG_PATH="$PROJECT_DIR/dashboard.config.json"

echo ""
echo "📝 Generating config..."

cat > "$CONFIG_PATH" <<EOF
{
  "server": {
    "port": $PORT
  },
  "gateway": {
    "url": "$GATEWAY_URL",
    "token": "\${OPENCLAW_GATEWAY_TOKEN}"
  },
  "openclaw": {
    "agentsDir": "$AGENTS_DIR"
  },
  "agents": $AGENTS_JSON,
  "spawnable": [],
  "remoteAgents": [],
  "features": {
    "fireAlarm": true,
    "breakerPanel": true,
    "hamRadio": true,
    "serverRack": true,
    "nickDesk": false,
    "dayNightCycle": true,
    "conversationHeat": true,
    "channelBadges": true,
    "sounds": true,
    "door": true
  }
}
EOF

echo "   ✓ Written to $CONFIG_PATH"

# ── Install + Build ─────────────────────────────────────────

echo ""
echo "📦 Installing dependencies..."
cd "$PROJECT_DIR"

if [[ ! -d "node_modules" ]]; then
  npm install --silent 2>&1 | tail -1
  echo "   ✓ Dependencies installed"
else
  echo "   ✓ Dependencies already installed"
fi

echo ""
echo "🔨 Building..."
npm run build 2>&1 | tail -1
echo "   ✓ Build complete"

# ── Done ────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎮 Pixel Agents Dashboard ready!"
echo ""
echo "   Start:  cd $PROJECT_DIR && npm start"
echo "   URL:    http://localhost:$PORT"
echo ""
echo "   Edit config: $CONFIG_PATH"
echo "   Example:     $PROJECT_DIR/dashboard.config.example.json"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
