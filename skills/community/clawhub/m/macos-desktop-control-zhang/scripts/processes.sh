#!/bin/bash
# macOS 进程列表脚本
# 用法：./processes.sh [选项]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "macOS 进程列表工具"
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项:"
    echo "  -a, --all        显示所有进程"
    echo "  -u, --user       仅显示用户进程（默认）"
    echo "  -g, --gui        仅显示图形界面应用"
    echo "  -s, --search NAME 搜索进程名称"
    echo "  -t, --top N      显示前 N 个 CPU 占用进程"
    echo "  -j, --json       JSON 格式输出"
    echo "  -h, --help       显示帮助"
    echo ""
    echo "示例:"
    echo "  $0                    # 显示用户进程"
    echo "  $0 -g                 # 显示图形界面应用"
    echo "  $0 -s Safari          # 搜索 Safari 进程"
    echo "  $0 -t 5               # 显示前 5 个 CPU 占用进程"
}

# 显示图形界面应用（优化版）
show_gui_apps() {
    echo -e "${BLUE}🖥️  当前运行的图形界面应用：${NC}"
    echo ""
    
    # 使用 System Events 获取前端应用（优化：只获取一次）
    local apps
    apps=$(osascript -e 'tell application "System Events" to get name of every application process whose background only is false' 2>/dev/null)
    
    if [ -n "$apps" ]; then
        # 优化：使用 awk 一次性处理
        echo "$apps" | tr ',' '\n' | awk '
        NF > 0 {
            gsub(/^[ \t]+|[ \t]+$/, "");  # 去除首尾空格
            if (length($0) > 0) {
                cmd = "pgrep -x \"" $0 "\" 2>/dev/null | head -1";
                cmd | getline pid;
                close(cmd);
                if (pid == "") pid = "N/A";
                printf "  \033[0;32m%-30s\033[0m PID: %s\n", $0, pid
            }
        }' | head -20  # 限制显示 20 个
    else
        # 回退方案：使用 ps（优化：减少处理）
        ps aux | awk '
        /Applications\/.+\.app/ {
            n = split($11, a, "/");
            app = a[n];
            gsub(/\.app$/, "", app);
            if (!seen[app]++) printf "  \033[0;32m%-30s\033[0m\n", app
        }' | head -20
    fi
    
    echo ""
}

# 显示所有进程
show_all_processes() {
    echo -e "${BLUE}📋 所有进程：${NC}"
    echo ""
    printf "  %-10s %-30s %s\n" "PID" "名称" "CPU%"
    echo "  ─────────────────────────────────────────"
    
    ps aux --no-headers | sort -k3 -rn | head -30 | while read -r user pid cpu mem vsz rss tty stat start time command; do
        # 简化命令名称
        local name
        name=$(basename "$command" | cut -c1-30)
        printf "  %-10s %-30s %s\n" "$pid" "$name" "$cpu"
    done
    
    echo ""
}

# 显示用户进程
show_user_processes() {
    echo -e "${BLUE}📋 用户进程（前 20 个）：${NC}"
    echo ""
    printf "  %-10s %-30s %s\n" "PID" "名称" "CPU%"
    echo "  ─────────────────────────────────────────"
    
    ps auxu | tail -n +2 | sort -k3 -rn | head -20 | while read -r user pid cpu mem vsz rss tty stat start time command; do
        local name
        name=$(basename "$command" | cut -c1-30)
        printf "  %-10s %-30s %s\n" "$pid" "$name" "$cpu"
    done
    
    echo ""
}

# 搜索进程
search_process() {
    local search_term="$1"
    
    echo -e "${BLUE}🔍 搜索进程：${search_term}${NC}"
    echo ""
    
    local result
    result=$(ps aux | grep -i "$search_term" | grep -v grep)
    
    if [ -n "$result" ]; then
        printf "  %-10s %-30s %s\n" "PID" "名称" "CPU%"
        echo "  ─────────────────────────────────────────"
        
        echo "$result" | while read -r user pid cpu mem vsz rss tty stat start time command; do
            local name
            name=$(basename "$command" | cut -c1-30)
            printf "  %-10s %-30s %s\n" "$pid" "$name" "$cpu"
        done
    else
        echo -e "${YELLOW}⚠️  未找到匹配的进程：${search_term}${NC}"
    fi
    
    echo ""
}

# 显示 Top N CPU 占用进程
show_top_cpu() {
    local count=${1:-10}
    
    echo -e "${BLUE}🔥 CPU 占用前 ${count} 的进程：${NC}"
    echo ""
    printf "  %-10s %-30s %s\n" "PID" "名称" "CPU%"
    echo "  ─────────────────────────────────────────"
    
    ps aux --no-headers | sort -k3 -rn | head -"$count" | while read -r user pid cpu mem vsz rss tty stat start time command; do
        local name
        name=$(basename "$command" | cut -c1-30)
        printf "  %-10s %-30s %s\n" "$pid" "$name" "$cpu"
    done
    
    echo ""
}

# JSON 格式输出
output_json() {
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"processes\": ["
    
    ps aux --no-headers | head -20 | awk '{
        gsub(/"/, "\\\"", $11);
        printf "    {\"pid\": %s, \"user\": \"%s\", \"cpu\": %s, \"command\": \"%s\"}", $2, $1, $3, $11;
        if (NR < 20) printf ",";
        printf "\n";
    }'
    
    echo "  ]"
    echo "}"
}

# 统计信息
show_stats() {
    local total_processes
    total_processes=$(ps aux | wc -l)
    total_processes=$((total_processes - 1))  # 减去标题行
    
    local user_processes
    user_processes=$(ps auxu | wc -l)
    user_processes=$((user_processes - 1))
    
    local gui_apps
    gui_apps=$(osascript -e 'tell application "System Events" to count (every application process whose background only is false)' 2>/dev/null || echo "0")
    
    echo -e "${BLUE}📊 进程统计：${NC}"
    echo ""
    echo "  总进程数：$total_processes"
    echo "  用户进程：$user_processes"
    echo "  图形应用：$gui_apps"
    echo ""
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        # 无参数：显示 GUI 应用 + 用户进程
        show_gui_apps
        show_user_processes
        show_stats
        exit 0
    fi
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -a|--all)
                show_all_processes
                shift
                ;;
            -u|--user)
                show_user_processes
                shift
                ;;
            -g|--gui)
                show_gui_apps
                shift
                ;;
            -s|--search)
                search_process "$2"
                shift 2
                ;;
            -t|--top)
                show_top_cpu "$2"
                shift 2
                ;;
            -j|--json)
                output_json
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}❌ 未知选项：$1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

# 运行主函数
main "$@"
