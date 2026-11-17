#!/bin/bash
# configure_firewall.sh - Linux 防火墙配置
# 仅允许内网段访问指定端口，禁止直接对公网开放
set -euo pipefail

PORTS="${1:-1433}"                 # 逗号分隔的端口列表，如 "3306,5432"
SOURCE_CIDR="${2:-10.0.0.0/8}"      # 允许的来源 IP 段（仅内网）
RULE_COMMENT="${3:-GotoCloudServerManager}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

# 安全检查：禁止对 0.0.0.0/0 开放数据库端口
if [ "$SOURCE_CIDR" = "0.0.0.0/0" ] || [ "$SOURCE_CIDR" = "Any" ] || [ "$SOURCE_CIDR" = "any" ]; then
    err "安全策略禁止将端口对公网（0.0.0.0/0）开放。请指定内网 CIDR。"
fi

detect_os() {
    [ -f /etc/os-release ] && . /etc/os-release && echo "$ID" || echo "unknown"
}

OS=$(detect_os)
log "操作系统：$OS，配置防火墙规则（来源：$SOURCE_CIDR）"

IFS=',' read -ra PORT_LIST <<< "$PORTS"

case "$OS" in
    ubuntu|debian)
        command -v ufw >/dev/null 2>&1 || apt-get install -y ufw
        for port in "${PORT_LIST[@]}"; do
            ufw allow from "$SOURCE_CIDR" to any port "$port" proto tcp comment "$RULE_COMMENT"
            log "已开放端口 $port（来源：$SOURCE_CIDR）"
        done
        ufw --force enable
        ;;
    centos|rhel|rocky|almalinux)
        command -v firewall-cmd >/dev/null 2>&1 || yum install -y firewalld
        systemctl enable --now firewalld
        for port in "${PORT_LIST[@]}"; do
            firewall-cmd --permanent --zone=public --add-rich-rule="rule family='ipv4' source address='$SOURCE_CIDR' port protocol='tcp' port='$port' accept"
            log "已开放端口 $port（来源：$SOURCE_CIDR）"
        done
        firewall-cmd --reload
        ;;
    *)
        err "不支持的操作系统：$OS"
        ;;
esac

log "防火墙规则配置完成"
exit 0
