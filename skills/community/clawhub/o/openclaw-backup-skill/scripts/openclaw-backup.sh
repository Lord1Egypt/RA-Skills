#!/usr/bin/env bash
set -euo pipefail

umask 077

# Create new files and directories as private by default.

SCRIPT_VERSION="0.2.2"

log() {
  printf '[openclaw-backup] %s\n' "$*" >&2
}

fail() {
  printf '[openclaw-backup] ERROR: %s\n' "$*" >&2
  exit 1
}

# This script relies on Bash 4+ features such as associative arrays.
if (( BASH_VERSINFO[0] < 4 )); then
fail "This script requires Bash 4+"
fi

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

require_runtime_commands() {
  require_cmd openclaw
  require_cmd date
  require_cmd mktemp
  require_cmd python3
  require_cmd sort
  require_cmd tar
  require_cmd tee
  require_cmd uname
  require_cmd basename
  require_cmd dirname
  require_cmd cp
  require_cmd mkdir
  require_cmd mv
  require_cmd rm
}

expand_path() {
  case "$1" in
    "~")
      printf '%s\n' "$HOME"
      ;;
    "~/"*)
      printf '%s\n' "$HOME/${1#\~/}"
      ;;
    *)
      printf '%s\n' "$1"
      ;;
  esac
}

# CLI mode flags and retention options are collected first, then validated.
MODE_AUTO=0
MODE_BACKUP=0
MODE_PRUNE=0
MODE_MANUAL=0

MODE=""

KEEP_DAYS=""
KEEP_WEEKS=""
KEEP_HOURS=""

DRY_RUN=0

OUTPUT_DIR=""

STATE_DIR=""

OUTPUT_DIR_WAS_EXPLICIT=0

declare -a POSITIONAL_ARGS=()

declare -a TMP_PATHS=()

LOG_TEE_ENABLED=0

LAST_CREATED_ARCHIVE_PATH=""

REGULAR_ARCHIVE_PREFIX="openclaw-light-backup-"

MANUAL_ARCHIVE_PREFIX="openclaw-light-manual-backup-"

REGULAR_ARCHIVE_GLOB="openclaw-light-backup-*.tar.gz"

