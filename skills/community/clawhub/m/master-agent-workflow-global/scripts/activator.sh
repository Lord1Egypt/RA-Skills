#!/bin/bash
# master-agent-workflow-global 激活脚本
# 在技能安装后自动执行

set -e

echo "激活 master-agent-workflow-global 技能..."

# 技能根目录
SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$HOME/.openclaw/global-skills/master-agent-workflow/config"

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 复制默认配置
if [ -f "$SKILL_ROOT/config-template.json" ]; then
    cp "$SKILL_ROOT/config-template.json" "$CONFIG_DIR/default.json"
    echo "✓ 复制默认配置"
fi

# 创建模板目录
TEMPLATE_DIR="$HOME/.openclaw/global-skills/master-agent-workflow/templates"
mkdir -p "$TEMPLATE_DIR"

# 复制预定义模板
if [ -d "$SKILL_ROOT/templates" ]; then
    cp -r "$SKILL_ROOT/templates/"* "$TEMPLATE_DIR/" 2>/dev/null || true
    echo "✓ 复制预定义模板"
fi

# 创建日志目录
LOG_DIR="$HOME/.openclaw/global-skills/master-agent-workflow/logs"
mkdir -p "$LOG_DIR"

# 设置环境变量
SHELL_RC="$HOME/.bashrc"
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "MAW_HOME" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# master-agent-workflow-global 环境变量" >> "$SHELL_RC"
    echo "export MAW_HOME=\"$HOME/.openclaw/global-skills/master-agent-workflow\"" >> "$SHELL_RC"
    echo "export PATH=\"\$MAW_HOME/scripts:\$PATH\"" >> "$SHELL_RC"
    echo "✓ 设置环境变量"
fi

# 创建快捷命令
if [ -d "$HOME/bin" ]; then
    ln -sf "$SKILL_ROOT/scripts/maw.sh" "$HOME/bin/maw" 2>/dev/null || true
    ln -sf "$SKILL_ROOT/scripts/maw-list.sh" "$HOME/bin/maw-list" 2>/dev/null || true
    echo "✓ 创建快捷命令"
fi

# 测试钩子处理器
if [ -f "$SKILL_ROOT/hooks/openclaw/handler.js" ]; then
    echo "测试钩子处理器..."
    node -e "
        const Handler = require('$SKILL_ROOT/hooks/openclaw/handler.js');
        const handler = new Handler();
        console.log('✓ 钩子处理器加载成功');
    " 2>/dev/null && echo "✓ 钩子处理器测试通过" || echo "⚠ 钩子处理器测试失败"
fi

# 生成激活报告
ACTIVATION_REPORT="$LOG_DIR/activation-$(date +%Y%m%d-%H%M%S).log"
{
    echo "=== master-agent-workflow-global 激活报告 ==="
    echo "激活时间: $(date)"
    echo "技能版本: 2.0.0"
    echo "安装目录: $SKILL_ROOT"
    echo "配置目录: $CONFIG_DIR"
    echo "模板目录: $TEMPLATE_DIR"
    echo "日志目录: $LOG_DIR"
    echo "环境变量: MAW_HOME=$HOME/.openclaw/global-skills/master-agent-workflow"
    echo "快捷命令: maw, maw-list"
    echo "状态: ✅ 激活成功"
} > "$ACTIVATION_REPORT"

echo ""
echo "✅ master-agent-workflow-global 激活完成！"
echo ""
echo "📋 激活信息:"
echo "   配置目录: $CONFIG_DIR"
echo "   模板目录: $TEMPLATE_DIR"
echo "   日志目录: $LOG_DIR"
echo "   快捷命令: maw, maw-list"
echo ""
echo "🚀 使用方法:"
echo "   1. 重新打开终端或执行: source $SHELL_RC"
echo "   2. 使用命令: maw \"你的任务\""
echo "   3. 查看模板: maw-list"
echo ""
echo "📄 详细文档: $SKILL_ROOT/SKILL.md"
echo "📊 激活报告: $ACTIVATION_REPORT"
echo ""