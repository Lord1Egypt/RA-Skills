#!/bin/bash
# Kids 积分日报发送脚本
# 由 OpenClaw Cron 调用

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHAT_ID="oc_7d968e918766825eb21d51ce45d7e043"
MESSAGE_FILE="/tmp/kids-points-daily-message.json"

# 1. 先运行日报生成（如果还没生成）
if [ ! -f "$MESSAGE_FILE" ]; then
    echo "生成日报..."
    node "$SCRIPT_DIR/daily-report.js"
fi

# 2. 检查消息文件
if [ ! -f "$MESSAGE_FILE" ]; then
    echo "没有消息需要发送"
    exit 0
fi

# 3. 读取并格式化消息
MESSAGE=$(node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('$MESSAGE_FILE', 'utf8'));
const msg = \`📊 \${data.date} 积分日报

\${data.message}

*Kids 积分系统自动生成*\`;
console.log(msg);
")

# 4. 保存到发送文件（供 Agent 读取）
echo "$MESSAGE" > /tmp/kids-points-ready-to-send.txt
echo "消息已准备: /tmp/kids-points-ready-to-send.txt"
echo "目标群聊: $CHAT_ID"
echo ""
echo "请使用以下指令发送:"
echo "message send --chatId $CHAT_ID --message '\$(cat /tmp/kids-points-ready-to-send.txt)'"

# 5. 删除原始消息文件
rm -f "$MESSAGE_FILE"
