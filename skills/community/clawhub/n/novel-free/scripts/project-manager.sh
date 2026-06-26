#!/usr/bin/env bash
#
# novel-free 项目管理脚本
# 提供项目切换、状态查看、环境隔离功能
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 配置
DEFAULT_PROJECTS_DIR="/root/.openclaw/workspace/novels"
PROJECT_ENV_FILE=".novel-free-env"

# 显示帮助
show_help() {
    cat << EOF
novel-free 项目管理脚本

用法: $0 <命令> [参数...]

命令:
  list               - 列出所有项目
  status <项目>      - 查看项目状态
  switch <项目>      - 切换到指定项目
  current            - 显示当前项目
  create <名称>      - 创建新项目
  delete <项目>      - 删除项目（需要确认）
  env <项目>         - 显示项目环境配置
  isolate            - 创建隔离环境脚本

示例:
  $0 list
  $0 status my-novel
  $0 switch my-novel
  $0 create new-story
EOF
}

# 列出所有项目
list_projects() {
    local projects_dir="${1:-$DEFAULT_PROJECTS_DIR}"
    
    if [[ ! -d "$projects_dir" ]]; then
        echo "项目目录不存在: $projects_dir"
        return 1
    fi
    
    echo "可用项目列表 ($projects_dir):"
    echo ""
    
    local count=0
    for project in "$projects_dir"/*/; do
        # 跳过备份目录和隐藏目录
        if [[ -d "$project" ]] && [[ "$(basename "$project")" != "backups" ]] && [[ ! "$(basename "$project")" =~ ^\. ]]; then
            local project_name=$(basename "$project")
            local state_file="$project/meta/workflow-state.json"
            local phase="未知"
            local current_chapter="0"
            
            if [[ -f "$state_file" ]]; then
                phase=$(grep -o '"currentPhase":[[:space:]]*[0-9]*' "$state_file" | grep -o '[0-9]*' || echo "0")
                current_chapter=$(grep -o '"currentChapter":[[:space:]]*[0-9]*' "$state_file" | grep -o '[0-9]*' || echo "0")
            fi
            
            echo "  $project_name"
            echo "    阶段: Phase $phase, 章节: $current_chapter"
            echo "    路径: $project"
            echo ""
            ((count++))
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo "  暂无项目"
    fi
}

# 查看项目状态
project_status() {
    local project_name="$1"
    local projects_dir="${2:-$DEFAULT_PROJECTS_DIR}"
    local project_dir="$projects_dir/$project_name"
    
    if [[ -z "$project_name" ]]; then
        echo "错误: 需要指定项目名称"
        return 1
    fi
    
    if [[ ! -d "$project_dir" ]]; then
        echo "错误: 项目不存在: $project_name"
        return 1
    fi
    
    echo "项目状态: $project_name"
    echo "路径: $project_dir"
    echo ""
    
    # 基本状态
    local state_file="$project_dir/meta/workflow-state.json"
    if [[ -f "$state_file" ]]; then
        echo "工作流状态:"
        grep -E '"currentPhase|"currentChapter|"resumeRequired|"architectureFinalized' "$state_file" | \
            sed 's/^[[:space:]]*//; s/"//g; s/,//'
        echo ""
    fi
    
    # 文件状态
    echo "关键文件:"
    local files=(
        "meta/project.md"
        "meta/config.md"
        "worldbuilding/world.md"
        "characters/protagonist.md"
        "outline/outline.md"
        "references/fixed-context.md"
    )
    
    for file in "${files[@]}"; do
        local full_path="$project_dir/$file"
        if [[ -f "$full_path" ]]; then
            local size=$(wc -l < "$full_path" 2>/dev/null || echo "0")
            local content_status="空"
            if [[ $size -gt 5 ]]; then
                content_status="已填写"
            elif [[ $size -gt 0 ]]; then
                content_status="部分填写"
            fi
            echo "  ✓ $file (${size}行, ${content_status})"
        else
            echo "  ✗ $file (缺失)"
        fi
    done
    
    # 章节状态
    echo ""
    echo "章节进度:"
    local chapters_dir="$project_dir/chapters"
    if [[ -d "$chapters_dir" ]]; then
        local chapter_count=$(find "$chapters_dir" -name "ch*.md" -type f | wc -l)
        echo "  已完成章节: $chapter_count"
        
        if [[ $chapter_count -gt 0 ]]; then
            echo "  最近章节:"
            find "$chapters_dir" -name "ch*.md" -type f | sort -V | tail -3 | while read -r chapter; do
                local ch_name=$(basename "$chapter")
                local ch_lines=$(wc -l < "$chapter" 2>/dev/null || echo "0")
                echo "    - $ch_name (${ch_lines}行)"
            done
        fi
    else
        echo "  暂无章节"
    fi
}

# 切换到项目
switch_project() {
    local project_name="$1"
    local projects_dir="${2:-$DEFAULT_PROJECTS_DIR}"
    local project_dir="$projects_dir/$project_name"
    
    if [[ -z "$project_name" ]]; then
        echo "错误: 需要指定项目名称"
        return 1
    fi
    
    if [[ ! -d "$project_dir" ]]; then
        echo "错误: 项目不存在: $project_name"
        return 1
    fi
    
    # 创建环境文件
    cat > "$PROJECT_ENV_FILE" << EOF
# novel-free 项目环境配置
# 生成时间: $(date)

NOVEL_FREE_PROJECT="$project_name"
NOVEL_FREE_PROJECT_DIR="$project_dir"
NOVEL_FREE_PROJECTS_DIR="$projects_dir"

# 快捷命令
alias novel-status="$0 status $project_name"
alias novel-backup="$SKILL_DIR/scripts/error-handler.sh backup $project_dir"
alias novel-resume="$SKILL_DIR/scripts/error-handler.sh resume $project_dir"

echo "已切换到项目: $project_name"
echo "项目路径: $project_dir"
echo ""
echo "可用快捷命令:"
echo "  novel-status    - 查看项目状态"
echo "  novel-backup    - 备份项目"
echo "  novel-resume    - 恢复项目"
echo "  $0 current     - 显示当前项目"
EOF
    
    echo "✅ 已切换到项目: $project_name"
    echo ""
    echo "要激活环境，请运行:"
    echo "  source $PROJECT_ENV_FILE"
    echo ""
    echo "或者直接使用:"
    echo "  $0 status $project_name"
}

