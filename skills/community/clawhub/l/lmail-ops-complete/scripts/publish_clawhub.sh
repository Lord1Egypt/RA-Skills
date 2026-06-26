#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SLUG="${SLUG:-lmail-ops-complete}"
NAME="${NAME:-LMail Ops Complete}"
VERSION="${VERSION:-}"
CHANGELOG="${CHANGELOG:-Initial release}"
TAGS="${TAGS:-latest}"
PRINT_ONLY=false
CLI=()
PUBLISH_PATH=""
TMP_PUBLISH_ROOT=""

usage() {
  cat <<'USAGE'
Usage: publish_clawhub.sh --version <semver> [options]

Options:
  --version <semver>     Required publish version, e.g. 1.0.0
  --slug <slug>          Registry slug (default: lmail-ops-complete)
  --name <name>          Display name (default: LMail Ops Complete)
  --changelog <text>     Changelog text
  --tags <tags>          Comma-separated tags (default: latest)
  --print-only           Print publish command without executing
  -h, --help             Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      VERSION="$2"
      shift 2
      ;;
    --slug)
      SLUG="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --changelog)
      CHANGELOG="$2"
      shift 2
      ;;
    --tags)
      TAGS="$2"
      shift 2
      ;;
    --print-only)
      PRINT_ONLY=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  echo "[ERR] --version is required" >&2
  usage >&2
  exit 1
fi

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "[ERR] invalid semver version: $VERSION" >&2
  exit 1
fi

bash "$SCRIPT_DIR/validate_openclaw_skill.sh"

if command -v clawhub >/dev/null 2>&1; then
  CLI=(clawhub)
elif command -v npx >/dev/null 2>&1; then
  CLI=(npx -y clawhub)
else
  echo "[ERR] neither clawhub nor npx is available" >&2
  exit 1
fi

PUBLISH_PATH="$SKILL_DIR"
if ! git -C "$SKILL_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  TMP_PUBLISH_ROOT="$(mktemp -d)"
  cp -a "$SKILL_DIR" "$TMP_PUBLISH_ROOT/"
  git -C "$TMP_PUBLISH_ROOT" init -q
  git -C "$TMP_PUBLISH_ROOT" config user.email "clawhub-publish@local"
  git -C "$TMP_PUBLISH_ROOT" config user.name "clawhub-publish"
  git -C "$TMP_PUBLISH_ROOT" add "$(basename "$SKILL_DIR")"
  git -C "$TMP_PUBLISH_ROOT" commit -q -m "prepare skill publish"
  PUBLISH_PATH="$TMP_PUBLISH_ROOT/$(basename "$SKILL_DIR")"
  echo "[INFO] skill folder is not in a git repo; using temporary git snapshot at $PUBLISH_PATH"
fi

PUBLISH_CMD=(
  publish "$PUBLISH_PATH"
  --slug "$SLUG"
  --name "$NAME"
  --version "$VERSION"
  --changelog "$CHANGELOG"
  --tags "$TAGS"
)

echo "[INFO] publish command:"
printf '  %q' "${CLI[@]}"
printf ' %q' "${PUBLISH_CMD[@]}"
printf '\n'

if [[ "$PRINT_ONLY" == true ]]; then
  echo "[DONE] print-only mode"
  exit 0
fi

if ! "${CLI[@]}" whoami >/dev/null 2>&1; then
  echo "[ERR] not authenticated. Run: clawhub login" >&2
  exit 1
fi

"${CLI[@]}" "${PUBLISH_CMD[@]}"
echo "[DONE] publish finished"

if [[ -n "$TMP_PUBLISH_ROOT" && -d "$TMP_PUBLISH_ROOT" ]]; then
  rm -rf "$TMP_PUBLISH_ROOT"
fi
