#!/bin/bash
# 环境检测脚本
# 支持本地或远程检测

set -euo pipefail

HOST=""
USER=""
PORT=22
PASSWORD=""
KEY=""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "$1"; }

usage() {
  cat <<EOF
Usage: $0 [--host <host> --user <user> --password <pwd>|--key <path> --port <port>]
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --host) HOST="$2"; shift 2;;
    --user) USER="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --password) PASSWORD="$2"; shift 2;;
    --key) KEY="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) log "${RED}未知参数: $1${NC}"; usage; exit 1;;
  esac
done

run_local_check() {
  log "📋 检测系统环境..."

  SYS_UNAME=$(uname -s)
  OS_NAME="Unknown"
  if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_NAME=${ID:-Unknown}
  else
    case "$SYS_UNAME" in
      *MINGW*|*MSYS*|*CYGWIN*) OS_NAME="Windows";;
      *) OS_NAME="$SYS_UNAME";;
    esac
  fi

  log "🖥️  系统: $OS_NAME"

  if command -v docker >/dev/null 2>&1; then
    log "${GREEN}✅ Docker 已安装${NC}"
  else
    log "${YELLOW}⚠️  Docker 未安装${NC}"
    case "$OS_NAME" in
      ubuntu|debian)
        log "   建议: curl -fsSL https://get.docker.com | sh";;
      centos|rhel|rocky|almalinux)
        log "   建议: yum install -y docker && systemctl enable --now docker";;
      *)
        log "   建议: 参考 Docker 官方安装文档";;
    esac
  fi

  if command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1; then
    log "${GREEN}✅ docker-compose 可用${NC}"
  else
    log "${YELLOW}⚠️  docker-compose 不可用${NC}"
    log "   建议: 安装 Docker Compose v2 或 docker-compose" 
  fi

  for dep in tar curl; do
    if command -v "$dep" >/dev/null 2>&1; then
      log "${GREEN}✅ $dep 已安装${NC}"
    else
      log "${YELLOW}⚠️  $dep 未安装${NC}"
    fi
  done

  log "✅ 环境检测完成"
}

run_remote_check() {
  if [ -z "$HOST" ] || [ -z "$USER" ]; then
    log "${RED}缺少 --host 或 --user${NC}"
    exit 1
  fi

  SSH_OPTS="-o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$HOME/.ssh/known_hosts -p $PORT"
  SSH_CMD=(ssh $SSH_OPTS)

  if [ -n "$KEY" ]; then
    SSH_CMD+=( -i "$KEY" )
  fi

  if [ -n "$PASSWORD" ]; then
    if ! command -v sshpass >/dev/null 2>&1; then
      log "${RED}需要 sshpass 以支持密码登录${NC}"
      exit 1
    fi
    SSH_CMD=(sshpass -p "$PASSWORD" ssh $SSH_OPTS)
  fi

  log "📋 远程环境检测: $USER@$HOST:$PORT"

  "${SSH_CMD[@]}" "$USER@$HOST" 'bash -s' <<'REMOTE'
set -e

log() { echo -e "$1"; }

SYS_UNAME=$(uname -s)
OS_NAME="Unknown"
if [ -f /etc/os-release ]; then
  . /etc/os-release
  OS_NAME=${ID:-Unknown}
else
  case "$SYS_UNAME" in
    *MINGW*|*MSYS*|*CYGWIN*) OS_NAME="Windows";;
    *) OS_NAME="$SYS_UNAME";;
  esac
fi

log "🖥️  系统: $OS_NAME"

if command -v docker >/dev/null 2>&1; then
  log "✅ Docker 已安装"
else
  log "⚠️  Docker 未安装"
  case "$OS_NAME" in
    ubuntu|debian)
      log "   建议: curl -fsSL https://get.docker.com | sh";;
    centos|rhel|rocky|almalinux)
      log "   建议: yum install -y docker && systemctl enable --now docker";;
    *)
      log "   建议: 参考 Docker 官方安装文档";;
  esac
fi

if command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1; then
  log "✅ docker-compose 可用"
else
  log "⚠️  docker-compose 不可用"
  log "   建议: 安装 Docker Compose v2 或 docker-compose"
fi

for dep in tar curl; do
  if command -v "$dep" >/dev/null 2>&1; then
    log "✅ $dep 已安装"
  else
    log "⚠️  $dep 未安装"
  fi
done

log "✅ 环境检测完成"
REMOTE
}

if [ -n "$HOST" ]; then
  run_remote_check
else
  run_local_check
fi
