#!/bin/bash
# 打包模块通用函数

# 颜色定义
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m'

# SHA256 命令
sha256_cmd() {
  if command -v sha256sum >/dev/null 2>&1; then
    echo "sha256sum"
  else
    echo "shasum -a 256"
  fi
}

# 日志函数
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# 获取版本
get_version() {
  local project_dir="${1:-.}"
  if command -v git >/dev/null 2>&1; then
    git -C "$project_dir" describe --tags --always --dirty 2>/dev/null || echo "dev"
  else
    echo "dev"
  fi
}

# 清理临时目录
cleanup_temp() {
  if [ -n "${TEMP_DIR:-}" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}