# Help text for the operational CLI.
usage() {
  cat <<EOF
OpenClaw backup script v$SCRIPT_VERSION

Usage:
  ${0##*/} (--auto | --backup | --prune | --manual) [options] [OUTPUT_DIR]

Description:
  Create or prune OpenClaw backup archives.

Modes (exactly one is required):
  --auto       Create a regular backup and then prune regular backups.
  --backup     Create only a regular backup.
  --prune      Prune only regular backups.
  --manual     Create a manual backup that is excluded from normal pruning.

Retention options:
  --keep-days N    Keep the latest regular backup for each of the last N UTC days.
  --keep-weeks M   Keep the latest regular backup for each of the last M UTC ISO weeks.
  --keep-hours H   Keep all regular backups from the last H hours (UTC rolling window).
  --dry-run        Allowed only with --prune. Show the prune plan without deleting files.

Arguments:
  OUTPUT_DIR       Optional existing directory where archives and matching .log
                   files will be written/read. If omitted, the default backup
                   directory is used as ../backups/openclaw relative to the
                   resolved OpenClaw state directory.

Examples:
  ${0##*/} --backup
  ${0##*/} --manual
  ${0##*/} --prune --dry-run --keep-days 7 --keep-weeks 4
  ${0##*/} --auto --keep-days 7 --keep-weeks 4
  ${0##*/} --auto --keep-hours 24 --keep-days 7 --keep-weeks 4
  ${0##*/} --auto --keep-days 7 /path/to/backups

Notes:
  - Regular archives use the name pattern:
      openclaw-light-backup-YYYY-MM-DDTHH-MM-SSZ.tar.gz
  - Manual archives use the name pattern:
      openclaw-light-manual-backup-YYYY-MM-DDTHH-MM-SSZ.tar.gz
  - Prune touches only regular archives and their matching .log files.
EOF
}

# Parse raw CLI input without applying business rules yet.
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --auto)
        MODE_AUTO=1
        shift
        ;;
      --backup)
        MODE_BACKUP=1
        shift
        ;;
      --prune)
        MODE_PRUNE=1
        shift
        ;;
      --manual)
        MODE_MANUAL=1
        shift
        ;;
      --keep-days)
        [[ $# -ge 2 ]] || fail "Option --keep-days requires a value"
        KEEP_DAYS="$2"
        shift 2
        ;;
      --keep-weeks)
        [[ $# -ge 2 ]] || fail "Option --keep-weeks requires a value"
        KEEP_WEEKS="$2"
        shift 2
        ;;
      --keep-hours)
        [[ $# -ge 2 ]] || fail "Option --keep-hours requires a value"
        KEEP_HOURS="$2"
        shift 2
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      --)
        shift
        while [[ $# -gt 0 ]]; do
          POSITIONAL_ARGS+=("$1")
          shift
        done
        ;;
      -*)
        fail "Unknown option: $1"
        ;;
      *)
        POSITIONAL_ARGS+=("$1")
        shift
        ;;
    esac
  done
}

is_nonnegative_integer() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

# Validate argument combinations after parsing.
validate_args() {

  local mode_count=$((MODE_AUTO + MODE_BACKUP + MODE_PRUNE + MODE_MANUAL))

  if [[ $mode_count -ne 1 ]]; then
    fail "Exactly one mode is required: --auto, --backup, --prune, or --manual"
  fi

  if [[ -n "$KEEP_DAYS" ]] && ! is_nonnegative_integer "$KEEP_DAYS"; then
    fail "--keep-days must be a non-negative integer"
  fi

  if [[ -n "$KEEP_WEEKS" ]] && ! is_nonnegative_integer "$KEEP_WEEKS"; then
    fail "--keep-weeks must be a non-negative integer"
  fi

  if [[ -n "$KEEP_HOURS" ]] && ! is_nonnegative_integer "$KEEP_HOURS"; then
    fail "--keep-hours must be a non-negative integer"
  fi

  if [[ ${#POSITIONAL_ARGS[@]} -gt 1 ]]; then
    fail "Too many positional arguments. Only OUTPUT_DIR is allowed."
  fi

  if [[ ${#POSITIONAL_ARGS[@]} -eq 1 ]]; then
    OUTPUT_DIR="${POSITIONAL_ARGS[0]}"
    OUTPUT_DIR_WAS_EXPLICIT=1
  fi

  if (( MODE_AUTO )); then
    MODE="auto"
  elif (( MODE_BACKUP )); then
    MODE="backup"
  elif (( MODE_PRUNE )); then
    MODE="prune"
  else
    MODE="manual"
  fi

  if (( DRY_RUN )) && [[ "$MODE" != "prune" ]]; then
    fail "--dry-run is allowed only together with --prune"
  fi

  case "$MODE" in
    auto|prune)
      local days="${KEEP_DAYS:-0}"
      local weeks="${KEEP_WEEKS:-0}"
      local hours="${KEEP_HOURS:-0}"

      if [[ -z "$KEEP_HOURS" && -z "$KEEP_DAYS" && -z "$KEEP_WEEKS" ]]; then
        fail "${MODE^} mode requires at least one retention option: --keep-hours, --keep-days and/or --keep-weeks"
      fi
  
      if (( hours == 0 && days == 0 && weeks == 0 )); then
        fail "At least one of --keep-hours, --keep-days or --keep-weeks must be greater than 0 for --$MODE"
      fi
      ;;
    backup|manual)
      if [[ -n "$KEEP_HOURS" || -n "$KEEP_DAYS" || -n "$KEEP_WEEKS" ]]; then
        fail "Retention options are not allowed with --$MODE"
      fi
      ;;
  esac
}

register_temp_path() {
  TMP_PATHS+=("$1")
}

cleanup() {
  local path
  for path in "${TMP_PATHS[@]}"; do
    if [[ -e "$path" ]]; then
      rm -rf "$path"
    fi
  done
  return 0
}

trap cleanup EXIT

# Mirror stdout/stderr into a backup-specific log file when backup modes run.

enable_log_tee() {
  local target_log_path="$1"

  if (( LOG_TEE_ENABLED )); then
    return 0
  fi

  exec > >(tee -a "$target_log_path") 2>&1

  LOG_TEE_ENABLED=1

  log "Log file: $target_log_path"
 }

# Build the matching .log path for a given archive path.
archive_log_path_from_archive() {
  local archive_path="$1"
  local archive_basename

  archive_basename="$(basename -- "$archive_path")"

  printf '%s/%s.log\n' "$(dirname -- "$archive_path")" "${archive_basename%.tar.gz}"
}

# Extract and validate the UTC timestamp encoded in a regular archive name.
extract_regular_archive_timestamp() {
  local archive_path="$1"
  local archive_basename
  local timestamp

  archive_basename="$(basename -- "$archive_path")"

  case "$archive_basename" in
    ${REGULAR_ARCHIVE_PREFIX}*.tar.gz)
      timestamp="${archive_basename#${REGULAR_ARCHIVE_PREFIX}}"

      timestamp="${timestamp%.tar.gz}"
      ;;
    *)
      return 1
      ;;
  esac

  python3 - "$timestamp" <<'PY'
import sys
from datetime import datetime

value = sys.argv[1]

datetime.strptime(value, '%Y-%m-%dT%H-%M-%SZ')

print(value)
PY
}

# Convert a validated archive timestamp into a UTC day key (YYYY-MM-DD).

timestamp_day_key() {
  python3 - "$1" <<'PY'
import sys
from datetime import datetime

value = sys.argv[1]
dt = datetime.strptime(value, '%Y-%m-%dT%H-%M-%SZ')
print(dt.strftime('%Y-%m-%d'))
PY
}

# Convert a validated archive timestamp into a UTC ISO week key (YYYY-Www).

timestamp_week_key() {
  python3 - "$1" <<'PY'
import sys
from datetime import datetime

value = sys.argv[1]
dt = datetime.strptime(value, '%Y-%m-%dT%H-%M-%SZ')
iso = dt.isocalendar()
print(f'{iso.year}-W{iso.week:02d}')
PY
}

# Convert a validated archive timestamp into Unix epoch seconds for comparison.

timestamp_epoch() {
  python3 - "$1" <<'PY'
import sys
from datetime import datetime, timezone

value = sys.argv[1]
dt = datetime.strptime(value, '%Y-%m-%dT%H-%M-%SZ').replace(tzinfo=timezone.utc)
print(int(dt.timestamp()))
PY
}

# Resolve workspace, state dir, config file, and default output directory.
resolve_workspace_and_config() {

  SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
  CONFIGURED_WORKSPACE="$(openclaw config get agents.defaults.workspace 2>/dev/null || true)"

  if [[ -n "$CONFIGURED_WORKSPACE" ]]; then
    WORKSPACE="$(expand_path "$CONFIGURED_WORKSPACE")"
  else
    WORKSPACE="$(cd -- "$SCRIPT_DIR/.." && pwd)"
  fi

  STATE_DIR="$(expand_path "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}")"
  CONFIGURED_CONFIG_FILE="$(openclaw config file 2>/dev/null || true)"

  if [[ -n "$CONFIGURED_CONFIG_FILE" ]]; then
    CONFIG_FILE="$(expand_path "$CONFIGURED_CONFIG_FILE")"
  else
    CONFIG_FILE="$(expand_path "${OPENCLAW_CONFIG_PATH:-$STATE_DIR/openclaw.json}")"
  fi

  # Default backup directory lives next to the resolved OpenClaw state dir.
  if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="$(dirname -- "$STATE_DIR")/backups/openclaw"
  fi
}

# Validate filesystem prerequisites before doing any real work.
validate_environment() {

  [[ -d "$WORKSPACE" ]] || fail "Workspace directory not found: $WORKSPACE"
  [[ -f "$WORKSPACE/AGENTS.md" ]] || fail "Workspace validation failed: AGENTS.md not found in $WORKSPACE"
  [[ -f "$WORKSPACE/SOUL.md" ]] || fail "Workspace validation failed: SOUL.md not found in $WORKSPACE"
  [[ -f "$WORKSPACE/USER.md" ]] || fail "Workspace validation failed: USER.md not found in $WORKSPACE"
  [[ -d "$STATE_DIR" ]] || fail "OpenClaw state directory not found: $STATE_DIR"
  [[ -f "$CONFIG_FILE" ]] || fail "OpenClaw config file not found: $CONFIG_FILE"

  if (( OUTPUT_DIR_WAS_EXPLICIT )); then
    [[ -d "$OUTPUT_DIR" ]] || fail "Output directory does not exist or is not a directory: $OUTPUT_DIR"
  else
    mkdir -p "$OUTPUT_DIR" || fail "Failed to create output directory: $OUTPUT_DIR"
  fi
}

# Create either a regular or manual backup archive.
create_backup() {
  local backup_kind="$1"

  local backup_mode_label
  local archive_name_prefix
  local timestamp
  local archive_name
  local archive_basename
  local staging_dir
  local archive_dir
  local final_archive_path
  local temp_archive_path
  local log_path
  case "$backup_kind" in
    regular)
      backup_mode_label="regular"
      archive_name_prefix="$REGULAR_ARCHIVE_PREFIX"
      ;;
    manual)
      backup_mode_label="manual"
      archive_name_prefix="$MANUAL_ARCHIVE_PREFIX"
      ;;
    *)
      fail "Unsupported backup kind: $backup_kind"
      ;;
  esac

  timestamp="$(date -u +%Y-%m-%dT%H-%M-%SZ)"

  archive_name="${archive_name_prefix}${timestamp}.tar.gz"

  archive_basename="${archive_name%.tar.gz}"

  final_archive_path="$OUTPUT_DIR/$archive_name"

  temp_archive_path="${final_archive_path}.part"

  log_path="$OUTPUT_DIR/${archive_basename}.log"

  # Write key metadata to the archive log before tee takes over process output.
  
  printf '[openclaw-backup] Script version: %s\n' "$SCRIPT_VERSION" >> "$log_path"
  printf '[openclaw-backup] Resolved workspace: %s\n' "$WORKSPACE" >> "$log_path"
  
  enable_log_tee "$log_path"

  log "Backup mode: $backup_mode_label"

  # Stage backup contents in a temporary directory before packing the archive.
  staging_dir="$(mktemp -d "${TMPDIR:-/tmp}/openclaw-backup.XXXXXXXX")"

  register_temp_path "$staging_dir"

  register_temp_path "$temp_archive_path"

  archive_dir="$staging_dir/$archive_basename"

  mkdir -p "$archive_dir/workspace"

  log "Staging workspace copy"

  tar \
    -C "$WORKSPACE" \
    --exclude='./backups' \
    --exclude='./temp' \
    -cf - . | tar -C "$archive_dir/workspace" -xf -

  log "Copying OpenClaw config"
  cp -p "$CONFIG_FILE" "$archive_dir/openclaw.json"

  log "Exporting cron jobs (machine-readable)"
  openclaw cron list --all --json > "$archive_dir/cron-export.json"

  [[ -s "$archive_dir/cron-export.json" ]] || fail "Cron export is empty"

  log "Generating cron summary"
  # Keep a human-readable cron export alongside the raw JSON export.
  python3 - "$archive_dir/cron-export.json" "$archive_dir/cron-summary.txt" <<'PY'
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])

data = json.loads(src.read_text(encoding='utf-8'))
jobs = data.get('jobs') or []
lines = []
lines.append(f"Total jobs: {len(jobs)}")
lines.append("")

for idx, job in enumerate(jobs, start=1):
    schedule = job.get('schedule') or {}
    delivery = job.get('delivery') or {}
    state = job.get('state') or {}
    payload = job.get('payload') or {}
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
    payload_json_indented = "\n".join(f"     {line}" for line in payload_json.splitlines())

    lines.extend([
        f"{idx}. {job.get('name') or '(unnamed)'}",
        f"   id: {job.get('id', '-')}",
        f"   enabled: {job.get('enabled')}",
        f"   schedule: kind={schedule.get('kind', '-')}; expr={schedule.get('expr', '-')}; tz={schedule.get('tz', '-')}",
        f"   sessionTarget: {job.get('sessionTarget', '-')}",
        f"   delivery: mode={delivery.get('mode', '-')}; channel={delivery.get('channel', '-')}; to={delivery.get('to', '-')}",
        "   payloadJson:",
        payload_json_indented,
        f"   nextRunAtMs: {state.get('nextRunAtMs', '-')}",
        "",
    ])

out.write_text("\n".join(lines).rstrip() + "\n", encoding='utf-8')
PY

  log "Collecting software versions"
  {

    printf 'Generated at (UTC): %s\n' "$timestamp"

    printf 'OpenClaw: %s\n' "$(openclaw --version 2>/dev/null || echo 'unknown')"

    printf 'Node.js: %s\n' "$(node -v 2>/dev/null || echo 'not-found')"

    if command -v npm >/dev/null 2>&1; then
      printf 'npm: %s\n' "$(npm -v 2>/dev/null || echo 'unknown')"
    fi

    OS_PRETTY_NAME="unknown"

    if [[ -r /etc/os-release ]]; then
      while IFS='=' read -r key value; do
        if [[ "$key" == "PRETTY_NAME" ]]; then
          OS_PRETTY_NAME="${value%\"}"

          OS_PRETTY_NAME="${OS_PRETTY_NAME#\"}"

          break
        fi
      done < /etc/os-release
    fi

    printf 'OS: %s\n' "$OS_PRETTY_NAME"
    printf 'Kernel: %s\n' "$(uname -sr 2>/dev/null || echo 'unknown')"
    printf 'OpenClaw Backup Script: %s\n' "$SCRIPT_VERSION"
  } > "$archive_dir/software_versions.txt"

  log "Writing restore instructions"

  cat > "$archive_dir/RESTORE.md" <<EOF
# RESTORE.md

This is a Light backup for OpenClaw. It is designed for quick operational recovery and intentionally does not include environment variables, system env, or system override files.

## Included
- workspace/ (full workspace copy excluding workspace/backups/ and workspace/temp/)
- openclaw.json
- cron-export.json
- cron-summary.txt
- software_versions.txt
- manifest.json

## Restore steps
1. Restore the contents of workspace/ into: $WORKSPACE
2. Restore openclaw.json into: $CONFIG_FILE
3. Recreate cron jobs from cron-export.json using your chosen restore procedure.
4. Restore required env variables, system env, and system override manually if necessary (they are not part of this Light backup).
5. Run verification commands after restore:
   - openclaw status
   - openclaw memory status --deep
   - openclaw models status
   - openclaw cron list --all --json
EOF

  log "Writing manifest"
  python3 - "$archive_dir/manifest.json" "$timestamp" "$WORKSPACE" "$CONFIG_FILE" "$archive_name" "$backup_mode_label" "$SCRIPT_VERSION" <<'PY'
import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])

