#!/bin/bash
# Setup a new OpenClaw agent with workspace and channel binding.
# Usage: ./setup-agent.sh <agent_name> <channel> [channel_credentials...]
#
# Examples:
#   ./setup-agent.sh luna telegram "BOT_TOKEN_HERE"
#   ./setup-agent.sh coder discord "BOT_TOKEN_HERE"
#   ./setup-agent.sh helper slack "APP_TOKEN" "BOT_TOKEN"
#   ./setup-agent.sh team feishu "APP_ID" "APP_SECRET"

set -e

AGENT_NAME="${1:?Usage: setup-agent.sh <name> <channel> [credentials...]}"
CHANNEL="${2:?Please specify channel: telegram|discord|slack|feishu|whatsapp|signal|googlechat}"
AGENT_ID="${AGENT_NAME,,}-agent"
AGENT_DIR="${AGENT_NAME,,}"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
WORKSPACE_DIR="${STATE_DIR}/workspace-groups/${AGENT_DIR}"
CONFIG_PATH="${STATE_DIR}/openclaw.json"

echo "Creating agent: ${AGENT_NAME} (${AGENT_ID}) on ${CHANNEL}"

# 1. Backup config
cp "${CONFIG_PATH}" "${CONFIG_PATH}.bak.$(date +%Y%m%d%H%M%S)"

# 2. Create workspace
mkdir -p "${WORKSPACE_DIR}"

# 3. Register agent
openclaw agents add "${AGENT_ID}" 2>/dev/null || true

# 4. Generate workspace files
cat > "${WORKSPACE_DIR}/IDENTITY.md" << EOF
# IDENTITY.md

- **Name:** ${AGENT_NAME}
- **Role:** [Define role here]
- **Emoji:** 🤖
EOF

cat > "${WORKSPACE_DIR}/SOUL.md" << EOF
# SOUL.md

You are ${AGENT_NAME}, an independent AI assistant.

Be genuinely helpful. Have opinions. Try before asking.
Keep private things private. Never send half-baked replies.
EOF

cat > "${WORKSPACE_DIR}/AGENTS.md" << EOF
# AGENTS.md

## On startup
1. Read SOUL.md
2. Read IDENTITY.md
3. Read USER.md if present

## Memory
Write important notes to memory/YYYY-MM-DD.md
EOF

cat > "${WORKSPACE_DIR}/USER.md" << EOF
# USER.md

- **Name:** [User Name]
- **Timezone:** UTC
EOF

touch "${WORKSPACE_DIR}/HEARTBEAT.md"
touch "${WORKSPACE_DIR}/TOOLS.md"

echo "✅ Workspace created at ${WORKSPACE_DIR}"
echo ""
echo "Next steps:"
echo "  1. Update openclaw.json with channel account and binding"
echo "  2. Run: openclaw gateway restart"
echo "  3. Run: openclaw agents list --bindings"
echo "  4. Send /start to the bot and approve pairing"
