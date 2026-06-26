#!/bin/bash
# install.sh — Install Grok Swarm from ClawHub skill
# Run this after: clawhub install grok-swarm

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1" >&2; }

echo "=========================================="
echo "  Grok Swarm Installer (from ClawHub)"
echo "=========================================="
echo

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    error "Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Install plugin
log "Installing OpenClaw plugin..."
PLUGIN_DIR="$OPENCLAW_HOME/extensions/grok-swarm"
mkdir -p "$PLUGIN_DIR"
if [ -f "$SCRIPT_DIR/openclaw.plugin.json" ]; then
    cp "$SCRIPT_DIR/openclaw.plugin.json" "$PLUGIN_DIR/"
    log "Plugin manifest installed"
else
    warn "No plugin manifest found, skipping"
fi

# Install bridge skill
log "Installing Grok Swarm bridge..."
SKILL_DIR="$OPENCLAW_HOME/skills/grok-refactor"
mkdir -p "$SKILL_DIR"

if [ -d "$SCRIPT_DIR/bridge" ]; then
    cp -r "$SCRIPT_DIR/bridge/"* "$SKILL_DIR/"
    log "Bridge files installed"
else
    error "Bridge files not found in skill!"
    exit 1
fi

# Set up Python venv
log "Setting up Python environment..."
if [ ! -d "$SKILL_DIR/.venv" ]; then
    python3 -m venv "$SKILL_DIR/.venv"
fi
"$SKILL_DIR/.venv/bin/pip" install -q openai>=1.0.0
log "Python packages installed"

# Create config directory
log "Setting up API key configuration..."
CONFIG_DIR="$HOME/.config/grok-swarm"
mkdir -p "$CONFIG_DIR"
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    echo '{"api_key": ""}' > "$CONFIG_DIR/config.json"
    chmod 600 "$CONFIG_DIR/config.json"
    warn "Created $CONFIG_DIR/config.json — add your OpenRouter API key"
fi

echo
log "Installation complete!"
echo
echo "Next steps:"
echo "  1. Add your API key to $CONFIG_DIR/config.json"
echo "     Or set: export OPENROUTER_API_KEY=sk-or-v1-..."
echo "  2. Update ~/.openclaw/openclaw.json to enable the plugin:"
echo "     - Add 'grok-swarm' to plugins.allow"
echo "     - Add 'grok_swarm' to agent tools.allow"
echo "  3. Restart OpenClaw: openclaw gateway restart"
echo
echo "Usage:"
echo "  node $SKILL_DIR/index.js --prompt 'Your task' --mode analyze"
