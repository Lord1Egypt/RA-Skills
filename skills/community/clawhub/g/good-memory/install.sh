#!/bin/bash
#
# Good-Memory 一键安装脚本
# 用法：curl -sSL https://xxx/install.sh | bash
#

set -e

OPENCLAW_BASE="${OPENCLAW_BASE:-/root/.openclaw}"
SKILL_DIR="${SKILL_DIR:-${OPENCLAW_BASE}/workspace/skills/good-memory}"
DOWNLOAD_URL="https://wry-manatee-359.convex.site/api/v1/download?slug=good-memory"

echo "=== Good-Memory 一键安装 ==="
echo ""

# 创建目录
mkdir -p "$SKILL_DIR"
cd "$SKILL_DIR"

# 下载
echo "📥 下载最新版本..."
curl -L -o good-memory.zip "$DOWNLOAD_URL"

# 解压
echo "📦 解压文件..."
unzip -o good-memory.zip
rm good-memory.zip

# 执行安装
echo "🔧 执行安装..."
bash scripts/install.sh

echo ""
echo "🎉 Good-Memory 安装完成！"
echo ""
echo "使用帮助：https://clawhub.ai/acilgit/good-memory"
