#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

UPLOAD=0
DRY_RUN=0
ENCRYPT_CONFIG=0
LOCAL_KEEP="${LOCAL_KEEP:-7}"
REMOTE_KEEP="${REMOTE_KEEP:-7}"
BACKUP_LEVEL="${BACKUP_LEVEL:-auto}"
BACKUP_STRATEGY="${BACKUP_STRATEGY:-daily}"
BACKUP_COMPRESS="${BACKUP_COMPRESS:-gzip}"  # gzip or zstd

# Upload retry configuration
UPLOAD_MAX_RETRIES="${UPLOAD_MAX_RETRIES:-3}"
UPLOAD_RETRY_DELAY_BASE="${UPLOAD_RETRY_DELAY_BASE:-2}"  # Base delay in seconds (exponential: 2, 4, 8...)

# Parallel compression configuration
PARALLEL_JOBS="${PARALLEL_JOBS:-$(nproc 2>/dev/null || echo 4)}"  # Auto-detect CPU cores, default 4

# Detect available compression tools (prefer parallel versions)
detect_compressor() {
  case "$BACKUP_COMPRESS" in
    pzstd|zstd)
      if command -v pzstd >/dev/null 2>&1; then
        echo "pzstd"
      elif command -v zstd >/dev/null 2>&1; then
        echo "zstd"
      else
        echo "gzip"
      fi
      ;;
    pigz|gzip)
      if command -v pigz >/dev/null 2>&1; then
        echo "pigz"
      elif command -v gzip >/dev/null 2>&1; then
        echo "gzip"
      else
        echo "cat"  # Fallback to no compression
      fi
      ;;
    *)
      if command -v pigz >/dev/null 2>&1; then
        echo "pigz"
      elif command -v gzip >/dev/null 2>&1; then
        echo "gzip"
      else
        echo "cat"  # Fallback to no compression
      fi
      ;;
  esac
}

# Get tar compression options
get_tar_compress_opts() {
  local compressor="$1"
  case "$compressor" in
    zstd) echo "--zstd" ;;
    gzip|pigz) echo "z" ;;
    *) echo "" ;;
  esac
}

# Get file extension for compressed archives
get_compress_ext() {
  local compressor="$1"
  case "$compressor" in
    zstd|pzstd) echo "tar.zst" ;;
    gzip|pigz) echo "tar.gz" ;;
    *) echo "tar" ;;
  esac
}

# Get compression program for tar (for parallel compressors)
get_tar_compress_program() {
  local compressor="$1"
  case "$compressor" in
    pigz) echo "pigz -p ${PARALLEL_JOBS}" ;;
    pzstd) echo "pzstd -p ${PARALLEL_JOBS}" ;;
    *) echo "" ;;
  esac
}

# Build a single tar --use-compress-program flag from program+args
# Returns empty string if no compress program is needed
build_compress_flag() {
  local compress_prog="$1"
  local compress_opt="$2"
  if [[ -n "$compress_prog" ]]; then
    echo "--use-compress-program=${compress_prog}"
  elif [[ -n "$compress_opt" ]]; then
    # compress_opt is 'z' or '--zstd' -- prepend dash when needed
    if [[ "$compress_opt" == "z" ]]; then
      echo "-z"
    else
      echo "$compress_opt"
    fi
  fi
}

for arg in "$@"; do
  case "$arg" in
    --upload) UPLOAD=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --encrypt-config) ENCRYPT_CONFIG=1 ;;
    --compress=*) BACKUP_COMPRESS="${arg#*=}" ;;
    --jobs=?*) PARALLEL_JOBS="${arg#*=}" ;;
    --level=?*) BACKUP_LEVEL="${arg#*=}" ;;
    --strategy=?*) BACKUP_STRATEGY="${arg#*=}" ;;
    --level) echo "Usage: --level=0|1|2|auto" >&2; exit 1 ;;
    --strategy) echo "Usage: --strategy=hourly|daily|weekly|smart" >&2; exit 1 ;;
    --compress) echo "Usage: --compress=gzip|pigz|zstd|pzstd" >&2; exit 1 ;;
    --jobs) echo "Usage: --jobs=N (number of parallel compression threads)" >&2; exit 1 ;;
    *) echo "Unknown argument: $arg" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
  WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR}"
