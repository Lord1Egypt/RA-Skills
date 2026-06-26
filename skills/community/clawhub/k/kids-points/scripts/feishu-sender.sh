#!/bin/bash
# OpenClaw Agent 发送脚本
# 这个脚本在 Agent 会话中执行，可以使用 message 工具

CHAT_ID="oc_7d968e918766825eb21d51ce45d7e043"
SEND_FILE="/tmp/kids-points-send-ready.txt"

if [ ! -f "$SEND_FILE" ]; then
    echo "没有待发送的消息"
    exit 0
fi

MESSAGE=$(cat "$SEND_FILE")

# 输出发送指令供 OpenClaw 解析
# 格式: SEND_MESSAGE|<chat_id>|<message>
echo "SEND_MESSAGE|$CHAT_ID|$MESSAGE"

# 删除已发送的文件
rm -f "$SEND_FILE"
