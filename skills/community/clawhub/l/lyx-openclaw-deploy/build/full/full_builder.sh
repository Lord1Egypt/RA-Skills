#!/bin/bash
# OpenClaw 一键部署脚本
# 用法: ./full_builder.sh [--host ...]

set -euo pipefail

# 加载通用函数
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
# shellcheck source=/dev/null
source "$PROJECT_DIR/deploy/common.sh"

DEPLOY_DIR="$PROJECT_DIR/deploy"
BUILD_DIR="$PROJECT_DIR/build"

HOST=""
USER=""
PORT=22
PASSWORD=""
KEY=""
PACKAGE="./openclaw-deploy.tar.gz"
INSTALL_DIR="/opt/openclaw"
MODE="cover"
DEPLOY_URL="${DEPLOY_URL:-}"

log() { log_info "$1"; }
err() { log_error "$1"; }

usage() {
  cat <<EOF
Usage:
  本地部署: $0 [--package <tar.gz>] [--install-dir <dir>] [--mode cover|backup|update]
  远程部署: $0 --host <host> --user <user> [--password <pwd>|--key <path>] [--port 22]
           [--package <tar.gz>] [--install-dir <dir>] [--mode cover|backup|update]
EOF
}

sha256_cmd() {
  if command -v sha256sum >/dev/null 2>&1; then
    echo "sha256sum"
  else
    echo "shasum -a 256"
  fi
}

verify_sha() {
  local pkg="$1"
  local sha_file="$2"
  if [ ! -f "$sha_file" ]; then
    log "${YELLOW}⚠️  未找到 SHA256 文件，跳过校验: $sha_file${NC}"
    return 0
  fi

  local cmd
  cmd="$(sha256_cmd)"
  local expected
  expected="$(awk '{print $1}' "$sha_file" | head -n1)"
  local actual
  actual="$($cmd "$pkg" | awk '{print $1}')"

  if [ -z "$expected" ] || [ -z "$actual" ]; then
    err "SHA256 校验失败：无法读取校验值"
    exit 1
  fi

  if [ "$expected" != "$actual" ]; then
    err "SHA256 校验失败：文件可能被篡改"
    exit 1
  fi

  log "${GREEN}✅ SHA256 校验通过${NC}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --host) HOST="$2"; shift 2;;
    --user) USER="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --password) PASSWORD="$2"; shift 2;;
    --key) KEY="$2"; shift 2;;
    --package) PACKAGE="$2"; shift 2;;
    --install-dir) INSTALL_DIR="$2"; shift 2;;
    --mode) MODE="$2"; shift 2;;
    --url) DEPLOY_URL="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) err "未知参数: $1"; usage; exit 1;;
  esac
done

echo "🪶 OpenClaw 一键部署"

# 远程部署
if [ -n "$HOST" ]; then
  "$DEPLOY_DIR/remote_deploy.sh" --host "$HOST" --user "$USER" --port "$PORT" \
    ${PASSWORD:+--password "$PASSWORD"} ${KEY:+--key "$KEY"} \
    --package "$PACKAGE" --install-dir "$INSTALL_DIR" --mode "$MODE"
  exit 0
fi

# 检查系统
check_system() {
  log "📋 检查系统要求..."

  # 检测系统
  if [ "$(uname)" != "Linux" ]; then
    log "${YELLOW}⚠️  此脚本专为 Linux 设计，当前系统: $(uname)${NC}"
    log "${YELLOW}   macOS 用户请手动安装 Docker Desktop${NC}"
  fi

  "$DEPLOY_DIR/check_env.sh"

  # 自动安装 Docker (仅 Linux)
  if ! command -v docker &> /dev/null; then
    if [ "$(uname)" = "Linux" ]; then
      log "🐳 安装 Docker..."
      curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
      sh /tmp/get-docker.sh
      rm /tmp/get-docker.sh
    fi
  else
    log "${GREEN}✅ Docker 已安装${NC}"
  fi

  log "${GREEN}✅ 系统检查通过${NC}"
}

