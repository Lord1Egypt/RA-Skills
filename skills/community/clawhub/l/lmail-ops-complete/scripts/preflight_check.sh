#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${LMAIL_BASE_URL:-http://localhost:3001}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url)
      BASE_URL="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'USAGE'
Usage: preflight_check.sh [--base-url URL]

Checks required tools and /api/v1/health reachability.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

required=(python3 curl)
for cmd in "${required[@]}"; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[OK] tool found: $cmd"
  else
    echo "[ERR] missing tool: $cmd" >&2
    exit 1
  fi
done

health_json="$(curl -sS "${BASE_URL%/}/api/v1/health" || true)"
if [[ -z "$health_json" ]]; then
  echo "[ERR] health endpoint unreachable: ${BASE_URL%/}/api/v1/health" >&2
  exit 1
fi

echo "$health_json" | python3 -m json.tool >/dev/null 2>&1 || {
  echo "[ERR] health response is not valid JSON" >&2
  exit 1
}

echo "[OK] health endpoint reachable: ${BASE_URL%/}/api/v1/health"
echo "[DONE] preflight passed"
