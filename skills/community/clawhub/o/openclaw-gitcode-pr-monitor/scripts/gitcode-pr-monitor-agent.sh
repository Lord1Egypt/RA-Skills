#!/bin/bash
# GitCode PR monitor + auto review (multi-repo)
#
# Anonymous-by-default skill package:
# - Default repo names are placeholders (ExampleOrg/example_repo_1 + example_repo_2)
# - Configure via env vars: REPO_OWNER, REPOS_CSV
# - Default notification channels: DingTalk + WeCom (configure via TARGET_DINGTALK / TARGET_WECOM)

set -euo pipefail

# ============ 环境变量配置 ============
OPENCLAW_CMD="${OPENCLAW_CMD:-$(command -v openclaw || true)}"

if [ -z "$OPENCLAW_CMD" ] || [ ! -x "$OPENCLAW_CMD" ]; then
    echo "❌ openclaw 可执行文件不存在，请设置 OPENCLAW_CMD 或确保 openclaw 在 PATH 中" >&2
    exit 1
fi

export PNPM_HOME="${PNPM_HOME:-${HOME}/.local/share/pnpm}"
export PATH="$PNPM_HOME:${HOME}/.npm-global/bin:${HOME}/.local/bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

SCRIPT_DIR="$(dirname "$0")"
MONITOR_SCRIPT="$SCRIPT_DIR/monitor-gitcode-pr.sh"
REVIEW_SCRIPT="$SCRIPT_DIR/code-review-robust.sh"
COMMENT_SCRIPT="$SCRIPT_DIR/submit-pr-comment.sh"

WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-${HOME}/.openclaw/workspace}"
ALERT_LOG="$WORKSPACE_DIR/logs/gitcode-pr-alerts.log"

# ============ 配置：监控仓库列表（建议用 env 覆盖） ============
REPO_OWNER="${REPO_OWNER:-ExampleOrg}"

REPOS_DEFAULT=(
  "example_repo_1"
  "example_repo_2"
)

if [ -n "${REPOS_CSV:-}" ]; then
  IFS=',' read -r -a REPOS <<< "$REPOS_CSV"
else
  REPOS=("${REPOS_DEFAULT[@]}")
fi

# ============ 通知目标（必须配置） ============
TARGET_DINGTALK="${TARGET_DINGTALK:-CHANGE_ME_DINGTALK}"
TARGET_WECOM="${TARGET_WECOM:-CHANGE_ME_WECOM}"

send_notify_started() {
  local repo_owner="$1" repo_name="$2" pr_id="$3" pr_title="$4" pr_author="$5" pr_created="$6" pr_url="$7"

  "$OPENCLAW_CMD" message send \
    --channel dingtalk \
    --target "$TARGET_DINGTALK" \
    --message "🔔 GitCode 新 PR 提醒\n\n📦 仓库：${repo_owner}/${repo_name}\n🔢 PR #${pr_id}\n📝 标题：${pr_title}\n👤 作者：${pr_author}\n🕐 时间：${pr_created}\n\n🔗 查看：${pr_url}\n\n---\n\n🔍 **代码审查已启动**（隔离会话按天复用），预计 3-5 分钟完成..." \
    2>&1 | tee -a "$ALERT_LOG"

  "$OPENCLAW_CMD" message send \
    --channel wecom-app \
    --target "$TARGET_WECOM" \
    --message "🔔 GitCode 新 PR\n\n仓库：${repo_owner}/${repo_name}\nPR #${pr_id}\n标题：${pr_title}\n作者：${pr_author}\n时间：${pr_created}\n链接：${pr_url}\n\n代码审查已启动（预计 3-5 分钟）" \
    2>&1 | tee -a "$ALERT_LOG"
}

