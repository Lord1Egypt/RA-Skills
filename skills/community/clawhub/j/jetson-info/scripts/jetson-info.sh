#!/bin/bash
# Jetson 设备信息

echo "=== Jetson Device Info ==="

# 检查工具
if command -v jetson_release &> /dev/null; then
    jetson_release
else
    echo "jetson_release not found"
fi
