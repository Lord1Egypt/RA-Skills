#!/bin/bash
# 中长期任务管理 - 每日总结脚本
# 每天 20:00 运行，生成任务进度日报

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$HOME/.openclaw/workspace/.tasks"
TASKS_FILE="$TASKS_DIR/tasks.json"
LOGS_DIR="$TASKS_DIR/logs"
TODAY=$(date +%Y-%m-%d)
SUMMARY_FILE="$TASKS_DIR/summaries/$TODAY.md"

# 确保目录存在
mkdir -p "$LOGS_DIR"
mkdir -p "$TASKS_DIR/summaries"

# 生成日报
cat > "$SUMMARY_FILE" << EOF
# 任务日报 - $TODAY

**生成时间:** $(date '+%Y-%m-%d %H:%M:%S')

---

## 📊 总体统计

EOF

# 统计任务状态（如果安装了 jq）
if command -v jq &> /dev/null && [ -f "$TASKS_FILE" ]; then
    TOTAL=$(jq '.tasks | length' "$TASKS_FILE")
    COMPLETED=$(jq '[.tasks[] | select(.status == "completed")] | length' "$TASKS_FILE")
    IN_PROGRESS=$(jq '[.tasks[] | select(.status == "in_progress")] | length' "$TASKS_FILE")
    PENDING=$(jq '[.tasks[] | select(.status == "pending")] | length' "$TASKS_FILE")
    BLOCKED=$(jq '[.tasks[] | select(.status == "blocked")] | length' "$TASKS_FILE")
    
    cat >> "$SUMMARY_FILE" << EOF
| 状态 | 数量 |
|------|------|
| 总计 | $TOTAL |
| 已完成 | $COMPLETED |
| 进行中 | $IN_PROGRESS |
| 待开始 | $PENDING |
| 阻塞 | $BLOCKED |

---

## ✅ 今日完成的任务

EOF
    
    # 列出今日完成的任务
    COMPLETED_TASKS=$(jq -r --arg today "$TODAY" '.tasks[] | select(.status == "completed") | select(.last_updated | startswith($today)) | "- \(.id): \(.name)"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$COMPLETED_TASKS" ]; then
        echo "$COMPLETED_TASKS" >> "$SUMMARY_FILE"
    else
        echo "- 无" >> "$SUMMARY_FILE"
    fi
    
    cat >> "$SUMMARY_FILE" << EOF

---

## 🔄 进行中的任务

EOF
    
    # 列出进行中的任务
    IN_PROGRESS_TASKS=$(jq -r '.tasks[] | select(.status == "in_progress") | "- \(.id): \(.name) (进度：\(.progress)%, 截止：\(.due_date))"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$IN_PROGRESS_TASKS" ]; then
        echo "$IN_PROGRESS_TASKS" >> "$SUMMARY_FILE"
    else
        echo "- 无" >> "$SUMMARY_FILE"
    fi
    
    cat >> "$SUMMARY_FILE" << EOF

---

## ⏰ 即将到期（7 天内）

EOF
    
    # 计算 7 天后的日期
    DUE_SOON=$(date -d "+7 days" +%Y-%m-%d 2>/dev/null || date -v+7d +%Y-%m-%d 2>/dev/null || echo "2099-12-31")
    
    DUE_SOON_TASKS=$(jq -r --arg due "$DUE_SOON" '.tasks[] | select(.status != "completed") | select(.due_date <= $due) | "- \(.id): \(.name) (截止：\(.due_date))"' "$TASKS_FILE" 2>/dev/null || echo "")
    
    if [ -n "$DUE_SOON_TASKS" ]; then
        echo "$DUE_SOON_TASKS" >> "$SUMMARY_FILE"
    else
        echo "- 无" >> "$SUMMARY_FILE"
    fi
else
    echo "- 未安装 jq 或任务文件不存在" >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << EOF

---

## 📝 备注

（手动填写今日观察和洞察）

EOF

echo "✅ 每日总结已生成：$SUMMARY_FILE"