send_notify_finished() {
  local repo_owner="$1" repo_name="$2" pr_id="$3" pr_title="$4" pr_author="$5" pr_created="$6" pr_url="$7" review_file="$8" blocker="$9" major="${10}" minor="${11}" summary="${12}" comment_status_text="${13}"

  "$OPENCLAW_CMD" message send \
    --channel dingtalk \
    --target "$TARGET_DINGTALK" \
    --message "🔔 GitCode 新 PR 提醒\n\n📦 仓库：${repo_owner}/${repo_name}\n🔢 PR #${pr_id}\n📝 标题：${pr_title}\n👤 作者：${pr_author}\n🕐 时间：${pr_created}\n\n🔗 查看：${pr_url}\n\n---\n\n🔍 **代码审查已完成！**\n\n📊 问题统计：\n- 🚨 严重问题：${blocker}\n- ⚠️ 主要问题：${major}\n- 💡 建议改进：${minor}\n\n${summary}\n\n${comment_status_text}\n\n📎 完整审查报告见下方附件。" \
    2>&1 | tee -a "$ALERT_LOG"

  "$OPENCLAW_CMD" message send \
    --channel dingtalk \
    --target "$TARGET_DINGTALK" \
    --media "$review_file" \
    --message "📄 ${repo_owner}/${repo_name} PR #${pr_id} 代码审查报告\n\n审查完成时间：$(date '+%Y-%m-%d %H:%M:%S')" \
    2>&1 | tee -a "$ALERT_LOG"

  "$OPENCLAW_CMD" message send \
    --channel wecom-app \
    --target "$TARGET_WECOM" \
    --message "✅ 代码审查完成\n\n仓库：${repo_owner}/${repo_name}\nPR #${pr_id}\n标题：${pr_title}\n\n问题统计：严重${blocker}/主要${major}/建议${minor}\n\n${comment_status_text}\n\n链接：${pr_url}" \
    2>&1 | tee -a "$ALERT_LOG"

  # WeCom 也发送报告附件（如果通道支持 media）
  "$OPENCLAW_CMD" message send \
    --channel wecom-app \
    --target "$TARGET_WECOM" \
    --media "$review_file" \
    --message "📎 ${repo_owner}/${repo_name} PR #${pr_id} 审查报告" \
    2>&1 | tee -a "$ALERT_LOG" || true
}

# ============ 单实例锁 + 超时保护机制（全局） ============
LOCKFILE="/tmp/gitcode-monitor.lock"
PIDFILE="/tmp/gitcode-monitor.pid"
MAX_AGE_SECONDS=1800

cleanup() {
    rm -f "$LOCKFILE" "$PIDFILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 清理锁文件，退出" >> "$ALERT_LOG"
}
trap cleanup EXIT INT TERM

