#!/bin/bash
# 帝王引擎紧急停止脚本

set -e

echo "🛑 帝王引擎紧急停止 🛑"
echo "========================"

# 立即禁用技能
echo "🔧 禁用帝王引擎..."
openclaw skill disable imperial-engine 2>/dev/null || true

# 卸载技能
echo "🗑️ 卸载帝王引擎..."
openclaw skill uninstall imperial-engine 2>/dev/null || true

# 清理内存文件
echo "🧹 清理临时文件..."
rm -f ~/.openclaw/memory/imperial_engine_step_*.md 2>/dev/null || true

# 检查进程
echo "🔍 检查相关进程..."
pkill -f "imperial" 2>/dev/null || true

# 显示当前状态
echo ""
echo "📊 当前状态："
openclaw skill list | grep -i engine || echo "未找到帝王引擎相关技能"

echo ""
echo "✅ 帝王引擎已完全停止！"
echo ""
echo "📈 最后消耗统计："
openclaw status --usage 2>/dev/null || echo "无法获取使用统计"
echo ""
echo "💾 建议：备份日志文件以便分析"
echo "日志位置：~/.openclaw/logs/"