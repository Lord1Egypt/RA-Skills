#!/bin/bash
# gateway-scan-ports.sh - 智能扫描 OpenClaw 网关端口

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
. "$SCRIPT_DIR/common.sh"

echo "=== OpenClaw 端口扫描 ==="
echo ""

for port in $(seq 18000 18999); do
    if port_is_listening "$port"; then
        pid="$(port_pid "$port")"
        is_main=false
        config_dir=""

        while IFS= read -r dir; do
            [ -n "$dir" ] || continue
            if [ -f "$dir/openclaw.json" ]; then
                cfg_port="$(read_gateway_port "$dir/openclaw.json")"
                if [ "$cfg_port" = "$port" ]; then
                    is_main=true
                    config_dir="$dir"
                    break
                fi
            fi
        done <<EOF
$(list_candidate_dirs)
EOF

        if [ "$is_main" = true ]; then
            browser_port=$((port + 2))
            canvas_port=$((port + 3))

            echo "🔹 网关实例 (主端口：$port)"
            echo "   PID: $pid"
            echo "   配置：$config_dir"

            aux=""
            if port_is_listening "$browser_port"; then
                aux="$aux 浏览器:$browser_port"
            fi
            if port_is_listening "$canvas_port"; then
                aux="$aux Canvas:$canvas_port"
            fi
            if [ -n "$aux" ]; then
                echo "   辅助端口:$aux"
            fi

            if [ -f "$config_dir/openclaw.json" ]; then
                channels=$(jq -r '.channels | keys | join(", ")' "$config_dir/openclaw.json" 2>/dev/null)
                if [ -n "$channels" ] && [ "$channels" != "null" ]; then
                    echo "   频道：$channels"
                fi
            fi

            echo "   Dashboard: http://127.0.0.1:$port/"
            echo ""
        fi
    fi
done

echo "=== 其他 Node 进程 (可能不是 OpenClaw) ==="
if command -v lsof >/dev/null 2>&1; then
    lsof -i -n -P 2>/dev/null | grep LISTEN | grep node | grep -v "18[0-9]\{3\}" | awk '{print $1, $9}' | sort -u | head -10
elif command -v ss >/dev/null 2>&1; then
    ss -lntp 2>/dev/null | grep node | head -10
fi