else
  WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
fi
HOME_DIR="${HOME}"
STATE_DIR="${HOME_DIR}/.openclaw"
CONFIG_FILE="${STATE_DIR}/openclaw.json"
EXTENSIONS_DIR="${STATE_DIR}/extensions"
BACKUP_ROOT="${WORKSPACE_DIR}/backups/openclaw"
TS="$(date +%F-%H%M%S)"
RUN_DIR="${BACKUP_ROOT}/${TS}"
LATEST_LINK="${BACKUP_ROOT}/latest"

# === Incremental Backup Functions ===

SNAPSHOT_DIR="${BACKUP_ROOT}/.snapshots"

# Lock file for concurrent backup prevention
 acquire_backup_lock() {
  local lock_file="${SNAPSHOT_DIR}/.backup.lock"
  local lock_fd=200
  
  mkdir -p "${SNAPSHOT_DIR}"
  
  # Open lock file
  eval "exec ${lock_fd}>\"${lock_file}\"" || return 1
  
  # Try to acquire exclusive lock with timeout
  if ! flock -x -w 30 "${lock_fd}"; then
    log "ERROR: Could not acquire backup lock (another backup is running)"
    return 1
  fi
  
  # Store fd for later release
  export BACKUP_LOCK_FD="${lock_fd}"
  return 0
}

# Release backup lock
release_backup_lock() {
  if [[ -n "${BACKUP_LOCK_FD:-}" ]]; then
    flock -u "${BACKUP_LOCK_FD}" 2>/dev/null || true
    eval "exec ${BACKUP_LOCK_FD}>&-" 2>/dev/null || true
    unset BACKUP_LOCK_FD
  fi
}

# Determine backup level based on strategy and existing snapshots
determine_backup_level() {
  local strategy="$1"
  local level="${BACKUP_LEVEL}"
  
  # If level explicitly set, use it
  if [[ "$level" != "auto" ]]; then
    echo "$level"
    return
  fi
  
  # Auto-determine based on strategy
  case "$strategy" in
    weekly)
      # Always level 0 (full) for weekly
      echo "0"
      ;;
    daily)
      # Check if we have a level 0 snapshot from this week
      if [[ -f "${SNAPSHOT_DIR}/level-0.snapshot" ]]; then
        echo "1"
      else
        echo "0"
      fi
      ;;
    hourly)
      # Level 2 if we have level 1, else level 1 if we have level 0
      if [[ -f "${SNAPSHOT_DIR}/level-1.snapshot" ]]; then
        echo "2"
      elif [[ -f "${SNAPSHOT_DIR}/level-0.snapshot" ]]; then
        echo "1"
      else
        echo "0"
      fi
      ;;
    smart)
      # Sunday = level 0, other days = level 1
      local weekday
      weekday=$(date +%u)  # 1=Monday, 7=Sunday
      if [[ "$weekday" == "7" ]]; then
        echo "0"
      else
        echo "1"
      fi
      ;;
    *)
      # Default: level 0 (full)
      echo "0"
      ;;
  esac
}

