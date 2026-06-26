#!/bin/bash
# 🦞 openclaw-Sys Guardian V4.1 (Metabolic Edition)
# 核心逻辑：指数退避探测 + 延迟指标上报 + 每日凌晨 03:00 深度自愈清创

# --- 配置区 ---
GATEWAY_URL="http://127.0.0.1:18789"
VAULT_DIR="$HOME/openclaw-backups-vault"
LOG_FILE="$HOME/.openclaw/lobster-guardian.log"
MAINTENANCE_MARKER="$HOME/.openclaw/.last_cleansing"

FAIL_COUNT=0
THRESHOLD=4
BASE_INTERVAL=1800 # 30 min
BACKOFF_STEPS=(60 180 300 600)

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"; }

# --- 核心引擎：深度自愈与维护 (Maintenance Mode) ---
run_maintenance() {
    # 检查是否在凌晨 03:00 窗口且今天还没跑过
    CURRENT_HOUR=$(date +%H)
    TODAY=$(date +%Y-%m-%d)
    LAST_RUN=$(cat "$MAINTENANCE_MARKER" 2>/dev/null)

    if [ "$CURRENT_HOUR" == "03" ] && [ "$TODAY" != "$LAST_RUN" ]; then
        log "[MAINTENANCE] Starting scheduled deep cleansing..."
        
        # 1. 物理配置自愈
        /opt/homebrew/bin/openclaw doctor --fix >> "$LOG_FILE" 2>&1
        log "[MAINTENANCE] Config integrity verified."

        # 2. 安全权限自动收紧
        /opt/homebrew/bin/openclaw security audit --fix >> "$LOG_FILE" 2>&1
        log "[MAINTENANCE] Security permissions hardened."

        # 3. Session 优化清理逻辑
        # 原逻辑：/opt/homebrew/bin/openclaw sessions cleanup --enforce (无差别清理)
        # 修改后：仅清理超过 48 小时未活跃或故障的 Session
        log "[MAINTENANCE] Conditional session purging started..."
        /opt/homebrew/bin/openclaw sessions cleanup --inactive-hours 48 --clean-zombies >> "$LOG_FILE" 2>&1
        log "[MAINTENANCE] Conditional session purging complete."

        # 4. 连通性测试 (轻量)
        /opt/homebrew/bin/openclaw status >> "$LOG_FILE" 2>&1
        
        echo "$TODAY" > "$MAINTENANCE_MARKER"
        log "[MAINTENANCE] Deep cleansing cycle complete."
    fi
}

# --- 核心生命体征探测 ---
check_health() {
    local start_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    local http_code=$(curl -s -m 10 -o /dev/null -w "%{http_code}" "${GATEWAY_URL}/health")
    local end_time=$(python3 -c 'import time; print(int(time.time() * 1000))')
    
    if [ "$http_code" == "200" ]; then
        echo $((end_time - start_time))
        return 0
    else
        return 1
    fi
}

self_heal_L1() {
    log "L1 Recovery: Restarting gateway..."
    lsof -ti:18789 | xargs kill -9 2>/dev/null
    /opt/homebrew/bin/openclaw gateway restart --force >> "$LOG_FILE" 2>&1
    sleep 30
}

self_heal_L2() {
    log "L2 Recovery: Rollback needed..."
    LATEST_BKP=$(ls -td ${VAULT_DIR}/daily/* | head -1)
    cp "${LATEST_BKP}/openclaw.json" "$HOME/.openclaw/"
    /opt/homebrew/bin/openclaw gateway restart --force >> "$LOG_FILE" 2>&1
    sleep 30
}

# --- 主循环 ---
log "Guardian V4.1 Metabolic Edition Started."

while true; do
    # 每次心跳先触碰维护逻辑检查
    run_maintenance

    MS_LATENCY=$(check_health)
    if [ $? -eq 0 ]; then
        FAIL_COUNT=0
        log "Heartbeat OK. Latency: ${MS_LATENCY}ms."
        sleep $BASE_INTERVAL
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        if [ $FAIL_COUNT -le $THRESHOLD ]; then
            WAIT_TIME=${BACKOFF_STEPS[$((FAIL_COUNT-1))]}
            log "ALERT: Heartbeat Lost ($FAIL_COUNT/$THRESHOLD). Retry in ${WAIT_TIME}s..."
            sleep $WAIT_TIME
        else
            self_heal_L1
            check_health > /dev/null || self_heal_L2
            FAIL_COUNT=0
            sleep $BASE_INTERVAL
        fi
    fi
done