timestamp = sys.argv[2]

workspace = sys.argv[3]

config_file = sys.argv[4]

archive_name = sys.argv[5]

backup_mode = sys.argv[6]

script_version = sys.argv[7]

manifest = {
    'backupType': 'light',
    'backupMode': backup_mode,
    'scriptVersion': script_version,
    'generatedAtUtc': timestamp,
    'archiveName': archive_name,
    'workspaceSource': workspace,
    'configSource': config_file,

    'included': [
        'workspace/ (excluding workspace/backups/ and workspace/temp/)',
        'openclaw.json',
        'cron-export.json',
        'cron-summary.txt',
        'software_versions.txt',
        'RESTORE.md',
        'manifest.json',
    ],

    'excluded': [
        'workspace/backups/',
        'workspace/temp/',
        'environment variables',
        'system env',
        'system override',
    ],

    'notes': [
        'Archive verification is performed by the script after archive creation.',
        'This manifest describes the intended contents and exclusions of the backup.',
    ],
}

manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY

  [[ -s "$archive_dir/openclaw.json" ]] || fail "Copied config file is empty"
  [[ -s "$archive_dir/manifest.json" ]] || fail "Manifest is empty"
  [[ -s "$archive_dir/cron-export.json" ]] || fail "Cron export is empty"
  [[ -f "$archive_dir/workspace/AGENTS.md" ]] || fail "Workspace copy is missing AGENTS.md"
  [[ -f "$archive_dir/workspace/SOUL.md" ]] || fail "Workspace copy is missing SOUL.md"
  [[ -f "$archive_dir/workspace/USER.md" ]] || fail "Workspace copy is missing USER.md"

  python3 -c 'import json, sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$archive_dir/manifest.json" \
    || fail "Manifest JSON is invalid"

  python3 -c 'import json, sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$archive_dir/cron-export.json" \
    || fail "Cron export JSON is invalid"

  log "Creating temporary archive: $temp_archive_path"
  tar -C "$staging_dir" -czf "$temp_archive_path" "$archive_basename"

  [[ -s "$temp_archive_path" ]] || fail "Temporary archive was created but is empty: $temp_archive_path"

  log "Verifying temporary archive readability"
  tar -tzf "$temp_archive_path" >/dev/null

  log "Finalizing archive: $final_archive_path"
  mv -- "$temp_archive_path" "$final_archive_path"

  [[ -s "$final_archive_path" ]] || fail "Final archive is empty after move: $final_archive_path"

  LAST_CREATED_ARCHIVE_PATH="$final_archive_path"

  log "Backup created successfully"
  log "Archive path:"
  printf '%s\n' "$final_archive_path"
}