# Create tar archive with incremental support
create_incremental_archive() {
  local level="$1"
  local source_dir="$2"
  local output_file="$3"
  local name="$4"
  
  # Acquire lock for snapshot operations
  if ! acquire_backup_lock; then
    log "ERROR: Failed to acquire backup lock"
    return 1
  fi
  
  # Ensure lock is released on exit (use subshell to isolate trap)
  local old_trap
  old_trap=$(trap -p EXIT)
  # Export for the trap to access
  export _OLD_TRAP="${old_trap}"
  trap 'release_backup_lock; eval "${_OLD_TRAP:-}"' EXIT
  
  # Detect and use preferred compression
  local compressor compress_opt compress_prog
  compressor=$(detect_compressor)
  compress_opt=$(get_tar_compress_opts "$compressor")
  compress_prog=$(get_tar_compress_program "$compressor")
  local compress_flag
  compress_flag=$(build_compress_flag "$compress_prog" "$compress_opt")
  
  if [[ "$compressor" == "pigz" || "$compressor" == "pzstd" ]]; then
    log "Using parallel compression: $compressor (${PARALLEL_JOBS} threads)"
  else
    log "Using compression: $compressor"
  fi
  
  mkdir -p "${SNAPSHOT_DIR}"
  local snapshot_file="${SNAPSHOT_DIR}/level-${level}.snapshot"
  
  log "Creating ${name} archive (level ${level})..."
  
  if [[ "$level" == "0" ]]; then
    # Full backup: remove old snapshots
    rm -f "${SNAPSHOT_DIR}"/level-*.snapshot
    snapshot_file="${SNAPSHOT_DIR}/level-0.snapshot"
    (cd "${source_dir}" && tar --exclude='node_modules' --exclude='.git' --exclude='backups/openclaw' --exclude='.env.backup' --exclude='.env.backup.secret' \
        --listed-incremental="${snapshot_file}" \
        ${compress_flag:+"$compress_flag"} -cf "${output_file}" .)
  else
    # Incremental backup: reference previous level
    local prev_level=$((level - 1))
    local prev_snapshot="${SNAPSHOT_DIR}/level-${prev_level}.snapshot"
    
    if [[ ! -f "$prev_snapshot" ]]; then
      log "Warning: Level ${prev_level} snapshot not found, falling back to level 0"
      snapshot_file="${SNAPSHOT_DIR}/level-0.snapshot"
      (cd "${source_dir}" && tar --exclude='node_modules' --exclude='.git' --exclude='backups/openclaw' --exclude='.env.backup' --exclude='.env.backup.secret' \
          --listed-incremental="${snapshot_file}" \
          ${compress_flag:+"$compress_flag"} -cf "${output_file}" .)
    else
      # Use previous snapshot as reference, create new snapshot for this level
      (cd "${source_dir}" && tar --exclude='node_modules' --exclude='.git' --exclude='backups/openclaw' --exclude='.env.backup' --exclude='.env.backup.secret' \
          --listed-incremental="${snapshot_file}" \
          ${compress_flag:+"$compress_flag"} -cf "${output_file}" .)
    fi
  fi
  
  # Save metadata
  echo "level=${level}" > "${RUN_DIR}/${name}.meta"
  echo "snapshot=${snapshot_file}" >> "${RUN_DIR}/${name}.meta"
  
  # Reset trap and release lock before returning
  trap - EXIT
  release_backup_lock
}

# === Checksum Generation ===

generate_checksums() {
  local backup_dir="$1"
  local checksum_file="${backup_dir}/checksums.sha256"
  
  log "Generating SHA-256 checksums..."
  
  (
    cd "$backup_dir" || exit 1
    sha256sum workspace.tar.gz 2>/dev/null || true
    sha256sum extensions.tar.gz 2>/dev/null || true
    sha256sum manifest.txt 2>/dev/null || true
  ) > "$checksum_file"
  
  log "  ✅ Checksums written to checksums.sha256"
}

