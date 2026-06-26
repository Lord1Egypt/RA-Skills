#!/bin/bash

# GitHub Sync Script - 技能同步到 GitHub
# 用法：sync_to_github.sh [--owner owner] [--repo repo] [--token token] [--skill skill-name]

set -e

# 默认配置
DEFAULT_OWNER="kuiilabs"
DEFAULT_REPO="claude-skills"
SKILLS_DIR="$HOME/.claude/skills"
GIT_USER_NAME="kuiilabs"
GIT_USER_EMAIL="kuiilabs@users.noreply.github.com"

# 用户创建的原创技能列表（白名单，只同步这些技能）
# 添加新技能时，在这里添加名称即可
USER_CREATED_SKILLS=(
    "ip-risk-scanner"
    "video-transcript"
    "github-sync-skill"
    "ollama-download-accelerator"
    "wechat-saver"
)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 解析参数
OWNER="$DEFAULT_OWNER"
REPO="$DEFAULT_REPO"
TOKEN="$GITHUB_TOKEN"
SPECIFIC_SKILL=""  # 指定同步单个技能

while [[ $# -gt 0 ]]; do
    case $1 in
        --owner)
            OWNER="$2"
            shift 2
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --token)
            TOKEN="$2"
            shift 2
            ;;
        --skill)
            SPECIFIC_SKILL="$2"
            shift 2
            ;;
        --help)
            echo "用法：$0 [--owner owner] [--repo repo] [--token token] [--skill skill-name]"
            echo ""
            echo "选项:"
            echo "  --owner    GitHub 用户名或组织 (默认：$DEFAULT_OWNER)"
            echo "  --repo     仓库名称 (默认：$DEFAULT_REPO)"
            echo "  --token    GitHub PAT Token (或使用 GITHUB_TOKEN 环境变量)"
            echo "  --skill    指定同步单个技能 (可选，不指定则增量同步所有用户技能)"
            echo ""
            echo "示例:"
            echo "  # 增量同步所有用户技能"
            echo "  $0 --owner kuiilabs --repo claude-skills --token ghp_xxx"
            echo ""
            echo "  # 仅同步指定技能"
            echo "  $0 --skill new-skill --owner kuiilabs --repo claude-skills --token ghp_xxx"
            exit 0
            ;;
        *)
            echo "未知选项：$1"
            exit 1
            ;;
    esac
done

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查环境依赖..."

    if ! command -v git &> /dev/null; then
        log_error "Git 未安装，请先安装 Git"
        exit 1
    fi

    if ! command -v curl &> /dev/null; then
        log_error "curl 未安装，请先安装 curl"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        log_warning "jq 未安装，建议安装以获得更好的体验"
    fi

    log_success "环境检查完成"
}

# 验证 Token
verify_token() {
    log_info "验证 GitHub Token..."

    if [ -z "$TOKEN" ]; then
        log_error "Token 为空，请使用 --token 参数或设置 GITHUB_TOKEN 环境变量"
        exit 1
    fi

    # 验证 Token 所有者
    response=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user)

    if echo "$response" | grep -q '"login"'; then
        login=$(echo "$response" | jq -r '.login' 2>/dev/null || echo "unknown")
        log_success "Token 有效，所有者：$login"
    else
        log_error "Token 无效，请检查 Token 是否正确"
        echo "响应：$response"
        exit 1
    fi
}

# 检查仓库是否存在
check_repo_exists() {
    log_info "检查仓库是否存在..."

    response=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO")

    if echo "$response" | grep -q '"full_name"'; then
        log_success "仓库已存在：$OWNER/$REPO"
        return 0
    else
        log_warning "仓库不存在，将创建新仓库"
        return 1
    fi
}

