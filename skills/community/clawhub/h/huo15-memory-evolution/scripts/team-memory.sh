#!/bin/bash
#===============================================================================
# huo15-memory-evolution: Team Memory 共享工具
#
# 功能:
#   1. 标记某个记忆为团队共享（可以跨 agent 访问）
#   2. 将团队共享记忆同步到其他群聊 agent
#   3. 查看团队共享的记忆列表
#
# 用法:
#   ./team-memory.sh share <memory-file>     # 共享记忆
#   ./team-memory.sh unshare <memory-file>   # 取消共享
#   ./team-memory.sh list                    # 列出团队共享记忆
#   ./team-memory.sh sync                    # 同步到所有群聊 agent
#   ./team-memory.sh interactive             # 交互模式
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$(dirname "$0")")" && pwd)"

# 动态路由：优先使用 PWD 检测 > OC_AGENT_ID > 默认
if [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
elif [ -n "${OC_AGENT_ID:-}" ]; then
    WORKSPACE_DIR="$HOME/.openclaw/workspace-${OC_AGENT_ID}"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
SHARED_DIR="$MEMORY_DIR/shared"
TODAY=$(date +%Y-%m-%d)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

# 列出团队共享记忆
list_shared() {
    log "📋 团队共享记忆列表"
    echo ""
    
    if [ ! -d "$SHARED_DIR" ]; then
        warn "还没有共享的记忆"
        return
    fi
    
    local count=0
    for file in "$SHARED_DIR"/*.md; do
        if [ -f "$file" ]; then
            local name=$(basename "$file" .md)
            local type=$(grep "^type:" "$file" | sed 's/type: //' | tr -d ' ')
            local desc=$(grep "^description:" "$file" | sed 's/description: //' | tr -d ' ')
            local updated=$(grep "^updated:" "$file" | sed 's/updated: //' | tr -d ' ')
            echo "  $CYAN$name$NC"
            echo "    类型: $type | 更新: $updated"
            echo "    描述: $desc"
            echo ""
            count=$((count + 1))
        fi
    done
    
    if [ $count -eq 0 ]; then
        warn "还没有共享的记忆"
    else
        log "共 $count 个共享记忆"
    fi
}

# 共享记忆
share_memory() {
    local memory_path="$1"
    
    if [ -z "$memory_path" ]; then
        error "请指定记忆文件路径"
        return 1
    fi
    
    # 解析路径
    local full_path=""
    local rel_path=""
    
    if [[ "$memory_path" == memory/* ]]; then
        full_path="$MEMORY_DIR/${memory_path#memory/}"
        rel_path="$memory_path"
    elif [[ "$memory_path" == */* ]]; then
        full_path="$MEMORY_DIR/$memory_path"
        rel_path="$memory_path"
    else
        # 尝试在各个类型目录中查找
        for type in user feedback project reference; do
            if [ -f "$MEMORY_DIR/$type/$memory_path.md" ]; then
                full_path="$MEMORY_DIR/$type/$memory_path.md"
                rel_path="$type/$memory_path.md"
                break
            fi
        done
    fi
    
    if [ ! -f "$full_path" ]; then
        error "文件不存在: $memory_path"
        return 1
    fi
    
    # 创建共享目录
    mkdir -p "$SHARED_DIR"
    
    # 复制到共享目录
    local filename=$(basename "$full_path")
    local shared_path="$SHARED_DIR/$filename"
    
    # 添加共享标记
    cat "$full_path" | sed "s/^---$/---\nshared: true\nshared_at: ${TODAY}/" > "$shared_path"
    
    # 添加到团队索引
    add_to_team_index "$shared_path" "$rel_path"
    
    log "✅ 已共享: $memory_path"
    log "   共享路径: shared/$filename"
}

# 从团队共享中移除
unshare_memory() {
    local memory_path="$1"
    
    if [ -z "$memory_path" ]; then
        error "请指定记忆文件路径"
        return 1
    fi
    
    local filename=$(basename "$memory_path" .md)
    local shared_path="$SHARED_DIR/${filename}.md"
    
    if [ ! -f "$shared_path" ]; then
        error "文件不在共享列表中: $memory_path"
        return 1
    fi
    
    rm "$shared_path"
    remove_from_team_index "$filename"
    
    log "✅ 已取消共享: $memory_path"
}

