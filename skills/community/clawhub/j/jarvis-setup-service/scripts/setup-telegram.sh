#!/bin/bash
# Telegram Bot 快速配置脚本 v1.0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CONFIG_FILE="${HOME}/.openclaw/config.yaml"

echo "📱 Telegram Bot 配置"
echo "================================"
echo ""

# 检查配置文件是否存在
if [[ ! -f "${CONFIG_FILE}" ]]; then
    echo -e "${YELLOW}⚠${NC} 配置文件不存在，先运行 config.sh"
    exit 1
fi

read -p "请输入 Bot Token: " TOKEN

if [[ -z "${TOKEN}" ]]; then
    echo -e "${RED}✗${NC} Token 不能为空"
    exit 1
fi

# 读取现有配置或创建新的
if grep -q "telegram:" "${CONFIG_FILE}"; then
    # 更新现有配置
    sed -i "s/botToken:.*/botToken: \"${TOKEN}\"/" "${CONFIG_FILE}"
    echo -e "${GREEN}✓${NC} Token 已更新"
else
    # 添加 Telegram 配置
    cat >> "${CONFIG_FILE}" << EOF

channels:
  telegram:
    enabled: true
    botToken: "${TOKEN}"
    adminIds: []
    groupAllowFrom: []
    groupPolicy: "allowlist"
EOF
    echo -e "${GREEN}✓${NC} Telegram 配置已添加"
fi

echo ""
echo -e "${GREEN}✓${NC} 配置完成!"
echo ""
echo "启动命令: openclaw gateway start"
echo ""
echo "配置Bot: @BotFather -> /newbot 获取Token"
