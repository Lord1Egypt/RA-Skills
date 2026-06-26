#!/bin/bash
# one-mail 账户管理脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# 显示帮助
show_help() {
    cat << EOF
one-mail 账户管理

用法:
  bash accounts.sh list                    列出所有账户
  bash accounts.sh add                     添加新账户
  bash accounts.sh remove --name <name>    删除账户
  bash accounts.sh set-default --name <name>  设置默认账户
  bash accounts.sh test --name <name>      测试账户连接

选项:
  --name <name>    账户名称或邮箱地址
EOF
}

# 列出所有账户
list_accounts() {
    load_config
    
    echo "📧 已配置的邮箱账户:"
    echo ""
    
    local default_account=$(echo "$CONFIG" | jq -r '.default_account')
    
    echo "$CONFIG" | jq -r '.accounts[] | "\(.name) (\(.type)) - \(.email)"' | while read -r line; do
        local email=$(echo "$line" | awk -F' - ' '{print $2}')
        if [ "$email" = "$default_account" ]; then
            echo "  ✓ $line (默认)"
        else
            echo "    $line"
        fi
    done
    
    echo ""
}

# 添加账户
add_account() {
    load_config
    
    echo "添加新账户"
    echo ""
    echo "支持的邮箱类型:"
    echo "  1) Gmail"
    echo "  2) Outlook"
    echo "  3) 网易邮箱 (163.com)"
    echo "  4) 网易邮箱 (126.com)"
    echo ""
    
    read -p "选择邮箱类型 (1-4): " choice
    
    case $choice in
        1)
            echo ""
            echo "配置 Gmail 账户"
            read -p "邮箱地址: " email
            
            if ! command -v gog &> /dev/null; then
                echo "❌ 未找到 gog 命令，请先安装 gog skill"
                exit 1
            fi
            
            CONFIG=$(echo "$CONFIG" | jq --arg email "$email" \
                '.accounts += [{
                    "name": "gmail",
                    "type": "gmail",
                    "email": $email,
                    "default": false
                }]')
            
            echo "$CONFIG" > "$CONFIG_FILE"
            echo "✅ Gmail 账户已添加"
            ;;
            
        2)
            echo ""
            echo "配置 Outlook 账户"
            read -p "邮箱地址: " email
            read -p "Client ID: " client_id
            read -p "Client Secret: " client_secret
            
            echo ""
            echo "请访问以下 URL 获取授权码:"
            echo "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=$client_id&response_type=code&redirect_uri=http://localhost&scope=Mail.ReadWrite%20Mail.Send"
            echo ""
            read -p "授权码: " auth_code
            
            token_response=$(curl -s -X POST \
                "https://login.microsoftonline.com/common/oauth2/v2.0/token" \
                -d "client_id=$client_id" \
                -d "client_secret=$client_secret" \
                -d "code=$auth_code" \
                -d "redirect_uri=http://localhost" \
                -d "grant_type=authorization_code")
            
            refresh_token=$(echo "$token_response" | jq -r '.refresh_token')
            
            if [ "$refresh_token" = "null" ]; then
                echo "❌ 获取 refresh token 失败"
                echo "$token_response"
                exit 1
            fi
            
            CONFIG=$(echo "$CONFIG" | jq --arg email "$email" --arg client_id "$client_id" \
                '.accounts += [{
                    "name": "outlook",
                    "type": "outlook",
                    "email": $email,
                    "client_id": $client_id,
                    "default": false
                }]')
            
            echo "$CONFIG" > "$CONFIG_FILE"
            
            local new_creds=$(jq -n \
                --arg client_secret "$client_secret" \
                --arg refresh_token "$refresh_token" \
                '{
                    "client_secret": $client_secret,
                    "refresh_token": $refresh_token
                }')
            
            save_credentials "outlook" "" "$new_creds"
            
            echo "✅ Outlook 账户已添加"
            ;;
            
        3)
            echo ""
            echo "配置网易邮箱账户"
            read -p "邮箱地址: " email
            read -s -p "应用专用密码: " password
            echo ""
            
            CONFIG=$(echo "$CONFIG" | jq --arg email "$email" \
                '.accounts += [{
                    "name": "163",
                    "type": "163",
                    "email": $email,
                    "imap_server": "imap.163.com",
                    "smtp_server": "smtp.163.com",
                    "default": false
                }]')
            
            echo "$CONFIG" > "$CONFIG_FILE"
            
            local new_creds=$(jq -n --arg password "$password" '{"password": $password}')
            save_credentials "163" "$email" "$new_creds"
            
            echo "✅ 网易邮箱账户已添加"
            ;;
            
        4)
            echo ""
            echo "配置网易 126 邮箱账户"
            read -p "邮箱地址: " email
            read -s -p "应用专用密码: " password
            echo ""
            
            CONFIG=$(echo "$CONFIG" | jq --arg email "$email" \
                '.accounts += [{
                    "name": "126",
                    "type": "126",
                    "email": $email,
                    "imap_server": "imap.126.com",
                    "smtp_server": "smtp.126.com",
                    "default": false
                }]')
            
            echo "$CONFIG" > "$CONFIG_FILE"
            
            local new_creds=$(jq -n --arg password "$password" '{"password": $password}')
            save_credentials "126" "$email" "$new_creds"
            
            echo "✅ 网易 126 邮箱账户已添加"
            ;;
            
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
}

