#!/bin/bash

# OpenClaw Key Management Skill Installer
# Usage: ./install.sh [workspace_path]

set -e

WORKSPACE_PATH="${1:-$HOME/.openclaw/zhaining}"
SKILL_NAME="openclaw-key-management"
SKILL_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing OpenClaw Key Management Skill..."
echo "Workspace: $WORKSPACE_PATH"
echo "Skill source: $SKILL_SOURCE"

# Create skills directory if it doesn't exist
mkdir -p "$WORKSPACE_PATH/skills"

# Copy skill to workspace
cp -r "$SKILL_SOURCE" "$WORKSPACE_PATH/skills/$SKILL_NAME"

echo "✅ Skill copied to $WORKSPACE_PATH/skills/$SKILL_NAME"

# Initialize the key vault
echo "🔧 Initializing key vault..."
cd "$WORKSPACE_PATH"
./skills/$SKILL_NAME/scripts/key_manager.sh init

echo "✅ Key vault initialized at $WORKSPACE_PATH/.secrets/"

# Check if there are existing credentials to migrate
if grep -q "{SECRET:" "$WORKSPACE_PATH/MEMORY.md" 2>/dev/null; then
    echo "🔍 Found existing secure references in MEMORY.md"
elif grep -q "sk_inst_\|api_key\|password" "$WORKSPACE_PATH/MEMORY.md" 2>/dev/null; then
    echo "⚠️  Found potential credentials in MEMORY.md"
    echo "💡 Run './skills/$SKILL_NAME/scripts/key_manager.sh migrate' to secure them"
else
    echo "✅ No existing credentials found to migrate"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add credentials: ./skills/$SKILL_NAME/scripts/key_manager.sh add my_api_key"
echo "2. Test retrieval: ./skills/$SKILL_NAME/scripts/key_manager.sh get my_api_key"
echo "3. View all commands: ./skills/$SKILL_NAME/scripts/key_manager.sh"
echo ""
echo "Documentation: $WORKSPACE_PATH/skills/$SKILL_NAME/SKILL.md"