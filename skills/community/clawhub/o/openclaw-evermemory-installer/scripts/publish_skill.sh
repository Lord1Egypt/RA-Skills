#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="${ROOT_DIR}/skills/openclaw-evermemory-installer"
SLUG="openclaw-evermemory-installer"
NAME="OpenClaw EverMemory Installer"
VERSION=""
CHANGELOG="Release from evermemory repository"
TAGS="latest"

usage() {
  cat <<'USAGE'
Usage:
  publish_skill.sh [options]

Options:
  --version <semver>      Required skill version (example: 0.1.0)
  --changelog <text>      Changelog text
  --slug <slug>           Skill slug (default: openclaw-evermemory-installer)
  --name <name>           Display name
  --tags <csv>            Comma-separated tags (default: latest)
  -h, --help              Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="${2:-}"
      shift 2
      ;;
    --changelog)
      CHANGELOG="${2:-}"
      shift 2
      ;;
    --slug)
      SLUG="${2:-}"
      shift 2
      ;;
    --name)
      NAME="${2:-}"
      shift 2
      ;;
    --tags)
      TAGS="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unsupported argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "[ERROR] --version is required." >&2
  exit 1
fi

echo "[INFO] Checking ClawHub login"
if ! clawhub whoami >/dev/null 2>&1; then
  echo "[ERROR] Not logged in to ClawHub. Run: clawhub login" >&2
  exit 1
fi

echo "[INFO] Publishing skill from: $SKILL_DIR"
clawhub publish "$SKILL_DIR" \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "$TAGS"

echo "[PASS] Skill publish command completed."