verify_checksums() {
  local backup_dir="$1"
  local checksum_file="${backup_dir}/checksums.sha256"
  
  if [[ ! -f "$checksum_file" ]]; then
    log "  ⚠️ No checksums file found"
    return 0
  fi
  
  log "Verifying SHA-256 checksums..."
  
  local errors=0
  while IFS= read -r line; do
    local expected_hash filename
    expected_hash=$(echo "$line" | awk '{print $1}')
    filename=$(echo "$line" | awk '{print $2}')
    
    local actual_hash
    actual_hash=$(sha256sum "${backup_dir}/${filename}" 2>/dev/null | awk '{print $1}')
    
    if [[ "$expected_hash" == "$actual_hash" ]]; then
      log "  ✅ ${filename}"
    else
      log "  ❌ ${filename}: checksum mismatch"
      errors=$((errors + 1))
    fi
  done < "$checksum_file"
  
  if [[ ${errors} -gt 0 ]]; then
    log "ERROR: ${errors} file(s) failed checksum verification"
    return 1
  fi
  
  return 0
}

# === Integrity Verification ===

verify_backup_integrity() {
  local backup_dir="$1"
  local errors=0
  
  log "Checking archive integrity..."
  
  # Helper: verify tar archive with correct decompression flags
  verify_tar_archive() {
    local archive="$1"
    local basename="$(basename "$archive")"
    if [[ "$archive" == *.tar.zst ]]; then
      tar --zstd -tf "$archive" >/dev/null 2>&1
    else
      tar -tzf "$archive" >/dev/null 2>&1
    fi
    local rc=$?
    if [[ $rc -eq 0 ]]; then
      log "  ✅ $basename is valid"
    else
      log "  ❌ $basename is corrupted"
    fi
    return $rc
  }
  
  # Check workspace archive
  if [[ -f "${backup_dir}/workspace.tar.gz" ]]; then
    verify_tar_archive "${backup_dir}/workspace.tar.gz" || errors=$((errors + 1))
  elif [[ -f "${backup_dir}/workspace.tar.zst" ]]; then
    verify_tar_archive "${backup_dir}/workspace.tar.zst" || errors=$((errors + 1))
  else
    log "  ❌ workspace archive is missing"
    errors=$((errors + 1))
  fi
  
  # Check extensions archive (optional)
  if [[ -f "${backup_dir}/extensions.tar.gz" ]]; then
    verify_tar_archive "${backup_dir}/extensions.tar.gz" || errors=$((errors + 1))
  elif [[ -f "${backup_dir}/extensions.tar.zst" ]]; then
    verify_tar_archive "${backup_dir}/extensions.tar.zst" || errors=$((errors + 1))
  fi
  
  # Check manifest
  if [[ -f "${backup_dir}/manifest.txt" ]]; then
    log "  ✅ manifest.txt exists"
  else
    log "  ⚠️ manifest.txt is missing"
  fi
  
  # Check metadata
  if [[ -f "${backup_dir}/workspace.meta" ]]; then
    log "  ✅ workspace.meta exists"
  else
    log "  ⚠️ workspace.meta is missing"
  fi
  
  # Check checksums if available
  if [[ -f "${backup_dir}/checksums.sha256" ]]; then
    verify_checksums "$backup_dir" || errors=$((errors + 1))
  fi
  
  if [[ ${errors} -gt 0 ]]; then
    log "Integrity check failed with ${errors} error(s)"
    return 1
  fi
  
  log "✅ All integrity checks passed"
  return 0
}

# === Rotation Functions (defined before use) ===

rotate_local_backups() {
  local root="$1"
  local keep="$2"
  [[ -d "$root" ]] || return 0
  
  # Safety: Validate root is within expected backup directory
  local canonical_root
  canonical_root=$(cd "$root" && pwd) || return 1
  if [[ ! "$canonical_root" =~ /backups/openclaw$ ]]; then
    log "ERROR: rotate_local_backups: root directory '$root' is not a valid backup directory"
    return 1
  fi
  
  mapfile -t dirs < <(find "$root" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}$' | sort)
  local count=${#dirs[@]}
  if (( count <= keep )); then
    return 0
  fi
  local remove_count=$((count - keep))
  for d in "${dirs[@]:0:remove_count}"; do
    # Safety: Validate directory name format and existence
    local full_path="$canonical_root/$d"
    if [[ -d "$full_path" ]] && [[ "$d" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}$ ]]; then
      rm -rf -- "$full_path"
      log "Rotated: $d"
    else
      log "WARNING: Skipping invalid backup directory: $d"
    fi
  done
}

