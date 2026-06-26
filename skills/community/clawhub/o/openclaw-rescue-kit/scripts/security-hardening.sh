#!/bin/bash
# ~/.openclaw/scripts/security-hardening.sh
# OpenClaw 安全加固脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="$OPENCLAW_HOME/logs"
LOG_FILE="$LOG_DIR/security-hardening.log"
SAFE_CONFIG_DIR="$OPENCLAW_HOME/backups/safe-config"
GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"

mkdir -p "$LOG_DIR" "$SAFE_CONFIG_DIR"

# 加载核心函数
source "$SCRIPT_DIR/core.sh"

# ==================== 保存安全配置 ====================
save_safe_config() {
    local config_file="$OPENCLAW_HOME/openclaw.json"
    local safe_config="$SAFE_CONFIG_DIR/openclaw.json.safe"
    
    if [ -f "$config_file" ]; then
        cp "$config_file" "$safe_config"
        log_info "安全配置已保存到: $safe_config"
        return 0
    fi
    return 1
}

# ==================== 检查公网暴露 ====================
check_public_exposure() {
    log_info "检查公网暴露..."
    
    local public_listen=false
    local listen_address=""
    
    # 使用 ss 检查
    if command -v ss >/dev/null 2>&1; then
        listen_address=$(ss -tlnp 2>/dev/null | grep ":$GATEWAY_PORT " | awk '{print $4}')
    elif command -v netstat >/dev/null 2>&1; then
        listen_address=$(netstat -tlnp 2>/dev/null | grep ":$GATEWAY_PORT " | awk '{print $4}')
    elif command -v lsof >/dev/null 2>&1; then
        listen_address=$(lsof -i :$GATEWAY_PORT -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $9}' | head -1)
    fi
    
    if echo "$listen_address" | grep -q "0.0.0.0"; then
        public_listen=true
        log_warn "端口 $GATEWAY_PORT 监听在 0.0.0.0 (公网可访问)"
    elif echo "$listen_address" | grep -q "::"; then
        public_listen=true
        log_warn "端口 $GATEWAY_PORT 监听在 :: (IPv6 公网可访问)"
    fi
    
    if [ "$public_listen" = true ]; then
        echo ""
        echo "⚠️  安全风险: 端口 $GATEWAY_PORT 公网暴露"
        echo "   当前监听: $listen_address"
        echo ""
        echo "建议修复方案:"
        echo "   1. 修改 OpenClaw 配置，将监听地址改为 127.0.0.1"
        echo "   2. 使用防火墙限制访问来源"
        echo ""
        
        read -p "是否自动修复? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            fix_public_exposure
        fi
        
        return 1
    else
        log_info "端口 $GATEWAY_PORT 仅本地监听: $listen_address"
        return 0
    fi
}

fix_public_exposure() {
    log_info "尝试修复公网暴露..."
    
    local config_file="$OPENCLAW_HOME/openclaw.json"
    
    if [ ! -f "$config_file" ]; then
        log_error "配置文件不存在"
        return 1
    fi
    
    # 备份
    cp "$config_file" "$config_file.bak.security_$(date +%Y%m%d_%H%M%S)"
    
    # 使用 jq 修改配置
    if command -v jq >/dev/null 2>&1; then
        # 尝试修改 gateway.host 或类似配置项
        jq '.gateway.host = "127.0.0.1"' "$config_file" > "${config_file}.tmp" 2>/dev/null && \
            mv "${config_file}.tmp" "$config_file" && \
            log_info "已修改配置，将网关地址改为 127.0.0.1" || \
            log_warn "无法自动修改配置，请手动编辑"
    else
        log_warn "jq 未安装，无法自动修改配置"
    fi
    
    # 提示重启
    echo ""
    echo "配置已备份，请重启 OpenClaw 网关使更改生效:"
    echo "   openclaw gateway restart"
}

