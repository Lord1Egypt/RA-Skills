#!/bin/bash

# OpenClaw Security Check Script
# Version: 1.0.0
# 检查OpenClaw安全配置，识别潜在风险

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# 检查OpenClaw是否运行
check_openclaw_running() {
    log_info "检查OpenClaw运行状态..."
    if systemctl is-active --quiet openclaw; then
        log_success "OpenClaw服务正在运行"
        return 0
    else
        log_warning "OpenClaw服务未运行或未使用systemctl管理"
        # 尝试其他检查方式
        if pgrep -f "openclaw" > /dev/null; then
            log_success "检测到OpenClaw进程"
            return 0
        else
            log_error "未检测到OpenClaw进程"
            return 1
        fi
    fi
}

# 检查配置文件权限
check_config_permissions() {
    log_info "检查配置文件权限..."
    
    local config_files=(
        "/etc/openclaw/config.yaml"
        "/etc/openclaw/config.json"
        "~/.openclaw/config.yaml"
        "~/.openclaw/config.json"
        "/root/.openclaw/config.yaml"
        "/root/.openclaw/config.json"
    )
    
    local found_files=()
    
    for file in "${config_files[@]}"; do
        if [[ -f "$file" ]]; then
            found_files+=("$file")
            local perms=$(stat -c "%a" "$file")
            local owner=$(stat -c "%U" "$file")
            
            if [[ "$perms" == "600" || "$perms" == "640" ]]; then
                log_success "$file: 权限正常 ($perms, 所有者: $owner)"
            else
                log_warning "$file: 权限可能过宽 ($perms, 所有者: $owner)，建议设置为600"
            fi
        fi
    done
    
    if [[ ${#found_files[@]} -eq 0 ]]; then
        log_warning "未找到OpenClaw配置文件"
    fi
}

# 检查API密钥安全
check_api_keys() {
    log_info "检查API密钥配置..."
    
    # 检查环境变量中的API密钥
    local sensitive_vars=("API_KEY" "OPENAI_API_KEY" "ANTHROPIC_API_KEY" "DEEPSEEK_API_KEY" "TOKEN")
    
    for var in "${sensitive_vars[@]}"; do
        if [[ -n "${!var}" ]]; then
            log_warning "环境变量 $var 已设置，可能包含敏感信息"
            # 显示前4个字符和后4个字符
            local value="${!var}"
            local masked="${value:0:4}...${value: -4}"
            log_info "  $var: $masked"
        fi
    done
    
    # 检查配置文件中的API密钥
    if [[ -f "/etc/openclaw/config.yaml" ]]; then
        if grep -q -i "api_key\|token\|secret\|password" /etc/openclaw/config.yaml; then
            log_warning "配置文件中可能包含敏感信息"
        fi
    fi
}

# 检查网络暴露
check_network_exposure() {
    log_info "检查网络暴露风险..."
    
    # 检查监听的端口
    local openclaw_ports=$(ss -tlnp | grep -i openclaw | awk '{print $4}' | cut -d: -f2 | sort -u)
    
    if [[ -n "$openclaw_ports" ]]; then
        log_info "OpenClaw监听的端口: $openclaw_ports"
        
        for port in $openclaw_ports; do
            if [[ "$port" == "80" || "$port" == "443" || "$port" == "3000" || "$port" == "8080" ]]; then
                log_warning "端口 $port 可能对外暴露，建议使用防火墙限制访问"
            fi
        done
    else
        log_success "未检测到OpenClaw监听端口"
    fi
    
    # 检查是否使用默认端口
    if echo "$openclaw_ports" | grep -q "3000"; then
        log_warning "使用默认端口3000，建议修改"
    fi
}

# 检查日志配置
check_logging() {
    log_info "检查日志配置..."
    
    # 检查系统日志
    if journalctl -u openclaw --since "1 hour ago" 2>/dev/null | grep -q -i "error\|fail\|exception"; then
        log_warning "发现OpenClaw错误日志"
        journalctl -u openclaw --since "1 hour ago" | grep -i "error\|fail\|exception" | head -5
    else
        log_success "最近1小时无错误日志"
    fi
    
    # 检查日志文件权限
    local log_files=(
        "/var/log/openclaw.log"
        "/var/log/openclaw/*.log"
        "/tmp/openclaw*.log"
    )
    
    for pattern in "${log_files[@]}"; do
        for file in $pattern; do
            if [[ -f "$file" ]]; then
                local perms=$(stat -c "%a" "$file" 2>/dev/null || echo "unknown")
                if [[ "$perms" != "600" && "$perms" != "640" ]]; then
                    log_warning "日志文件 $file 权限过宽 ($perms)"
                fi
            fi
        done
    done
}

# 检查Token使用情况
check_token_usage() {
    log_info "检查Token使用情况..."
    
    # 尝试从日志中提取Token使用信息
    local token_logs=$(journalctl -u openclaw --since "1 day ago" 2>/dev/null | grep -i "token\|cost" | tail -10)
    
    if [[ -n "$token_logs" ]]; then
        log_info "最近Token使用记录:"
        echo "$token_logs"
        
        # 检查是否有异常消耗
        if echo "$token_logs" | grep -q -i "high\|excessive\|warning"; then
            log_warning "检测到可能的Token异常消耗"
        fi
    else
        log_success "未找到Token使用记录"
    fi
}

# 生成安全报告
generate_security_report() {
    log_info "生成安全报告..."
    
    local report_file="/tmp/openclaw-security-report-$(date +%Y%m%d-%H%M%S).txt"
    
    {
        echo "=== OpenClaw安全配置检查报告 ==="
        echo "生成时间: $(date)"
        echo "系统: $(uname -a)"
        echo ""
        echo "1. 服务状态:"
        systemctl is-active openclaw && echo "  OpenClaw服务: 运行中" || echo "  OpenClaw服务: 未运行"
        echo ""
        echo "2. 配置文件检查:"
        check_config_permissions | grep -E "\[(WARNING|ERROR|SUCCESS)\]" | sed 's/^/  /'
        echo ""
        echo "3. 网络暴露检查:"
        check_network_exposure | grep -E "\[(WARNING|ERROR|SUCCESS)\]" | sed 's/^/  /'
        echo ""
        echo "4. 日志检查:"
        check_logging | grep -E "\[(WARNING|ERROR|SUCCESS)\]" | sed 's/^/  /'
        echo ""
        echo "5. Token使用检查:"
        check_token_usage | grep -E "\[(WARNING|ERROR|SUCCESS)\]" | sed 's/^/  /'
        echo ""
        echo "=== 安全建议 ==="
        echo "1. 确保配置文件权限为600"
        echo "2. 使用防火墙限制OpenClaw端口访问"
        echo "3. 定期检查Token消耗情况"
        echo "4. 监控错误日志并及时处理"
        echo "5. 避免在配置文件中明文存储API密钥"
    } > "$report_file"
    
    log_success "安全报告已生成: $report_file"
    cat "$report_file"
}

# 主函数
main() {
    echo "========================================"
    echo "    OpenClaw安全配置检查工具 v1.0.0"
    echo "========================================"
    echo ""
    
    # 检查运行权限
    if [[ $EUID -ne 0 ]]; then
        log_warning "建议使用root权限运行以获得完整检查结果"
    fi
    
    # 执行各项检查
    check_openclaw_running
    echo ""
    
    check_config_permissions
    echo ""
    
    check_api_keys
    echo ""
    
    check_network_exposure
    echo ""
    
    check_logging
    echo ""
    
    check_token_usage
    echo ""
    
    # 生成报告
    generate_security_report
    
    echo ""
    echo "========================================"
    echo "检查完成！请根据报告中的建议进行安全加固。"
    echo "========================================"
}

# 执行主函数
main "$@"