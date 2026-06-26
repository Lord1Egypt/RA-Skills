#!/bin/bash
# gateway-set-port.sh - 修改网关端口

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

INSTANCE="$1"
NEW_PORT="$2"

if [ -z "$INSTANCE" ] || [ -z "$NEW_PORT" ]; then
    echo "用法：gateway-set-port.sh <实例名> <新端口>"
    echo ""
    echo "实例名别名:"
    echo "  local-shrimp / 本地虾 / 18789 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 / 18790 → ~/.openclaw/"
    echo "  qclaw / 腾讯 / 28789 → ~/.qclaw/"
    exit 1
fi

resolve_instance "$INSTANCE"

echo "🔧 修改 $INSTANCE_NAME 端口 → $NEW_PORT"
echo ""

if ! ensure_port_free "$NEW_PORT"; then
    echo "❌ 端口 $NEW_PORT 已被占用"
    if command -v lsof >/dev/null 2>&1; then
        lsof -i :"$NEW_PORT"
    fi
    exit 1
fi
echo "✅ 端口 $NEW_PORT 可用"

CONFIG_FILE="$CONFIG_DIR/openclaw.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    exit 1
fi

cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d%H%M%S)"
jq ".gateway.port = $NEW_PORT" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
echo "✅ 配置文件已更新：$CONFIG_FILE"

if [ -d "$CONFIG_DIR/.openclaw" ]; then
    cp "$CONFIG_FILE" "$CONFIG_DIR/.openclaw/openclaw.json"
    echo "✅ 嵌套配置已同步"
fi

if [ -n "$SERVICE_FILE" ] && [ -f "$SERVICE_FILE" ]; then
    create_service_file "$INSTANCE_KEY" "$CONFIG_DIR" "$NEW_PORT" "$SERVICE_FILE"
    echo "✅ 服务文件已更新：$SERVICE_FILE"
else
    echo "⚠️  未找到服务文件，将仅更新配置"
fi

echo ""
echo "🔄 重启网关..."
restart_service "$INSTANCE_KEY" "$CONFIG_DIR" "$SERVICE_FILE" >/dev/null 2>&1 || echo "⚠️  自动重启失败，请手动执行 OPENCLAW_HOME=$CONFIG_DIR openclaw gateway restart"
sleep 3

echo ""
if port_is_listening "$NEW_PORT"; then
    echo "✅ 网关已在端口 $NEW_PORT 运行"
    echo ""
    echo "📊 Dashboard: http://127.0.0.1:$NEW_PORT/"
else
    echo "⚠️  网关未在端口 $NEW_PORT 监听"
    echo "请手动执行：OPENCLAW_HOME=$CONFIG_DIR openclaw gateway restart"
fi
