#!/usr/bin/env bash
set -euo pipefail

# OpenClaw 备份配置健康检查
# 检查备份环境配置是否完整、可用

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
  WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR}"
else
  WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
fi

HOME_DIR="${HOME}"
STATE_DIR="${HOME_DIR}/.openclaw"
BACKUP_ROOT="${WORKSPACE_DIR}/backups/openclaw"

ENV_FILE="${WORKSPACE_DIR}/.env.backup"
SECRET_FILE="${WORKSPACE_DIR}/.env.backup.secret"

CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

log() { printf '[health] %s\n' "$*"; }
pass() { printf '  ✅ %s\n' "$*"; CHECKS_PASSED=$((CHECKS_PASSED + 1)); }
fail() { printf '  ❌ %s\n' "$*"; CHECKS_FAILED=$((CHECKS_FAILED + 1)); }
warn() { printf '  ⚠️  %s\n' "$*"; WARNINGS=$((WARNINGS + 1)); }

need_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

echo ""
echo "🔍 OpenClaw Backup Health Check"
echo "================================"
echo ""

# 1. 检查基础环境
log "Checking base environment..."

if [[ -d "${WORKSPACE_DIR}" ]]; then
  pass "Workspace directory exists: ${WORKSPACE_DIR}"
else
  fail "Workspace directory missing: ${WORKSPACE_DIR}"
fi

if [[ -d "${STATE_DIR}" ]]; then
  pass "OpenClaw state directory exists: ${STATE_DIR}"
else
  fail "OpenClaw state directory missing: ${STATE_DIR}"
fi

if [[ -f "${STATE_DIR}/openclaw.json" ]]; then
  pass "openclaw.json exists"
else
  warn "openclaw.json not found (will be created on first run)"
fi

if [[ -d "${STATE_DIR}/extensions" ]]; then
  pass "Extensions directory exists"
else
  warn "Extensions directory not found"
fi

echo ""

# 2. 检查备份目录
log "Checking backup infrastructure..."

if [[ -d "${BACKUP_ROOT}" ]]; then
  pass "Backup root directory exists: ${BACKUP_ROOT}"
  
  # 检查备份数量
  backup_count=$(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d ! -name ".snapshots" | wc -l)
  if [[ ${backup_count} -gt 0 ]]; then
    pass "Found ${backup_count} backup(s)"
  else
    warn "No backups found yet"
  fi
  
  # 检查快照目录
  if [[ -d "${BACKUP_ROOT}/.snapshots" ]]; then
    pass "Snapshot directory exists"
    
    # 检查快照文件
    if [[ -f "${BACKUP_ROOT}/.snapshots/level-0.snapshot" ]]; then
      pass "Level-0 snapshot exists"
    fi
    if [[ -f "${BACKUP_ROOT}/.snapshots/level-1.snapshot" ]]; then
      pass "Level-1 snapshot exists"
    fi
  else
    warn "Snapshot directory not found (will be created on first backup)"
  fi
else
  warn "Backup root directory not found (will be created on first backup): ${BACKUP_ROOT}"
fi

echo ""

# 3. 检查依赖命令
log "Checking dependencies..."

if need_cmd tar; then
  pass "tar command available"
else
  fail "tar command missing"
fi

if need_cmd curl; then
  pass "curl command available"
else
  warn "curl command missing (required for WebDAV upload)"
fi

if need_cmd openssl; then
  pass "openssl command available"
else
  warn "openssl command missing (required for config encryption)"
fi

echo ""

# 4. 检查配置文件
log "Checking configuration files..."

