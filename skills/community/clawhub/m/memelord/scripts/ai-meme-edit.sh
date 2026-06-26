#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord: POST /api/v1/ai-meme/edit
# Provide:
#   - instruction (string)
#   - template_id (string)
#   - template_data (object)
# Option A: pass --from <ai-meme-response.json> to auto-pull template_id + template_data from results[0]
# Option B: pass --template-id + --template-data (JSON string) OR --template-data-file

usage() {
  cat <<'USAGE'
Usage:
  ai-meme-edit.sh --instruction "<what to change>" [--out <json_path>] [--png <png_path>] \
    (--from <ai_meme_json> | --template-id <id> (--template-data '<json>' | --template-data-file <path>)) \
    [--target-index <n>]

Examples:
  # Edit from a previous generation response:
  ./ai-meme-edit.sh --from ./memelord_ai_meme.json --instruction "make it about javascript instead" --png ./edited.png

  # Provide explicit template id + data:
  ./ai-meme-edit.sh --template-id abc-123 --template-data-file ./template_data.json \
    --instruction "change the top text" --out ./edit.json
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

OUT="./memelord_ai_meme_edit.json"
PNG=""
INSTRUCTION=""
FROM_JSON=""
TEMPLATE_ID=""
TEMPLATE_DATA_JSON=""
TEMPLATE_DATA_FILE=""
TARGET_INDEX=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --png) PNG="$2"; shift 2;;
    --instruction) INSTRUCTION="$2"; shift 2;;
    --from) FROM_JSON="$2"; shift 2;;
    --template-id) TEMPLATE_ID="$2"; shift 2;;
    --template-data) TEMPLATE_DATA_JSON="$2"; shift 2;;
    --template-data-file) TEMPLATE_DATA_FILE="$2"; shift 2;;
    --target-index) TARGET_INDEX="$2"; shift 2;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2
      ;;
  esac
done

: "${MEMELORD_API_KEY:?MEMELORD_API_KEY not set}"

if [[ -z "$INSTRUCTION" ]]; then
  echo "Missing --instruction" >&2
  exit 2
fi

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

# Build request body using node for robust JSON handling
node - <<'NODE' \
  "$INSTRUCTION" "$FROM_JSON" "$TEMPLATE_ID" "$TEMPLATE_DATA_JSON" "$TEMPLATE_DATA_FILE" "$TARGET_INDEX" \
  > "$TMP_BODY"
const fs = require('fs');

const instruction = process.argv[2];
const fromJson = process.argv[3];
let templateId = process.argv[4];
let templateDataJson = process.argv[5];
const templateDataFile = process.argv[6];
const targetIndex = process.argv[7];

let templateData;

if (fromJson) {
  const j = JSON.parse(fs.readFileSync(fromJson, 'utf8'));
  const r = (j.results && j.results[0]) || null;
  if (!r) throw new Error('Could not find results[0] in --from JSON');
  templateId = r.template_id || r.templateId || templateId;
  templateData = r.template_data || r.templateData || null;
  if (!templateId) throw new Error('Missing template_id in --from JSON');
  if (!templateData) throw new Error('Missing template_data in --from JSON');
} else {
  if (!templateId) throw new Error('Missing --template-id (or use --from)');
  if (templateDataFile) templateDataJson = fs.readFileSync(templateDataFile, 'utf8');
  if (!templateDataJson) throw new Error('Missing --template-data or --template-data-file (or use --from)');
  templateData = JSON.parse(templateDataJson);
}

const body = {
  instruction,
  template_id: templateId,
  template_data: templateData,
};

if (targetIndex) body.target_index = Number(targetIndex);

process.stdout.write(JSON.stringify(body));
NODE

curl -sS -X POST 'https://www.memelord.com/api/v1/ai-meme/edit' \
  -H "Authorization: Bearer $MEMELORD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @"$TMP_BODY" \
  > "$OUT"

if [[ -n "$PNG" ]]; then
  node - "$OUT" "$PNG" <<'NODE'
const fs = require('fs');
const https = require('https');
const j = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = process.argv[3];
if (!j.success) { console.error(j); process.exit(2); }
const url = j.url;
if (!url) throw new Error('No url in response');

function pipeResToFile(res, out, resolve, reject) {
  if (!res.statusCode || res.statusCode < 200 || res.statusCode >= 300) {
    reject(new Error(`Failed to fetch image (status ${res.statusCode})`));
    return;
  }
  const file = fs.createWriteStream(out);
  res.pipe(file);
  file.on('finish', () => file.close(resolve));
  file.on('error', reject);
}

https.get(url, (res) => {
  if (res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
    https.get(res.headers.location, (res2) => pipeResToFile(res2, out, () => {}, (e) => { throw e; }));
    return;
  }
  pipeResToFile(res, out, () => {}, (e) => { throw e; });
}).on('error', (e) => { throw e; });
NODE
fi

echo "$OUT" >&2
