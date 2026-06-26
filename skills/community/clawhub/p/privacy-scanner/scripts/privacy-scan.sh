#!/bin/bash
# Privacy Scanner - 发布前隐私扫描
# 扫描代码中是否包含敏感信息，防止隐私数据泄露

set -uo pipefail

# ==================== 配置 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN_DIR="${1:-.}"
STRICT_MODE=false
EXIT_CODE=0
CURRENT_USER=$(whoami)
CURRENT_HOST=$(hostname)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 计数器
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

# ==================== 解析参数 ====================
for arg in "$@"; do
    case "$arg" in
        --strict) STRICT_MODE=true ;;
        -h|--help)
            echo "用法: $0 [--strict] [扫描目录]"
            echo "  --strict  发现问题即返回非零退出码"
            exit 0
            ;;
    esac
done

# 如果第一个参数是目录（不是选项），设为扫描目录
if [ -d "$1" ] 2>/dev/null; then
    SCAN_DIR="$1"
elif [ "$1" = "--strict" ]; then
    SCAN_DIR="${2:-.}"
fi

if [ ! -d "$SCAN_DIR" ]; then
    echo -e "${RED}❌ 目录不存在: $SCAN_DIR${NC}"
    exit 1
fi

# ==================== 工具函数 ====================
print_header() {
    echo ""
    echo -e "${CYAN}${BOLD}━━━ $1 ━━━${NC}"
}

pass() {
    echo -e "  ${GREEN}✅${NC} $1"
    ((PASS_COUNT++)) || true
}

warn() {
    echo -e "  ${YELLOW}⚠️${NC}  $1"
    ((WARN_COUNT++)) || true
    [ "$STRICT_MODE" = true ] && EXIT_CODE=1
}

fail() {
    echo -e "  ${RED}❌${NC} $1"
    ((FAIL_COUNT++)) || true
    EXIT_CODE=1
}

# 跳过规则
should_skip() {
    local path="$1"
    # 跳过目录
    for skip_dir in node_modules .git backups logs agents extensions browser; do
        [[ "$path" == *"/$skip_dir/"* ]] && return 0
        [[ "$path" == *"/$skip_dir" ]] && return 0
    done
    # 跳过文件
    for skip_file in *.log *.tmp *.bak *.sqlite *.db *.png *.jpg *.jpeg *.gif *.zip *.tar *.gz *.ico; do
        [[ "$path" == *$skip_file ]] && return 0
    done
    return 1
}

