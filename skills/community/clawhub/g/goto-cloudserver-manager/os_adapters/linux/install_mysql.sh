#!/bin/bash
# install_mysql.sh - MySQL 8.0 安装（支持 Ubuntu 22.04 / Debian 12 / CentOS 7 / Rocky Linux 9）
set -euo pipefail

MYSQL_VERSION="${1:-8.0}"
MYSQL_ROOT_PASSWORD="${2:-$(openssl rand -base64 16)}"
DATA_DIR="${3:-/var/lib/mysql}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

# 检测系统
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
log "检测到操作系统：$OS"

# 检查是否已安装
if systemctl is-active mysql &>/dev/null || systemctl is-active mysqld &>/dev/null; then
    log "MySQL 已安装并运行，跳过安装"
    exit 0
fi

log "开始安装 MySQL $MYSQL_VERSION..."

case "$OS" in
    ubuntu|debian)
        export DEBIAN_FRONTEND=noninteractive
        apt-get update -q
        apt-get install -y gnupg curl

        # 添加 MySQL APT 仓库
        MYSQL_APT_DEB="mysql-apt-config_0.8.29-1_all.deb"
        curl -fsSL "https://dev.mysql.com/get/${MYSQL_APT_DEB}" -o "/tmp/${MYSQL_APT_DEB}"
        echo "mysql-apt-config mysql-apt-config/select-server select mysql-8.0" | debconf-set-selections
        DEBIAN_FRONTEND=noninteractive dpkg -i "/tmp/${MYSQL_APT_DEB}"
        apt-get update -q
        DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

        SERVICE="mysql"
        ;;
    centos|rhel|rocky|almalinux|ol)
        # 添加 MySQL 8.0 仓库
        rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
        cat > /etc/yum.repos.d/mysql.repo << 'EOF'
[mysql80-community]
name=MySQL 8.0 Community Server
baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/7/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql-2022
EOF
        yum install -y mysql-community-server

        SERVICE="mysqld"
        ;;
    *)
        err "不支持的操作系统：$OS"
        ;;
esac

# 启动 MySQL
systemctl enable "$SERVICE"
systemctl start "$SERVICE"
sleep 3

# 获取临时密码（CentOS）并设置 root 密码
if [ "$OS" = "centos" ] || [ "$OS" = "rocky" ] || [ "$OS" = "rhel" ]; then
    TEMP_PW=$(grep 'temporary password' /var/log/mysqld.log | tail -1 | awk '{print $NF}')
    if [ -n "$TEMP_PW" ]; then
        mysql --connect-expired-password -uroot -p"${TEMP_PW}" -e \
            "ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}'; FLUSH PRIVILEGES;"
    fi
else
    mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';" 2>/dev/null || true
fi

# 安全配置：删除匿名用户，禁止 root 远程登录
mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" << 'SQL'
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
SQL

log "MySQL root 密码已设置（请妥善保存）"
log "MySQL 安装完成，服务名：$SERVICE"
echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}"
exit 0