webdav_list_dirs() {
  local url="$1"
  local error_file="${TEMP_DIR:-/tmp}/webdav_error_$$.txt"
  local response
  
  response=$(curl --silent --show-error -u "${WEBDAV_USER}:${WEBDAV_PASS}" -X PROPFIND -H 'Depth: 1' "$url" 2>"${error_file}") || {
    local curl_error=$(cat "${error_file}" 2>/dev/null || echo "unknown error")
    log "ERROR: WebDAV PROPFIND failed for $url: $curl_error"
    rm -f "${error_file}"
    return 1
  }
  rm -f "${error_file}"
  echo "$response"
}

webdav_delete_dir() {
  local url="$1"
  if [[ ${DRY_RUN} -eq 1 ]]; then
    log "DRY RUN delete remote dir: ${url}"
    return 0
  fi
  
  local error_file="${TEMP_DIR:-/tmp}/webdav_error_$$.txt"
  local http_code
  
  http_code=$(curl --silent --show-error -o /dev/null -w "%{http_code}" -u "${WEBDAV_USER}:${WEBDAV_PASS}" -X DELETE "$url" 2>"${error_file}") || {
    local curl_error=$(cat "${error_file}" 2>/dev/null || echo "unknown error")
    log "ERROR: WebDAV DELETE failed for $url: HTTP $http_code - $curl_error"
    rm -f "${error_file}"
    return 1
  }
  rm -f "${error_file}"
  
  if [[ "$http_code" != "200" && "$http_code" != "202" && "$http_code" != "204" ]]; then
    log "WARNING: WebDAV DELETE returned HTTP $http_code for $url"
    return 1
  fi
  return 0
}

rotate_remote_backups() {
  local root="$1"
  local keep="$2"
  local xml
  xml=$(webdav_list_dirs "$root") || return 0
  mapfile -t names < <(printf '%s' "$xml" | grep -oP '(?<=<d:href>)[^<]+' | sed 's#/$##' | awk -F'/' 'NF{print $NF}' | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}$' | sort -u)
  local count=${#names[@]}
  if (( count <= keep )); then
    return 0
  fi
  local remove_count=$((count - keep))
  for d in "${names[@]:0:remove_count}"; do
    webdav_delete_dir "$root/$d"
  done
}

# === End Rotation Functions ===

mkdir -p "${RUN_DIR}"
mkdir -p "${SNAPSHOT_DIR}"
mkdir -p "${SNAPSHOT_DIR}"

WORKSPACE_ARCHIVE="${RUN_DIR}/workspace.tar.gz"
EXTENSIONS_ARCHIVE="${RUN_DIR}/extensions.tar.gz"
CONFIG_COPY="${RUN_DIR}/openclaw.json"
CONFIG_ENC="${RUN_DIR}/openclaw.json.enc"
RESTORE_NOTE="${RUN_DIR}/RESTORE-NOTES.txt"
MANIFEST="${RUN_DIR}/manifest.txt"
NOTIFY_SUMMARY="${RUN_DIR}/notify.txt"
NOTIFY_SCRIPT="${WORKSPACE_DIR}/skills/openclaw-webdav-backup/scripts/openclaw-backup-notify.impl.sh"
FAILED_STAGE="initializing"

log() { printf '[backup] %s\n' "$*"; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }; }

send_notify() {
  local status="$1"
  [[ -x "$NOTIFY_SCRIPT" || -f "$NOTIFY_SCRIPT" ]] || return 0
  /usr/bin/bash "$NOTIFY_SCRIPT" "$status" "$NOTIFY_SUMMARY" || true
}

