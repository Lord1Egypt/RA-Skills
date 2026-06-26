#!/bin/bash

# Port Manager - 端口管理脚本

PORTS_FILE="$HOME/.openclaw/workspace/skills/port-manager/.data/ports.json"

# 初始化文件
init_file() {
    if [ ! -f "$PORTS_FILE" ]; then
        mkdir -p "$(dirname "$PORTS_FILE")"
        echo '{"services": []}' > "$PORTS_FILE"
    fi
}

# 记录端口
record() {
    init_file
    local service=$1
    local port=$2
    
    if [ -z "$service" ] || [ -z "$port" ]; then
        echo "用法: port record <服务名> <端口>"
        return 1
    fi
    
    # 检查端口是否已被占用
    local pid=$(lsof -t -i :$port 2>/dev/null)
    local existing_service=""
    
    if [ -n "$pid" ]; then
        existing_service=$(ps -p $pid - comm= 2>/dev/null | head -1)
        echo "⚠️  端口 $port 已被占用 (PID: $pid, 进程: $existing_service)"
    fi
    
    # 使用 jq 更新 JSON
    local temp=$(mktemp)
    jq --arg service "$service" --arg port "$port" \
        '.services |= map(select(.service != $service)) + [{"service": $service, "port": $port, "recorded_at": now | strftime("%Y-%m-%d %H:%M:%S")}]' \
        "$PORTS_FILE" > "$temp" && mv "$temp" "$PORTS_FILE"
    
    echo "✅ 已记录: $service -> 端口 $port"
}

# 列出所有端口
list() {
    init_file
    echo "📋 已记录的端口:"
    echo ""
    jq -r '.services[] | "  \(.service): 端口 \(.port) (记录于: \(.recorded_at))"' "$PORTS_FILE"
    echo ""
    echo "📡 当前系统端口占用:"
    echo ""
    lsof -i -P -n 2>/dev/null | grep LISTEN | awk '{print "  端口 " $9 " -> " $1 " (PID: " $2 ")"}' | sed 's/.*: //' | sort -u
}

# 查询端口
query() {
    local port=$1
    
    if [ -z "$port" ]; then
        echo "用法: port query <端口>"
        return 1
    fi
    
    echo "🔍 端口 $port 占用情况:"
    
    # 检查系统
    local info=$(lsof -i :$port 2>/dev/null)
    if [ -n "$info" ]; then
        echo "$info"
    else
        echo "  当前没有被占用"
    fi
    
    # 检查记录
    local recorded=$(jq -r --arg port "$port" '.services[] | select(.port == $port) | .service' "$PORTS_FILE" 2>/dev/null)
    if [ -n "$recorded" ]; then
        echo "  已记录的服务: $recorded"
    fi
}

# 释放端口
free() {
    local port=$1
    
    if [ -z "$port" ]; then
        echo "用法: port free <端口>"
        return 1
    fi
    
    # 获取占用进程
    local pid=$(lsof -t -i :$port 2>/dev/null)
    
    if [ -z "$pid" ]; then
        echo "端口 $port 没有被占用"
        return 1
    fi
    
    local pname=$(ps -p $pid - comm= 2>/dev/null | head -1)
    echo "⚠️  端口 $port 被 $pname (PID: $pid) 占用"
    echo "是否释放? (y/n)"
    
    read -r confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        kill $pid
        echo "✅ 已释放端口 $port (终止了进程 $pid)"
    else
        echo "❌ 已取消"
    fi
}

# 检查端口
check() {
    local port=$1
    
    if [ -z "$port" ]; then
        echo "用法: port check <端口>"
        return 1
    fi
    
    local pid=$(lsof -t -i :$port 2>/dev/null)
    
    if [ -n "$pid" ]; then
        local pname=$(ps -p $pid - comm= 2>/dev/null | head -1)
        echo "⚠️  端口 $port 已被占用!"
        echo "  进程: $pname (PID: $pid)"
        
        # 查找记录
        local recorded=$(jq -r --arg port "$port" '.services[] | select(.port == $port) | .service' "$PORTS_FILE" 2>/dev/null)
        if [ -n "$recorded" ]; then
            echo "  已记录的服务: $recorded"
        fi
        
        echo ""
        echo "是否释放此端口? (y/n)"
        read -r confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            free $port
        fi
    else
        echo "✅ 端口 $port 可用"
    fi
}

# 自动分配端口
allocate() {
    local service=$1
    local preferred=$2
    
    if [ -z "$service" ]; then
        echo "用法: port allocate <服务名> [首选端口]"
        return 1
    fi
    
    local port=$preferred
    
    # 如果没有首选，随机一个
    if [ -z "$port" ]; then
        port=$((8000 + RANDOM % 1000))
    fi
    
    # 检查端口
    while true; do
        if lsof -t -i :$port >/dev/null 2>&1; then
            if [ -n "$preferred" ]; then
                echo "⚠️  首选端口 $port 被占用"
            fi
            port=$((port + 1))
            if [ $port -gt 9000 ]; then
                echo "❌ 无法找到可用端口"
                return 1
            fi
        else
            break
        fi
    done
    
    echo "✅ 为 $service 分配端口: $port"
    record $service $port
}

# 主命令
case "$1" in
    record)
        record "$2" "$3"
        ;;
    list)
        list
        ;;
    query)
        query "$2"
        ;;
    free)
        free "$2"
        ;;
    check)
        check "$2"
        ;;
    allocate)
        allocate "$2" "$3"
        ;;
    *)
        echo "Port Manager - 端口管理工具"
        echo ""
        echo "用法: port <命令> [参数]"
        echo ""
        echo "命令:"
        echo "  record <服务名> <端口>   记录端口占用"
        echo "  list                      列出所有记录的端口"
        echo "  query <端口>              查询端口占用情况"
        echo "  free <端口>               释放指定端口"
        echo "  check <端口>             检查端口并询问是否释放"
        echo "  allocate <服务名> [端口]  自动分配可用端口"
        ;;
esac
