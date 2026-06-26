#!/usr/bin/env bash
set -euo pipefail

# Setup script for oauth-coder-bridge skill
# Installs the HTTP bridge and updates OpenClaw config

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Copy bridge script to ~/.openclaw/scripts
mkdir -p ~/.openclaw/scripts
cp "$SCRIPT_DIR/oauth-coder-bridge.py" ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/oauth-coder-bridge.py

echo "Installed: ~/.openclaw/scripts/oauth-coder-bridge.py"

# Update OpenClaw config (adds claude-cli provider)
python3 "$SCRIPT_DIR/update-openclaw-config.py"

echo ""
echo "Setup complete. Start the bridge with:"
echo "  python3 ~/.openclaw/scripts/oauth-coder-bridge.py &"
echo ""
echo "Or enable systemd auto-start:"
echo "  systemctl --user enable --now oauth-coder-bridge"
