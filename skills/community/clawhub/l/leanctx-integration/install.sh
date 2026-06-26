#!/bin/bash
# LeanContext Integration Installer for OpenClaw

# SECURITY MANIFEST:
#   Environment variables accessed: HOME (only)
#   External endpoints called: none
#   Local files read: $HOME/.openclaw/openclaw.json
#   Local files written: $HOME/.openclaw/openclaw.json (backup created)

set -euo pipefail

echo "Installing LeanContext integration for OpenClaw..."

SKILL_DIR="$HOME/.openclaw/workspace/skills/leanctx-integration"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# Build the skill
cd "$SKILL_DIR"
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Building..."
# Skip build - dist/ already contains compiled JavaScript
# npx tsc

# Check if already configured
if grep -q "leanctx-integration" "$CONFIG_FILE" 2>/dev/null; then
    echo "Already configured in openclaw.json"
else
    echo "Adding to OpenClaw config..."
    
    # Create backup
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%s)"
    
    # Add to hooks section
    # This is a simplified approach - in production would use jq
    echo ""
    echo "Add this to your openclaw.json under 'hooks.internal.entries':"
    echo ""
    cat <<EOF
    "leanctx-integration": {
      "enabled": true,
      "config": {
        "threshold": 100,
        "cacheEnabled": true,
        "excludedPaths": ["node_modules", ".git", "dist", ".svelte-kit"],
        "excludedCommands": ["cat", "echo", "head", "tail"]
      }
    }
EOF
    echo ""
fi

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit ~/.openclaw/openclaw.json and add the hook config (shown above)"
echo "2. Restart OpenClaw"
echo "3. Run 'openclaw skills run leanctx-integration --action=metrics' to see savings"
echo ""
