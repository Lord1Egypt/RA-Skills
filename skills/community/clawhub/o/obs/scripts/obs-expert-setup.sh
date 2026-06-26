#!/bin/bash
# obs-expert-setup.sh - OBS Expert Configuration Script
# OBS Expert 配置脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBS_CONFIG_DIR="$HOME/.config/osc"
OBS_CONFIG_FILE="$OBS_CONFIG_DIR/oscrc"

# 颜色定义 | Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_title() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

echo_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 检查安装 | Check Installation
check_installation() {
    echo_title "检查安装状态 | Checking Installation Status"
    
    if [ -f "$SCRIPT_DIR/scripts/obs-expert" ]; then
        echo_success "OBS Expert 脚本已安装 | OBS Expert script installed"
    else
        echo_error "OBS Expert 脚本未找到 | OBS Expert script not found"
        exit 1
    fi
    
    if [ -f "$SCRIPT_DIR/references/obs-lib.sh" ]; then
        echo_success "OBS API 库已安装 | OBS API library installed"
    else
        echo_error "OBS API 库未找到 | OBS API library not found"
        exit 1
    fi
}

# 检查现有配置 | Check Existing Configuration
check_existing_config() {
    echo_title "检查现有配置 | Checking Existing Configuration"
    
    local has_config=false
    
    # 检查 oscrc
    if [ -f "$OBS_CONFIG_FILE" ]; then
        echo_success "找到 oscrc 配置文件 | Found oscrc config file"
        has_config=true
    else
        echo_warning "未找到 oscrc 配置文件 | oscrc config file not found"
    fi
    
    # 检查环境变量
    if [ -n "$OBS_USERNAME" ] && [ -n "$OBS_TOKEN" ]; then
        echo_success "找到 OBS 环境变量 | Found OBS environment variables"
        has_config=true
    else
        echo_warning "未设置 OBS 环境变量 | OBS environment variables not set"
    fi
    
    if [ "$has_config" = true ]; then
        echo ""
        echo_warning "检测到现有配置 | Existing configuration detected"
        read -p "是否重新配置？| Reconfigure? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "使用现有配置 | Using existing configuration"
            test_connection
            exit 0
        fi
    fi
}

# 获取用户输入 | Get User Input
get_user_input() {
    echo_title "配置 OBS 凭证 | Configure OBS Credentials"
    
    echo ""
    echo "请在 OBS Web UI 获取 API Token:"
    echo "Please get API Token from OBS Web UI:"
    echo "1. 登录 | Login: https://build.opensuse.org"
    echo "2. 点击用户名 | Click your username (top right)"
    echo "3. 选择 Settings -> API Tokens"
    echo "4. 创建新 Token | Create new token"
    echo "5. 复制 Token（只显示一次！）| Copy token (shown only once!)"
    echo ""
    
    read -p "输入 OBS 用户名 | Enter OBS username: " OBS_USERNAME_INPUT
    read -sp "输入 OBS API Token | Enter OBS API Token: " OBS_TOKEN_INPUT
    echo ""
    
    if [ -z "$OBS_USERNAME_INPUT" ] || [ -z "$OBS_TOKEN_INPUT" ]; then
        echo_error "用户名和 Token 不能为空 | Username and Token cannot be empty"
        exit 1
    fi
}

