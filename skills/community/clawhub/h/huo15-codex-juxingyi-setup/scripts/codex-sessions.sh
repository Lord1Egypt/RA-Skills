#!/usr/bin/env bash
# 列出/查看 Codex 会话历史
# 用法:
#   bash codex-sessions.sh --limit 10        列出最近 10 条会话
#   bash codex-sessions.sh --detail <id>     查看某条会话详情
#   bash codex-sessions.sh --search "关键词"  搜索会话
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SESSION_INDEX="$CODEX_HOME/session_index.jsonl"
SESSIONS_DIR="$CODEX_HOME/sessions"

LIMIT=10
DETAIL=""
SEARCH=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --limit) LIMIT="$2"; shift 2 ;;
    --detail) DETAIL="$2"; shift 2 ;;
    --search) SEARCH="$2"; shift 2 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

# --- 查看会话详情 ---
if [ -n "$DETAIL" ]; then
  echo "=== 会话详情: $DETAIL ==="
  echo ""

  # 查找对应的 rollout 文件
  ROLLOUT_FILE=$(find "$SESSIONS_DIR" -name "*$DETAIL*" -name "*.jsonl" 2>/dev/null | head -1)
  if [ -z "$ROLLOUT_FILE" ]; then
    echo "未找到会话文件: $DETAIL"
    echo "提示: session ID 格式如 019f49f8-8966-7621-9801-809eeb2bedc1"
    exit 1
  fi

  echo "文件: $ROLLOUT_FILE"
  echo ""

  if ! command -v jq &>/dev/null; then
    echo "需要 jq 来解析会话内容。安装: brew install jq"
    echo "原始内容:"
    cat "$ROLLOUT_FILE"
    exit 0
  fi

  # 解析会话内容
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    TYPE=$(echo "$line" | jq -r '.type' 2>/dev/null || echo "")
    PAYLOAD_TYPE=$(echo "$line" | jq -r '.payload.type' 2>/dev/null || echo "")
    TIMESTAMP=$(echo "$line" | jq -r '.timestamp[0:19]' 2>/dev/null || echo "")

    case "$TYPE" in
      session_meta)
        CWD=$(echo "$line" | jq -r '.payload.cwd' 2>/dev/null || echo "")
        ORIGINATOR=$(echo "$line" | jq -r '.payload.originator' 2>/dev/null || echo "")
        VERSION=$(echo "$line" | jq -r '.payload.cli_version' 2>/dev/null || echo "")
        MODEL_PROVIDER=$(echo "$line" | jq -r '.payload.model_provider' 2>/dev/null || echo "")
        echo "--- 会话元信息 ---"
        echo "  时间: $TIMESTAMP"
        echo "  工作目录: $CWD"
        echo "  来源: $ORIGINATOR (v$VERSION)"
        echo "  Provider: $MODEL_PROVIDER"
        echo ""
        ;;
      event_msg)
        case "$PAYLOAD_TYPE" in
          user_message)
            MSG=$(echo "$line" | jq -r '.payload.message' 2>/dev/null || echo "")
            echo "[$TIMESTAMP] 用户:"
            echo "$MSG" | head -20
            echo ""
            ;;
          agent_message)
            MSG=$(echo "$line" | jq -r '.payload.message' 2>/dev/null || echo "")
            echo "[$TIMESTAMP] Codex:"
            echo "$MSG" | head -20
            echo ""
            ;;
          task_started)
            echo "[$TIMESTAMP] --- 任务开始 ---"
            ;;
          task_completed)
            echo "[$TIMESTAMP] --- 任务完成 ---"
            echo ""
            ;;
        esac
        ;;
      response_item)
        case "$PAYLOAD_TYPE" in
          function_call)
            FUNC_NAME=$(echo "$line" | jq -r '.payload.name' 2>/dev/null || echo "")
            FUNC_ARGS=$(echo "$line" | jq -r '.payload.arguments' 2>/dev/null | head -c 200 || echo "")
            echo "[$TIMESTAMP] [工具调用] $FUNC_NAME"
            echo "  参数: $FUNC_ARGS"
            ;;
          function_call_output)
            OUTPUT=$(echo "$line" | jq -r '.payload.output' 2>/dev/null | head -c 200 || echo "")
            echo "[$TIMESTAMP] [工具结果] $OUTPUT"
            ;;
        esac
        ;;
    esac
  done < "$ROLLOUT_FILE"

  exit 0
fi

# --- 列出会话 ---
echo "=== Codex 会话列表 ==="
echo ""

if [ ! -f "$SESSION_INDEX" ]; then
  echo "无会话索引文件: $SESSION_INDEX"
  echo "提示: 先使用 Codex 创建一次会话"
  exit 0
fi

if ! command -v jq &>/dev/null; then
  echo "需要 jq 来解析会话列表。安装: brew install jq"
  echo "原始内容:"
  tail -"$LIMIT" "$SESSION_INDEX"
  exit 0
fi

if [ -n "$SEARCH" ]; then
  echo "搜索: \"$SEARCH\""
  echo ""
  grep -i "$SEARCH" "$SESSION_INDEX" | tail -"$LIMIT" | jq -r '. | "\(.updated_at[0:19])  \(.id[0:8])  \(.thread_name[0:70])"' 2>/dev/null
else
  echo "最近 $LIMIT 条会话:"
  echo ""
  echo "时间                  ID(前8位)  名称"
  echo "----                  --------  ----"
  tail -"$LIMIT" "$SESSION_INDEX" | jq -r '. | "\(.updated_at[0:19])  \(.id[0:8])  \(.thread_name[0:70])"' 2>/dev/null
fi

echo ""
echo "查看详情: bash codex-sessions.sh --detail <session_id>"
