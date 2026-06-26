#!/bin/bash
# OpenClaw 每日技巧发送脚本
# 早上 7:21 发送当日技巧

OBSIDIAN_PATH="$HOME/Obsidian/Docs/OpenClaw"
TIPS_FILE="$OBSIDIAN_PATH/daily-tips.json"
TIPS_LOG="$OBSIDIAN_PATH/tips-log.md"

# 读取当日选择的技巧
TODAY=$(date +%Y-%m-%d)
TIP=$(cat "$TIPS_FILE" | jq -r ".\"$TODAY\"" 2>/dev/null)

if [[ -z "$TIP" || "$TIP" == "null" ]]; then
    echo "❌ 今日技巧未选择，请在晚上 21:05 选择"
    exit 1
fi

# 读取技巧详细内容
TIP_CONTENT=$(cat "$OBSIDIAN_PATH/tips/$TIP.md" 2>/dev/null)

# 读取版本更新
VERSION=$(cat "$OBSIDIAN_PATH/latest-version.txt" 2>/dev/null)

# 发送消息
MESSAGE="🌅 早安！今日 OpenClaw 技巧分享：\n\n"
MESSAGE+="📌 $TIP\n\n"
MESSAGE+="$TIP_CONTENT\n"

if [[ -n "$VERSION" ]]; then
    MESSAGE+="\n🔔 版本更新: $VERSION"
fi

# 通过 OpenClaw 发送消息给用户
openclaw message send --target "ou_6492d43062b301922db4bb3b91f2c22a" --message "$MESSAGE"

echo "✅ 已发送今日技巧: $TIP"
