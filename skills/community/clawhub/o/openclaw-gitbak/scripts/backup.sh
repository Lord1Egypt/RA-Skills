#!/bin/bash
# OpenClaw GitBak 通用备份脚本
# 用法: backup.sh [key|all] [commitmessage]
# 示例:
#   bash ./backup.sh cfg "ORG"
#   bash ./backup.sh workspace-coder "ORG"
#   bash ./backup.sh all "ORG"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

COMMIT_MSG="${2:-ORG}"
TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "用法: backup.sh [key|all] [commitmessage]"
    echo "可用备份项:"
    for key in $(get_backup_keys); do
        local item=$(get_backup_item "$key")
        local desc=$(echo "$item" | cut -d: -f3)
        echo "  $key - $desc"
    done
    exit 1
fi

# 解析需要备份的键列表
get_keys_to_backup() {
    local target="$1"
    if [ "$target" = "all" ]; then
        get_backup_keys
    else
        # 检查是否包含通配符
        if [[ "$target" == *"*"* ]]; then
            # 支持通配符匹配
            get_backup_keys | grep -E "$target"
        else
            # 自动匹配以 target 开头的所有项
            local matched_keys=$(get_backup_keys | grep -E "^$target")
            if [ -n "$matched_keys" ]; then
                echo "$matched_keys"
            else
                # 无匹配时使用精确匹配
                echo "$target"
            fi
        fi
    fi
}

# 执行单个备份
do_backup() {
    local key="$1"
    local item=$(get_backup_item "$key")

    if [ -z "$item" ]; then
        echo "错误: 未找到备份项 '$key'"
        return 1
    fi

    local dir=$(echo "$item" | cut -d: -f1)
    local repo=$(echo "$item" | cut -d: -f2)
    local desc=$(echo "$item" | cut -d: -f3)

    # 展开 ~ 为实际路径
    dir="${dir/#\~/$HOME}"

    echo "=== 备份: $key ($desc) ==="
    echo "路径: $dir"
    echo "仓库: $repo"

    if [ ! -d "$dir" ]; then
        echo "错误: 目录不存在: $dir"
        return 1
    fi

    cd "$dir" || return 1

    # 检查是否有 git 仓库，如果没有则初始化
    if [ ! -d ".git" ]; then
        echo "警告: $dir 不是一个 git 仓库，正在初始化..."
        git init

        # 拷贝 .gitignore 到目标目录（如果存在）
        local skill_gitignore="$SCRIPT_DIR/../.gitignore"
        if [ -f "$skill_gitignore" ]; then
            cp "$skill_gitignore" "$dir/.gitignore"
            echo "已拷贝 .gitignore 到 $dir"
        fi

        git add .
        git commit -m "ORG"
    fi

    # 添加远程仓库（如果不存在）
    if ! git remote | grep -q origin; then
        git remote add origin "$(get_remote_url "$repo")"
    fi

    # 检查远程是否有本地不存在的提交（防止 -f 强制覆盖导致远程提交丢失）
    if git rev-parse "origin/$GIT_BRANCH" >/dev/null 2>&1; then
        local remote_ahead=$(git rev-list --count "origin/$GIT_BRANCH"..HEAD 2>/dev/null || echo 0)
        local local_ahead=$(git rev-list --count HEAD.."origin/$GIT_BRANCH" 2>/dev/null || echo 0)
        if [ "$remote_ahead" -gt 0 ] && [ "$local_ahead" -eq 0 ]; then
            echo "错误: 远程分支包含本地不存在的提交，拒绝强制推送以防止数据丢失。"
            echo "请先拉取远程更新: git pull origin $GIT_BRANCH --rebase"
            return 1
        fi
    fi

    # 执行备份
    git add .
    git commit -m "$COMMIT_MSG"
    git push -u origin "$GIT_BRANCH"

    echo ""
}

# 停止 gateway(调试的时候不要用)
# openclaw gateway stop

# 备份指定的项
FAILED=0
for key in $(get_keys_to_backup "$TARGET"); do
    do_backup "$key" || FAILED=1
done

# 启动 gateway(调试的时候不要用)
# openclaw gateway start

if [ "$FAILED" -eq 0 ]; then
    echo "=== 备份完成 ==="
else
    echo "=== 备份失败 ==="
    exit 1
fi