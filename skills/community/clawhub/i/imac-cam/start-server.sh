#!/bin/bash
# 启动 HTTP 服务器（后台运行）
mkdir -p /tmp

# 检查是否已运行
if ! lsof -i :8765 >/dev/null 2>&1; then
    cd /tmp && python3 -m http.server 8765 &
    sleep 1
fi

echo "HTTP 服务器已启动: http://192.168.3.210:8765"
