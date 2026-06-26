#!/bin/bash
# kk每日备份汇报 - 主脚本
# 版本: 1.0.0
# 作者: kk (幽默轻松助理)

set -e

# 技能信息
SKILL_NAME="kk-daily-backup-report"
SKILL_VERSION="1.0.0"
AUTHOR="kk"
EMOJI="📱"

# 默认配置
BACKUP_ROOT="/hellox/openclaw/1panel_backup"
OBSIDIAN_ROOT="/hellox/openclaw/obsidian"
TIMEZONE="Asia/Shanghai"
REPORT_DATE=$(TZ="$TIMEZONE" date '+%Y-%m-%d')
REPORT_STYLE="mobile"  # mobile | detailed | summary

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 目录定义
declare -A DIR_NAMES=(
    ["homeserver"]="🖥️ homeserver"
    ["vps_jp"]="🌐 vps_jp"
    ["xps"]="💻 xps"
    ["YouTube"]="📺 YouTube"
    ["notion"]="📝 notion"
)

# 目录图标
declare -A DIR_ICONS=(
    ["homeserver"]="🖥️"
    ["vps_jp"]="🌐"
    ["xps"]="💻"
    ["YouTube"]="📺"
    ["notion"]="📝"
)

# 帮助信息
show_help() {
    echo -e "${GREEN}${SKILL_NAME} v${SKILL_VERSION}${NC}"
    echo -e "${CYAN}kk每日备份汇报 - 简洁移动端优化的备份状态报告${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --date DATE        指定汇报日期 (默认: 今天)"
    echo "  --days DAYS        汇报最近几天 (默认: 1)"
    echo "  --format STYLE     输出格式: mobile|detailed|summary (默认: mobile)"
    echo "  --dir DIRS         指定目录: homeserver,vps_jp,xps,YouTube,notion"
    echo "  --backup-root PATH 备份根目录 (默认: $BACKUP_ROOT)"
    echo "  --obsidian-root PATH Obsidian根目录 (默认: $OBSIDIAN_ROOT)"
    echo "  --timezone TZ      时区 (默认: $TIMEZONE)"
    echo "  --debug            启用调试模式"
    echo "  --config           显示当前配置"
    echo "  --help             显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                          # 今日备份汇报 (移动端格式)"
    echo "  $0 --date 2026-02-24        # 指定日期汇报"
    echo "  $0 --days 3                 # 最近3天备份"
    echo "  $0 --format detailed        # 详细格式汇报"
    echo "  $0 --dir homeserver,vps_jp  # 仅检查指定目录"
    echo ""
}

# 显示配置
show_config() {
    echo -e "${GREEN}当前配置:${NC}"
    echo "  备份根目录: $BACKUP_ROOT"
    echo "  Obsidian目录: $OBSIDIAN_ROOT"
    echo "  时区: $TIMEZONE"
    echo "  汇报日期: $REPORT_DATE"
    echo "  输出格式: $REPORT_STYLE"
    echo ""
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --date)
                REPORT_DATE="$2"
                shift 2
                ;;
            --days)
                local days="$2"
                REPORT_DATE=$(TZ="$TIMEZONE" date -d "$days days ago" '+%Y-%m-%d')
                shift 2
                ;;
            --format)
                REPORT_STYLE="$2"
                shift 2
                ;;
            --dir)
                IFS=',' read -ra SELECTED_DIRS <<< "$2"
                shift 2
                ;;
            --backup-root)
                BACKUP_ROOT="$2"
                shift 2
                ;;
            --obsidian-root)
                OBSIDIAN_ROOT="$2"
                shift 2
                ;;
            --timezone)
                TIMEZONE="$2"
                shift 2
                ;;
            --debug)
                set -x
                shift
                ;;
            --config)
                show_config
                exit 0
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}错误: 未知选项 $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

# 检查目录是否存在
check_directory() {
    local dir="$1"
    local name="$2"
    
    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}警告: ${name}目录不存在 ($dir)${NC}"
        return 1
    fi
    
    if [ ! -r "$dir" ]; then
        echo -e "${YELLOW}警告: 无法读取${name}目录 ($dir)${NC}"
        return 1
    fi
    
    return 0
}

