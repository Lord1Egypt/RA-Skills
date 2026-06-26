#!/bin/bash
# Local File Manager - Entry point

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${CWD:-.}"  # Use CWD env if set, else current

usage() {
  cat <<EOF
Usage: file-manager --action <read|write|append|list|mkdir|delete> [options]

Options:
  --action <action>     Required: read, write, append, list, mkdir, delete
  --path <filepath>     Target file path (relative to cwd)
  --dir <directory>     Target directory (for list/mkdir)
  --content <string>    Content to write/append (use - for stdin)
  --pattern <glob>      File pattern for list (e.g., "*.md")
  --dry-run             Show what would be done without doing it
  -h, --help            Show this help

Examples:
  file-manager --action read --path config.yaml
  file-manager --action write --path output.json --content '{"result":"ok"}'
  file-manager --action append --path log.txt --content "New entry"
  file-manager --action list --dir . --pattern "*.py"
  file-manager --action mkdir --dir reports
EOF
  exit 1
}

# Parse args
ACTION=""
PATH=""
DIR=""
CONTENT=""
PATTERN=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --action)
      ACTION="$2"; shift 2 ;;
    --path)
      PATH="$2"; shift 2 ;;
    --dir)
      DIR="$2"; shift 2 ;;
    --content)
      CONTENT="$2"; shift 2 ;;
    --pattern)
      PATTERN="$2"; shift 2 ;;
    --dry-run)
      DRY_RUN=1; shift ;;
    -h|--help)
      usage ;;
    *)
      echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$ACTION" ]]; then
  echo "Error: --action required" >&2
  usage
fi

# Safety: Resolve paths within cwd
resolve_path() {
  local p="$1"
  # Remove any leading /
  p="${p#/}"
  # Ensure it doesn't contain ..
  if [[ "$p" == *".."* ]]; then
    echo "Error: Path contains '..' - not allowed" >&2
    exit 1
  fi
  echo "$p"
}

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${FILE_MANAGER_LOG:-$HOME/.openclaw/logs/file-manager.log}"
}

case $ACTION in
  read)
    [[ -z "$PATH" ]] && { echo "Error: --path required for read" >&2; exit 1; }
    FILE="$(resolve_path "$PATH")"
    if [[ ! -f "$FILE" ]]; then
      echo "Error: File not found: $FILE" >&2
      exit 1
    fi
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would read: $FILE"
      exit 0
    fi
    cat "$FILE"
    log "READ $FILE"
    ;;

  write)
    [[ -z "$PATH" ]] && { echo "Error: --path required for write" >&2; exit 1; }
    FILE="$(resolve_path "$PATH")"
    if [[ -z "$CONTENT" ]]; then
      # Read from stdin
      CONTENT=$(cat)
    fi
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would write to: $FILE ($(echo -n "$CONTENT" | wc -c) bytes)"
      exit 0
    fi
    mkdir -p "$(dirname "$FILE")"
    printf "%s" "$CONTENT" > "$FILE"
    log "WRITE $FILE ($(echo -n "$CONTENT" | wc -c) bytes)"
    ;;

  append)
    [[ -z "$PATH" ]] && { echo "Error: --path required for append" >&2; exit 1; }
    FILE="$(resolve_path "$PATH")"
    if [[ -z "$CONTENT" ]]; then
      CONTENT=$(cat)
    fi
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would append to: $FILE"
      exit 0
    fi
    mkdir -p "$(dirname "$FILE")"
    printf "%s\n" "$CONTENT" >> "$FILE"
    log "APPEND $FILE"
    ;;

  list)
    if [[ -z "$DIR" ]]; then
      DIR="."
    fi
    DIR="$(resolve_path "$DIR")"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would list: $DIR${PATTERN:+, pattern: $PATTERN}"
      exit 0
    fi
    if [[ -n "$PATTERN" ]]; then
      find "$DIR" -maxdepth 1 -type f -name "$PATTERN" -printf "%f\n"
    else
      find "$DIR" -maxdepth 1 -type f -printf "%f\n"
    fi
    log "LIST $DIR${PATTERN:+($PATTERN)}"
    ;;

  mkdir)
    [[ -z "$DIR" ]] && { echo "Error: --dir required for mkdir" >&2; exit 1; }
    DIR="$(resolve_path "$DIR")"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would create directory: $DIR"
      exit 0
    fi
    mkdir -p "$DIR"
    log "MKDIR $DIR"
    ;;

  delete)
    [[ -z "$PATH" ]] && { echo "Error: --path required for delete" >&2; exit 1; }
    FILE="$(resolve_path "$PATH")"
    if [[ ! -f "$FILE" ]]; then
      echo "Error: File not found: $FILE" >&2
      exit 1
    fi
    # Protect hidden files
    if [[ "$(basename "$FILE")" == .* ]]; then
      echo "Error: Cannot delete hidden files" >&2
      exit 1
    fi
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[DRY-RUN] Would delete: $FILE"
      exit 0
    fi
    rm "$FILE"
    log "DELETE $FILE"
    ;;

  *)
    echo "Error: Unknown action: $ACTION" >&2
    usage
    ;;
esac