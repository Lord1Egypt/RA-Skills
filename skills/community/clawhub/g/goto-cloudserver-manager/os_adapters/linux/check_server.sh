#!/bin/bash
# check_server.sh - Linux 服务器状态检查
set -euo pipefail

echo "===== 系统信息 ====="
echo "主机名: $(hostname)"
echo "系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')"
echo "内核: $(uname -r)"
echo "运行时间: $(uptime -p 2>/dev/null || uptime)"
echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"

echo ""
echo "===== CPU 使用率 ====="
echo "CPU 核心数: $(nproc)"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "N/A")
echo "CPU 使用率: ${CPU_USAGE}%"
echo "负载均衡: $(cat /proc/loadavg)"

echo ""
echo "===== 内存使用 ====="
free -h

echo ""
echo "===== 磁盘使用 ====="
df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs | grep -v devtmpfs

echo ""
echo "===== 网络接口 ====="
ip addr show | grep -E "^[0-9]+:|inet " | head -20

echo ""
echo "===== 关键服务状态 ====="
SERVICES=("sshd" "firewalld" "chronyd" "rsyslog")
for svc in "${SERVICES[@]}"; do
    STATUS=$(systemctl is-active "$svc" 2>/dev/null || echo "not-found")
    echo "$svc: $STATUS"
done

echo ""
echo "===== 最近系统错误（dmesg，10条）====="
dmesg --level=err --time-format=reltime 2>/dev/null | tail -10 || dmesg | grep -i "error" | tail -10 || echo "无错误日志"

echo ""
echo "===== 检查完成 ====="
exit 0
