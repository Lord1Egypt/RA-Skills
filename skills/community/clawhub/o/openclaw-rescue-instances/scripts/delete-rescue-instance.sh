#!/bin/bash
# delete-rescue-instance.sh - 删除 OpenClaw 救援 Gateway 实例
# 用法：./delete-rescue-instance.sh [实例编号或名称]

set -e

RESCUE_INPUT=${1:-""}

if [ -z "$RESCUE_INPUT" ]; then
  echo "用法：./delete-rescue-instance.sh [实例编号或名称]"
  echo "示例："
  echo "  ./delete-rescue-instance.sh 1      # 删除 rescue1"
  echo "  ./delete-rescue-instance.sh rescue2  # 删除 rescue2"
  exit 1
fi

# 解析输入
if [[ "$RESCUE_INPUT" =~ ^[0-9]+$ ]]; then
  RESCUE_NAME="rescue${RESCUE_INPUT}"
else
  RESCUE_NAME="$RESCUE_INPUT"
fi

RESCUE_DIR="$HOME/.openclaw-$RESCUE_NAME"
PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-$RESCUE_NAME.plist"

echo "=== 删除救援实例 $RESCUE_NAME ==="

# 1. 卸载服务
if [ -f "$PLIST_FILE" ]; then
  launchctl unload "$PLIST_FILE" 2>/dev/null || true
  rm "$PLIST_FILE"
  echo "✓ 卸载服务：$RESCUE_NAME"
else
  echo "⚠ 服务文件不存在：$PLIST_FILE"
fi

# 2. 删除配置目录
if [ -d "$RESCUE_DIR" ]; then
  rm -rf "$RESCUE_DIR"
  echo "✓ 删除目录：$RESCUE_DIR"
else
  echo "⚠ 目录不存在：$RESCUE_DIR"
fi

echo ""
echo "完成！实例 $RESCUE_NAME 已删除。"
