#!/bin/bash
# 中长期任务管理 - 每周 Review 脚本
# 每周一 09:00 运行，生成周报并调整计划

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$HOME/.openclaw/workspace/.tasks"
TASKS_FILE="$TASKS_DIR/tasks.json"
WEEKLY_DIR="$TASKS_DIR/weekly"
TODAY=$(date +%Y-%m-%d)
WEEK_START=$(date -d "last monday" +%Y-%m-%d 2>/dev/null || date -v-mon +%Y-%m-%d 2>/dev/null || echo "$TODAY")
WEEK_END=$(date -d "next sunday" +%Y-%m-%d 2>/dev/null || date -v-sun +%Y-%m-%d 2>/dev/null || echo "$TODAY")
REPORT_FILE="$WEEKLY_DIR/week-of-$WEEK_START.md"

# 确保目录存在
mkdir -p "$WEEKLY_DIR"

# 生成周报
cat > "$REPORT_FILE" << EOF
# 任务周报

**周期:** $WEEK_START ~ $WEEK_END  
**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 本周概览

EOF

# 统计（如果安装了 jq）
if command -v jq &> /dev/null && [ -f "$TASKS_FILE" ]; then
    # 本周完成的任务数
    COMPLETED_THIS_WEEK=$(jq --arg start "$WEEK_START" --arg end "$WEEK_END" '[.tasks[] | select(.status == "completed") | select(.last_updated >= $start and .last_updated <= $end)] | length' "$TASKS_FILE" 2>/dev/null || echo "0")
    
    # 当前进行中的任务数
    IN_PROGRESS=$(jq '[.tasks[] | select(.status == "in_progress")] | length' "$TASKS_FILE" 2>/dev/null || echo "0")
    
    # 延期的任务数
    OVERDUE=$(jq --arg today "$TODAY" '[.tasks[] | select(.status != "completed") | select(.due_date < $today)] | length' "$TASKS_FILE" 2>/dev/null || echo "0")
    
    cat >> "$REPORT_FILE" << EOF
| 指标 | 数值 |
|------|------|
| 本周完成任务 | $COMPLETED_THIS_WEEK |
| 当前进行中 | $IN_PROGRESS |
| 延期任务 | $OVERDUE |

---

## ✅ 本周完成

EOF
    
    COMPLETED=$(jq -r --arg start "$WEEK_START" --arg end "$WEEK_END" '.tasks[] | select(.status == "completed") | select(.last_updated >= $start and .last_updated <= $end) | "- \(.id): \(.name)"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$COMPLETED" ]; then
        echo "$COMPLETED" >> "$REPORT_FILE"
    else
        echo "- 无" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF

---

## 🔄 进行中任务

EOF
    
    IN_PROGRESS_LIST=$(jq -r '.tasks[] | select(.status == "in_progress") | "- \(.id): \(.name)\n  - 进度：\(.progress)%\n  - 截止：\(.due_date)"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$IN_PROGRESS_LIST" ]; then
        echo "$IN_PROGRESS_LIST" >> "$REPORT_FILE"
    else
        echo "- 无" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF

---

## ⚠️ 延期任务

EOF
    
    OVERDUE_LIST=$(jq -r --arg today "$TODAY" '.tasks[] | select(.status != "completed") | select(.due_date < $today) | "- \(.id): \(.name)\n  - 原截止：\(.due_date)\n  - 延期：\((now - (.due_date | strptime("%Y-%m-%d") | mktime)) / 86400 | floor) 天"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$OVERDUE_LIST" ]; then
        echo "$OVERDUE_LIST" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "**处理建议:**" >> "$REPORT_FILE"
        echo "1. 重新评估优先级" >> "$REPORT_FILE"
        echo "2. 调整截止日期或分解任务" >> "$REPORT_FILE"
        echo "3. 识别并解决阻塞问题" >> "$REPORT_FILE"
    else
        echo "- 无延期任务 ✅" >> "$REPORT_FILE"
    fi
    
    cat >> "$REPORT_FILE" << EOF

---

## 📅 下周计划

### 优先处理
- [ ] （填写）

### 计划开始
- [ ] （填写）

### 预期完成
- [ ] （填写）

---

## 💡 反思与改进

（本周的洞察、教训、改进建议）

EOF
else
    echo "- 未安装 jq 或任务文件不存在" >> "$REPORT_FILE"
fi

echo "✅ 周报已生成：$REPORT_FILE"
