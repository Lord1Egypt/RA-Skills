#!/bin/bash
# Mail MCP 安装脚本

set -e

REPO_URL="https://github.com/AdJIa/mail-mcp-server.git"
PACKAGE_NAME="mail-mcp"
CONFIG_FILE="$HOME/.mcporter/mcporter.json"

echo "=== Mail MCP 安装脚本 ==="

# 检查 mail-mcp 是否已安装
if command -v mail-mcp &> /dev/null; then
    echo "✅ mail-mcp 已安装: $(which mail-mcp)"
else
    echo "📦 正在安装 mail-mcp..."
    pip install git+$REPO_URL --break-system-packages -q
    echo "✅ 安装完成: $(which mail-mcp)"
fi

# 检查 mcporter 配置
if [ -f "$CONFIG_FILE" ]; then
    if grep -q '"mail-mcp"' "$CONFIG_FILE"; then
        echo "✅ mcporter 已配置 mail-mcp"
    else
        echo "⚠️ mcporter 配置中未找到 mail-mcp"
        echo "   请手动添加配置到 $CONFIG_FILE"
    fi
else
    echo "⚠️ mcporter 配置文件不存在: $CONFIG_FILE"
fi

# 显示使用示例
echo ""
echo "=== 使用示例 ==="
echo "mcporter call mail-mcp.list_folders"
echo "mcporter call mail-mcp.send_email --args '{\"to\": [\"user@example.com\"], \"subject\": \"测试\", \"body_text\": \"内容\"}'"
echo ""
echo "完整文档: https://github.com/AdJIa/mail-mcp-server"