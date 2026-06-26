#!/bin/sh
# QNX CPU监控脚本 - 日志模式带色彩

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 配置参数
INTERVAL=3
LOG_DIR="/userdata/log/cpu_monitor"
LOG_FILE="${LOG_DIR}/cpu_monitor_$(date '+%Y%m%d_%H%M%S').log"
MAX_LOG_DAYS=7  # 保留7天日志

# 创建日志目录
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
fi

# 清理旧日志
clean_old_logs() {
    find "$LOG_DIR" -name "cpu_monitor_*.log" -type f -mtime +$MAX_LOG_DAYS -delete 2>/dev/null
}

# 写入日志函数
write_log() {
    echo "$1" | tee -a "$LOG_FILE"
}

# 带颜色的写入
write_color_log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# 获取CPU负载颜色
get_cpu_color() {
    CPU_IDLE=$(pidin info 2>/dev/null | grep "CPU:" | grep -o "[0-9]\+% idle" | sed 's/% idle//')
    if [ -n "$CPU_IDLE" ]; then
        CPU_USED=$((100 - CPU_IDLE))
        if [ $CPU_USED -gt 80 ]; then
            echo "$RED"
        elif [ $CPU_USED -gt 50 ]; then
            echo "$YELLOW"
        else
            echo "$GREEN"
        fi
    else
        echo "$NC"
    fi
}

# 清理函数
cleanup() {
    write_color_log "\n${GREEN}监控已停止，日志保存至: $LOG_FILE${NC}"
    exit 0
}
trap cleanup INT TERM

# 初始化日志
write_color_log "${CYAN}════════════════════════════════════════════════════════════════${NC}"
write_color_log "${CYAN}              QNX CPU监控启动 - $(date '+%Y-%m-%d %H:%M:%S')${NC}"
write_color_log "${CYAN}════════════════════════════════════════════════════════════════${NC}"
write_log ""

# 主循环
while true; do
    # 清理旧日志
    clean_old_logs

    # 获取当前时间
    CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

    # 写入时间分隔线
    write_log ""
    write_color_log "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    write_color_log "${YELLOW}                      ${CURRENT_TIME}${NC}"
    write_color_log "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    write_log ""

    # 系统概要
    write_color_log "${BLUE}【系统概要】${NC}"
    pidin info 2>/dev/null | head -5 | while read line; do
        write_log "  $line"
    done
    write_log ""

    # CPU负载颜色
    CPU_COLOR=$(get_cpu_color)

    # hogs CPU排名前15
    write_color_log "${PURPLE}【hogs CPU占用 TOP 15】${NC}"
    write_log "PID      CPU%    MEM     STACK   PATH"
    write_log "─────────────────────────────────────────────────"
    hogs -l 256 2>/dev/null | grep -v "CPU%" | head -15 | \
    while read pid name cpu mem stack rest; do
        if [ -n "$pid" ]; then
            CPU_VAL=$(echo "$cpu" | sed 's/%//')
            if [ -n "$CPU_VAL" ] && [ "$CPU_VAL" -gt 20 ] 2>/dev/null; then
                printf "${RED}%-8s %-6s %-8s %-8s %s${NC}\n" "$pid" "$cpu" "$mem" "$stack" "$name" | tee -a "$LOG_FILE"
            else
                printf "%-8s %-6s %-8s %-8s %s\n" "$pid" "$cpu" "$mem" "$stack" "$name" >> "$LOG_FILE"
                printf "%-8s %-6s %-8s %-8s %s\n" "$pid" "$cpu" "$mem" "$stack" "$name"
            fi
        fi
    done
    write_log ""

    # hogs 内存排名前15
    write_color_log "${GREEN}【hogs 内存占用 TOP 15】${NC}"
    write_log "PID      MEM     CPU%    STACK   PATH"
    write_log "─────────────────────────────────────────────────"
    hogs -l 256 -S m 2>/dev/null | grep -v "CPU%" | head -15 | \
    while read pid name cpu mem stack rest; do
        if [ -n "$pid" ]; then
            MEM_VAL=$(echo "$mem" | sed 's/[kM]//g')
            if [ -n "$MEM_VAL" ] && [ "$MEM_VAL" -gt 10000 ] 2>/dev/null; then
                printf "${YELLOW}%-8s %-8s %-6s %-8s %s${NC}\n" "$pid" "$mem" "$cpu" "$stack" "$name" | tee -a "$LOG_FILE"
            else
                printf "%-8s %-8s %-6s %-8s %s\n" "$pid" "$mem" "$cpu" "$stack" "$name" >> "$LOG_FILE"
                printf "%-8s %-8s %-6s %-8s %s\n" "$pid" "$mem" "$cpu" "$stack" "$name"
            fi
        fi
    done
    write_log ""

    # top输出
    write_color_log "${CYAN}【top 进程状态】${NC}"
    top -b -i 1 -z 15 -D 1 2>/dev/null | while read line; do
        write_log "  $line"
    done
    write_log ""

    # CPU核心状态
    write_color_log "${BLUE}【CPU核心状态】${NC}"
    top -b -i 1 -z 5 -D 1 2>/dev/null | grep -A 4 "Idle:" | while read line; do
        write_log "  $line"
    done
    write_log ""

    # 统计信息
    write_color_log "${YELLOW}【统计摘要】${NC}"

    # 总进程数
    PROC_COUNT=$(pidin info 2>/dev/null | grep "Processes:" | grep -o "[0-9]\+")
    THREAD_COUNT=$(pidin info 2>/dev/null | grep "Threads:" | grep -o "[0-9]\+")
    write_log "  进程数: ${PROC_COUNT:-N/A}, 线程数: ${THREAD_COUNT:-N/A}"

    # 内存使用
    MEM_INFO=$(pidin info 2>/dev/null | grep "FreeMem:")
    write_log "  内存: $MEM_INFO"
    write_log ""

    # 日志位置提示
    write_color_log "${GREEN}日志保存至: $LOG_FILE${NC}"
    write_color_log "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # 等待刷新
    sleep $INTERVAL
done
