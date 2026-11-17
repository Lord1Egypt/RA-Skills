#!/bin/bash
# install_postgresql.sh - PostgreSQL 15/16 安装
set -euo pipefail

PG_VERSION="${1:-15}"
PG_PORT="${2:-5432}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
log "操作系统：$OS，安装 PostgreSQL $PG_VERSION"

# 检查是否已安装
if systemctl is-active "postgresql" &>/dev/null || systemctl is-active "postgresql-${PG_VERSION}" &>/dev/null; then
    log "PostgreSQL 已运行，跳过安装"
    exit 0
fi

case "$OS" in
    ubuntu|debian)
        apt-get update -q
        apt-get install -y curl ca-certificates gnupg

        # PostgreSQL 官方 APT 仓库
        curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
            gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg

        . /etc/os-release
        echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] https://apt.postgresql.org/pub/repos/apt ${VERSION_CODENAME}-pgdg main" \
            > /etc/apt/sources.list.d/pgdg.list

        apt-get update -q
        apt-get install -y "postgresql-${PG_VERSION}"
        SERVICE="postgresql"
        DATA_DIR="/var/lib/postgresql/${PG_VERSION}/main"
        ;;
    centos|rhel|rocky|almalinux)
        # PostgreSQL 官方 PGDG 仓库
        PGDG_RPM="https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm"
        yum install -y "$PGDG_RPM" || true
        yum install -y "postgresql${PG_VERSION/./}-server"
        "/usr/pgsql-${PG_VERSION}/bin/postgresql-${PG_VERSION}-setup" initdb
        SERVICE="postgresql-${PG_VERSION}"
        DATA_DIR="/var/lib/pgsql/${PG_VERSION}/data"
        ;;
    openeuler)
        dnf install -y postgresql postgresql-server
        postgresql-setup --initdb
        SERVICE="postgresql"
        DATA_DIR="/var/lib/pgsql/data"
        ;;
    *)
        err "不支持的操作系统：$OS"
        ;;
esac

# 配置 postgresql.conf：监听内网，设置端口
PG_CONF=$(find /etc/postgresql /var/lib/pgsql -name "postgresql.conf" 2>/dev/null | head -1)
if [ -n "$PG_CONF" ]; then
    sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost,10.0.0.0\/8'/" "$PG_CONF" 2>/dev/null || true
    sed -i "s/#port = 5432/port = ${PG_PORT}/" "$PG_CONF" 2>/dev/null || true
fi

# 配置 pg_hba.conf：允许内网连接
PG_HBA=$(find /etc/postgresql /var/lib/pgsql -name "pg_hba.conf" 2>/dev/null | head -1)
if [ -n "$PG_HBA" ]; then
    echo "host    all             all             10.0.0.0/8              scram-sha-256" >> "$PG_HBA"
fi

systemctl enable "$SERVICE"
systemctl start "$SERVICE"
sleep 3

log "PostgreSQL ${PG_VERSION} 安装完成，端口：${PG_PORT}"
exit 0
