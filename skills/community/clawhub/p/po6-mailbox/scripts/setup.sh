#!/usr/bin/env bash
set -euo pipefail

# PO6 Mailbox — OpenClaw MCP Server Setup
# Adds the PO6 MCP server to your OpenClaw configuration.
# https://po6.com/docs/mcp

CONFIG_DIR="$HOME/.openclaw"
CONFIG_FILE="$CONFIG_DIR/openclaw.json"

echo "PO6 Mailbox — OpenClaw Setup"
echo "=============================="
echo ""

# 1. Check for API key
if [ -z "${PO6_API_KEY:-}" ]; then
    echo "Error: PO6_API_KEY is not set."
    echo ""
    echo "To get your API key:"
    echo "  1. Go to https://po6.com/dashboard/mailbox"
    echo "  2. Create a new API key"
    echo "  3. Run: export PO6_API_KEY=\"mcp_po6_your_key_here\""
    echo "  4. Re-run this script"
    echo ""
    exit 1
fi

# 2. Validate key format
if [[ ! "$PO6_API_KEY" =~ ^mcp_po6_ ]]; then
    echo "Warning: PO6_API_KEY doesn't start with 'mcp_po6_'."
    echo "Make sure you copied the full key from your dashboard."
    echo ""
    read -r -p "Continue anyway? [y/N] " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 3. Add MCP server to config file (with auth header)
echo "Adding MCP server to $CONFIG_FILE..."

# Create config directory if needed
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
fi

MCP_ENTRY='{
  "type": "streamable-http",
  "url": "https://mcp.po6.com",
  "headers": {
    "Authorization": "Bearer ${PO6_API_KEY}"
  }
}'

if [ ! -f "$CONFIG_FILE" ]; then
    # No config file — create one from scratch
    cat > "$CONFIG_FILE" << 'JSONEOF'
{
  "mcpServers": {
    "po6-mailbox": {
      "type": "streamable-http",
      "url": "https://mcp.po6.com",
      "headers": {
        "Authorization": "Bearer ${PO6_API_KEY}"
      }
    }
  }
}
JSONEOF
    echo "Created $CONFIG_FILE with PO6 MCP server."
else
    # Config file exists — merge using jq
    if ! command -v jq &> /dev/null; then
        echo ""
        echo "Error: jq is not installed and is needed to safely edit $CONFIG_FILE."
        echo ""
        echo "Install jq (https://jqlang.github.io/jq/download/) and re-run, or"
        echo "manually add this under \"mcpServers\" in $CONFIG_FILE:"
        echo ""
        echo '    "po6-mailbox": {
      "type": "streamable-http",
      "url": "https://mcp.po6.com",
      "headers": {
        "Authorization": "Bearer ${PO6_API_KEY}"
      }
    }'
        echo ""
        exit 1
    fi

    if jq -e '.mcpServers["po6-mailbox"]' "$CONFIG_FILE" &> /dev/null; then
        echo "PO6 MCP server is already configured."
        read -r -p "Overwrite existing config? [y/N] " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "No changes made."
            exit 0
        fi
    fi

    # Ensure mcpServers key exists, then add po6-mailbox
    jq --argjson entry "$MCP_ENTRY" \
       '.mcpServers //= {} | .mcpServers["po6-mailbox"] = $entry' \
       "$CONFIG_FILE" > "${CONFIG_FILE}.tmp"
    mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
    echo "PO6 MCP server added to $CONFIG_FILE."
fi

# 5. Test connectivity via the MCP discovery endpoint (no auth required)
echo ""
echo "Testing connection to mcp.po6.com..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://mcp.po6.com/.well-known/mcp.json" 2>/dev/null || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "Connection successful! MCP server is reachable."
elif [ "$HTTP_STATUS" = "000" ]; then
    echo "Warning: Could not reach mcp.po6.com. Check your internet connection."
else
    echo "Warning: MCP server responded with HTTP $HTTP_STATUS."
    echo "The server may be temporarily unavailable. Try again later."
fi

echo ""
echo "Restart OpenClaw to start using the PO6 skill."
