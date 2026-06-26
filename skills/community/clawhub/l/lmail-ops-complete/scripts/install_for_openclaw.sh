#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_ROOT="/root/clawd/skills"
TARGET_ROOT_2=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET_ROOT="$2"
      shift 2
      ;;
    --target-2)
      TARGET_ROOT_2="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'USAGE'
Usage: install_for_openclaw.sh [--target /root/clawd/skills] [--target-2 /another/skills]

Copies this skill into OpenClaw skill directory/directories.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

install_one() {
  local root="$1"
  mkdir -p "$root"
  local dst="$root/lmail-ops-complete"
  rm -rf "$dst"
  cp -a "$SKILL_DIR" "$dst"
  rm -rf "$dst/scripts/__pycache__"
  echo "[OK] installed at $dst"
}

install_one "$TARGET_ROOT"
if [[ -n "$TARGET_ROOT_2" ]]; then
  install_one "$TARGET_ROOT_2"
fi

echo "[DONE] OpenClaw installation complete"
