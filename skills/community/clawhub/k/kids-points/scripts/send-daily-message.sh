#!/bin/bash
# 发送 Kids 积分日报消息到飞书群聊
# 这个脚本由 OpenClaw Agent 调用

MESSAGE_FILE="/tmp/kids-points-daily-message.json"
CHAT_ID="oc_7d968e918766825eb21d51ce45d7e043"

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "消息文件不存在: $MESSAGE_FILE"
    exit 1
fi

# 读取消息内容
MESSAGE=$(python3 -c "import json; print(json.load(open('$MESSAGE_FILE'))['message'])")
DATE=$(python3 -c "import json; print(json.load(open('$MESSAGE_FILE'))['date'])")

# 添加标题
FULL_MESSAGE="📊 ${DATE} 积分日报

${MESSAGE}

*Kids 积分系统自动生成*"

# 使用 openclaw message 发送（通过 Bot）
openclaw message send --target="chat:$CHAT_ID" --channel=feishu --message="$FULL_MESSAGE" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 消息发送成功"
    # 删除已发送的消息文件
    rm -f "$MESSAGE_FILE"
else
    echo "❌ 消息发送失败"
    exit 1
fi
