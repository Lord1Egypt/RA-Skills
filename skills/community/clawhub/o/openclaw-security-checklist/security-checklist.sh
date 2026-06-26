#!/bin/bash
# OpenClaw 安全部署检查清单 - 快速检查脚本
# 用法：./security-checklist.sh [--full|--category P0|--report|--interactive]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
REPORT_FILE="$WORKSPACE_DIR/security-report-$(date +%Y%m%d-%H%M%S).md"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 计数器
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARN_CHECKS=0

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[FAIL]${NC} $1"; }

# 记录检查结果
declare -a CHECK_RESULTS

record_check() {
    local category=$1
    local item=$2
    local status=$3  # pass/fail/warn
    local suggestion=$4
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [ "$status" = "pass" ]; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        CHECK_RESULTS+=("$category|$item|✅|$suggestion")
    elif [ "$status" = "warn" ]; then
        WARN_CHECKS=$((WARN_CHECKS + 1))
        CHECK_RESULTS+=("$category|$item|⚠️|$suggestion")
    else
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        CHECK_RESULTS+=("$category|$item|❌|$suggestion")
    fi
}

# P0 - 身份认证与密钥管理
check_p0() {
    log_info "检查 P0 - 身份认证与密钥管理..."
    
    # 检查 .env 文件是否存在明文密钥
    if [ -f "$HOME/.openclaw/config/.env" ]; then
        if grep -qE "(API_KEY|SECRET|TOKEN)=" "$HOME/.openclaw/config/.env" 2>/dev/null; then
            record_check "P0" "API 密钥加密存储" "warn" "建议使用 openclaw config set 或系统密钥链"
        else
            record_check "P0" "API 密钥加密存储" "pass" ""
        fi
    else
        record_check "P0" "API 密钥加密存储" "pass" ""
    fi
    
    # 检查 openclaw config 是否已配置
    if command -v openclaw &> /dev/null; then
        if openclaw config list &> /dev/null; then
            record_check "P0" "使用 openclaw config 管理配置" "pass" ""
        else
            record_check "P0" "使用 openclaw config 管理配置" "warn" "运行 openclaw config init 初始化"
        fi
    fi
    
    # 检查密钥文件权限
    if [ -f "$HOME/.openclaw/config/credentials.json" ]; then
        perms=$(stat -f "%Lp" "$HOME/.openclaw/config/credentials.json" 2>/dev/null || stat -c "%a" "$HOME/.openclaw/config/credentials.json" 2>/dev/null)
        if [ "$perms" = "600" ] || [ "$perms" = "400" ]; then
            record_check "P0" "密钥文件权限 (600)" "pass" ""
        else
            record_check "P0" "密钥文件权限 (600)" "fail" "执行：chmod 600 $HOME/.openclaw/config/credentials.json"
        fi
    fi
}

# P1 - 网络安全
check_p1() {
    log_info "检查 P1 - 网络安全..."
    
    # 检查防火墙状态 (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        fw_status=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "disabled")
        if echo "$fw_status" | grep -q "enabled"; then
            record_check "P1" "防火墙已启用" "pass" ""
        else
            record_check "P1" "防火墙已启用" "warn" "系统偏好设置 → 安全性与隐私 → 防火墙"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v ufw &> /dev/null; then
            if ufw status 2>/dev/null | grep -q "Status: active"; then
                record_check "P1" "防火墙已启用 (ufw)" "pass" ""
            else
                record_check "P1" "防火墙已启用 (ufw)" "warn" "执行：sudo ufw enable"
            fi
        else
            record_check "P1" "防火墙已启用" "warn" "安装 ufw 或配置 iptables"
        fi
    fi
    
    # 检查监听端口
    log_info "检查监听端口..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        listening_ports=$(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | grep LISTEN | wc -l)
    else
        listening_ports=$(ss -tlnp 2>/dev/null | grep LISTEN | wc -l)
    fi
    
    if [ "$listening_ports" -gt 0 ]; then
        record_check "P1" "监听端口数量: $listening_ports" "warn" "确认所有端口都是必要的"
    else
        record_check "P1" "无监听端口" "pass" ""
    fi
    
    # 检查 Gateway 配置
    if [ -f "$HOME/.openclaw/gateway/config.json" ]; then
        if grep -q '"bind": "127.0.0.1"' "$HOME/.openclaw/gateway/config.json" 2>/dev/null; then
            record_check "P1" "Gateway 绑定本地回环" "pass" ""
        elif grep -q '"bind": "0.0.0.0"' "$HOME/.openclaw/gateway/config.json" 2>/dev/null; then
            record_check "P1" "Gateway 绑定所有接口" "warn" "建议改为 127.0.0.1 或使用防火墙限制"
        fi
    fi
}

# P2 - 数据合规
check_p2() {
    log_info "检查 P2 - 数据合规..."
    
    # 检查日志配置
    if [ -d "$HOME/.openclaw/logs" ]; then
        log_size=$(du -sh "$HOME/.openclaw/logs" 2>/dev/null | cut -f1)
        record_check "P2" "日志目录存在 ($log_size)" "pass" ""
    else
        record_check "P2" "日志目录存在" "warn" "创建日志目录用于审计"
    fi
    
    # 检查是否使用境内 API
    if [ -f "$HOME/.openclaw/config/config.json" ]; then
        if grep -qE "(aliyun|bailian|baidu|tencent)" "$HOME/.openclaw/config/config.json" 2>/dev/null; then
            record_check "P2" "使用境内云服务" "pass" ""
        else
            record_check "P2" "使用境内云服务" "warn" "考虑使用阿里云/百度智能云满足数据合规"
        fi
    fi
}

