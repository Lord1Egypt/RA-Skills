#!/bin/bash
# MEMORY.md Manager 安装脚本

set -e

echo "🧠 MEMORY.md Manager 安装脚本"
echo "=============================="

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
SKILL_DIR="$WORKSPACE/skills/memory-manager"

# 检查工作区
if [ ! -d "$WORKSPACE" ]; then
    echo "❌ 错误：未找到 OpenClaw 工作区"
    exit 1
fi

echo "✅ 检测到 OpenClaw 工作区：$WORKSPACE"

# 创建 scripts 目录
mkdir -p "$SKILL_DIR/scripts"

# 创建初始化脚本
cat > "$SKILL_DIR/scripts/init-memory.sh" << 'INIT_SCRIPT'
#!/bin/bash
# 初始化 MEMORY.md

WORKSPACE="$HOME/.openclaw/workspace"
TEMPLATE="$WORKSPACE/skills/memory-manager/templates/MEMORY.md.template"
MEMORY_FILE="$WORKSPACE/MEMORY.md"

if [ -f "$MEMORY_FILE" ]; then
    echo "⚠️  MEMORY.md 已存在，是否覆盖？(y/N)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "已取消"
        exit 0
    fi
fi

if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$MEMORY_FILE"
    echo "✅ MEMORY.md 已创建"
else
    # 使用内置模板
    cat > "$MEMORY_FILE" << 'EOF'
# MEMORY.md - 长期记忆

## 👤 关于用户
- 称呼：
- 时区：

## 🏠 系统环境
- OpenClaw 版本：

## 📅 重要事件
- 

## 📌 待办事项
- [ ] 

EOF
    echo "✅ MEMORY.md 已创建 (基础模板)"
fi

chmod 600 "$MEMORY_FILE"
echo "🔒 文件权限已设置为 600"
INIT_SCRIPT

chmod +x "$SKILL_DIR/scripts/init-memory.sh"

# 创建更新脚本
cat > "$SKILL_DIR/scripts/update-memory.sh" << 'UPDATE_SCRIPT'
#!/bin/bash
# 更新 MEMORY.md (由 cron 自动调用)

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)

echo "📝 检查当天会话..."

# 检查是否有当天的 memory 文件
if [ -d "$MEMORY_DIR" ]; then
    TODAY_FILE="$MEMORY_DIR/$TODAY.md"
    if [ -f "$TODAY_FILE" ]; then
        echo "📄 发现当天会话记录：$TODAY_FILE"
        # 这里可以添加解析逻辑，提取重要事件
        # 简单示例：追加到重要事件
        echo "" >> "$MEMORY_FILE"
        echo "### $TODAY" >> "$MEMORY_FILE"
        echo "- 会话记录已保存到 $TODAY_FILE" >> "$MEMORY_FILE"
        echo "✅ MEMORY.md 已更新"
    else
        echo "⏭️  当天无会话记录，跳过更新"
    fi
else
    echo "⏭️  memory 目录不存在，跳过更新"
fi
UPDATE_SCRIPT

chmod +x "$SKILL_DIR/scripts/update-memory.sh"

# 创建 cron 配置脚本
cat > "$SKILL_DIR/scripts/setup-cron.sh" << 'CRON_SCRIPT'
#!/bin/bash
# 配置每日更新 cron 任务

echo "⏰ 配置 MEMORY.md 每日更新任务..."

# 检查是否已存在
EXISTING=$(openclaw cron list 2>/dev/null | grep -c "MEMORY" || true)

if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️  MEMORY 更新任务已存在"
    echo "是否重新创建？(y/N)"
    read -r response
    if [[ "$response" != "y" ]]; then
        echo "已取消"
        exit 0
    fi
fi

# 创建 cron 任务 (需要用户确认)
echo ""
echo "将创建以下 cron 任务："
echo "  名称：MEMORY.md 每日更新"
echo "  时间：每天午夜 00:00 (Asia/Shanghai)"
echo "  任务：检查当天会话，更新 MEMORY.md"
echo ""
echo "是否继续？(Y/n)"
read -r response
if [[ "$response" == "n" ]]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "请运行以下命令创建 cron 任务："
echo ""
echo 'openclaw cron add --name "MEMORY.md 每日更新" \\'
echo '  --schedule "0 0 * * *" \\'
echo '  --tz "Asia/Shanghai" \\'
echo '  --message "检查当天会话历史，更新 MEMORY.md 的重要事件记录"'
echo ""

CRON_SCRIPT

chmod +x "$SKILL_DIR/scripts/setup-cron.sh"

# 创建配置示例
cat > "$SKILL_DIR/config.example.json" << 'CONFIG_EXAMPLE'
{
  "$schema": "https://docs.openclaw.ai/schemas/config.v1.json",
  "hooks": {
    "internal": {
      "entries": {
        "session-memory": {
          "enabled": true
        }
      }
    }
  }
}
CONFIG_EXAMPLE

echo ""
echo "✅ 文件结构已创建"
echo ""

# 初始化 MEMORY.md
echo "📝 是否现在创建 MEMORY.md？(Y/n)"
read -r response
if [[ "$response" != "n" ]]; then
    "$SKILL_DIR/scripts/init-memory.sh"
fi

# 配置 cron
echo ""
echo "⏰ 是否配置每日自动更新？(Y/n)"
read -r response
if [[ "$response" != "n" ]]; then
    "$SKILL_DIR/scripts/setup-cron.sh"
fi

echo ""
echo "🎉 MEMORY.md Manager 安装完成！"
echo ""
echo "使用指南："
echo "1. 查看 MEMORY.md: cat ~/.openclaw/workspace/MEMORY.md"
echo "2. 手动更新：$SKILL_DIR/scripts/update-memory.sh"
echo "3. 管理 cron: openclaw cron list"
