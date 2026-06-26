#!/bin/bash
# Likes Training Planner Skill Installer
# IMPORTANT: Must be installed to ~/.openclaw/workspace/skills/

set -e

SKILL_NAME="likes-training-planner"
SKILL_URL="https://gitee.com/chenyinshu/likes-training-planner/releases/latest/download/likes-training-planner.skill"

echo "📦 Installing Likes Training Planner Skill..."
echo ""

# Detect correct OpenClaw workspace skills directory
# Priority:
# 1. ~/.openclaw/workspace/skills/ (recommended)
# 2. Fallback to other locations

if [ -d "$HOME/.openclaw/workspace/skills" ]; then
    SKILLS_DIR="$HOME/.openclaw/workspace/skills"
    echo "✓ Found OpenClaw workspace skills directory"
elif [ -d "$HOME/.openclaw/workspace" ]; then
    # Create the skills subdirectory
    SKILLS_DIR="$HOME/.openclaw/workspace/skills"
    mkdir -p "$SKILLS_DIR"
    echo "✓ Created OpenClaw workspace/skills directory"
else
    echo "❌ Error: Could not find OpenClaw workspace directory"
    echo ""
    echo "Expected location: ~/.openclaw/workspace/skills/"
    echo ""
    echo "Please ensure OpenClaw is properly installed."
    exit 1
fi

echo "📁 Install location: $SKILLS_DIR/$SKILL_NAME"
echo ""

# Verify it's the correct location (not workspace root)
if [[ "$SKILLS_DIR" == *"/workspace" ]] && [[ ! "$SKILLS_DIR" == *"/workspace/skills" ]]; then
    echo "❌ Error: Cannot install directly to workspace/"
    echo "   Must install to workspace/skills/ subdirectory"
    echo ""
    echo "Creating correct directory structure..."
    SKILLS_DIR="$SKILLS_DIR/skills"
    mkdir -p "$SKILLS_DIR"
fi

# Create temp directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

# Download skill
echo "⬇️  Downloading skill..."
if command -v curl &> /dev/null; then
    curl -fsSL -o "$SKILL_NAME.skill" "$SKILL_URL"
elif command -v wget &> /dev/null; then
    wget -q -O "$SKILL_NAME.skill" "$SKILL_URL"
else
    echo "❌ Error: curl or wget required"
    exit 1
fi

# Check if skill file was downloaded
if [ ! -f "$SKILL_NAME.skill" ]; then
    echo "❌ Error: Failed to download skill"
    exit 1
fi

echo "✅ Downloaded"

# Remove old version if exists
if [ -d "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo "🔄 Removing old version..."
    rm -rf "$SKILLS_DIR/$SKILL_NAME"
fi

# Extract skill to correct location
echo "📂 Extracting to $SKILLS_DIR/..."
unzip -q "$SKILL_NAME.skill" -d "$SKILLS_DIR/"

# Verify installation
if [ -d "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo "✅ Skill extracted successfully"
else
    echo "❌ Error: Failed to extract skill"
    exit 1
fi

# Cleanup
rm -rf "$TMP_DIR"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Installation Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📍 Installed to: $SKILLS_DIR/$SKILL_NAME"
echo ""
echo "📝 Next steps:"
echo "1. Restart OpenClaw:"
echo "   openclaw gateway restart"
echo ""
echo "2. Open OpenClaw Control UI:"
echo "   http://127.0.0.1:18789"
echo ""
echo "3. Go to Skills → likes-training-planner → Configure"
echo ""
echo "4. Enter your Likes API Key"
echo "   (Get it from: https://my.likes.com.cn → 设置 → API 文档)"
echo ""
echo "5. Start using: '帮我生成一个训练计划'"
echo ""
echo "📚 Documentation: https://gitee.com/chenyinshu/likes-training-planner"
echo "════════════════════════════════════════════════════════════"
