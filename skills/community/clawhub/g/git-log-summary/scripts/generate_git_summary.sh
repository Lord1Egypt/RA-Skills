#!/bin/bash

# Git提交记录摘要生成脚本（Markdown格式）
# 按照固定格式输出git仓库的详细统计信息，生成Markdown文档

set -e

# 默认参数
OUTPUT_FILE=""
NUM_COMMITS=20
ALL_BRANCHES=false
SHOW_HELP=false

# 提交类型定义（使用兼容的数组格式）
COMMIT_TYPES_KEYS="feat fix merge docs style refactor test chore perf ci build revert"
COMMIT_TYPES_FEAT="新功能"
COMMIT_TYPES_FIX="Bug修复"
COMMIT_TYPES_MERGE="合并分支"
COMMIT_TYPES_DOCS="文档更新"
COMMIT_TYPES_STYLE="代码格式调整"
COMMIT_TYPES_REFACTOR="代码重构"
COMMIT_TYPES_TEST="测试相关"
COMMIT_TYPES_CHORE="构建过程或辅助工具变动"
COMMIT_TYPES_PERF="性能优化"
COMMIT_TYPES_CI="CI/CD相关"
COMMIT_TYPES_BUILD="构建系统"
COMMIT_TYPES_REVERT="回退提交"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -n|--num-commits)
            NUM_COMMITS="$2"
            shift 2
            ;;
        -a|--all-branches)
            ALL_BRANCHES=true
            shift
            ;;
        -h|--help)
            SHOW_HELP=true
            shift
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 显示帮助信息
if [ "$SHOW_HELP" = true ]; then
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -o, --output <file>     指定输出文件（默认输出到控制台）"
    echo "  -n, --num-commits <n>   指定显示的最近提交数量（默认20）"
    echo "  -a, --all-branches      包含所有分支的统计"
    echo "  -h, --help              显示此帮助信息"
    exit 0
fi

# 检查是否在git仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "错误：当前目录不是git仓库"
    exit 1
fi

# 输出函数
output() {
    if [ -n "$OUTPUT_FILE" ]; then
        echo "$1" >> "$OUTPUT_FILE"
    else
        echo "$1"
    fi
}

# 获取项目名称
get_project_name() {
    local project_name
    
    # 尝试从remote获取项目名
    if git remote -v | grep -q origin; then
        project_name=$(git remote get-url origin 2>/dev/null || git config --get remote.origin.url)
        project_name=$(basename "$project_name" .git)
    else
        # 使用目录名作为项目名
        project_name=$(basename "$(pwd)")
    fi
    
    echo "$project_name"
}

# 获取仓库基本信息
get_repo_info() {
    local repo_path=$(pwd)
    local git_version=$(git --version | cut -d' ' -f3)
    local total_commits=$(git rev-list --count HEAD)
    
    echo "- **Git版本**: $git_version"
    echo "- **仓库创建时间**: $(git log --reverse --pretty=format:"%ad" --date=short | head -1)"
    echo "- **最后提交时间**: $(git log -1 --pretty=format:"%ad" --date=short)"
}

# 获取当前分支信息
get_current_branch() {
    git branch --show-current
}

# 获取远程仓库信息
get_remote_info() {
    if git remote -v | grep -q .; then
        git remote -v | while read line; do
            echo "- $line"
        done
    else
        echo "- 未配置远程仓库"
    fi
}

# 获取所有分支
get_all_branches() {
    echo "### 本地分支"
    echo ""
    git branch --format="  - %(refname:short)" | sed 's/^\* //'
    
    echo ""
    echo "### 远程分支"
    echo ""
    git branch -r --format="  - %(refname:short)" | sed 's/^origin\///'
}

# 获取提交统计
get_commit_stats() {
    local total_commits
    
    if [ "$ALL_BRANCHES" = true ]; then
        total_commits=$(git rev-list --all --count)
    else
        total_commits=$(git rev-list --count HEAD)
    fi
    
    echo "$total_commits"
}

# 获取作者统计（Markdown表格格式）
get_author_stats() {
    local stats
    local total_commits=$(get_commit_stats)
    
    if [ "$total_commits" -eq 0 ]; then
        echo "| 作者 | 提交次数 | 占比 |"
        echo "|------|----------|------|"
        return
    fi
    
    if [ "$ALL_BRANCHES" = true ]; then
        stats=$(git shortlog -sn --all 2>/dev/null || echo "")
    else
        stats=$(git shortlog -sn 2>/dev/null || echo "")
    fi
    
    # 输出Markdown表格
    echo "| 作者 | 提交次数 | 占比 |"
    echo "|------|----------|------|"
    
    if [ -n "$stats" ]; then
        echo "$stats" | while read count author; do
            if [ -n "$count" ] && [ -n "$author" ]; then
                percentage=$(echo "scale=2; $count * 100 / $total_commits" | bc 2>/dev/null || echo "0.00")
                printf "| %s | %s | %.2f%% |\n" "$author" "$count" "$percentage"
            fi
        done
    else
        # 如果没有shortlog输出，尝试从git log获取
        git log --pretty=format:"%an" | sort | uniq -c | sort -nr | while read count author; do
            percentage=$(echo "scale=2; $count * 100 / $total_commits" | bc 2>/dev/null || echo "0.00")
            printf "| %s | %s | %.2f%% |\n" "$author" "$count" "$percentage"
        done
    fi
}

