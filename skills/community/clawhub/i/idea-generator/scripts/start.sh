#!/usr/bin/env bash
# 创意工作台启动脚本
# 用法: bash start.sh [端口]
# 示例: bash start.sh 51000

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PORT_FILE="$DIR/.server_port"
LOG_FILE="$DIR/server.log"

# 支持命令行传入端口
if [ -n "$1" ]; then
  echo "$1" > "$PORT_FILE"
  echo "[start] 端口设置为 $1"
fi

# 读取当前端口（用于提示）
if [ -f "$PORT_FILE" ]; then
  PORT=$(cat "$PORT_FILE")
else
  PORT=50000
  echo "$PORT" > "$PORT_FILE"
fi

# 如果已有进程在运行，先停掉
OLD_PID=$(lsof -ti :"$PORT" 2>/dev/null || true)
if [ -n "$OLD_PID" ]; then
  echo "[start] 端口 $PORT 已被占用 (PID $OLD_PID)，正在停止旧进程..."
  kill "$OLD_PID" 2>/dev/null || true
  sleep 1
fi

echo "[start] 启动创意工作台服务..."
cd "$DIR"
nohup python3 server.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# 等待服务就绪（最多 5 秒）
for i in 1 2 3 4 5; do
  sleep 1
  if curl -s "http://localhost:$PORT/" > /dev/null 2>&1; then
    echo "[start] ✅ 服务已启动 (PID $SERVER_PID)"
    echo ""
    echo "  🎨 工作台地址：http://localhost:$PORT/live-dashboard.html"
    echo ""
    exit 0
  fi
done

echo "[start] ⚠️ 服务启动超时，请查看日志：$LOG_FILE"
exit 1
