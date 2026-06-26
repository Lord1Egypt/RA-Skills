#!/bin/bash
# 远程部署脚本

set -euo pipefail

HOST=""
USER=""
PORT=22
PASSWORD=""
KEY=""
PACKAGE="./openclaw-deploy.tar.gz"
INSTALL_DIR="/opt/openclaw"
MODE="cover"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "$1"; }
err() { echo -e "${RED}❌ $1${NC}"; }

usage() {
  cat <<EOF
Usage: $0 --host <host> --user <user> [--password <pwd>|--key <path>] [--port 22]
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
    -h|--help) usage; exit 0;;
    *) err "未知参数: $1"; usage; exit 1;;
  esac
done

if [ -z "$HOST" ] || [ -z "$USER" ]; then
  err "必须提供 --host 和 --user"
  exit 1
fi

if [ ! -f "$PACKAGE" ]; then
  err "部署包不存在: $PACKAGE"
  exit 1
fi

SSH_OPTS=(
  -o "StrictHostKeyChecking=accept-new"
  -o "UserKnownHostsFile=$HOME/.ssh/known_hosts"
  -p "$PORT"
)
SSH_CMD=(ssh "${SSH_OPTS[@]}")
SCP_CMD=(scp "${SSH_OPTS[@]}")

if [ -n "$KEY" ]; then
  SSH_CMD+=( -i "$KEY" )
  SCP_CMD+=( -i "$KEY" )
fi

if [ -n "$PASSWORD" ]; then
  if ! command -v sshpass >/dev/null 2>&1; then
    err "使用密码登录需要安装 sshpass"
    exit 1
  fi
  SSH_CMD=(sshpass -p "$PASSWORD" ssh "${SSH_OPTS[@]}")
  SCP_CMD=(sshpass -p "$PASSWORD" scp "${SSH_OPTS[@]}")
fi

log "📋 远程环境检测..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/check_env.sh" --host "$HOST" --user "$USER" --port "$PORT" ${PASSWORD:+--password "$PASSWORD"} ${KEY:+--key "$KEY"}

REMOTE_PKG="/tmp/openclaw-deploy.tar.gz"
REMOTE_SHA="/tmp/openclaw-deploy.tar.gz.sha256"
REMOTE_TMP="/tmp/openclaw-deploy-$(date +%s)"

log "📤 上传部署包到远程: $REMOTE_PKG"
"${SCP_CMD[@]}" "$PACKAGE" "$USER@$HOST:$REMOTE_PKG"

if [ -f "${PACKAGE}.sha256" ]; then
  log "📤 上传 SHA256 文件到远程: $REMOTE_SHA"
  "${SCP_CMD[@]}" "${PACKAGE}.sha256" "$USER@$HOST:$REMOTE_SHA"
fi

log "🚀 开始远程部署..."
REMOTE_CMD=(
  "INSTALL_DIR=$(printf %q "$INSTALL_DIR")"
  "REMOTE_PKG=$(printf %q "$REMOTE_PKG")"
  "REMOTE_SHA=$(printf %q "$REMOTE_SHA")"
  "REMOTE_TMP=$(printf %q "$REMOTE_TMP")"
  "MODE=$(printf %q "$MODE")"
  "bash -s"
)
"${SSH_CMD[@]}" "$USER@$HOST" "${REMOTE_CMD[*]}" <<'REMOTE'
set -euo pipefail

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
    echo "⚠️  未找到 SHA256 文件，跳过校验: $sha_file"
    return 0
  fi

  local cmd
  cmd="$(sha256_cmd)"
  local expected
  expected="$(awk '{print $1}' "$sha_file" | head -n1)"
  local actual
  actual="$($cmd "$pkg" | awk '{print $1}')"

  if [ -z "$expected" ] || [ -z "$actual" ]; then
    echo "❌ SHA256 校验失败：无法读取校验值"
    exit 1
  fi

  if [ "$expected" != "$actual" ]; then
    echo "❌ SHA256 校验失败：文件可能被篡改"
    exit 1
  fi

  echo "✅ SHA256 校验通过"
}

mkdir -p "${REMOTE_TMP}"

# 解压
if [ -f "${REMOTE_PKG}" ]; then
  verify_sha "${REMOTE_PKG}" "${REMOTE_SHA}"
  tar -xzf "${REMOTE_PKG}" -C "${REMOTE_TMP}"
else
  echo "❌ 远程部署包不存在"
  exit 1
fi

# 冲突处理
HANDLE_SCRIPT="${REMOTE_TMP}/scripts/deploy/handle_conflict.sh"
if [ ! -f "${HANDLE_SCRIPT}" ]; then
  echo "❌ 未找到冲突处理脚本: ${HANDLE_SCRIPT}"
  exit 1
fi
chmod +x "${HANDLE_SCRIPT}"
"${HANDLE_SCRIPT}" --mode "${MODE}" --target "${INSTALL_DIR}" --source "${REMOTE_TMP}"

# 配置
if [ -f "${INSTALL_DIR}/docker/.env.example" ] && [ ! -f "${INSTALL_DIR}/docker/.env" ]; then
  cp "${INSTALL_DIR}/docker/.env.example" "${INSTALL_DIR}/docker/.env"
  echo "⚠️  请编辑 ${INSTALL_DIR}/docker/.env 填入 API Keys"
fi
mkdir -p "${INSTALL_DIR}/data/openclaw" "${INSTALL_DIR}/data/workspace"

# 启动
cd "${INSTALL_DIR}/docker"
if docker compose version >/dev/null 2>&1; then
  docker compose up -d
else
  docker-compose up -d
fi

echo "✅ 远程部署完成"
REMOTE

log "${GREEN}✅ 远程部署完成${NC}"
