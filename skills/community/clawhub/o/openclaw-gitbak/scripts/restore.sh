#!/bin/bash
# OpenClaw GitBak 通用恢复脚本
# 用法: restore.sh [key|all]
# 示例:
#   bash ./restore.sh cfg
#   bash ./restore.sh workspace-coder
#   bash ./restore.sh all

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.sh"

TARGET="$1"

if [ -z "$TARGET" ]; then
    echo "用法: restore.sh [key|all]"
    echo "可用恢复项:"
    for key in $(get_backup_keys); do
        local item=$(get_backup_item "$key")
        local desc=$(echo "$item" | cut -d: -f3)
        echo "  $key - $desc"
    done
    exit 1
fi

# 解析需要恢复的键列表
get_keys_to_restore() {
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
# 执行单个恢复
do_restore() {
    local key="$1"
    local item=$(get_backup_item "$key")

    if [ -z "$item" ]; then
        echo "错误: 未找到恢复项 '$key'"
        return 1
    fi
    local dir=$(echo "$item" | cut -d: -f1)
    local repo=$(echo "$item" | cut -d: -f2)
    local desc=$(echo "$item" | cut -d: -f3)
    # 展开 ~ 为实际路径
    dir="${dir/#\~/$HOME}"
    echo "=== 恢复: $key ($desc) ==="
    echo "路径: $dir"
    echo "仓库: $repo"
    # 停止 gateway(调试的时候不要用)
    # openclaw gateway stop
    # 目录存在：拉取，不存在：克隆
    if [ -d "$dir" ]; then
        echo "$dir 目录已存在，从git拉取"
        cd "$dir" || return 1
        # 添加远程仓库（如果不存在）
        if ! git remote | grep -q origin; then
            find . -type f -not -path './.git/*' -delete        # 删除，除.git目录外的所有文件，否则会要求合并
            git remote add origin "$(get_remote_url "$repo")"   # 添加远程仓库
        fi
        # 拉取最新代码
        git fetch origin
        git pull origin "$GIT_BRANCH"
    else
        # 创建父目录
        local parent_dir="$(dirname "$dir")"
        mkdir -p "$parent_dir"
        cd "$parent_dir" || return 1
        git clone "$(get_remote_url "$repo")" "$(basename "$dir")"
    fi
    # 启动 gateway(调试的时候不要用)
    # openclaw gateway start
    echo ""
}
# 恢复指定的项
FAILED=0
for key in $(get_keys_to_restore "$TARGET"); do
    do_restore "$key" || FAILED=1
done

if [ "$FAILED" -eq 0 ]; then
    echo "=== 恢复完成 ==="
else
    echo "=== 恢复失败 ==="
    exit 1
fi
