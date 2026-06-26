#!/bin/bash
# Progress Reporter - 定时进度汇报系统
# 功能：每 10 分钟自动汇报当前任务进展

set -eo pipefail

TASKS_DIR="/root/.openclaw/workspace/tasks"
MEMORY_DIR="/root/.openclaw/workspace/memory"
REPORTS_DIR="${TASKS_DIR}/progress-reports"
LOG_PREFIX="[reporter]"

log() {
    echo "$LOG_PREFIX $1"
}

ensure_dirs() {
    mkdir -p "$REPORTS_DIR"
}

# 获取当前任务
get_current_task() {
    local running_task=$(ls -t "${TASKS_DIR}/running/"*.json 2>/dev/null | head -1)
    if [[ -n "$running_task" ]]; then
        echo "$running_task"
        return 0
    fi
    return 1
}

# 生成进度报告
generate_report() {
    local task_file="$1"
    local task_id=$(basename "$task_file" .json)
    local task_desc=$(jq -r '.task' "$task_file" 2>/dev/null || echo "未知任务")
    local report_file="${REPORTS_DIR}/${task_id}-$(date +%H%M).md"
    
    # 获取执行日志
    local log_file="${TASKS_DIR}/running/${task_id}.log"
    local iteration_count=0
    local last_action="无记录"
    
    if [[ -f "$log_file" ]]; then
        iteration_count=$(grep -c "迭代 #" "$log_file" 2>/dev/null || echo "0")
        last_action=$(tail -10 "$log_file" | grep -v "^#" | tail -1 || echo "无记录")
    fi
    
    cat > "$report_file" << EOF
# 📊 进度汇报

**时间**: $(date "+%Y-%m-%d %H:%M:%S")  
**任务 ID**: $task_id  
**任务内容**: $task_desc

---

## 当前状态

🔄 **执行中** - 迭代 #$iteration_count

---

## 本周期完成的工作

$(if [[ -f "$log_file" ]]; then
    # 提取最近 10 分钟的日志
    tail -20 "$log_file" | grep -v "^#" | head -10
else
    echo "_暂无详细日志_"
fi)

---

## 当前进展

- **总迭代次数**: $iteration_count
- **最近操作**: $last_action
- **状态**: 执行中

---

## 下一步计划

- 继续执行当前迭代
- 评估结果质量
- 调整策略（如需要）

---

*自主迭代系统 - 定时进度汇报 (每 10 分钟)*
EOF

    echo "$report_file"
}

# 发送通知
send_notification() {
    local report_file="$1"
    local notify_file="${MEMORY_DIR}/progress-$(date +%Y%m%d-%H%M).md"
    
    local task_id=$(basename "$report_file" .md | cut -d- -f1)
    
    cat > "$notify_file" << EOF
# 📬 进度汇报

**时间**: $(date "+%H:%M:%S")  
**任务**: $task_id

---

详细报告：$report_file

---

*每 10 分钟自动汇报*
EOF

    log "📬 汇报已发送：$notify_file"
}

# 主流程
ensure_dirs

task_file=$(get_current_task || echo "")

if [[ -z "$task_file" ]]; then
    log "😴 无运行中任务，跳过汇报"
    echo "no_task"
    exit 0
fi

log "📊 生成进度报告..."
report_file=$(generate_report "$task_file")
log "📊 报告已生成：$report_file"

send_notification "$report_file"

echo "completed:$report_file"