# 创建仓库
create_repo() {
    log_info "创建仓库 $OWNER/$REPO..."

    response=$(curl -s -X POST \
        -H "Authorization: token $TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        https://api.github.com/user/repos \
        -d "{\"name\":\"$REPO\",\"private\":false,\"auto_init\":true}")

    if echo "$response" | grep -q '"full_name"'; then
        log_success "仓库创建成功：$OWNER/$REPO"
        return 0
    else
        log_error "仓库创建失败"
        echo "响应：$response"
        exit 1
    fi
}

# 获取远程仓库已有的技能列表
get_remote_skills() {
    log_info "获取远程仓库技能列表..."

    local skills=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO/contents" | \
        jq -r '.[] | select(.type=="dir") | .name' 2>/dev/null)

    echo "$skills"
}

# 从 SKILL.md 提取技能信息
extract_skill_info() {
    local skill_dir="$1"
    local skill_file="$skill_dir/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        echo ""
        return
    fi

    # 提取 name, description, tags
    local name=$(grep -m1 "^name:" "$skill_file" 2>/dev/null | sed 's/name: *//' | tr -d '"')
    local desc=$(grep -m1 "^description:" "$skill_file" 2>/dev/null | sed 's/description: *//' | tr -d '"')
    local tags=$(grep -m1 "^tags:" "$skill_file" 2>/dev/null | sed 's/tags: *//' | tr -d '[]"' | tr ' ' ',')

    if [ -z "$name" ]; then
        name=$(basename "$skill_dir")
    fi

    echo "$name|$desc|$tags"
}

# 生成 README.md 内容
generate_readme() {
    local skills_info="$1"

    cat << EOF
# Claude Code Skills Collection

> 个人创建和开发的 Claude Code 技能集合

## 📚 技能列表

EOF

    echo "$skills_info" | while IFS='|' read -r name desc tags path; do
        if [ -n "$name" ]; then
            echo "### $name"
            echo ""
            echo "$desc"
            echo ""
            if [ -n "$tags" ]; then
                echo "**标签**: $tags"
            fi
            echo ""
        fi
    done

    cat << EOF
## 🚀 使用方法

### 安装

1. 克隆本仓库：
\`\`\`bash
git clone https://github.com/$OWNER/$REPO.git
\`\`\`

2. 将技能链接到 Claude Code 目录：
\`\`\`bash
ln -s \$(pwd)/<skill-name> ~/.claude/skills/<skill-name>
\`\`\`

### 同步技能

使用 \`github-sync-skill\` 自动同步：

\`\`\`bash
# 增量同步所有用户技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh

# 仅同步指定技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh --skill <skill-name>
\`\`\`

## 📦 技能详情

每个技能文件夹包含：
- \`SKILL.md\` - 技能说明文档
- \`scripts/\` - 执行脚本
- \`references/\` - 参考文档（可选）

## 📝 更新日志

EOF
    echo "* $(date '+%Y-%m-%d') - 初始化仓库，包含 ${USER_CREATED_SKILLS[*]}"
}

# 更新 README.md
update_readme() {
    local synced_skills="$1"

    log_info "更新 README.md..."

    # 获取当前 README
    local current_readme=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO/contents/README.md")

    local readme_sha=$(echo "$current_readme" | jq -r '.sha' 2>/dev/null)
    local readme_content=""

    # 构建技能信息
    local skills_info=""

    # 获取远程所有技能
    local remote_skills=$(get_remote_skills)

    # 合并已存在的技能信息 + 新同步的技能
    for skill in $remote_skills $synced_skills; do
        # 跳过非技能目录
        if [[ "$skill" == ".git" ]] || [[ -z "$skill" ]]; then
            continue
        fi

        local skill_path="$SKILLS_DIR/$skill"
        if [ -d "$skill_path" ]; then
            local info=$(extract_skill_info "$skill_path")
            if [ -n "$info" ]; then
                local name=$(echo "$info" | cut -d'|' -f1)
                local desc=$(echo "$info" | cut -d'|' -f2)
                local tags=$(echo "$info" | cut -d'|' -f3)
                skills_info+="$name|$desc|$tags|$skill\n"
            fi
        fi
    done

    # 生成新的 README 内容
    local new_readme=$(generate_readme "$skills_info")

    # Base64 编码
    local encoded=$(echo -n "$new_readme" | base64 | tr -d '\n')

    # 更新 README
    if [ -n "$readme_sha" ] && [ "$readme_sha" != "null" ]; then
        # 已存在，更新
        curl -s -X PUT -H "Authorization: token $TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/$OWNER/$REPO/contents/README.md" \
            -d "{\"message\":\"Update README with new skills: $synced_skills\",\"content\":\"$encoded\",\"sha\":\"$readme_sha\",\"branch\":\"main\"}" > /dev/null
    else
        # 不存在，创建
        curl -s -X PUT -H "Authorization: token $TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/$OWNER/$REPO/contents/README.md" \
            -d "{\"message\":\"Create README.md\",\"content\":\"$encoded\",\"branch\":\"main\"}" > /dev/null
    fi

    log_success "README.md 已更新"
}

# 增量同步技能
sync_skills() {
    cd "$SKILLS_DIR"

    # 获取远程已有的技能
    local remote_skills=$(get_remote_skills)

    # 确定要同步的技能
    local skills_to_sync=()

    if [ -n "$SPECIFIC_SKILL" ]; then
        # 同步指定技能
        if [ -d "$SPECIFIC_SKILL" ]; then
            skills_to_sync=("$SPECIFIC_SKILL")
            log_info "同步指定技能：$SPECIFIC_SKILL"
        else
            log_error "技能目录不存在：$SPECIFIC_SKILL"
            exit 1
        fi
    else
        # 增量同步：只同步本地有但远程没有的技能
        log_info "增量同步模式：检测新技能..."

        for skill in "${USER_CREATED_SKILLS[@]}"; do
            if [ -d "$skill" ]; then
                # 检查远程是否存在
                if ! echo "$remote_skills" | grep -q "^$skill$"; then
                    skills_to_sync+=("$skill")
                    log_info "  🆕 新技能：$skill"
                else
                    log_info "  ✅ 已存在：$skill"
                fi
            fi
        done
    fi

    if [ ${#skills_to_sync[@]} -eq 0 ]; then
        log_info "没有需要同步的技能"
        return 0
    fi

    # 同步每个技能
    local synced_names=""
    for skill in "${skills_to_sync[@]}"; do
        log_info "正在同步：$skill"

        # 上传技能文件
        while IFS= read -r file; do
            rel_path="${file#$SKILLS_DIR/}"
            upload_file "$file" "$rel_path" "Add $skill skill"
        done < <(find "$skill" -type f)

        synced_names+="$skill "
    done

    # 更新 README
    update_readme "$synced_names"

    log_success "同步完成：$synced_names"
}

# 上传单个文件到 GitHub
upload_file() {
    local file="$1"
    local path="$2"
    local message="$3"

    # Base64 编码
    local encoded=$(base64 -i "$file" | tr -d '\n')

    # 检查文件是否已存在
    local sha=""
    local check=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO/contents/$path")

    if echo "$check" | grep -q '"sha"'; then
        sha=$(echo "$check" | jq -r '.sha')
    fi

    # 创建/更新文件
    if [ -n "$sha" ]; then
        result=$(curl -s -X PUT -H "Authorization: token $TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/$OWNER/$REPO/contents/$path" \
            -d "{\"message\":\"$message\",\"content\":\"$encoded\",\"sha\":\"$sha\",\"branch\":\"main\"}")
    else
        result=$(curl -s -X PUT -H "Authorization: token $TOKEN" \
            -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/$OWNER/$REPO/contents/$path" \
            -d "{\"message\":\"$message\",\"content\":\"$encoded\",\"branch\":\"main\"}")
    fi

    if echo "$result" | grep -q '"content"'; then
        return 0
    else
        log_error "上传失败：$path"
        return 1
    fi
}

# 生成报告
generate_report() {
    log_info "生成同步报告..."

    echo ""
    echo "============================================================"
    echo "  GitHub Sync Report"
    echo "============================================================"
    echo ""
    echo "仓库：$OWNER/$REPO"
    echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
    if [ -n "$SPECIFIC_SKILL" ]; then
        echo "同步模式：指定技能 ($SPECIFIC_SKILL)"
    else
        echo "同步模式：增量同步"
    fi
    echo "状态：✅ 成功"
    echo ""
    echo "仓库链接：https://github.com/$OWNER/$REPO"
    echo ""
    echo "============================================================"
}

# 检查远程是否有非原创技能
check_foreign_skills() {
    log_info "检查远程仓库内容..."

    local remote_items=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$OWNER/$REPO/contents" | \
        jq -r '.[] | .name')

    local foreign_count=0
    for item in $remote_items; do
        [[ "$item" == ".git" || "$item" == "README.md" || "$item" == ".gitignore" ]] && continue

        local keep=false
        for k in "${USER_CREATED_SKILLS[@]}"; do
            [[ "$item" == "$k" ]] && keep=true && break
        done

        if [ "$keep" = false ]; then
            if [ $foreign_count -eq 0 ]; then
                log_warning "发现非原创技能（可能是误上传）:"
            fi
            echo "  - $item"
            ((foreign_count++))
        fi
    done

    if [ $foreign_count -gt 0 ]; then
        echo ""
        log_warning "发现 $foreign_count 个非原创技能在远程仓库中"
        log_info "建议先运行清理脚本："
        echo "  ~/.claude/skills/github-sync-skill/scripts/cleanup_remote_repo.sh"
        echo ""
        read -p "是否继续同步？(y/N): " confirm
        if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
            log_info "已取消同步"
            exit 0
        fi
    fi
}

# 主流程
main() {
    echo ""
    echo "============================================================"
    echo "  GitHub Sync - 技能同步工具"
    echo "============================================================"
    echo ""

    check_dependencies
    verify_token

    # 检查仓库是否存在，不存在则创建
    if ! check_repo_exists; then
        create_repo
    fi

    # 检查是否有非原创技能（防止误上传）
    check_foreign_skills

    # 同步技能
    sync_skills

    generate_report
}

# 执行主流程
main
