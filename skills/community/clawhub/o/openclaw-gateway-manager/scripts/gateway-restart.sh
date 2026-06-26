#!/bin/bash
# gateway-restart.sh - 重启网关

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

INSTANCE="$1"

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-restart.sh <实例名|all>"
    echo ""
    echo "实例名:"
    echo "  local-shrimp / 本地虾 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 → ~/.openclaw/"
    echo "  qclaw / 腾讯 → ~/.qclaw/"
    echo "  all → 重启所有网关"
    exit 1
fi

restart_gateway() {
    local raw_instance="$1"

    resolve_instance "$raw_instance"
    echo "🔄 重启 $INSTANCE_NAME..."

    if restart_service "$INSTANCE_KEY" "$CONFIG_DIR" "$SERVICE_FILE"; then
        echo "✅ $INSTANCE_NAME 已重启 ($(service_kind))"
    else
        echo "❌ 自动重启失败"
        echo "请手动执行：OPENCLAW_HOME=$CONFIG_DIR openclaw gateway restart"
    fi
}

case "$INSTANCE" in
    all)
        while IFS= read -r dir; do
            [ -n "$dir" ] || continue
            case "$dir" in
                "$HOME/.jvs/.openclaw") target="local-shrimp" ;;
                "$HOME/.openclaw") target="feishu" ;;
                "$HOME/.qclaw") target="qclaw" ;;
                *)
                    base="$(basename "$dir")"
                    case "$base" in
                        .openclaw-*) target="${base#".openclaw-"}" ;;
                        openclaw-*) target="${base#"openclaw-"}" ;;
                        *) target="" ;;
                    esac
                    ;;
            esac
            [ -n "$target" ] || continue
            restart_gateway "$target"
            echo ""
        done <<EOF
$(list_candidate_dirs)
EOF
        ;;
    *)
        restart_gateway "$INSTANCE"
        ;;
esac

echo ""
echo "=== 验证状态 ==="
sleep 2
if command -v lsof >/dev/null 2>&1; then
    lsof -i -n -P | grep LISTEN | grep "node" | grep "openclaw" | awk -F: '{print "✅ 端口: " $2}' | awk '{print $1}'
elif command -v ss >/dev/null 2>&1; then
    ss -lntp 2>/dev/null | grep -i openclaw
fi