# 创建配置 | Create Configuration
create_config() {
    echo_title "创建配置文件 | Creating Configuration File"
    
    # 创建配置目录
    mkdir -p "$OBS_CONFIG_DIR"
    
    # 创建配置文件
    cat > "$OBS_CONFIG_FILE" << EOF
[general]
apiurl = https://api.opensuse.org

[https://api.opensuse.org]
user = $OBS_USERNAME_INPUT
pass = $OBS_TOKEN_INPUT
EOF
    
    # 设置权限
    chmod 600 "$OBS_CONFIG_FILE"
    
    echo_success "配置文件已创建 | Configuration file created: $OBS_CONFIG_FILE"
    echo_success "文件权限已设置为 600（仅用户可读）| File permissions set to 600 (user read-only)"
}

# 设置环境变量 | Setup Environment Variables
setup_env_vars() {
    echo_title "设置环境变量 | Setting Environment Variables"
    
    local env_file="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        env_file="$HOME/.zshrc"
    fi
    
    echo ""
    read -p "是否添加到 $env_file？| Add to $env_file? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 检查是否已存在
        if grep -q "OBS_APIURL" "$env_file" 2>/dev/null; then
            echo_warning "$env_file 中已存在 OBS 配置 | OBS config already exists in $env_file"
            read -p "是否覆盖？| Overwrite? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sed -i '/^export OBS_/d' "$env_file"
            else
                echo "跳过环境变量配置 | Skipping environment variable configuration"
                return
            fi
        fi
        
        # 添加环境变量
        cat >> "$env_file" << EOF

# OBS Expert Configuration (added by obs-expert-setup.sh)
export OBS_APIURL=https://api.opensuse.org
export OBS_USERNAME=$OBS_USERNAME_INPUT
export OBS_TOKEN=$OBS_TOKEN_INPUT
EOF
        
        echo_success "环境变量已添加到 $env_file | Environment variables added to $env_file"
        echo_warning "请运行 'source $env_file' 使配置生效 | Run 'source $env_file' to apply changes"
    fi
}

# 测试连接 | Test Connection
test_connection() {
    echo_title "测试 OBS 连接 | Testing OBS Connection"
    
    # 导出环境变量
    export OBS_APIURL=https://api.opensuse.org
    
    if [ -f "$OBS_CONFIG_FILE" ]; then
        # 从 oscrc 读取凭证
        OBS_USERNAME_INPUT=$(grep -E "^user\s*=" "$OBS_CONFIG_FILE" | head -1 | cut -d'=' -f2 | tr -d ' ')
        OBS_TOKEN_INPUT=$(grep -E "^pass\s*=" "$OBS_CONFIG_FILE" | head -1 | cut -d'=' -f2 | tr -d ' ')
        export OBS_USERNAME="$OBS_USERNAME_INPUT"
        export OBS_TOKEN="$OBS_TOKEN_INPUT"
    fi
    
    if [ -z "$OBS_USERNAME" ] || [ -z "$OBS_TOKEN" ]; then
        echo_error "未配置凭证 | Credentials not configured"
        return 1
    fi
    
    echo "正在测试认证 | Testing authentication..."
    echo "API URL: $OBS_APIURL"
    echo "Username: $OBS_USERNAME"
    
    # 使用 curl 测试
    local response
    response=$(curl -s -u "$OBS_USERNAME:$OBS_TOKEN" "$OBS_APIURL/person/$OBS_USERNAME" 2>&1)
    
    if echo "$response" | grep -q "status=\"complete\""; then
        echo_success "认证成功 | Authentication successful!"
        echo_success "欢迎，$OBS_USERNAME | Welcome, $OBS_USERNAME"
        return 0
    else
        echo_error "认证失败 | Authentication failed"
        echo "响应 | Response: $response"
        echo ""
        echo_warning "可能的原因 | Possible reasons:"
        echo "  1. 用户名或 Token 错误 | Wrong username or token"
        echo "  2. 网络连接问题 | Network connection issue"
        echo "  3. OBS API 暂时不可用 | OBS API temporarily unavailable"
        return 1
    fi
}

# 显示使用说明 | Show Usage Instructions
show_usage() {
    echo_title "使用说明 | Usage Instructions"
    
    cat << 'EOF'
恭喜！OBS Expert 已配置完成！
Congratulations! OBS Expert is now configured!

常用命令 | Common Commands:
------------------------

# 查看帮助 | View help
obs-expert --help

# 查看项目帮助 | View project help
obs-expert project --help

# 创建项目 | Create project
obs-expert project create --name "home:username:project" --title "My Project" --description "Description"

# 创建包 | Create package
obs-expert package create --project "home:username:project" --package "mypackage"

# 上传文件 | Upload file
obs-expert file upload --project "home:username:project" --package "mypackage" --file "./mypackage.spec" --message "Initial commit"

# 触发构建 | Trigger build
obs-expert build rebuild --project "home:username:project" --package "mypackage" --repository "openSUSE_Tumbleweed" --arch "x86_64"

# 创建提交请求 | Create submit request
obs-expert request create --source-project "home:username:project" --source-package "mypackage" --target-project "openSUSE:Factory" --target-package "mypackage" --description "Update"

详细文档 | Full Documentation:
----------------------------
查看 | View: /root/.openclaw/workspace-obs/skills/obs-expert/README.md
查看 | View: /root/.openclaw/workspace-obs/skills/obs-expert/SETUP.md

EOF
}

# 主函数 | Main
main() {
    echo ""
    echo_title "OBS Expert 配置向导 | OBS Expert Configuration Wizard"
    echo ""
    
    check_installation
    echo ""
    check_existing_config
    echo ""
    get_user_input
    echo ""
    create_config
    echo ""
    setup_env_vars
    echo ""
    
    if test_connection; then
        echo ""
        show_usage
        echo_success "配置完成！| Configuration complete!"
    else
        echo ""
        echo_warning "配置已保存，但连接测试失败 | Configuration saved, but connection test failed"
        echo_warning "请检查凭证后重新运行测试 | Please check credentials and re-run test"
        echo ""
        echo "运行以下命令重新测试 | Run this to re-test:"
        echo "  obs-expert auth test"
    fi
}

main "$@"
