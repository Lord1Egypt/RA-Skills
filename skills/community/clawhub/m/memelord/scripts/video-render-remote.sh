#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord: GET /api/video/render/remote?jobId=<id>
# Poll render job status (for ai-video-meme and ai-video-meme/edit when not using webhooks).

usage() {
  cat <<'USAGE'
Usage:
  video-render-remote.sh --job-id <render-job-id> [--out <json_path>]

Examples:
  ./video-render-remote.sh --job-id render-1740524400000-abc12
  ./video-render-remote.sh --job-id render-1740524400000-abc12 --out ./status.json
USAGE
}

JOB_ID=""
OUT=""

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --job-id) JOB_ID="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

: "${MEMELORD_API_KEY:?MEMELORD_API_KEY not set}"

if [[ -z "$JOB_ID" ]]; then
  echo "Missing --job-id" >&2
  usage
  exit 2
fi

URL="https://www.memelord.com/api/video/render/remote?jobId=$(node -p 'encodeURIComponent(process.argv[1])' "$JOB_ID")"

if [[ -n "$OUT" ]]; then
  curl -sS -X GET "$URL" \
    -H "Authorization: Bearer $MEMELORD_API_KEY" \
    -H 'Accept: application/json' \
    > "$OUT"
  echo "$OUT" >&2
else
  curl -sS -X GET "$URL" \
    -H "Authorization: Bearer $MEMELORD_API_KEY" \
    -H 'Accept: application/json'
fi
