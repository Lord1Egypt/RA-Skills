#!/bin/bash
# 部署模块通用函数

# 颜色定义
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# 安全路径检查（防止 rm -rf /）
safe_path() {
  local path="$1"
  if [[ "$path" == "/" ]] || [[ "$path" == "$HOME" ]] || [[ "$path" == "$HOME/" ]]; then
    log_error "不允许操作根目录或 home 目录: $path"
    return 1
  fi
  return 0
}

# 验证部署包
verify_package() {
  local pkg="$1"
  if [ ! -f "$pkg" ]; then
    log_error "部署包不存在: $pkg"
    return 1
  fi

  local size
  size=$(stat -f%z "$pkg" 2>/dev/null || stat -c%s "$pkg" 2>/dev/null || echo 0)
  if [ "$size" -lt 1024 ]; then
    log_error "部署包过小，可能损坏: $pkg"
    return 1
  fi

  return 0
}

# SSH 连接测试
test_ssh_connection() {
  local host="$1"
  local user="$2"
  local port="${3:-22}"

  if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=accept-new -p "$port" "$user@$host" "echo ok" &>/dev/null; then
    return 0
  fi
  return 1
}