# P3 - 系统加固
check_p3() {
    log_info "检查 P3 - 系统加固..."
    
    # 检查磁盘加密 (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if fdesetup status 2>/dev/null | grep -q "FileVault is On"; then
            record_check "P3" "FileVault 已启用" "pass" ""
        else
            record_check "P3" "FileVault 已启用" "warn" "系统偏好设置 → 安全性与隐私 → FileVault"
        fi
    fi
    
    # 检查自动更新
    if [[ "$OSTYPE" == "darwin"* ]]; then
        auto_update=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null || echo "0")
        if [ "$auto_update" = "1" ]; then
            record_check "P3" "自动更新已启用" "pass" ""
        else
            record_check "P3" "自动更新已启用" "warn" "系统偏好设置 → 软件更新"
        fi
    fi
    
    # 检查 OpenClaw 版本
    if command -v openclaw &> /dev/null; then
        version=$(openclaw --version 2>/dev/null || echo "unknown")
        record_check "P3" "OpenClaw 版本: $version" "pass" ""
    else
        record_check "P3" "OpenClaw 已安装" "fail" "安装 OpenClaw: npm install -g openclaw"
    fi
}

# P4 - 监控与响应
check_p4() {
    log_info "检查 P4 - 监控与响应..."
    
    # 检查安全审计日志
    if command -v openclaw &> /dev/null; then
        if [ -f "$HOME/.openclaw/logs/security-audit.log" ]; then
            record_check "P4" "安全审计日志存在" "pass" ""
        else
            record_check "P4" "安全审计日志" "warn" "运行 openclaw security audit 生成基线"
        fi
    fi
    
    # 检查备份
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if tmutil status 2>/dev/null | grep -q "Snapshot Summary"; then
            record_check "P4" "Time Machine 备份" "pass" ""
        else
            record_check "P4" "Time Machine 备份" "warn" "启用 Time Machine 定期备份"
        fi
    fi
}

# 生成报告
generate_report() {
    log_info "生成检查报告..."
    
    cat > "$REPORT_FILE" << EOF
# OpenClaw 安全部署检查报告

**生成时间**: $(date '+%Y-%m-%d %H:%M')
**检查脚本**: $0
**部署环境**: $OSTYPE

## 总体评分: $(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))/100

- ✅ 通过: $PASSED_CHECKS
- ⚠️  警告: $WARN_CHECKS
- ❌ 失败: $FAILED_CHECKS
- 📊 总计: $TOTAL_CHECKS

---

## 详细结果

EOF

    # 按类别分组
    local current_category=""
    for result in "${CHECK_RESULTS[@]}"; do
        IFS='|' read -r category item status suggestion <<< "$result"
        
        if [ "$category" != "$current_category" ]; then
            echo "### $category" >> "$REPORT_FILE"
            current_category=$category
        fi
        
        echo "- $status $item" >> "$REPORT_FILE"
        if [ -n "$suggestion" ]; then
            echo "  - 💡 建议: $suggestion" >> "$REPORT_FILE"
        fi
    done
    
    # 高风险项
    echo -e "\n## 高风险项（需立即修复）\n" >> "$REPORT_FILE"
    for result in "${CHECK_RESULTS[@]}"; do
        IFS='|' read -r category item status suggestion <<< "$result"
        if [ "$status" = "❌" ]; then
            echo "1. [$category] $item - $suggestion" >> "$REPORT_FILE"
        fi
    done
    
    # 中风险项
    echo -e "\n## 中风险项（建议修复）\n" >> "$REPORT_FILE"
    for result in "${CHECK_RESULTS[@]}"; do
        IFS='|' read -r category item status suggestion <<< "$result"
        if [ "$status" = "⚠️" ]; then
            echo "1. [$category] $item - $suggestion" >> "$REPORT_FILE"
        fi
    done
    
    log_success "报告已生成：$REPORT_FILE"
}

# 主函数
main() {
    echo "🔒 OpenClaw 安全部署检查清单"
    echo "============================"
    echo ""
    
    case "${1:-}" in
        --full)
            check_p0
            check_p1
            check_p2
            check_p3
            check_p4
            generate_report
            ;;
        --category)
            case "${2:-}" in
                P0) check_p0 ;;
                P1) check_p1 ;;
                P2) check_p2 ;;
                P3) check_p3 ;;
                P4) check_p4 ;;
                *) log_error "未知类别：$2"; exit 1 ;;
            esac
            ;;
        --report)
            check_p0
            check_p1
            check_p2
            check_p3
            check_p4
            generate_report
            ;;
        --interactive)
            log_info "交互模式暂未实现，使用 --full 运行完整检查"
            check_p0
            check_p1
            check_p2
            check_p3
            check_p4
            ;;
        *)
            # 默认快速检查
            check_p0
            check_p1
            check_p3
            ;;
    esac
    
    # 输出摘要
    echo ""
    echo "============================"
    echo "检查完成!"
    echo "  通过：$PASSED_CHECKS"
    echo "  警告：$WARN_CHECKS"
    echo "  失败：$FAILED_CHECKS"
    echo ""
    
    if [ $FAILED_CHECKS -gt 0 ]; then
        log_error "发现 $FAILED_CHECKS 个高风险项，请立即修复!"
        exit 1
    elif [ $WARN_CHECKS -gt 0 ]; then
        log_warning "发现 $WARN_CHECKS 个警告项，建议优化"
        exit 0
    else
        log_success "所有检查通过!"
        exit 0
    fi
}

main "$@"
