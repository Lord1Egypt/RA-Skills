#!/bin/bash
# =============================================================================
# Linux 持续性能监控脚本
# performance-mastery skill - scripts/perf_monitor.sh
# 用途：后台持续采样关键性能指标，超阈值输出告警
# 用法：
#   bash perf_monitor.sh            # 前台运行，Ctrl+C 停止
#   bash perf_monitor.sh &          # 后台运行
#   bash perf_monitor.sh --report   # 输出汇总报告
# 注意：不使用 set -e，因为采样循环中个别命令失败不应中断持续监控
# =============================================================================

# 核心依赖检查
if ! command -v vmstat &>/dev/null; then
    echo "❌ 错误：vmstat 未安装（核心依赖），请先安装 procps 包"
    echo "   → apt install procps / yum install procps-ng"
    exit 1
fi

INTERVAL=5          # 采样间隔（秒）
LOG_FILE="${TMPDIR:-/tmp}/perf_monitor_$(date +%Y%m%d_%H%M%S).log"
ALERT_LOG="${TMPDIR:-/tmp}/perf_alerts_$(date +%Y%m%d).log"

# 告警阈值（警告级别，与 SKILL.md 告警阈值参考表对齐）
THRESH_CPU_WARN=70         # CPU 使用率 %（警告）
THRESH_CPU_CRIT=90         # CPU 使用率 %（严重）
THRESH_MEM_FREE_WARN=20    # 内存可用率 %（低于此值警告）
THRESH_MEM_FREE_CRIT=10    # 内存可用率 %（低于此值严重）
THRESH_LOAD_WARN=1.5       # load average / CPU核数 比值（警告）
THRESH_LOAD_CRIT=2         # load average / CPU核数 比值（严重）
THRESH_IOWAIT_WARN=20      # iowait %（警告）
THRESH_IOWAIT_CRIT=50      # iowait %（严重）
THRESH_CS_WARN=100000      # 上下文切换次数/秒（警告）
THRESH_CS_CRIT=500000      # 上下文切换次数/秒（严重）

CPU_CORES=$(nproc)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE" >&2
}

alert() {
    local msg="ALERT: $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $msg" | tee -a "$LOG_FILE" >&2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $msg" >> "$ALERT_LOG"
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
    local start_ts=$(date +%s)

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

    # 检查告警（双级：警告 ⚠️ + 严重 🔴）
    if [[ $cpu_used -gt $THRESH_CPU_CRIT ]]; then
        alert "🔴 CPU 使用率严重过高: ${cpu_used}% > ${THRESH_CPU_CRIT}%"
    elif [[ $cpu_used -gt $THRESH_CPU_WARN ]]; then
        alert "⚠️  CPU 使用率偏高: ${cpu_used}% > ${THRESH_CPU_WARN}%"
    fi
    if [[ $mem_free_pct -lt $THRESH_MEM_FREE_CRIT ]]; then
        alert "🔴 内存可用率严重过低: ${mem_free_pct}% < ${THRESH_MEM_FREE_CRIT}%"
    elif [[ $mem_free_pct -lt $THRESH_MEM_FREE_WARN ]]; then
        alert "⚠️  内存可用率偏低: ${mem_free_pct}% < ${THRESH_MEM_FREE_WARN}%"
    fi
    if [[ $(echo "$load_ratio $THRESH_LOAD_CRIT" | awk '{print ($1 > $2)}') -eq 1 ]]; then
        alert "🔴 负载严重过高: load1=${load1}, 核数=${CPU_CORES}, 比值=${load_ratio}x > ${THRESH_LOAD_CRIT}x"
    elif [[ $(echo "$load_ratio $THRESH_LOAD_WARN" | awk '{print ($1 > $2)}') -eq 1 ]]; then
        alert "⚠️  负载偏高: load1=${load1}, 核数=${CPU_CORES}, 比值=${load_ratio}x > ${THRESH_LOAD_WARN}x"
    fi
    if [[ $wa -gt $THRESH_IOWAIT_CRIT ]]; then
        alert "🔴 iowait 严重过高: ${wa}% > ${THRESH_IOWAIT_CRIT}%"
    elif [[ $wa -gt $THRESH_IOWAIT_WARN ]]; then
        alert "⚠️  iowait 偏高: ${wa}% > ${THRESH_IOWAIT_WARN}%"
    fi
    if [[ $cs -gt $THRESH_CS_CRIT ]]; then
        alert "🔴 上下文切换严重过高: ${cs}/s > ${THRESH_CS_CRIT}/s"
    elif [[ $cs -gt $THRESH_CS_WARN ]]; then
        alert "⚠️  上下文切换偏高: ${cs}/s > ${THRESH_CS_WARN}/s"
    fi
    if [[ $swap_total -gt 0 ]]; then
        local swap_used=$((swap_total - swap_free))
        local swap_pct=$((swap_used * 100 / swap_total))
        [[ $swap_pct -gt 30 ]] && alert "Swap 使用率过高: ${swap_pct}%"
    fi

    # 计算剩余等待时间，确保总间隔接近 INTERVAL 秒
    local end_ts=$(date +%s)
    local elapsed=$((end_ts - start_ts))
    local remaining=$((INTERVAL - elapsed))
    if [[ $remaining -gt 0 ]]; then
        sleep "$remaining"
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
done
