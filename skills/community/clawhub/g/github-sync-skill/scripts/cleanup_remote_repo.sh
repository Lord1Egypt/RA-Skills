#!/bin/bash

# 清理远程仓库 - 递归删除非原创技能
# 用法：cleanup_remote_repo.sh [--dry-run]

set -e

OWNER="kuiilabs"
REPO="claude-skills"
TOKEN="${GITHUB_TOKEN:-}"
DRY_RUN=false

# 原创技能白名单（只保留这些）
KEEP_SKILLS=(
    "ip-risk-scanner"
    "video-transcript"
    "github-sync-skill"
    "ollama-download-accelerator"
    "wechat-saver"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --token)
            TOKEN="$2"
            shift 2
            ;;
        *)
            echo "用法：$0 [--dry-run] [--token TOKEN]"
            echo "  --dry-run  只检查不删除"
            exit 1
            ;;
    esac
done

if [ -z "$TOKEN" ]; then
    log_error "Token 为空，请使用 --token 参数或设置 GITHUB_TOKEN 环境变量"
    exit 1
fi

# 递归删除目录
delete_tree() {
    local path=$1
    local items=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO/contents/$path" | \
        jq -r '.[] | "\(.path)|\(.sha)|\(.type)"')

    while IFS='|' read -r item_path sha type; do
        if [ -n "$item_path" ] && [ "$item_path" != "null" ]; then
            if [ "$type" = "dir" ]; then
                delete_tree "$item_path"
            fi
            if [ "$DRY_RUN" = true ]; then
                log_info "  [DRY-RUN] 删除：$item_path"
            else
                log_info "  删除：$item_path"
                curl -s -X DELETE -H "Authorization: token $TOKEN" \
                    "https://api.github.com/repos/$OWNER/$REPO/contents/$item_path" \
                    -d "{\"message\":\"Cleanup\",\"sha\":\"$sha\",\"branch\":\"main\"}" > /dev/null
            fi
        fi
    done <<< "$items"
}

# 主流程
log_info "获取远程仓库内容..."
remote_items=$(curl -s -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$OWNER/$REPO/contents" | \
    jq -r '.[] | .name')

to_delete=()
to_keep=()

for item in $remote_items; do
    [[ "$item" == ".git" || "$item" == "README.md" || "$item" == ".gitignore" ]] && continue

    keep=false
    for k in "${KEEP_SKILLS[@]}"; do
        [[ "$item" == "$k" ]] && keep=true && break
    done

    if [ "$keep" = true ]; then
        to_keep+=("$item")
    else
        to_delete+=("$item")
    fi
done

echo ""
log_info "保留的技能 (${#to_keep[@]}): ${to_keep[*]}"
log_info "待删除的技能 (${#to_delete[@]}): ${to_delete[*]}"

if [ ${#to_delete[@]} -eq 0 ]; then
    log_success "没有需要清理的内容"
    exit 0
fi

if [ "$DRY_RUN" = true ]; then
    log_warning "干运行模式，不执行删除"
    exit 0
fi

echo ""
read -p "确认删除以上 ${#to_delete[@]} 个技能？(y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    log_info "已取消"
    exit 0
fi

# 删除每个技能
for skill in "${to_delete[@]}"; do
    log_info "删除：$skill"
    delete_tree "$skill"
done

log_success "清理完成！远程仓库现在只包含原创技能"
