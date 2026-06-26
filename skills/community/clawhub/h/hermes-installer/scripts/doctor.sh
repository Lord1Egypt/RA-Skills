#!/bin/bash
# Hermes Agent 健康检查脚本 (Linux/macOS)
# 用法: bash doctor.sh

set -e

HERMES_DIR="$HOME/.hermes"
HERMES_AGENT_DIR="$HERMES_DIR/hermes-agent"
ENV_FILE="$HERMES_DIR/.env"
CONFIG_FILE="$HERMES_DIR/config.yaml"

echo "╔════════════════════════════════════════╗"
echo "║     Hermes Agent 健康检查              ║"
echo "╚════════════════════════════════════════╝"
echo ""

ERRORS=0
WARNINGS=0

# 1. 检查安装目录
echo "📁 检查安装目录..."
if [ -d "$HERMES_AGENT_DIR" ]; then
    echo "  ✅ 安装目录存在: $HERMES_AGENT_DIR"
else
    echo "  ❌ 安装目录不存在: $HERMES_AGENT_DIR"
    ERRORS=$((ERRORS + 1))
fi

# 2. 检查虚拟环境
echo ""
echo "🐍 检查虚拟环境..."
if [ -d "$HERMES_AGENT_DIR/venv" ]; then
    echo "  ✅ 虚拟环境存在"
    if [ -f "$HERMES_AGENT_DIR/venv/bin/activate" ]; then
        echo "  ✅ 激活脚本存在"
    else
        echo "  ❌ 激活脚本不存在"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "  ❌ 虚拟环境不存在"
    ERRORS=$((ERRORS + 1))
fi

# 3. 检查配置文件
echo ""
echo "📄 检查配置文件..."
if [ -f "$CONFIG_FILE" ]; then
    echo "  ✅ config.yaml 存在"
else
    echo "  ⚠️  config.yaml 不存在"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -f "$ENV_FILE" ]; then
    echo "  ✅ .env 文件存在"
    
    # 检查必要的环境变量
    echo ""
    echo "🔐 检查环境变量..."
    
    if grep -q "OPENAI_API_KEY=" "$ENV_FILE" && [ -n "$(grep 'OPENAI_API_KEY=' "$ENV_FILE" | cut -d'=' -f2)" ]; then
        echo "  ✅ OPENAI_API_KEY 已设置"
    else
        echo "  ⚠️  OPENAI_API_KEY 未设置"
        WARNINGS=$((WARNINGS + 1))
    fi
    
    if grep -q "OPENAI_BASE_URL=" "$ENV_FILE" && [ -n "$(grep 'OPENAI_BASE_URL=' "$ENV_FILE" | cut -d'=' -f2)" ]; then
        BASE_URL=$(grep 'OPENAI_BASE_URL=' "$ENV_FILE" | cut -d'=' -f2)
        echo "  ✅ OPENAI_BASE_URL 已设置: $BASE_URL"
    else
        echo "  ⚠️  OPENAI_BASE_URL 未设置"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ⚠️  .env 文件不存在"
    WARNINGS=$((WARNINGS + 1))
fi

# 4. 检查网关状态
echo ""
echo "🌐 检查网关状态..."
cd "$HERMES_AGENT_DIR" 2>/dev/null || true
if [ -d "$HERMES_AGENT_DIR/venv" ]; then
    source "$HERMES_AGENT_DIR/venv/bin/activate" 2>/dev/null || true
    GATEWAY_STATUS=$(hermes gateway status 2>/dev/null || echo "未知")
    echo "  状态: $GATEWAY_STATUS"
else
    echo "  ⚠️  无法检查（虚拟环境不存在）"
    WARNINGS=$((WARNINGS + 1))
fi

# 5. 测试 API 连接
echo ""
echo "🔌 测试 API 连接..."
if [ -f "$ENV_FILE" ]; then
    API_KEY=$(grep 'OPENAI_API_KEY=' "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    BASE_URL=$(grep 'OPENAI_BASE_URL=' "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    
    if [ -n "$API_KEY" ] && [ -n "$BASE_URL" ]; then
        # 提取 base_url 的域名部分
        API_ENDPOINT="$BASE_URL/chat/completions"
        
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
            -X POST "$API_ENDPOINT" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d '{"model": "test", "messages": [{"role": "user", "content": "hi"}]}' \
            --connect-timeout 10 2>/dev/null || echo "000")
        
        if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "400" ] || [ "$RESPONSE" = "401" ]; then
            echo "  ✅ API 端点可达 (HTTP $RESPONSE)"
        elif [ "$RESPONSE" = "000" ]; then
            echo "  ❌ API 端点无法连接"
            ERRORS=$((ERRORS + 1))
        else
            echo "  ⚠️  API 返回异常状态码: HTTP $RESPONSE"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo "  ⚠️  API Key 或 Base URL 未配置"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "  ⚠️  .env 文件不存在，跳过 API 测试"
fi

# 6. 检查日志
echo ""
echo "📋 检查最近日志..."
LOG_FILE="$HERMES_DIR/logs/agent.log"
if [ -f "$LOG_FILE" ]; then
    ERROR_COUNT=$(grep -c -i "error" "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "  ⚠️  发现 $ERROR_COUNT 条错误日志"
        echo ""
        echo "  最近错误:"
        grep -i "error" "$LOG_FILE" | tail -3 | sed 's/^/    /'
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ✅ 未发现错误日志"
    fi
else
    echo "  ℹ️  日志文件不存在"
fi

# 汇总
echo ""
echo "╔════════════════════════════════════════╗"
echo "║              检查结果汇总              ║"
echo "╠════════════════════════════════════════╣"
echo "║  ❌ 错误: $ERRORS                            ║"
echo "║  ⚠️  警告: $WARNINGS                            ║"
echo "╚════════════════════════════════════════╝"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ Hermes Agent 状态良好！"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Hermes Agent 基本正常，但有 $WARNINGS 个警告"
    exit 0
else
    echo "❌ Hermes Agent 存在 $ERRORS 个错误，请检查！"
    exit 1
fi
