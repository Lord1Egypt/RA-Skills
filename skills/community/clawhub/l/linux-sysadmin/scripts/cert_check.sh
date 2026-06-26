#!/usr/bin/env bash
# cert_check.sh — 证书过期检查脚本
# 支持：远程域名检查、本地证书文件检查、Let's Encrypt 状态检查
# 注意：本脚本使用 GNU date（date -d），仅支持 Linux 系统，macOS/BSD 不兼容
# 用法:
#   bash scripts/cert_check.sh                          — 检查预置域名列表
#   bash scripts/cert_check.sh example.com api.example.com  — 检查指定域名
#   bash scripts/cert_check.sh --file /path/to/cert.pem     — 检查本地证书
#   bash scripts/cert_check.sh --letsencrypt                 — 检查 Let's Encrypt 证书

WARN_DAYS="${CERT_WARN_DAYS:-30}"
CRIT_DAYS="${CERT_CRIT_DAYS:-7}"

# 参数解析（优先处理 --help/--version）
case "${1:-}" in
    --help|-h)
        echo "用法: bash $0 [OPTIONS] [DOMAIN...]"
        echo ""
        echo "证书过期检查：支持远程域名、本地文件、Let's Encrypt 状态检查。"
        echo ""
        echo "选项:"
        echo "  --file FILE           检查本地证书文件"
        echo "  --letsencrypt         检查 Let's Encrypt 证书"
        echo "  --warn-days DAYS      警告阈值天数（默认: 30）"
        echo "  --crit-days DAYS      严重阈值天数（默认: 7）"
        echo "  --help, -h            显示此帮助信息"
        echo "  --version             显示版本信息"
        echo ""
        echo "示例:"
        echo "  $0 example.com api.example.com"
        echo "  $0 --file /etc/ssl/certs/server.crt"
        echo "  $0 --letsencrypt"
        echo "  $0 example.com:8443"
        exit 0
        ;;
    --version)
        echo "cert_check.sh v3.0.2"
        exit 0
        ;;
esac

# 颜色（非终端环境自动禁用，避免转义码泄露）
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' NC=''
fi

TOTAL=0
PASS=0
WARN=0
FAIL=0

check_remote_cert() {
    local host="$1"
    local port="${2:-443}"
    TOTAL=$((TOTAL + 1))

    # 获取证书信息
    local cert_info
    cert_info=$(echo | timeout 10 openssl s_client -connect "${host}:${port}" -servername "$host" 2>/dev/null)

    if [ -z "$cert_info" ]; then
        echo -e "  ${RED}❌${NC} ${host}:${port} — 无法连接或获取证书"
        FAIL=$((FAIL + 1))
        return 1
    fi

    # 提取过期时间
    local expiry
    expiry=$(echo "$cert_info" | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -z "$expiry" ]; then
        echo -e "  ${RED}❌${NC} ${host}:${port} — 无法解析证书"
        FAIL=$((FAIL + 1))
        return 1
    fi

    local expiry_ts now_ts days_left
    expiry_ts=$(date -d "$expiry" +%s 2>/dev/null)
    now_ts=$(date +%s)
    days_left=$(( (expiry_ts - now_ts) / 86400 ))

    # 提取颁发者和主题
    local subject issuer san
    subject=$(echo "$cert_info" | openssl x509 -noout -subject 2>/dev/null | sed 's/subject=//')
    issuer=$(echo "$cert_info" | openssl x509 -noout -issuer 2>/dev/null | sed 's/issuer=//' | sed 's/.*CN = //')
    san=$(echo "$cert_info" | openssl x509 -noout -ext subjectAltName 2>/dev/null | grep -o "DNS:[^,]*" | head -5 | tr '\n' ' ')

    # 输出结果
    if [ "$days_left" -lt 0 ]; then
        echo -e "  ${RED}❌ 已过期${NC} ${host}:${port}"
        echo -e "     过期时间: ${expiry}（已过期 ${days_left#-} 天）"
        FAIL=$((FAIL + 1))
    elif [ "$days_left" -lt "$CRIT_DAYS" ]; then
        echo -e "  ${RED}❌ 即将过期${NC} ${host}:${port}"
        echo -e "     剩余: ${days_left} 天（过期时间: ${expiry}）"
        FAIL=$((FAIL + 1))
    elif [ "$days_left" -lt "$WARN_DAYS" ]; then
        echo -e "  ${YELLOW}⚠️  即将过期${NC} ${host}:${port}"
        echo -e "     剩余: ${days_left} 天（过期时间: ${expiry}）"
        WARN=$((WARN + 1))
    else
        echo -e "  ${GREEN}✅${NC} ${host}:${port} — ${days_left} 天后过期"
        PASS=$((PASS + 1))
    fi
    echo -e "     颁发者: ${issuer}"
    [ -n "$san" ] && echo -e "     SAN: ${san}"
}

