#!/bin/bash
# 飞书发图脚本 - 通过底层 API 发送图片消息
# 使用方式: ./feishu_send_image.sh <图片路径> <接收者ID> [账户ID]

set -e

# 配置
FEISHU_API_BASE="https://open.feishu.cn/open-apis"
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"

# 打印帮助信息
usage() {
    echo "用法: $0 <图片路径> <接收者ID> [账户ID]"
    echo ""
    echo "参数:"
    echo "  图片路径    - 要发送的图片文件路径 (必填)"
    echo "  接收者ID    - 飞书用户 open_id 或群聊 chat_id (必填)"
    echo "  账户ID      - 飞书账户ID (可选,默认: prompt)"
    echo ""
    echo "示例:"
    echo "  $0 /path/to/image.jpg ou_xxxxxxxx"
    echo "  $0 /path/to/image.jpg ou_xxxxxxxx prompt"
    echo "  $0 /path/to/image.jpg oc_xxxxxxxx prompt"
    exit 1
}

# 检查参数
if [ $# -lt 2 ]; then
    usage
fi

IMAGE_PATH="$1"
RECEIVER_ID="$2"
ACCOUNT_ID="${3:-prompt}"

# 检查图片文件是否存在
if [ ! -f "$IMAGE_PATH" ]; then
    echo "错误: 图片文件不存在: $IMAGE_PATH"
    exit 1
fi

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 找不到 OpenClaw 配置文件: $CONFIG_FILE"
    exit 1
fi

# 检查 jq 是否安装
if ! command -v jq &> /dev/null; then
    echo "错误: 需要安装 jq 工具"
    echo "Ubuntu/Debian: sudo apt-get install jq"
    echo "CentOS/RHEL: sudo yum install jq"
    exit 1
fi

echo "=========================================="
echo "飞书图片发送工具"
echo "=========================================="
echo ""

# 步骤1: 读取配置
echo "步骤 1/4: 读取配置..."
echo "使用账户: $ACCOUNT_ID"
echo "接收者ID: $RECEIVER_ID"

APP_ID=$(jq -r ".channels.feishu.accounts[\"$ACCOUNT_ID\"].appId // empty" "$CONFIG_FILE")
APP_SECRET=$(jq -r ".channels.feishu.accounts[\"$ACCOUNT_ID\"].appSecret // empty" "$CONFIG_FILE")

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "错误: 账户 $ACCOUNT_ID 缺少 app_id 或 app_secret"
    exit 1
fi

echo "App ID: ${APP_ID:0:10}..."
echo ""

# 步骤2: 获取 access token
echo "步骤 2/4: 获取 access token..."

TOKEN_RESPONSE=$(curl -s -X POST "${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN_CODE=$(echo "$TOKEN_RESPONSE" | jq -r '.code // 0')
ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token // empty')

if [ "$TOKEN_CODE" != "0" ] || [ -z "$ACCESS_TOKEN" ]; then
    echo "错误: 获取 access token 失败"
    echo "响应: $TOKEN_RESPONSE"
    exit 1
fi

echo "✓ Token 获取成功"
echo ""

# 步骤3: 上传图片
echo "步骤 3/4: 上传图片..."
echo "图片路径: $IMAGE_PATH"

UPLOAD_RESPONSE=$(curl -s -X POST "${FEISHU_API_BASE}/im/v1/images" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -F "image_type=message" \
    -F "image=@$IMAGE_PATH")

UPLOAD_CODE=$(echo "$UPLOAD_RESPONSE" | jq -r '.code // 0')
IMAGE_KEY=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.image_key // empty')

if [ "$UPLOAD_CODE" != "0" ] || [ -z "$IMAGE_KEY" ]; then
    echo "错误: 上传图片失败"
    echo "响应: $UPLOAD_RESPONSE"
    exit 1
fi

echo "✓ 图片上传成功"
echo "Image Key: $IMAGE_KEY"
echo ""

# 步骤4: 发送消息
echo "步骤 4/4: 发送图片消息..."

# 判断接收者类型
RECEIVE_ID_TYPE="open_id"
if [[ "$RECEIVER_ID" == oc_* ]]; then
    RECEIVE_ID_TYPE="chat_id"
    echo "检测到群聊 ID，使用 chat_id 类型"
fi

# 构造 payload (content 必须是 JSON 字符串)
PAYLOAD=$(jq -n \
    --arg rid "$RECEIVER_ID" \
    --arg key "$IMAGE_KEY" \
    '{receive_id: $rid, msg_type: "image", content: ({image_key: $key} | tojson)}')

SEND_RESPONSE=$(curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code // 0')
MESSAGE_ID=$(echo "$SEND_RESPONSE" | jq -r '.data.message_id // empty')

if [ "$SEND_CODE" != "0" ]; then
    echo "错误: 发送消息失败"
    echo "响应: $SEND_RESPONSE"
    exit 1
fi

echo "✓ 消息发送成功!"
echo "Message ID: $MESSAGE_ID"
echo ""

echo "=========================================="
echo "图片发送完成!"
echo "=========================================="
