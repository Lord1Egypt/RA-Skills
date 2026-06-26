#!/bin/bash
# Infra Heartbeat Daemon — OpenClaw 基础设施心跳监控
# 用法: heartbeat-daemon.sh --config <配置文件>
# 不带参数时读取默认配置 ~/.config/infra-heartbeat/config.env

set -euo pipefail

# 默认配置路径
DEFAULT_CONFIG_DIR="${HOME}/.config/infra-heartbeat"
DEFAULT_CONFIG="${DEFAULT_CONFIG_DIR}/config.env"
LOG_DIR="${HOME}/.openclaw/workspace-infra"
LOG="${LOG_DIR}/heartbeat.log"
ALERT_LOG="${LOG_DIR}/alerts.log"
FAIL_COUNT_FILE="${LOG_DIR}/restart-fail-count"

# WS module 路径（自动检测）
detect_ws_module() {
    local openclaw_node_modules
    openclaw_node_modules=$(find "${HOME}/.npm-global/lib/node_modules/openclaw/node_modules/ws" -maxdepth 0 2>/dev/null || echo "")
    if [[ -z "$openclaw_node_modules" ]]; then
        openclaw_node_modules=$(find "${HOME}/.npm-global/lib/node_modules/openclaw" -path "*/node_modules/ws" 2>/dev/null | head -1)
    fi
    echo "$openclaw_node_modules"
}

# 加载配置
load_config() {
    local config_file="${1:-${DEFAULT_CONFIG}}"
    if [[ -f "$config_file" ]]; then
        set -a
        source "$config_file"
        set +a
    else
        echo "ERROR: 配置文件不存在: $config_file" >&2
        exit 1
    fi
}

# 日志
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG"
}

# 校验 JSON
validate_json() {
    node -e "
const fs = require('fs');
try {
    JSON.parse(fs.readFileSync('${OPENCLAW_JSON}', 'utf8'));
    console.log('VALID');
} catch(e) {
    console.log('INVALID: ' + e.message);
}
" 2>/dev/null
}

# 备份配置
backup_config() {
    local bak="${OPENCLAW_JSON}.auto.$(date '+%Y%m%d_%H%M%S')"
    mkdir -p "$(dirname "$bak")"
    cp "$OPENCLAW_JSON" "$bak"
    log "CONFIG: 备份已创建 $bak"
    # 只保留最近5份
    ls -t "${OPENCLAW_JSON}.auto."* 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
}

# 保存"最后一次已知良好"配置（最多3份，MD5 不重复才保存）
save_last_good() {
    local newest="${OPENCLAW_JSON}.last-good.1"
    # 如果存在 last-good.1，检查 MD5 是否真的变了，没变则跳过
    if [[ -f "$newest" ]]; then
        local cur_md5 new_md5
        cur_md5=$(md5sum "$newest" | awk '{print $1}')
        new_md5=$(md5sum "$OPENCLAW_JSON" | awk '{print $1}')
        if [[ "$cur_md5" == "$new_md5" ]]; then
            log "CONFIG: 配置未变更，跳过 last-good 保存"
            return 0
        fi
    fi

    # 轮转：last-good.2 → last-good.3（会被覆盖），last-good.1 → last-good.2
    [[ -f "${OPENCLAW_JSON}.last-good.2" ]] && cp "${OPENCLAW_JSON}.last-good.2" "${OPENCLAW_JSON}.last-good.3" && log "CONFIG: last-good.2 → last-good.3"
    [[ -f "$newest" ]] && cp "$newest" "${OPENCLAW_JSON}.last-good.2" && log "CONFIG: last-good.1 → last-good.2"
    cp "$OPENCLAW_JSON" "$newest"
    log "CONFIG: 已保存 last-good.1（MD5: $(md5sum "$newest" | awk '{print $1}'))"
}

# 仅回滚配置文件到 last-good.1（不回滚、不重启，给 JSON 无效场景用）
rollback_one() {
    local newest="${OPENCLAW_JSON}.last-good.1"
    if [[ -f "$newest" ]]; then
        cp "$newest" "$OPENCLAW_JSON"
        log "CONFIG: 已回滚到 last-good.1"
        return 0
    else
        log "CONFIG: 无 last-good.1 可回滚"
        return 1
    fi
}

