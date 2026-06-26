#!/bin/bash
# one-mail 初始化配置脚本

set -e

CONFIG_DIR="$HOME/.onemail"
CONFIG_FILE="$CONFIG_DIR/config.json"
CREDS_FILE="$CONFIG_DIR/credentials.json"

echo "🔧 one-mail 初始化配置"
echo ""

# 创建配置目录
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

# 检查是否已有配置
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件已存在: $CONFIG_FILE"
    read -p "是否覆盖? (y/N): " confirm
    if [ "$confirm" != "y" ]; then
        echo "取消配置"
        exit 0
    fi
fi

# 初始化配置
cat > "$CONFIG_FILE" << 'EOF'
{
  "accounts": [],
  "default_account": null
}
EOF

# 初始化凭证文件
cat > "$CREDS_FILE" << 'EOF'
{
  "gmail": {},
  "outlook": {},
  "163": {},
  "126": {}
}
EOF

chmod 600 "$CREDS_FILE"

echo "✅ 配置文件已创建: $CONFIG_FILE"
echo ""

# 添加账户
echo "📧 添加邮箱账户"
echo ""
echo "支持的邮箱类型:"
echo "  1) Gmail"
echo "  2) Outlook"
echo "  3) 网易邮箱 (163.com)"
echo "  4) 网易邮箱 (126.com)"
echo ""

while true; do
    read -p "选择邮箱类型 (1-4, 或按 Enter 跳过): " choice
    
    if [ -z "$choice" ]; then
        break
    fi
    
    case $choice in
        1)
            echo ""
            echo "配置 Gmail 账户"
            read -p "邮箱地址: " email
            
            # 检查 gog 是否已配置
            if ! command -v gog &> /dev/null; then
                echo "❌ 未找到 gog 命令，请先安装 gog skill"
                continue
            fi
            
            # 添加到配置
            jq --arg email "$email" \
               '.accounts += [{
                   "name": "gmail",
                   "type": "gmail",
                   "email": $email,
                   "default": (.accounts | length == 0)
               }]' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
            mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            
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
            
            # 获取 refresh token
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
                continue
            fi
            
            # 添加到配置
            jq --arg email "$email" \
               --arg client_id "$client_id" \
               '.accounts += [{
                   "name": "outlook",
                   "type": "outlook",
                   "email": $email,
                   "client_id": $client_id,
                   "default": (.accounts | length == 0)
               }]' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
            mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            
            # 保存凭证
            jq --arg client_secret "$client_secret" \
               --arg refresh_token "$refresh_token" \
               '.outlook = {
                   "client_secret": $client_secret,
                   "refresh_token": $refresh_token
               }' "$CREDS_FILE" > "$CREDS_FILE.tmp"
            mv "$CREDS_FILE.tmp" "$CREDS_FILE"
            
            echo "✅ Outlook 账户已添加"
            ;;
            
        3)
            echo ""
            echo "配置网易邮箱账户"
            read -p "邮箱地址: " email
            read -s -p "应用专用密码: " password
            echo ""
            
            # 添加到配置
            jq --arg email "$email" \
               '.accounts += [{
                   "name": "163",
                   "type": "163",
                   "email": $email,
                   "imap_server": "imap.163.com",
                   "smtp_server": "smtp.163.com",
                   "default": (.accounts | length == 0)
               }]' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
            mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            
            # 保存凭证
            jq --arg email "$email" \
               --arg password "$password" \
               '.["163"][$email] = {
                   "password": $password
               }' "$CREDS_FILE" > "$CREDS_FILE.tmp"
            mv "$CREDS_FILE.tmp" "$CREDS_FILE"
            
            echo "✅ 网易邮箱账户已添加"
            ;;
            
        4)
            echo ""
            echo "配置网易 126 邮箱账户"
            read -p "邮箱地址: " email
            read -s -p "应用专用密码: " password
            echo ""
            
            # 添加到配置
            jq --arg email "$email" \
               '.accounts += [{
                   "name": "126",
                   "type": "126",
                   "email": $email,
                   "imap_server": "imap.126.com",
                   "smtp_server": "smtp.126.com",
                   "default": (.accounts | length == 0)
               }]' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
            mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            
            # 保存凭证
            jq --arg email "$email" \
               --arg password "$password" \
               '.["126"][$email] = {
                   "password": $password
               }' "$CREDS_FILE" > "$CREDS_FILE.tmp"
            mv "$CREDS_FILE.tmp" "$CREDS_FILE"
            
            echo "✅ 网易 126 邮箱账户已添加"
            ;;
            
        *)
            echo "❌ 无效选择"
            ;;
    esac
    
    echo ""
done

# 设置默认账户
if [ "$(jq '.accounts | length' "$CONFIG_FILE")" -gt 0 ]; then
    default_email=$(jq -r '.accounts[0].email' "$CONFIG_FILE")
    jq --arg email "$default_email" \
       '.default_account = $email' "$CONFIG_FILE" > "$CONFIG_FILE.tmp"
    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo "✅ 默认账户: $default_email"
fi

echo ""
echo "🎉 配置完成！"
echo ""
echo "使用方法:"
echo "  收取邮件: bash ~/clawd/skills/one-mail/fetch.sh"
echo "  发送邮件: bash ~/clawd/skills/one-mail/send.sh --to recipient@example.com --subject 'Hello' --body 'Content'"
echo "  账户管理: bash ~/clawd/skills/one-mail/accounts.sh list"
