#!/usr/bin/env bash
#===============================================================================
# task-progress.sh - 任务进度追踪器
# 
# 对标 context-persistence 的 Layer 3（Task Progress Files），
# 实现跨会话的任务状态持久化。
#
# 功能：
#   1. 创建任务进度文件
#   2. 更新任务状态
#   3. 跨会话恢复任务上下文
#   4. 任务完成后归档
#
# 文件位置：memory/project/{task-name}-progress.md
#
# 作者：火一五 | 基于 Claude Code 架构分析
#===============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 自动检测 workspace 路径
# 优先级：WORKSPACE_DIR 环境变量 > PWD > 默认
if [ -n "${WORKSPACE_DIR:-}" ]; then
    : # 使用环境变量
elif [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi
MEMORY_DIR="$WORKSPACE_DIR/memory"
PROJECT_DIR="$MEMORY_DIR/project"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }

#----------------------------------------------------------
# 创建任务
#----------------------------------------------------------
task_create() {
    local name="$1"
    local description="${2:-}"
    local priority="${3:-medium}"
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    if [ -z "$name" ]; then
        log_warn "用法: task-progress.sh create <任务名> [描述] [优先级]"
        return 1
    fi
    
    # 安全的文件名（支持中文）
    local safe_name
    safe_name=$(echo "$name" | python3 -c "import sys,re; print(re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]','_',sys.stdin.read())[:50])")
    local filepath="$PROJECT_DIR/${safe_name}-progress.md"
    
    mkdir -p "$PROJECT_DIR"
    
    cat > "$filepath" << EOF
---
name: "$name"
status: in-progress
priority: $priority
created: $timestamp
updated: $timestamp
---

# $name

$description

## 进度日志

### $timestamp
- 任务创建

## 检查点

- [ ] 检查点 1
- [ ] 检查点 2

## 关联记忆

_(在此记录相关的 memory/* 文件)_

## 备注

_(额外信息)_
EOF
    
    log_ok "任务已创建: $safe_name-progress.md"
    echo "$filepath"
}

#----------------------------------------------------------
# 更新任务状态
#----------------------------------------------------------
task_update() {
    local name="$1"
    local update_type="$2"  # status/progress/note/checkpoint/done
    local value="${3:-}"
    
    if [ -z "$name" ] || [ -z "$update_type" ]; then
        log_warn "用法: task-progress.sh update <任务名> <类型> [值]"
        return 1
    fi
    
    local safe_name
    safe_name=$(echo "$name" | python3 -c "import sys,re; print(re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]','_',sys.stdin.read())[:50])")
    local filepath="$PROJECT_DIR/${safe_name}-progress.md"
    
    if [ ! -f "$filepath" ]; then
        log_warn "任务不存在: $safe_name"
        return 1
    fi
    
    local timestamp
    timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    case "$update_type" in
        status)
            if [ -z "$value" ]; then
                log_warn "需要指定状态值: in-progress/blocked/done/waiting"
                return 1
            fi
            sed -i '' "s/^status:.*/status: $value/" "$filepath"
            log_ok "状态更新: $value"
            ;;
        progress)
            if [ -z "$value" ]; then
                log_warn "需要指定进度描述"
                return 1
            fi
            sed -i '' "s/^updated:.*/updated: $timestamp/" "$filepath"
            echo "" >> "$filepath"
            echo "### $timestamp" >> "$filepath"
            echo "- $value" >> "$filepath"
            log_ok "进度已记录"
            ;;
        note)
            if [ -z "$value" ]; then
                log_warn "需要指定备注内容"
                return 1
            fi
            sed -i '' "s/^updated:.*/updated: $timestamp/" "$filepath"
            echo "" >> "$filepath"
            echo "## 备注" >> "$filepath"
            echo "$value" >> "$filepath"
            log_ok "备注已添加"
            ;;
        checkpoint)
            local checkpoint="${value:-检查点}"
            sed -i '' "s/^updated:.*/updated: $timestamp/" "$filepath"
            sed -i '' "s/- \[ \] \(.*\)/- [x] \1/" "$filepath"
            echo "" >> "$filepath"
            echo "### $timestamp" >> "$filepath"
            echo "- 完成: $checkpoint" >> "$filepath"
            log_ok "检查点已完成: $checkpoint"
            ;;
        done)
            sed -i '' "s/^status:.*/status: done/" "$filepath"
            sed -i '' "s/^updated:.*/updated: $timestamp/" "$filepath"
            echo "" >> "$filepath"
            echo "### $timestamp" >> "$filepath"
            echo "- 任务完成" >> "$filepath"
            log_ok "任务已标记为完成"
            ;;
        *)
            log_warn "未知更新类型: $update_type"
            return 1
            ;;
    esac
}