# 回滚到 last-good（依次尝试 last-good.1 → .2 → .3）
# 返回：0=恢复成功，1=所有 last-good 都失败
rollback_config() {
    local rolled_back=false

    for ver in 1 2 3; do
        local candidate="${OPENCLAW_JSON}.last-good.${ver}"
        if [[ ! -f "$candidate" ]]; then
            [[ "$ver" == "1" ]] && log "CONFIG: 无 last-good 可回滚（文件不存在）"
            continue
        fi

        local before_md5 after_md5
        before_md5=$(md5sum "$OPENCLAW_JSON" | awk '{print $1}')
        cp "$candidate" "$OPENCLAW_JSON"
        after_md5=$(md5sum "$OPENCLAW_JSON" | awk '{print $1}')
        log "CONFIG: 尝试回滚到 last-good.${ver}（MD5: ${after_md5}）"

        systemctl --user restart openclaw-gateway
        sleep 60
        local gw_check
        gw_check=$(check_gateway)

        if [[ "$gw_check" == "UP" ]]; then
            log "CONFIG: 回滚到 last-good.${ver} 后 Gateway 已恢复"
            return 0
        else
            log "CONFIG: last-good.${ver} 仍失败，继续尝试下一份..."
        fi
    done

    log "CONFIG: 所有 last-good（1/2/3）均回滚失败，需人工介入"
    return 1
}

# Gateway 检测
check_gateway() {
    local ws_module="${WS_MODULE:-$(detect_ws_module)}"
    node -e "
const WebSocket = require('${ws_module}');
const ws = new WebSocket('ws://127.0.0.1:${GATEWAY_PORT}', {
    headers: { 'Authorization': 'Bearer ${GATEWAY_TOKEN}' }
});
ws.on('open', () => { console.log('UP'); ws.close(); process.exit(0); });
ws.on('error', () => { console.log('DOWN'); process.exit(0); });
setTimeout(() => { console.log('DOWN'); process.exit(1); }, 4000);
" 2>/dev/null
}

check_disk() {
    df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
}

check_memory() {
    free | awk 'NR==2 {printf "%.0f\n", $3/$2 * 100}'
}

check_cpu() {
    vmstat 1 1 | awk 'NR==3 {printf "%.1f\n", 100-$15}'
}

check_process() {
    pgrep -f "openclaw" > /dev/null 2>&1 && echo "UP" || echo "DOWN"
}

