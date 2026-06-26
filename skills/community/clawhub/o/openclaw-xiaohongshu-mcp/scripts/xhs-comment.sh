#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$SKILL_DIR/assets/config/mcporter.json"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "❌ 未找到 mcporter，请先安装或确保 PATH 正确。"
  exit 1
fi

if [ $# -lt 3 ]; then
  echo "用法（一级评论）: $0 <feed_id> <xsec_token> <content>"
  echo "用法（回复评论）: $0 <feed_id> <xsec_token> <content> <comment_id> <user_id>"
  exit 1
fi

FEED_ID="$1"
XSEC_TOKEN="$2"
CONTENT="$3"
COMMENT_ID="${4:-}"
USER_ID="${5:-}"

if [ -n "$COMMENT_ID" ] || [ -n "$USER_ID" ]; then
  if [ -z "$COMMENT_ID" ] || [ -z "$USER_ID" ]; then
    echo "❌ 回复指定评论时，comment_id 和 user_id 必须同时提供。"
    exit 1
  fi
  mcporter --config "$CONFIG" call xiaohongshu.reply_comment_in_feed --args "$(printf '{\"feed_id\":\"%s\",\"xsec_token\":\"%s\",\"content\":\"%s\",\"comment_id\":\"%s\",\"user_id\":\"%s\"}' "$FEED_ID" "$XSEC_TOKEN" "$CONTENT" "$COMMENT_ID" "$USER_ID")"
else
  mcporter --config "$CONFIG" call xiaohongshu.post_comment_to_feed --args "$(printf '{\"feed_id\":\"%s\",\"xsec_token\":\"%s\",\"content\":\"%s\"}' "$FEED_ID" "$XSEC_TOKEN" "$CONTENT")"
fi
