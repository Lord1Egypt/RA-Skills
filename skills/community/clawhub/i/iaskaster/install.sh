#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

detect_claw_variant() {
    local variant=""
    local config_path=""
    
    if [ -d "/Applications/OpenClaw.app" ] || [ -d "$HOME/Applications/OpenClaw.app" ]; then
        variant="openclaw"
        config_path="$HOME/.openclaw"
    elif [ -d "/Applications/QClaw.app" ] || [ -d "$HOME/Applications/QClaw.app" ]; then
        variant="qclaw"
        config_path="$HOME/.qclaw"
    elif [ -d "/Applications/Claw.app" ] || [ -d "$HOME/Applications/Claw.app" ]; then
        variant="claw"
        config_path="$HOME/.claw"
    elif [ -d "/Applications/OpenCodeAI.app" ]; then
        variant="opencode"
        config_path="$HOME/.openclaw"
    elif [ -f "$HOME/.openclaw/openclaw.json" ]; then
        variant="openclaw"
        config_path="$HOME/.openclaw"
    elif [ -f "$HOME/.qclaw/openclaw.json" ]; then
        variant="qclaw"
        config_path="$HOME/.qclaw"
    else
        variant="openclaw"
        config_path="$HOME/.openclaw"
    fi
    
    echo "$variant:$config_path"
}

VARIANT_INFO=$(detect_claw_variant)
VARIANT=$(echo "$VARIANT_INFO" | cut -d':' -f1)
CONFIG_BASE=$(echo "$VARIANT_INFO" | cut -d':' -f2)
CONFIG_FILE="$CONFIG_BASE/openclaw.json"
SKILL_PATH="$CONFIG_BASE/workspace/skills/iaskaster"

echo "Detected variant: $VARIANT"
echo "Config path: $CONFIG_BASE"
echo ""

echo "Installing iaskaster skill..."

echo ""
echo "=========================================="
echo "  Environment Check"
echo "=========================================="
echo ""

ERRORS=0

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js: NOT FOUND"
    echo "   Please install Node.js: https://nodejs.org/"
    ERRORS=$((ERRORS + 1))
fi

# Check for single-file bundle or source
USE_BUNDLE=false
if [ -f "$SCRIPT_DIR/index.js" ]; then
    echo "✅ index.js: found (single-file mode)"
    USE_BUNDLE=true
elif [ -d "$SCRIPT_DIR/node_modules" ]; then
    echo "✅ node_modules: installed (source mode)"
else
    echo "❌ index.js: NOT FOUND"
    echo "   Please run: cd $SCRIPT_DIR && bash build.sh"
    ERRORS=$((ERRORS + 1))
fi

# Check required files
REQUIRED_FILES=(
    "SKILL.md"
    "openclaw.plugin.json"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "✅ $file: exists"
    else
        echo "❌ $file: NOT FOUND"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check openclaw.json exists
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ openclaw.json: found"
else
    echo "⚠️  openclaw.json: NOT FOUND at $CONFIG_FILE"
    echo "   Will be created during installation"
fi

echo ""
echo "=========================================="

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ Environment check FAILED with $ERRORS error(s)"
    echo "   Please fix the issues above before installing"
    echo ""
    exit 1
fi

echo "✅ Environment check PASSED"
echo ""
echo "Starting installation..."
echo ""

# Copy skill to workspace (exclude node_modules)
mkdir -p "$CONFIG_BASE/workspace/skills"
rm -rf "$SKILL_PATH"
mkdir -p "$SKILL_PATH"

if [ "$USE_BUNDLE" = true ]; then
    # Single-file mode: only copy bundle and config files
    cp "$SCRIPT_DIR/index.js" "$SKILL_PATH/"
    cp "$SCRIPT_DIR/SKILL.md" "$SKILL_PATH/"
    cp "$SCRIPT_DIR/openclaw.plugin.json" "$SKILL_PATH/"
    cp "$SCRIPT_DIR/package.json" "$SKILL_PATH/"
    
    # Install only puppeteer-core for screenshot feature
    cd "$SKILL_PATH"
    npm install puppeteer-core
else
    # Source mode: copy all files and install dependencies
    for item in "$SCRIPT_DIR"/*; do
      if [ "$(basename "$item")" != "node_modules" ]; then
        cp -r "$item" "$SKILL_PATH/"
      fi
    done
    
    cd "$SKILL_PATH"
    npm install
fi

# Add skill config to openclaw.json if not exists
if [ -f "$CONFIG_FILE" ]; then
    # Check if iaskaster already in skills.entries
    if grep -q '"iaskaster"' "$CONFIG_FILE" && grep -q '"entries"' "$CONFIG_FILE"; then
        # Check if it's in entries specifically
        if grep -A5 '"entries"' "$CONFIG_FILE" | grep -q '"iaskaster"'; then
            echo "Skill already configured in openclaw.json"
        else
            update_config=true
        fi
    else
        update_config=true
    fi

    if [ "$update_config" = true ]; then
        # Use node to add skill config with new format
        node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));

if (!config.skills) config.skills = {};
if (!config.skills.allowBundled) config.skills.allowBundled = [];
if (!config.skills.allowBundled.includes('iaskaster')) config.skills.allowBundled.push('iaskaster');

if (!config.skills.load) config.skills.load = {};
if (!config.skills.load.extraDirs) config.skills.load.extraDirs = [];
const skillDir = '$CONFIG_BASE/workspace/skills';
if (!config.skills.load.extraDirs.includes(skillDir)) config.skills.load.extraDirs.push(skillDir);
if (!('watch' in config.skills.load)) config.skills.load.watch = true;
if (!('watchDebounceMs' in config.skills.load)) config.skills.load.watchDebounceMs = 250;

if (!config.skills.install) config.skills.install = {};
if (!config.skills.install.preferBrew) config.skills.install.preferBrew = true;
if (!config.skills.install.nodeManager) config.skills.install.nodeManager = 'npm';

if (!config.skills.entries) config.skills.entries = {};
if (!config.skills.entries.iaskaster) config.skills.entries.iaskaster = { enabled: true };

fs.writeFileSync('$CONFIG_FILE', JSON.stringify(config, null, 2));
"
        echo "Updated openclaw.json"
    fi
else
    echo "Warning: openclaw.json not found at $CONFIG_FILE"
    echo "Please manually add skill configuration"
fi

echo ""
echo "Installation complete! Restart $VARIANT gateway:"
echo "  $VARIANT gateway restart"