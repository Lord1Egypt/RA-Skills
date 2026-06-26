#!/bin/bash
# 中长期任务管理 - 心跳检查脚本
# 在每次心跳检查时运行，review 所有进行中的任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$HOME/.openclaw/workspace/.tasks"
TASKS_FILE="$TASKS_DIR/tasks.json"
LOGS_DIR="$TASKS_DIR/logs"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOGS_DIR/$TODAY.md"

# 确保日志目录存在
mkdir -p "$LOGS_DIR"

# 初始化今日日志
if [ ! -f "$LOG_FILE" ]; then
    cat > "$LOG_FILE" << EOF
# 任务进度日志 - $TODAY

## 检查记录

EOF
fi

# 添加检查时间戳
echo "- **$(date '+%H:%M:%S')** - 心跳检查" >> "$LOG_FILE"

# 检查 tasks.json 是否存在
if [ ! -f "$TASKS_FILE" ]; then
    echo "  - ⚠️ 任务文件不存在，跳过检查" >> "$LOG_FILE"
    exit 0
fi

# 使用 jq 解析任务（如果安装了 jq）
if command -v jq &> /dev/null; then
    # 获取所有进行中的任务
    IN_PROGRESS_TASKS=$(jq -r '.tasks[] | select(.status == "in_progress") | "\(.id)|\(.name)|\(.due_date)|\(.progress)"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$IN_PROGRESS_TASKS" ]; then
        echo "" >> "$LOG_FILE"
        echo "## 进行中的任务" >> "$LOG_FILE"
        
        while IFS='|' read -r task_id task_name due_date progress; do
            echo "" >> "$LOG_FILE"
            echo "### $task_id: $task_name" >> "$LOG_FILE"
            echo "- **截止日期:** $due_date" >> "$LOG_FILE"
            echo "- **当前进度:** $progress%" >> "$LOG_FILE"
            
            # 计算剩余天数
            DUE_TIMESTAMP=$(date -d "$due_date" +%s 2>/dev/null || echo "0")
            NOW_TIMESTAMP=$(date +%s)
            DAYS_LEFT=$(( (DUE_TIMESTAMP - NOW_TIMESTAMP) / 86400 ))
            
            if [ $DAYS_LEFT -lt 0 ]; then
                echo "- **状态:** ❌ 已延期 $(( -DAYS_LEFT )) 天" >> "$LOG_FILE"
                echo "  - 🚨 **需要立即处理！**" >> "$LOG_FILE"
            elif [ $DAYS_LEFT -le 2 ]; then
                echo "- **状态:** ⚠️ 即将到期（剩余 $DAYS_LEFT 天）" >> "$LOG_FILE"
            else
                echo "- **状态:** ✅ 正常（剩余 $DAYS_LEFT 天）" >> "$LOG_FILE"
            fi
        done <<< "$IN_PROGRESS_TASKS"
    else
        echo "" >> "$LOG_FILE"
        echo "## 进行中的任务" >> "$LOG_FILE"
        echo "- 暂无进行中的任务" >> "$LOG_FILE"
    fi
    
    # 检查今日到期的任务
    TODAY_TASKS=$(jq -r --arg today "$TODAY" '.tasks[] | select(.due_date == $today and .status != "completed") | "\(.id)|\(.name)"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$TODAY_TASKS" ]; then
        echo "" >> "$LOG_FILE"
        echo "## ⏰ 今日到期任务" >> "$LOG_FILE"
        while IFS='|' read -r task_id task_name; do
            echo "- $task_id: $task_name" >> "$LOG_FILE"
        done <<< "$TODAY_TASKS"
    fi
else
    echo "" >> "$LOG_FILE"
    echo "## 提示" >> "$LOG_FILE"
    echo "- 未安装 jq，无法解析任务详情" >> "$LOG_FILE"
    echo "- 请安装：sudo apt install jq 或 brew install jq" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

# 输出摘要到 stdout（供心跳检查汇报使用）
echo "✅ 任务检查完成，日志已记录到 $LOG_FILE"
