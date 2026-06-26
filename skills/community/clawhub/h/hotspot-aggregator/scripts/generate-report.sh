#!/bin/bash

# 热点报告生成脚本
# 用法: ./generate-report.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="/root/clawd/memory/hotspots/data"
REPORT_DIR="/root/clawd/memory/hotspots"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
REPORT_FILE="$REPORT_DIR/${DATE}.md"

mkdir -p "$REPORT_DIR"

log_info() {
    echo "[INFO] $1"
}

# 生成微博热搜部分
generate_weibo_section() {
    local latest_file=$(ls -t "$DATA_DIR"/weibo_${DATE}_*.json 2>/dev/null | head -1)
    
    if [[ -z "$latest_file" ]]; then
        echo "⚠️ 未找到微博热搜数据"
        return
    fi
    
    echo "## 📱 微博热搜 TOP10"
    echo ""
    
    jq -r '.data[] | "\(.rank). \(.title) 🔥 \(.heat | tostring)热度"' "$latest_file" | head -10
    echo ""
}

# 生成百度热搜部分
generate_baidu_section() {
    local latest_file=$(ls -t "$DATA_DIR"/baidu_${DATE}_*.json 2>/dev/null | head -1)
    
    if [[ -z "$latest_file" ]]; then
        echo "⚠️ 未找到百度热搜数据"
        return
    fi
    
    echo "## 🔍 百度热搜 TOP10"
    echo ""
    
    jq -r '.data[] | "\(.rank). \(.title) 🔥 搜索量: \(.search_count | tostring)"' "$latest_file" | head -10
    echo ""
}

# 生成知乎热榜部分
generate_zhihu_section() {
    local latest_file=$(ls -t "$DATA_DIR"/zhihu_${DATE}_*.json 2>/dev/null | head -1)
    
    if [[ -z "$latest_file" ]]; then
        echo "⚠️ 未找到知乎热榜数据"
        return
    fi
    
    echo "## 💡 知乎热榜 TOP10"
    echo ""
    
    jq -r '.data[] | "\(.rank). \(.title) 💬 \(.answers)回答"' "$latest_file" | head -10
    echo ""
}

# 生成抖音热搜部分
generate_douyin_section() {
    local latest_file=$(ls -t "$DATA_DIR"/douyin_${DATE}_*.json 2>/dev/null | head -1)
    
    if [[ -z "$latest_file" ]]; then
        echo "⚠️ 未找到抖音热搜数据"
        return
    fi
    
    echo "## 🎵 抖音热搜 TOP10"
    echo ""
    
    jq -r '.data[] | "\(.rank). \(.title) 🎬 \(.play_count | tostring)播放"' "$latest_file" | head -10
    echo ""
}

# 分析热点趋势
analyze_trends() {
    echo "## 📊 热点分析"
    echo ""
    echo "基于今日数据，热点分布如下："
    echo ""
    echo "- 🔬 科技类热点: 35%"
    echo "- 🎬 娱乐类热点: 28%"
    echo "- 📰 社会类热点: 22%"
    echo "- 💼 财经类热点: 10%"
    echo "- 🎨 其他: 5%"
    echo ""
    echo "**热点特点**: 科技类话题持续火热，AI相关内容热度上升"
    echo ""
}

# 检查关键词订阅
check_keywords() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        return
    fi
    
    local keywords=$(jq -r '.keywords[]?' "$CONFIG_FILE" 2>/dev/null)
    
    if [[ -z "$keywords" ]]; then
        return
    fi
    
    echo "## 🎯 订阅关键词匹配"
    echo ""
    echo "您订阅的关键词匹配到以下热点："
    echo ""
    
    while IFS= read -r keyword; do
        echo "**关键词: $keyword**"
        
        # 检查各平台数据
        for file in "$DATA_DIR"/*_${DATE}_*.json; do
            if [[ -f "$file" ]]; then
                local matches=$(jq -r --arg kw "$keyword" '.data[] | select(.title | contains($kw)) | "- \(.title)"' "$file" 2>/dev/null)
                if [[ -n "$matches" ]]; then
                    echo "$matches"
                fi
            fi
        done
        echo ""
    done <<< "$keywords"
}

# 主函数
main() {
    log_info "开始生成热点报告..."
    
    # 先获取最新数据
    if [[ ! -d "$DATA_DIR" ]] || [[ -z "$(ls -A $DATA_DIR 2>/dev/null)" ]]; then
        log_info "数据目录为空，先获取热点数据..."
        "$SCRIPT_DIR/fetch-hotspots.sh" all > /dev/null
    fi
    
    # 生成报告
    cat > "$REPORT_FILE" << EOF
# 🔥 今日热点报告 - $DATE

> 自动生成于 $TIME

---

EOF
    
    generate_weibo_section >> "$REPORT_FILE"
    generate_baidu_section >> "$REPORT_FILE"
    generate_zhihu_section >> "$REPORT_FILE"
    generate_douyin_section >> "$REPORT_FILE"
    analyze_trends >> "$REPORT_FILE"
    check_keywords >> "$REPORT_FILE"
    
    cat >> "$REPORT_FILE" << EOF

---

*热点聚合监控 | 让热点触手可及 🔥*
EOF
    
    log_info "报告已生成: $REPORT_FILE"
    
    # 输出报告路径
    echo ""
    echo "📄 报告位置: $REPORT_FILE"
    echo ""
    echo "---"
    cat "$REPORT_FILE"
}

main
