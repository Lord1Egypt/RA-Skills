#!/usr/bin/env bash
# 启动本地 PRD 原型与打点持久化服务。
# 只读预览可用: python3 -m http.server 3000

if command -v node >/dev/null 2>&1; then
  node server.js
else
  echo "未检测到 Node.js。只读预览请执行: python3 -m http.server 3000"
fi
