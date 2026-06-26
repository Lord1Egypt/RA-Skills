#!/bin/bash
# OpenClaw 配置脚本 v1.0

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

OPENCLAW_DIR="${HOME}/.openclaw"
CONFIG_FILE="${OPENCLAW_DIR}/config.yaml"

echo "🔧 OpenClaw 配置脚本"
echo "================================"
echo ""

# 创建目录
mkdir -p "${OPENCLAW_DIR}"
mkdir -p "${OPENCLAW_DIR}/skills"
mkdir -p "${OPENCLAW_DIR}/logs"
mkdir -p "${OPENCLAW_DIR}/data"

# 检查是否已存在配置
if [[ -f "${CONFIG_FILE}" ]]; then
    echo "检测到已有配置文件: ${CONFIG_FILE}"
    read -p "是否覆盖? (y/n): " confirm
    if [[ "${confirm}" != "y" ]]; then
        echo "取消配置"
        exit 0
    fi
fi

# 收集配置信息
echo ""
echo "【基础配置】"

read -p "请输入 Telegram Bot Token (留空跳过): " TELEGRAM_TOKEN
read -p "请输入管理员 Chat ID (留空跳过): " ADMIN_ID

# 生成配置文件
cat > "${CONFIG_FILE}" << EOF
# OpenClaw 配置文件
# 版本: 1.0
# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')

version: "1.0"

# 频道配置
channels:
  telegram:
    enabled: true
    botToken: "${TELEGRAM_TOKEN:-YOUR_BOT_TOKEN}"
    adminIds:
      - "${ADMIN_ID:-YOUR_ADMIN_ID}"
    groupAllowFrom: []
    groupPolicy: "allowlist"

# 技能设置
skills:
  autoUpdate: true
  installPath: "${OPENCLAW_DIR}/skills"

# 日志配置
logging:
  level: info
  file: "${OPENCLAW_DIR}/logs/jarvis.log"
  maxSize: 10m
  maxFiles: 5

# 服务器配置
server:
  port: 18789
  host: "0.0.0.0"
  selfUrl: "http://localhost:18789"

# 数据目录
data:
  path: "${OPENCLAW_DIR}/data"
EOF

echo ""
echo -e "${GREEN}✓${NC} 配置文件已创建: ${CONFIG_FILE}"
echo ""
echo "下一步:"
echo "  1. 编辑配置: nano ${CONFIG_FILE}"
echo "  2. 启动服务: openclaw gateway start"
