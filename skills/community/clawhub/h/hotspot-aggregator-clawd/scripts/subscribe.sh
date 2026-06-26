#!/bin/bash

# 关键词订阅管理脚本
# 用法: ./subscribe.sh add|list|remove <keyword>

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1"
}

# 初始化配置文件
init_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        mkdir -p "$(dirname "$CONFIG_FILE")"
        cat > "$CONFIG_FILE" << EOF
{
  "platforms": ["weibo", "baidu", "zhihu", "douyin"],
  "reportTime": "08:00",
  "keywords": [],
  "notifyChannel": ""
}
EOF
    fi
}

# 添加订阅
add_subscription() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        log_error "请提供关键词"
        exit 1
    fi
    
    # 检查是否已存在
    local exists=$(jq -r --arg kw "$keyword" '.keywords | contains([$kw])' "$CONFIG_FILE")
    if [[ "$exists" == "true" ]]; then
        log_info "关键词 '$keyword' 已在订阅列表中"
        return
    fi
    
    # 添加到列表
    jq --arg kw "$keyword" '.keywords += [$kw]' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    log_info "✅ 已添加订阅关键词: $keyword"
}

# 列出订阅
list_subscriptions() {
    local keywords=$(jq -r '.keywords[]?' "$CONFIG_FILE")
    
    if [[ -z "$keywords" ]]; then
        echo "暂无订阅关键词"
        return
    fi
    
    echo "📋 订阅关键词列表:"
    echo "$keywords" | nl
}

# 删除订阅
remove_subscription() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        log_error "请提供关键词"
        exit 1
    fi
    
    jq --arg kw "$keyword" 'del(.keywords[] | select(. == $kw))' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    log_info "✅ 已删除订阅关键词: $keyword"
}

# 主函数
main() {
    local action="${1:-list}"
    local keyword="$2"
    
    init_config
    
    case "$action" in
        add)
            add_subscription "$keyword"
            ;;
        list)
            list_subscriptions
            ;;
        remove)
            remove_subscription "$keyword"
            ;;
        *)
            echo "用法: $0 add|list|remove <keyword>"
            exit 1
            ;;
    esac
}

main "$@"
