#!/bin/bash
# install_redis.sh - Redis 7 安装
set -euo pipefail

REDIS_PORT="${1:-6379}"
REDIS_PASSWORD="${2:-$(openssl rand -hex 16)}"
BIND_ADDR="${3:-127.0.0.1}"  # 默认只绑定本机，禁止直接公网访问

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

detect_os() {
    [ -f /etc/os-release ] && . /etc/os-release && echo "$ID" || echo "unknown"
}

OS=$(detect_os)
log "操作系统：$OS，安装 Redis"

if systemctl is-active redis &>/dev/null || systemctl is-active redis-server &>/dev/null; then
    log "Redis 已运行，跳过安装"
    exit 0
fi

case "$OS" in
    ubuntu|debian)
        apt-get update -q
        apt-get install -y redis-server
        SERVICE="redis-server"
        CONFIG="/etc/redis/redis.conf"
        ;;
    centos|rhel|rocky|almalinux)
        yum install -y epel-release
        yum install -y redis
        SERVICE="redis"
        CONFIG="/etc/redis.conf"
        ;;
    *)
        err "不支持的操作系统：$OS"
        ;;
esac

# 配置 Redis
log "配置 Redis..."
sed -i "s/^bind .*/bind ${BIND_ADDR}/" "$CONFIG"
sed -i "s/^port .*/port ${REDIS_PORT}/" "$CONFIG"
sed -i "s/^# requirepass .*/requirepass ${REDIS_PASSWORD}/" "$CONFIG"
sed -i "s/^requirepass .*/requirepass ${REDIS_PASSWORD}/" "$CONFIG"
# 禁用危险命令
echo "rename-command FLUSHALL \"\"" >> "$CONFIG"
echo "rename-command FLUSHDB \"\"" >> "$CONFIG"
echo "rename-command CONFIG \"REDIS_CONFIG_$(openssl rand -hex 4)\"" >> "$CONFIG"
echo "rename-command DEBUG \"\"" >> "$CONFIG"

# 设置最大内存（默认 256MB）
TOTAL_MEM=$(free -m | awk '/^Mem:/{print $2}')
MAX_MEM=$(( TOTAL_MEM / 4 ))
if [ $MAX_MEM -gt 1024 ]; then MAX_MEM=1024; fi
echo "maxmemory ${MAX_MEM}mb" >> "$CONFIG"
echo "maxmemory-policy allkeys-lru" >> "$CONFIG"

systemctl enable "$SERVICE"
systemctl start "$SERVICE"
sleep 2

# 验证
redis-cli -p "$REDIS_PORT" -a "$REDIS_PASSWORD" ping | grep -q "PONG" && \
    log "Redis 安装成功，端口：$REDIS_PORT" || \
    err "Redis 启动验证失败"

echo "REDIS_PASSWORD=${REDIS_PASSWORD}"
exit 0
