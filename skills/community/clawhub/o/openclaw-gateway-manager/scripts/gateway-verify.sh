#!/bin/bash
# gateway-verify.sh - 验证网关配置

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

INSTANCE="$1"

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-verify.sh <实例名>"
    echo ""
    echo "实例名:"
    echo "  local-shrimp / 本地虾 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 → ~/.openclaw/"
    echo "  qclaw / 腾讯 → ~/.qclaw/"
    exit 1
fi

resolve_instance "$INSTANCE"

echo "=== 验证 $INSTANCE_NAME 配置 ==="
echo ""

ERRORS=0
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
PORT=""

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 配置文件存在：$CONFIG_FILE"
    PORT="$(read_gateway_port "$CONFIG_FILE")"
    echo "   配置端口：$PORT"
else
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$CONFIG_DIR/.openclaw/openclaw.json" ]; then
    NESTED_PORT="$(read_gateway_port "$CONFIG_DIR/.openclaw/openclaw.json")"
    if [ "$PORT" = "$NESTED_PORT" ]; then
        echo "✅ 嵌套配置一致：$NESTED_PORT"
    else
        echo "❌ 嵌套配置不一致：$NESTED_PORT (应该是 $PORT)"
        ERRORS=$((ERRORS + 1))
    fi
fi

if [ -n "$SERVICE_FILE" ] && [ -f "$SERVICE_FILE" ]; then
    echo "✅ 服务文件存在：$SERVICE_FILE"
    FILE_PORT="$(grep -Eo -- '--port[ =][0-9]+' "$SERVICE_FILE" | grep -Eo '[0-9]+' | head -1)"
    if [ -n "$FILE_PORT" ]; then
        echo "   服务端口：$FILE_PORT"
        if [ -n "$PORT" ] && [ "$PORT" != "$FILE_PORT" ]; then
            echo "⚠️  服务文件端口与配置文件不一致"
            ERRORS=$((ERRORS + 1))
        fi
    fi
else
    echo "ℹ️  未找到服务文件：${SERVICE_FILE:-当前系统为手动模式}"
fi

if [ -n "$PORT" ]; then
    if port_is_listening "$PORT"; then
        PID="$(port_pid "$PORT")"
        echo "✅ 端口 $PORT 正在监听 (PID: $PID)"
    else
        echo "❌ 端口 $PORT 未监听"
        ERRORS=$((ERRORS + 1))
    fi
fi

if ps aux | grep "[o]penclaw.*gateway" >/dev/null 2>&1; then
    echo "✅ 网关进程运行中"
else
    echo "❌ 网关进程未运行"
    ERRORS=$((ERRORS + 1))
fi

if [ -n "$PORT" ]; then
    if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT/" 2>/dev/null | grep -E "200|30[0-9]" >/dev/null; then
        echo "✅ Dashboard 可访问：http://127.0.0.1:$PORT/"
    else
        echo "⚠️  Dashboard 无法访问：http://127.0.0.1:$PORT/"
    fi
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "🎉 所有检查通过！"
else
    echo "⚠️  发现 $ERRORS 个问题"
fi

exit "$ERRORS"
