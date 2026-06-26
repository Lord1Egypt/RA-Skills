#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord: POST /api/v1/ai-video-meme
# Starts async render jobs; if webhookUrl is provided, results are posted there.

usage() {
  cat <<'USAGE'
Usage:
  ai-video-meme.sh "<prompt>" [--out <json_path>] [--count <n>] [--category <trending|classic>] \
    [--template-id <id>] [--webhook-url <url>] [--webhook-secret <secret>]

Examples:
  ./ai-video-meme.sh "when the code works on the first try" --count 2 --out ./jobs.json
  ./ai-video-meme.sh "ship it" --webhook-url https://example.com/webhook --webhook-secret supersecret
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

PROMPT="$1"; shift

OUT="./memelord_ai_video_meme.json"
COUNT=""
CATEGORY=""
TEMPLATE_ID=""
WEBHOOK_URL=""
WEBHOOK_SECRET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --count) COUNT="$2"; shift 2;;
    --category) CATEGORY="$2"; shift 2;;
    --template-id) TEMPLATE_ID="$2"; shift 2;;
    --webhook-url) WEBHOOK_URL="$2"; shift 2;;
    --webhook-secret) WEBHOOK_SECRET="$2"; shift 2;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

: "${MEMELORD_API_KEY:?MEMELORD_API_KEY not set}"

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

node - <<'NODE' "$PROMPT" "$COUNT" "$WEBHOOK_URL" "$WEBHOOK_SECRET" "$CATEGORY" "$TEMPLATE_ID" > "$TMP_BODY"
const prompt = process.argv[2];
const count = process.argv[3];
const webhookUrl = process.argv[4];
const webhookSecret = process.argv[5];
const category = process.argv[6];
const templateId = process.argv[7];

const body = { prompt };
if (count) body.count = Number(count);
if (webhookUrl) body.webhookUrl = webhookUrl;
if (webhookSecret) body.webhookSecret = webhookSecret;
if (category) body.category = category;
if (templateId) body.template_id = templateId;

process.stdout.write(JSON.stringify(body));
NODE

curl -sS -X POST 'https://www.memelord.com/api/v1/ai-video-meme' \
  -H "Authorization: Bearer $MEMELORD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @"$TMP_BODY" \
  > "$OUT"

echo "$OUT" >&2