write_success_summary() {
  local level_str="level-${CURRENT_LEVEL}"
  if [[ "${BACKUP_STRATEGY}" != "daily" || "${CURRENT_LEVEL}" != "0" ]]; then
    level_str="${BACKUP_STRATEGY} ${level_str}"
  fi
  cat > "$NOTIFY_SUMMARY" <<EOF
✅ OpenClaw backup succeeded
Time: ${TS}
Type: ${level_str}
Local dir: ${RUN_DIR}
Encrypted config: $([[ ${ENCRYPT_CONFIG} -eq 1 ]] && echo yes || echo no)
WebDAV upload: $([[ ${UPLOAD} -eq 1 ]] && echo yes || echo no)
Retention: local ${LOCAL_KEEP}, remote ${REMOTE_KEEP}
EOF
}

write_failure_summary() {
  cat > "$NOTIFY_SUMMARY" <<EOF
❌ OpenClaw backup failed
Time: ${TS}
Stage: ${FAILED_STAGE}
Local dir: ${RUN_DIR}
Encrypted config: $([[ ${ENCRYPT_CONFIG} -eq 1 ]] && echo yes || echo no)
WebDAV upload: $([[ ${UPLOAD} -eq 1 ]] && echo yes || echo no)
Hint: check cron log or rerun manually for details
EOF
}

on_error() {
  write_failure_summary
  send_notify failure
}

trap on_error ERR

resolve_encrypt_pass() {
  if [[ -n "${BACKUP_ENCRYPT_PASS:-}" ]]; then
    return 0
  fi
  local secret_file="${WORKSPACE_DIR}/.env.backup.secret"
  if [[ -f "${secret_file}" ]]; then
    # shellcheck disable=SC1090
    source "${secret_file}"
  fi
  if [[ -n "${BACKUP_ENCRYPT_PASS:-}" ]]; then
    export BACKUP_ENCRYPT_PASS
    return 0
  fi
  if [[ -t 0 ]]; then
    read -r -s -p 'Enter backup encryption password: ' BACKUP_ENCRYPT_PASS
    echo
    [[ -n "${BACKUP_ENCRYPT_PASS}" ]] || { echo "Empty encryption password" >&2; exit 1; }
    export BACKUP_ENCRYPT_PASS
    return 0
  fi
  echo "Missing BACKUP_ENCRYPT_PASS. Set env var, provide .env.backup.secret, or run interactively." >&2
  exit 1
}

need_cmd tar
need_cmd curl

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Config file not found: ${CONFIG_FILE}" >&2
  exit 1
fi

# Determine backup level based on strategy
CURRENT_LEVEL=$(determine_backup_level "${BACKUP_STRATEGY}")
log "Backup strategy: ${BACKUP_STRATEGY}, Level: ${CURRENT_LEVEL}"

FAILED_STAGE="creating workspace archive"
# Pre-backup disk space check
FAILED_STAGE="checking disk space"
log "Checking available disk space"
# Estimate required space: workspace size * 0.3 (compression ratio)
estimated_size_mb=$(du -sm "${WORKSPACE_DIR}" 2>/dev/null | awk '{print int($1 * 0.3) + 50}' || echo 500)
required_space_mb=${estimated_size_mb}

available_mb=$(df -m "${BACKUP_ROOT}" 2>/dev/null | awk 'NR==2 {print $4}' || echo 0)

if [[ ${available_mb} -lt ${required_space_mb} ]]; then
    log "ERROR: Insufficient disk space. Required: ${required_space_mb}MB, Available: ${available_mb}MB"
    exit 1
fi
log "Disk space check passed: ${available_mb}MB available (need ${required_space_mb}MB)"

FAILED_STAGE="creating workspace archive"
log "Creating workspace archive"
# Update extension for zstd/pzstd compression
_work_compressor=$(detect_compressor)
if [[ "$_work_compressor" == "zstd" || "$_work_compressor" == "pzstd" ]]; then
  WORKSPACE_ARCHIVE="${RUN_DIR}/workspace.tar.zst"
