#!/bin/bash
# Setup Gitee Repository for OpenClaw Agent Backup
#
# Usage: ./setup-gitee.sh <agent-name> [gitee-username]
#
# This script:
# 1. Creates a new Gitee repository (if token has projects permission)
# 2. Configures local git for backup
# 3. Saves configuration for backup script

set -e

AGENT_NAME="${1:-}"
GITEE_USERNAME="${2:-}"
GITEE_TOKEN="${GITEE_TOKEN:-}"

# Validate inputs
if [[ -z "$AGENT_NAME" ]]; then
    echo "Usage: ./setup-gitee.sh <agent-name> [gitee-username]"
    echo ""
    echo "Example: ./setup-gitee.sh elder myusername"
    echo ""
    echo "Environment variables:"
    echo "  GITEE_TOKEN - Your Gitee Personal Access Token (required)"
    exit 1
fi

if [[ -z "$GITEE_TOKEN" ]]; then
    echo "Error: GITEE_TOKEN not set."
    echo ""
    echo "Create a token at: https://gitee.com/profile/personal_access_tokens"
    echo "Required scopes: projects (for repo creation), user_info"
    echo ""
    echo "Then export: export GITEE_TOKEN=your_token_here"
    exit 1
fi

REPO_NAME="openclaw-${AGENT_NAME}"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
CONFIG_FILE="$WORKSPACE_DIR/.gitee-backup"

echo "=== Gitee Backup Setup ==="
echo "Agent: $AGENT_NAME"
echo "Repo: $REPO_NAME"
echo ""

# Get username from API if not provided
if [[ -z "$GITEE_USERNAME" ]]; then
    echo "Fetching Gitee username..."
    GITEE_USERNAME=$(curl -s "https://gitee.com/api/v5/user?access_token=$GITEE_TOKEN" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
    if [[ -z "$GITEE_USERNAME" ]]; then
        echo "Error: Could not fetch username. Please provide it manually."
        exit 1
    fi
    echo "Username: $GITEE_USERNAME"
fi

REPO_URL="https://gitee.com/${GITEE_USERNAME}/${REPO_NAME}.git"

# Try to create repository
echo ""
echo "Creating repository: $REPO_NAME"
CREATE_RESULT=$(curl -s -X POST "https://gitee.com/api/v5/user/repos" \
    -H "Content-Type: application/json" \
    -d "{
        \"access_token\": \"$GITEE_TOKEN\",
        \"name\": \"$REPO_NAME\",
        \"description\": \"OpenClaw Agent $AGENT_NAME - Workspace Backup\",
        \"private\": true,
        \"has_issues\": false,
        \"has_wiki\": false,
        \"auto_init\": true
    }" 2>&1)

if echo "$CREATE_RESULT" | grep -q '"id"'; then
    echo "✅ Repository created successfully"
elif echo "$CREATE_RESULT" | grep -q "already exists"; then
    echo "ℹ️  Repository already exists, continuing..."
else
    echo "⚠️  Could not create repository (may need manual creation)"
    echo "   Response: $CREATE_RESULT"
fi

# Save configuration
echo ""
echo "Saving configuration..."
cat > "$CONFIG_FILE" << EOF
# Gitee Backup Configuration
# Generated: $(date)
AGENT_NAME=$AGENT_NAME
GITEE_USERNAME=$GITEE_USERNAME
GITEE_REPO=$REPO_URL
EOF

echo "✅ Configuration saved to: $CONFIG_FILE"
echo ""
echo "=== Setup Complete ==="
echo ""
echo "Repo URL: $REPO_URL"
echo ""
echo "Next steps:"
echo "1. Test backup: GITEE_TOKEN=xxx ./scripts/backup-to-gitee.sh"
echo "2. Add to cron for auto-backup:"
echo "   crontab -e"
echo "   # Add: 0 */4 * * * GITEE_TOKEN=xxx /path/to/backup-to-gitee.sh >> /tmp/backup.log 2>&1"
echo ""
echo "Or set GITEE_TOKEN in your environment for persistent use."