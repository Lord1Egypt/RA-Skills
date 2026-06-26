#!/bin/bash
# Setup a new OpenClaw agent workspace and register it.
# Usage: ./setup-agent.sh <agent_name>
#
# Examples:
#   ./setup-agent.sh luna
#   ./setup-agent.sh pear
#
# After running this script, you still need to:
#   1. Add channel account + binding to openclaw.json (see SKILL.md Step 3)
#   2. Restart gateway: openclaw gateway restart
#   3. Pair: send /start to the bot, then openclaw pairing approve ...

set -e

AGENT_NAME="${1:?Usage: setup-agent.sh <agent_name>}"
AGENT_NAME_LOWER="${AGENT_NAME,,}"
AGENT_ID="${AGENT_NAME_LOWER}-agent"
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
WORKSPACE_DIR="${STATE_DIR}/workspace-groups/${AGENT_NAME_LOWER}"
CONFIG_PATH="${STATE_DIR}/openclaw.json"

echo "🤖 Creating agent: ${AGENT_NAME} (${AGENT_ID})"

# 1. Backup config
if [ -f "${CONFIG_PATH}" ]; then
  cp "${CONFIG_PATH}" "${CONFIG_PATH}.bak.$(date +%Y%m%d%H%M%S)"
  echo "📦 Config backed up"
fi

# 2. Create workspace
mkdir -p "${WORKSPACE_DIR}"

# 3. Generate workspace files
cat > "${WORKSPACE_DIR}/IDENTITY.md" << EOF
# IDENTITY.md - Who Am I?

- **Name:** ${AGENT_NAME}
- **Role:** AI 助手
- **Emoji:** 🤖
EOF

cat > "${WORKSPACE_DIR}/SOUL.md" << EOF
# SOUL.md - Who You Are

你是 **${AGENT_NAME}**，一个 AI 助手。

## 核心原则

- 友好、靠谱、高效
- 有问必答，遇到不确定的事情诚实说
- 用简洁的语言沟通

## 工作流程

1. 读 IDENTITY.md 和 USER.md 了解上下文
2. 认真回答问题
3. 重要信息记录到 MEMORY.md
EOF

cat > "${WORKSPACE_DIR}/AGENTS.md" << EOF
# AGENTS.md

## Session Startup

1. Read **SOUL.md** - 了解你的角色
2. Read **IDENTITY.md** - 确认身份
3. Read **USER.md** - 了解用户需求
EOF

cat > "${WORKSPACE_DIR}/USER.md" << EOF
# USER.md - About Your Human

- **Name:** [User Name]
- **Timezone:** UTC
EOF

echo "📁 Workspace created at ${WORKSPACE_DIR}"

# 4. Register agent (non-interactive)
if openclaw agents add "${AGENT_ID}" \
  --workspace "${WORKSPACE_DIR}" \
  --non-interactive 2>/dev/null; then
  echo "✅ Agent ${AGENT_ID} registered"
else
  echo "⚠️  Agent registration failed or already exists. Check manually:"
  echo "   openclaw agents add ${AGENT_ID} --workspace ${WORKSPACE_DIR} --non-interactive"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Workspace + registration done!"
echo ""
echo "Next steps (see SKILL.md Step 3):"
echo "  1. Add channel account to openclaw.json"
echo "     → channels.{channel}.accounts.${AGENT_NAME_LOWER}"
echo "  2. Add binding to top-level 'bindings' array:"
echo '     {"agentId": "'${AGENT_ID}'", "match": {"channel": "...", "accountId": "'${AGENT_NAME_LOWER}'"}}'
echo "  3. openclaw gateway restart"
echo "  4. openclaw agents list --bindings"
echo "  5. Send /start to bot → openclaw pairing approve ..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
