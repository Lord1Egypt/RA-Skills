#!/bin/bash

# github-pr-push.sh - GitHub PR 一键推送工具
#
# 功能：
# 1. 创建 PR 并推送代码
# 2. 支持自动 PR 描述生成
# 3. 支持关联 Issue
# 4. 支持多重提交合并
# 5. 支持 PR 标签和审查人
#
# 用法：
#   ./github-pr-push.sh create [branch]   # 创建 PR
#   ./github-pr-push.sh push [branch]     # 推送分支
#   ./github-pr-push.sh update [branch]   # 更新现有 PR
#   ./github-pr-push.sh merge [pr-number] # 合并 PR
#   ./github-pr-push.sh help              # 显示帮助

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 当前分支
CURRENT_BRANCH=$(git branch --show-current)

# 显示帮助信息
show_help() {
    cat << EOF
GitHub PR 一键推送工具

用法：
  github-pr-push.sh [command] [branch] [options]

命令:
  create [branch]    创建新的 PR（从指定分支或当前分支）
  push [branch]      推送分支到远程
  update [branch]    更新现有 PR
  merge [pr-number]  合并指定的 PR
  help, --help, -h   显示此帮助信息

选项:
  -m, --message      自定义 PR 描述
  -i, --issue        关联的 Issue 编号（多个用逗号分隔）
  -t, --title        自定义 PR 标题
  -l, --labels       添加标签（逗号分隔）
  -r, --reviewers    添加审查人（逗号分隔）
  -d, --draft        创建草稿 PR
  -f, --force        强制推送
  -c, --close        关闭 PR
  --auto-merge       合并时自动删除源分支

示例:
  github-pr-push.sh create feature/new-feature
  github-pr-push.sh create -m "描述内容" -i 123,456
  github-pr-push.sh push main
  github-pr-push.sh merge 123

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
    
    # 检查是否有本地提交
    local commit_count=$(git log --oneline | wc -l)
    if [[ $commit_count -eq 0 ]]; then
        echo -e "${YELLOW}⚠️  警告：暂无本地提交${NC}"
    fi
}

# 获取当前仓库信息
get_repo_info() {
    local remote_url=$(git remote get-url origin 2>/dev/null)
    
    # 解析仓库信息
    if [[ "$remote_url" =~ ^git@github\.com:([^/]+)/(.+)\.git$ ]] || \
       [[ "$remote_url" =~ ^https://github\.com/([^/]+)/(.+)\.git$ ]]; then
        REPO_OWNER="${BASH_REMATCH[1]}"
        REPO_NAME="${BASH_REMATCH[2]}"
    else
        echo -e "${RED}❌ 无法解析远程仓库 URL${NC}"
        echo "   $remote_url"
        exit 1
    fi
    
    REPO_SLUG="${REPO_OWNER}/${REPO_NAME}"
}

# 生成 PR 标题
generate_pr_title() {
    local branch="$1"
    local title="$2"
    
    if [[ -n "$title" ]]; then
        echo "$title"
    else
        # 从分支名生成标题
        local clean_branch=$(echo "$branch" | sed 's/[^a-zA-Z0-9]/ /g')
        local title=$(echo "$clean_branch" | xargs | sed 's/\b\([a-z]\)/\u\1/g')
        echo "$title"
    fi
}

# 生成 PR 描述
generate_pr_body() {
    local branch="$1"
    local message="$2"
    local issues="$3"
    
    local body=""
    
    # 自定义描述
    if [[ -n "$message" ]]; then
        body="$message"
    else
        # 从提交历史生成
        local recent_commits=$(git log --oneline -5)
        body="## Changes\n\n"
        body+="- 自动生成的 PR 描述\n\n"
        body+="### 最近提交\n\`\`\`\n${recent_commits}\n\`\`\`\n\n"
    fi
    
    # 关联 Issue
    if [[ -n "$issues" ]]; then
        body+="\n---\n\n### 关联 Issues\n\n"
        IFS=',' read -ra ISSUE_ARRAY <<< "$issues"
        for issue in "${ISSUE_ARRAY[@]}"; do
            body+="- #$(echo "$issue" | xargs)\n"
        done
    fi
    
    echo "$body"
}

# 创建 PR
create_pr() {
    local branch="${1:-$CURRENT_BRANCH}"
    local title="$2"
    local message="$3"
    local issues="$4"
    local labels="$5"
    local reviewers="$6"
    local draft=false
    
    shift 6 || true
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -m|--message)
                message="$2"
                shift 2
                ;;
            -i|--issue)
                issues="$2"
                shift 2
                ;;
            -t|--title)
                title="$2"
                shift 2
                ;;
            -l|--labels)
                labels="$2"
                shift 2
                ;;
            -r|--reviewers)
                reviewers="$2"
                shift 2
                ;;
            -d|--draft)
                draft=true
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ➕ 创建 GitHub Pull Request                     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    get_repo_info
    
    echo -e "${YELLOW}仓库：${REPO_SLUG}${NC}"
    echo -e "${YELLOW}分支：${branch}${NC}"
    echo ""
    
    # 推送分支
    echo -e "${CYAN}推送分支到远程...${NC}"
    git push -u origin "$branch"
    
    # 生成 PR 信息
    local pr_title=$(generate_pr_title "$branch" "$title")
    local pr_body=$(generate_pr_body "$branch" "$message" "$issues")
    
    echo -e "${CYAN}标题：${pr_title}${NC}"
    echo ""
    
    # 创建 PR
    local draft_flag=""
    if [[ "$draft" == "true" ]]; then
        draft_flag="--draft"
    fi
    
    local pr_url=$(gh pr create \
        --title "$pr_title" \
        --body "$pr_body" \
        --base main \
        --head "$branch" \
        $draft_flag \
        2>/dev/null)
    
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ PR 创建成功！${NC}"
        echo -e "${BLUE}PR 地址：${pr_url}${NC}"
        
        # 添加标签
        if [[ -n "$labels" ]]; then
            echo -e "${CYAN}添加标签：${labels}${NC}"
            IFS=',' read -ra LABEL_ARRAY <<< "$labels"
            for label in "${LABEL_ARRAY[@]}"; do
                gh pr edit "$(echo "$pr_url" | grep -o 'pull/[^/]*' | cut -d'/' -f2)" \
                    --add-label "$(echo "$label" | xargs)"
            done
        fi
        
        # 设置审查人
        if [[ -n "$reviewers" ]]; then
            echo -e "${CYAN}设置审查人：${reviewers}${NC}"
            IFS=',' read -ra REVIEWER_ARRAY <<< "$reviewers"
            for reviewer in "${REVIEWER_ARRAY[@]}"; do
                gh pr review "$(echo "$pr_url" | grep -o 'pull/[^/]*' | cut -d'/' -f2)" \
                    --request "$(echo "$reviewer" | xargs)"
            done
        fi
        
        echo ""
        echo -e "${GREEN}完成！${NC}"
    else
        echo -e "${RED}❌ PR 创建失败${NC}"
        exit 1
    fi
}

