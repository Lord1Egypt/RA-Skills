#!/bin/bash
# check_manobrowser.sh — 检测 ManoBrowser MCP 连接
# 用法: bash check_manobrowser.sh [endpoint] [api_key]
# 返回: exit 0 = 连接正常, exit 1 = 未配置, exit 2 = 设备离线

ENDPOINT="${1:-}"
API_KEY="${2:-}"

echo "🔍 ManoBrowser 连接检测..."

# Step 1: 检查连接配置
if [ -z "$ENDPOINT" ] || [ -z "$API_KEY" ]; then
    echo "❌ ManoBrowser MCP 连接未配置"
    echo ""
    echo "ManoBrowser 是一个 Chrome 浏览器插件，让 AI 能采集网页数据。"
    echo ""
    echo "📦 安装步骤："
    echo "  1. 从 https://github.com/ClawCap/ManoBrowser 下载插件"
    echo "  2. 在 Chrome 打开 chrome://extensions"
    echo "  3. 开启「开发者模式」→「加载已解压的扩展程序」"
    echo "  4. 安装后，在插件设置中获取 MCP Endpoint 和 API Key"
    echo "  5. 将 Endpoint 和 API Key 配置到 TOOLS.md 中"
    echo ""
    echo "配置格式（添加到 TOOLS.md）："
    echo "  ## ManoBrowser"
    echo "  - Endpoint: https://datasaver.deepminingai.com/api/v2/{deviceId}/mcp"
    echo "  - API Key: mb_xxxxxx"
    exit 1
fi
echo "✅ MCP 配置存在: $ENDPOINT"

# Step 2: 验证连接
RESPONSE=$(curl -s --max-time 10 -X POST "$ENDPOINT" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' 2>&1)

if echo "$RESPONSE" | grep -q '"tools"'; then
    TOOL_COUNT=$(echo "$RESPONSE" | grep -o '"name"' | wc -l | tr -d ' ')
    echo "✅ ManoBrowser 连接正常 ($TOOL_COUNT 个工具可用)"
    exit 0
elif echo "$RESPONSE" | grep -qi "not found"; then
    echo "❌ 设备未找到 — ManoBrowser 插件未安装或 API Key 错误"
    echo "   请确认 Chrome 已安装 ManoBrowser 插件，并检查 API Key 是否正确"
    exit 1
elif echo "$RESPONSE" | grep -qi "offline\|parse error\|Syntax error"; then
    echo "⚠️ 设备离线 — 请打开 Chrome 浏览器并确认 ManoBrowser 插件已激活"
    echo "   插件图标应显示为彩色（非灰色）"
    exit 2
else
    echo "❌ 连接异常"
    echo "   返回: ${RESPONSE:0:200}"
    exit 1
fi
