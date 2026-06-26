#!/bin/bash
# log_work.sh — 工作即时记录脚本
# 用法：./log_work.sh "任务描述" "文件路径 1" "文件路径 2" ...
# 
# 核心功能：
# 1. 工作完成后立即记录到 daily log
# 2. 自动 git add + commit
# 3. 防止记忆遗漏（2026-03-21 教训）

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE" || exit 1

TASK="$1"
shift
FILES="$@"

if [ -z "$TASK" ]; then
    echo "❌ 用法：./log_work.sh \"任务描述\" \"文件路径 1\" \"文件路径 2\" ..."
    echo ""
    echo "示例："
    echo "  ./log_work.sh \"Day-1 内容创作\" \"docs/articles/Day-01-为什么选 OpenClaw.md\""
    echo "  ./log_work.sh \"配置 SSH 免密\" \".ssh/authorized_keys\""
    exit 1
fi

# 获取当天日期
TODAY=$(date +%Y-%m-%d)
DAILY_LOG="memory/${TODAY}.md"

# 创建 daily log（如果不存在）
if [ ! -f "$DAILY_LOG" ]; then
    echo "# ${TODAY} Daily Log" > "$DAILY_LOG"
    echo "" >> "$DAILY_LOG"
    echo "**创建时间:** $(date +%H:%M)" >> "$DAILY_LOG"
    echo "" >> "$DAILY_LOG"
fi

# 追加记录
cat >> "$DAILY_LOG" << EOF

## ${TASK} ($(date +%H:%M))

**文件：** ${FILES}
**状态：** ✅ 已完成

EOF

echo "✅ 已记录到 ${DAILY_LOG}"
echo ""
echo "📝 记录内容："
echo "---"
echo "## ${TASK} ($(date +%H:%M))"
echo "**文件：** ${FILES}"
echo "**状态：** ✅ 已完成"
echo "---"

# 自动 git add + commit
if [ -d .git ]; then
    git add "$DAILY_LOG" 2>/dev/null
    git add ${FILES} 2>/dev/null
    
    COMMIT_MSG="memory: 记录 ${TASK}"
    git commit -m "$COMMIT_MSG" --quiet 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Git commit 完成：$COMMIT_MSG"
    else
        echo "⚠️ Git commit 失败（可能没有改动）"
    fi
else
    echo "⚠️ 不是 git 仓库，跳过 commit"
fi

echo ""
echo "💡 提示：养成工作后立即执行此脚本的习惯，防止记忆遗漏"
