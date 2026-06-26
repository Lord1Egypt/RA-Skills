#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord: POST /api/v1/ai-video-meme/edit
# Edits the caption of an existing video meme (async job).

usage() {
  cat <<'USAGE'
Usage:
  ai-video-meme-edit.sh \
    --template-id <id> \
    --caption "<current caption>" \
    --instruction "<what to change>" \
    [--audio-overlay-url <url>] \
    [--webhook-url <url>] \
    [--out <json_path>]

Examples:
  ./ai-video-meme-edit.sh --template-id abc-123 \
    --caption "When the code works on the first try" \
    --instruction "make it about not knowing why it works" \
    --out ./video_edit_job.json

  ./ai-video-meme-edit.sh --template-id abc-123 \
    --caption "Ship it" --instruction "make it more hype" \
    --audio-overlay-url https://example.com/audio.mp3 \
    --webhook-url https://example.com/webhook
USAGE
}

OUT="./memelord_ai_video_meme_edit.json"
TEMPLATE_ID=""
CAPTION=""
INSTRUCTION=""
AUDIO_OVERLAY_URL=""
WEBHOOK_URL=""

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --template-id) TEMPLATE_ID="$2"; shift 2;;
    --caption) CAPTION="$2"; shift 2;;
    --instruction) INSTRUCTION="$2"; shift 2;;
    --audio-overlay-url) AUDIO_OVERLAY_URL="$2"; shift 2;;
    --webhook-url) WEBHOOK_URL="$2"; shift 2;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

: "${MEMELORD_API_KEY:?MEMELORD_API_KEY not set}"

if [[ -z "$TEMPLATE_ID" || -z "$CAPTION" || -z "$INSTRUCTION" ]]; then
  echo "Missing required args: --template-id, --caption, --instruction" >&2
  usage
  exit 2
fi

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

node - <<'NODE' "$TEMPLATE_ID" "$CAPTION" "$INSTRUCTION" "$AUDIO_OVERLAY_URL" "$WEBHOOK_URL" > "$TMP_BODY"
const template_id = process.argv[2];
const caption = process.argv[3];
const instruction = process.argv[4];
const audio_overlay_url = process.argv[5];
const webhookUrl = process.argv[6];

const body = { template_id, caption, instruction };
if (audio_overlay_url) body.audio_overlay_url = audio_overlay_url;
if (webhookUrl) body.webhookUrl = webhookUrl;

process.stdout.write(JSON.stringify(body));
NODE

curl -sS -X POST 'https://www.memelord.com/api/v1/ai-video-meme/edit' \
  -H "Authorization: Bearer $MEMELORD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @"$TMP_BODY" \
  > "$OUT"

echo "$OUT" >&2
