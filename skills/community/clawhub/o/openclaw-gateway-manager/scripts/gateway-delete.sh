#!/bin/bash
# gateway-delete.sh - 删除 OpenClaw 网关实例（需要多重确认）

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

INSTANCE="$1"

show_warning() {
    echo "⚠️  ⚠️  ⚠️  危险操作警告  ⚠️  ⚠️  ⚠️"
    echo ""
    echo "这将永久删除以下实例："
    echo "   实例名：$INSTANCE"
    echo "   配置目录：$CONFIG_DIR"
    echo "   服务文件：${SERVICE_FILE:-手动模式，无服务文件}"
    echo ""
    echo "此操作会："
    echo "   ❌ 停止网关进程"
    echo "   ❌ 删除所有配置文件"
    echo "   ❌ 删除所有会话历史"
    echo "   ❌ 删除所有记忆文件"
    echo "   ❌ 删除服务文件"
    echo ""
    echo "此操作不可恢复！"
    echo ""
}

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-delete.sh <实例名>"
    echo ""
    echo "⚠️  警告：这是危险操作，需要多重确认！"
    echo ""
    echo "可用实例:"
    echo "   本地虾 (18789)"
    echo "   飞书 (18790)"
    echo "   腾讯 (28789)"
    echo "   或其他自定义实例名"
    echo ""
    echo "示例：gateway-delete.sh test-bot"
    exit 1
fi

resolve_instance "$INSTANCE"
PORT="$(read_gateway_port "$CONFIG_DIR/openclaw.json")"
[ -n "$PORT" ] || PORT="未知"

if [ ! -d "$CONFIG_DIR" ]; then
    echo "❌ 配置目录不存在：$CONFIG_DIR"
    exit 1
fi

show_warning

echo -n "确认 1/3: 你真的要删除这个实例吗？(输入 YES 继续): "
read -r confirm1
if [ "$confirm1" != "YES" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo -n "确认 2/3: 请输入实例名 '$INSTANCE' 确认： "
read -r confirm2
if [ "$confirm2" != "$INSTANCE" ]; then
    echo "❌ 实例名不匹配，操作已取消"
    exit 1
fi

echo -n "确认 3/3: 输入 'delete' 执行删除： "
read -r confirm3
if [ "$confirm3" != "delete" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "🔴 开始删除..."
echo ""

if [ -n "$PORT" ] && [ "$PORT" != "未知" ]; then
    pid="$(port_pid "$PORT")"
    if [ -n "$pid" ]; then
        echo "⏹️  停止网关进程 (PID: $pid)..."
        kill "$pid" 2>/dev/null
        sleep 2
        echo "✅ 进程已停止"
    fi
fi

if [ -n "$SERVICE_FILE" ] && [ -f "$SERVICE_FILE" ]; then
    echo "⏹️  卸载服务..."
    stop_service "$INSTANCE_KEY" "$SERVICE_FILE" >/dev/null 2>&1 || true
    delete_service_file "$SERVICE_FILE"
    echo "✅ 服务文件已删除"
else
    echo "ℹ️  服务文件不存在"
fi

BACKUP_DIR="$HOME/.openclaw-deleted-backups/$INSTANCE-$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "💾 备份配置到：$BACKUP_DIR"
cp -r "$CONFIG_DIR" "$BACKUP_DIR/" 2>/dev/null
echo "✅ 备份完成（7 天内可恢复）"

echo "🗑️  删除配置目录：$CONFIG_DIR"
rm -rf "$CONFIG_DIR"
echo "✅ 配置目录已删除"

echo ""
echo "✅ 删除完成！"
echo ""
echo "备份位置：$BACKUP_DIR"
echo "如需恢复，执行：cp -r $BACKUP_DIR/* $CONFIG_DIR/"
echo ""
echo "已删除的内容："
echo "   - 配置文件 (openclaw.json)"
echo "   - 会话历史 (sessions/)"
echo "   - 记忆文件 (memory/, MEMORY.md)"
echo "   - 服务文件"
echo ""
echo "⚠️  请手动验证："
echo "   1. 检查端口 $PORT 是否已释放"
echo "   2. 检查服务是否已删除"
echo "   3. 检查 Dashboard 是否无法访问：http://127.0.0.1:$PORT/"