# 发送飞书告警
send_alert() {
    local msg="$1"
    log "ALERT: $msg"
    echo "$(date '+%Y-%m-%d %H:%M:%S') $msg" >> "$ALERT_LOG"

    local token_resp
    token_resp=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\": \"${FEISHU_APP_ID}\", \"app_secret\": \"${FEISHU_APP_SECRET}\"}")

    local token
    token=$(echo "$token_resp" | node -e "
const data = require('fs').readFileSync('/dev/stdin', 'utf8');
try {
    const j = JSON.parse(data);
    console.log(j.tenant_access_token || '');
} catch(e) { console.log(''); }
" 2>/dev/null)

    if [[ -z "$token" ]]; then
        log "Feishu token fetch failed"
        return 1
    fi

    local send_resp
    send_resp=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: application/json" \
        -d "{\"receive_id\": \"${TARGET_OPEN_ID}\", \"msg_type\": \"text\", \"content\": \"{\\\"text\\\":\\\"${msg}\\\"}\"}")

    local code
    code=$(echo "$send_resp" | node -e "
const data = require('fs').readFileSync('/dev/stdin', 'utf8');
try {
    const j = JSON.parse(data);
    console.log(j.code || 'PARSE_ERROR');
} catch(e) { console.log('PARSE_ERROR'); }
" 2>/dev/null | tr -d '\n')

    [[ "$code" == "0" ]] && log "Feishu alert sent OK" || log "Feishu alert failed: code=$code"
}

get_fail_count() { [[ -f "$FAIL_COUNT_FILE" ]] && cat "$FAIL_COUNT_FILE" || echo "0"; }
inc_fail_count() { echo "$(($(get_fail_count) + 1))" > "$FAIL_COUNT_FILE"; echo "$(cat "$FAIL_COUNT_FILE")"; }
reset_fail_count() { echo "0" > "$FAIL_COUNT_FILE"; }

# 主循环
run_heartbeat() {
    local config_file="${1:-}"
    [[ -n "$config_file" ]] && load_config "$config_file" || load_config "$DEFAULT_CONFIG"

    mkdir -p "$LOG_DIR"
    : > "$LOG"
    log "Heartbeat daemon started (PID: $$)"

    # 启动时检查 ws_module
    WS_MODULE="${WS_MODULE:-$(detect_ws_module)}"
    log "WS module: $WS_MODULE"

    # 启动时若 Gateway 已在线，保存健康锚点
    if [[ "$(check_gateway)" == "UP" ]]; then
        save_last_good
    fi

    while true; do
        alerts=""
        gw_action_taken=false

        # Gateway
        gw=$(check_gateway)
        if [[ "$gw" != "UP" ]]; then
            local fail_count
            fail_count=$(get_fail_count)

            if [[ "$fail_count" -ge "$MAX_RESTART_FAILS" ]]; then
                log "CHECK: Gateway=DOWN，连续失败${fail_count}次，停止自动重启"
                alerts="${alerts}##【心跳告警】Gateway DOWN，连续失败${fail_count}次，已停止自动重启，请人工检查"
            else
                log "CHECK: Gateway=$gw — 第${fail_count}次失败，尝试重启..."

                backup_config

                local json_valid
                json_valid=$(validate_json)
                if [[ "$json_valid" != VALID* ]]; then
                    log "CONFIG: JSON 无效，尝试回滚 last-good.1..."
                    rollback_one
                fi

                systemctl --user restart openclaw-gateway
                sleep 60
                gw_new=$(check_gateway)

                if [[ "$gw_new" == "UP" ]]; then
                    reset_fail_count
                    log "CHECK: Gateway 已自动恢复"
                    send_alert "【心跳告警】Gateway DOWN，已自动重启恢复 ✅"
                else
                    # 重启失败：依次尝试 last-good.1 → .2 → .3，每次重启验证
                    log "CHECK: Gateway 仍 DOWN，尝试回滚 last-good（最多3个版本）..."
                    if rollback_config; then
                        reset_fail_count
                        send_alert "【心跳告警】Gateway DOWN，重启失败，已自动回滚历史配置并恢复 ✅"
                    else
                        local new_count
                        new_count=$(inc_fail_count)
                        alerts="${alerts}##【心跳告警】Gateway DOWN，所有 last-good 版本均回滚失败（${new_count}/${MAX_RESTART_FAILS}），请人工介入"
                    fi
                fi
            fi
            gw_action_taken=true
        else
            reset_fail_count
            # Gateway 稳定在线，保存已知良好配置锚点
            save_last_good
        fi

        # Disk
        disk=$(check_disk)
        if [[ "$disk" -gt "${DISK_THRESHOLD:-80}" ]]; then
            alerts="${alerts}##【心跳告警】磁盘: ${disk}% > ${DISK_THRESHOLD:-80}%"
            log "CHECK: Disk=$disk%"
        fi

        # Memory
        mem=$(check_memory)
        if [[ -n "$mem" && "$mem" -gt "${MEM_THRESHOLD:-85}" ]]; then
            alerts="${alerts}##【心跳告警】内存: ${mem}% > ${MEM_THRESHOLD:-85}%"
            log "CHECK: Memory=$mem%"
        fi

        # CPU
        cpu=$(check_cpu)
        local cpu_int=${cpu%.*}
        if [[ -n "$cpu_int" && "$cpu_int" -gt "${CPU_THRESHOLD:-60}" ]]; then
            alerts="${alerts}##【心跳告警】CPU: ${cpu}% > ${CPU_THRESHOLD:-60}%"
            log "CHECK: CPU=$cpu%"
        fi

        # Process
        proc=$(check_process)
        if [[ "$proc" != "UP" ]]; then
            alerts="${alerts}##【心跳告警】进程: ${proc}"
            log "CHECK: Process=$proc"
        fi

        # 发告警
        if [[ -n "$alerts" ]]; then
            while IFS= read -r alert; do
                alert=$(echo "$alert" | sed 's/^#*//' | sed 's/^ *//')
                [[ -n "$alert" ]] && send_alert "$alert"
            done <<< "$(echo "$alerts" | tr '#' '\n')"
        else
            log "CHECK: All healthy"
        fi

        sleep "${CHECK_INTERVAL:-180}"
    done
}

# 显示帮助
show_help() {
    echo "Infra Heartbeat Daemon"
    echo ""
    echo "用法:"
    echo "  heartbeat-daemon.sh [--config <文件>]"
    echo "  heartbeat-daemon.sh --help"
    echo ""
    echo "参数:"
    echo "  --config <文件>   指定配置文件（默认: ~/.config/infra-heartbeat/config.env）"
    echo "  --help            显示帮助"
}

case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    --config)
        shift
        run_heartbeat "$1"
        ;;
    "")
        run_heartbeat
        ;;
    *)
        echo "未知参数: $1"
        show_help
        exit 1
        ;;
esac
