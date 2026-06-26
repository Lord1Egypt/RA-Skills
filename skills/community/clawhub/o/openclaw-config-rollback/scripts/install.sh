#!/bin/bash

# Config Rollback Skill 安装脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_DIR=~/.openclaw

echo "🔧 安装 Config Rollback Skill..."
echo ""

# 1. 复制脚本到 OpenClaw 目录
echo "📦 复制脚本..."
mkdir -p $OPENCLAW_DIR/scripts
cp $SCRIPT_DIR/*.sh $OPENCLAW_DIR/scripts/
echo "   ✅ 脚本已复制到 $OPENCLAW_DIR/scripts/"

# 2. 设置执行权限
echo ""
echo "🔐 设置执行权限..."
chmod +x $OPENCLAW_DIR/scripts/prepare-config-change.sh
chmod +x $OPENCLAW_DIR/scripts/rollback-guardian.sh
chmod +x $OPENCLAW_DIR/scripts/config-alias.sh
echo "   ✅ 权限已设置"

# 3. 创建备份目录
echo ""
echo "📁 创建备份目录..."
mkdir -p $OPENCLAW_DIR/backups
echo "   ✅ 备份目录已创建"

# 4. 设置 Cron
echo ""
echo "⏰ 设置 Cron 守护任务..."
(crontab -l 2>/dev/null | grep -v "rollback-guardian"; echo "*/1 * * * * $OPENCLAW_DIR/scripts/rollback-guardian.sh") | crontab -
echo "   ✅ Cron 任务已添加"

# 5. 验证
echo ""
echo "🔍 验证安装..."
if [ -x "$OPENCLAW_DIR/scripts/prepare-config-change.sh" ]; then
    echo "   ✅ prepare-config-change.sh 可执行"
else
    echo "   ❌ prepare-config-change.sh 权限问题"
    exit 1
fi

if crontab -l 2>/dev/null | grep -q "rollback-guardian"; then
    echo "   ✅ Cron 任务已配置"
else
    echo "   ❌ Cron 任务配置失败"
    exit 1
fi

# 6. 输出使用说明
echo ""
echo "✅ Config Rollback Skill 安装完成！"
echo ""
echo "📚 使用方式："
echo ""
echo "   # 1. 加载助手（可选）"
echo "   source $OPENCLAW_DIR/scripts/config-alias.sh"
echo ""
echo "   # 2. 准备修改配置"
echo "   $OPENCLAW_DIR/scripts/prepare-config-change.sh \"修改描述\" \"验证事项\""
echo ""
echo "   # 3. 编辑配置"
echo "   # 编辑 ~/.openclaw/openclaw.json"
echo ""
echo "   # 4. 重启 Gateway（5 分钟内）"
echo "   openclaw gateway restart"
echo ""
echo "📖 详见：$SKILL_DIR/SKILL.md"
echo ""
