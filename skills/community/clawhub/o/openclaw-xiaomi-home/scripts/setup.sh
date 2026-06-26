#!/bin/bash
# Setup script for openclaw-xiaomi-home skill
# This script helps users install Home Assistant and configure the MCP server

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$SKILL_DIR/scripts/ha-mcp-server"
PLIST_SRC="$SCRIPT_DIR/ai.openclaw.ha-mcp.plist"

echo "=========================================="
echo "Xiaomi Home Skill Setup"
echo "=========================================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker Desktop from: https://docs.docker.com/desktop/setup/install/mac-install/"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "Error: Docker is not running."
    echo "Please start Docker Desktop."
    exit 1
fi
echo "✓ Docker is installed and running"

# Start Home Assistant
echo ""
echo "Starting Home Assistant..."
cd "$SKILL_DIR"
docker compose up -d 2>/dev/null || docker run -d \
  --name homeassistant \
  --privileged \
  -p 8123:8123 \
  -v ~/homeassistant/config:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -e TZ=Asia/Shanghai \
  --dns=8.8.8.8 \
  --dns=223.5.5.5 \
  --restart=unless-stopped \
  ghcr.io/home-assistant/home-assistant:stable

echo "✓ Home Assistant started"
echo "  Access at: http://localhost:8123"
echo ""
echo "  First-time setup:"
echo "  1. Open http://localhost:8123 and create your account"
echo "  2. Add 'external_url: http://localhost:8123' to ~/homeassistant/config/configuration.yaml"
echo "  3. Go to Settings → Devices & Services → Add Integration"
echo "  4. Search 'Xiaomi Home' and login with your Xiaomi account"
echo "  5. Profile → Security → Create Long-Lived Access Token"
echo ""

# Setup HA token
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "=========================================="
    echo "MCP Server Configuration"
    echo "=========================================="
    echo "Enter your Home Assistant Long-Lived Access Token:"
    read -r HA_TOKEN
    echo "HA_URL=http://localhost:8123" > "$SCRIPT_DIR/.env"
    echo "HA_TOKEN=$HA_TOKEN" >> "$SCRIPT_DIR/.env"
    echo "PORT=3002" >> "$SCRIPT_DIR/.env"
    echo "✓ Created .env file"
else
    echo "✓ .env file already exists"
fi

# Install MCP Server dependencies
echo ""
echo "Installing MCP Server..."
cd "$SCRIPT_DIR"
npm install --silent 2>/dev/null

# Setup LaunchAgent
echo ""
echo "Installing HA MCP Server as LaunchAgent..."
mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "$(dirname "$PLIST_SRC")"

# Create user-specific plist
PLIST_DST="$HOME/Library/LaunchAgents/ai.openclaw.ha-mcp.plist"
sed "s|/Users/nanali|$HOME|g" "$PLIST_SRC" > "$PLIST_DST"
launchctl load "$PLIST_DST" 2>/dev/null || true
echo "✓ HA MCP Server installed as LaunchAgent"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "HA MCP Server: http://localhost:3002"
echo "Home Assistant: http://localhost:8123"
echo ""
echo "Test the MCP server:"
echo "  node $SCRIPT_DIR/src/call-tool.mjs ping_ha"
echo ""
echo "For OpenClaw integration, add this skill to your OpenClaw"
echo "and the MCP server will automatically handle device control."
