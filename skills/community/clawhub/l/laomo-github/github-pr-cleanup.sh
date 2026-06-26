#!/bin/bash

# github-pr-cleanup.sh - GitHub PR 自动清理工具
#
# 功能：
# 1. 清理已合并的 PR 分支
# 2. 删除过期的临时分支
# 3. 合并冲突的 PR
# 4. 管理 PR 状态
#
# 用法：
#   ./github-pr-cleanup.sh merged         # 清理已合并的 PR
#   ./github-pr-cleanup.sh old            # 删除过期分支
#   ./github-pr-cleanup.sh conflicts      # 处理冲突的 PR
#   ./github-pr-cleanup.sh stale          # 标记陈旧 PR
#   ./github-pr-cleanup.sh help           # 显示帮助

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
MAX_DAYS_OLD=30  # 分支过期天数
FETCH_LIMIT=100  # 获取 PR 数量限制

# 显示帮助信息
show_help() {
    cat << EOF
GitHub PR 自动清理工具

用法：
  github-pr-cleanup.sh [command] [options]

命令:
  merged        清理已合并且已关闭的 PR 分支
  old           删除超过指定天数的陈旧分支
  conflicts     处理存在冲突的 PR
  stale         标记长期未更新的 PR（陈旧）
  help, --help, -h  显示此帮助信息

选项:
  -r, --repo        GitHub 仓库 (owner/repo)
  -d, --days        过期天数（默认：30）
  -l, --limit       获取 PR 数量限制（默认：100）
  -y, --yes         自动确认所有操作
  -n, --dry-run     仅显示将要执行的操作
  -v, --verbose     显示详细信息

示例:
  github-pr-cleanup.sh merged
  github-pr-cleanup.sh old --days 14
  github-pr-cleanup.sh stale --repo owner/repo

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
    
    # 检查是否有远程仓库
    if ! git remote get-url origin > /dev/null 2>&1; then
        echo -e "${RED}❌ 错误：未配置远程仓库${NC}"
        echo ""
        echo -e "${BLUE}添加远程：${NC}"
        echo "   git remote add origin https://github.com/USER/REPO.git"
        exit 1
    fi
    
    # 更新远程引用
    git fetch --prune 2>/dev/null || true
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
        # 解析仓库信息
        if [[ "$remote_url" =~ ^git@github\.com:([^/]+)/(.+)\.git$ ]] || \
           [[ "$remote_url" =~ ^https://github\.com/([^/]+)/(.+)\.git$ ]]; then
            REPO_OWNER="${BASH_REMATCH[1]}"
            REPO_NAME="${BASH_REMATCH[2]}"
            REPO_SLUG="${REPO_OWNER}/${REPO_NAME}"
        else
            echo -e "${RED}❌ 无法解析远程仓库 URL${NC}"
            echo "   $remote_url"
            exit 1
        fi
    fi
}

# 清理已合并的 PR
cleanup_merged() {
    local repo="$1"
    local dry_run="${2:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🗑️  清理已合并的 PR 分支                         ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${CYAN}获取已合并的 PR...${NC}"
    echo ""
    
    # 获取已合并的 PR（关闭且已合并）
    local pr_list=$(gh pr list \
        --repo "$REPO_SLUG" \
        --state closed \
        --merged \
        --limit "${FETCH_LIMIT}" \
        --json number,title,headRefName,mergedAt \
        --jq '.[] | select(.headRefName != null)' \
        2>/dev/null)
    
    if [[ -z "$pr_list" ]]; then
        echo -e "${GREEN}✅ 未找到已合并的 PR${NC}"
        return
    fi
    
    echo -e "${YELLOW}找到 ${pr_list | jq length} 个已合并的 PR${NC}"
    echo ""
    
    # 统计
    local total=0
    local cleaned=0
    local failed=0
    
    echo "$pr_list" | jq -c '.[]' | while read -r pr; do
        local pr_number=$(echo "$pr" | jq -r '.number')
        local title=$(echo "$pr" | jq -r '.title')
        local branch=$(echo "$pr" | jq -r '.headRefName')
        local merged_at=$(echo "$pr" | jq -r '.mergedAt')
        
        ((total++))
        
        echo -e "${CYAN}PR #${pr_number}: ${title}${NC}"
        echo -e "   分支：${branch}"
        echo -e "   合并时间：${merged_at}"
        
        if [[ "$dry_run" == "true" ]]; then
            echo -e "${YELLOW}[tid_run] 将删除分支：${branch}${NC}"
        else
            # 删除远程分支
            if git push origin --delete "$branch" 2>/dev/null; then
                echo -e "${GREEN}✨ 已删除分支：${branch}${NC}"
                ((cleaned++))
            else
                echo -e "${RED}❌ 删除失败：${branch}${NC}"
                ((failed++))
            fi
        fi
        echo ""
    done
    
    if [[ "$dry_run" != "true" ]]; then
        echo ""
        echo -e "${BLUE}统计：${NC}"
        echo -e "   总计：${total}"
        echo -e "   已清理：${cleaned}"
        echo -e "   失败：${failed}"
    fi
}

# 清理陈旧的分支
cleanup_old() {
    local repo="$1"
    local days="${2:-$MAX_DAYS_OLD}"
    local dry_run="${3:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🧹 清理陈旧的分支                               ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${CYAN}陈旧天数：${days} 天${NC}"
    echo ""
    
    # 获取所有远程分支
    echo -e "${YELLOW}获取远程分支...${NC}"
    echo ""
    
    local branches=$(git branch -r --format='%(refname:short)')
    local cutoff_date=$(date -d "-${days} days" +%s 2>/dev/null || date -v-"${days}d" +%s)
    
    local count=0
    local cleaned=0
    local failed=0
    
    for branch in $branches; do
        # 跳过 main 和 master
        if [[ "$branch" == "origin/main" ]] || [[ "$branch" == "origin/master" ]]; then
            continue
        fi
        
        # 跳过已经本地删除的分支
        local local_branch="${branch#origin/}"
        if git show-ref --verify --quiet "refs/heads/$local_branch" 2>/dev/null; then
            continue
        fi
        
        ((count++))
        
        # 获取分支最后更新时间
        local last_commit=$(git log -1 --format=%ct "origin/$local_branch" 2>/dev/null || echo "0")
        
        if [[ $last_commit -lt $cutoff_date ]]; then
            echo -e "${YELLOW}陈旧分支（最后提交：$(date -d @${last_commit} '+%Y-%m-%d')）${NC}"
            echo -e "   ${branch}"
            
            if [[ "$dry_run" == "true" ]]; then
                echo -e "${YELLOW}[dry_run] 将删除分支：${branch}${NC}"
                ((cleaned++))
            else
                if git push origin --delete "$local_branch" 2>/dev/null; then
                    echo -e "${GREEN}✨ 已删除：${branch}${NC}"
                    ((cleaned++))
                else
                    echo -e "${RED}❌ 删除失败：${branch}${NC}"
                    ((failed++))
                fi
            fi
            echo ""
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo -e "${YELLOW}未找到分支${NC}"
    else
        echo ""
        echo -e "${BLUE}统计：${NC}"
        echo -e "   总计分支：${count}"
        echo -e "   陈旧分支：${cleaned}"
        if [[ "$dry_run" != "true" ]]; then
            echo -e "   失败：${failed}"
        fi
    fi
}

# 处理冲突的 PR
handle_conflicts() {
    local repo="$1"
    local dry_run="${2:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🆘 处理冲突的 PR                                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo ""
    
    # 获取有冲突的 PR
    echo -e "${YELLOW}获取冲突的 PR...${NC}"
    echo ""
    
    local pr_list=$(gh pr list \
        --repo "$REPO_SLUG" \
        --state open \
        --json number,title,state,mergeable,headRefName \
        --jq '.[] | select(.mergeable == "CONFLICTING")' \
        2>/dev/null)
    
    if [[ -z "$pr_list" ]]; then
        echo -e "${GREEN}✅ 未找到冲突的 PR${NC}"
        return
    fi
    
    echo "$pr_list" | jq -c '.[]' | while read -r pr; do
        local pr_number=$(echo "$pr" | jq -r '.number')
        local title=$(echo "$pr" | jq -r '.title')
        local branch=$(echo "$pr" | jq -r '.headRefName')
        
        echo -e "${RED}⚠️  PR #${pr_number}: ${title}${NC}"
        echo -e "   状态：${RED}CONFLICTING${NC}"
        echo -e "   分支：${branch}"
        echo ""
        
        if [[ "$dry_run" == "true" ]]; then
            echo -e "${YELLOW}[dry_run] 建议操作：${NC}"
            echo "   1. 合并主分支：git checkout $branch && git merge main"
            echo "   2. 解决冲突后提交"
            echo "   3. 推送更新：git push origin $branch"
        else
            echo -e "${CYAN}构建合并提示：${NC}"
            echo ""
            echo -e "${BLUE}手动操作步骤：${NC}"
            echo "   git fetch origin"
            echo "   git checkout $branch"
            echo "   git merge origin/main"
            echo "   # 解决冲突后"
            echo "   git add ."
            echo "   git commit -m 'Merge main into $branch'"
            echo "   git push origin $branch"
            echo ""
        fi
    done
}

# 标记陈旧的 PR
mark_stale() {
    local repo="$1"
    local days="${2:-30}"
    local dry_run="${3:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  📌 标记陈旧的 PR                                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info "$repo"
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${CYAN}陈旧天数：${days} 天${NC}"
    echo ""
    
    # 获取最近未活动的 PR
    echo -e "${YELLOW}获取陈旧的 PR...${NC}"
    echo ""
    
    local pr_list=$(gh pr list \
        --repo "$REPO_SLUG" \
        --state open \
        --limit "${FETCH_LIMIT}" \
        --json number,title,lastEditedAt,noRecentActivity \
        --jq '.[] | select(.noRecentActivity == true)' \
        2>/dev/null)
    
    if [[ -z "$pr_list" ]]; then
        echo -e "${GREEN}✅ 未找到陈旧的 PR${NC}"
        return
    fi
    
    echo "$pr_list" | jq -c '.[]' | while read -r pr; do
        local pr_number=$(echo "$pr" | jq -r '.number')
        local title=$(echo "$pr" | jq -r '.title')
        local last_edited=$(echo "$pr" | jq -r '.lastEditedAt')
        
        echo -e "${YELLOW}陈旧 PR #${pr_number}: ${title}${NC}"
        echo -e "   最后活动：${last_edited}"
        echo -e "   标记状态：${YELLOW}STALE${NC}"
        echo ""
        
        if [[ "$dry_run" != "true" ]]; then
            echo -e "${CYAN}添加陈旧标签...${NC}"
            gh pr edit "$pr_number" --add-label "stale" 2>/dev/null || true
            echo -e "${GREEN}✅ 已标记为 STALE${NC}"
            echo ""
        fi
    done
}

# 主函数
main() {
    check_gh
    check_git
    
    local command="${1:-help}"
    shift || true
    
    local repo=""
    local days="$MAX_DAYS_OLD"
    local dry_run="false"
    local verbose="false"
    
    # 解析选项
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -r|--repo)
                repo="$2"
                shift 2
                ;;
            -d|--days)
                days="$2"
                shift 2
                ;;
            -l|--limit)
                FETCH_LIMIT="$2"
                shift 2
                ;;
            -y|--yes)
                NO_PROMPT="true"
                shift
                ;;
            -n|--dry-run)
                dry_run="true"
                shift
                ;;
            -v|--verbose)
                verbose="true"
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
    
    case "$command" in
        merged)
            cleanup_merged "$repo" "$dry_run"
            ;;
        old)
            cleanup_old "$repo" "$days" "$dry_run"
            ;;
        conflicts)
            handle_conflicts "$repo" "$dry_run"
            ;;
        stale)
            mark_stale "$repo" "$days" "$dry_run"
            ;;
        *)
            echo -e "${RED}❌ 未知命令：${command}${NC}"
            echo ""
            show_help
            ;;
    esac
}

main "$@"
