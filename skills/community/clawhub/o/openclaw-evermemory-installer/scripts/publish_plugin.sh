#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DRY_RUN="true"
TAG="latest"

usage() {
  cat <<'USAGE'
Usage:
  publish_plugin.sh [options]

Options:
  --dry-run                Run npm publish --dry-run (default)
  --no-dry-run             Run real npm publish
  --tag <tag>              npm publish tag (default: latest)
  -h, --help               Show this help
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --no-dry-run)
      DRY_RUN="false"
      shift
      ;;
    --tag)
      TAG="${2:-}"
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

cd "$ROOT_DIR"

if node -e "const p=require('./package.json'); if (p.private) process.exit(1)"; then
  :
else
  echo "[ERROR] package.json has private=true. Set private=false before publish." >&2
  exit 1
fi

echo "[INFO] Running release gates before publish"
npm run teams:release
npm run release:pack

publish_cmd=(npm publish --access public --tag "$TAG")
if [[ "$DRY_RUN" == "true" ]]; then
  publish_cmd+=(--dry-run)
fi

echo "[INFO] Running: ${publish_cmd[*]}"
"${publish_cmd[@]}"

echo "[PASS] Plugin publish command completed."
