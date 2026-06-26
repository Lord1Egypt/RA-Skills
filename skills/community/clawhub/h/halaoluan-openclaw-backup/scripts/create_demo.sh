#!/bin/bash
# 演示脚本 - 展示备份功能
# 用于录制GIF演示

set -e

echo "======================================"
echo "OpenClaw Backup - 演示"
echo "======================================"
echo ""

# 模拟备份过程
echo "📋 步骤1：创建加密备份"
echo ""
echo "$ bash backup_encrypted.sh"
echo ""
sleep 1

echo "🐈‍⬛ OpenClaw 加密备份开始..."
sleep 0.5
echo "✓ 发现: ~/.openclaw"
sleep 0.5
echo "⏸  停止 OpenClaw 网关..."
sleep 1
echo "📦 打包中..."
sleep 2
echo "🔐 加密中..."
sleep 2
echo "▶️  重启 OpenClaw 网关..."
sleep 1
echo ""
echo "✅ 加密备份完成！"
echo "📁 位置: ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc"
echo "🔐 校验: ~/Desktop/OpenClaw_Backups/openclaw_backup_2026-03-13_20-40-13.tar.gz.enc.sha256"
echo ""

sleep 2

echo "======================================"
echo "📋 步骤2：查看备份列表"
echo ""
echo "$ bash list_backups.sh"
echo ""
sleep 1

echo "🐈‍⬛ OpenClaw 备份列表"
echo "位置: ~/Desktop/OpenClaw_Backups"
echo ""
echo "📦 共 2 个备份文件，总计 2.0G"
echo ""
echo "[🔐 加密] openclaw_backup_2026-03-13_20-40-13.tar.gz.enc"
echo "  大小: 1.0G | 日期: Mar 13 20:41 | 校验: ✓"
echo ""
echo "[📂 未加密] openclaw_backup_2026-03-13_20-46-27.tar.gz"
echo "  大小: 1.0G | 日期: Mar 13 20:47 | 校验: ✓"
echo ""

sleep 2

echo "======================================"
echo "✅ 演示完成！"
echo "======================================"
echo ""
echo "功能特性："
echo "  ✓ AES-256-CBC 加密"
echo "  ✓ SHA256 完整性校验"
echo "  ✓ 自动停止/重启网关"
echo "  ✓ 支持定时备份"
echo ""
echo "了解更多: https://github.com/halaoluan/openclaw-backup"