# 获取最近提交记录（Markdown表格格式）
get_recent_commits() {
    local format="%h | %an | %ar | %s"
    
    echo "| Commit Hash | 作者 | 提交时间 | 提交日志 |"
    echo "|-------------|------|----------|----------|"
    
    if [ "$ALL_BRANCHES" = true ]; then
        git log --all --pretty=format:"| %h | %an | %ar | %s |" -n "$NUM_COMMITS"
    else
        git log --pretty=format:"| %h | %an | %ar | %s |" -n "$NUM_COMMITS"
    fi
}

# 分析提交类型（Markdown表格格式）
analyze_commit_types() {
    local total_commits=$(get_commit_stats)
    
    # 初始化类型计数器
    type_counts_feat=0
    type_counts_fix=0
    type_counts_merge=0
    type_counts_docs=0
    type_counts_style=0
    type_counts_refactor=0
    type_counts_test=0
    type_counts_chore=0
    type_counts_perf=0
    type_counts_ci=0
    type_counts_build=0
    type_counts_revert=0
    type_counts_other=0
    
    # 获取提交信息并统计
    local commits
    if [ "$ALL_BRANCHES" = true ]; then
        commits=$(git log --all --pretty=format:"%s" | head -1000)
    else
        commits=$(git log --pretty=format:"%s" | head -1000)
    fi
    
    # 统计提交类型
    while IFS= read -r commit_msg; do
        local found=false
        
        # 检查是否有类型前缀（如 "feat: " 或 "feat("）
        if [[ "$commit_msg" =~ ^feat[:\(] ]]; then
            ((type_counts_feat++))
            found=true
        elif [[ "$commit_msg" =~ ^fix[:\(] ]]; then
            ((type_counts_fix++))
            found=true
        elif [[ "$commit_msg" =~ ^merge[:\(] ]] || [[ "$commit_msg" =~ ^Merge ]]; then
            ((type_counts_merge++))
            found=true
        elif [[ "$commit_msg" =~ ^docs[:\(] ]]; then
            ((type_counts_docs++))
            found=true
        elif [[ "$commit_msg" =~ ^style[:\(] ]]; then
            ((type_counts_style++))
            found=true
        elif [[ "$commit_msg" =~ ^refactor[:\(] ]]; then
            ((type_counts_refactor++))
            found=true
        elif [[ "$commit_msg" =~ ^test[:\(] ]]; then
            ((type_counts_test++))
            found=true
        elif [[ "$commit_msg" =~ ^chore[:\(] ]]; then
            ((type_counts_chore++))
            found=true
        elif [[ "$commit_msg" =~ ^perf[:\(] ]]; then
            ((type_counts_perf++))
            found=true
        elif [[ "$commit_msg" =~ ^ci[:\(] ]]; then
            ((type_counts_ci++))
            found=true
        elif [[ "$commit_msg" =~ ^build[:\(] ]]; then
            ((type_counts_build++))
            found=true
        elif [[ "$commit_msg" =~ ^revert[:\(] ]]; then
            ((type_counts_revert++))
            found=true
        fi
        
        if [ "$found" = false ]; then
            ((type_counts_other++))
        fi
    done <<< "$commits"
    
    local total_analyzed=$(echo "$commits" | wc -l)
    
    # 输出Markdown表格
    echo "| 类型 | 数量 | 占比 | 说明 |"
    echo "|------|------|------|------|"
    
    # 输出每种类型的统计
    if [ $type_counts_feat -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_feat * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "feat" "$type_counts_feat" "$percentage" "$COMMIT_TYPES_FEAT"
    fi
    
    if [ $type_counts_fix -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_fix * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "fix" "$type_counts_fix" "$percentage" "$COMMIT_TYPES_FIX"
    fi
    
    if [ $type_counts_merge -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_merge * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "merge" "$type_counts_merge" "$percentage" "$COMMIT_TYPES_MERGE"
    fi
    
    if [ $type_counts_docs -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_docs * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "docs" "$type_counts_docs" "$percentage" "$COMMIT_TYPES_DOCS"
    fi
    
    if [ $type_counts_style -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_style * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "style" "$type_counts_style" "$percentage" "$COMMIT_TYPES_STYLE"
    fi
    
    if [ $type_counts_refactor -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_refactor * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "refactor" "$type_counts_refactor" "$percentage" "$COMMIT_TYPES_REFACTOR"
    fi
    
    if [ $type_counts_test -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_test * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "test" "$type_counts_test" "$percentage" "$COMMIT_TYPES_TEST"
    fi
    
    if [ $type_counts_chore -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_chore * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "chore" "$type_counts_chore" "$percentage" "$COMMIT_TYPES_CHORE"
    fi
    
    if [ $type_counts_perf -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_perf * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "perf" "$type_counts_perf" "$percentage" "$COMMIT_TYPES_PERF"
    fi
    
    if [ $type_counts_ci -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_ci * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "ci" "$type_counts_ci" "$percentage" "$COMMIT_TYPES_CI"
    fi
    
    if [ $type_counts_build -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_build * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "build" "$type_counts_build" "$percentage" "$COMMIT_TYPES_BUILD"
    fi
    
    if [ $type_counts_revert -gt 0 ]; then
        local percentage=$(echo "scale=2; $type_counts_revert * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "revert" "$type_counts_revert" "$percentage" "$COMMIT_TYPES_REVERT"
    fi
    
    # 其他类型
    if [ $type_counts_other -gt 0 ]; then
        local other_percentage=$(echo "scale=2; $type_counts_other * 100 / $total_analyzed" | bc)
        printf "| %s | %s | %.1f%% | %s |\n" "other" "$type_counts_other" "$other_percentage" "其他提交"
    fi
}

# 生成Markdown格式报告
generate_markdown_report() {
    local project_name=$(get_project_name)
    local current_time=$(date "+%Y-%m-%d %H:%M:%S")
    local repo_path=$(pwd)
    
    # 报告标题
    output "# $project_name Git提交记录摘要"
    output ""
    output "## 报告信息"
    output ""
    output "- **生成时间**: $current_time"
    output "- **仓库路径**: \`$repo_path\`"
    output "- **仓库基本信息**:"
    output ""
    get_repo_info | while read line; do output "  $line"; done
    output ""
    
    # 分支信息
    output "## 分支信息"
    output ""
    output "### 当前分支"
    output ""
    output "\`$(get_current_branch)\`"
    output ""
    output "### 远程仓库"
    output ""
    get_remote_info | while read line; do output "$line"; done
    output ""
    
    # 提交统计
    output "## 提交统计"
    output ""
    output "### 总提交数"
    output ""
    output "**总提交数**: $(get_commit_stats)"
    output ""
    output "### 按作者统计"
    output ""
    get_author_stats | while read line; do output "$line"; done
    output ""
    
    # 最近提交记录
    output "## 最近提交记录"
    output ""
    output "显示最近 $NUM_COMMITS 条提交记录："
    output ""
    get_recent_commits | while read line; do output "$line"; done
    output ""
    
    # 分支信息
    output "## 所有分支"
    output ""
    get_all_branches | while read line; do output "$line"; done
    output ""
    
    # 提交类型统计
    output "## 提交类型统计"
    output ""
    output "基于最近1000条提交信息的类型分析："
    output ""
    analyze_commit_types | while read line; do output "$line"; done
    output ""
    
    output "---"
    output "*报告生成完成*"
}

# 获取项目名称（用于文件名）
get_project_name_for_file() {
    local project_name
    
    # 尝试从remote获取项目名
    if git remote -v | grep -q origin; then
        project_name=$(git remote get-url origin 2>/dev/null || git config --get remote.origin.url)
        project_name=$(basename "$project_name" .git)
    else
        # 使用目录名作为项目名
        project_name=$(basename "$(pwd)")
    fi
    
    # 清理项目名中的特殊字符，只保留字母、数字、连字符和下划线
    project_name=$(echo "$project_name" | sed 's/[^a-zA-Z0-9_-]//g')
    
    echo "$project_name"
}

# 生成默认文件名
generate_default_filename() {
    local project_name=$(get_project_name_for_file)
    local timestamp=$(date "+%Y%m%d-%H%M%S")
    echo "${project_name}-git-log-${timestamp}.md"
}

# 主函数
main() {
    # 如果没有指定输出文件，生成默认文件名
    if [ -z "$OUTPUT_FILE" ]; then
        OUTPUT_FILE=$(generate_default_filename)
        echo "未指定输出文件，使用默认文件名: $OUTPUT_FILE"
    fi
    
    # 清空输出文件
    > "$OUTPUT_FILE"
    echo "Markdown报告将保存到: $OUTPUT_FILE"
    
    # 生成报告
    generate_markdown_report
    
    echo "Markdown报告生成完成！"
    echo "文件位置: $OUTPUT_FILE"
}

# 运行主函数
main "$@"
