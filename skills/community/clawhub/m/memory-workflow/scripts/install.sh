#!/bin/bash
# Memory Workflow 安装配置脚本
# 自动配置 cron 任务、创建必要文件和目录

set -e

WORKSPACE="/root/.openclaw/workspace"
SKILL_DIR="$WORKSPACE/skills/memory-workflow"
SCRIPTS_DIR="$SKILL_DIR/scripts"
LOGS_DIR="$WORKSPACE/logs"
MEMORY_DIR="$WORKSPACE/memory"

echo "📒 Memory Workflow 安装配置"
echo "=========================="

# 1. 创建必要目录
echo "📁 创建目录..."
mkdir -p "$LOGS_DIR"
mkdir -p "$MEMORY_DIR"

# 2. 创建配置文件模板
echo "⚙️ 创建配置文件..."
if [ ! -f "$WORKSPACE/.memory-workflow-config" ]; then
    cat > "$WORKSPACE/.memory-workflow-config" << 'CONFIG'
# Memory Workflow 配置文件
# 修改后重启 cron 生效

# 每日摘要时间（小时，24 小时制）
DAILY_SUMMARY_HOUR=23

# 超时等待时间（分钟）
SUMMARY_TIMEOUT_MINUTES=5

# 读档频率：new_session_only | every_message
ARCHIVE_FREQUENCY=new_session_only

# 保留每日笔记天数
KEEP_DAYS=7
CONFIG
    echo "✅ 配置文件已创建：$WORKSPACE/.memory-workflow-config"
else
    echo "⚠️  配置文件已存在，跳过"
fi

# 3. 创建每日笔记模板
echo "📝 创建每日笔记模板..."
if [ ! -f "$SKILL_DIR/templates/daily-note-template.md" ]; then
    cat > "$SKILL_DIR/templates/daily-note-template.md" << 'TEMPLATE'
# {{DATE}} - 每日摘要

## 📋 今日重点
_待填充..._

## 💬 重要对话
_待填充..._

## 🎯 关键决策
_待填充..._

## 📝 待办更新
_待填充..._

---
*自动生成时间：{{TIMESTAMP}}*
*记录者：[助手名称]*
TEMPLATE
    echo "✅ 模板已创建：$SKILL_DIR/templates/daily-note-template.md"
else
    echo "⚠️  模板已存在，跳过"
fi

# 4. 创建 MEMORY.md 模板（如果不存在）
echo "📖 检查 MEMORY.md..."
if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
    cat > "$WORKSPACE/MEMORY.md" << 'MEMORY'
# MEMORY.md - 长期记忆

> 这是助手的长期记忆文件，记录核心身份、重要关系、关键渠道和持续跟踪事项。
> 每次会话启动时自动读取，确保记忆连续性。

---

## 🎭 核心身份

### 助手信息
| 设定 | 内容 |
|------|------|
| **姓名** | [助手名称] |
| **MBTI** | [人格类型] |
| **核心特质** | [特质描述] |
| **角色** | [角色说明] |

### 用户信息
| 设定 | 内容 |
|------|------|
| **称呼** | [用户称呼] |
| **姓名** | [用户姓名] |
| **职业** | [用户职业] |

---

## 🌐 重要渠道

_待补充..._

---

## 📝 待办事项

_待补充..._

---

## 📚 记忆维护规则

### 更新时机
- 每天结束时：回顾当天重要对话，更新 `memory/YYYY-MM-DD.md`
- 重要决策后：同步到 MEMORY.md
- 新信息获取：及时补充

### 精简原则
- MEMORY.md 保持精简（核心信息）
- 详细信息归档到 `memory/` 每日笔记
- 定期（每周）回顾，删除过时信息

---

*最后更新：{{TIMESTAMP}}*
MEMORY
    echo "✅ MEMORY.md 模板已创建"
else
    echo "⚠️  MEMORY.md 已存在，跳过"
fi

# 5. 配置 cron 任务
echo "⏰ 配置 cron 任务..."

# 读取配置
if [ -f "$WORKSPACE/.memory-workflow-config" ]; then
    source "$WORKSPACE/.memory-workflow-config"
fi

# 默认值
DAILY_SUMMARY_HOUR=${DAILY_SUMMARY_HOUR:-23}

# 移除旧的 cron 任务（如果有）
(crontab -l 2>/dev/null | grep -v "memory-workflow" || true) > /tmp/cron_temp

# 添加新的 cron 任务
echo "*/1 * * * * $SCRIPTS_DIR/daily-summary.sh >> $LOGS_DIR/daily-summary.log 2>&1" >> /tmp/cron_temp

# 安装 cron 任务
crontab /tmp/cron_temp
rm /tmp/cron_temp

echo "✅ cron 任务已配置：每天 ${DAILY_SUMMARY_HOUR}:00 执行每日摘要"

# 6. 设置脚本权限
echo "🔐 设置脚本权限..."
chmod +x "$SCRIPTS_DIR/daily-summary.sh" 2>/dev/null || true
chmod +x "$SCRIPTS_DIR/weekly-review.sh" 2>/dev/null || true

echo ""
echo "=========================="
echo "✅ Memory Workflow 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 编辑 $WORKSPACE/.memory-workflow-config 自定义配置"
echo "2. 填写 $WORKSPACE/MEMORY.md 核心信息"
echo "3. 等待每天 ${DAILY_SUMMARY_HOUR}:00 自动执行每日摘要"
echo ""
echo "🎉 开始使用吧！"
