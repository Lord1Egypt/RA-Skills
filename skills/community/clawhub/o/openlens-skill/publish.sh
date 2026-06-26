#!/bin/bash
#
# OpenLens 一键发布脚本
# 自动推送到 GitHub 并发布到 ClawHub
#

echo "=========================================="
echo "🎬 OpenLens 一键发布"
echo "=========================================="

# 进入 skill 目录
cd /Users/clawdbot/.openclaw/workspace/openlens-skill

# 添加 GitHub 远程（如果还没有）
if ! git remote get-url origin &>/dev/null; then
    echo "⚠️ 未找到 remote，添加 GitHub 仓库..."
    git remote add origin git@github.com:openclawrr/openlens-skill.git
fi

# 提交所有更改
echo ""
echo "[1/3] 📦 提交代码..."
git add -A
git commit -m "v1.0.1 - 支持自定义视频模型" || echo "ℹ️ 没有新更改需要提交"

# 推送到 GitHub
echo ""
echo "[2/3] 🚀 推送到 GitHub..."
git push -u origin main

# 发布到 ClawHub
echo ""
echo "[3/3] 📡 发布到 ClawHub..."
clawhub publish .

echo ""
echo "=========================================="
echo "✅ 发布完成！"
echo "=========================================="
echo ""
echo "检查状态:"
echo "  - GitHub: https://github.com/openclawrr/openlens-skill"
echo "  - ClawHub: https://clawhub.ai/skill/openlens-skill"
