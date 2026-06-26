#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

# OpenClaw Backup Diff Tool
# Compare current workspace vs backup

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -n "${OPENCLAW_WORKSPACE_DIR:-}" ]]; then
  WORKSPACE_DIR="${OPENCLAW_WORKSPACE_DIR}"
else
  WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
fi

HOME_DIR="${HOME}"
STATE_DIR="${HOME_DIR}/.openclaw"
BACKUP_ROOT="${WORKSPACE_DIR}/backups/openclaw"

BACKUP_DIR=""
FORMAT="summary"  # summary, full, json
SHOW_UNCHANGED=0
SHOW_TOKENS=1

log() { printf '[diff] %s\n' "$*"; }

usage() {
  cat <<EOF
Usage: $(basename "$0") --from <backup_dir> [OPTIONS]

Options:
  --from <dir>      Backup directory to compare against
  --format <type>   Output format: summary|full|json (default: summary)
  --show-unchanged  Include unchanged files in output
  --hide-tokens     Mask API tokens/keys in diff output
  --config-only     Only compare openclaw.json
  --skills-only     Only compare skills directory
  --memory-only     Only compare memory files
  -h, --help        Show this help

Examples:
  $(basename "$0") --from backups/openclaw/2026-04-02-030000
  $(basename "$0") --from backups/openclaw/2026-04-02-030000 --format=full
  $(basename "$0") --from backups/openclaw/2026-04-02-030000 --config-only
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)
      BACKUP_DIR="$2"
      shift 2
      ;;
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --show-unchanged)
      SHOW_UNCHANGED=1
      shift
      ;;
    --hide-tokens)
      SHOW_TOKENS=0
      shift
      ;;
    --config-only)
      FILTER="config"
      shift
      ;;
    --skills-only)
      FILTER="skills"
      shift
      ;;
    --memory-only)
      FILTER="memory"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${BACKUP_DIR}" ]]; then
  echo "Error: --from is required" >&2
  usage
  exit 1
fi

# Resolve backup dir
if [[ ! -d "${BACKUP_DIR}" ]]; then
  # Try relative to backup root
  if [[ -d "${BACKUP_ROOT}/${BACKUP_DIR}" ]]; then
    BACKUP_DIR="${BACKUP_ROOT}/${BACKUP_DIR}"
  else
    echo "Error: Backup directory not found: ${BACKUP_DIR}" >&2
    exit 1
  fi
fi

BACKUP_DIR="$(cd "${BACKUP_DIR}" && pwd)"
BACKUP_NAME=$(basename "${BACKUP_DIR}")

# Create temp directory for extraction
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "${TEMP_DIR}"' EXIT

# Extract backup for comparison
extract_backup() {
  log "Extracting backup for comparison..."
  
  if [[ -f "${BACKUP_DIR}/workspace.tar.gz" ]]; then
    tar -xzf "${BACKUP_DIR}/workspace.tar.gz" -C "${TEMP_DIR}"
  fi
  
  if [[ -f "${BACKUP_DIR}/extensions.tar.gz" ]]; then
    mkdir -p "${TEMP_DIR}/extensions"
    tar -xzf "${BACKUP_DIR}/extensions.tar.gz" -C "${TEMP_DIR}/extensions"
  fi
  
  if [[ -f "${BACKUP_DIR}/openclaw.json" ]]; then
    cp "${BACKUP_DIR}/openclaw.json" "${TEMP_DIR}/openclaw.json"
  elif [[ -f "${BACKUP_DIR}/openclaw.json.enc" ]]; then
    echo "[encrypted]" > "${TEMP_DIR}/openclaw.json"
  fi
}

