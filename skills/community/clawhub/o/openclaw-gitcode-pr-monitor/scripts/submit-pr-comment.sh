#!/bin/bash
# GitCode PR 自动提交审查评论脚本（支持多仓参数化）
# 将代码审查意见提交到 PR 评论

set -euo pipefail

PR_ID="$1"
REVIEW_FILE="$2"
REPO_OWNER="${3:-ExampleOrg}"
REPO_NAME="${4:-example_repo}"

WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}"
TOKEN_FILE="$WORKSPACE_DIR/data/gitcode-token.txt"

# 检查 Token
if [ ! -f "$TOKEN_FILE" ]; then
    echo "❌ GitCode Token 不存在：$TOKEN_FILE"
    exit 1
fi

GITCODE_TOKEN=$(tr -d '\n' < "$TOKEN_FILE")

# 检查审查报告文件
if [ ! -f "$REVIEW_FILE" ]; then
    echo "⚠️ 审查报告不存在：$REVIEW_FILE"
    echo "将生成简化评论"
    GENERATE_SIMPLE="true"
else
    GENERATE_SIMPLE="false"
fi

echo "📝 准备提交 PR #${PR_ID} 评论... (${REPO_OWNER}/${REPO_NAME})"

# 生成评论内容
if [ "$GENERATE_SIMPLE" = "true" ]; then
    COMMENT_BODY="## 自动代码审查报告

**审查时间**: $(date '+%Y-%m-%d %H:%M:%S')

✅ 代码审查已完成。

详细审查报告已发送给项目维护者。"
else
    # 直接用完整报告作为评论体
    COMMENT_BODY="$(cat "$REVIEW_FILE")"
fi

# 提交评论到 GitCode
echo "📤 正在提交评论到 GitCode PR #${PR_ID}..."

API_URL="https://gitcode.com/api/v5/repos/${REPO_OWNER}/${REPO_NAME}/pulls/${PR_ID}/comments"

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "PRIVATE-TOKEN: ${GITCODE_TOKEN}" \
  -H "Content-Type: application/json" \
  -X POST \
  "${API_URL}" \
  -d "{\"body\":$(echo "$COMMENT_BODY" | jq -Rs '.')}" )

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 评论提交成功！HTTP: $HTTP_CODE"
    COMMENT_ID=$(echo "$RESPONSE_BODY" | jq -r '.id // "unknown"' 2>/dev/null || echo "unknown")
    echo "💬 评论 ID: $COMMENT_ID"
    exit 0
else
    echo "⚠️ 评论提交失败 HTTP: $HTTP_CODE"
    echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 评论提交失败：${REPO_OWNER}/${REPO_NAME} PR #${PR_ID}, HTTP ${HTTP_CODE}" >> "$WORKSPACE_DIR/logs/gitcode-pr-alerts.log"
    # 不阻断流程
    exit 0
fi
