#!/usr/bin/env bash
# discover-sessions.sh — 扫描 OpenClaw 会话数据目录，输出会话文件列表
# 输出：_mbti_work/session_list.txt（每行一个文件路径）

set -euo pipefail

WORK_DIR="_mbti_work"
SESSION_LIST="$WORK_DIR/session_list.txt"
# 支持环境变量覆盖，方便测试：OPENCLAW_DIR=./test_files bash scripts/discover-sessions.sh
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"

mkdir -p "$WORK_DIR"
: > "$SESSION_LIST"

echo "=== 扫描 OpenClaw 聊天记录 ==="

# 检查 OpenClaw 目录是否存在
if [ ! -d "$OPENCLAW_DIR" ]; then
  echo "❌ 未找到 OpenClaw 数据目录: $OPENCLAW_DIR"
  echo "   请确认 OpenClaw 已安装并使用过。"
  echo "0" > "$WORK_DIR/session_count.txt"
  exit 0
fi

echo "✅ 找到 OpenClaw 数据目录: $OPENCLAW_DIR"

# OpenClaw 会话文件有两种形态：
#   1. 活跃会话：<uuid>.jsonl
#   2. 归档/重置会话：<uuid>.jsonl.reset.<timestamp>
# 因此不能只用 -name "*.jsonl"，需要同时匹配包含 .jsonl 的文件名

# 扫描 sessions/ 目录
if [ -d "$OPENCLAW_DIR/sessions" ]; then
  echo "   扫描 sessions/ ..."
  find "$OPENCLAW_DIR/sessions" -type f \( -name "*.jsonl" -o -name "*.jsonl.reset.*" \) 2>/dev/null >> "$SESSION_LIST" || true
fi

# 扫描 agents/ 目录（包含子目录如 agents/main/sessions/）
if [ -d "$OPENCLAW_DIR/agents" ]; then
  echo "   扫描 agents/ ..."
  find "$OPENCLAW_DIR/agents" -type f \( -name "*.jsonl" -o -name "*.jsonl.reset.*" \) 2>/dev/null >> "$SESSION_LIST" || true
fi

# 如果 sessions/ 和 agents/ 都没找到文件，尝试递归搜索整个 .openclaw 目录
LINE_COUNT=$(wc -l < "$SESSION_LIST" | tr -d ' ')
if [ "$LINE_COUNT" -eq 0 ]; then
  echo "   sessions/ 和 agents/ 未找到 JSONL，尝试递归搜索..."
  find "$OPENCLAW_DIR" -type f \( -name "*.jsonl" -o -name "*.jsonl.reset.*" \) 2>/dev/null >> "$SESSION_LIST" || true
  # 也搜索 .json 文件（排除元数据文件）
  find "$OPENCLAW_DIR" -name "*.json" -type f ! -name "sessions.json" ! -name "config.json" ! -name "package.json" ! -name "skill.json" 2>/dev/null >> "$SESSION_LIST" || true
fi

# 去重
if [ -f "$SESSION_LIST" ]; then
  sort -u "$SESSION_LIST" -o "$SESSION_LIST"
fi

# 统计
TOTAL=$(wc -l < "$SESSION_LIST" | tr -d ' ')
echo ""
echo "📊 发现 $TOTAL 个会话文件"
echo "$TOTAL" > "$WORK_DIR/session_count.txt"

if [ "$TOTAL" -eq 0 ]; then
  echo "⚠️  未找到任何会话文件。"
  echo "   请检查 $OPENCLAW_DIR 目录结构。"
  echo ""
  echo "   当前目录结构："
  ls -la "$OPENCLAW_DIR" 2>/dev/null || echo "   （无法列出）"
fi

