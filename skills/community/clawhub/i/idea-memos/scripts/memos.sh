#!/bin/bash
# 硅虾备忘录 - 服务管理脚本
# 用法: ./memos.sh {start|stop|restart|status|log|open}

DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DIR/memos.pid"
LOG_FILE="$DIR/server.log"
PORT=3377

case "$1" in
  start)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "🦐 备忘录已在运行 PID=$(cat $PID_FILE)"
      exit 0
    fi
    cd "$DIR"
    nohup node server.js > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1
    if kill -0 $! 2>/dev/null; then
      echo "✅ 已启动 → http://localhost:$PORT"
    else
      echo "❌ 启动失败，检查日志: $LOG_FILE"
      tail -5 "$LOG_FILE"
    fi
    ;;
  stop)
    if [ ! -f "$PID_FILE" ]; then
      echo "⚠️  没有运行中的服务"
      exit 0
    fi
    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
    echo "🛑 已停止"
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  status)
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
      echo "🦐 运行中 PID=$(cat $PID_FILE) → http://localhost:$PORT"
    else
      echo "🫙  未运行"
    fi
    ;;
  log)
    tail -f "$LOG_FILE"
    ;;
  open)
    xdg-open "http://localhost:$PORT" 2>/dev/null || \
      sensible-browser "http://localhost:$PORT" 2>/dev/null || \
      echo "http://localhost:$PORT"
    ;;
  *)
    echo "🦐 硅虾备忘录 管理脚本"
    echo ""
    echo "用法: $0 {start|stop|restart|status|log|open}"
    echo ""
    echo "  start   - 启动服务"
    echo "  stop    - 停止服务"
    echo "  restart - 重启"
    echo "  status  - 查看状态"
    echo "  log     - 查看日志"
    echo "  open    - 在浏览器打开"
    ;;
esac