# ==================== 检查 Token ====================
check_token() {
    log_info "检查访问令牌配置..."
    
    local config_file="$OPENCLAW_HOME/openclaw.json"
    
    if [ ! -f "$config_file" ]; then
        log_error "配置文件不存在"
        return 1
    fi
    
    local has_token=false
    
    # 检查各种可能的 token 配置
    if command -v jq >/dev/null 2>&1; then
        if jq -e '.token' "$config_file" >/dev/null 2>&1; then
            has_token=true
        elif jq -e '.gateway.token' "$config_file" >/dev/null 2>&1; then
            has_token=true
        elif jq -e '.gateway.access_token' "$config_file" >/dev/null 2>&1; then
            has_token=true
        elif jq -e '."--token"' "$config_file" >/dev/null 2>&1; then
            has_token=true
        fi
    fi
    
    if [ "$has_token" = true ]; then
        log_info "已配置访问令牌"
        return 0
    else
        log_warn "未配置访问令牌"
        echo ""
        echo "⚠️  安全风险: 未配置访问令牌"
        echo ""
        echo "建议:"
        echo "   请在配置文件中添加 token 字段"
        echo "   或使用 --token 参数启动网关"
        echo ""
        
        read -p "是否生成随机令牌并配置? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            fix_token
        fi
        
        return 1
    fi
}

fix_token() {
    log_info "生成随机令牌..."
    
    local config_file="$OPENCLAW_HOME/openclaw.json"
    local token
    token=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xxd -p)
    
    # 备份
    cp "$config_file" "$config_file.bak.token_$(date +%Y%m%d_%H%M%S)"
    
    # 添加 token
    if command -v jq >/dev/null 2>&1; then
        jq ".token = \"$token\"" "$config_file" > "${config_file}.tmp" 2>/dev/null && \
            mv "${config_file}.tmp" "$config_file" && \
            log_info "已添加令牌到配置" || \
            log_error "无法添加令牌"
    fi
    
    echo "令牌已生成并配置。"
    echo "请重启网关: openclaw gateway restart"
}

# ==================== 检查重复服务 ====================
check_duplicate_services() {
    log_info "检查重复服务..."
    
    local services_found=0
    local service_list=""
    
    # 检查 systemd 用户级
    if command -v systemctl >/dev/null 2>&1; then
        local user_services
        user_services=$(systemctl --user list-units --type=service --all 2>/dev/null | grep -i openclaw || true)
        
        if [ -n "$user_services" ]; then
            log_warn "发现用户级 systemd 服务:"
            echo "$user_services"
            ((services_found++))
            service_list+="用户级 systemd: $user_services\n"
        fi
    fi
    
    # 检查 launchctl (macOS)
    if command -v launchctl >/dev/null 2>&1; then
        local launchctl_output
        launchctl_output=$(launchctl list 2>/dev/null | grep -i openclaw || true)
        
        if [ -n "$launchctl_output" ]; then
            log_warn "发现 launchctl 服务:"
            echo "$launchctl_output"
            ((services_found++))
            service_list+="launchctl: $launchctl_output\n"
        fi
    fi
    
    # 检查系统级 systemd
    if [ -d /etc/systemd/system ]; then
        local system_services
        system_services=$(ls /etc/systemd/system/openclaw*.service 2>/dev/null || true)
        
        if [ -n "$system_services" ]; then
            log_warn "发现系统级 systemd 服务:"
            echo "$system_services"
            ((services_found++))
            service_list+="系统级 systemd: $system_services\n"
        fi
    fi
    
    if [ "$services_found" -gt 1 ]; then
        log_error "发现 $services_found 个 OpenClaw 服务，可能存在冲突"
        echo ""
        echo "⚠️  安全风险: 检测到重复服务"
        echo ""
        echo "建议: 删除多余的服务，只保留一个"
        echo ""
        
        read -p "是否查看删除多余服务的命令? (y/n): " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            echo "删除多余服务命令  mac:"
            echo "OS: launchctl remove <service-name>"
            echo "  Linux: sudo systemctl stop <service-name> && sudo systemctl disable <service-name>"
        fi
        
        return 1
    elif [ "$services_found" -eq 1 ]; then
        log_info "检测到 1 个 OpenClaw 服务，正常"
        return 0
    else
        log_warn "未检测到任何 OpenClaw 服务"
        return 0
    fi
}