fi
create_incremental_archive "${CURRENT_LEVEL}" "${WORKSPACE_DIR}" "${WORKSPACE_ARCHIVE}" "workspace"

if [[ -d "${EXTENSIONS_DIR}" ]]; then
  FAILED_STAGE="creating extensions archive"
  log "Creating extensions archive"
  compressor=$(detect_compressor)
  ext_compress_opt=$(get_tar_compress_opts "$compressor")
  ext_compress_prog=$(get_tar_compress_program "$compressor")
  ext_compress_flag=$(build_compress_flag "$ext_compress_prog" "$ext_compress_opt")
  if [[ "$compressor" == "zstd" || "$compressor" == "pzstd" ]]; then
    EXTENSIONS_ARCHIVE="${RUN_DIR}/extensions.tar.zst"
  fi
  tar ${ext_compress_flag:+"$ext_compress_flag"} -cf "${EXTENSIONS_ARCHIVE}" -C "${STATE_DIR}" extensions
fi

FAILED_STAGE="copying config"
log "Copying config"
cp "${CONFIG_FILE}" "${CONFIG_COPY}"

if [[ ${ENCRYPT_CONFIG} -eq 1 ]]; then
  ENV_FILE="${WORKSPACE_DIR}/.env.backup"
  [[ -f "${ENV_FILE}" ]] || { echo "Missing ${ENV_FILE}" >&2; exit 1; }
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  resolve_encrypt_pass
  : "${BACKUP_ENCRYPT_PASS:?BACKUP_ENCRYPT_PASS is required when --encrypt-config is used}"
  need_cmd openssl
  FAILED_STAGE="encrypting config"
log "Encrypting config copy"
  openssl enc -aes-256-cbc -pbkdf2 -salt -in "${CONFIG_COPY}" -out "${CONFIG_ENC}" -pass env:BACKUP_ENCRYPT_PASS >/dev/null 2>&1
  rm -f "${CONFIG_COPY}"
fi

cat > "${RESTORE_NOTE}" <<NOTE
OpenClaw restore notes
Generated at: ${TS}
Security note: openclaw.json may contain secrets/tokens/API keys.
If encrypted backup is used, decrypt openclaw.json.enc before restore.
NOTE

{
  echo "timestamp=${TS}"
  echo "workspace_archive=$(basename "${WORKSPACE_ARCHIVE}")"
  [[ -f "${EXTENSIONS_ARCHIVE}" ]] && echo "extensions_archive=$(basename "${EXTENSIONS_ARCHIVE}")"
  if [[ -f "${CONFIG_ENC}" ]]; then
    echo "config_encrypted=$(basename "${CONFIG_ENC}")"
  else
    echo "config_copy=$(basename "${CONFIG_COPY}")"
  fi
} > "${MANIFEST}"

ln -sfn "${RUN_DIR}" "${LATEST_LINK}"
log "Backup set created at: ${RUN_DIR}"

# 完整性检查
FAILED_STAGE="verifying backup integrity"
log "Verifying backup integrity"
verify_backup_integrity "${RUN_DIR}"

# 生成校验和
FAILED_STAGE="generating checksums"
generate_checksums "${RUN_DIR}"

FAILED_STAGE="applying local retention"
log "Applying local retention: keep ${LOCAL_KEEP}"
rotate_local_backups "${BACKUP_ROOT}" "${LOCAL_KEEP}"