check_local_cert() {
    local cert_file="$1"
    TOTAL=$((TOTAL + 1))

    if [ ! -f "$cert_file" ]; then
        echo -e "  ${RED}❌${NC} ${cert_file} — 文件不存在"
        FAIL=$((FAIL + 1))
        return 1
    fi

    local expiry
    expiry=$(openssl x509 -in "$cert_file" -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -z "$expiry" ]; then
        echo -e "  ${RED}❌${NC} ${cert_file} — 无法解析证书"
        FAIL=$((FAIL + 1))
        return 1
    fi

    local expiry_ts now_ts days_left
    expiry_ts=$(date -d "$expiry" +%s 2>/dev/null)
    now_ts=$(date +%s)
    days_left=$(( (expiry_ts - now_ts) / 86400 ))

    local subject
    subject=$(openssl x509 -in "$cert_file" -noout -subject 2>/dev/null | sed 's/subject=//')

    if [ "$days_left" -lt 0 ]; then
        echo -e "  ${RED}❌ 已过期${NC} ${cert_file}"
        echo -e "     ${subject}"
        FAIL=$((FAIL + 1))
    elif [ "$days_left" -lt "$WARN_DAYS" ]; then
        echo -e "  ${YELLOW}⚠️  ${days_left} 天后过期${NC} ${cert_file}"
        echo -e "     ${subject}"
        WARN=$((WARN + 1))
    else
        echo -e "  ${GREEN}✅${NC} ${cert_file} — ${days_left} 天后过期"
        PASS=$((PASS + 1))
    fi
}

check_letsencrypt() {
    local le_dir="/etc/letsencrypt/live"
    if [ ! -d "$le_dir" ]; then
        echo -e "  ${YELLOW}⚠️${NC} Let's Encrypt 目录不存在: $le_dir"
        return
    fi

    echo -e "  ${CYAN}--- Let's Encrypt 证书 ---${NC}"

    for cert_dir in "$le_dir"/*/; do
        [ -d "$cert_dir" ] || continue
        local domain
        domain=$(basename "$cert_dir")
        local cert_file="${cert_dir}fullchain.pem"

        if [ -f "$cert_file" ]; then
            check_local_cert "$cert_file"
        fi
    done

    echo ""
    echo -e "  ${CYAN}--- Certbot 续期状态 ---${NC}"
    if command -v certbot &>/dev/null; then
        certbot certificates 2>/dev/null | grep -E "Domains:|Expiry Date:" | while read -r line; do
            echo "    $line"
        done

        # 检查自动续期 timer
        if systemctl is-active certbot.timer &>/dev/null; then
            echo -e "  ${GREEN}✅${NC} certbot.timer 已启用"
        elif systemctl is-active snap.certbot.renew.timer &>/dev/null; then
            echo -e "  ${GREEN}✅${NC} snap.certbot.renew.timer 已启用"
        elif crontab -l 2>/dev/null | grep -q certbot; then
            echo -e "  ${GREEN}✅${NC} certbot cron 任务已配置"
        else
            echo -e "  ${YELLOW}⚠️${NC} 未检测到自动续期配置"
        fi
    else
        echo -e "  ${YELLOW}⚠️${NC} certbot 未安装"
    fi
}

# ==================== 主入口 ====================
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          证书过期检查报告                                   ║"
echo "║          检查时间: $(date '+%Y-%m-%d %H:%M:%S')                     ║"
echo "║          警告阈值: ${WARN_DAYS} 天 | 严重阈值: ${CRIT_DAYS} 天        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

if [ $# -eq 0 ]; then
    # 无参数：检查 Let's Encrypt + 本地证书
    echo "=== Let's Encrypt 证书 ==="
    check_letsencrypt
    echo ""

    # 检查常见位置的证书文件
    echo "=== 本地证书文件 ==="
    for cert_path in /etc/ssl/certs /etc/nginx/ssl /etc/pki/tls/certs; do
        if [ -d "$cert_path" ]; then
            find "$cert_path" -maxdepth 2 -name "*.crt" -o -name "*.pem" 2>/dev/null | while read -r f; do
                # 跳过 CA 证书和符号链接
                [ -L "$f" ] && continue
                openssl x509 -in "$f" -noout 2>/dev/null || continue
                # 只检查服务器证书（非 CA）
                is_ca=$(openssl x509 -in "$f" -noout -ext basicConstraints 2>/dev/null | grep "CA:TRUE")
                [ -n "$is_ca" ] && continue
                check_local_cert "$f"
            done
        fi
    done
else
    # 有参数：按参数类型处理
    while [ $# -gt 0 ]; do
        case "$1" in
            --file)
                shift
                echo "=== 本地证书检查 ==="
                check_local_cert "$1"
                shift
                ;;
            --letsencrypt)
                echo "=== Let's Encrypt 证书 ==="
                check_letsencrypt
                shift
                ;;
            --warn-days)
                shift
                WARN_DAYS="$1"
                shift
                ;;
            --crit-days)
                shift
                CRIT_DAYS="$1"
                shift
                ;;
            *)
                # 域名检查
                echo "=== 远程证书检查 ==="
                for domain in "$@"; do
                    # 支持 host:port 格式
                    if [[ "$domain" == *:* ]]; then
                        host="${domain%%:*}"
                        port="${domain##*:}"
                        check_remote_cert "$host" "$port"
                    else
                        check_remote_cert "$domain"
                    fi
                done
                break
                ;;
        esac
    done
fi

# ==================== 汇总 ====================
echo ""
echo "================================================================"
echo "  检查汇总"
echo "================================================================"
echo "  总计: $TOTAL 个证书"
echo -e "  ${GREEN}✅ 正常${NC}: $PASS"
echo -e "  ${YELLOW}⚠️  警告${NC}: $WARN"
echo -e "  ${RED}❌ 失败${NC}: $FAIL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo -e "  ${RED}⚠️  发现 $FAIL 个证书问题，请尽快处理${NC}"
    exit 1
elif [ "$WARN" -gt 0 ]; then
    echo -e "  ${YELLOW}👍 无严重问题，建议关注即将过期的证书${NC}"
    exit 0
else
    echo -e "  ${GREEN}🎉 所有证书状态正常${NC}"
    exit 0
fi
