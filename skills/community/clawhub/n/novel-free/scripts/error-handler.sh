#!/usr/bin/env bash
#
# novel-free 错误处理与恢复脚本
# 提供统一的错误处理框架
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 日志函数
log_error() {
    local project_dir="$1"
    local agent="$2"
    local task="$3"
    local error="$4"
    local archive_file="$project_dir/archive/archive.md"
    
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    echo "[ERROR $timestamp] Agent: $agent, Task: $task, Error: $error"
    
    if [[ -f "$archive_file" ]]; then
        echo -e "\n## 错误记录" >> "$archive_file"
        echo "| 时间 | Agent | 任务 | 错误 |" >> "$archive_file"
        echo "|------|-------|------|------|" >> "$archive_file"
        echo "| $timestamp | $agent | $task | $error |" >> "$archive_file"
    fi
}

# 恢复函数
resume_project() {
    local project_dir="$1"
    
    if [[ -z "$project_dir" ]] || [[ ! -d "$project_dir" ]]; then
        echo "用法: $0 resume <项目目录>"
        exit 1
    fi
    
    echo "开始恢复项目: $project_dir"
    
    # 检查状态文件
    local state_file="$project_dir/meta/workflow-state.json"
    if [[ ! -f "$state_file" ]]; then
        echo "错误: 未找到工作流状态文件"
        exit 1
    fi
    
    # 读取当前状态
    local phase current_chapter resume_required
    phase=$(grep -o '"currentPhase":[[:space:]]*[0-9]*' "$state_file" | grep -o '[0-9]*')
    current_chapter=$(grep -o '"currentChapter":[[:space:]]*[0-9]*' "$state_file" | grep -o '[0-9]*')
    resume_required=$(grep -o '"resumeRequired":[[:space:]]*true' "$state_file")
    
    echo "项目状态:"
    echo "  当前阶段: Phase $phase"
    echo "  当前章节: 第 $current_chapter 章"
    echo "  需要恢复: ${resume_required:+是}${resume_required:-否}"
    
    # 提供恢复建议
    case $phase in
        0)
            echo "恢复建议: 项目处于初始化阶段，请继续 Phase 0 流程"
            ;;
        1)
            echo "恢复建议: 项目处于架构阶段，请检查 Phase 1 各步骤完成情况"
            echo "  检查文件:"
            echo "    - $project_dir/worldbuilding/world.md"
            echo "    - $project_dir/characters/protagonist.md"
            echo "    - $project_dir/outline/outline.md"
            ;;
        2)
            if [[ -n "$resume_required" ]]; then
                echo "恢复建议: 需要执行恢复协议 (resume-protocol.md)"
                echo "  1. 阅读 $SKILL_DIR/references/resume-protocol.md"
                echo "  2. 检查上一章状态"
                echo "  3. 更新工作流状态"
            else
                echo "恢复建议: 继续写作第 $((current_chapter + 1)) 章"
            fi
            ;;
        3)
            echo "恢复建议: 项目处于维护阶段"
            ;;
        *)
            echo "恢复建议: 未知阶段"
            ;;
    esac
    
    # 检查关键文件
    echo ""
    echo "关键文件状态:"
    local files=(
        "$project_dir/meta/config.md"
        "$project_dir/meta/style-anchor.md"
        "$project_dir/references/fixed-context.md"
    )
    
    for file in "${files[@]}"; do
        if [[ -f "$file" ]]; then
            local size=$(wc -l < "$file" 2>/dev/null || echo "0")
            echo "  ✓ $(basename "$file") (${size}行)"
        else
            echo "  ✗ $(basename "$file") (缺失)"
        fi
    done
}

# 备份函数
backup_project() {
    local project_dir="$1"
    local backup_dir="${2:-$project_dir/../backups}"
    
    if [[ -z "$project_dir" ]] || [[ ! -d "$project_dir" ]]; then
        echo "用法: $0 backup <项目目录> [备份目录]"
        exit 1
    fi
    
    local project_name=$(basename "$project_dir")
    local timestamp=$(date +"%Y%m%d-%H%M%S")
    local backup_name="${project_name}_${timestamp}.tar.gz"
    local backup_path="$backup_dir/$backup_name"
    
    mkdir -p "$backup_dir"
    
    echo "开始备份项目: $project_name"
    echo "备份到: $backup_path"
    
    # 排除临时文件和缓存
    tar -czf "$backup_path" \
        --exclude="*.bak" \
        --exclude="*/.cache" \
        --exclude="*/temp" \
        -C "$(dirname "$project_dir")" \
        "$project_name"
    
    local size=$(du -h "$backup_path" | cut -f1)
    echo "✅ 备份完成: $backup_name (${size})"
    
    # 保留最近5个备份
    ls -t "$backup_dir"/"${project_name}"_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -f
}

# 模型回退函数
model_fallback() {
    local agent="$1"
    local original_model="$2"
    local config_file="$3"
    
    echo "模型回退触发: $agent 使用 $original_model 失败"
    
    # 读取备选模型配置
    local fallback_model=""
    if [[ -f "$config_file" ]]; then
        # 简化实现：使用OOC模型作为备选
        fallback_model=$(grep -A1 "OOC守护" "$config_file" | tail -1 | grep -o '|[^|]*|' | tr -d '| ' | head -1)
    fi
    
    if [[ -n "$fallback_model" ]] && [[ "$fallback_model" != "$original_model" ]]; then
        echo "回退到备选模型: $fallback_model"
        echo "$fallback_model"
    else
        echo "无可用备选模型，需要Coordinator自行处理"
        echo "coordinator"
    fi
}

# 主函数
main() {
    local action="$1"
    local project_dir="$2"
    
    case "$action" in
        "resume")
            resume_project "$project_dir"
            ;;
        "backup")
            backup_project "$project_dir" "$3"
            ;;
        "log-error")
            log_error "$project_dir" "$3" "$4" "$5"
            ;;
        "model-fallback")
            model_fallback "$3" "$4" "$project_dir/meta/config.md"
            ;;
        *)
            echo "用法: $0 <action> <项目目录> [参数...]"
            echo ""
            echo "可用操作:"
            echo "  resume         - 恢复中断的项目"
            echo "  backup         - 备份项目"
            echo "  log-error      - 记录错误日志"
            echo "  model-fallback - 模型回退处理"
            echo ""
            echo "示例:"
            echo "  $0 resume /path/to/novel-project"
            echo "  $0 backup /path/to/novel-project"
            exit 1
            ;;
    esac
}

main "$@"