# 添加到团队索引
add_to_team_index() {
    local shared_path="$1"
    local original_path="$2"
    
    local team_index="$MEMORY_DIR/team-index.md"
    
    if [ ! -f "$team_index" ]; then
        cat << 'EOF' > "$team_index"
---
name: team-memory-index
type: reference
description: 团队共享记忆索引
created: ${TODAY}
updated: ${TODAY}
---

# Team Memory Index

## 共享记忆

EOF
    fi
    
    local name=$(basename "$shared_path" .md)
    local type=$(grep "^type:" "$shared_path" | sed 's/type: //' | tr -d ' ')
    local desc=$(grep "^description:" "$shared_path" | sed 's/description: //' | tr -d ' ')
    
    # 添加条目
    echo "- **$name** ($type) - $desc" >> "$team_index"
}

# 从团队索引移除
remove_from_team_index() {
    local name="$1"
    
    local team_index="$MEMORY_DIR/team-index.md"
    
    if [ -f "$team_index" ]; then
        sed -i '' "/^- \*\*$name\*\*/d" "$team_index"
        log "   已从团队索引移除"
    fi
}

# 同步到所有群聊 agent
sync_to_group_agents() {
    log "🔄 同步团队共享记忆到群聊 Agent..."
    echo ""
    
    # 找到所有群聊 workspace
    local group_workspaces=$(find "$HOME/.openclaw" -maxdepth 1 -type d -name "workspace-wecom-default-group-*" | sort)
    local count=0
    
    for ws in $group_workspaces; do
        local ws_name=$(basename "$ws")
        
        # 跳过当前 agent
        if [[ "$ws" == "$WORKSPACE_DIR" ]]; then
            continue
        fi
        
        # 创建共享目录
        mkdir -p "$ws/memory/shared"
        
        # 同步共享记忆
        if [ -d "$SHARED_DIR" ]; then
            for shared_file in "$SHARED_DIR"/*.md; do
                if [ -f "$shared_file" ]; then
                    cp "$shared_file" "$ws/memory/shared/"
                    count=$((count + 1))
                fi
            done
        fi
        
        echo "  → $ws_name"
    done
    
    log "✅ 同步完成: $count 个文件"
}

# 交互模式
interactive() {
    log "👥 Team Memory 共享 - 交互模式"
    echo ""
    
    while true; do
        echo "选择操作:"
        echo "  1) 共享记忆"
        echo "  2) 取消共享"
        echo "  3) 查看共享列表"
        echo "  4) 同步到群聊"
        echo "  5) 退出"
        read -p "请输入选项 (1-5): " choice
        
        case "$choice" in
            1)
                echo ""
                list_all_memories
                echo ""
                read -p "请输入要共享的记忆名称: " mem_name
                share_memory "$mem_name"
                ;;
            2)
                echo ""
                list_shared
                echo ""
                read -p "请输入要取消共享的记忆名称: " mem_name
                unshare_memory "$mem_name"
                ;;
            3)
                echo ""
                list_shared
                ;;
            4)
                echo ""
                sync_to_group_agents
                ;;
            5)
                log "再见!"
                break
                ;;
            *)
                error "无效选择"
                ;;
        esac
        echo ""
    done
}

# 列出所有可共享的记忆
list_all_memories() {
    log "📚 可共享的记忆:"
    echo ""
    
    for type in user feedback project reference; do
        local type_dir="$MEMORY_DIR/$type"
        if [ -d "$type_dir" ]; then
            for file in "$type_dir"/*.md; do
                if [ -f "$file" ]; then
                    local name=$(basename "$file" .md)
                    local desc=$(grep "^description:" "$file" | sed 's/description: //' | tr -d ' ')
                    echo "  [$type] $name - $desc"
                fi
            done
        fi
    done
}

# 主逻辑
main() {
    local command="$1"
    shift
    
    case "$command" in
        share)
            share_memory "$1"
            ;;
        unshare)
            unshare_memory "$1"
            ;;
        list)
            list_shared
            ;;
        sync)
            sync_to_group_agents
            ;;
        interactive|-i)
            interactive
            ;;
        *)
            echo "用法: $0 <share|unshare|list|sync|interactive>"
            echo ""
            echo "  share <memory>   - 共享记忆"
            echo "  unshare <memory> - 取消共享"
            echo "  list            - 列出共享记忆"
            echo "  sync           - 同步到群聊"
            echo "  interactive    - 交互模式"
            ;;
    esac
}

main "$@"