if [[ -f "${ENV_FILE}" ]]; then
  pass "Backup env file exists: ${ENV_FILE}"
  
  # 检查变量（不显示值，只检查存在性）
  # shellcheck source=/dev/null
  source "${ENV_FILE}" 2>/dev/null || true
  
  if [[ -n "${WEBDAV_URL:-}" ]]; then
    pass "WEBDAV_URL configured"
  else
    warn "WEBDAV_URL not set"
  fi
  
  if [[ -n "${WEBDAV_USER:-}" ]]; then
    pass "WEBDAV_USER configured"
  else
    warn "WEBDAV_USER not set"
  fi
  
  if [[ -n "${WEBDAV_PASS:-}" ]]; then
    pass "WEBDAV_PASS configured (hidden)"
  else
    warn "WEBDAV_PASS not set"
  fi
  
  if [[ -n "${REMOTE_KEEP:-}" ]]; then
    pass "REMOTE_KEEP configured: ${REMOTE_KEEP}"
  else
    warn "REMOTE_KEEP not set (will use default: 7)"
  fi
  
  if [[ -n "${LOCAL_KEEP:-}" ]]; then
    pass "LOCAL_KEEP configured: ${LOCAL_KEEP}"
  else
    warn "LOCAL_KEEP not set (will use default: 7)"
  fi
else
  warn "Backup env file not found: ${ENV_FILE}"
  warn "Create it for WebDAV upload support"
fi

if [[ -f "${SECRET_FILE}" ]]; then
  pass "Secret file exists: ${SECRET_FILE}"
  
  # 检查加密密码
  # shellcheck source=/dev/null
  source "${SECRET_FILE}" 2>/dev/null || true
  if [[ -n "${BACKUP_ENCRYPT_PASS:-}" ]]; then
    pass "BACKUP_ENCRYPT_PASS configured (hidden)"
  else
    warn "BACKUP_ENCRYPT_PASS not set in secret file"
  fi
else
  warn "Secret file not found: ${SECRET_FILE}"
  warn "Create it for config encryption support"
fi

echo ""

# 5. 检查现有备份完整性
log "Checking existing backup integrity..."

if [[ -d "${BACKUP_ROOT}" ]]; then
  corrupted=0
  checked=0
  
  while IFS= read -r -d '' backup_dir; do
    name=$(basename "${backup_dir}")
    [[ "${name}" == ".snapshots" ]] && continue
    
    if [[ -f "${backup_dir}/workspace.tar.gz" ]]; then
      checked=$((checked + 1))
      if tar -tzf "${backup_dir}/workspace.tar.gz" >/dev/null 2>&1; then
        : # OK
      else
        corrupted=$((corrupted + 1))
        fail "Corrupted workspace.tar.gz in ${name}"
      fi
    elif [[ -f "${backup_dir}/workspace.tar.zst" ]]; then
      checked=$((checked + 1))
      if tar --zstd -tf "${backup_dir}/workspace.tar.zst" >/dev/null 2>&1; then
        : # OK
      else
        corrupted=$((corrupted + 1))
        fail "Corrupted workspace.tar.zst in ${name}"
      fi
    fi
    
    if [[ -f "${backup_dir}/extensions.tar.gz" ]]; then
      checked=$((checked + 1))
      if tar -tzf "${backup_dir}/extensions.tar.gz" >/dev/null 2>&1; then
        : # OK
      else
        corrupted=$((corrupted + 1))
        fail "Corrupted extensions.tar.gz in ${name}"
      fi
    elif [[ -f "${backup_dir}/extensions.tar.zst" ]]; then
      checked=$((checked + 1))
      if tar --zstd -tf "${backup_dir}/extensions.tar.zst" >/dev/null 2>&1; then
        : # OK
      else
        corrupted=$((corrupted + 1))
        fail "Corrupted extensions.tar.zst in ${name}"
      fi
    fi
  done < <(find "${BACKUP_ROOT}" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)
  
  if [[ ${checked} -gt 0 && ${corrupted} -eq 0 ]]; then
    pass "All ${checked} archive(s) are valid"
  elif [[ ${checked} -eq 0 ]]; then
    warn "No archives to check"
  fi
fi

echo ""
echo "================================"
echo "Health Check Summary"
echo "================================"
printf '  ✅ Passed:  %d\n' "${CHECKS_PASSED}"
printf '  ⚠️  Warnings: %d\n' "${WARNINGS}"
printf '  ❌ Failed:   %d\n' "${CHECKS_FAILED}"
echo ""

if [[ ${CHECKS_FAILED} -eq 0 ]]; then
  echo "✅ Health check completed with no errors"
  exit 0
else
  echo "❌ Health check found ${CHECKS_FAILED} error(s)"
  exit 1
fi
