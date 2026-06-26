#!/bin/bash
# gateway-create.sh - 创建新的 OpenClaw 网关实例

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

INSTANCE_NAME="$1"
PORT="$2"
CHANNEL="$3"

if [ -z "$INSTANCE_NAME" ] || [ -z "$PORT" ]; then
    echo "用法：gateway-create.sh <实例名> <端口> [频道]"
    echo ""
    echo "示例:"
    echo "  gateway-create.sh test-instance 18888 openim"
    echo "  gateway-create.sh wechat-bot 18889 wechat"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "❌ 错误：需要 jq 命令"
    echo "macOS 安装：brew install jq"
    echo "Linux 安装：sudo apt install jq"
    exit 1
fi

INSTANCE_KEY="$INSTANCE_NAME"
CONFIG_DIR="$HOME/.openclaw-$INSTANCE_NAME"
SERVICE_FILE="$(service_file_for_instance "$INSTANCE_KEY")"

echo "🔧 创建新实例：$INSTANCE_NAME"
echo "   配置目录：$CONFIG_DIR"
if [ -n "$SERVICE_FILE" ]; then
    echo "   服务文件：$SERVICE_FILE"
fi
echo "   端口：$PORT"
echo "   频道：${CHANNEL:-openim}"
echo ""

if ! ensure_port_free "$PORT"; then
    echo "❌ 端口 $PORT 已被占用"
    exit 1
fi
echo "✅ 端口 $PORT 可用"

mkdir -p "$CONFIG_DIR"
echo "✅ 配置目录已创建：$CONFIG_DIR"

BASE_CONFIG=""
while IFS= read -r dir; do
    [ -n "$dir" ] || continue
    if [ -f "$dir/openclaw.json" ] && [ "$dir" != "$CONFIG_DIR" ]; then
        BASE_CONFIG="$dir/openclaw.json"
        break
    fi
done <<EOF
$(list_candidate_dirs)
EOF

if [ -n "$BASE_CONFIG" ]; then
    cp "$BASE_CONFIG" "$CONFIG_DIR/openclaw.json"
    echo "✅ 配置文件已复制：$BASE_CONFIG"
else
    echo "⚠️  未找到基础配置，需要手动配置"
fi

if [ -f "$CONFIG_DIR/openclaw.json" ]; then
    jq ".gateway.port = $PORT" "$CONFIG_DIR/openclaw.json" > "$CONFIG_DIR/openclaw.json.tmp" && mv "$CONFIG_DIR/openclaw.json.tmp" "$CONFIG_DIR/openclaw.json"
    echo "✅ 端口已设置为：$PORT"
fi

if create_service_file "$INSTANCE_KEY" "$CONFIG_DIR" "$PORT" "$SERVICE_FILE"; then
    echo "✅ 服务文件已创建：$SERVICE_FILE"
else
    echo "ℹ️  当前系统仅创建配置目录，服务请手动启动"
fi

if enable_service "$INSTANCE_KEY" "$SERVICE_FILE"; then
    sleep 3
    echo "✅ 网关已启动"
else
    echo "⚠️  自动启动失败，请手动执行：OPENCLAW_HOME=$CONFIG_DIR openclaw gateway --port $PORT"
fi

echo ""
echo "=== 验证 ==="
if port_is_listening "$PORT"; then
    echo "✅ 网关运行在端口 $PORT"
    echo "📊 Dashboard: http://127.0.0.1:$PORT/"
else
    echo "⚠️  网关未启动，请检查日志：$CONFIG_DIR/logs/"
fi
