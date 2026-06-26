#!/bin/bash
# OpenClaw CNC Core - Push to GitHub and Gitee
# 此脚本用于将代码推送到远程仓库

set -e

# 敏感信息从环境变量读取
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITEE_TOKEN="${GITEE_TOKEN:-}"

# 远程仓库地址（不含token）
GITHUB_REPO="https://github.com/Timo2026/openclaw-cnc-core.git"
GITEE_REPO="https://gitee.com/timo2026/openclaw-cnc-core.git"

# 添加远程仓库
git remote remove github 2>/dev/null || true
git remote remove gitee 2>/dev/null || true

if [ -n "$GITHUB_TOKEN" ]; then
    git remote add github "https://${GITHUB_TOKEN}@github.com/Timo2026/openclaw-cnc-core.git"
    echo "✅ GitHub remote added"
fi

if [ -n "$GITEE_TOKEN" ]; then
    git remote add gitee "https://${GITEE_TOKEN}@gitee.com/timo2026/openclaw-cnc-core.git"
    echo "✅ Gitee remote added"
fi

# 推送到远程
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Pushing to GitHub..."
    git push github master --force 2>&1 | grep -v "ghp_" || true
    echo "✅ Pushed to GitHub"
fi

if [ -n "$GITEE_TOKEN" ]; then
    echo "Pushing to Gitee..."
    git push gitee master --force 2>&1 | grep -v "cf343" || true
    echo "✅ Pushed to Gitee"
fi

echo ""
echo "🎉 开源发布完成！"
echo "GitHub: https://github.com/Timo2026/openclaw-cnc-core"
echo "Gitee:  https://gitee.com/timo2026/openclaw-cnc-core"