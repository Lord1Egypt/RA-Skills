#!/bin/bash
# GitCode PR monitor script (repo-parameterized)
# Anonymous-by-default: configure via --owner/--repo or env-managed wrapper.

set -euo pipefail

# ============ 环境变量配置 ============
export PATH="${HOME}/.npm-global/bin:${HOME}/.local/bin:/home/linuxbrew/.linuxbrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# ============ 参数解析 ============
REPO_OWNER="ExampleOrg"
REPO_NAME="example_repo"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --owner)
            REPO_OWNER="$2"; shift 2 ;;
        --repo|--name)
            REPO_NAME="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 [--owner <owner>] [--repo <repo>]"; exit 0 ;;
        *)
            echo "Unknown arg: $1" >&2; exit 2 ;;
    esac
done

STATE_DIR="${OPENCLAW_WORKSPACE:-/home/admin/.openclaw/workspace}/data"
LOG_DIR="${OPENCLAW_WORKSPACE:-/home/admin/.openclaw/workspace}/logs"
TOKEN_FILE="$STATE_DIR/gitcode-token.txt"

STATE_FILE="$STATE_DIR/gitcode-pr-state-${REPO_NAME}.json"
# 兼容旧版本（wifi 仓使用 gitcode-pr-state.json）
LEGACY_STATE_FILE="$STATE_DIR/gitcode-pr-state.json"

LOG_FILE="$LOG_DIR/gitcode-pr-monitor-${REPO_NAME}.log"

# ============ 单实例锁机制（子进程级，按仓隔离） ============
SUB_LOCKFILE="/tmp/gitcode-monitor-sub-${REPO_NAME}.lock"
SUB_PIDFILE="/tmp/gitcode-monitor-sub-${REPO_NAME}.pid"
SUB_MAX_AGE_SECONDS=240  # 4 分钟超时

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$REPO_OWNER/$REPO_NAME] $1" >> "$LOG_FILE"
}

# 清理函数
sub_cleanup() {
    rm -f "$SUB_LOCKFILE" "$SUB_PIDFILE"
    log "清理子进程锁文件，退出"
}

trap sub_cleanup EXIT INT TERM

# ============ 创建必要的目录 ============
mkdir -p "$STATE_DIR" "$LOG_DIR"

log "开始检查 GitCode PR (PID: $$)..."

