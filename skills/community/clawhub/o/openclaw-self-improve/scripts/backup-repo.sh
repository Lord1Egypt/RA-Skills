#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  backup-repo.sh --repo <path> --backup-dir <dir> [--exclude <pattern>] [--timestamp <ts>]

Creates a zip backup of a repository for rollback purposes.
Useful for non-git repositories or as an additional safety measure.

Options:
  --repo <path>                 Repository path to back up
  --backup-dir <dir>            Directory where the zip backup is written
  --exclude <pattern>           Extra exclude pattern (repeatable)
  --timestamp <YYYYMMDD-HHMMSS> Custom timestamp (default: current UTC)
  -h, --help                    Show this message

Prints the absolute path of the created backup file on success.
USAGE
}

REPO=""
BACKUP_DIR=""
TIMESTAMP="$(date -u +%Y%m%d-%H%M%S)"
EXTRA_EXCLUDES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --backup-dir) BACKUP_DIR="${2:-}"; shift 2 ;;
    --timestamp) TIMESTAMP="${2:-}"; shift 2 ;;
    --exclude) EXTRA_EXCLUDES+=("${2:-}"); shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Missing required --repo <path>" >&2; usage >&2; exit 1
fi
if [[ -z "$BACKUP_DIR" ]]; then
  echo "Missing required --backup-dir <dir>" >&2; usage >&2; exit 1
fi
if [[ ! -d "$REPO" ]]; then
  echo "Repository path does not exist: $REPO" >&2; exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
  echo "zip command not found in PATH; install it first." >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"
BACKUP_DIR_ABS="$(cd "$BACKUP_DIR" && pwd)"
REPO_ABS="$(cd "$REPO" && pwd)"
REPO_NAME="$(basename "$REPO_ABS")"
BACKUP_FILE="$BACKUP_DIR_ABS/${REPO_NAME}_backup_${TIMESTAMP}.zip"

# Default exclude patterns
DEFAULT_EXCLUDES=(
  ".git/*" "*/.git/*"
  "node_modules/*" "*/node_modules/*"
  ".venv/*" "*/.venv/*"
  "venv/*" "*/venv/*"
  "__pycache__/*" "*/__pycache__/*"
  ".pytest_cache/*" "*/.pytest_cache/*"
  "dist/*" "*/dist/*"
  "build/*" "*/build/*"
  ".DS_Store" "*/.DS_Store"
  "*.log"
  ".openclaw-self-improve/*" "*/.openclaw-self-improve/*"
)

# Build the zip command as an array; never use eval.
CMD=(zip -r -q "$BACKUP_FILE" ".")
for excl in "${DEFAULT_EXCLUDES[@]}"; do
  CMD+=(-x "$excl")
done
for excl in "${EXTRA_EXCLUDES[@]}"; do
  [[ -n "$excl" ]] && CMD+=(-x "$excl")
done

# Run zip from inside the repo so paths are clean.
if (cd "$REPO_ABS" && "${CMD[@]}") >/dev/null 2>&1; then
  printf '%s\n' "$BACKUP_FILE"
else
  rc=$?
  echo "Failed to create backup at $BACKUP_FILE (zip exit code $rc)" >&2
  exit 1
fi