if [[ ${UPLOAD} -eq 1 ]]; then
  ENV_FILE="${WORKSPACE_DIR}/.env.backup"
  [[ -f "${ENV_FILE}" ]] || { echo "Missing upload env file: ${ENV_FILE}" >&2; exit 1; }
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  : "${WEBDAV_URL:?WEBDAV_URL is required}"
  : "${WEBDAV_USER:?WEBDAV_USER is required}"
  : "${WEBDAV_PASS:?WEBDAV_PASS is required}"

  mkcol_if_needed() {
    local url="$1"
    if [[ ${DRY_RUN} -eq 1 ]]; then
      log "DRY RUN MKCOL ${url}"
      return 0
    fi
    local code
    code=$(curl --silent --show-error -u "${WEBDAV_USER}:${WEBDAV_PASS}" -o /dev/null -w '%{http_code}' -X MKCOL "$url")
    case "$code" in
      201|301|405) return 0 ;;
      *) echo "MKCOL failed for $url (HTTP $code)" >&2; return 1 ;;
    esac
  }

  upload_file() {
    local local_file="$1"
    local remote_url="$2"
    if [[ ${DRY_RUN} -eq 1 ]]; then
      log "DRY RUN upload: ${local_file} -> ${remote_url}"
      return 0
    fi
    curl --fail --silent --show-error -u "${WEBDAV_USER}:${WEBDAV_PASS}" -T "${local_file}" "$remote_url" >/dev/null
  }

  # Upload with exponential backoff retry
  upload_file_with_retry() {
    local local_file="$1"
    local remote_url="$2"
    local filename
    filename=$(basename "$local_file")
    local attempt=0
    local delay

    while [[ $attempt -lt $UPLOAD_MAX_RETRIES ]]; do
      attempt=$((attempt + 1))
      if upload_file "$local_file" "$remote_url"; then
        [[ $attempt -gt 1 ]] && log "Upload succeeded on attempt $attempt: $filename"
        return 0
      fi

      if [[ $attempt -lt $UPLOAD_MAX_RETRIES ]]; then
        delay=$((UPLOAD_RETRY_DELAY_BASE ** attempt))
        log "WARN: Upload failed for $filename (attempt $attempt/$UPLOAD_MAX_RETRIES), retrying in ${delay}s..."
        sleep $delay
      fi
    done

    log "ERROR: Upload failed for $filename after $UPLOAD_MAX_RETRIES attempts"
    return 1
  }

  REMOTE_ROOT="${WEBDAV_URL%/}/openclaw-backup"
  REMOTE_RUN="${REMOTE_ROOT}/${TS}"

  FAILED_STAGE="creating remote directories"
  log "Ensuring remote directories exist"
  mkcol_if_needed "${REMOTE_ROOT}"
  mkcol_if_needed "${REMOTE_RUN}"

  FAILED_STAGE="uploading to WebDAV"
  log "Uploading backup files to WebDAV (max ${UPLOAD_MAX_RETRIES} retries)"
  upload_file_with_retry "${WORKSPACE_ARCHIVE}" "${REMOTE_RUN}/$(basename "${WORKSPACE_ARCHIVE}")"
  [[ -f "${EXTENSIONS_ARCHIVE}" ]] && upload_file_with_retry "${EXTENSIONS_ARCHIVE}" "${REMOTE_RUN}/$(basename "${EXTENSIONS_ARCHIVE}")"
  [[ -f "${CONFIG_COPY}" ]] && upload_file_with_retry "${CONFIG_COPY}" "${REMOTE_RUN}/$(basename "${CONFIG_COPY}")"
  [[ -f "${CONFIG_ENC}" ]] && upload_file_with_retry "${CONFIG_ENC}" "${REMOTE_RUN}/$(basename "${CONFIG_ENC}")"
  upload_file_with_retry "${RESTORE_NOTE}" "${REMOTE_RUN}/$(basename "${RESTORE_NOTE}")"
  upload_file_with_retry "${MANIFEST}" "${REMOTE_RUN}/$(basename "${MANIFEST}")"
  log "Upload finished successfully"
  FAILED_STAGE="applying remote retention"
  log "Applying remote retention: keep ${REMOTE_KEEP}"
  rotate_remote_backups "${REMOTE_ROOT}" "${REMOTE_KEEP}"
else
  log "Upload skipped (use --upload to enable)"
fi

write_success_summary
send_notify success
log "Done"
