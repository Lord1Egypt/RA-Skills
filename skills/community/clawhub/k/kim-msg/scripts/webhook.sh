#!/usr/bin/env bash
# Kim Webhook 消息发送脚本
# 智能密钥加载：环境变量优先，自动 fallback 到密钥文件
# 用法：webhook.sh <消息内容> [--text]

set -euo pipefail

# 常见密钥文件路径（按优先级排序）
CREDENTIAL_FILES=(
  "$HOME/.openclaw/.secrets"
  "$HOME/.kim_credentials"
  "./kim_credentials"
)

# 从密钥文件加载 Webhook Token
load_webhook_token() {
  for cred_file in "${CREDENTIAL_FILES[@]}"; do
    if [[ -f "$cred_file" ]]; then
      local token=$(grep "^KIM_WEBHOOK_TOKEN=" "$cred_file" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')
      if [[ -n "$token" ]]; then
        echo "$token"
        return 0
      fi
    fi
  done
  return 1
}

# 检查环境变量
if [[ -z "${KIM_WEBHOOK_TOKEN:-}" ]]; then
  # 环境变量未设置，尝试从文件加载
  API_TOKEN=$(load_webhook_token) || {
    echo "❌ 错误：缺少 Kim Webhook Token"
    echo ""
    echo "请用以下任一方式配置："
    echo "  1. 设置环境变量："
    echo "     export KIM_WEBHOOK_TOKEN=your_webhook_token"
    echo ""
    echo "  2. 创建密钥文件（推荐）："
    echo "     KIM_WEBHOOK_TOKEN=your_webhook_token"
    echo ""
    echo "     支持的文件位置："
    echo "     - ~/.openclaw/.secrets"
    echo "     - ~/.kim_credentials"
    echo "     - ./kim_credentials"
    exit 1
  }
else
  API_TOKEN="$KIM_WEBHOOK_TOKEN"
fi

# 解析参数
MSG_TYPE="markdown"
CONTENT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)
      MSG_TYPE="text"
      shift
      ;;
    *)
      CONTENT="$1"
      shift
      ;;
  esac
done

if [[ -z "$CONTENT" ]]; then
  echo "Usage: $0 <消息内容> [--text]" >&2
  exit 1
fi

# 构造请求体
if [[ "$MSG_TYPE" == "markdown" ]]; then
  BODY=$(jq -n --arg content "$CONTENT" '{"msgtype": "markdown", "markdown": {"content": $content}}')
else
  BODY=$(jq -n --arg content "$CONTENT" '{"msgtype": "text", "text": {"content": $content}}')
fi

# 发送请求
URL="https://kim-robot.kwaitalk.com/api/robot/send?key=$API_TOKEN"
RESPONSE=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "$BODY")

# 检查结果
if echo "$RESPONSE" | jq -e '.code == 200' > /dev/null 2>&1; then
  echo "✅ 消息发送成功！"
  echo "$RESPONSE" | jq -r '.msg // .'
else
  echo "❌ 发送失败：" >&2
  echo "$RESPONSE" >&2
  exit 1
fi
