#!/bin/bash
# kk每日备份汇报技能测试脚本

echo "🧪 测试kk每日备份汇报技能..."
echo "========================================"

# 测试移动端格式
echo ""
echo "📱 测试移动端格式:"
./kk_daily_backup_report.sh --format mobile

echo ""
echo "========================================"
echo "📋 测试详细格式:"
./kk_daily_backup_report.sh --format detailed

echo ""
echo "========================================"
echo "📊 测试摘要格式:"
./kk_daily_backup_report.sh --format summary

echo ""
echo "========================================"
echo "🎯 测试特定目录:"
./kk_daily_backup_report.sh --dir homeserver,vps_jp --format mobile

echo ""
echo "========================================"
echo "⚙️ 显示配置:"
./kk_daily_backup_report.sh --config

echo ""
echo "========================================"
echo "✅ 技能测试完成！"
echo "技能位置: $(pwd)"
echo "使用方法: ./kk_daily_backup_report.sh [选项]"