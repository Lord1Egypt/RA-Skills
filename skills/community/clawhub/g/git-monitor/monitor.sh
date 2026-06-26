#!/bin/bash
# GitHub 仓库监控脚本

set -e

REPO_URL="$1"
REPO_NAME="$2"
LOCAL_PATH="$3"
BRANCH="${4:-main}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 检查仓库: $REPO_NAME"
echo "📍 URL: $REPO_URL"
echo "📂 本地路径: $LOCAL_PATH"
echo ""

# 创建目录
mkdir -p "$(dirname "$LOCAL_PATH")"

# 如果本地不存在，克隆仓库
if [ ! -d "$LOCAL_PATH" ]; then
    echo "📥 首次克隆仓库（可能需要几分钟，请耐心等待）..."
    git clone --progress "$REPO_URL" "$LOCAL_PATH" 2>&1
    cd "$LOCAL_PATH"
    INITIAL_COMMIT=$(git rev-parse HEAD)
    echo "✅ 克隆完成"
    echo "INITIAL_COMMIT=$INITIAL_COMMIT"
    exit 0
fi

cd "$LOCAL_PATH"

# 保存当前 commit
OLD_COMMIT=$(git rev-parse HEAD)
echo "📌 当前 commit: ${OLD_COMMIT:0:7}"

# 拉取最新代码
echo "🔄 拉取远程更新..."
git fetch origin "$BRANCH" 2>&1

# 检查是否有更新
NEW_COMMIT=$(git rev-parse "origin/$BRANCH")
echo "📌 远程 commit: ${NEW_COMMIT:0:7}"

if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    echo "✅ 已是最新版本，无需更新"
    echo "NO_UPDATES"
    exit 0
fi

# 有更新，生成变更信息
echo ""
echo "🎉 发现新更新！"
echo ""

# 获取新增的 commits
echo "=== COMMITS_START ==="
git log --pretty=format:"%H|%an|%ar|%s" "$OLD_COMMIT..$NEW_COMMIT"
echo ""
echo "=== COMMITS_END ==="
echo ""

# 获取文件变更统计
echo "=== STATS_START ==="
git diff --stat "$OLD_COMMIT..$NEW_COMMIT"
echo "=== STATS_END ==="
echo ""

# 获取详细的文件变更列表
echo "=== FILES_START ==="
git diff --name-status "$OLD_COMMIT..$NEW_COMMIT"
echo "=== FILES_END ==="
echo ""

# 更新本地代码
echo "⬇️  更新本地代码..."
git merge "origin/$BRANCH" --ff-only

echo ""
echo "✅ 更新完成"
echo "OLD_COMMIT=$OLD_COMMIT"
echo "NEW_COMMIT=$NEW_COMMIT"
