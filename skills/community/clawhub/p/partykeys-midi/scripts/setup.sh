#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="partykeys_midi"
MCP_NAME="partykeys"

echo "=== PartyKeys MIDI Skill Setup ==="
echo "Skill directory: $SKILL_DIR"
echo ""

# ── 1. Check prerequisites ──────────────────────────────────────────
check_bin() {
  if ! command -v "$1" &>/dev/null; then
    echo "ERROR: '$1' not found. Please install it first."
    exit 1
  fi
}

check_bin python3

echo "[✓] Prerequisites: python3"

# ── 2. Copy MCP server source if not present ────────────────────────
SERVER_DIR="$SKILL_DIR/server"

if [ ! -f "$SERVER_DIR/mcp_server.py" ]; then
  REPO_SERVER="$(cd "$SKILL_DIR/../../partykeys-mcp/server" 2>/dev/null && pwd || true)"
  if [ -n "$REPO_SERVER" ] && [ -f "$REPO_SERVER/mcp_server.py" ]; then
    echo "Copying MCP server source from repo..."
    mkdir -p "$SERVER_DIR"
    cp "$REPO_SERVER/mcp_server.py" "$SERVER_DIR/"
    cp "$REPO_SERVER/script_ble_client.py" "$SERVER_DIR/"
    [ -f "$REPO_SERVER/requirements.txt" ] && cp "$REPO_SERVER/requirements.txt" "$SERVER_DIR/"
  else
    echo "ERROR: server/mcp_server.py not found."
    echo "Please copy partykeys-mcp/server/ contents into $SERVER_DIR/"
    exit 1
  fi
fi

echo "[✓] MCP server source ready"

# ── 3. Create Python venv & install deps ────────────────────────────
VENV_DIR="$SKILL_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet mcp aiohttp

echo "[✓] Python dependencies installed"

# ── 5. Register MCP server in OpenClaw ───────────────────────────────
PYTHON_BIN="$VENV_DIR/bin/python"
MCP_ENTRY="$SERVER_DIR/mcp_server.py"
MCP_JSON="$HOME/.openclaw/mcp.json"
OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"

cleanup_openclaw_json() {
  if [ -f "$OPENCLAW_JSON" ] && command -v jq &>/dev/null; then
    if jq -e '.mcp' "$OPENCLAW_JSON" &>/dev/null; then
      echo "Cleaning up stale 'mcp' key from openclaw.json..."
      local tmp
      tmp=$(mktemp)
      jq 'del(.mcp)' "$OPENCLAW_JSON" > "$tmp" && mv "$tmp" "$OPENCLAW_JSON"
      echo "[✓] Removed invalid 'mcp' key from openclaw.json"
    fi
  fi
}

register_mcp() {
  mkdir -p "$HOME/.openclaw"
  cleanup_openclaw_json

  if [ ! -f "$MCP_JSON" ]; then
    echo "{}" > "$MCP_JSON"
  fi

  if command -v jq &>/dev/null; then
    local tmp
    tmp=$(mktemp)
    jq --arg name "$MCP_NAME" \
       --arg cmd "$PYTHON_BIN" \
       --arg entry "$MCP_ENTRY" \
       '.mcpServers[$name] = {"command": $cmd, "args": [$entry]}' \
       "$MCP_JSON" > "$tmp" && mv "$tmp" "$MCP_JSON"
    echo "[✓] MCP server registered in $MCP_JSON"
  else
    cat > "$MCP_JSON" << MCPEOF
{
  "mcpServers": {
    "$MCP_NAME": {
      "command": "$PYTHON_BIN",
      "args": ["$MCP_ENTRY"]
    }
  }
}
MCPEOF
    echo "[✓] MCP server written to $MCP_JSON"
    echo "    (⚠ jq not found — existing entries in mcp.json may have been overwritten)"
  fi
}

register_mcp

# ── 6. Copy skill to OpenClaw skills directory ──────────────────────
OPENCLAW_SKILLS_DIR="$HOME/.openclaw/skills/$SKILL_NAME"

if [ ! -d "$OPENCLAW_SKILLS_DIR" ] || [ "$SKILL_DIR" != "$OPENCLAW_SKILLS_DIR" ]; then
  echo "Linking skill to OpenClaw skills directory..."
  mkdir -p "$HOME/.openclaw/skills"
  ln -sfn "$SKILL_DIR" "$OPENCLAW_SKILLS_DIR"
  echo "[✓] Skill linked at $OPENCLAW_SKILLS_DIR"
fi

# ── 7. Done ─────────────────────────────────────────────────────────
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw:  openclaw gateway restart"
echo "  2. Verify skill:      openclaw skills list"
echo "  3. Verify MCP:        openclaw mcp list"
echo "  4. Test:              Ask the agent '连接我的 MIDI 键盘'"
echo ""
echo "MCP server: $PYTHON_BIN $MCP_ENTRY"
echo "Skill path: $SKILL_DIR"
