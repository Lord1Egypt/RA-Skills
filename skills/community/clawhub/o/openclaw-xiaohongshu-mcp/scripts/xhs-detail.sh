#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$SKILL_DIR/assets/config/mcporter.json"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "❌ 未找到 mcporter，请先安装或确保 PATH 正确。"
  exit 1
fi

if [ $# -lt 2 ]; then
  cat <<'USAGE'
用法:
  ./scripts/xhs-detail.sh <feed_id> <xsec_token> [load_all_comments]
USAGE
  exit 1
fi

FEED_ID="$1"
XSEC_TOKEN="$2"
LOAD_ALL="${3:-false}"

echo "📖 读取小红书笔记详情"
echo "  feed_id: $FEED_ID"
echo "  load_all_comments: $LOAD_ALL"

mcporter --config "$CONFIG" call xiaohongshu.get_feed_detail --args "$(printf '{\"feed_id\":\"%s\",\"xsec_token\":\"%s\",\"load_all_comments\":%s}' "$FEED_ID" "$XSEC_TOKEN" "$LOAD_ALL")"
