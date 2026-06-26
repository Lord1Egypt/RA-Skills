#!/bin/bash
# gateway-status.sh - 跨平台 OpenClaw 网关管理器

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

OS="$CURRENT_OS"

echo "=== OpenClaw Gateway Manager ==="
echo "💡 跨平台统一管理 - 支持多平台/多云部署"
echo "📊 当前系统：$OS"
print_repo_usage_hint
echo ""

check_instance() {
    local config_dir="$1"
    local name="$2"
    local config_file="$config_dir/openclaw.json"
    local port
    local pid
    local status
    local browser_port
    local canvas_port
    local aux_ports
    local channel

    [ -f "$config_file" ] || return 0

    port="$(read_gateway_port "$config_file")"
    [ -n "$port" ] || return 0

    pid="$(port_pid "$port")"
    status="❌ 已停止"
    if [ -n "$pid" ]; then
        status="✅ 运行中 (PID: $pid)"
    fi

    browser_port=$((port + 2))
    canvas_port=$((port + 3))
    aux_ports=""
    if port_is_listening "$browser_port"; then
        aux_ports="$aux_ports $browser_port(浏览器)"
    fi
    if port_is_listening "$canvas_port"; then
        aux_ports="$aux_ports $canvas_port(Canvas)"
    fi

    echo "🔹 $name"
    echo "   主端口：$port"
    if [ -n "$aux_ports" ]; then
        echo "   辅助端口：$aux_ports"
    fi
    echo "   配置：$config_dir"
    echo "   状态：$status"

    channel="$(read_primary_channel "$config_file")"
    if [ -n "$channel" ]; then
        echo "   频道：$channel"
    fi

    if [ -n "$pid" ]; then
        echo "   Dashboard: http://127.0.0.1:$port/"
    else
        echo "   ⚠️  进程未运行，需要重启"
    fi
    echo ""
}

label_for_dir() {
    local dir="$1"
    local base

    case "$dir" in
        "$HOME/.openclaw") echo "OpenClaw (默认)" ;;
        "$HOME/.jvs/.openclaw") echo "JVS Claw" ;;
        "$HOME/.qclaw") echo "QClaw" ;;
        "$HOME/.claw-cloud"|"$HOME/.openclaw-cloud") echo "Cloud Claw" ;;
        "$HOME/.config/openclaw") echo "OpenClaw (XDG)" ;;
        /opt/openclaw) echo "OpenClaw (System)" ;;
        *)
            base="$(basename "$dir")"
            case "$base" in
                .openclaw-*) echo "自定义实例：${base#".openclaw-"}" ;;
                openclaw-*) echo "自定义实例：${base#"openclaw-"}" ;;
                *) echo "自定义实例：$base" ;;
            esac
            ;;
    esac
}

echo "🔍 扫描 OpenClaw 配置路径..."
echo ""

while IFS= read -r dir; do
    [ -n "$dir" ] || continue
    check_instance "$dir" "$(label_for_dir "$dir")"
done <<EOF
$(list_candidate_dirs)
EOF

echo "=== 服务状态 ==="
if [[ "$OS" == "macOS" ]]; then
    launchctl list 2>/dev/null | grep -i "claw\|gateway" | while read -r line; do
        status=$(echo "$line" | awk '{print $2}')
        label=$(echo "$line" | awk '{print $3}')
        if [ "$status" = "0" ] || [ "$status" = "1" ]; then
            echo "   ✅ $label (状态：$status)"
        else
            echo "   ❌ $label (状态：$status - 已停止)"
        fi
    done
elif [[ "$OS" == "Linux" ]]; then
    systemctl --user list-units --type=service 2>/dev/null | grep -i "claw\|gateway" | while read -r line; do
        echo "   $line"
    done
else
    echo "   当前系统暂不支持自动查询服务管理器，使用手动模式"
fi

echo ""
echo "=== 所有 Claw 相关端口 ==="
if command -v lsof >/dev/null 2>&1; then
    lsof -i -n -P 2>/dev/null | grep LISTEN | grep -E "node|Claw|QClaw" | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | awk '{print $1, $9}' | sort -u
elif command -v ss >/dev/null 2>&1; then
    ss -lntp 2>/dev/null | grep -E "18[0-9]{3}|1900[0-9]|28789|29000"
elif command -v netstat >/dev/null 2>&1; then
    netstat -tlnp 2>/dev/null | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | awk '{print $4, $7}'
fi

echo ""
echo "📊 统计信息："
if command -v lsof >/dev/null 2>&1; then
    total=$(lsof -i -n -P 2>/dev/null | grep LISTEN | grep -E "node|Claw|QClaw" | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | wc -l | tr -d ' ')
    echo "   检测到的端口数：$total"
elif command -v ss >/dev/null 2>&1; then
    total=$(ss -lnt 2>/dev/null | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | wc -l | tr -d ' ')
    echo "   检测到的端口数：$total"
fi

echo ""
echo "💡 提示：使用 gateway-scan-ports.sh 查看更详细的端口信息"
