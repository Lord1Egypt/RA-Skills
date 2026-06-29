#!/bin/bash
# health_check.sh - Linux 服务器健康检查（JSON 输出）
set -euo pipefail

# CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | tr -d '%us,' 2>/dev/null || echo "0")
LOAD=$(cat /proc/loadavg | awk '{print $1}')
CORES=$(nproc)

# 内存
MEM_TOTAL=$(free -m | awk '/^Mem:/{print $2}')
MEM_FREE=$(free -m | awk '/^Mem:/{print $4}')
MEM_USED=$(( MEM_TOTAL - MEM_FREE ))
MEM_PERCENT=$(awk "BEGIN {printf \"%.1f\", ($MEM_USED/$MEM_TOTAL)*100}")

# 磁盘
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
DISK_FREE=$(df -h / | tail -1 | awk '{print $4}')

# 服务状态
check_service() {
    systemctl is-active "$1" 2>/dev/null || echo "inactive"
}

# 健康状态
HEALTHY=true
WARNINGS=""

[ "${CPU_USAGE%.*}" -gt 90 ] 2>/dev/null && HEALTHY=false && WARNINGS="${WARNINGS}CPU使用率过高:${CPU_USAGE}%; "
[ "${MEM_PERCENT%.*}" -gt 90 ] 2>/dev/null && HEALTHY=false && WARNINGS="${WARNINGS}内存使用率过高:${MEM_PERCENT}%; "
[ "$DISK_USAGE" -gt 85 ] 2>/dev/null && WARNINGS="${WARNINGS}磁盘使用率较高:${DISK_USAGE}%; "

cat << EOF
{
  "cpu_percent": ${CPU_USAGE:-0},
  "load_1min": ${LOAD},
  "cpu_cores": ${CORES},
  "memory_total_mb": ${MEM_TOTAL},
  "memory_used_mb": ${MEM_USED},
  "memory_percent": ${MEM_PERCENT},
  "disk_root_percent": ${DISK_USAGE},
  "disk_root_free": "${DISK_FREE}",
  "healthy": ${HEALTHY},
  "warnings": "${WARNINGS}"
}
EOF
exit 0