#----------------------------------------------------------
# 列出任务
#----------------------------------------------------------
task_list() {
    local filter="${1:-}"  # all/in-progress/done/blocked
    
    if [ ! -d "$PROJECT_DIR" ]; then
        echo "暂无任务"
        return
    fi
    
    echo "📋 任务列表"
    echo "============"
    echo ""
    
    local count=0
    for f in "$PROJECT_DIR"/*-progress.md; do
        [ -f "$f" ] || continue
        
        local name status priority updated
        name=$(grep "^name:" "$f" | head -1 | cut -d'"' -f2)
        status=$(grep "^status:" "$f" | head -1 | awk '{print $2}')
        priority=$(grep "^priority:" "$f" | head -1 | awk '{print $2}')
        updated=$(grep "^updated:" "$f" | head -1 | awk '{print $2}')
        
        # 状态颜色
        local status_color=""
        case "$status" in
            in-progress) status_color="🟡" ;;
            done) status_color="🟢" ;;
            blocked) status_color="🔴" ;;
            waiting) status_color="⚪" ;;
            *) status_color="⚪" ;;
        esac
        
        # 过滤器
        if [ -n "$filter" ] && [ "$filter" != "all" ] && [ "$status" != "$filter" ]; then
            continue
        fi
        
        echo "$status_color $name"
        echo "   状态: $status | 优先级: $priority | 更新: $updated"
        echo ""
        
        count=$((count + 1))
    done
    
    if [ "$count" -eq 0 ]; then
        echo "(无任务)"
    fi
}

#----------------------------------------------------------
# 恢复任务上下文
#----------------------------------------------------------
task_resume() {
    local name="$1"
    
    if [ -z "$name" ]; then
        log_warn "用法: task-progress.sh resume <任务名>"
        return 1
    fi
    
    local safe_name
    safe_name=$(echo "$name" | python3 -c "import sys,re; print(re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]','_',sys.stdin.read())[:50])")
    local filepath="$PROJECT_DIR/${safe_name}-progress.md"
    
    if [ ! -f "$filepath" ]; then
        log_warn "任务不存在: $safe_name"
        return 1
    fi
    
    echo "## 📋 恢复任务: $name"
    echo ""
    grep -A 50 "^---$" "$filepath" | tail -n +2 | head -30
    echo ""
    echo "_完整内容见: $(basename "$filepath")_"
}

#----------------------------------------------------------
# 主函数
#----------------------------------------------------------
main() {
    local command="${1:-}"
    
    case "$command" in
        create|new)
            task_create "${2:-}" "${3:-}" "${4:-medium}"
            ;;
        update|set)
            task_update "${2:-}" "${3:-}" "${4:-}"
            ;;
        list|ls)
            task_list "${2:-all}"
            ;;
        resume|show)
            task_resume "${2:-}"
            ;;
        -h|--help|help)
            cat << 'EOF'
task-progress.sh - 任务进度追踪器

用法:
  task-progress.sh create <任务名> [描述] [优先级]
  task-progress.sh update <任务名> <类型> [值]
  task-progress.sh list [过滤器]
  task-progress.sh resume <任务名>
  task-progress.sh -h

更新类型:
  status <值>      - 设置状态 (in-progress/blocked/done/waiting)
  progress <描述>  - 添加进度日志
  note <内容>      - 添加备注
  checkpoint <名称> - 标记检查点完成
  done             - 标记任务完成

示例:
  task-progress.sh create "软著申请" "准备材料并提交" high
  task-progress.sh update "软著申请" progress "已收集所有文档"
  task-progress.sh update "软著申请" checkpoint "文档审查"
  task-progress.sh list in-progress
EOF
            ;;
        *)
            log_warn "用法: task-progress.sh <命令>"
            echo "输入 -h 查看帮助"
            return 1
            ;;
    esac
}

main "$@"