# 下载部署包
download_package() {
  log "📥 下载部署包..."

  if [ -f "$PACKAGE" ]; then
    log "   使用本地包: $PACKAGE"
    cp "$PACKAGE" /tmp/openclaw.tar.gz
    if [ -f "${PACKAGE}.sha256" ]; then
      cp "${PACKAGE}.sha256" /tmp/openclaw.tar.gz.sha256
    fi
  elif [ -n "$DEPLOY_URL" ]; then
    log "   从 URL 下载: $DEPLOY_URL"
    curl -fsSL "$DEPLOY_URL" -o /tmp/openclaw.tar.gz
    if curl -fsSL "${DEPLOY_URL}.sha256" -o /tmp/openclaw.tar.gz.sha256; then
      log "   ✓ 已下载 SHA256 校验文件"
    else
      log "${YELLOW}⚠️  未获取到 SHA256 校验文件${NC}"
    fi
  else
    err "请提供部署包: openclaw-deploy.tar.gz 或设置 --url"
    exit 1
  fi

  if [ -f /tmp/openclaw.tar.gz.sha256 ]; then
    verify_sha /tmp/openclaw.tar.gz /tmp/openclaw.tar.gz.sha256
  fi

  # 解压到临时目录
  log "📦 解压文件..."
  TMP_DIR="/tmp/openclaw-deploy-$(date +%s)"
  mkdir -p "$TMP_DIR"
  tar -xzf /tmp/openclaw.tar.gz -C "$TMP_DIR"
  echo "$TMP_DIR"
}

# 配置
configure() {
  log "⚙️  配置服务..."

  if [ -f "$INSTALL_DIR/docker/.env.example" ] && [ ! -f "$INSTALL_DIR/docker/.env" ]; then
    cp "$INSTALL_DIR/docker/.env.example" "$INSTALL_DIR/docker/.env"
    log "${YELLOW}⚠️  请编辑 $INSTALL_DIR/docker/.env 填入 API Keys${NC}"
  fi

  mkdir -p "$INSTALL_DIR/data/openclaw" "$INSTALL_DIR/data/workspace"
}

# 验证部署结果
verify_deployment() {
  log "🔍 验证部署结果..."

  local max_attempts=30
  local attempt=1
  local container_name="openclaw-gateway"

  # 等待容器启动
  log "   等待容器启动..."
  while [ $attempt -le $max_attempts ]; do
    if docker ps --format '{{.Names}}' | grep -q "$container_name"; then
      local status
      status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null || echo "unknown")
      if [ "$status" = "running" ]; then
        log "   ✓ 容器运行中"
        break
      fi
    fi
    sleep 1
    attempt=$((attempt + 1))
  done

  if [ $attempt -gt $max_attempts ]; then
    log "${YELLOW}⚠️  容器启动超时${NC}"
    return 1
  fi

  # 检查容器健康状态
  local health
  health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "none")

  if [ "$health" = "healthy" ]; then
    log "${GREEN}✅ 服务健康检查通过${NC}"
  elif [ "$health" != "none" ]; then
    log "${YELLOW}⚠️  服务健康状态: $health${NC}"
  else
    # 检查端口
    if docker port "$container_name" 2026 &>/dev/null; then
      log "${GREEN}✅ 端口 2026 已监听${NC}"
    else
      log "${YELLOW}⚠️  无法确认端口监听状态${NC}"
    fi
  fi

  # 列出运行中的容器
  log ""
  log "📦 运行中的容器:"
  docker ps --format "   {{.Names}}: {{.Status}}" 2>/dev/null || true

  log "${GREEN}✅ 部署验证完成${NC}"
}

# 启动
start() {
  log "🚀 启动服务..."

  cd "$INSTALL_DIR/docker"

  if docker compose version &> /dev/null; then
    docker compose up -d
  else
    docker-compose up -d
  fi

  # 验证部署
  verify_deployment

  log "${GREEN}✅ OpenClaw 启动完成！${NC}"
  echo ""
  echo "📍 访问地址:"
  echo "   Gateway: http://localhost:2026"
  echo "   Web UI:  http://localhost:3000"
  echo ""
  echo "📝 下一步:"
  echo "   1. 编辑 $INSTALL_DIR/docker/.env 填入 API Keys"
  echo "   2. 运行: docker compose restart"
}

# 主流程
main() {
  check_system
  TMP_DIR=$(download_package)
  "$DEPLOY_DIR/handle_conflict.sh" --mode "$MODE" --target "$INSTALL_DIR" --source "$TMP_DIR"
  configure
  start
}

main "$@"
