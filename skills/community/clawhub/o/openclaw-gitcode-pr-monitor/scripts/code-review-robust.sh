#!/bin/bash
# GitCode PR 代码审查脚本 - 增强版（支持多仓参数化）
# 通过 OpenClaw agent + 固定隔离会话（按天轮换）进行审查

# ============ 环境变量配置 ============
export PATH="${HOME}/.npm-global/bin:${HOME}/.local/bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

set -euo pipefail

PR_ID="$1"
PR_URL="$2"
REPO_OWNER="${3:-ExampleOrg}"
REPO_NAME="${4:-example_repo}"

# openclaw CLI 路径（优先使用环境变量或 PATH）
OPENCLAW_CMD="${OPENCLAW_CMD:-$(command -v openclaw || true)}"
if [ -z "$OPENCLAW_CMD" ] || [ ! -x "$OPENCLAW_CMD" ]; then
    echo "❌ openclaw 可执行文件不存在，请设置 OPENCLAW_CMD 或确保 openclaw 在 PATH 中" >&2
    exit 1
fi

# ✅ 固定隔离会话（按仓 + 按天轮换）：避免每次 cron 都起新会话（提升缓存命中率/减少冷启动），同时防止会话历史无限增长
SESSION_ID="gitcode-pr-review-${REPO_OWNER}-${REPO_NAME}-$(date +%Y%m%d)"

# 配置参数
MAX_RETRIES=3
RETRY_DELAY=10
WAIT_INTERVAL=10
MAX_WAIT_CYCLES=60  # 最多等待 10 分钟 (60 * 10 秒)

WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}"

# 创建审查报告目录
REVIEW_DIR="$WORKSPACE_DIR/reviews/$(date +%Y-%m)"
mkdir -p "$REVIEW_DIR"

# 审查报告输出文件
REVIEW_FILE="$REVIEW_DIR/PR-${PR_ID}-${REPO_NAME}.md"
LOG_FILE="$WORKSPACE_DIR/logs/code-review-${REPO_NAME}-${PR_ID}.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$REPO_OWNER/$REPO_NAME] $1" | tee -a "$LOG_FILE"
}

log "🔍 开始审查 PR #${PR_ID}..."
log "📁 报告将保存到：$REVIEW_FILE"
log "🧩 使用固定隔离会话：$SESSION_ID"

# 清理旧报告（如果有）
rm -f "$REVIEW_FILE"

# 构建审查任务
TASK="你是一个专业的代码审查专家。你将反复收到不同 PR 的审查请求，请始终以【本次消息】里的 PR 信息为准，忽略历史 PR 上下文。

请审查以下 GitCode PR：

PR 信息：
- PR 号：${PR_ID}
- 仓库：${REPO_OWNER}/${REPO_NAME}
- URL: ${PR_URL}

审查要求：
1. 使用 GitCode API 获取 PR 的变更内容（diff）
   - API: https://gitcode.com/api/v5/repos/${REPO_OWNER}/${REPO_NAME}/pulls/${PR_ID}/files
   - Token 路径：$WORKSPACE_DIR/data/gitcode-token.txt
2. 分析代码质量问题（安全漏洞、内存问题、编码规范等）
3. 生成详细的 Markdown 审查报告
4. 报告必须保存到：${REVIEW_FILE}

审查报告格式要求：
- 使用小图标标记问题级别（🚨严重 ⚠️主要 💡建议）
- 每个问题包含：位置、描述、影响、修复建议（含修改后代码）
- 给出总体评分和建议操作
- 不要添加 AI 相关字样

请直接开始审查，完成后告诉我。"

# 启动审查（重试机制）
RETRY_COUNT=0
AGENT_SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$AGENT_SUCCESS" = "false" ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))

    log "📤 启动审查隔离会话 (尝试 ${RETRY_COUNT}/${MAX_RETRIES})..."

    AGENT_OUTPUT=$("$OPENCLAW_CMD" agent \
        --agent main \
        --session-id "$SESSION_ID" \
        --message "$TASK" \
        --timeout 600 \
        --thinking high \
        2>&1) || true

    log "Agent 执行输出：$AGENT_OUTPUT"

    if echo "$AGENT_OUTPUT" | grep -qi "error\|failed\|command not found"; then
        log "⚠️ Agent 执行可能失败，等待 ${RETRY_DELAY} 秒后重试..."
        sleep $RETRY_DELAY
    else
        log "✅ Agent 执行完成"
        AGENT_SUCCESS=true
    fi
done

if [ "$AGENT_SUCCESS" = "false" ]; then
    log "❌ 隔离会话执行失败，已尝试 ${MAX_RETRIES} 次"
    exit 1
fi

# 等待报告生成
log "⏳ 等待审查报告生成..."
CYCLE=0
REPORT_GENERATED=false

while [ $CYCLE -lt $MAX_WAIT_CYCLES ]; do
    CYCLE=$((CYCLE + 1))

    if [ -f "$REVIEW_FILE" ] && [ -s "$REVIEW_FILE" ]; then
        if head -1 "$REVIEW_FILE" | grep -q "^#"; then
            log "✅ 审查报告已生成！ (${CYCLE} 个周期)"
            REPORT_GENERATED=true
            break
        else
            log "⚠️ 报告文件存在但内容不完整，继续等待..."
        fi
    fi

    if [ $((CYCLE % 6)) -eq 0 ]; then
        log "⏳ 等待中... (${CYCLE}/${MAX_WAIT_CYCLES})"
    fi

    sleep $WAIT_INTERVAL
done

if [ "$REPORT_GENERATED" = "true" ]; then
    log "📁 完整报告：$REVIEW_FILE"
    log "✅ 审查完成！"
    exit 0
else
    log "❌ 审查报告未生成，已等待 $((MAX_WAIT_CYCLES * WAIT_INTERVAL)) 秒"
    exit 1
fi
