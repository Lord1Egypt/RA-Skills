#!/bin/bash
# OpenClaw Backup Skill - 安装脚本
# 用途：一键配置 OpenClaw 自动备份到 GitHub

set -e

OPENCLAW_DIR="$HOME/.openclaw"
SKILL_DIR="$OPENCLAW_DIR/workspace/skills/openclaw-backup"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 检查依赖
check_dependencies() {
    log_step "检查依赖..."
    
    if ! command -v git &>/dev/null; then
        log_error "未安装 Git，请先安装："
        echo "  Ubuntu/Debian: sudo apt install git"
        echo "  macOS: brew install git"
        exit 1
    fi
    
    log_info "Git 已安装: $(git --version)"
}

# 检查 SSH Key
check_ssh_key() {
    log_step "检查 SSH Key..."
    
    if [[ -f ~/.ssh/id_ed25519.pub ]] || [[ -f ~/.ssh/id_rsa.pub ]]; then
        log_info "已找到 SSH Key"
        
        # 测试 GitHub 连接
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
            log_info "GitHub SSH 连接正常"
            return 0
        else
            log_warn "SSH Key 可能未添加到 GitHub"
            echo "请将以下公钥添加到 GitHub → Settings → SSH Keys："
            cat ~/.ssh/id_ed25519.pub 2>/dev/null || cat ~/.ssh/id_rsa.pub 2>/dev/null
            echo ""
            read -p "已添加到 GitHub？继续安装？(y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    else
        log_warn "未找到 SSH Key，正在生成..."
        ssh-keygen -t ed25519 -C "openclaw-backup" -f ~/.ssh/id_ed25519 -N ""
        log_info "SSH Key 已生成"
        echo ""
        echo "请将以下公钥添加到 GitHub → Settings → SSH Keys："
        cat ~/.ssh/id_ed25519.pub
        echo ""
        read -p "已添加到 GitHub？继续安装？(y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # 添加 GitHub 到 known_hosts
    ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
}

# 获取配置
get_config() {
    log_step "配置 Git 用户信息..."
    
    # Git 用户名
    read -p "Git 用户名 (默认: $(whoami)): " git_name
    git_name=${git_name:-$(whoami)}
    
    # Git 邮箱
    read -p "Git 邮箱 (默认: ${git_name}@users.noreply.github.com): " git_email
    git_email=${git_email:-"${git_name}@users.noreply.github.com"}
    
    # 仓库地址
    echo ""
    echo "请在 GitHub 创建一个私有仓库："
    echo "  1. 访问 https://github.com/new"
    echo "  2. 仓库名建议: openclaw-backup"
    echo "  3. 必须选择 Private（私有）"
    echo "  4. 不要勾选 README/gitignore"
    echo ""
    read -p "GitHub 仓库地址 (如: git@github.com:yourname/openclaw-backup.git): " repo_url
    
    if [[ -z "$repo_url" ]]; then
        log_error "仓库地址不能为空"
        exit 1
    fi
    
    # 配置 Git
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    log_info "Git 用户配置完成"
    
    REPO_URL="$repo_url"
}

# 安装脚本
install_scripts() {
    log_step "安装备份脚本..."
    
    # 复制备份脚本
    cp "$SKILL_DIR/scripts/backup.sh" "$OPENCLAW_DIR/backup.sh"
    chmod +x "$OPENCLAW_DIR/backup.sh"
    log_info "已安装 backup.sh"
    
    # 复制活跃检查脚本
    cp "$SKILL_DIR/scripts/check-activity.sh" "$OPENCLAW_DIR/check-activity.sh"
    chmod +x "$OPENCLAW_DIR/check-activity.sh"
    log_info "已安装 check-activity.sh"
    
    # 创建 .gitignore
    cat > "$OPENCLAW_DIR/.gitignore" << 'EOF'
# OpenClaw Backup - 只排除日志文件

# API Key 在配置文件中 - 需要脱敏处理
openclaw.json.original

# 日志文件 - 无需备份
logs/
*.log

# 临时文件
*.tmp

# 系统文件
.DS_Store
Thumbs.db
EOF
    log_info "已创建 .gitignore"
}

# 初始化 Git 仓库
init_git() {
    log_step "初始化 Git 仓库..."
    
    cd "$OPENCLAW_DIR"
    
    if [[ -d ".git" ]]; then
        log_warn "Git 仓库已存在，更新远程地址..."
        git remote set-url origin "$REPO_URL" 2>/dev/null || git remote add origin "$REPO_URL"
    else
        git init
        git branch -M main
        git remote add origin "$REPO_URL"
        log_info "Git 仓库已初始化"
    fi
}

# 执行首次备份
first_backup() {
    log_step "执行首次备份..."
    
    cd "$OPENCLAW_DIR"
    
    # 清理嵌入的 git 仓库
    find . -name ".git" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # 脱敏配置
    if [[ -f "openclaw.json" ]]; then
        cp openclaw.json openclaw.json.original
        sed -E 's/"apiKey": "[^"]+"/"apiKey": "***SET_YOUR_API_KEY***"/g' openclaw.json.original > openclaw.json.staged
        mv openclaw.json.staged openclaw.json
    fi
    
    # 添加文件
    git add -A
    
    # 检查是否有文件
    if git diff --cached --quiet; then
        log_warn "没有文件需要提交"
    else
        git commit -m "Initial backup: OpenClaw configuration ($(date '+%Y-%m-%d %H:%M'))"
        log_info "已创建首次提交"
    fi
    
    # 推送
    if git push -u origin main --force; then
        log_info "已推送到 GitHub"
    else
        log_error "推送失败，请检查仓库地址和权限"
        exit 1
    fi
    
    # 恢复原始配置
    if [[ -f "openclaw.json.original" ]]; then
        mv openclaw.json.original openclaw.json
        log_info "已恢复原始配置"
    fi
}

# 配置 cron（可选）
setup_cron() {
    log_step "配置自动备份..."
    
    echo ""
    echo "是否配置自动备份？"
    echo "  - 活跃时每小时备份"
    echo "  - 非活跃时每天备份"
    read -p "配置自动备份？(y/n) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 这需要在 OpenClaw 中使用 cron 工具配置
        log_info "请在 OpenClaw 中运行以下命令配置自动备份："
        echo ""
        echo "使用 OpenClaw 的 cron 功能创建每小时检查任务"
        log_warn "自动备份需要手动在 OpenClaw 中配置 cron 任务"
    fi
}

# 完成
print_summary() {
    echo ""
    echo "========================================"
    log_info "安装完成！"
    echo "========================================"
    echo ""
    echo "📦 仓库地址: $REPO_URL"
    echo ""
    echo "使用方法："
    echo "  手动备份:  ~/.openclaw/backup.sh backup"
    echo "  自动检查:  ~/.openclaw/backup.sh auto"
    echo "  恢复配置:  ~/.openclaw/backup.sh restore"
    echo ""
    echo "查看备份: "
    echo "  ${REPO_URL%.git}"
    echo ""
}

# 主函数
main() {
    echo ""
    echo "========================================"
    echo "  OpenClaw Backup Skill 安装向导"
    echo "========================================"
    echo ""
    
    check_dependencies
    check_ssh_key
    get_config
    install_scripts
    init_git
    first_backup
    setup_cron
    print_summary
}

main "$@"