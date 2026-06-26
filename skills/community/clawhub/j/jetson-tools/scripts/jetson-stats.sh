#!/bin/bash
# Jetson 系统状态监控

# 检查工具是否存在
command -v tegrastats >/dev/null 2>&1 || { echo "Error: tegrastats not found"; exit 1; }

# 显示系统信息
echo "=== Jetson System Status ==="
echo ""

# CPU 信息
echo "--- CPU ---"
nproc
cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2

# 内存信息
echo ""
echo "--- Memory ---"
free -h

# 磁盘信息
echo ""
echo "--- Disk ---"
df -h / | tail -1

# GPU 状态
echo ""
echo "--- GPU Status ---"
tegrastats --interval 1000 --stop 2>/dev/null | head -5

echo ""
echo "=== Done ==="
