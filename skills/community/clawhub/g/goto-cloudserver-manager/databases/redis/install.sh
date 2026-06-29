#!/bin/bash
# databases/redis/install.sh - Redis 安装入口
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/../../os_adapters/linux/install_redis.sh" "$@"
