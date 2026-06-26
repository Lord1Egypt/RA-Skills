#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$SKILL_DIR/assets/config/mcporter.json"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "❌ 未找到 mcporter，请先安装或确保 PATH 正确。"
  exit 1
fi

if [ $# -lt 1 ]; then
  echo "用法: $0 <关键词>"
  echo "示例: $0 OpenClaw"
  exit 1
fi

KEYWORD="$*"

echo "🔎 搜索小红书关键词: $KEYWORD"
mcporter --config "$CONFIG" call xiaohongshu.search_feeds keyword="$KEYWORD"
