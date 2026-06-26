#!/bin/bash
# OpenClaw Security Deployment Checklist
# 部署前安全检查脚本 - 可逐项执行并生成报告

# 移除 set -e，允许检查继续执行即使某些项失败
# set -e

# 颜色输出（支持 --no-color 参数禁用）
if [[ "$1" == "--no-color" || -n "$NO_COLOR" ]]; then
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
else
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
fi

# 检查结果计数
PASS=0
WARN=0
FAIL=0

# 打印检查结果
print_result() {
    local status=$1
    local item=$2
    local details=$3
    
    case $status in
        "PASS")
            echo -e "${GREEN}✓${NC} $item"
            ((PASS++))
            ;;
        "WARN")
            echo -e "${YELLOW}⚠${NC} $item"
            [[ -n "$details" ]] && echo -e "  ${BLUE}→${NC} $details"
            ((WARN++))
            ;;
        "FAIL")
            echo -e "${RED}✗${NC} $item"
            [[ -n "$details" ]] && echo -e "  ${RED}→${NC} $details"
            ((FAIL++))
            ;;
    esac
}

# 分隔线
section() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

# 检查防火墙状态
check_firewall() {
    section "🔥 防火墙配置"
    
    if command -v ufw &> /dev/null; then
        if ufw status | grep -q "Status: active"; then
            print_result "PASS" "UFW 防火墙已启用"
        else
            print_result "WARN" "UFW 防火墙未启用" "建议运行：sudo ufw enable"
        fi
    elif command -v firewall-cmd &> /dev/null; then
        if firewall-cmd --state | grep -q "running"; then
            print_result "PASS" "firewalld 已启用"
        else
            print_result "WARN" "firewalld 未启用"
        fi
    elif command -v pfctl &> /dev/null; then
        if pfctl -sr 2>/dev/null | grep -q "anchor"; then
            print_result "PASS" "macOS 防火墙已配置"
        else
            print_result "WARN" "macOS 防火墙未配置" "建议在系统偏好设置中启用"
        fi
    else
        print_result "WARN" "未检测到防火墙工具" "建议安装 ufw 或配置 iptables"
    fi
    
    # 检查 OpenClaw 端口
    if netstat -tlnp 2>/dev/null | grep -q ":7001\|:7002"; then
        print_result "WARN" "OpenClaw 端口已开放" "确保防火墙规则限制了访问来源"
    fi
}

# 检查 SSH 配置
check_ssh() {
    section "🔐 SSH 安全配置"
    
    if [[ -f /etc/ssh/sshd_config ]]; then
        # 检查是否允许 root 登录
        if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config; then
            print_result "PASS" "禁止 root 登录"
        elif grep -q "^PermitRootLogin prohibit-password"; then
            print_result "WARN" "root 仅限密钥登录" "建议完全禁止：PermitRootLogin no"
        else
            print_result "FAIL" "root 登录未限制" "建议设置：PermitRootLogin no"
        fi
        
        # 检查密码认证
        if grep -q "^PasswordAuthentication no" /etc/ssh/sshd_config; then
            print_result "PASS" "禁用密码认证（仅密钥）"
        else
            print_result "WARN" "密码认证未禁用" "建议改用 SSH 密钥并禁用密码"
        fi
        
        # 检查端口
        if grep -q "^Port 22$" /etc/ssh/sshd_config; then
            print_result "WARN" "使用默认 SSH 端口 22" "建议改为非标准端口减少扫描"
        else
            PORT=$(grep "^Port" /etc/ssh/sshd_config | awk '{print $2}')
            print_result "PASS" "使用非标准 SSH 端口：$PORT"
        fi
    else
        print_result "WARN" "未找到 sshd_config" "如使用 VPS 请检查云服务商控制台"
    fi
}

# 检查 API 密钥管理
check_api_keys() {
    section "🔑 API 密钥管理"
    
    # 检查常见密钥文件
    if [[ -f ~/.openclaw/config.json ]]; then
        if grep -q "password\|secret\|key" ~/.openclaw/config.json 2>/dev/null; then
            print_result "WARN" "config.json 可能包含敏感信息" "建议使用环境变量或加密存储"
        else
            print_result "PASS" "config.json 无明显敏感信息"
        fi
    fi
    
    # 检查环境变量
    if env | grep -qi "api_key\|secret\|token" 2>/dev/null; then
        print_result "WARN" "检测到 API 密钥环境变量" "确保未泄露到日志或错误输出"
    fi
    
    # 检查 .env 文件权限
    if [[ -f ~/.openclaw/.env ]]; then
        perms=$(stat -c %a ~/.openclaw/.env 2>/dev/null || stat -f %A ~/.openclaw/.env 2>/dev/null)
        if [[ "$perms" == "600" || "$perms" == "400" ]]; then
            print_result "PASS" ".env 文件权限安全 ($perms)"
        else
            print_result "FAIL" ".env 文件权限不安全 ($perms)" "建议运行：chmod 600 ~/.openclaw/.env"
        fi
    else
        print_result "PASS" "未发现 .env 文件"
    fi
    
    # 检查密钥是否硬编码
    if grep -r "sk-\|Bearer\|api_key=" ~/.openclaw/workspace 2>/dev/null | grep -v ".git" | head -5; then
        print_result "WARN" "检测到可能的硬编码密钥" "请审查上述文件"
    fi
}

