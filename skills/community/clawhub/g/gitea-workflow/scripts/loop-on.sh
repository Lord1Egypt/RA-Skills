#!/usr/bin/env bash
# 启用 gitea-workflow 循环 cron
# 每个 agent 跑前自己设置环境变量:
#   export GITEA_WORKFLOW_CRON="<自己的 cron 名>"
# 默认按 agent 类型推 cron 名(用 /etc/openclaw/agent-name 或 $USER)

set -euo pipefail

# 1. 决定 cron 名
if [ -z "${GITEA_WORKFLOW_CRON:-}" ]; then
    if [ -f /etc/openclaw/agent-name ]; then
        AGENT=$(cat /etc/openclaw/agent-name)
    else
        AGENT="${USER:-unknown}"
    fi
    CRON_NAME="gitea-workflow-${AGENT}"
else
    CRON_NAME="$GITEA_WORKFLOW_CRON"
fi

echo "[loop-on] enabling cron: $CRON_NAME"

# 2. 启用 cron(openclaw CLI 用法)
openclaw cron enable "$CRON_NAME" 2>&1 | tail -5

# 3. 显示状态
echo ""
echo "[loop-on] current status:"
openclaw cron get "$CRON_NAME" 2>&1 | head -10 || echo "(cron not found - need to set up first, see references/cron-setup.md)"
