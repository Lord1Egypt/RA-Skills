#!/usr/bin/env bash
# 停用 gitea-workflow 循环 cron
# (跟 loop-on.sh 配对,语义相反)

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

echo "[loop-off] disabling cron: $CRON_NAME"

# 2. 停用 cron
openclaw cron disable "$CRON_NAME" 2>&1 | tail -5

# 3. 显示状态
echo ""
echo "[loop-off] current status:"
openclaw cron get "$CRON_NAME" 2>&1 | head -10 || echo "(cron not found)"