# 推送分支
push_branch() {
    local branch="${1:-$CURRENT_BRANCH}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  📤 推送分支到 GitHub                            ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    
    echo -e "${YELLOW}分支：${branch}${NC}"
    echo ""
    
    # 推送分支
    git push -u origin "$branch"
    
    echo -e "${GREEN}✅ 分支已推送：${branch}${NC}"
}

# 更新现有 PR
update_pr() {
    local branch="${1:-$CURRENT_BRANCH}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ✏️  更新 GitHub Pull Request                    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    
    echo -e "${YELLOW}分支：${branch}${NC}"
    echo ""
    
    # 获取当前分支的 PR
    local pr_number=$(gh pr list --head "$branch" --json number --jq '.[0].number' 2>/dev/null)
    
    if [[ -n "$pr_number" ]]; then
        echo -e "${CYAN}找到 PR #${pr_number}${NC}"
        echo ""
        
        # 推送更新
        git push origin "$branch"
        
        echo -e "${GREEN}✅ PR 已更新${NC}"
    else
        echo -e "${YELLOW}⚠️  未找到关联的 PR，创建新的 PR${NC}"
        create_pr "$branch"
    fi
}

# 合并 PR
merge_pr() {
    local pr_number="$1"
    local delete_branch="${2:-false}"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🔄 合并 Pull Request                             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    check_git
    
    if [[ -z "$pr_number" ]]; then
        echo -e "${RED}❌ 用法：./github-pr-push.sh merge <pr-number> [delete-branch]${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}PR #${pr_number}${NC}"
    echo ""
    
    # 获取 PR 信息
    local pr_info=$(gh pr view "$pr_number" --json title,author,state,mergeable,headRefName,baseRefName 2>/dev/null)
    
    if [[ -z "$pr_info" ]]; then
        echo -e "${RED}❌ 无法获取 PR 信息${NC}"
        exit 1
    fi
    
    local title=$(echo "$pr_info" | grep -o '"title": *"[^"]*"' | cut -d'"' -f4)
    local author=$(echo "$pr_info" | grep -o '"author": *{[^}]*}' | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)
    local state=$(echo "$pr_info" | grep -o '"state": *"[^"]*"' | cut -d'"' -f4)
    local mergeable=$(echo "$pr_info" | grep -o '"mergeable": *"[^"]*"' | cut -d'"' -f4)
    local head_ref=$(echo "$pr_info" | grep -o '"headRefName": *"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${YELLOW}标题：${title}${NC}"
    echo -e "${CYAN}作者：${author}${NC}"
    echo -e "${YELLOW}状态：${state}${NC}"
    echo ""
    
    if [[ "$state" != "OPEN" ]]; then
        echo -e "${YELLOW}⚠️  PR 已关闭或合并${NC}"
        exit 0
    fi
    
    # 询问是否合并
    if [[ "$mergeable" == "MERGEABLE" ]] || [[ "$mergeable" == "CONFLICTING" ]]; then
        echo -e "${CYAN}是否合并此 PR？${NC}"
        read -p "输入 'yes' 确认： " -r
        echo ""
        
        if [[ "$REPLY" == "yes" ]]; then
            if gh pr merge "$pr_number" --squash; then
                echo -e "${GREEN}✅ PR 已合并${NC}"
                
                # 是否删除分支
                if [[ "$delete_branch" == "true" ]] || [[ "$delete_branch" == "yes" ]]; then
                    echo -e "${CYAN}删除分支：${head_ref}${NC}"
                    git push origin --delete "$head_ref"
                    echo -e "${GREEN}✅ 分支已删除${NC}"
                fi
            else
                echo -e "${RED}❌ 合并失败${NC}"
                exit 1
            fi
        else
            echo -e "${CYAN}❌ 合并已取消${NC}"
        fi
    else
        echo -e "${RED}❌ PR 不可合并（Conflict 或其他问题）${NC}"
        exit 1
    fi
}

# 主函数
main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        create)
            create_pr "$@"
            ;;
        push)
            push_branch "$@"
            ;;
        update)
            update_pr "$@"
            ;;
        merge)
            merge_pr "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ 未知命令：${command}${NC}"
            echo ""
            show_help
            ;;
    esac
}

main "$@"
