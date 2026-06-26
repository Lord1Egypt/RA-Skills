#!/bin/bash

# github-review.sh - GitHub PR 行级审查工具
#
# 功能：
# 1. 下载 PR 代码
# 2. 本地代码审查
# 3. 行级评论生成
# 4. 提交审查意见
#
# 用法：
#   ./github-review.sh download <pr-number>   # 下载 PR 代码
#   ./github-review.sh review <pr-number>     # 审查 PR
#   ./github-review.sh comment <pr-number>    # 添加审查评论
#   ./github-review.sh approve <pr-number>    # 批准 PR
#   ./github-review.sh help                   # 显示帮助

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# PR 下载目录
PR_DOWNLOAD_DIR="$HOME/.config/github-pr-download"

# 显示帮助信息
show_help() {
    cat << EOF
GitHub PR 行级审查工具

用法：
  github-review.sh [command] <pr-number> [options]

命令:
  download <pr-number>   下载 PR 代码到本地目录
  review <pr-number>     审查 PR 并生成审查意见
  comment <pr-number>    添加审查评论
  approve <pr-number>    批准 PR
  decline <pr-number>    驳回 PR
  help, --help, -h       显示此帮助信息

选项:
  -r, --repo        GitHub 仓库 (owner/repo)
  -o, --output      下载目录（默认：~/github-pr-download）
  -l, --lines       审查行数限制
  -f, --file        审查特定文件
  -v, --verbose     显示详细信息

审查类型:
  -s, --style       代码风格审查
  -b, --bug         Bug 修复审查
  -p, --performance 性能审查
  -a, --security    安全审查
  -c, --complexity  复杂度审查

示例:
  github-review.sh download 123
  github-review.sh review 123 --style --bug
  github-review.sh comment 123 -m "LGTM, nice work!"

前提条件：
  1. 本地已配置 GitHub 仓库
  2. 已安装 gh CLI: brew install gh
  3. 已认证: gh auth login

EOF
    exit 0
}

# 检查 gh CLI
check_gh() {
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ 错误：gh CLI 未安装${NC}"
        echo ""
        echo -e "${BLUE}安装方法:${NC}"
        echo "   brew install gh"
        echo ""
        echo "然后运行：gh auth login"
        exit 1
    fi
}

# 检查 git 状态
check_git() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}❌ 错误：当前目录不是 Git 仓库${NC}"
        exit 1
    fi
    
    if ! git remote get-url origin > /dev/null 2>&1; then
        echo -e "${RED}❌ 错误：未配置远程仓库${NC}"
        exit 1
    fi
}