# Prune regular archives according to recent/hourly, daily, and weekly retention rules.
prune_regular_archives() {
  local forced_keep_archive_path="${1:-}"

  local keep_days="${KEEP_DAYS:-0}"
  local keep_weeks="${KEEP_WEEKS:-0}"
  local keep_hours="${KEEP_HOURS:-0}"

  local archive_path
  local timestamp
  local epoch
  local now_epoch
  local now_human
  local recent_cutoff_epoch
  local recent_cutoff_human
  local day_key
  local week_key
  local paired_log_path

  local -a archives=()
  local -a valid_archives=()
  local -a ignored_archives=()
  local -a sorted_day_keys=()
  local -a sorted_week_keys=()
  local -a sorted_keep_list=()
  local -a sorted_delete_list=()
  local -a delete_list=()

  local key
  local start_index
  local i

  declare -A day_winner_path=()
  declare -A day_winner_epoch=()
  declare -A week_winner_path=()
  declare -A week_winner_epoch=()
  declare -A keep_set=()

  log "Prune mode: dry-run=${DRY_RUN}, keep-hours=${KEEP_HOURS:-0}, keep-days=${KEEP_DAYS:-0}, keep-weeks=${KEEP_WEEKS:-0}"

  shopt -s nullglob
  archives=("$OUTPUT_DIR"/$REGULAR_ARCHIVE_GLOB)
  shopt -u nullglob

  if [[ ${#archives[@]} -eq 0 ]]; then
    log "No regular backup archives found for prune in: $OUTPUT_DIR"
    return 0
  fi

  # Build the recent-retention rolling window in UTC.
  now_epoch="$(date -u +%s)"
  recent_cutoff_epoch=$(( now_epoch - keep_hours * 3600 ))

  if (( keep_hours > 0 )); then
    log "Recent retention mode enabled: keeping all regular backups from the last ${keep_hours} hours"

    if recent_cutoff_human="$(date -u -d "@$recent_cutoff_epoch" '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null)" \
      && now_human="$(date -u -d "@$now_epoch" '+%Y-%m-%d %H:%M:%S UTC' 2>/dev/null)"; then
      log "Recent retention window: ${recent_cutoff_human} (${recent_cutoff_epoch}) -> ${now_human} (${now_epoch})"
      else
      log "Recent retention window: ${recent_cutoff_epoch} -> ${now_epoch}"
    fi
  fi

  # Scan every regular archive candidate once and feed all retention buckets.
  for archive_path in "${archives[@]}"; do
    if ! timestamp="$(extract_regular_archive_timestamp "$archive_path" 2>/dev/null)"; then
      ignored_archives+=("$archive_path")
      continue
    fi

    epoch="$(timestamp_epoch "$timestamp")"
    valid_archives+=("$archive_path")

    if (( keep_hours > 0 )) && (( epoch >= recent_cutoff_epoch )); then
      keep_set["$archive_path"]=1
    fi

    if (( keep_days > 0 )); then
      day_key="$(timestamp_day_key "$timestamp")"

      if [[ -z "${day_winner_epoch[$day_key]:-}" || "$epoch" -gt "${day_winner_epoch[$day_key]}" ]]; then
        day_winner_epoch[$day_key]="$epoch"
        day_winner_path[$day_key]="$archive_path"
      fi
    fi

    if (( keep_weeks > 0 )); then
      week_key="$(timestamp_week_key "$timestamp")"

      if [[ -z "${week_winner_epoch[$week_key]:-}" || "$epoch" -gt "${week_winner_epoch[$week_key]}" ]]; then
        week_winner_epoch[$week_key]="$epoch"
        week_winner_path[$week_key]="$archive_path"
      fi
    fi
  done

  if [[ ${#ignored_archives[@]} -gt 0 ]]; then
    log "Ignoring archives with unparseable regular-backup names: ${#ignored_archives[@]}"
    for archive_path in "${ignored_archives[@]}"; do
      log "Ignored: $archive_path"
    done
  fi

  if [[ ${#valid_archives[@]} -eq 0 ]]; then
    log "No valid regular backup archives remain after filename validation"
    return 0
  fi

  if (( keep_days > 0 )) && [[ ${#day_winner_path[@]} -gt 0 ]]; then
    readarray -t sorted_day_keys < <(printf '%s\n' "${!day_winner_path[@]}" | sort)

    start_index=0
    if (( ${#sorted_day_keys[@]} > keep_days )); then
      start_index=$(( ${#sorted_day_keys[@]} - keep_days ))
    fi

    for (( i = start_index; i < ${#sorted_day_keys[@]}; i++ )); do
      key="${sorted_day_keys[$i]}"
      keep_set["${day_winner_path[$key]}"]=1
    done
  fi

  if (( keep_weeks > 0 )) && [[ ${#week_winner_path[@]} -gt 0 ]]; then
    readarray -t sorted_week_keys < <(printf '%s\n' "${!week_winner_path[@]}" | sort)

    start_index=0
    if (( ${#sorted_week_keys[@]} > keep_weeks )); then
      start_index=$(( ${#sorted_week_keys[@]} - keep_weeks ))
    fi

    for (( i = start_index; i < ${#sorted_week_keys[@]}; i++ )); do
      key="${sorted_week_keys[$i]}"
      keep_set["${week_winner_path[$key]}"]=1
    done
  fi

  if [[ -n "$forced_keep_archive_path" ]]; then
    keep_set["$forced_keep_archive_path"]=1
  fi

  for archive_path in "${valid_archives[@]}"; do
    if [[ -z "${keep_set[$archive_path]:-}" ]]; then
      delete_list+=("$archive_path")
    fi
  done

  readarray -t sorted_keep_list < <(printf '%s\n' "${!keep_set[@]}" | sort)

  if [[ ${#delete_list[@]} -gt 0 ]]; then
    readarray -t sorted_delete_list < <(printf '%s\n' "${delete_list[@]}" | sort)
  fi

  log "Prune summary: total valid regular archives=${#valid_archives[@]}, keep=${#sorted_keep_list[@]}, delete=${#delete_list[@]}"

  if [[ ${#sorted_keep_list[@]} -gt 0 ]]; then
    log "Keep set:"
    for archive_path in "${sorted_keep_list[@]}"; do
      log "KEEP  $archive_path"
    done
  fi

  if [[ ${#sorted_delete_list[@]} -eq 0 ]]; then
    log "Nothing to delete"
    return 0
  fi

  if (( DRY_RUN )); then
    log "Dry-run mode enabled; planned deletions:"
    for archive_path in "${sorted_delete_list[@]}"; do
      paired_log_path="$(archive_log_path_from_archive "$archive_path")"
      log "DELETE $archive_path"
      if [[ -e "$paired_log_path" ]]; then
        log "DELETE $paired_log_path"
      fi
    done
    return 0
  fi

  log "Deleting archives outside keep set"
  for archive_path in "${sorted_delete_list[@]}"; do
    rm -f -- "$archive_path"
    log "Deleted archive: $archive_path"
    paired_log_path="$(archive_log_path_from_archive "$archive_path")"
    if [[ -e "$paired_log_path" ]]; then
      rm -f -- "$paired_log_path"
      log "Deleted log: $paired_log_path"
    fi
  done
}

# Main entry point: parse, validate, resolve, then dispatch by mode.
main() {
  parse_args "$@"
  validate_args
  require_runtime_commands
  resolve_workspace_and_config
  validate_environment
  
  log "OpenClaw Backup Script version: $SCRIPT_VERSION"
  log "Resolved workspace: $WORKSPACE"
  
  case "$MODE" in
    backup)
      create_backup regular
      ;;
    manual)
      create_backup manual
      ;;
    prune)
      prune_regular_archives
      ;;
    auto)
      create_backup regular

      prune_regular_archives "$LAST_CREATED_ARCHIVE_PATH"
      ;;
    *)
      fail "Unsupported mode dispatch: $MODE"
      ;;
  esac
}

main "$@"
