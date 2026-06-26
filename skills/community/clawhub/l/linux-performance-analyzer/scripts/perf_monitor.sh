#!/bin/bash
# =============================================================================
# Linux 持续性能监控脚本
# linux-perf-master skill - scripts/perf_monitor.sh
# 用途：后台持续采样关键性能指标，超阈值输出告警
# 用法：
#   bash perf_monitor.sh            # 前台运行，Ctrl+C 停止
#   bash perf_monitor.sh &          # 后台运行
#   bash perf_monitor.sh --report   # 输出汇总报告
# =============================================================================

INTERVAL=5          # 采样间隔（秒）
LOG_FILE="/tmp/perf_monitor_$(date +%Y%m%d_%H%M%S).log"
ALERT_LOG="/tmp/perf_alerts_$(date +%Y%m%d).log"

# 告警阈值
THRESH_CPU=80          # CPU 使用率 %
THRESH_MEM_FREE=10     # 内存可用率 %（低于此值告警）
THRESH_LOAD_RATIO=2    # load average / CPU核数 比值
THRESH_IOWAIT=20       # iowait %
THRESH_CS=100000       # 上下文切换次数/秒

CPU_CORES=$(nproc)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert() {
    local msg="⚠️  ALERT: $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $msg" | tee -a "$LOG_FILE" >> "$ALERT_LOG"
}

print_header() {
    log "============================================================"
    log "  Linux 性能监控启动"
    log "  CPU核数: $CPU_CORES  |  采样间隔: ${INTERVAL}s"
    log "  日志文件: $LOG_FILE"
    log "  告警文件: $ALERT_LOG"
    log "============================================================"
}

monitor_once() {
    # CPU & 负载
    local load1=$(awk '{print $1}' /proc/loadavg)
    local load5=$(awk '{print $2}' /proc/loadavg)
    local load_ratio=$(echo "$load1 $CPU_CORES" | awk '{printf "%.1f", $1/$2}')

    # 内存
    local mem_total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    local mem_avail=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    local mem_free_pct=$(echo "$mem_avail $mem_total" | awk '{printf "%d", $1*100/$2}')
    local swap_total=$(grep SwapTotal /proc/meminfo | awk '{print $2}')
    local swap_free=$(grep SwapFree /proc/meminfo | awk '{print $2}')

    # vmstat (上下文切换 & iowait)
    local vmstat_line=$(vmstat 1 2 | tail -1)
    local cs=$(echo $vmstat_line | awk '{print $12}')
    local wa=$(echo $vmstat_line | awk '{print $16}')
    local us=$(echo $vmstat_line | awk '{print $13}')
    local sy=$(echo $vmstat_line | awk '{print $14}')
    local cpu_used=$((us + sy))

    log "CPU: ${cpu_used}% (us+sy)  iowait: ${wa}%  load: ${load1}/${load5} (ratio: ${load_ratio}x)  cs/s: ${cs}  Mem可用: ${mem_free_pct}%"

    # 检查告警
    [[ $cpu_used -gt $THRESH_CPU ]] && alert "CPU 使用率过高: ${cpu_used}% > ${THRESH_CPU}%"
    [[ $mem_free_pct -lt $THRESH_MEM_FREE ]] && alert "内存可用率过低: ${mem_free_pct}% < ${THRESH_MEM_FREE}%"
    [[ $(echo "$load_ratio $THRESH_LOAD_RATIO" | awk '{print ($1 > $2)}') -eq 1 ]] && alert "负载过高: load1=${load1}, 核数=${CPU_CORES}, 比值=${load_ratio}x > ${THRESH_LOAD_RATIO}x"
    [[ $wa -gt $THRESH_IOWAIT ]] && alert "iowait 过高: ${wa}% > ${THRESH_IOWAIT}%"
    [[ $cs -gt $THRESH_CS ]] && alert "上下文切换过高: ${cs}/s > ${THRESH_CS}/s"
    if [[ $swap_total -gt 0 ]]; then
        local swap_used=$((swap_total - swap_free))
        local swap_pct=$((swap_used * 100 / swap_total))
        [[ $swap_pct -gt 30 ]] && alert "Swap 使用率过高: ${swap_pct}%"
    fi
}

print_report() {
    echo ""
    echo "============================================================"
    echo "  性能监控报告汇总"
    echo "============================================================"
    if [[ -f "$ALERT_LOG" ]]; then
        echo "告警记录："
        cat "$ALERT_LOG"
    else
        echo "无告警记录"
    fi
    echo ""
    echo "完整日志：$LOG_FILE"
}

# ── 主逻辑 ──
if [[ "$1" == "--report" ]]; then
    print_report
    exit 0
fi

print_header
trap 'echo ""; log "监控停止"; print_report; exit 0' INT TERM

while true; do
    monitor_once
    sleep "$INTERVAL"
done