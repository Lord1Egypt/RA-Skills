#!/bin/bash

# GitHub Memory Sync Script
# 将 OpenClaw 完整工作空间配置同步到 GitHub

set -e

WORKSPACE_DIR="${WORKSPACE_DIR:-/root/.openclaw/workspace}"
GITHUB_REPO="${GITHUB_REPO}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"
GITHUB_TOKEN="${GITHUBTOKEN}"

# 同步模式：full（完整）或 memory-only（仅记忆）
SYNC_MODE="${SYNC_MODE:-full}"

if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_REPO" ]; then
    echo "❌ 错误：请配置 GITHUBTOKEN 和 GITHUB_REPO 环境变量"
    exit 1
fi

REPO_URL="https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git"
SYNC_DIR="/tmp/openclaw-memory-sync-$$"

cleanup() {
    rm -rf "$SYNC_DIR"
}
trap cleanup EXIT

# 复制所有工作空间文件
copy_workspace_files() {
    local src="$1"
    local dst="$2"
    local count=0
    
    # 核心记忆文件（必须同步）
    local core_files=("MEMORY.md" "SOUL.md" "IDENTITY.md" "USER.md" "TOOLS.md" "HEARTBEAT.md" "AGENTS.md")
    
    for file in "${core_files[@]}"; do
        if [ -f "$src/$file" ]; then
            cp "$src/$file" "$dst/$file"
            echo "  📄 $file"
            count=$((count + 1))
        fi
    done
    
    # memory/ 目录
    if [ -d "$src/memory" ] && [ "$(ls -A "$src/memory" 2>/dev/null)" ]; then
        mkdir -p "$dst/memory"
        cp -r "$src/memory"/* "$dst/memory/"
        echo "  📁 memory/ 目录 ($(ls "$src/memory" | wc -l) 个文件)"
        count=$((count + 1))
    fi
    
    # 可选：skills/ 目录（自定义技能）
    if [ "$SYNC_MODE" = "full" ] && [ -d "$src/skills" ] && [ "$(ls -A "$src/skills" 2>/dev/null)" ]; then
        mkdir -p "$dst/skills"
        # 排除 node_modules
        rsync -a --exclude 'node_modules' "$src/skills/" "$dst/skills/" 2>/dev/null || cp -r "$src/skills"/* "$dst/skills/"
        echo "  📁 skills/ 目录"
        count=$((count + 1))
    fi
    
    # 可选：avatars/ 目录
    if [ "$SYNC_MODE" = "full" ] && [ -d "$src/avatars" ] && [ "$(ls -A "$src/avatars" 2>/dev/null)" ]; then
        mkdir -p "$dst/avatars"
        cp -r "$src/avatars"/* "$dst/avatars/"
        echo "  📁 avatars/ 目录"
        count=$((count + 1))
    fi
    
    # 可选：BOOTSTRAP.md
    if [ -f "$src/BOOTSTRAP.md" ]; then
        cp "$src/BOOTSTRAP.md" "$dst/BOOTSTRAP.md"
        echo "  📄 BOOTSTRAP.md"
        count=$((count + 1))
    fi
    
    # 可选：projects/agents/ 目录（多 Agent 配置）
    if [ "$SYNC_MODE" = "full" ] && [ -d "$src/projects/agents" ] && [ "$(ls -A "$src/projects/agents" 2>/dev/null)" ]; then
        mkdir -p "$dst/projects/agents"
        cp -r "$src/projects/agents"/* "$dst/projects/agents/"
        echo "  📁 projects/agents/ 目录 ($(ls "$src/projects/agents" | wc -l) 个 Agent)"
        count=$((count + 1))
    fi
    
    echo ""
    echo "  共计：$count 个文件/目录"
}

# 显示帮助
show_help() {
    echo "GitHub Memory Sync - 完整工作空间备份工具"
    echo ""
    echo "用法：$0 {init|push|pull|status|list} [选项]"
    echo ""
    echo "命令说明:"
    echo "  init   - 初始化 GitHub 仓库连接（首次使用）"
    echo "  push   - 推送本地工作空间到 GitHub"
    echo "  pull   - 从 GitHub 拉取工作空间到本地"
    echo "  status - 检查同步状态"
    echo "  list   - 列出所有同步的文件"
    echo ""
    echo "选项:"
    echo "  --memory-only  - 仅同步 memory 文件（不包括 SOUL.md, IDENTITY.md 等）"
    echo "  --full         - 同步完整工作空间（包括 skills/, avatars/ 等）"
    echo ""
    echo "环境变量:"
    echo "  GITHUBTOKEN    - GitHub Personal Access Token"
    echo "  GITHUB_REPO    - GitHub 仓库 (格式：username/repo)"
    echo "  GITHUB_BRANCH  - 分支名称 (默认：main)"
    echo "  WORKSPACE_DIR  - Workspace 目录路径 (默认：/root/.openclaw/workspace)"
    echo "  SYNC_MODE      - 同步模式：full 或 memory-only (默认：full)"
    echo ""
    echo "示例:"
    echo "  $0 push                    # 完整同步"
    echo "  $0 push --memory-only      # 仅同步 memory"
    echo "  $0 pull                    # 恢复所有文件"
    echo "  $0 status                  # 检查同步状态"
    exit 1
}

case "$1" in
    init)
        echo "🔧 初始化 GitHub Memory 同步..."
        echo "📁 Workspace 目录：$WORKSPACE_DIR"
        echo "📦 GitHub 仓库：$GITHUB_REPO"
        echo "🌿 分支：$GITHUB_BRANCH"
        echo "📋 同步模式：$SYNC_MODE"
        echo ""
        
        mkdir -p "$SYNC_DIR"
        cd "$SYNC_DIR"
        git init -q
        git remote add origin "$REPO_URL"
        
        # 复制文件
        echo "📋 准备同步的文件："
        copy_workspace_files "$WORKSPACE_DIR" "$SYNC_DIR"
        
        # 检查是否有文件
        file_count=$(find . -type f ! -path "./.git/*" | wc -l)
        if [ "$file_count" -eq 0 ]; then
            echo "⚠️ 没有找到文件，创建占位符"
            mkdir -p memory
            touch memory/.gitkeep
        fi
        
        git add .
        git commit -m "Initial workspace backup - $(date +%Y-%m-%d)"
        
        # 重命名分支并推送
        git branch -M "$GITHUB_BRANCH"
        git push -u origin "$GITHUB_BRANCH" 2>/dev/null || {
            echo "ℹ️ 远程仓库已有内容，正在合并..."
            git pull origin "$GITHUB_BRANCH" --no-rebase --allow-unrelated-histories
            git push -u origin "$GITHUB_BRANCH"
        }
        
        echo ""
        echo "✅ 初始化完成"
        ;;
    
    push)
        # 解析选项
        shift
        while [[ $# -gt 0 ]]; do
            case $1 in
                --memory-only)
                    SYNC_MODE="memory-only"
                    shift
                    ;;
                --full)
                    SYNC_MODE="full"
                    shift
                    ;;
                *)
                    shift
                    ;;
            esac
        done
        
        echo "📤 推送工作空间到 GitHub..."
        echo "📋 同步模式：$SYNC_MODE"
        echo ""
        
        mkdir -p "$SYNC_DIR"
        cd "$SYNC_DIR"
        
        # 克隆或拉取
        cloned=false
        if [ -d ".git" ]; then
            git fetch origin "$GITHUB_BRANCH" 2>/dev/null && {
                git reset --hard "origin/$GITHUB_BRANCH" 2>/dev/null
                cloned=true
            }
        fi
        
        if [ "$cloned" = false ]; then
            git clone -b "$GITHUB_BRANCH" "$REPO_URL" . 2>/dev/null && cloned=true || {
                echo "ℹ️ 克隆失败，尝试初始化新仓库..."
                git init -q
                git remote add origin "$REPO_URL"
                git fetch origin "$GITHUB_BRANCH" 2>/dev/null && {
                    git reset --hard "origin/$GITHUB_BRANCH"
                    cloned=true
                } || {
                    echo "ℹ️ 远程无内容，创建新分支"
                    git checkout -b "$GITHUB_BRANCH"
                }
            }
        fi
        
        # 确保当前分支名正确
        git branch -M "$GITHUB_BRANCH" 2>/dev/null || true
        
        # 复制文件
        echo "📋 准备同步的文件："
        # 先清理旧文件（保留.git）
        find . -maxdepth 1 -type f ! -name ".git*" -delete
        rm -rf memory skills avatars
        
        copy_workspace_files "$WORKSPACE_DIR" "."
        
        # 检查是否有文件
        file_count=$(find . -type f ! -path "./.git/*" | wc -l)
        if [ "$file_count" -eq 0 ]; then
            echo "⚠️ 没有找到文件，创建占位符"
            mkdir -p memory
            touch memory/.gitkeep
        fi
        
        git add .
        git commit -m "Update workspace backup - $(date '+%Y-%m-%d %H:%M')" || {
            echo "ℹ️ 没有更改需要提交"
            echo "✅ 已经是最新状态"
            exit 0
        }
        git push origin "$GITHUB_BRANCH"
        
        echo ""
        echo "✅ 推送成功"
        echo "📦 仓库地址：https://github.com/${GITHUB_REPO}"
        ;;
    
    pull)
        echo "📥 从 GitHub 拉取工作空间..."
        echo ""
        
        mkdir -p "$SYNC_DIR"
        cd "$SYNC_DIR"
        
        git clone -b "$GITHUB_BRANCH" "$REPO_URL" .
        
        # 复制回 workspace
        echo "📋 恢复文件到 workspace："
        local count=0
        
        # 核心文件
        local core_files=("MEMORY.md" "SOUL.md" "IDENTITY.md" "USER.md" "TOOLS.md" "HEARTBEAT.md" "AGENTS.md")
        for file in "${core_files[@]}"; do
            if [ -f "$file" ]; then
                cp "$file" "$WORKSPACE_DIR/$file"
                echo "  📄 $file"
                count=$((count + 1))
            fi
        done
        
        # memory/ 目录
        if [ -d "memory" ] && [ "$(ls -A memory 2>/dev/null)" ]; then
            mkdir -p "$WORKSPACE_DIR/memory"
            cp -r memory/* "$WORKSPACE_DIR/memory/"
            echo "  📁 memory/ 目录"
            count=$((count + 1))
        fi
        
        # skills/ 目录（如果存在）
        if [ -d "skills" ] && [ "$(ls -A skills 2>/dev/null)" ]; then
            mkdir -p "$WORKSPACE_DIR/skills"
            cp -r skills/* "$WORKSPACE_DIR/skills/"
            echo "  📁 skills/ 目录"
            count=$((count + 1))
        fi
        
        # avatars/ 目录（如果存在）
        if [ -d "avatars" ] && [ "$(ls -A avatars 2>/dev/null)" ]; then
            mkdir -p "$WORKSPACE_DIR/avatars"
            cp -r avatars/* "$WORKSPACE_DIR/avatars/"
            echo "  📁 avatars/ 目录"
            count=$((count + 1))
        fi
        
        # BOOTSTRAP.md
        if [ -f "BOOTSTRAP.md" ]; then
            cp "BOOTSTRAP.md" "$WORKSPACE_DIR/BOOTSTRAP.md"
            echo "  📄 BOOTSTRAP.md"
            count=$((count + 1))
        fi
        
        # projects/agents/ 目录（如果存在）
        if [ -d "projects/agents" ] && [ "$(ls -A projects/agents 2>/dev/null)" ]; then
            mkdir -p "$WORKSPACE_DIR/projects/agents"
            cp -r projects/agents/* "$WORKSPACE_DIR/projects/agents/"
            echo "  📁 projects/agents/ 目录"
            count=$((count + 1))
        fi
        
        echo ""
        echo "✅ 拉取成功"
        echo "📂 恢复 $count 个文件/目录到：$WORKSPACE_DIR"
        ;;
    
    status)
        echo "📊 检查同步状态..."
        echo ""
        
        mkdir -p "$SYNC_DIR"
        cd "$SYNC_DIR"
        
        if [ ! -d ".git" ]; then
            git clone -b "$GITHUB_BRANCH" "$REPO_URL" . 2>/dev/null || {
                echo "⚠️ 远程仓库不存在，需要先初始化"
                exit 1
            }
        else
            git fetch origin "$GITHUB_BRANCH" 2>/dev/null || true
        fi
        
        echo "📁 本地文件（$WORKSPACE_DIR）："
        local local_count=0
        local core_files=("MEMORY.md" "SOUL.md" "IDENTITY.md" "USER.md" "TOOLS.md" "HEARTBEAT.md" "AGENTS.md")
        for file in "${core_files[@]}"; do
            if [ -f "$WORKSPACE_DIR/$file" ]; then
                echo "  ✅ $file"
                local_count=$((local_count + 1))
            else
                echo "  ❌ $file (不存在)"
            fi
        done
        
        if [ -d "$WORKSPACE_DIR/memory" ] && [ "$(ls -A "$WORKSPACE_DIR/memory" 2>/dev/null)" ]; then
            echo "  ✅ memory/ 目录 ($(ls "$WORKSPACE_DIR/memory" | wc -l) 个文件)"
            local_count=$((local_count + 1))
        else
            echo "  ⚠️ memory/ 目录 (空)"
        fi
        
        echo ""
        echo "📁 远程文件（GitHub）："
        local remote_count=0
        for file in "${core_files[@]}"; do
            if [ -f "$file" ]; then
                echo "  ✅ $file"
                remote_count=$((remote_count + 1))
            else
                echo "  ❌ $file (不存在)"
            fi
        done
        
        if [ -d "memory" ] && [ "$(ls -A memory 2>/dev/null)" ]; then
            echo "  ✅ memory/ 目录 ($(ls memory | wc -l) 个文件)"
            remote_count=$((remote_count + 1))
        else
            echo "  ⚠️ memory/ 目录 (空)"
        fi
        
        echo ""
        echo "🔍 差异检查："
        local diff_count=0
        
        for file in "${core_files[@]}"; do
            if [ -f "$WORKSPACE_DIR/$file" ] && [ -f "$file" ]; then
                if ! diff -q "$WORKSPACE_DIR/$file" "$file" > /dev/null 2>&1; then
                    echo "  ⚠️ $file 有差异"
                    diff_count=$((diff_count + 1))
                else
                    echo "  ✅ $file 已同步"
                fi
            fi
        done
        
        if [ -d "$WORKSPACE_DIR/memory" ] && [ -d "memory" ]; then
            if ! diff -rq "$WORKSPACE_DIR/memory" "memory" > /dev/null 2>&1; then
                echo "  ⚠️ memory/ 目录有差异"
                diff_count=$((diff_count + 1))
            else
                echo "  ✅ memory/ 目录已同步"
            fi
        fi
        
        echo ""
        if [ $diff_count -eq 0 ]; then
            echo "✅ 本地和远程完全同步"
        else
            echo "⚠️ 检测到 $diff_count 处差异，建议执行推送或拉取"
        fi
        ;;
    
    list)
        echo "📋 列出所有同步的文件..."
        echo ""
        
        echo "本地工作空间文件："
        find "$WORKSPACE_DIR" -maxdepth 1 -type f -name "*.md" | sort | while read file; do
            echo "  📄 $(basename "$file")"
        done
        
        if [ -d "$WORKSPACE_DIR/memory" ]; then
            echo ""
            echo "Memory 文件："
            find "$WORKSPACE_DIR/memory" -type f -name "*.md" | sort | while read file; do
                echo "  📄 memory/$(basename "$file")"
            done
        fi
        
        if [ -d "$WORKSPACE_DIR/skills" ]; then
            echo ""
            echo "Skills 目录："
            ls -la "$WORKSPACE_DIR/skills" | tail -n +4 | while read line; do
                echo "  📁 $line"
            done
        fi
        ;;
    
    *)
        show_help
        ;;
esac