# Compare file lists
compare_file_lists() {
  local src1="$1"
  local src2="$2"
  local label="$3"
  
  if [[ ! -d "${src1}" && ! -d "${src2}" ]]; then
    return 0
  fi
  
  echo ""
  echo "📁 ${label}:"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  # Find all files in both directories
  local files1 files2
  files1=$(find "${src1}" -type f 2>/dev/null | sed "s|${src1}/||" | sort || true)
  files2=$(find "${src2}" -type f 2>/dev/null | sed "s|${src2}/||" | sort || true)
  
  # Files only in backup (will be added)
  local added
  added=$(comm -23 <(echo "${files1}") <(echo "${files2}") 2>/dev/null || true)
  if [[ -n "${added}" ]]; then
    local count
    count=$(echo "${added}" | wc -l)
    echo "📥 Will add: ${count} file(s)"
    if [[ "${FORMAT}" == "full" ]]; then
      echo "${added}" | head -20 | sed 's/^/   + /'
      [[ ${count} -gt 20 ]] && echo "   ... and $((count - 20)) more"
    fi
  fi
  
  # Files only in current (will be removed)
  local removed
  removed=$(comm -13 <(echo "${files1}") <(echo "${files2}") 2>/dev/null || true)
  if [[ -n "${removed}" ]]; then
    local count
    count=$(echo "${removed}" | wc -l)
    echo "📤 Will remove: ${count} file(s)"
    if [[ "${FORMAT}" == "full" ]]; then
      echo "${removed}" | head -20 | sed 's/^/   - /'
      [[ ${count} -gt 20 ]] && echo "   ... and $((count - 20)) more"
    fi
  fi
  
  # Files in both (check for modifications)
  local common
  common=$(comm -12 <(echo "${files1}") <(echo "${files2}") 2>/dev/null || true)
  if [[ -n "${common}" ]]; then
    local modified=0
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        if ! diff -q "${src1}/${file}" "${src2}/${file}" >/dev/null 2>&1; then
          ((modified++)) || true
          if [[ "${FORMAT}" == "full" && ${modified} -le 20 ]]; then
            echo "   ~ ${file}"
          fi
        fi
      fi
    done <<< "${common}"
    
    if [[ ${modified} -gt 0 ]]; then
      echo "📝 Will modify: ${modified} file(s)"
      [[ "${FORMAT}" == "full" && ${modified} -gt 20 ]] && echo "   ... and $((modified - 20)) more"
    fi
    
    local unchanged
    unchanged=$(echo "${common}" | wc -l)
    unchanged=$((unchanged - modified))
    if [[ ${unchanged} -gt 0 && ${SHOW_UNCHANGED} -eq 1 ]]; then
      echo "✓ Unchanged: ${unchanged} file(s)"
    fi
  fi
}