# grep 扫描（排除跳过的路径）
scan() {
    local pattern="$1"
    local desc="$2"
    local exclude_placeholder="${3:-}"
    
    local results
    if [ -n "$exclude_placeholder" ]; then
        results=$(grep -rn --include="*.sh" --include="*.md" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.ts" --include="*.js" --include="*.plist" \
            "$pattern" "$SCAN_DIR" 2>/dev/null | grep -v "$exclude_placeholder" | head -5 || true)
    else
        results=$(grep -rn --include="*.sh" --include="*.md" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.ts" --include="*.js" --include="*.plist" \
            "$pattern" "$SCAN_DIR" 2>/dev/null | head -5 || true)
    fi
    
    echo "$results"
}

# ==================== 扫描项 ====================

echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       🔍 Privacy Scanner - 隐私扫描              ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo "扫描目录: $(cd "$SCAN_DIR" && pwd)"
echo "严格模式: $STRICT_MODE"

# 1. Webhook URL
print_header "1. Webhook URL"
results=$(scan "hook/[a-f0-9]\{20,\}" "真实 webhook" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实 Webhook URL:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 Webhook URL"
fi

# 2. 飞书 ID
print_header "2. 飞书 ID (ou_/oc_/om_)"
results=$(scan "ou_[a-z0-9]\{20,\}\|oc_[a-z0-9]\{20,\}\|om_[a-z0-9]\{20,\}" "飞书 ID" "YOUR_\|PLACEHOLDER\|EXAMPLE\|xxx\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实飞书 ID:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实飞书 ID"
fi

# 3. 用户名路径
print_header "3. 用户名路径"
# 排除文档中的示例路径（/Users/xxx, /home/alice 等虚构用户名）
results=$(scan "/Users/[a-zA-Z0-9_-]\+\|/home/[a-zA-Z0-9_-]\+" "用户名路径" \
    "__USER_HOME__\|\$HOME\|~\|/Users/xxx\|/Users/john\|/Users/alice\|/Users/bob\|/home/xxx\|/home/user\|/home/alice")
if [ -n "$results" ]; then
    # 过滤掉文件路径本身包含用户名的情况（只看内容）
    filtered=$(echo "$results" | grep -v "^$SCAN_DIR" | grep -v "README.md\|SKILL.md.*用户" | head -5 || true)
    if [ -n "$filtered" ]; then
        fail "发现硬编码用户名路径:"
        echo "$filtered" | while IFS= read -r line; do echo "    $line"; done
    else
        pass "无硬编码用户名路径（文档中的示例路径已跳过）"
    fi
else
    pass "无硬编码用户名路径"
fi

# 4. API Token / Key
print_header "4. API Token / Key"
results=$(scan "sk-[a-zA-Z0-9]\{20,\}\|ghp_[a-zA-Z0-9]\{30,\}\|xoxb-[a-zA-Z0-9]\|gho_[a-zA-Z0-9]\{30,\}\|AKIA[A-Z0-9]\{16,\}" "API Key" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实 API Key:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 API Key"
fi

# 5. Bearer Token
print_header "5. Bearer Token"
results=$(scan "Bearer [a-zA-Z0-9_-]\{20,\}" "Bearer Token" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实 Bearer Token:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 Bearer Token"
fi

# 6. 内网 IP
print_header "6. 内网 IP 地址"
results=$(scan "192\.168\.[0-9]\{1,3\}\.[0-9]\{1,3\}\|10\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\|172\.1[6-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\|172\.2[0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\|172\.3[0-1]\.[0-9]\{1,3\}\.[0-9]\{1,3\}" "内网 IP")
if [ -n "$results" ]; then
    warn "发现内网 IP 地址（通常无害，确认是否应公开）:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无内网 IP 地址"
fi

# 7. 邮箱地址
print_header "7. 邮箱地址"
results=$(scan "[a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}" "邮箱" "example\.com\|your_\|PLACEHOLDER\|noreply\|openclaw@local\|user@domain\|test@\|admin@localhost")
if [ -n "$results" ]; then
    warn "发现疑似真实邮箱地址:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实邮箱地址"
fi

# 8. 手机号（中国大陆）
print_header "8. 手机号"
results=$(scan "1[3-9][0-9]\{9\}" "手机号")
if [ -n "$results" ]; then
    fail "发现疑似手机号:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无手机号"
fi

# 9. 敏感文件
print_header "9. 敏感文件"
sensitive_found=false
for file in ".env" "credentials.json" "secrets.json" "id_rsa" "id_ed25519" ".pem" ".key" ".p12" ".pfx"; do
    matches=$(find "$SCAN_DIR" -name "*$file*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null || true)
    if [ -n "$matches" ]; then
        fail "发现敏感文件: $file"
        echo "$matches" | while IFS= read -r line; do echo "    $line"; done
        sensitive_found=true
    fi
done
[ "$sensitive_found" = false ] && pass "无敏感文件"

# 10. 密码/secret 硬编码
print_header "10. 密码/Secret 硬编码"
results=$(scan "password\s*=\s*['\"][^'\"]\{8,\}\|secret\s*=\s*['\"][^'\"]\{8,\}\|PASSWORD\s*=\s*['\"][^'\"]\{8,\}\|SECRET\s*=\s*['\"][^'\"]\{8,\}" "密码/secret" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_\|password123\|changeme")
if [ -n "$results" ]; then
    fail "发现疑似硬编码密码/secret:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无硬编码密码/secret"
fi

# 11. Discord Webhook
print_header "11. Discord Webhook"
results=$(scan "discord\.com/api/webhooks/\|discordapp\.com/api/webhooks/" "Discord Webhook" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_\|│\||")
if [ -n "$results" ]; then
    fail "发现疑似真实 Discord Webhook:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 Discord Webhook"
fi

# 12. Slack Webhook
print_header "12. Slack Webhook"
results=$(scan "hooks\.slack\.com/services/" "Slack Webhook" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_\|│\||")
if [ -n "$results" ]; then
    fail "发现疑似真实 Slack Webhook:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 Slack Webhook"
fi

# 13. Telegram Bot Token
print_header "13. Telegram Bot Token"
results=$(scan "[0-9]\{8,10\}:[a-zA-Z0-9_-]\{35,\}" "Telegram Bot Token" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_\|1234567890")
if [ -n "$results" ]; then
    fail "发现疑似真实 Telegram Bot Token:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 Telegram Bot Token"
fi

# 14. Discord/Telegram 数字 ID
print_header "14. Discord/Telegram 数字 ID"
# Discord snowflake: 17-19 digits; Telegram chat ID: starts with -100
results=$(scan "[0-9]\{17,19\}\|-100[0-9]\{10,\}" "数字 ID" "hook\|pid\|port\|StartInterval\|18789\|YOUR_\|PLACEHOLDER")
if [ -n "$results" ]; then
    warn "发现疑似 Discord/Telegram 数字 ID（需人工确认）:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无 Discord/Telegram 数字 ID"
fi

# 15. JWT Token
print_header "15. JWT Token"
results=$(scan "eyJ[a-zA-Z0-9_-]\{20,\}\.eyJ[a-zA-Z0-9_-]\{20,\}" "JWT Token" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实 JWT Token:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实 JWT Token"
fi

# 16. SSH Private Key
print_header "16. SSH 私钥"
results=$(scan "-----BEGIN.*PRIVATE KEY-----" "SSH 私钥")
if [ -n "$results" ]; then
    fail "发现 SSH 私钥内容:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无 SSH 私钥"
fi

# 17. 数据库连接字符串
print_header "17. 数据库连接字符串"
results=$(scan "mongodb://\|postgresql://\|mysql://\|redis://" "数据库连接" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_\|localhost\|127\.0\.0\.1\|│\||")
if [ -n "$results" ]; then
    fail "发现疑似真实数据库连接字符串:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实数据库连接字符串"
fi

# 18. OpenAI/Anthropic/Stripe API Key
print_header "18. 第三方 API Key"
results=$(scan "sk-proj-[a-zA-Z0-9]\{20,\}\|sk-ant-[a-zA-Z0-9]\{20,\}\|sk_live_[a-zA-Z0-9]\{20,\}\|pk_live_[a-zA-Z0-9]\{20,\}\|AIza[a-zA-Z0-9_-]\{35,\}\|ghs_[a-zA-Z0-9]\{30,\}\|ghu_[a-zA-Z0-9]\{30,\}\|ghr_[a-zA-Z0-9]\{30,\}" "第三方 API Key" "YOUR_\|PLACEHOLDER\|EXAMPLE\|your_")
if [ -n "$results" ]; then
    fail "发现疑似真实第三方 API Key:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无真实第三方 API Key"
fi

# 19. 主机名/机器名
print_header "19. 主机名/机器名"
results=$(scan "$CURRENT_HOST" "主机名")
if [ -n "$results" ]; then
    warn "发现当前主机名 '$CURRENT_HOST'（可能无害，确认是否应公开）:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无主机名泄露"
fi

# 20. 公网 IP 地址
print_header "20. 公网 IP 地址"
# 排除 127.x, 192.168.x, 10.x, 172.16-31.x, 0.0.0.0, 255.255.255.x
results=$(scan "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}" "公网 IP" \
    "127\.\|192\.168\.\|10\.\|172\.1[6-9]\.\|172\.2[0-9]\.\|172\.3[0-1]\.\|0\.0\.0\.0\|255\.255\.255\.\|1\.1\.1\.1\|8\.8\.8\.\|YOUR_\|PLACEHOLDER")
if [ -n "$results" ]; then
    warn "发现疑似公网 IP（需人工确认是否为示例）:"
    echo "$results" | while IFS= read -r line; do echo "    $line"; done
else
    pass "无公网 IP 地址"
fi

# ==================== 总结 ====================
print_header "扫描结果"
echo ""
echo -e "  ${GREEN}✅ 通过: $PASS_COUNT${NC}"
echo -e "  ${YELLOW}⚠️  警告: $WARN_COUNT${NC}"
echo -e "  ${RED}❌ 失败: $FAIL_COUNT${NC}"
echo ""

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo -e "${RED}${BOLD}❌ 扫描未通过，发现 $FAIL_COUNT 项严重问题${NC}"
    echo -e "${RED}   请修复后再发布！${NC}"
elif [ "$WARN_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}${BOLD}⚠️  扫描通过，但有 $WARN_COUNT 项警告需人工确认${NC}"
else
    echo -e "${GREEN}${BOLD}✅ 扫描全部通过，可以安全发布！${NC}"
fi

echo ""
exit $EXIT_CODE
