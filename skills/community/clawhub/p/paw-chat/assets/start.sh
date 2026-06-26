#!/usr/bin/env bash
# Paw — 启动本地服务器并打开浏览器
cd "$(dirname "$0")"
PORT=18790

echo "🐾 Paw — http://localhost:$PORT"
echo ""

# 检查 Python
if command -v python3 &>/dev/null; then
  PY=python3
elif command -v python &>/dev/null; then
  PY=python
else
  echo "❌ 需要安装 Python 才能启动本地服务器"
  echo ""
  echo "   macOS:  系统自带 python3，或 brew install python"
  echo "   Linux:  sudo apt install python3"
  echo ""
  echo "按回车键退出..."
  read
  exit 1
fi

echo "使用 $PY ($(${PY} --version 2>&1))"
echo "按 Ctrl+C 停止服务器"
echo ""

# 打开浏览器（后台，不阻塞）
(sleep 1 && (open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null || true)) &

# 启动服务器
$PY -m http.server "$PORT" || {
  echo ""
  echo "❌ 启动失败，端口 $PORT 可能被占用，尝试其他端口..."
  PORT=8081
  echo "🐾 Paw — http://localhost:$PORT"
  (sleep 1 && (open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null || true)) &
  $PY -m http.server "$PORT" || {
    echo ""
    echo "❌ 启动失败"
    echo "按回车键退出..."
    read
    exit 1
  }
}
