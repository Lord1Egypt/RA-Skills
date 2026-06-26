#!/bin/bash

# 关键词检测脚本
# 用法: ./check-keywords.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="/root/clawd/memory/hotspots/data"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

DATE=$(date +%Y-%m-%d)

log_info() {
    echo "[INFO] $1"
}

# 检查关键词
check_keywords() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_info "未找到配置文件，跳过关键词检测"
        return
    fi
    
    local keywords=$(jq -r '.keywords[]?' "$CONFIG_FILE" 2>/dev/null)
    
    if [[ -z "$keywords" ]]; then
        log_info "暂无订阅关键词"
        return
    fi
    
    echo "🔍 检测订阅关键词..."
    echo ""
    
    while IFS= read -r keyword; do
        echo "📌 关键词: $keyword"
        
        local found=false
        
        # 检查各平台数据
        for file in "$DATA_DIR"/*_${DATE}_*.json; do
            if [[ -f "$file" ]]; then
                local platform=$(basename "$file" | cut -d'_' -f1)
                local matches=$(jq -r --arg kw "$keyword" '.data[] | select(.title | contains($kw)) | "  - \(.title)"' "$file" 2>/dev/null)
                
                if [[ -n "$matches" ]]; then
                    echo "  平台: $platform"
                    echo "$matches"
                    found=true
                fi
            fi
        done
        
        if [[ "$found" == "false" ]]; then
            echo "  (未匹配到相关热点)"
        fi
        echo ""
    done <<< "$keywords"
}

# 主函数
main() {
    # 先确保有数据
    if [[ ! -d "$DATA_DIR" ]] || [[ -z "$(ls -A $DATA_DIR 2>/dev/null)" ]]; then
        log_info "数据目录为空，先获取热点数据..."
        "$SCRIPT_DIR/fetch-hotspots.sh" all > /dev/null
    fi
    
    check_keywords
}

main