# 获取当前仓库信息
get_repo_info() {
    local remote_url=$(git remote get-url origin 2>/dev/null)
    local repo="${1:-}"
    
    if [[ -n "$repo" ]]; then
        REPO_SLUG="$repo"
        REPO_OWNER=$(echo "$repo" | cut -d'/' -f1)
        REPO_NAME=$(echo "$repo" | cut -d'/' -f2)
    else
        if [[ "$remote_url" =~ ^git@github\.com:([^/]+)/(.+)\.git$ ]] || \
           [[ "$remote_url" =~ ^https://github\.com/([^/]+)/(.+)\.git$ ]]; then
            REPO_OWNER="${BASH_REMATCH[1]}"
            REPO_NAME="${BASH_REMATCH[2]}"
            REPO_SLUG="${REPO_OWNER}/${REPO_NAME}"
        else
            echo -e "${RED}❌ 无法解析远程仓库 URL${NC}"
            exit 1
        fi
    fi
}

# 初始化下载目录
init_download_dir() {
    local output_dir="${1:-$PR_DOWNLOAD_DIR}"
    mkdir -p "$output_dir"
    echo "$output_dir"
}

# 下载 PR 代码
download_pr() {
    local pr_number="$1"
    local output_dir="${2:-$PR_DOWNLOAD_DIR}"
    local repo="$3"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  📥 下载 PR 代码                                 ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    output_dir=$(init_download_dir "$output_dir")
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo -e "${CYAN}下载目录：${output_dir}${NC}"
    echo ""
    
    # 创建 PR 目录
    local pr_dir="$output_dir/pr-${pr_number}"
    mkdir -p "$pr_dir"
    
    # 获取 PR 信息
    echo -e "${CYAN}获取 PR 信息...${NC}"
    local pr_info=$(gh pr view "$pr_number" --json title,author,state,mergeable,headRefName,baseRefName,files,additions,deletions,reviewRequests,comments,author,createdAt,mergedAt,closedAt,reviewDecision,statusCheckRollup,mergeStateStatus,latestReviews,wasRebased,isInMergeQueue,isMergeable,latestReview,headRepository,baseRepository 2>/dev/null)
    
    if [[ -z "$pr_info" ]]; then
        echo -e "${RED}❌ 无法获取 PR 信息${NC}"
        exit 1
    fi
    
    local title=$(echo "$pr_info" | grep -o '"title": *"[^"]*"' | cut -d'"' -f4)
    local author=$(echo "$pr_info" | grep -o '"author": *{[^}]*}' | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)
    local state=$(echo "$pr_info" | grep -o '"state": *"[^"]*"' | cut -d'"' -f4)
    local additions=$(echo "$pr_info" | grep -o '"additions": *[0-9]*' | grep -o '[0-9]*')
    local deletions=$(echo "$pr_info" | grep -o '"deletions": *[0-9]*' | grep -o '[0-9]*')
    
    echo -e "${YELLOW}标题：${title}${NC}"
    echo -e "${CYAN}作者：${author}${NC}"
    echo -e "${YELLOW}状态：${state}${NC}"
    echo -e "${CYAN}新增：${additions} 行，删除：${deletions} 行${NC}"
    echo ""
    
    # 保存 PR 信息
    echo "$pr_info" > "$pr_dir/pr-info.json"
    
    # 下载代码
    echo -e "${CYAN}下载 PR 代码...${NC}"
    gh pr checkout "$pr_number" -C "$pr_dir" 2>/dev/null || {
        echo -e "${YELLOW}⚠️  PR 已关闭，正在下载快照...${NC}"
        gh pr diff "$pr_number" > "$pr_dir/changes.diff" 2>/dev/null || true
    }
    
    # 获取文件列表
    echo -e "${CYAN}获取文件列表...${NC}"
    gh pr diff "$pr_number" > "$pr_dir/changes.diff" 2>/dev/null || true
    
    local files=$(gh pr view "$pr_number" --json files --jq '.files[].path' 2>/dev/null)
    
    if [[ -n "$files" ]]; then
        echo "文件列表已保存到：$pr_dir/files.txt"
        echo "$files" > "$pr_dir/files.txt"
    fi
    
    echo ""
    echo -e "${GREEN}✅ PR 代码已下载到：${pr_dir}${NC}"
    echo ""
    echo -e "${BLUE}文件列表：${NC}"
    if [[ -f "$pr_dir/files.txt" ]]; then
        cat "$pr_dir/files.txt"
    fi
    echo ""
    echo -e "${BLUE}操作步骤：${NC}"
    echo "   cd $pr_dir"
    echo "   # 进行代码审查"
    echo "   # 编辑任选文件后运行：github-review.sh review $pr_number"
}

# 审查 PR
review_pr() {
    local pr_number="$1"
    local repo="$2"
    local review_types="${3:-}"
    local verbose="${4:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  👀 审查 PR                                     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo -e "${CYAN}审核类型：${review_types:-全部}${NC}"
    echo ""
    
    # 获取 PR 详情
    local pr_info=$(gh pr view "$pr_number" --json title,author,reviewDecision,number,state,additions,deletions,body 2>/dev/null)
    
    if [[ -z "$pr_info" ]]; then
        echo -e "${RED}❌ 无法获取 PR 信息${NC}"
        exit 1
    fi
    
    local title=$(echo "$pr_info" | grep -o '"title": *"[^"]*"' | cut -d'"' -f4)
    local author=$(echo "$pr_info" | grep -o '"author": *{[^}]*}' | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)
    local review_decision=$(echo "$pr_info" | grep -o '"reviewDecision": *"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${YELLOW}标题：${title}${NC}"
    echo -e "${CYAN}作者：${author}${NC}"
    echo -e "${YELLOW}审核状态：${review_decision}${NC}"
    echo ""
    
    # 获取变更内容
    echo -e "${CYAN}获取变更内容...${NC}"
    local diff=$(gh pr diff "$pr_number" 2>/dev/null)
    
    # 分析代码
    echo -e "${CYAN}分析代码变更...${NC}"
    
    # 添加/删除统计
    local additions=$(echo "$pr_info" | grep -o '"additions": *[0-9]*' | grep -o '[0-9]*')
    local deletions=$(echo "$pr_info" | grep -o '"deletions": *[0-9]*' | grep -o '[0-9]*')
    
    echo -e "${BLUE}变更统计：${NC}"
    echo -e "   新增：${GREEN}+${additions}${NC} 行"
    echo -e "   删除：${RED}-${deletions}${NC} 行"
    echo -e "   净变化：${CYAN}$((additions - deletions))${NC} 行"
    echo ""
    
    # 生成审查报告
    local review_report="$HOME/.config/github-pr-review/review-${pr_number}.md"
    mkdir -p "$(dirname "$review_report")"
    
    cat > "$review_report" << EOF
# PR #${pr_number} 审查报告

**PR 标题**: ${title}
**作者**: ${author}
**审核状态**: ${review_decision}
**审查时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 变更概览

- **新增代码**: ${additions} 行
- **删除代码**: ${deletions} 行
- **净变化**: $((additions - deletions)) 行

## 审查结果

### 代码质量评估

\`\`\`json
{
  "review_decision": "${review_decision}",
  "files_changed": [],
  "comments": []
}
\`\`\`

### 建议

1. 检查是否有潜在的 Bug
2. 确认代码符合项目规范
3. 验证测试覆盖
4. 确认性能影响可接受

### 详细审查

TODO: 请在此处添加详细审查意见

---

*此报告由 github-review.sh 生成*
EOF

    echo -e "${GREEN}✅ 审查报告已生成：${review_report}${NC}"
    echo ""
    echo -e "${BLUE}审查步骤：${NC}"
    echo "   1. 查看审查报告：cat $review_report"
    echo "   2. 编辑审查意见：vim $review_report"
    echo "   3. 添加评论：github-review.sh comment $pr_number -m \"审查意见\""
    echo "   4. 批准或驳回：github-review.sh approve $pr_number"
}

# 添加评论
add_comment() {
    local pr_number="$1"
    local message="${2:-}"
    local repo="${3:-}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  💬 添加 PR 评论                                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo ""
    
    # 获取评论
    if [[ -z "$message" ]]; then
        echo -e "${YELLOW}输入评论内容（Ctrl+D 结束）：${NC}"
        message=$(cat)
    fi
    
    # 添加评论
    if gh pr comment "$pr_number" --body "$message"; then
        echo ""
        echo -e "${GREEN}✅ 评论已添加${NC}"
    else
        echo -e "${RED}❌ 评论添加失败${NC}"
        exit 1
    fi
}

# 批准 PR
approve_pr() {
    local pr_number="$1"
    local repo="${2:-}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ✅ 批准 PR                                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    get_repo_info "$repo"
    
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo ""
    
    # 获取 PR 信息
    local pr_info=$(gh pr view "$pr_number" --json title,author,reviewDecision 2>/dev/null)
    local title=$(echo "$pr_info" | grep -o '"title": *"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${YELLOW}标题：${title}${NC}"
    echo ""
    
    # 批准 PR
    if gh pr review "$pr_number" --comment --body "LGTM! 👍"; then
        echo -e "${GREEN}✅ PR 已批准${NC}"
    else
        echo -e "${RED}❌ 批准失败${NC}"
        exit 1
    fi
}

# 驳回 PR
decline_pr() {
    local pr_number="$1"
    local message="${2:-}"
    local repo="${3:-}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ❌ 驳回 PR                                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    get_repo_info "$repo"
    
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo ""
    
    # 获取 PR 信息
    local pr_info=$(gh pr view "$pr_number" --json title,author 2>/dev/null)
    local title=$(echo "$pr_info" | grep -o '"title": *"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${YELLOW}标题：${title}${NC}"
    echo ""
    
    # 请求修改
    if [[ -z "$message" ]]; then
        message="请修改以下问题后再提交"
    fi
    
    if gh pr review "$pr_number" --request-changes --body "$message"; then
        echo -e "${GREEN}✅ PR 已请求修改${NC}"
    else
        echo -e "${RED}❌ 请求修改失败${NC}"
        exit 1
    fi
}

# 主函数
main() {
    check_gh
    check_git
    
    local command="${1:-help}"
    shift || true
    
    local pr_number="$1"
    shift || true
    
    local repo=""
    local output_dir=""
    local review_types=""
    local verbose="false"
    local message=""
    
    # 解析选项
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -r|--repo)
                repo="$2"
                shift 2
                ;;
            -o|--output)
                output_dir="$2"
                shift 2
                ;;
            -l|--lines)
                SHIFT_LINES="$2"
                shift 2
                ;;
            -f|--file)
                FILE_PATTERN="$2"
                shift 2
                ;;
            -s|--style)
                review_types+="style "
                shift
                ;;
            -b|--bug)
                review_types+="bug "
                shift
                ;;
            -p|--performance)
                review_types+="performance "
                shift
                ;;
            -a|--security)
                review_types+="security "
                shift
                ;;
            -c|--complexity)
                review_types+="complexity "
                shift
                ;;
            -m|--message)
                message="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose="true"
                shift
                ;;
            -y|--yes)
                NO_PROMPT="true"
                shift
                ;;
            --)
                shift
                break
                ;;
            *)
                break
                ;;
        esac
    done
    
    # 如果没有提供命令，显示帮助
    if [[ "$command" == "help" ]] || [[ "$command" == "--help" ]] || [[ "$command" == "-h" ]]; then
        show_help
    fi
    
    # 必须提供 PR 编号
    if [[ -z "$pr_number" ]]; then
        echo -e "${RED}❌ 错误：必须提供 PR 编号${NC}"
        echo ""
        echo -e "${BLUE}用法：${NC}"
        echo "   github-review.sh [command] <pr-number> [options]"
        echo ""
        show_help
    fi
    
    case "$command" in
        download)
            download_pr "$pr_number" "$output_dir" "$repo"
            ;;
        review)
            review_pr "$pr_number" "$repo" "$review_types" "$verbose"
            ;;
        comment)
            add_comment "$pr_number" "$message" "$repo"
            ;;
        approve)
            approve_pr "$pr_number" "$repo"
            ;;
        decline)
            decline_pr "$pr_number" "$message" "$repo"
            ;;
        *)
            echo -e "${RED}❌ 未知命令：${command}${NC}"
            echo ""
            show_help
            ;;
    esac
}

main "$@"