# ==================== 检查防火墙 ====================
check_firewall() {
    log_info "检查防火墙状态..."
    
    local firewall_enabled=false
    
    # 检查 macOS 防火墙
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v /usr/libexec/ApplicationFirewall/socketfilterfw >/dev/null 2>&1; then
            local fw_status
            fw_status=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "unknown")
            
            if echo "$fw_status" | grep -q "enabled\|on"; then
                firewall_enabled=true
                log_info "macOS 防火墙已开启"
            else
                log_warn "macOS 防火墙未开启"
            fi
        fi
    else
        # 检查 Linux 防火墙
        if command -v ufw >/dev/null 2>&1; then
            if ufw status 2>/dev/null | grep -q "Status: active"; then
                firewall_enabled=true
                log_info "UFW 防火墙已开启"
            fi
        elif command -v firewall-cmd >/dev/null 2>&1; then
            if firewall-cmd --state 2>/dev/null | grep -q "running"; then
                firewall_enabled=true
                log_info "firewalld 防火墙已开启"
            fi
        elif command -v iptables >/dev/null 2>&1; then
            if iptables -L -n 2>/dev/null | grep -q "Chain INPUT"; then
                firewall_enabled=true
                log_info "iptables 防火墙已配置"
            fi
        fi
    fi
    
    if [ "$firewall_enabled" = false ]; then
        echo ""
        echo "⚠️  建议开启防火墙"
        echo ""
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            echo "macOS 开启防火墙命令:"
            echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
        else
            echo "Linux 开启防火墙示例 (UFW):"
            echo "   sudo ufw enable"
            echo "   sudo ufw allow 22/tcp"
            echo "   sudo ufw allow $GATEWAY_PORT"
        fi
    fi
    
    return 0
}

# ==================== 主函数 ====================
main() {
    echo "========================================"
    echo "    OpenClaw 安全加固扫描"
    echo "========================================"
    echo ""
    
    # 保存安全配置选项
    if [ "${1:-}" = "--save-safe" ] || [ "${1:-}" = "-s" ]; then
        echo "[INFO] 保存当前安全配置..."
        if save_safe_config; then
            echo "[SUCCESS] 安全配置已保存"
        else
            echo "[ERROR] 保存安全配置失败"
            exit 1
        fi
        echo ""
    fi
    
    local issues=0
    
    # 1. 公网暴露检查
    echo "1. 检查公网暴露..."
    if check_public_exposure; then
        echo "   ✅ 无公网暴露风险"
    else
        echo "   ❌ 存在公网暴露风险"
        ((issues++))
    fi
    echo ""
    
    # 2. Token 检查
    echo "2. 检查访问令牌..."
    if check_token; then
        echo "   ✅ 已配置访问令牌"
    else
        echo "   ⚠️ 未配置访问令牌"
        ((issues++))
    fi
    echo ""
    
    # 3. 重复服务检查
    echo "3. 检查重复服务..."
    if check_duplicate_services; then
        echo "   ✅ 无重复服务"
    else
        echo "   ❌ 存在重复服务冲突"
        ((issues++))
    fi
    echo ""
    
    # 4. 防火墙检查
    echo "4. 检查防火墙..."
    if check_firewall; then
        echo "   ✅ 防火墙状态正常"
    else
        echo "   ℹ️  防火墙建议已给出"
    fi
    echo ""
    
    echo "========================================"
    
    if [ "$issues" -eq 0 ]; then
        echo "   ✅ 安全扫描通过 (问题: $issues)"
        echo ""
        echo "[INFO] 自动保存当前安全配置..."
        save_safe_config
    else
        echo "   ⚠️ 发现 $issues 项安全风险"
    fi
    
    echo "========================================"
    echo ""
    echo "使用说明:"
    echo "  保存安全配置: bash security-hardening.sh --save-safe"
    echo "  回滚到安全配置: bash git-tag.sh quick-rollback"
    echo ""
    echo "详细日志: $LOG_FILE"
}

main "$@"
