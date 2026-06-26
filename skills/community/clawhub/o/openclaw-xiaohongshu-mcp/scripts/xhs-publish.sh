#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$SKILL_DIR/assets/config/mcporter.json"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "❌ 未找到 mcporter，请先安装或确保 PATH 正确。"
  exit 1
fi

export MCPORTER_CALL_TIMEOUT="${MCPORTER_CALL_TIMEOUT:-300000}"

if [ $# -lt 1 ]; then
  echo "用法: $0 <payload.json>"
  exit 1
fi

PAYLOAD_FILE="$1"
if [ ! -f "$PAYLOAD_FILE" ]; then
  echo "❌ 文件不存在: $PAYLOAD_FILE"
  exit 1
fi

echo "📝 发布小红书图文，载荷文件: $PAYLOAD_FILE"
mcporter --config "$CONFIG" call xiaohongshu.publish_content --args "$(cat "$PAYLOAD_FILE")"
