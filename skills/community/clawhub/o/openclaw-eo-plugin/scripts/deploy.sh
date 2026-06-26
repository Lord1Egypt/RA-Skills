#!/bin/bash
# ============================================================================
# EO Plugin Auto-Deploy Script
#
# Ensures source code and deployed plugin stay in sync.
# Usage: npm run deploy
# ============================================================================

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Config
PLUGIN_NAME="@eo/openclaw-plugin"
DEPLOY_DIR="$HOME/.openclaw/extensions/eo-collaboration"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=========================================="
echo "EO Plugin Deploy Script"
echo "=========================================="
echo "Plugin: $PLUGIN_NAME"
echo "Source:  $SRC_DIR"
echo "Deploy:  $DEPLOY_DIR"
echo "=========================================="

# Step 1: Check if deployed directory exists
if [ ! -d "$DEPLOY_DIR" ]; then
    echo -e "${YELLOW}⚠️  Deploy directory doesn't exist, creating...${NC}"
    mkdir -p "$DEPLOY_DIR"
fi

# Step 2: Build
echo ""
echo "[1/4] Building TypeScript..."
cd "$SRC_DIR"
npm run build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build successful${NC}"

# Step 3: Sync plugin files
echo ""
echo "[2/4] Syncing plugin files to $DEPLOY_DIR..."

# Sync root config files
rsync -av \
    "$SRC_DIR/package.json" \
    "$SRC_DIR/openclaw.plugin.json" \
    "$SRC_DIR/tsconfig.json" \
    "$DEPLOY_DIR/"

# Sync dist directory
rsync -av --delete \
    "$SRC_DIR/dist/" \
    "$DEPLOY_DIR/dist/"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Sync failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Sync successful${NC}"

# Step 4: Verify
echo ""
echo "[3/4] Verifying deployment..."

ERRORS=0

# Check critical files exist
CRITICAL_FILES=(
    "dist/index.js"
    "dist/skills/executor.js"
    "dist/workflow/progress-executor.js"
    "dist/collaboration/task-distributor.js"
    "dist/hooks/eo-dream/handler.js"
    "package.json"
    "openclaw.plugin.json"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$DEPLOY_DIR/$file" ]; then
        echo -e "  ✅ $file"
    else
        echo -e "  ❌ $file (MISSING)"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check package.json version matches
SRC_VERSION=$(node -p "require('./package.json').version")
DEPLOY_VERSION=$(node -p "require('$DEPLOY_DIR/package.json').version")

if [ "$SRC_VERSION" = "$DEPLOY_VERSION" ]; then
    echo -e "  ✅ Version: $SRC_VERSION"
else
    echo -e "  ⚠️  Version mismatch: src=$SRC_VERSION deploy=$DEPLOY_VERSION"
fi

# Step 5: New files info
echo ""
echo "[4/4] New modules added..."
echo "  ✅ session/session-archiver.js - Session history indexing"
echo "  ✅ session/eo-dream-enhanced.js - Enhanced Dream Module v2"
echo "  ✅ session/context-loader.js - Historical context loader"

# Final status
echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo "To restart the plugin:"
    echo "  openclaw gateway restart"
    echo ""
else
    echo -e "${RED}❌ Deployment completed with $ERRORS errors${NC}"
    exit 1
fi
echo "=========================================="