# 删除账户
remove_account() {
    local name="$1"
    
    if [ -z "$name" ]; then
        echo "❌ 缺少账户名称 (--name)" >&2
        exit 1
    fi
    
    load_config
    
    local account=$(echo "$CONFIG" | jq -r --arg name "$name" '.accounts[] | select(.email == $name or .name == $name)')
    if [ -z "$account" ]; then
        echo "❌ 账户不存在: $name" >&2
        exit 1
    fi
    
    local email=$(echo "$account" | jq -r '.email')
    
    read -p "确认删除账户 $email? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        echo "取消删除"
        exit 0
    fi
    
    CONFIG=$(echo "$CONFIG" | jq --arg email "$email" '.accounts = [.accounts[] | select(.email != $email)]')
    echo "$CONFIG" > "$CONFIG_FILE"
    
    echo "✅ 账户已删除: $email"
}

# 设置默认账户
set_default() {
    local name="$1"
    
    if [ -z "$name" ]; then
        echo "❌ 缺少账户名称 (--name)" >&2
        exit 1
    fi
    
    load_config
    
    local account=$(echo "$CONFIG" | jq -r --arg name "$name" '.accounts[] | select(.email == $name or .name == $name)')
    if [ -z "$account" ]; then
        echo "❌ 账户不存在: $name" >&2
        exit 1
    fi
    
    local email=$(echo "$account" | jq -r '.email')
    
    CONFIG=$(echo "$CONFIG" | jq --arg email "$email" '.default_account = $email')
    echo "$CONFIG" > "$CONFIG_FILE"
    
    echo "✅ 默认账户已设置: $email"
}

# 测试账户连接
test_account() {
    local name="$1"
    
    if [ -z "$name" ]; then
        echo "❌ 缺少账户名称 (--name)" >&2
        exit 1
    fi
    
    load_config
    
    local account=$(echo "$CONFIG" | jq -r --arg name "$name" '.accounts[] | select(.email == $name or .name == $name)')
    if [ -z "$account" ]; then
        echo "❌ 账户不存在: $name" >&2
        exit 1
    fi
    
    local account_type=$(echo "$account" | jq -r '.type')
    local email=$(echo "$account" | jq -r '.email')
    
    echo "测试账户连接: $email ($account_type)"
    
    case $account_type in
        gmail)
            if gog gmail list --limit 1 &> /dev/null; then
                echo "✅ Gmail 连接正常"
            else
                echo "❌ Gmail 连接失败"
                exit 1
            fi
            ;;
        outlook)
            source "$SCRIPT_DIR/lib/outlook.sh"
            if get_outlook_token "$account" &> /dev/null; then
                echo "✅ Outlook 连接正常"
            else
                echo "❌ Outlook 连接失败"
                exit 1
            fi
            ;;
        163|126)
            echo "⚠️  网易邮箱连接测试暂未实现"
            ;;
        *)
            echo "❌ 不支持的账户类型: $account_type"
            exit 1
            ;;
    esac
}

# 主函数
main() {
    local action="$1"
    shift
    
    case $action in
        list)
            list_accounts
            ;;
        add)
            add_account
            ;;
        remove)
            local name=""
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --name)
                        name="$2"
                        shift 2
                        ;;
                    *)
                        echo "未知参数: $1"
                        exit 1
                        ;;
                esac
            done
            remove_account "$name"
            ;;
        set-default)
            local name=""
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --name)
                        name="$2"
                        shift 2
                        ;;
                    *)
                        echo "未知参数: $1"
                        exit 1
                        ;;
                esac
            done
            set_default "$name"
            ;;
        test)
            local name=""
            while [[ $# -gt 0 ]]; do
                case $1 in
                    --name)
                        name="$2"
                        shift 2
                        ;;
                    *)
                        echo "未知参数: $1"
                        exit 1
                        ;;
                esac
            done
            test_account "$name"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "❌ 未知操作: $action"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