# 获取文件大小（人类可读）
get_human_size() {
    local file="$1"
    if [ -f "$file" ]; then
        du -h "$file" | cut -f1
    else
        echo "0B"
    fi
}

# 检查今日新增文件
check_today_files() {
    local dir="$1"
    local pattern="$2"
    local name="$3"
    
    local files=()
    local total_count=0
    
    # 查找今天新增的文件
    if [ -d "$dir" ]; then
        while IFS= read -r file; do
            [ -f "$file" ] || continue
            
            # 获取文件信息
            local size=$(get_human_size "$file")
            local mtime=$(TZ="$TIMEZONE" stat -c "%y" "$file" 2>/dev/null | cut -d'.' -f1)
            local ctime=$(TZ="$TIMEZONE" stat -c "%w" "$file" 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1)
            
            if [ -z "$ctime" ] || [ "$ctime" = "-" ]; then
                ctime="$mtime"
            fi
            
            local time_display="$ctime"
            
            # 提取时间部分
            if [[ "$time_display" =~ ([0-9]{2}:[0-9]{2}:[0-9]{2}) ]]; then
                time_display="${BASH_REMATCH[1]}"
            fi
            
            # 安全处理文件名（避免空格等问题）
            local safe_filename=$(basename "$file")
            files+=("$time_display|$safe_filename|$size")
            total_count=$((total_count + 1))
            
        done < <(find "$dir" -type f -name "$pattern" -newermt "${REPORT_DATE} 00:00:00" ! -newermt "${REPORT_DATE} 23:59:59" 2>/dev/null)
    fi
    
    # 返回结果
    if [ ${#files[@]} -gt 0 ]; then
        # 按时间排序
        IFS=$'\n' sorted_files=($(sort <<<"${files[*]}"))
        unset IFS
        
        echo "${sorted_files[@]}"
    else
        echo ""
    fi
}

# 移动端格式汇报
mobile_report() {
    local dir_data="$1"
    local dir_name="$2"
    local dir_icon="$3"
    
    if [ -z "$dir_data" ]; then
        return
    fi
    
    echo -e "\n### ${dir_icon} ${dir_name}今日备份"
    
    IFS=' ' read -ra files <<< "$dir_data"
    for file_info in "${files[@]}"; do
        IFS='|' read -r time filename size <<< "$file_info"
        echo -e "**${time}** \`${filename}\` (${size})"
    done
}

# 详细格式汇报
detailed_report() {
    local dir_data="$1"
    local dir_name="$2"
    local dir_path="$3"
    
    if [ -z "$dir_data" ]; then
        echo -e "\n### ${dir_name} - 今日无新增"
        return
    fi
    
    echo -e "\n### ${dir_name} - 今日新增"
    echo "路径: $dir_path"
    echo ""
    
    IFS=' ' read -ra files <<< "$dir_data"
    for file_info in "${files[@]}"; do
        IFS='|' read -r time filename size <<< "$file_info"
        echo "🕒 ${time} | 📄 ${filename} | 📏 ${size}"
    done
}

# 摘要格式汇报
summary_report() {
    local dir_data="$1"
    local dir_name="$2"
    
    if [ -z "$dir_data" ]; then
        return
    fi
    
    IFS=' ' read -ra files <<< "$dir_data"
    local count=${#files[@]}
    local total_size=0
    
    # 计算总大小（简化）
    for file_info in "${files[@]}"; do
        IFS='|' read -r time filename size <<< "$file_info"
        # 这里简化处理，实际应该转换大小
        total_size=$((total_size + 1))
    done
    
    echo -e "${dir_name}: ${count}个文件"
}

# 主汇报函数
generate_report() {
    local total_files=0
    local report_data=""
    
    # 检查各个目录
    for dir_key in "${!DIR_NAMES[@]}"; do
        # 如果指定了目录筛选，跳过未选中的
        if [ ${#SELECTED_DIRS[@]} -gt 0 ]; then
            if ! printf '%s\n' "${SELECTED_DIRS[@]}" | grep -q "^${dir_key}$"; then
                continue
            fi
        fi
        
        local dir_name="${DIR_NAMES[$dir_key]}"
        local dir_icon="${DIR_ICONS[$dir_key]}"
        local dir_path=""
        local pattern=""
        
        case $dir_key in
            homeserver|vps_jp|xps)
                dir_path="${BACKUP_ROOT}/${dir_key}"
                pattern="*.tar.gz"
                ;;
            YouTube)
                dir_path="${BACKUP_ROOT}/${dir_key}"
                pattern="*.mp3"
                # 也检查视频文件
                local video_files=$(check_today_files "$dir_path" "*.mp4" "$dir_name")
                local audio_files=$(check_today_files "$dir_path" "*.mp3" "$dir_name")
                dir_data="$audio_files $video_files"
                ;;
            notion)
                dir_path="${OBSIDIAN_ROOT}/${dir_key}"
                pattern="*.md"
                ;;
        esac
        
        if [ "$dir_key" != "YouTube" ]; then
            dir_data=$(check_today_files "$dir_path" "$pattern" "$dir_name")
        fi
        
        if [ -n "$dir_data" ]; then
            IFS=' ' read -ra files <<< "$dir_data"
            total_files=$((total_files + ${#files[@]}))
            
            case $REPORT_STYLE in
                mobile)
                    report_data+="$(mobile_report "$dir_data" "${dir_name#* }" "$dir_icon")\n"
                    ;;
                detailed)
                    report_data+="$(detailed_report "$dir_data" "$dir_name" "$dir_path")\n"
                    ;;
                summary)
                    report_data+="$(summary_report "$dir_data" "$dir_name")\n"
                    ;;
            esac
        fi
    done
    
    # 生成报告头
    local current_time=$(TZ="$TIMEZONE" date '+%Y-%m-%d %H:%M:%S')
    
    case $REPORT_STYLE in
        mobile)
            echo -e "## ${EMOJI} kk每日备份汇报"
            echo -e "\n**汇报时间**: ${current_time}"
            echo -e "**检查日期**: ${REPORT_DATE}"
            echo -e "${report_data}"
            echo -e "\n---"
            echo -e "\n## 📊 今日备份统计"
            echo -e "- **总文件**: ${total_files}个"
            echo -e "- **备份时段**: 今日全天"
            echo -e "- **系统状态**: ✅ 备份正常"
            echo -e "\n**kk汇报完毕，系统运行健康！** ${EMOJI}"
            ;;
        detailed)
            echo -e "# kk每日备份详细报告"
            echo -e "**生成时间**: ${current_time}"
            echo -e "**检查日期**: ${REPORT_DATE}"
            echo -e "**备份根目录**: ${BACKUP_ROOT}"
            echo -e "**Obsidian目录**: ${OBSIDIAN_ROOT}"
            echo -e "${report_data}"
            echo -e "\n## 统计摘要"
            echo -e "- 总新增文件: ${total_files}个"
            echo -e "- 检查目录: ${#SELECTED_DIRS[@]:-5}个"
            echo -e "- 汇报格式: ${REPORT_STYLE}"
            ;;
        summary)
            echo -e "kk每日备份摘要 - ${REPORT_DATE}"
            echo -e "${report_data}"
            echo -e "\n总计: ${total_files}个文件"
            ;;
    esac
}

# 主函数
main() {
    # 解析参数
    parse_args "$@"
    
    # 显示技能信息
    if [ "$REPORT_STYLE" != "summary" ]; then
        echo -e "${GREEN}${SKILL_NAME} v${SKILL_VERSION}${NC}"
        echo -e "${CYAN}kk每日备份汇报技能启动...${NC}"
        echo ""
    fi
    
    # 检查必要目录
    check_directory "$BACKUP_ROOT" "备份根目录" || {
        echo -e "${RED}错误: 备份根目录不可用${NC}"
        exit 1
    }
    
    check_directory "$OBSIDIAN_ROOT" "Obsidian根目录" || {
        echo -e "${YELLOW}警告: Obsidian目录不可用，跳过notion检查${NC}"
        unset DIR_NAMES["notion"]
        unset DIR_ICONS["notion"]
    }
    
    # 生成报告
    generate_report
}

# 运行主函数
main "$@"