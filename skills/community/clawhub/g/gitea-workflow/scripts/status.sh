#!/usr/bin/env bash
# 查看 gitea-workflow 当前状态
# 1. cron 状态 (enabled? schedule? last run?)
# 2. 自己仓库的 open issue 数量
# 3. 上次群消息时间

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

echo "=== gitea-workflow status ==="
echo "agent:   $AGENT"
echo "cron:    $CRON_NAME"
echo ""

echo "--- cron state ---"
openclaw cron get "$CRON_NAME" 2>&1 | head -15 || echo "(cron not configured - see references/cron-setup.md)"
echo ""

echo "--- open issues in my repo ---"
# 决定自己的 repo(根据 agent 名)
# programmer -> <your-org>/<your-repo>
# designer   -> <your-org>/<your-repo>-designer
# tester     -> <your-org>/<your-repo>-qa
# artist     -> (待定)
case "$AGENT" in
    programmer) REPO="<your-org>/<your-repo>" ;;
    designer)   REPO="<your-org>/<your-repo>-designer" ;;
    tester)     REPO="<your-org>/<your-repo>-qa" ;;
    artist)     REPO="(待定)" ;;
    producer)   REPO="(跨所有仓库)" ;;
    *)          REPO="(未配置)" ;;
esac
echo "repo:    $REPO"

# 如果有 Gitea token, 拉一下 issue 数量
GITEA_TOKEN_FILE="${GITEA_TOKEN_FILE:-$HOME/.config/gitea/token}"
if [ -f "$GITEA_TOKEN_FILE" ] && [ "$REPO" != "(待定)" ] && [ "$REPO" != "(跨所有仓库)" ] && [ "$REPO" != "(未配置)" ]; then
    TOKEN=$(cat "$GITEA_TOKEN_FILE")
    open_count=$(curl -s -H "Authorization: token $TOKEN" \
        "http://127.0.0.1:3000/api/v1/repos/${REPO}/issues?state=open&limit=50" 2>/dev/null \
        | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
    echo "open:    $open_count issues"
else
    echo "open:    (no Gitea token at $GITEA_TOKEN_FILE)"
fi
echo ""

echo "--- last loop run ---"
# 上次唤醒时间可从 cron state 读
echo "(see cron lastRunAtMs above)"
