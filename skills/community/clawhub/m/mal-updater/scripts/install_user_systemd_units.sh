#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/ops/systemd-user"
TARGET_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
SERVICE_ENV_SOURCE="$SOURCE_DIR/mal-updater-service.env.example"
SERVICE_ENV_TARGET="${XDG_CONFIG_HOME:-$HOME/.config}/mal-updater-service.env"
ENABLE_SERVICE=1
RELOAD_DAEMON=1
START_SERVICE=0
COPY_SERVICE_ENV=1
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: scripts/install_user_systemd_units.sh [options]

Render and install the repo-owned user-level MAL-Updater daemon service.

Options:
  --target-dir PATH           Override the systemd user unit target directory.
  --service-env-target PATH   Override where the optional service env file is copied.
  --no-enable                 Copy/update the service unit but do not enable it.
  --start-service             After install/reload, start the service immediately.
  --no-daemon-reload          Skip `systemctl --user daemon-reload`.
  --no-service-env            Do not copy the example service env file.
  --dry-run                   Print planned actions without changing anything.
  -h, --help                  Show this help.
EOF
}

log() {
  printf '%s\n' "$*"
}

run_cmd() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run]'
    for arg in "$@"; do
      printf ' %q' "$arg"
    done
    printf '\n'
    return 0
  fi
  "$@"
}

copy_file() {
  local source_path="$1"
  local target_path="$2"
  local mode="${3:-644}"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] install -D -m %s %q %q\n' "$mode" "$source_path" "$target_path"
    return 0
  fi
  install -D -m "$mode" "$source_path" "$target_path"
}

render_unit() {
  local source_path="$1"
  local target_path="$2"
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run] render %q -> %q\n' "$source_path" "$target_path"
    return 0
  fi
  python3 - "$source_path" "$target_path" "$ROOT_DIR" "$SERVICE_ENV_TARGET" <<'PY'
from pathlib import Path
import sys
source_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
repo_root = Path(sys.argv[3]).resolve()
service_env_target = sys.argv[4]
text = source_path.read_text(encoding='utf-8')
text = text.replace('__MAL_UPDATER_REPO_ROOT__', str(repo_root))
text = text.replace('__MAL_UPDATER_SERVICE_ENV_FILE__', service_env_target)
target_path.parent.mkdir(parents=True, exist_ok=True)
target_path.write_text(text, encoding='utf-8')
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir)
      [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 2; }
      TARGET_DIR="$2"
      shift 2
      ;;
    --service-env-target)
      [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 2; }
      SERVICE_ENV_TARGET="$2"
      shift 2
      ;;
    --no-enable)
      ENABLE_SERVICE=0
      shift
      ;;
    --start-service)
      START_SERVICE=1
      shift
      ;;
    --no-daemon-reload)
      RELOAD_DAEMON=0
      shift
      ;;
    --no-service-env)
      COPY_SERVICE_ENV=0
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

UNIT_NAME="mal-updater.service"
SOURCE_PATH="$SOURCE_DIR/$UNIT_NAME"
TARGET_PATH="$TARGET_DIR/$UNIT_NAME"

if [[ ! -f "$SOURCE_PATH" ]]; then
  echo "missing source unit file: $SOURCE_PATH" >&2
  exit 1
fi

log "repo_root=$ROOT_DIR"
log "source_dir=$SOURCE_DIR"
log "target_dir=$TARGET_DIR"
log "service_env_target=$SERVICE_ENV_TARGET"

rendered_content="$(python3 - "$SOURCE_PATH" "$ROOT_DIR" "$SERVICE_ENV_TARGET" <<'PY'
from pathlib import Path
import sys
source_path = Path(sys.argv[1])
repo_root = Path(sys.argv[2]).resolve()
service_env_target = sys.argv[3]
text = source_path.read_text(encoding='utf-8')
text = text.replace('__MAL_UPDATER_REPO_ROOT__', str(repo_root))
text = text.replace('__MAL_UPDATER_SERVICE_ENV_FILE__', service_env_target)
print(text, end='')
PY
)"

if [[ ! -e "$TARGET_PATH" ]]; then
  log "installed_units=$UNIT_NAME"
elif [[ "$(cat "$TARGET_PATH")" == "$rendered_content" ]]; then
  log "unchanged_units=$UNIT_NAME"
else
  log "updated_units=$UNIT_NAME"
fi
render_unit "$SOURCE_PATH" "$TARGET_PATH"

service_env_action="skipped"
if [[ "$COPY_SERVICE_ENV" == "1" ]]; then
  if [[ -e "$SERVICE_ENV_TARGET" ]]; then
    service_env_action="preserved"
    log "service env already exists; leaving it untouched: $SERVICE_ENV_TARGET"
  else
    service_env_action="installed"
    copy_file "$SERVICE_ENV_SOURCE" "$SERVICE_ENV_TARGET"
  fi
fi
log "service_env_action=$service_env_action"

if [[ "$RELOAD_DAEMON" == "1" ]]; then
  run_cmd systemctl --user daemon-reload
fi

if [[ "$ENABLE_SERVICE" == "1" ]]; then
  run_cmd systemctl --user enable "$UNIT_NAME"
else
  log "service enable skipped (--no-enable)"
fi

if [[ "$START_SERVICE" == "1" ]]; then
  run_cmd systemctl --user restart "$UNIT_NAME"
fi

if ! run_cmd systemctl --user status "$UNIT_NAME" --no-pager; then
  log "service status probe failed; continuing"
fi

log "user-level MAL-Updater systemd service install completed"
