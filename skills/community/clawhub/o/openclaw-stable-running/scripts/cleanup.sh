#!/bin/bash
#
# OpenClaw 清理脚本
# 用法: 0 3 * * * /home/openclaw/scripts/cleanup.sh
#
# 功能:
#   - 清理 7 天前的日志
#   - 清理临时文件
#   - 限制日志目录大小
#

LOG_FILE="/var/log/openclaw/cleanup.log"
LOGDIR="/var/log/openclaw"
DATADIR="/home/openclaw/data"
OPENCLAW_TMP="/tmp/openclaw"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

do_cleanup() {
    log "===== 开始清理 ====="

    # 1. 清理 7 天前的日志
    if [ -d "$LOGDIR" ]; then
        OLD_LOGS=$(find "$LOGDIR" -name "*.log" -mtime +7 -type f 2>/dev/null | wc -l)
        find "$LOGDIR" -name "*.log" -mtime +7 -type f -delete 2>/dev/null
        log "清理过期日志文件: ${OLD_LOGS} 个"
    fi

    # 2. 清理临时文件
    if [ -d "$OPENCLAW_TMP" ]; then
        OLD_TMP=$(find "$OPENCLAW_TMP" -type f -mtime +1 2>/dev/null | wc -l)
        find "$OPENCLAW_TMP" -type f -mtime +1 -delete 2>/dev/null
        log "清理临时文件: ${OLD_TMP} 个"
    fi

    # 3. 清理 node_modules 缓存（可选，注释掉）
    # npm cache clean --force 2>/dev/null

    # 4. 限制日志目录总大小（保留最新 500MB）
    if [ -d "$LOGDIR" ] && command -v du > /dev/null 2>&1; then
        TOTAL_SIZE=$(du -sm "$LOGDIR" 2>/dev/null | awk '{print $1}')
        if [ "$TOTAL_SIZE" -gt 500 ]; then
            log "日志目录超过 500MB，当前 ${TOTAL_SIZE}MB，开始精简..."
            find "$LOGDIR" -name "*.log" -type f -exec ls -lt {} + 2>/dev/null \
                | tail -n +20 | awk '{print $NF}' | xargs rm -f 2>/dev/null
            log "精简完成"
        else
            log "日志目录大小正常: ${TOTAL_SIZE}MB"
        fi
    fi

    log "===== 清理完成 ====="
}

# 运行清理
do_cleanup
