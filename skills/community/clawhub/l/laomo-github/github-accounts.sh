#!/bin/bash

# github-accounts.sh - GitHub 多账户管理工具
#
# 功能：
# 1. 列出已配置的 GitHub 账户
# 2. 添加新账户
# 3. 切换当前账户
# 4. 删除账户
# 5. 验证账户状态
#
# 用法：
#   ./github-accounts.sh list           # 列出账户
#   ./github-accounts.sh add [alias]    # 添加账户
#   ./github-accounts.sh switch [alias] # 切换账户
#   ./github-accounts.sh remove [alias] # 删除账户
#   ./github-accounts.sh validate       # 验证所有账户
#   ./github-accounts.sh current        # 显示当前账户
#   ./github-accounts.sh --help         # 显示帮助

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 账户配置目录
ACCOUNTS_DIR="$HOME/.config/github-accounts"
CURRENT_ACCOUNT_FILE="$ACCOUNTS_DIR/.current"

# 显示帮助信息
show_help() {
    cat << EOF
GitHub 多账户管理工具

用法：
  github-accounts.sh [command] [options]

命令:
  list              列出所有已配置的账户
  add [alias]       添加新账户（需要交互式认证）
  switch [alias]    切换到指定账户
  remove [alias]    删除指定账户
  validate          验证所有账户是否有效
  current           显示当前使用的账户
  help, --help, -h  显示此帮助信息

示例:
  github-accounts.sh add personal           # 添加个人账户
  github-accounts.sh switch work            # 切换到工作账户
  github-accounts.sh validate               # 验证所有账户

配置文件位置：$ACCOUNTS_DIR
当前账户文件：$CURRENT_ACCOUNT_FILE

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

# 初始化账户目录
init_accounts() {
    mkdir -p "$ACCOUNTS_DIR"
}

# 获取当前账户
get_current_account() {
    if [[ -f "$CURRENT_ACCOUNT_FILE" ]]; then
        cat "$CURRENT_ACCOUNT_FILE"
    else
        echo "default"
    fi
}

# 设置当前账户
set_current_account() {
    local alias="$1"
    echo "$alias" > "$CURRENT_ACCOUNT_FILE"
}

# 切换 GitHub 账户
switch_account() {
    local alias="$1"
    
    if [[ -z "$alias" ]]; then
        echo -e "${RED}❌ 用法：./github-accounts.sh switch <alias>${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🔄 切换 GitHub 账户                              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    
    local config_file="$ACCOUNTS_DIR/${alias}.json"
    
    if [[ ! -f "$config_file" ]]; then
        echo -e "${YELLOW}⚠️  账户配置不存在，需要重新认证${NC}"
        echo ""
        
        # 保存当前账户
        local current=$(get_current_account)
        echo "$current" > "$ACCOUNTS_DIR/.backup_current"
        
        # 退出当前认证
        gh auth logout -y 2>/dev/null || true
        
        # 重新认证
        gh auth login --hostname github.com --git-protocol https
        
        # 保存配置
        local user=$(gh api user --jq .login 2>/dev/null)
        local email=$(gh api user --jq .email 2>/dev/null || echo "private")
        
        cat > "$config_file" << EOF
{
  "alias": "${alias}",
  "username": "${user}",
  "email": "${email}",
  "hostname": "github.com",
  "protocol": "https",
  "authedAt": "$(date -Iseconds)",
  "scopes": ["repo", "user", "workflow"]
}
EOF
        
        set_current_account "$alias"
        
        echo ""
        echo -e "${GREEN}✅ 账户配置已保存：${alias}${NC}"
        echo -e "${CYAN}👤 用户名：${user}${NC}"
        echo -e "${CYAN}📧 邮箱：${email}${NC}"
    else
        set_current_account "$alias"
        echo -e "${GREEN}✅ 已切换到账户：${alias}${NC}"
    fi
    
    echo ""
    
    # 验证账户
    validate_account "$alias"
}

# 验证账户状态
validate_account() {
    local alias="${1:-$(get_current_account)}"
    local config_file="$ACCOUNTS_DIR/${alias}.json"
    
    if [[ ! -f "$config_file" ]]; then
        echo -e "${RED}❌ 账户配置不存在：${alias}${NC}"
        return 1
    fi
    
    # 读取配置
    local username=$(cat "$config_file" | grep -o '"username": *"[^"]*"' | cut -d'"' -f4)
    
    echo -e "${BLUE}验证账户：${alias}${NC}"
    echo -e "${CYAN}用户名：${username}${NC}"
    
    # 尝试获取用户信息
    if gh auth status 2>/dev/null | grep -q "logged in"; then
        echo -e "${GREEN}✅ 账户状态：已登录${NC}"
        return 0
    else
        echo -e "${RED}❌ 账户状态：未登录${NC}"
        return 1
    fi
}

# 添加新账户
add_account() {
    local alias="${1:-}"
    
    if [[ -z "$alias" ]]; then
        echo -e "${RED}❌ 用法：./github-accounts.sh add <alias>${NC}"
        echo ""
        echo "示例："
        echo "   ./github-accounts.sh add personal"
        echo "   ./github-accounts.sh add work"
        exit 1
    fi
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ➕ 添加 GitHub 账户                              ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    check_gh
    
    # 检查是否已存在
    local config_file="$ACCOUNTS_DIR/${alias}.json"
    if [[ -f "$config_file" ]]; then
        echo -e "${YELLOW}⚠️  账户 ${alias} 已存在${NC}"
        echo ""
        echo -e "${CYAN}当前配置：${NC}"
        cat "$config_file"
        echo ""
        read -p "是否覆盖？(y/N) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
    
    # 保存当前账户
    local current=$(get_current_account)
    echo "$current" > "$ACCOUNTS_DIR/.backup_current"
    
    # 退出当前认证
    gh auth logout -y 2>/dev/null || true
    
    # 交互式认证
    echo -e "${YELLOW}📝 开始认证流程...${NC}"
    echo ""
    gh auth login --hostname github.com --git-protocol https
    
    # 获取用户信息
    local user=$(gh api user --jq .login 2>/dev/null)
    local email=$(gh api user --jq .email 2>/dev/null || echo "private")
    
    # 保存配置
    cat > "$config_file" << EOF
{
  "alias": "${alias}",
  "username": "${user}",
  "email": "${email}",
  "hostname": "github.com",
  "protocol": "https",
  "authedAt": "$(date -Iseconds)",
  "scopes": ["repo", "user", "workflow"]
}
EOF
    
    set_current_account "$alias"
    
    echo ""
    echo -e "${GREEN}✅ 账户已添加：${alias}${NC}"
    echo -e "${CYAN}👤 用户名：${user}${NC}"
    echo -e "${CYAN}📧 邮箱：${email}${NC}"
}

# 删除账户
remove_account() {
    local alias="$1"
    
    if [[ -z "$alias" ]]; then
        echo -e "${RED}❌ 用法：./github-accounts.sh remove <alias>${NC}"
        exit 1
    fi
    
    local config_file="$ACCOUNTS_DIR/${alias}.json"
    
    if [[ ! -f "$config_file" ]]; then
        echo -e "${RED}❌ 账户不存在：${alias}${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}⚠️  确认删除账户：${alias}${NC}"
    read -p "此操作不可恢复，是否继续？(y/N) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}❌ 操作已取消${NC}"
        exit 0
    fi
    
    # 删除配置文件
    rm "$config_file"
    
    # 如果删除的是当前账户，切换到默认
    if [[ "$(get_current_account)" == "$alias" ]]; then
        rm "$CURRENT_ACCOUNT_FILE"
    fi
    
    echo -e "${GREEN}✅ 账户已删除：${alias}${NC}"
}

# 列出所有账户
list_accounts() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${Blue}║  📋 GitHub 账户列表                               ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [[ ! -d "$ACCOUNTS_DIR" ]] || [[ -z "$(ls -A "$ACCOUNTS_DIR" 2>/dev/null | grep -v '\.backup_current')" ]]; then
        echo -e "${YELLOW} confident 账户。运行 'github-accounts.sh add <alias>' 添加账户${NC}"
        return
    fi
    
    echo -e "${YELLOW}可用账户：${NC}"
    echo ""
    
    local current=$(get_current_account)
    
    for config_file in "$ACCOUNTS_DIR"/*.json; do
        if [[ -f "$config_file" ]]; then
            local alias=$(cat "$config_file" | grep -o '"alias": *"[^"]*"' | cut -d'"' -f4)
            local username=$(cat "$config_file" | grep -o '"username": *"[^"]*"' | cut -d'"' -f4)
            
            local marker=""
            if [[ "$alias" == "$current" ]]; then
                marker=" ← ${GREEN}当前账户${NC}"
            fi
            
            echo -e "📌 ${CYAN}${alias}${NC} (${username})${marker}"
        fi
    done
    
    echo ""
    echo -e "${BLUE}提示：${NC}"
    echo "   - 切换账户：github-accounts.sh switch <alias>"
    echo "   - 添加账户：github-accounts.sh add <alias>"
    echo "   - 删除账户：github-accounts.sh remove <alias>"
}

# 验证所有账户
validate_all() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ✅ 验证所有 GitHub 账户                          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    local success=0
    local failed=0
    
    for config_file in "$ACCOUNTS_DIR"/*.json; do
        if [[ -f "$config_file" ]]; then
            local alias=$(cat "$config_file" | grep -o '"alias": *"[^"]*"' | cut -d'"' -f4)
            
            if validate_account "$alias" 2>/dev/null; then
                ((success++))
            else
                ((failed++))
            fi
        fi
    done
    
    echo ""
    echo -e "${BLUE}统计：${NC}"
    echo -e "   ✅ 有效：${success}"
    echo -e "   ❌ 失效：${failed}"
}

# 显示当前账户
show_current() {
    local current=$(get_current_account)
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  📍 当前 GitHub 账户                             ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [[ -f "$ACCOUNTS_DIR/${current}.json" ]]; then
        local username=$(cat "$ACCOUNTS_DIR/${current}.json" | grep -o '"username": *"[^"]*"' | cut -d'"' -f4)
        local authed_at=$(cat "$ACCOUNTS_DIR/${current}.json" | grep -o '"authedAt": *"[^"]*"' | cut -d'"' -f4)
        
        echo -e "${GREEN}当前账户：${current}${NC}"
        echo -e "${CYAN}用户名：${username}${NC}"
        echo -e "${YELLOW}认证时间：${authed_at}${NC}"
        
        # 显示验证状态
        if validate_account "$current" 2>/dev/null; then
            echo -e "${GREEN}状态：✓ 已登录${NC}"
        else
            echo -e "${RED}状态：✗ 未登录${NC}"
        fi
    else
        echo -e "${YELLOW}当前账户：${current} (未配置)${NC}"
    fi
}

# 主函数
main() {
    init_accounts
    
    local command="${1:-list}"
    shift || true
    
    case "$command" in
        list|ls)
            list_accounts
            ;;
        add)
            add_account "$@"
            ;;
        switch|use)
            switch_account "$@"
            ;;
        remove|rm|del)
            remove_account "$@"
            ;;
        validate|check)
            validate_all
            ;;
        current|whoami)
            show_current
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
