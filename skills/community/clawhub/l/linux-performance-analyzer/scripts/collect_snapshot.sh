#!/bin/bash
# =============================================================================
# Linux 系统性能快照采集脚本
# linux-perf-master skill - scripts/collect_snapshot.sh
# 用途：一键采集系统全维度性能数据，输出结构化报告
# 用法：bash collect_snapshot.sh [--output /path/to/report.txt]
# =============================================================================

OUTPUT=""
if [[ "$1" == "--output" && -n "$2" ]]; then
    OUTPUT="$2"
fi

print_section() {
    local title="$1"
    echo ""
    echo "=================================================================="
    echo "  $title"
    echo "  采集时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=================================================================="
}

run_cmd() {
    local desc="$1"
    local cmd="$2"
    echo ""
    echo "--- $desc ---"
    eval "$cmd" 2>/dev/null || echo "[命令不可用: $cmd]"
}

collect() {

# ─────────────────────────────────────────────
# 1. 基础信息
# ─────────────────────────────────────────────
print_section "系统基础信息"
run_cmd "主机名 & 内核版本" "uname -a"
run_cmd "操作系统版本" "cat /etc/os-release 2>/dev/null | grep -E 'PRETTY_NAME|VERSION_ID' || cat /etc/redhat-release 2>/dev/null"
run_cmd "CPU 信息" "lscpu | grep -E 'Model name|CPU\(s\)|Thread|Core|Socket|NUMA|MHz|Cache'"
run_cmd "内存总量" "free -h"
run_cmd "磁盘概览" "lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"
run_cmd "磁盘空间" "df -h --exclude-type=tmpfs --exclude-type=devtmpfs"
run_cmd "系统运行时间" "uptime"

# ─────────────────────────────────────────────
# 2. CPU 性能
# ─────────────────────────────────────────────
print_section "CPU 性能"
run_cmd "负载均值" "cat /proc/loadavg"
run_cmd "CPU 使用率 (各核)" "mpstat -P ALL 1 3 2>/dev/null || vmstat 1 3"
run_cmd "运行队列 & 上下文切换 (vmstat 3次)" "vmstat 1 3"
run_cmd "CPU 频率调速策略" "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo '无调速策略'"
run_cmd "CPU 密集型进程 TOP10" "ps aux --sort=-%cpu | head -11"
run_cmd "中断分布 TOP10" "cat /proc/interrupts | sort -k2 -rn | head -11"
run_cmd "软中断统计" "cat /proc/softirqs | head -20"
run_cmd "调度器统计" "cat /proc/schedstat 2>/dev/null | head -5"
run_cmd "NUMA 拓扑" "numastat 2>/dev/null | head -20 || echo 'numastat 不可用'"

# ─────────────────────────────────────────────
# 3. 内存性能
# ─────────────────────────────────────────────
print_section "内存性能"
run_cmd "内存详情" "cat /proc/meminfo"
run_cmd "Swap 信息" "swapon --show 2>/dev/null || echo '无 Swap'"
run_cmd "内存密集型进程 TOP10" "ps aux --sort=-%mem | head -11"
run_cmd "Slab 缓存" "slabtop -o 2>/dev/null | head -20 || echo 'slabtop 不可用'"
run_cmd "透明大页状态" "cat /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null"
run_cmd "HugePage 配置" "grep -i huge /proc/meminfo"
run_cmd "OOM 历史 (dmesg)" "dmesg | grep -iE 'oom|killed process' | tail -20"
run_cmd "内存 cgroup 状态" "cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null && cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null && cat /sys/fs/cgroup/memory/memory.failcnt 2>/dev/null || echo '无 cgroup 内存限制信息'"

# ─────────────────────────────────────────────
# 4. 磁盘 I/O 性能
# ─────────────────────────────────────────────
print_section "磁盘 I/O 性能"
run_cmd "I/O 统计 (iostat 3次)" "iostat -xz 1 3 2>/dev/null || echo 'iostat 不可用（建议安装 sysstat）'"
run_cmd "I/O 调度器" "for d in /sys/block/*/queue/scheduler; do echo \"\$(basename \$(dirname \$(dirname \$d))): \$(cat \$d)\"; done"
run_cmd "磁盘队列深度" "for d in /sys/block/*/queue/nr_requests; do echo \"\$(basename \$(dirname \$(dirname \$d))): \$(cat \$d)\"; done"
run_cmd "读预读配置" "for d in /sys/block/*/queue/read_ahead_kb; do echo \"\$(basename \$(dirname \$(dirname \$d))): \$(cat \$d) KB\"; done"
run_cmd "挂载选项" "mount | grep -v 'tmpfs\|proc\|sys\|dev\|cgroup'"
run_cmd "高 I/O 进程" "iotop -o -b -n 3 2>/dev/null | head -20 || echo 'iotop 不可用'"
run_cmd "磁盘健康 (smartctl)" "for d in /dev/sd? /dev/vd?; do [ -b \"\$d\" ] && smartctl -H \$d 2>/dev/null | grep -E 'result|PASSED|FAILED' && echo \"\$d\"; done 2>/dev/null || echo 'smartctl 不可用'"

# ─────────────────────────────────────────────
# 5. 网络性能
# ─────────────────────────────────────────────
print_section "网络性能"
run_cmd "连接状态统计" "ss -s"
run_cmd "TCP 连接状态分布" "ss -ant | awk '{print \$1}' | sort | uniq -c | sort -rn"
run_cmd "网络接口统计" "ip -s link"
run_cmd "网络错误/丢包统计" "netstat -s 2>/dev/null | grep -E 'fail|error|drop|overflow|reject|retransmit' | grep -v '^    0'"
run_cmd "网络接口信息" "ip addr show"
run_cmd "路由表" "ip route"
run_cmd "conntrack 状态" "cat /proc/sys/net/netfilter/nf_conntrack_count 2>/dev/null && cat /proc/sys/net/netfilter/nf_conntrack_max 2>/dev/null || echo 'conntrack 不可用'"

# ─────────────────────────────────────────────
# 6. 内核参数现状
# ─────────────────────────────────────────────
print_section "关键内核参数"
run_cmd "内存相关参数" "sysctl -a 2>/dev/null | grep -E '^vm\.' | sort"
run_cmd "网络相关参数" "sysctl -a 2>/dev/null | grep -E '^net\.(core|ipv4\.tcp|ipv4\.ip_local)' | sort"
run_cmd "调度器相关参数" "sysctl -a 2>/dev/null | grep -E '^kernel\.(sched|numa)' | sort"
run_cmd "文件描述符参数" "sysctl -a 2>/dev/null | grep -E 'fs\.file'"
run_cmd "当前文件描述符使用" "cat /proc/sys/fs/file-nr"

# ─────────────────────────────────────────────
# 7. 进程与系统调用
# ─────────────────────────────────────────────
print_section "进程与系统状态"
run_cmd "进程总数统计" "ps aux | wc -l"
run_cmd "D状态进程（不可中断睡眠）" "ps aux | awk '\$8==\"D\" {print \$0}' | head -10"
run_cmd "僵尸进程" "ps aux | awk '\$8==\"Z\" {print \$0}' | head -10"
run_cmd "打开文件数统计" "lsof 2>/dev/null | wc -l || echo 'lsof 不可用'"
run_cmd "内核日志（最近50条）" "dmesg | tail -50"

}

# 执行采集
if [[ -n "$OUTPUT" ]]; then
    collect | tee "$OUTPUT"
    echo ""
    echo "✅ 报告已保存到: $OUTPUT"
else
    collect
fi