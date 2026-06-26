#!/bin/bash
# 添加Bug记录到企业微信智能表格

# 参数说明：
# $1 - 问题描述

WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key=1jziPisqM429DXY1ZZFTwMInCX86CuIDLQvmOCNSHNYWmGesn1PjC9M9SxzhAkDxzK37s9uRTTSQvwiQ9fOxK0Ajpo5SigZ0EMJPPUiVUf3B"

# 问题描述
DESCRIPTION="$1"

# 构造JSON请求 - 发现问题的人员、发现日期、解决时间都留空
cat > /tmp/bug_request.json <<EOF
{
  "schema": {
    "fafLxW": "问题描述",
    "fF5OvO": "发现问题的人员",
    "f9kmWq": "处理进度",
    "f4LSb8": "严重程度",
    "f90ViZ": "处理人",
    "frMCUq": "发现日期",
    "fsoY1c": "解决时间"
  },
  "add_records": [
    {
      "values": {
        "fafLxW": "$DESCRIPTION",
        "fF5OvO": [],
        "f9kmWq": [{"text": "处理中"}],
        "f4LSb8": [],
        "f90ViZ": [{"text": "姜春波"}],
        "frMCUq": "",
        "fsoY1c": ""
      }
    }
  ]
}
EOF

# 发送请求
RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @/tmp/bug_request.json)

# 清理
rm -f /tmp/bug_request.json

# 检查是否成功
if echo "$RESPONSE" | grep -q '"errcode":0'; then
  cat <<EOF
✅ 问题已成功上报，会尽快处理

问题描述：$DESCRIPTION
处理进度：处理中
处理人：姜春波

已添加到企业微信智能表格中。
EOF
  exit 0
else
  echo "❌ 添加失败，错误信息："
  echo "$RESPONSE"
  exit 1
fi