# Compare JSON config with token masking
compare_config() {
  local backup_config="${BACKUP_DIR}/openclaw.json"
  local current_config="${STATE_DIR}/openclaw.json"
  
  echo ""
  echo "⚙️  Config (openclaw.json):"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  if [[ ! -f "${backup_config}" && ! -f "${BACKUP_DIR}/openclaw.json.enc" ]]; then
    echo "⚠️  No config in backup"
    return 0
  fi
  
  if [[ ! -f "${current_config}" ]]; then
    echo "⚠️  No current config found"
    return 0
  fi
  
  if [[ -f "${BACKUP_DIR}/openclaw.json.enc" ]]; then
    echo "🔒 Config is encrypted in backup"
    echo "   Use --decrypt-config during restore to compare contents"
    return 0
  fi
  
  # Generate diff with optional token masking
  local diff_output
  diff_output=$(diff -u "${backup_config}" "${current_config}" 2>/dev/null || true)
  
  if [[ -z "${diff_output}" ]]; then
    echo "✓ Config is identical"
    return 0
  fi
  
  # Mask sensitive tokens if requested
  if [[ ${SHOW_TOKENS} -eq 0 ]]; then
    diff_output=$(echo "${diff_output}" | sed -E 's/(["'\''']?(api[_-]?key|token|secret|password|pass)["'\''']?[[:space:]]*[:=][[:space:]]*)["'\''']?[^"'\''"[:space:]]{8,}["'\''']?/\1"***"/gi')
  fi
  
  echo "📝 Config differences found:"
  
  if [[ "${FORMAT}" == "full" ]]; then
    if [[ ${SHOW_TOKENS} -eq 1 ]]; then
      # Mask sensitive values
      echo "${diff_output}" | grep -E "^[\+\-]" | head -50 | \
        sed -E 's/("token"|"api_key"|"password"|"secret"): "[^"]+"/\1: "***MASKED***"/g' | \
        sed 's/^+/\x1b[32m+\x1b[0m/' | \
        sed 's/^-/\x1b[31m-\x1b[0m/'
    else
      echo "${diff_output}" | grep -E "^[\+\-]" | head -50
    fi
    
    local lines
    lines=$(echo "${diff_output}" | grep -E "^[\+\-]" | wc -l)
    [[ ${lines} -gt 50 ]] && echo "... and $((lines - 50)) more lines"
  else
    # Summary mode - show key changes
    local added removed
    added=$(echo "${diff_output}" | grep -c "^+" 2>/dev/null || echo "0")
    removed=$(echo "${diff_output}" | grep -c "^-" 2>/dev/null || echo "0")
    echo "   Lines added: ${added}"
    echo "   Lines removed: ${removed}"
    
    # Show specific key changes
    local key_changes
    key_changes=$(echo "${diff_output}" | grep -E "^[\+\-].*:" | sed 's/^[+-]//' | cut -d: -f1 | sort -u | head -10)
    if [[ -n "${key_changes}" ]]; then
      echo "   Changed keys:"
      echo "${key_changes}" | sed 's/^/      - /'
    fi
  fi
}

# Generate summary
show_summary() {
  echo ""
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║           📊 Restore Preview Summary                     ║"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo ""
  echo "Backup: ${BACKUP_NAME}"
  echo "Date: $(date -d "$(echo ${BACKUP_NAME} | sed 's/-/ /3' | sed 's/-/:/g')" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo ${BACKUP_NAME})"
  echo ""
  
  # Count files in backup
  local ws_count=0 ext_count=0
  if [[ -f "${BACKUP_DIR}/workspace.tar.gz" ]]; then
    ws_count=$(tar -tzf "${BACKUP_DIR}/workspace.tar.gz" 2>/dev/null | wc -l)
  fi
  if [[ -f "${BACKUP_DIR}/extensions.tar.gz" ]]; then
    ext_count=$(tar -tzf "${BACKUP_DIR}/extensions.tar.gz" 2>/dev/null | wc -l)
  fi
  
  echo "Backup contains:"
  echo "  - ${ws_count} workspace files"
  echo "  - ${ext_count} extension files"
  [[ -f "${BACKUP_DIR}/openclaw.json" || -f "${BACKUP_DIR}/openclaw.json.enc" ]] && echo "  - 1 config file"
  echo ""
  
  echo "⚠️  Important Notes:"
  echo "  • This preview shows what WILL change during restore"
  echo "  • Current files will be overwritten"
  echo "  • Consider using --backup-current before restore"
  echo ""
  echo "To restore, run:"
  echo "  openclaw-restore.sh --from ${BACKUP_NAME}"
}

# Main
echo ""
echo "🔍 OpenClaw Backup Diff"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Comparing:"
echo "  Backup:  ${BACKUP_DIR}"
echo "  Current: ${WORKSPACE_DIR}"
echo ""

extract_backup

# Apply filters
if [[ -z "${FILTER:-}" ]]; then
  compare_file_lists "${TEMP_DIR}" "${WORKSPACE_DIR}" "Workspace Files"
  
  if [[ -d "${TEMP_DIR}/extensions" ]]; then
    compare_file_lists "${TEMP_DIR}/extensions" "${EXTENSIONS_DIR:-${STATE_DIR}/extensions}" "Extensions"
  fi
  
  compare_config
elif [[ "${FILTER}" == "config" ]]; then
  compare_config
elif [[ "${FILTER}" == "skills" ]]; then
  compare_file_lists "${TEMP_DIR}/skills" "${WORKSPACE_DIR}/skills" "Skills"
elif [[ "${FILTER}" == "memory" ]]; then
  compare_file_lists "${TEMP_DIR}/memory" "${WORKSPACE_DIR}/memory" "Memory"
fi

show_summary
