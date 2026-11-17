#!/usr/bin/env bash
# 查看 Codex 当前状态
# 用法: bash codex-status.sh
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CONFIG_FILE="$CODEX_HOME/config.toml"

echo "=== Codex 当前状态 ==="
echo ""

# --- 配置信息 ---
echo "[配置]"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "  配置文件不存在: $CONFIG_FILE"
  echo "  请先运行 configure.sh"
  exit 1
fi

MODEL=$(grep -E '^model ' "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "未设置")
PROVIDER=$(grep -E '^model_provider' "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "未设置")
BASE_URL=$(grep -E '^openai_base_url' "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "未设置")
EFFORT=$(grep -E '^model_reasoning_effort' "$CONFIG_FILE" 2>/dev/null | head -1 | sed 's/.*= *"\(.*\)".*/\1/' || echo "默认")

echo "  模型:     $MODEL"
echo "  Provider: $PROVIDER"
echo "  Base URL: $BASE_URL"
echo "  思考力度: $EFFORT"
echo ""

# --- 活跃项目 ---
echo "[活跃项目]"
PROJECTS=$(grep -E '^\[projects\.' "$CONFIG_FILE" 2>/dev/null | sed 's/\[projects\.\(.*\)\]/\1/' || echo "")
if [ -n "$PROJECTS" ]; then
  echo "$PROJECTS" | while read -r proj; do
    TRUST=$(grep -A1 "^\[projects\.$proj\]" "$CONFIG_FILE" 2>/dev/null | grep 'trust_level' | sed 's/.*= *"\(.*\)".*/\1/' || echo "")
    echo "  $proj (信任: $TRUST)"
  done
else
  echo "  (无配置项目)"
fi
echo ""

# --- 最近会话 ---
echo "[最近会话]"
SESSION_INDEX="$CODEX_HOME/session_index.jsonl"
if [ -f "$SESSION_INDEX" ]; then
  SESSION_COUNT=$(wc -l < "$SESSION_INDEX" | tr -d ' ')
  echo "  总会话数: $SESSION_COUNT"
  echo "  最近 5 条:"
  if command -v jq &>/dev/null; then
    tail -5 "$SESSION_INDEX" | jq -r '. | "    \(.updated_at[0:19])  \(.thread_name[0:60])"' 2>/dev/null || echo "    (解析失败)"
  else
    tail -5 "$SESSION_INDEX"
  fi
else
  echo "  (无会话记录)"
fi
echo ""

# --- 安装状态 ---
echo "[安装状态]"
if [ -d "/Applications/ChatGPT.app" ]; then
  echo "  ChatGPT 桌面版: 已安装"
else
  echo "  ChatGPT 桌面版: 未安装"
fi
if command -v codex &>/dev/null; then
  echo "  Codex CLI: $(codex --version 2>/dev/null || echo '已安装')"
else
  echo "  Codex CLI: 未安装"
fi
echo ""

echo "=== 状态查看完成 ==="
