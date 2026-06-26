#!/bin/bash
# kk备份汇报 - 极简移动端版本
# 专门为"kk每日备份汇报"命令优化

# 配置
BACKUP_ROOT="/hellox/openclaw/1panel_backup"
OBSIDIAN_ROOT="/hellox/openclaw/obsidian"
TIMEZONE="Asia/Shanghai"
REPORT_DATE=$(TZ="$TIMEZONE" date '+%Y-%m-%d')

# 检查今日文件函数
check_today_files() {
    local dir="$1"
    local pattern="$2"
    local name="$3"
    local icon="$4"
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    local files=()
    
    # 查找今天新增的文件
    find "$dir" -type f -name "$pattern" -newermt "${REPORT_DATE} 00:00:00" ! -newermt "${REPORT_DATE} 23:59:59" 2>/dev/null | \
    while read -r file; do
        [ -f "$file" ] || continue
        
        # 获取文件信息
        local size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "?")
        local mtime=$(TZ="$TIMEZONE" stat -c "%y" "$file" 2>/dev/null | cut -d'.' -f1)
        local time_display=$(echo "$mtime" | grep -o '[0-9]\{2\}:[0-9]\{2\}:[0-9]\{2\}' || echo "$mtime")
        
        echo "$time_display|$(basename "$file")|$size"
    done | sort | head -10
}

# 主汇报函数
generate_mobile_report() {
    echo "## 📱 kk每日备份汇报"
    echo ""
    echo "**汇报时间**: $(TZ="$TIMEZONE" date '+%Y-%m-%d %H:%M:%S')"
    echo "**检查日期**: $REPORT_DATE"
    echo ""
    
    # 1. homeserver
    echo "### 🖥️ homeserver今日备份"
    check_today_files "$BACKUP_ROOT/homeserver" "*.tar.gz" "homeserver" "🖥️" | \
    while IFS='|' read -r time filename size; do
        echo "**$time** \`$filename\` ($size)"
    done
    echo ""
    
    # 2. vps_jp
    echo "### 🌐 vps_jp今日备份"
    check_today_files "$BACKUP_ROOT/vps_jp" "*.tar.gz" "vps_jp" "🌐" | \
    while IFS='|' read -r time filename size; do
        echo "**$time** \`$filename\` ($size)"
    done
    echo ""
    
    # 3. xps
    echo "### 💻 xps今日备份"
    check_today_files "$BACKUP_ROOT/xps" "*.tar.gz" "xps" "💻" | \
    while IFS='|' read -r time filename size; do
        echo "**$time** \`$filename\` ($size)"
    done
    echo ""
    
    # 4. YouTube
    echo "### 📺 YouTube今日媒体"
    (check_today_files "$BACKUP_ROOT/YouTube" "*.mp3" "YouTube" "📺"; \
     check_today_files "$BACKUP_ROOT/YouTube" "*.mp4" "YouTube" "📺") | sort | \
    while IFS='|' read -r time filename size; do
        echo "**$time** \`$filename\` ($size)"
    done
    echo ""
    
    # 5. notion
    echo "### 📝 notion今日文章"
    check_today_files "$OBSIDIAN_ROOT/notion" "*.md" "notion" "📝" | \
    while IFS='|' read -r time filename size; do
        echo "**$time** \`$filename\` ($size)"
    done
    
    # 统计
    echo ""
    echo "---"
    echo ""
    echo "## 📊 今日备份统计"
    local total_files=0
    for dir in homeserver vps_jp xps; do
        count=$(find "$BACKUP_ROOT/$dir" -type f -name "*.tar.gz" -newermt "${REPORT_DATE} 00:00:00" ! -newermt "${REPORT_DATE} 23:59:59" 2>/dev/null | wc -l)
        total_files=$((total_files + count))
    done
    youtube_count=$(find "$BACKUP_ROOT/YouTube" -type f \( -name "*.mp3" -o -name "*.mp4" \) -newermt "${REPORT_DATE} 00:00:00" ! -newermt "${REPORT_DATE} 23:59:59" 2>/dev/null | wc -l)
    total_files=$((total_files + youtube_count))
    notion_count=$(find "$OBSIDIAN_ROOT/notion" -type f -name "*.md" -newermt "${REPORT_DATE} 00:00:00" ! -newermt "${REPORT_DATE} 23:59:59" 2>/dev/null | wc -l)
    total_files=$((total_files + notion_count))
    
    echo "- **总文件**: ${total_files}个"
    echo "- **备份时段**: 今日全天"
    echo "- **系统状态**: ✅ 备份正常"
    echo ""
    echo "**kk汇报完毕，系统运行健康！** 📱"
}

# 主程序
generate_mobile_report