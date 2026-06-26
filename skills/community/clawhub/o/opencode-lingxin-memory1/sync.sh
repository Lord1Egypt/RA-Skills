#!/bin/bash
# OpenCode 记忆同步脚本
# 同步记忆到Gitee

MEMORY_DIR="$HOME/.opencode-memory"

cd "$MEMORY_DIR" || exit 1

echo "🔄 同步记忆到Gitee..."

# 检查是否有远程仓库
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE" ]; then
    echo "❌ 未配置远程仓库，无法同步"
    echo "请先添加远程仓库:"
    echo "  git remote add origin <你的Gitee仓库URL>"
    exit 1
fi

# 添加所有更改
git add .

# 检查是否有更改
if git diff --cached --quiet; then
    echo "✅ 没有需要同步的内容"
    exit 0
fi

# 提交
git commit -m "sync: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
git push origin master

echo "✅ 同步完成!"