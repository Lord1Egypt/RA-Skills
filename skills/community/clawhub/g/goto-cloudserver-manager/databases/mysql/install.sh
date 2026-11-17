#!/bin/bash
# databases/mysql/install.sh - MySQL 安装入口（委托给 os_adapters）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${SCRIPT_DIR}/../../os_adapters/linux/install_mysql.sh" "$@"
