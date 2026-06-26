#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Memelord render helper
# - Safely JSON-encodes prompts (avoids shell-quote footguns like WE'RE / WHAT'S)
# - Writes response JSON to --out (default: ./memelord_render.json)
# - Optionally writes a PNG file if base64 is present

usage() {
  cat <<'USAGE'
Usage:
  render.sh "<prompt>" [--out <json_path>] [--png <png_path>] [--count <n>]

Examples:
  ./render.sh "Make a meme about venture capital. Founder says we're changing the world." \
    --out ./vc.json --png ./vc.png
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || ${1:-} == "" ]]; then
  usage
  exit 0
fi

PROMPT="$1"
shift

OUT="./memelord_render.json"
PNG=""
COUNT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      OUT="$2"; shift 2;;
    --png)
      PNG="$2"; shift 2;;
    --count)
      COUNT="$2"; shift 2;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2;;
  esac
done

: "${MEMELORD_API_KEY:?MEMELORD_API_KEY not set}"

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

if [[ -n "$COUNT" ]]; then
  node -p 'JSON.stringify({prompt: process.argv[1], count: Number(process.argv[2])})' "$PROMPT" "$COUNT" > "$TMP_BODY"
else
  node -p 'JSON.stringify({prompt: process.argv[1]})' "$PROMPT" > "$TMP_BODY"
fi

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
  // If user provided a printf-style pattern, use it.
  if (basePath.includes('%d')) return basePath.replace('%d', String(i));
  // Otherwise, insert _<i> before extension when multiple.
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
      // Fallback: fetch the image from a URL if the API returns urls instead of base64.
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
