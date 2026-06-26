#!/bin/bash

# AI 服务管理脚本
# 用法: start_ai.sh [start|stop|status|restart]

export HF_ENDPOINT=https://hf-mirror.com
LOG_DIR=~/.openclaw/logs
mkdir -p "$LOG_DIR"

check_embedding() {
    curl -s http://localhost:8081/health > /dev/null 2>&1
}

check_chat() {
    curl -s http://localhost:8080/v1/models > /dev/null 2>&1
}

start_services() {
    echo "🚀 启动 AI 服务..."
    source ~/mlx-env/bin/activate
    
    # Embedding 服务
    if check_embedding; then
        echo "✅ Embedding 服务已运行 (端口 8081)"
    else
        echo "📊 启动 Embedding 服务..."
        nohup python ~/embedding_server.py > "$LOG_DIR/embedding.log" 2>&1 &
        sleep 3
        if check_embedding; then
            echo "✅ Embedding 服务启动成功"
        else
            echo "❌ Embedding 服务启动失败"
        fi
    fi
    
    # Chat 服务
    if check_chat; then
        echo "✅ Chat 服务已运行 (端口 8080)"
    else
        echo "💬 启动 Chat 服务 (mlx-community/Qwen3.5-4B-OptiQ-4bit)..."
        nohup python -m mlx_lm.server \
            --model mlx-community/Qwen3.5-4B-OptiQ-4bit \
            --trust-remote-code \
            --temp 0.3 \
            --chat-template-args '{"enable_thinking": false}' \
            --port 8080 > "$LOG_DIR/chat.log" 2>&1 &
        sleep 5
        if check_chat; then
            echo "✅ Chat 服务启动成功"
        else
            echo "❌ Chat 服务启动失败，查看日志: $LOG_DIR/chat.log"
        fi
    fi
}

stop_services() {
    echo "🛑 停止 AI 服务..."
    
    # 停止 Chat 服务
    if pgrep -f "mlx_lm.server" > /dev/null; then
        pkill -f "mlx_lm.server"
        echo "✅ Chat 服务已停止"
    else
        echo "ℹ️  Chat 服务未运行"
    fi
    
    # 停止 Embedding 服务
    if pgrep -f "embedding_server.py" > /dev/null; then
        pkill -f "embedding_server.py"
        echo "✅ Embedding 服务已停止"
    else
        echo "ℹ️  Embedding 服务未运行"
    fi
}

show_status() {
    echo "📊 AI 服务状态"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Embedding 服务
    if check_embedding; then
        INFO=$(curl -s http://localhost:8081/health 2>/dev/null)
        MEM_COUNT=$(echo "$INFO" | jq -r '.memory_count // "N/A"' 2>/dev/null)
        echo "Embedding (8081): ✅ 运行中 ($MEM_COUNT 条记忆)"
    else
        echo "Embedding (8081): ❌ 未运行"
    fi
    
    # Chat 服务
    if check_chat; then
        MODEL=$(curl -s http://localhost:8080/v1/models 2>/dev/null | jq -r '.data[0].id // "unknown"' 2>/dev/null)
        echo "Chat (8080):      ✅ 运行中 ($MODEL)"
    else
        echo "Chat (8080):      ❌ 未运行"
    fi
    
    echo ""
    echo "日志目录: $LOG_DIR"
}

case "${1:-}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    status)
        show_status
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        ;;
    "")
        start_services
        ;;
    *)
        echo "用法: $0 [start|stop|status|restart]"
        echo ""
        echo "  start   - 启动所有服务 (默认)"
        echo "  stop    - 停止所有服务"
        echo "  status  - 查看服务状态"
        echo "  restart - 重启所有服务"
        exit 1
        ;;
esac
