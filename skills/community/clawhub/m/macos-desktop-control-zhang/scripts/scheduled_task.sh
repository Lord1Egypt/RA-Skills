#!/bin/bash
# macOS 定时任务脚本
# 用法：./scheduled_task.sh [命令] [参数]

set -euo pipefail

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_FILE="$HOME/.openclaw_workspace/macos-desktop-tasks.cron"

show_help() {
    echo "macOS 定时任务工具"
    echo ""
    echo "用法：$0 [命令] [参数]"
    echo ""
    echo "命令:"
    echo "  add TIME COMMAND    添加定时任务"
    echo "  list                列出所有任务"
    echo "  remove ID           删除任务"
    echo "  run ID              立即运行任务"
    echo "  clear               清空所有任务"
    echo ""
    echo "时间格式:"
    echo "  每分钟：* * * * *"
    echo "  每小时：0 * * * *"
    echo "  每天：0 8 * * *     (每天 8:00)"
    echo "  每周：0 8 * * 1     (每周一 8:00)"
    echo ""
    echo "示例:"
    echo "  $0 add \"*/5 * * * *\" \"bash $SCRIPT_DIR/screenshot.sh\""
    echo "  $0 add \"0 9 * * *\" \"bash $SCRIPT_DIR/automation_workflows.sh morning\""
    echo "  $0 list"
}

# 添加任务
add_task() {
    local schedule="$1"
    local command="$2"
    local id=$(date +%s)
    
    echo -e "${BLUE}📅 添加定时任务...${NC}"
    echo "   计划：$schedule"
    echo "   命令：$command"
    echo "   ID: $id"
    echo ""
    
    # 添加到 crontab
    local cron_entry="$schedule bash $command # mdc-task-$id"
    
    (crontab -l 2>/dev/null | grep -v "mdc-task-" || true; echo "$cron_entry") | crontab -
    
    echo -e "${GREEN}✅ 任务已添加${NC}"
    echo ""
    echo "💡 提示：使用 '$0 list' 查看所有任务"
}

# 列出任务
list_tasks() {
    echo -e "${BLUE}📋 定时任务列表：${NC}"
    echo ""
    
    local tasks=$(crontab -l 2>/dev/null | grep "mdc-task-" || true)
    
    if [ -n "$tasks" ]; then
        echo "ID | 计划 | 命令"
        echo "─────────────────────────────────────────────"
        
        echo "$tasks" | while read -r line; do
            local id=$(echo "$line" | grep -oP 'mdc-task-\K\d+')
            local schedule=$(echo "$line" | awk '{print $1, $2, $3, $4, $5}')
            local command=$(echo "$line" | sed 's/.*bash //' | sed 's/ # mdc-task-.*//')
            
            echo "$id | $schedule | $command"
        done
    else
        echo -e "${YELLOW}⚠️  没有定时任务${NC}"
        echo ""
        echo "使用 '$0 add \"计划\" \"命令\"' 添加任务"
    fi
    
    echo ""
}

# 删除任务
remove_task() {
    local task_id="$1"
    
    if [ -z "$task_id" ]; then
        echo -e "${RED}❌ 请提供任务 ID${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🗑️  删除任务 $task_id...${NC}"
    
    (crontab -l 2>/dev/null | grep -v "mdc-task-$task_id" || true) | crontab -
    
    echo -e "${GREEN}✅ 任务已删除${NC}"
}

# 运行任务
run_task() {
    local task_id="$1"
    
    if [ -z "$task_id" ]; then
        echo -e "${RED}❌ 请提供任务 ID${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}▶️  运行任务 $task_id...${NC}"
    
    local task=$(crontab -l 2>/dev/null | grep "mdc-task-$task_id" || true)
    
    if [ -n "$task" ]; then
        local command=$(echo "$task" | sed 's/.*bash //' | sed 's/ # mdc-task-.*//')
        bash -c "$command"
        echo -e "${GREEN}✅ 任务执行完成${NC}"
    else
        echo -e "${RED}❌ 未找到任务 $task_id${NC}"
    fi
}

# 清空所有任务
clear_tasks() {
    echo -e "${YELLOW}⚠️  确认清空所有定时任务？(y/n)${NC}"
    read -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        (crontab -l 2>/dev/null | grep -v "mdc-task-" || true) | crontab -
        echo -e "${GREEN}✅ 已清空所有任务${NC}"
    else
        echo "已取消"
    fi
}

# 主逻辑
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case $1 in
        add)
            add_task "$2" "$3"
            ;;
        list)
            list_tasks
            ;;
        remove)
            remove_task "$2"
            ;;
        run)
            run_task "$2"
            ;;
        clear)
            clear_tasks
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo -e "${RED}❌ 未知命令：$1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