# 检查是否有旧子进程在运行
if [ -f "$SUB_PIDFILE" ]; then
    OLD_PID=$(cat "$SUB_PIDFILE" 2>/dev/null || true)
    OLD_AGE=$(( $(date +%s) - $(stat -c %Y "$SUB_PIDFILE" 2>/dev/null || echo 0) ))

    if [ -n "${OLD_PID:-}" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        if [ "$OLD_AGE" -gt "$SUB_MAX_AGE_SECONDS" ]; then
            log "检测到超时子进程 (PID: $OLD_PID, 运行时间：${OLD_AGE}s)，终止中..."
            kill -9 "$OLD_PID" 2>/dev/null || true
            sleep 1
            rm -f "$SUB_LOCKFILE" "$SUB_PIDFILE"
        else
            log "另一个子进程正在运行 (PID: $OLD_PID, 已运行：${OLD_AGE}s)，跳过"
            echo "SUB_PROCESS_RUNNING"
            exit 0
        fi
    else
        rm -f "$SUB_LOCKFILE" "$SUB_PIDFILE"
    fi
fi

if [ -f "$SUB_LOCKFILE" ]; then
    log "子进程锁文件存在，跳过"
    echo "SUB_LOCK_EXISTS"
    exit 0
fi

echo "$$" > "$SUB_PIDFILE"
touch "$SUB_LOCKFILE"

# ============ 读取 Token（如果存在） ============
GITCODE_TOKEN=""
if [ -f "$TOKEN_FILE" ]; then
    GITCODE_TOKEN=$(tr -d '\n' < "$TOKEN_FILE")
fi

# ============ 构建 API 请求 ============
API_URL="https://gitcode.com/api/v5/repos/${REPO_OWNER}/${REPO_NAME}/pulls?state=open&sort=created&direction=desc&per_page=5"

if [ -n "$GITCODE_TOKEN" ]; then
    log "使用 Token 认证"
    PR_RESPONSE=$(curl -s -H "PRIVATE-TOKEN: ${GITCODE_TOKEN}" "$API_URL" 2>/dev/null || true)
else
    log "警告：未配置 Token，尝试无认证访问"
    PR_RESPONSE=$(curl -s "$API_URL" 2>/dev/null || true)
fi

if [ -z "$PR_RESPONSE" ]; then
    log "错误：无法获取 PR 列表"
    echo "ERROR:API_FAILED"
    exit 1
fi

# ============ 提取最新的 PR 信息 ============
LATEST_PR_ID=$(echo "$PR_RESPONSE" | jq -r '.[0].number // empty' 2>/dev/null || true)
LATEST_PR_TITLE=$(echo "$PR_RESPONSE" | jq -r '.[0].title // empty' 2>/dev/null || true)
LATEST_PR_USER=$(echo "$PR_RESPONSE" | jq -r '.[0].user.login // empty' 2>/dev/null || true)
LATEST_PR_URL=$(echo "$PR_RESPONSE" | jq -r '.[0].html_url // empty' 2>/dev/null || true)
LATEST_PR_CREATED=$(echo "$PR_RESPONSE" | jq -r '.[0].created_at // empty' 2>/dev/null || true)

if [ -z "${LATEST_PR_ID:-}" ]; then
    log "警告：无法解析 PR 信息"
    echo "NO_PR_FOUND"
    exit 0
fi

log "最新 PR: #${LATEST_PR_ID} - ${LATEST_PR_TITLE}"

# ============ 读取上次记录的 PR ID（兼容旧 state） ============
LAST_CHECKED_PR_ID=""
if [ -f "$STATE_FILE" ]; then
    LAST_CHECKED_PR_ID=$(jq -r '.last_pr_id // empty' "$STATE_FILE" 2>/dev/null || true)
elif [ "$REPO_NAME" = "example_repo" ] && [ -f "$LEGACY_STATE_FILE" ]; then
    # 仅对匿名默认仓名兼容旧 state 占位逻辑
    LAST_CHECKED_PR_ID=$(jq -r '.last_pr_id // empty' "$LEGACY_STATE_FILE" 2>/dev/null || true)
fi

# 如果是第一次运行，记录当前 PR 但不发送通知
if [ -z "${LAST_CHECKED_PR_ID:-}" ]; then
    log "首次运行，记录当前 PR #${LATEST_PR_ID} 但不发送通知"
    echo "{\"last_pr_id\": \"${LATEST_PR_ID}\", \"last_check\": \"$(date -Iseconds)\"}" > "$STATE_FILE"
    echo "FIRST_RUN"
    exit 0
fi

# 检查是否有新的 PR
if [ "$LATEST_PR_ID" != "$LAST_CHECKED_PR_ID" ]; then
    log "发现新 PR! #${LATEST_PR_ID} (上次：${LAST_CHECKED_PR_ID})"

    cat << EOF
NEW_PR_DETECTED
OWNER: ${REPO_OWNER}
REPO: ${REPO_NAME}
ID: ${LATEST_PR_ID}
TITLE: ${LATEST_PR_TITLE}
AUTHOR: ${LATEST_PR_USER}
URL: ${LATEST_PR_URL}
CREATED: ${LATEST_PR_CREATED}
EOF

    echo "{\"last_pr_id\": \"${LATEST_PR_ID}\", \"last_check\": \"$(date -Iseconds)\"}" > "$STATE_FILE"
    log "状态已更新"
else
    log "没有新 PR"
    echo "NO_NEW_PR"
fi

exit 0
