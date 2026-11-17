#!/usr/bin/env bash
# 聚合 Codex 全部上下文，供 Agent 一次性读取
# 用法: bash codex-context.sh [--sessions N]  (N=包含最近几条会话详情，默认3)
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CONFIG_FILE="$CODEX_HOME/config.toml"
SESSION_INDEX="$CODEX_HOME/session_index.jsonl"
SESSIONS_DIR="$CODEX_HOME/sessions"
SESSION_DETAIL_COUNT=3

while [[ $# -gt 0 ]]; do
  case $1 in
    --sessions) SESSION_DETAIL_COUNT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "=========================================="
echo "Codex 上下文报告"
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# === 1. 配置信息 ===
echo "## 1. 配置信息"
echo ""
if [ -f "$CONFIG_FILE" ]; then
  echo '```toml'
  cat "$CONFIG_FILE"
  echo '```'
else
  echo "(配置文件不存在)"
fi
echo ""

# === 2. 安装状态 ===
echo "## 2. 安装状态"
echo ""
echo "| 组件 | 状态 |"
echo "|---|---|"
if [ -d "/Applications/ChatGPT.app" ]; then
  VER=$(defaults read "/Applications/ChatGPT.app/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null || echo "?")
  echo "| ChatGPT 桌面版 | 已安装 (v$VER) |"
else
  echo "| ChatGPT 桌面版 | 未安装 |"
fi
if command -v codex &>/dev/null; then
  echo "| Codex CLI | 已安装 ($(codex --version 2>/dev/null || echo '?')) |"
else
  echo "| Codex CLI | 未安装 |"
fi
if command -v jq &>/dev/null; then
  echo "| jq | 已安装 |"
else
  echo "| jq | 未安装 |"
fi
echo ""

# === 3. 活跃项目 ===
echo "## 3. 活跃项目"
echo ""
if [ -f "$CONFIG_FILE" ]; then
  PROJECTS=$(grep -E '^\[projects\.' "$CONFIG_FILE" 2>/dev/null | sed 's/\[projects\.\(.*\)\]/\1/' || echo "")
  if [ -n "$PROJECTS" ]; then
    echo "| 项目路径 | 信任级别 |"
    echo "|---|---|"
    echo "$PROJECTS" | while read -r proj; do
      TRUST=$(grep -A1 "^\[projects\.$proj\]" "$CONFIG_FILE" 2>/dev/null | grep 'trust_level' | sed 's/.*= *"\(.*\)".*/\1/' || echo "")
      echo "| \`$proj\` | $TRUST |"
    done
  else
    echo "(无配置项目)"
  fi
fi
echo ""

# === 4. 会话列表 ===
echo "## 4. 会话列表"
echo ""
if [ -f "$SESSION_INDEX" ] && command -v jq &>/dev/null; then
  SESSION_COUNT=$(wc -l < "$SESSION_INDEX" | tr -d ' ')
  echo "总会话数: $SESSION_COUNT"
  echo ""
  echo "### 最近 $SESSION_DETAIL_COUNT 条会话"
  echo ""
  tail -"$SESSION_DETAIL_COUNT" "$SESSION_INDEX" | jq -r '. | "#### \(.thread_name[0:60])\n- ID: \(.id)\n- 时间: \(.updated_at[0:19])\n"' 2>/dev/null
else
  echo "(无会话记录或 jq 未安装)"
fi
echo ""

# === 5. 最近会话内容摘要 ===
echo "## 5. 最近会话内容摘要"
echo ""
if [ -d "$SESSIONS_DIR" ] && command -v jq &>/dev/null; then
  # 找到最近 N 个 rollout 文件
  RECENT_FILES=$(find "$SESSIONS_DIR" -name "rollout-*.jsonl" -type f 2>/dev/null | sort -r | head -"$SESSION_DETAIL_COUNT")
  if [ -n "$RECENT_FILES" ]; then
    for FILE in $RECENT_FILES; do
      echo "### $(basename "$FILE")"
      echo ""

      # 提取会话元信息
      META=$(head -1 "$FILE" 2>/dev/null || echo "")
      if [ -n "$META" ]; then
        CWD=$(echo "$META" | jq -r '.payload.cwd // "未知"' 2>/dev/null || echo "未知")
        ORIGINATOR=$(echo "$META" | jq -r '.payload.originator // "未知"' 2>/dev/null || echo "未知")
        echo "- 工作目录: \`$CWD\`"
        echo "- 来源: $ORIGINATOR"
      fi

      # 提取用户消息（前3条）
      echo "- 用户消息摘要:"
      grep '"type":"user_message"' "$FILE" 2>/dev/null | head -3 | jq -r '. | "  - \(.payload.message[0:100])"' 2>/dev/null || echo "  (无)"

      # 提取 Agent 消息（前3条）
      echo "- Codex 回复摘要:"
      grep '"type":"agent_message"' "$FILE" 2>/dev/null | head -3 | jq -r '. | "  - \(.payload.message[0:100])"' 2>/dev/null || echo "  (无)"

      # 统计工具调用
      TOOL_COUNT=$(grep '"type":"function_call"' "$FILE" 2>/dev/null | wc -l | tr -d ' ')
      echo "- 工具调用次数: $TOOL_COUNT"

      echo ""
    done
  else
    echo "(无会话文件)"
  fi
else
  echo "(无会话目录或 jq 未安装)"
fi
echo ""

# === 6. 网关连通性 ===
echo "## 6. 网关连通性"
echo ""
if [ -f "$CONFIG_FILE" ]; then
  BASE_URL=$(grep -E '^openai_base_url' "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "")
  if [ -n "$BASE_URL" ]; then
    echo "网关地址: $BASE_URL"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/models" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "200" ]; then
      echo "连通状态: 正常 (HTTP $HTTP_CODE)"
    else
      echo "连通状态: 异常 (HTTP $HTTP_CODE)"
    fi
  fi
fi
echo ""

echo "=========================================="
echo "上下文报告结束"
echo "=========================================="
