#!/bin/bash

# OpenClaw 监控告警系统快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/monitor.pid"
LOG_FILE="$SCRIPT_DIR/monitor.log"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "⚠️  监控服务已在运行 (PID: $PID)"
                exit 0
            fi
        fi
        
        echo "🚀 启动监控服务..."
        cd "$SCRIPT_DIR"
        nohup node monitor.js start > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ 监控服务已启动 (PID: $(cat $PID_FILE))"
        echo "📝 日志文件：$LOG_FILE"
        echo ""
        echo "查看日志：tail -f $LOG_FILE"
        echo "停止服务：$0 stop"
        ;;
        
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "🛑 停止监控服务 (PID: $PID)..."
                kill $PID
                rm -f "$PID_FILE"
                echo "✅ 监控服务已停止"
            else
                echo "⚠️  监控服务未运行"
                rm -f "$PID_FILE"
            fi
        else
            echo "⚠️  未找到 PID 文件，监控服务可能未运行"
        fi
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "✅ 监控服务运行中 (PID: $PID)"
                node "$SCRIPT_DIR/monitor.js" status
            else
                echo "❌ 监控服务未运行 (PID 文件存在但进程不存在)"
            fi
        else
            echo "❌ 监控服务未运行"
        fi
        ;;
        
    log)
        if [ -f "$LOG_FILE" ]; then
            tail -f "$LOG_FILE"
        else
            echo "⚠️  日志文件不存在"
        fi
        ;;
        
    *)
        echo "用法：$0 {start|stop|restart|status|log}"
        echo ""
        echo "命令:"
        echo "  start   - 启动监控服务"
        echo "  stop    - 停止监控服务"
        echo "  restart - 重启监控服务"
        echo "  status  - 查看服务状态"
        echo "  log     - 查看实时日志"
        exit 1
        ;;
esac