# 显示当前项目
current_project() {
    if [[ -f "$PROJECT_ENV_FILE" ]]; then
        echo "当前项目环境:"
        grep -E "^NOVEL_FREE_PROJECT=" "$PROJECT_ENV_FILE" | cut -d= -f2
        echo ""
        echo "环境文件: $PROJECT_ENV_FILE"
        echo ""
        echo "要激活环境，请运行:"
        echo "  source $PROJECT_ENV_FILE"
    else
        echo "当前无活跃项目"
        echo ""
        echo "使用以下命令切换到项目:"
        echo "  $0 switch <项目名称>"
    fi
}

# 创建新项目（封装）
create_project() {
    local project_name="$1"
    
    if [[ -z "$project_name" ]]; then
        echo "错误: 需要指定项目名称"
        return 1
    fi
    
    echo "创建新项目: $project_name"
    echo ""
    
    # 使用我们之前创建的包装脚本
    if [[ -f "$SKILL_DIR/scripts/create-novel.sh" ]]; then
        "$SKILL_DIR/scripts/create-novel.sh" "$project_name"
        
        # 自动配置模型
        local project_dir="$DEFAULT_PROJECTS_DIR/$project_name"
        if [[ -d "$project_dir" ]]; then
            echo ""
            echo "自动配置模型..."
            "$SKILL_DIR/scripts/simple-auto-configure.sh" "$project_dir"
        fi
    else
        echo "错误: 未找到项目创建脚本"
        return 1
    fi
}

# 显示项目环境
show_env() {
    local project_name="$1"
    local projects_dir="${2:-$DEFAULT_PROJECTS_DIR}"
    local project_dir="$projects_dir/$project_name"
    
    if [[ -z "$project_name" ]]; then
        echo "错误: 需要指定项目名称"
        return 1
    fi
    
    if [[ ! -d "$project_dir" ]]; then
        echo "错误: 项目不存在: $project_name"
        return 1
    fi
    
    echo "项目环境: $project_name"
    echo "路径: $project_dir"
    echo ""
    
    # 显示配置
    local config_file="$project_dir/meta/config.md"
    if [[ -f "$config_file" ]]; then
        echo "模型配置:"
        grep -E "^[|].*模型.*[|]" "$config_file" | head -15
        echo ""
    fi
    
    # 显示关键配置
    echo "关键配置:"
    echo "  项目目录: $project_dir"
    echo "  技能目录: $SKILL_DIR"
    echo "  备份目录: $project_dir/../backups/"
}

# 创建隔离环境脚本
create_isolated_env() {
    local project_name="$1"
    local projects_dir="${2:-$DEFAULT_PROJECTS_DIR}"
    local project_dir="$projects_dir/$project_name"
    
    if [[ -z "$project_name" ]]; then
        echo "错误: 需要指定项目名称"
        return 1
    fi
    
    if [[ ! -d "$project_dir" ]]; then
        echo "错误: 项目不存在: $project_name"
        return 1
    fi
    
    local env_script="$project_dir/isolated-env.sh"
    
    cat > "$env_script" << EOF
#!/usr/bin/env bash
#
# novel-free 隔离环境脚本
# 项目: $project_name
#

# 设置环境变量
export NOVEL_FREE_PROJECT="$project_name"
export NOVEL_FREE_PROJECT_DIR="$project_dir"
export NOVEL_FREE_SKILL_DIR="$SKILL_DIR"

# 设置工作目录
cd "$project_dir"

echo "🐾 novel-free 隔离环境"
echo "项目: $project_name"
echo "目录: $project_dir"
echo ""

# 快捷命令
alias status="$0 status $project_name"
alias backup="$SKILL_DIR/scripts/error-handler.sh backup $project_dir"
alias resume="$SKILL_DIR/scripts/error-handler.sh resume $project_dir"
alias models="$SKILL_DIR/scripts/simple-auto-configure.sh $project_dir"

echo "可用命令:"
echo "  status  - 查看项目状态"
echo "  backup  - 备份项目"
echo "  resume  - 恢复项目"
echo "  models  - 重新配置模型"
echo ""
echo "当前目录已切换到项目根目录"
EOF
    
    chmod +x "$env_script"
    echo "✅ 创建隔离环境脚本: $env_script"
    echo ""
    echo "使用方法:"
    echo "  source $env_script"
    echo "  或"
    echo "  ./$env_script"
}

# 主函数
main() {
    local command="$1"
    local project_name="$2"
    
    case "$command" in
        "list"|"ls")
            list_projects "$3"
            ;;
        "status"|"stat")
            project_status "$project_name" "$3"
            ;;
        "switch"|"use")
            switch_project "$project_name" "$3"
            ;;
        "current"|"cur")
            current_project
            ;;
        "create"|"new")
            create_project "$project_name"
            ;;
        "env")
            show_env "$project_name" "$3"
            ;;
        "isolate")
            create_isolated_env "$project_name" "$3"
            ;;
        "help"|"-h"|"--help"|"")
            show_help
            ;;
        *)
            echo "错误: 未知命令: $command"
            show_help
            return 1
            ;;
    esac
}

main "$@"