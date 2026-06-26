#!/bin/bash
# Deploy script for last-words skill to OpenClaw server
# Usage: ./deploy.sh user@hostname

set -e

# 请修改为你的服务器地址
REMOTE=${1:-"user@your-server.com"}
SKILL_NAME="last-words"
LOCAL_SKILL_PATH="$HOME/.openclaw/workspace/${SKILL_NAME}.skill"
REMOTE_PATH="/tmp/${SKILL_NAME}.skill"

echo "🚀 Deploying ${SKILL_NAME} skill to ${REMOTE}..."

# Check if skill package exists
if [ ! -f "$LOCAL_SKILL_PATH" ]; then
    echo "✗ Skill package not found: $LOCAL_SKILL_PATH"
    echo "  Run package script first:"
    echo "  python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py ~/.openclaw/workspace/last-words ~/.openclaw/workspace/"
    exit 1
fi

# Copy skill to server
echo "📦 Copying skill package..."
scp "$LOCAL_SKILL_PATH" "${REMOTE}:${REMOTE_PATH}"

# Install skill on remote server
echo "🔧 Installing skill on remote server..."
ssh "${REMOTE}" << EOF
    # Check if openclaw is installed
    if ! command -v openclaw &> /dev/null; then
        echo "✗ OpenClaw not found on remote server"
        exit 1
    fi

    # Find OpenClaw skills directory
    SKILL_DIR="\$HOME/.openclaw/skills"
    if [ ! -d "\$SKILL_DIR" ]; then
        mkdir -p "\$SKILL_DIR"
    fi

    # Extract skill
    cd "\$SKILL_DIR"
    unzip -o "${REMOTE_PATH}" -d "${SKILL_NAME}"

    # Clean up
    rm "${REMOTE_PATH}"

    echo "✓ Skill installed to \$SKILL_DIR/${SKILL_NAME}"

    # Show status
    openclaw skills list | grep last-words || echo "Skill installed but may need OpenClaw restart to detect"
EOF

echo "✓ Deployment complete!"
echo ""
echo "Next steps on the server:"
echo "  1. Test the skill: openclaw skills info last-words"
echo "  2. Set up daily cron: openclaw cron add --name 'last-words-check' --schedule '0 9 * * *' --command 'python3 ~/.openclaw/skills/last-words/scripts/check_activity.py'"
