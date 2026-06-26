#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord: POST /api/v1/ai-meme
# - Safe JSON encoding for prompt, supports count/category/include_nsfw
# - Writes response JSON to --out (default: ./memelord_ai_meme.json)
# - Optionally downloads PNG(s) from results[].url or results[].base64

usage() {
  cat <<'USAGE'
Usage:
  ai-meme.sh "<prompt>" [--out <json_path>] [--png <png_path>] [--count <n>] [--category <trending|classic>] [--include-nsfw <true|false>]

Examples:
  ./ai-meme.sh "developer fixing bugs at 3am" --png ./meme.png
  ./ai-meme.sh "when the code works on the first try" --count 3 --png ./meme_%d.png
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

PROMPT="$1"; shift

OUT="./memelord_ai_meme.json"
PNG=""
COUNT=""
CATEGORY=""
INCLUDE_NSFW=""  # empty means omit (API default)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="$2"; shift 2;;
    --png) PNG="$2"; shift 2;;
    --count) COUNT="$2"; shift 2;;
    --category) CATEGORY="$2"; shift 2;;
    --include-nsfw) INCLUDE_NSFW="$2"; shift 2;;
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

node - <<'NODE' "$PROMPT" "$COUNT" "$CATEGORY" "$INCLUDE_NSFW" > "$TMP_BODY"
const prompt = process.argv[2];
const count = process.argv[3];
const category = process.argv[4];
const includeNsfw = process.argv[5];

const body = { prompt };
if (count) body.count = Number(count);
if (category) body.category = category;
if (includeNsfw !== '') {
  if (includeNsfw === 'true' || includeNsfw === 'false') body.include_nsfw = (includeNsfw === 'true');
  else throw new Error('--include-nsfw must be true or false');
}

process.stdout.write(JSON.stringify(body));
NODE

curl -sS -X POST 'https://www.memelord.com/api/v1/ai-meme' \
  -H "Authorization: Bearer $MEMELORD_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @"$TMP_BODY" \
  > "$OUT"

if [[ -n "$PNG" ]]; then
  node - "$OUT" "$PNG" <<'NODE'
const fs = require('fs');
const path = require('path');
const jsonPath = process.argv[2];
const pngPathArg = process.argv[3];
const j = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
if (!j.success) {
  console.error(j);
  process.exit(2);
}
const results = j.results || [];
if (!Array.isArray(results) || results.length === 0) throw new Error('No results[]');

function outPathForIndex(basePath, i){
  if (basePath.includes('%d')) return basePath.replace('%d', String(i));
  const ext = path.extname(basePath);
  const name = ext ? basePath.slice(0, -ext.length) : basePath;
  return results.length > 1 ? `${name}_${i}${ext || '.png'}` : (ext ? basePath : `${basePath}.png`);
}

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

(async () => {
  const written=[];
  for (let idx=0; idx<results.length; idx++){
    const r = results[idx];
    const out = outPathForIndex(pngPathArg, idx+1);

    const b64 = r?.base64;
    const url = r?.url;

    if (b64) {
      const m = b64.match(/^data:image\/(png|jpeg);base64,(.+)$/);
      if (!m) throw new Error('Unexpected base64 data URI');
      fs.writeFileSync(out, Buffer.from(m[2], 'base64'));
      written.push(out);
      continue;
    }

    if (url) {
      const https = require('https');
      await new Promise((resolve, reject) => {
        https.get(url, (res) => {
          if (res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
            https.get(res.headers.location, (res2) => pipeResToFile(res2, out, resolve, reject));
            return;
          }
          pipeResToFile(res, out, resolve, reject);
        }).on('error', reject);
      });
      written.push(out);
      continue;
    }

    throw new Error(`No base64 or url in results[${idx}]`);
  }
  console.log(written.join('\n'));
})().catch((err) => {
  console.error(err);
  process.exit(2);
});
NODE
fi

echo "$OUT" >&2
