#!/bin/bash

# 远程Git仓库提交记录摘要生成脚本
# 分析远程Git仓库并生成Markdown格式报告，保留报告文件

set -e

# 默认参数
REPO_URL=""
OUTPUT_FILE=""
NUM_COMMITS=20
ALL_BRANCHES=false
SHOW_HELP=false
KEEP_CLONE=false  # 是否保留克隆的仓库

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            REPO_URL="$2"
            shift 2
            ;;
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
        -k|--keep-clone)
            KEEP_CLONE=true
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
    echo "  -u, --url <url>         远程Git仓库URL（必需）"
    echo "  -o, --output <file>     指定输出文件（默认自动生成）"
    echo "  -n, --num-commits <n>   指定显示的最近提交数量（默认20）"
    echo "  -a, --all-branches      包含所有分支的统计"
    echo "  -k, --keep-clone        保留克隆的仓库目录（默认不保留）"
    echo "  -h, --help              显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -u https://gitee.com/user/repo.git"
    echo "  $0 -u https://github.com/user/repo.git -o report.md"
    echo "  $0 -u https://gitee.com/user/repo.git -k -n 30"
    exit 0
fi

# 检查必需参数
if [ -z "$REPO_URL" ]; then
    echo "错误：必须指定远程仓库URL（使用 -u 参数）"
    exit 1
fi

# 从URL提取项目名
extract_project_name_from_url() {
    local url="$1"
    local project_name
    
    # 移除.git后缀
    project_name=$(basename "$url" .git)
    
    # 清理特殊字符，只保留字母、数字、连字符和下划线
    project_name=$(echo "$project_name" | sed 's/[^a-zA-Z0-9_-]//g')
    
    echo "$project_name"
}

# 生成默认文件名
generate_default_filename() {
    local project_name=$(extract_project_name_from_url "$REPO_URL")
    local timestamp=$(date "+%Y%m%d-%H%M%S")
    echo "${project_name}-git-log-${timestamp}.md"
}

# 生成克隆目录名
generate_clone_dirname() {
    local project_name=$(extract_project_name_from_url "$REPO_URL")
    local timestamp=$(date "+%Y%m%d-%H%M%S")
    echo "clone-${project_name}-${timestamp}"
}

# 主函数
main() {
    echo "=== 远程Git仓库分析开始 ==="
    echo "仓库URL: $REPO_URL"
    
    # 生成克隆目录名
    CLONE_DIR=$(generate_clone_dirname)
    echo "克隆目录: $CLONE_DIR"
    
    # 如果没有指定输出文件，生成默认文件名
    if [ -z "$OUTPUT_FILE" ]; then
        OUTPUT_FILE=$(generate_default_filename)
        echo "输出文件: $OUTPUT_FILE (自动生成)"
    else
        echo "输出文件: $OUTPUT_FILE"
    fi
    
    # 克隆远程仓库
    echo "正在克隆仓库..."
    if ! git clone "$REPO_URL" "$CLONE_DIR" 2>/dev/null; then
        echo "错误：克隆仓库失败，请检查URL和网络连接"
        exit 1
    fi
    echo "克隆完成"
    
    # 进入克隆目录
    cd "$CLONE_DIR"
    
    # 使用本地分析脚本生成报告
    echo "正在生成分析报告..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # 构建参数
    PARAMS=""
    if [ -n "$OUTPUT_FILE" ]; then
        # 如果输出文件是相对路径，转换为绝对路径
        if [[ "$OUTPUT_FILE" != /* ]]; then
            OUTPUT_FILE="$(pwd)/../$OUTPUT_FILE"
        fi
        PARAMS="$PARAMS -o \"$OUTPUT_FILE\""
    fi
    
    if [ "$NUM_COMMITS" != "20" ]; then
        PARAMS="$PARAMS -n $NUM_COMMITS"
    fi
    
    if [ "$ALL_BRANCHES" = true ]; then
        PARAMS="$PARAMS -a"
    fi
    
    # 执行本地分析脚本
    eval "\"$SCRIPT_DIR/generate_git_summary.sh\" $PARAMS"
    
    # 返回上级目录
    cd ..
    
    # 处理克隆目录
    if [ "$KEEP_CLONE" = true ]; then
        echo "已保留克隆目录: $CLONE_DIR"
    else
        echo "正在清理克隆目录..."
        rm -rf "$CLONE_DIR"
        echo "克隆目录已清理"
    fi
    
    # 输出报告位置
    if [[ "$OUTPUT_FILE" == /* ]]; then
        REPORT_PATH="$OUTPUT_FILE"
    else
        REPORT_PATH="$(pwd)/$OUTPUT_FILE"
    fi
    
    echo ""
    echo "=== 分析完成 ==="
    echo "报告文件: $REPORT_PATH"
    
    if [ -f "$REPORT_PATH" ]; then
        echo "文件大小: $(wc -l < "$REPORT_PATH") 行"
        echo "生成时间: $(date)"
    else
        # 尝试在上级目录查找
        PARENT_REPORT_PATH="$(dirname "$(pwd)")/$OUTPUT_FILE"
        if [ -f "$PARENT_REPORT_PATH" ]; then
            echo "报告文件: $PARENT_REPORT_PATH"
            echo "文件大小: $(wc -l < "$PARENT_REPORT_PATH") 行"
            echo "生成时间: $(date)"
        else
            echo "警告：报告文件未找到，请检查输出路径"
        fi
    fi
}

# 运行主函数
main "$@"