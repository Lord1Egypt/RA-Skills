#!/bin/bash

set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
GIT_DIR="$OPENCLAW_HOME/.git"

TAG_PREFIX_SAFE="config-safe-"
TAG_PREFIX_WORKING="config-working-"
TAG_PREFIX_BASELINE="config-baseline-"

# 注意：实际忽略规则以 .gitignore 为准，这里仅作参考

show_usage() {
    cat << EOF
OpenClaw 配置文件 Git 标记管理工具

用法: $(basename "$0") <命令> [选项]

命令:
    save-safe      保存当前安全版本标记
    save-working  保存当前工作版本标记
    save-baseline 保存每日基线版本标记
    list          列出所有配置标记
    rollback <标签> 回滚到指定标签
    quick-rollback 快速回滚到上一个安全版本
    diff <标签>   查看当前配置与指定标签的差异
    status        查看当前Git状态
    help          显示帮助信息

示例:
    $(basename "$0") save-safe          # 保存当前为安全版本
    $(basename "$0") list                # 列出所有标记
    $(basename "$0") quick-rollback     # 快速回滚到上一个安全版本
    $(basename "$0") diff config-safe-20260306-100000

EOF
}

cd "$OPENCLAW_HOME"

init_git_repo() {
    if [ ! -d "$GIT_DIR" ]; then
        git init
        git config user.email "openclaw@local"
        git config user.name "OpenClaw"
        
        if [ ! -f .gitignore ]; then
            cat > .gitignore << 'GITIGNORE'
logs/
*.log
backups/
agents/
extensions/
node_modules/
.DS_Store
*.db
*.sqlite
*.tmp
credentials/
GITIGNORE
            git add -f .gitignore
            git commit -m "Initial: add .gitignore" >/dev/null 2>&1 || true
        fi
        
        echo "✅ Git 仓库已初始化"
    fi
}

get_timestamp() {
    date '+%Y%m%d-%H%M%S'
}

save_tag() {
    local prefix="$1"
    local tag_name="${prefix}$(get_timestamp)"
    
    init_git_repo
    
    cd "$OPENCLAW_HOME"
    
    git add -A -- ':!.gitignore'
    
    if git diff --staged --quiet; then
        echo "⚠️  没有需要提交的更改"
        return 0
    fi
    
    git commit -m "Config: $tag_name" >/dev/null 2>&1 || true
    
    git tag "$tag_name"
    
    echo "✅ 已保存标记: $tag_name"
}

list_tags() {
    cd "$OPENCLAW_HOME"
    
    if [ ! -d "$GIT_DIR" ]; then
        echo "❌ Git 仓库未初始化，请先运行 save-safe"
        exit 1
    fi
    
    echo "========================================"
    echo "    OpenClaw 配置标记列表"
    echo "========================================"
    echo ""
    
    echo "🛡️  安全版本:"
    git tag -l "${TAG_PREFIX_SAFE}*" 2>/dev/null | sort -r | head -5 || echo "   (无)"
    echo ""
    
    echo "✅ 工作版本:"
    git tag -l "${TAG_PREFIX_WORKING}*" 2>/dev/null | sort -r | head -5 || echo "   (无)"
    echo ""
    
    echo "📅 基线版本:"
    git tag -l "${TAG_PREFIX_BASELINE}*" 2>/dev/null | sort -r | head -5 || echo "   (无)"
    echo ""
}

rollback_to_tag() {
    local tag_name="$1"
    
    if [ -z "$tag_name" ]; then
        echo "❌ 请指定标签名称"
        echo "   使用 $(basename "$0") quick-rollback 快速回滚"
        exit 1
    fi
    
    cd "$OPENCLAW_HOME"
    
    if git show-ref --tags --verify --quiet "refs/tags/$tag_name"; then
        echo "📥 正在回滚到: $tag_name"
        
        git checkout "$tag_name" -- . >/dev/null 2>&1
        
        echo "✅ 配置已恢复到: $tag_name"
        
        if command -v openclaw >/dev/null 2>&1; then
            echo ""
            echo "🔄 正在重启网关..."
            openclaw gateway stop 2>/dev/null || true
            sleep 1
            openclaw gateway >/dev/null 2>&1 &
            sleep 3
            echo "✅ 网关已重启"
        fi
    else
        echo "❌ 标签不存在: $tag_name"
        echo "   使用 $(basename "$0") list 查看所有标签"
        exit 1
    fi
}

quick_rollback() {
    cd "$OPENCLAW_HOME"
    
    local latest_safe
    latest_safe=$(git tag -l "${TAG_PREFIX_SAFE}*" 2>/dev/null | sort -r | head -1)
    
    if [ -n "$latest_safe" ]; then
        echo "🔄 快速回滚到上一个安全版本: $latest_safe"
        rollback_to_tag "$latest_safe"
    else
        echo "❌ 未找到安全版本标记"
        echo "   请先使用 $(basename "$0") save-safe 保存安全版本"
        exit 1
    fi
}

show_diff() {
    local tag_name="$1"
    
    if [ -z "$tag_name" ]; then
        echo "❌ 请指定标签名称"
        exit 1
    fi
    
    cd "$OPENCLAW_HOME"
    
    if git show-ref --tags --verify --quiet "refs/tags/$tag_name"; then
        echo "========================================"
        echo "    当前配置 vs $tag_name"
        echo "========================================"
        echo ""
        
        git diff "$tag_name" -- . | head -80
    else
        echo "❌ 标签不存在: $tag_name"
        exit 1
    fi
}

show_status() {
    cd "$OPENCLAW_HOME"
    
    if [ ! -d "$GIT_DIR" ]; then
        echo "❌ Git 仓库未初始化"
        exit 1
    fi
    
    echo "========================================"
    echo "    OpenClaw Git 状态"
    echo "========================================"
    echo ""
    
    git status --short
    echo ""
    git log --oneline -5
}

case "${1:-help}" in
    save-safe)
        save_tag "$TAG_PREFIX_SAFE"
        ;;
    save-working)
        save_tag "$TAG_PREFIX_WORKING"
        ;;
    save-baseline)
        save_tag "$TAG_PREFIX_BASELINE"
        ;;
    list)
        list_tags
        ;;
    rollback)
        rollback_to_tag "${2:-}"
        ;;
    quick-rollback)
        quick_rollback
        ;;
    diff)
        show_diff "${2:-}"
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "未知命令: $1"
        show_usage
        exit 1
        ;;
esac
