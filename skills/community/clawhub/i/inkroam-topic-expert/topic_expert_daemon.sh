#!/bin/bash
# 选题专家系统 - 守护进程启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/topic_expert.pid"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/daemon_$(date +%Y%m%d).log"

mkdir -p "$LOG_DIR"

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null 2>&1; then
                echo "❌ 选题专家已在运行 (PID: $PID)"
                exit 1
            fi
        fi
        
        echo "🚀 启动选题专家守护进程..."
        nohup python3 "$SCRIPT_DIR/scripts/scheduler.py" --mode daemon >> "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ 已启动 (PID: $(cat $PID_FILE))"
        echo "📋 日志文件: $LOG_FILE"
        ;;
    
    stop)
        if [ ! -f "$PID_FILE" ]; then
            echo "⚠️  选题专家未运行"
            exit 1
        fi
        
        PID=$(cat "$PID_FILE")
        echo "🛑 停止选题专家 (PID: $PID)..."
        kill $PID
        rm -f "$PID_FILE"
        echo "✅ 已停止"
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
                echo "✅ 选题专家正在运行 (PID: $PID)"
                echo ""
                echo "📊 进程信息："
                ps -p $PID -o pid,ppid,etime,cmd
                echo ""
                echo "📋 最新日志（最后20行）："
                tail -20 "$LOG_FILE"
            else
                echo "❌ PID 文件存在但进程未运行"
                rm -f "$PID_FILE"
            fi
        else
            echo "⚠️  选题专家未运行"
        fi
        ;;
    
    once)
        echo "🔄 运行一次数据采集..."
        python3 "$SCRIPT_DIR/scripts/scheduler.py" --mode once
        ;;
    
    report)
        echo "📧 发送每日早报..."
        python3 "$SCRIPT_DIR/scripts/scheduler.py" --daily-report
        ;;
    
    logs)
        echo "📋 实时日志（Ctrl+C 退出）："
        tail -f "$LOG_FILE"
        ;;
    
    *)
        echo "用法: $0 {start|stop|restart|status|once|report|logs}"
        echo ""
        echo "命令说明："
        echo "  start   - 启动守护进程（7×24小时运行）"
        echo "  stop    - 停止守护进程"
        echo "  restart - 重启守护进程"
        echo "  status  - 查看运行状态"
        echo "  once    - 手动运行一次数据采集"
        echo "  report  - 手动发送每日早报"
        echo "  logs    - 查看实时日志"
        exit 1
        ;;
esac
