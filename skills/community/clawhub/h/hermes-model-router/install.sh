#!/bin/bash
#
# Model Router Skill Installer (OpenClaw Version)
# 本地优先的智能模型选择器安装脚本
#

set -e

echo "🧠 Model Router Skill Installer (OpenClaw)"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SKILL_DIR="$HOME/.clawdbot/skills/model-router"
WORKSPACE_SKILL_DIR="$HOME/clawd/skills/model-router"

# Determine where to install
if [ -d "$HOME/clawd/skills" ]; then
    TARGET_DIR="$WORKSPACE_SKILL_DIR"
    echo -e "${GREEN}📁${NC} Installing to workspace skills: $TARGET_DIR"
elif [ -d "$HOME/.clawdbot/skills" ]; then
    TARGET_DIR="$SKILL_DIR"
    echo -e "${GREEN}📁${NC} Installing to global skills: $TARGET_DIR"
else
    mkdir -p "$SKILL_DIR"
    TARGET_DIR="$SKILL_DIR"
    echo -e "${GREEN}📁${NC} Creating global skills directory: $TARGET_DIR"
fi

# Get current directory
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${GREEN}📦${NC} Installing from: $CURRENT_DIR"

# Copy files
echo -e "${GREEN}📋${NC} Copying skill files..."
cp -r "$CURRENT_DIR"/* "$TARGET_DIR/"

# Make scripts executable
echo -e "${GREEN}🔧${NC} Making scripts executable..."
chmod +x "$TARGET_DIR/scripts/"*.py 2>/dev/null || true

# Create config directory
mkdir -p "$HOME/.model-router"
chmod 700 "$HOME/.model-router"

echo ""
echo -e "${GREEN}✅${NC} Skill installed to: $TARGET_DIR"
echo ""
echo -e "${GREEN}🧠${NC} Model Router v1.0.0 (OpenClaw)"
echo ""
echo -e "${GREEN}📖${NC} Next steps:"
echo "   1. Run the setup wizard:"
echo "      cd $TARGET_DIR"
echo "      python3 scripts/setup_wizard.py"
echo ""
echo "   2. Configure your providers (local / cloud)"
echo ""
echo "   3. Start routing tasks optimally!"
echo ""
echo -e "${GREEN}📚${NC} Documentation: $TARGET_DIR/SKILL.md"
echo ""
echo -e "${GREEN}🎉${NC} Installation complete!"