# 检查数据出境合规
check_data_border() {
    section "🌍 数据出境合规（中国法规）"
    
    # 检查服务器位置
    if command -v curl &> /dev/null; then
        location=$(curl -s ipinfo.io/country 2>/dev/null || echo "UNKNOWN")
        if [[ "$location" == "CN" ]]; then
            print_result "PASS" "服务器位于中国境内 ($location)"
        else
            print_result "WARN" "服务器位于中国境外 ($location)" "如涉及中国用户数据，需申报数据出境安全评估"
        fi
    fi
    
    # 检查隐私政策
    if [[ -f ~/.openclaw/workspace/PRIVACY.md ]]; then
        print_result "PASS" "存在隐私政策文档"
    else
        print_result "WARN" "未发现隐私政策文档" "建议创建 PRIVACY.md 说明数据收集和使用"
    fi
    
    # 检查数据加密
    if command -v openssl &> /dev/null; then
        print_result "PASS" "OpenSSL 可用（支持数据加密）"
    else
        print_result "WARN" "OpenSSL 未安装" "建议安装以支持数据加密存储"
    fi
}

# 检查部署场景特定项
check_deployment() {
    section "📦 部署场景检查"
    
    # 检测部署类型
    if [[ -f /etc/docker/version.json ]] || command -v docker &> /dev/null; then
        print_result "PASS" "Docker 环境已检测"
        if docker ps 2>/dev/null | grep -q openclaw; then
            print_result "PASS" "OpenClaw 容器正在运行"
        fi
    fi
    
    # 检查是否为 VPS
    if command -v dmidecode &> /dev/null; then
        manufacturer=$(dmidecode -s system-manufacturer 2>/dev/null | tr '[:upper:]' '[:lower:]')
        if [[ "$manufacturer" == *"alibaba"* || "$manufacturer" == *"tencent"* || "$manufacturer" == *"aws"* ]]; then
            print_result "PASS" "VPS 环境已识别 ($manufacturer)"
            print_result "WARN" "VPS 需额外检查安全组规则" "请登录云服务商控制台确认"
        fi
    fi
    
    # 检查是否为个人 Mac
    if [[ "$(uname)" == "Darwin" ]]; then
        print_result "PASS" "macOS 个人设备"
        print_result "WARN" "确保启用了 FileVault 磁盘加密" "系统偏好设置 → 安全性与隐私"
    fi
}

# 检查自动更新
check_updates() {
    section "🔄 系统更新"
    
    # 检查 OpenClaw 版本
    if command -v openclaw &> /dev/null; then
        version=$(openclaw --version 2>/dev/null || echo "unknown")
        print_result "PASS" "OpenClaw 已安装 (版本：$version)"
    else
        print_result "FAIL" "OpenClaw 未安装或不在 PATH"
    fi
    
    # 检查系统更新
    if command -v apt &> /dev/null; then
        if [[ -f /var/lib/apt/periodic/update-success-stamp ]]; then
            last_update=$(stat -c %y /var/lib/apt/periodic/update-success-stamp 2>/dev/null | cut -d' ' -f1)
            print_result "PASS" "系统包列表已更新 ($last_update)"
        else
            print_result "WARN" "建议运行：sudo apt update"
        fi
    elif command -v brew &> /dev/null; then
        print_result "PASS" "Homebrew 已安装"
        print_result "WARN" "建议定期运行：brew update && brew upgrade"
    fi
}

# 生成报告
generate_report() {
    section "📊 检查报告"
    
    TOTAL=$((PASS + WARN + FAIL))
    echo "检查项目总数：$TOTAL"
    echo -e "${GREEN}通过：$PASS${NC}"
    echo -e "${YELLOW}警告：$WARN${NC}"
    echo -e "${RED}失败：$FAIL${NC}"
    echo ""
    
    if [[ $FAIL -gt 0 ]]; then
        echo -e "${RED}⚠️  发现 $FAIL 项严重问题，建议立即修复！${NC}"
    elif [[ $WARN -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  发现 $WARN 项警告，建议优化配置${NC}"
    else
        echo -e "${GREEN}✅ 所有检查项通过！${NC}"
    fi
    
    echo ""
    echo "详细检查报告已保存到：~/openclaw-security-report.txt"
    
    # 保存报告到文件
    {
        echo "OpenClaw Security Deployment Checklist Report"
        echo "Generated: $(date)"
        echo "============================================"
        echo "PASS: $PASS"
        echo "WARN: $WARN"
        echo "FAIL: $FAIL"
    } > ~/openclaw-security-report.txt
}

# 主函数
main() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════╗"
    echo "║  OpenClaw Security Deployment Checklist   ║"
    echo "║        安全部署检查清单 v1.0              ║"
    echo "╚═══════════════════════════════════════════╝"
    echo -e "${NC}"
    
    check_firewall
    check_ssh
    check_api_keys
    check_data_border
    check_deployment
    check_updates
    generate_report
}

# 执行
main "$@"