if [ -f "$PIDFILE" ]; then
    OLD_PID=$(cat "$PIDFILE" 2>/dev/null || true)
    OLD_AGE=$(( $(date +%s) - $(stat -c %Y "$PIDFILE" 2>/dev/null || echo 0) ))

    if [ -n "${OLD_PID:-}" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        if [ "$OLD_AGE" -gt "$MAX_AGE_SECONDS" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到超时进程 (PID: $OLD_PID, 运行时间：${OLD_AGE}s)，终止中..." >> "$ALERT_LOG"
            kill -9 "$OLD_PID" 2>/dev/null || true
            sleep 1
            rm -f "$LOCKFILE" "$PIDFILE"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 另一个实例正在运行 (PID: $OLD_PID, 已运行：${OLD_AGE}s)，跳过本次执行" >> "$ALERT_LOG"
            exit 0
        fi
    else
        rm -f "$LOCKFILE" "$PIDFILE"
    fi
fi

if [ -f "$LOCKFILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 锁文件存在，跳过本次执行" >> "$ALERT_LOG"
    exit 0
fi

CURRENT_PID=$$
echo "$CURRENT_PID" > "$PIDFILE"
touch "$LOCKFILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 启动监控 (PID: $CURRENT_PID)" >> "$ALERT_LOG"

# ============ 主流程：逐仓监控 ============
for REPO_NAME in "${REPOS[@]}"; do
    RESULT=$("$MONITOR_SCRIPT" --owner "$REPO_OWNER" --repo "$REPO_NAME" || true)

    if echo "$RESULT" | grep -q "NEW_PR_DETECTED"; then
        PR_ID=$(echo "$RESULT" | grep "^ID:" | cut -d' ' -f2)
        PR_TITLE=$(echo "$RESULT" | grep "^TITLE:" | cut -d' ' -f2-)
        PR_AUTHOR=$(echo "$RESULT" | grep "^AUTHOR:" | cut -d' ' -f2)
        PR_URL=$(echo "$RESULT" | grep "^URL:" | cut -d' ' -f2)
        PR_CREATED=$(echo "$RESULT" | grep "^CREATED:" | cut -d' ' -f2-)

        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到新 PR ${REPO_OWNER}/${REPO_NAME} #${PR_ID}" >> "$ALERT_LOG"

        REVIEW_FILE="$WORKSPACE_DIR/reviews/$(date +%Y-%m)/PR-${PR_ID}-${REPO_NAME}.md"

        send_notify_started "$REPO_OWNER" "$REPO_NAME" "$PR_ID" "$PR_TITLE" "$PR_AUTHOR" "$PR_CREATED" "$PR_URL"

        REVIEW_STATUS=0
        REVIEW_OUTPUT=$("$REVIEW_SCRIPT" "$PR_ID" "$PR_URL" "$REPO_OWNER" "$REPO_NAME" 2>&1) || REVIEW_STATUS=$?
        echo "$REVIEW_OUTPUT" >> "$ALERT_LOG"

        if [ $REVIEW_STATUS -eq 0 ] && [ -f "$REVIEW_FILE" ] && [ -s "$REVIEW_FILE" ]; then
            SUMMARY=$(grep -A5 "总体评分" "$REVIEW_FILE" 2>/dev/null | head -6 || echo "审查完成")
            BLOCKER_COUNT=$(grep "🚨 严重问题" "$REVIEW_FILE" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "0")
            MAJOR_COUNT=$(grep "⚠️ 主要问题" "$REVIEW_FILE" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "0")
            MINOR_COUNT=$(grep "💡 建议改进" "$REVIEW_FILE" 2>/dev/null | grep -oE '[0-9]+' | head -1 || echo "0")

            COMMENT_OUTPUT=$("$COMMENT_SCRIPT" "$PR_ID" "$REVIEW_FILE" "$REPO_OWNER" "$REPO_NAME" 2>&1)
            COMMENT_STATUS=$?
            echo "$COMMENT_OUTPUT" >> "$ALERT_LOG"

            if [ $COMMENT_STATUS -eq 0 ]; then
                COMMENT_STATUS_TEXT="✅ 审查评论已提交到 PR 页面"
            else
                COMMENT_STATUS_TEXT="⚠️ 评论提交失败（见日志）"
            fi

            send_notify_finished "$REPO_OWNER" "$REPO_NAME" "$PR_ID" "$PR_TITLE" "$PR_AUTHOR" "$PR_CREATED" "$PR_URL" \
              "$REVIEW_FILE" "$BLOCKER_COUNT" "$MAJOR_COUNT" "$MINOR_COUNT" "$SUMMARY" "$COMMENT_STATUS_TEXT"
        else
            "$OPENCLAW_CMD" message send \
              --channel dingtalk \
              --target "$TARGET_DINGTALK" \
              --message "⚠️ GitCode PR 审查失败\n\n📦 仓库：${REPO_OWNER}/${REPO_NAME}\n🔢 PR #${PR_ID}\n📝 标题：${PR_TITLE}\n\n🔗 查看 PR: ${PR_URL}" \
              2>&1 | tee -a "$ALERT_LOG"

            "$OPENCLAW_CMD" message send \
              --channel wecom-app \
              --target "$TARGET_WECOM" \
              --message "⚠️ PR 审查失败\n\n仓库：${REPO_OWNER}/${REPO_NAME}\nPR #${PR_ID}\n标题：${PR_TITLE}\n\n链接：${PR_URL}" \
              2>&1 | tee -a "$ALERT_LOG" || true
        fi

    elif echo "$RESULT" | grep -q "FIRST_RUN"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️ ${REPO_OWNER}/${REPO_NAME} 首次运行已记录当前 PR 状态（不通知）" >> "$ALERT_LOG"
    elif echo "$RESULT" | grep -q "NO_NEW_PR"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ ${REPO_OWNER}/${REPO_NAME} 检查完成，无新 PR" >> "$ALERT_LOG"
    elif echo "$RESULT" | grep -q "ERROR"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ ${REPO_OWNER}/${REPO_NAME} 监控出错：$RESULT" >> "$ALERT_LOG"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ? ${REPO_OWNER}/${REPO_NAME} 未知状态：$RESULT" >> "$ALERT_LOG"
    fi
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 监控周期结束" >> "$ALERT_LOG"
