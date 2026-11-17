#!/bin/bash
# post-exec-log.sh — 执行后日志记录
# 从 stdin 读取 JSON 事件数据，记录执行结果到审计日志

set -euo pipefail

# 读取 stdin 事件数据
EVENT_DATA=$(cat)

# 提取字段
if command -v jq &>/dev/null; then
    COMMAND=$(echo "$EVENT_DATA" | jq -r '.command // "unknown"')
    EXIT_CODE=$(echo "$EVENT_DATA" | jq -r '.exitCode // -1')
    DURATION=$(echo "$EVENT_DATA" | jq -r '.duration // 0')
    STDERR=$(echo "$EVENT_DATA" | jq -r '.stderr // ""' | head -c 200)
else
    COMMAND=$(echo "$EVENT_DATA" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
    EXIT_CODE=$(echo "$EVENT_DATA" | grep -o '"exitCode"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | sed 's/.*: *//')
    DURATION=$(echo "$EVENT_DATA" | grep -o '"duration"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | sed 's/.*: *//')
    STDERR=""
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# 确定日志目录
WORKSPACE="${OPENCLAW_WORKSPACE:-.}"
LOG_DIR="$WORKSPACE/memory"
LOG_FILE="$LOG_DIR/hook-audit.log"

# 确保目录存在
mkdir -p "$LOG_DIR" 2>/dev/null || true

# 判断执行状态
if [[ "$EXIT_CODE" == "0" ]]; then
    STATUS="success"
    DECISION="allow"
    MESSAGE="命令执行成功 (耗时 ${DURATION}ms)"
elif [[ "$EXIT_CODE" == "-1" ]]; then
    STATUS="unknown"
    DECISION="warn"
    MESSAGE="命令执行状态未知"
else
    STATUS="failed"
    DECISION="warn"
    MESSAGE="命令执行失败 (exit=$EXIT_CODE, 耗时 ${DURATION}ms)"
    if [[ -n "$STDERR" ]]; then
        MESSAGE+=": ${STDERR:0:100}"
    fi
fi

# 写入审计日志
echo "[$TIMESTAMP] [PostExec] [$DECISION] [$STATUS] cmd=$COMMAND exit=$EXIT_CODE duration=${DURATION}ms" >> "$LOG_FILE" 2>/dev/null || true

# 输出 JSON 结果
cat <<EOF
{
  "decision": "$DECISION",
  "message": "$MESSAGE",
  "matched_rules": [],
  "timestamp": "$TIMESTAMP"
}
EOF
