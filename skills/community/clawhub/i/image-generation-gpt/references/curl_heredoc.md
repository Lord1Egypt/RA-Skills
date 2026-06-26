# curl + bash (Unix/macOS, no dependencies)

> Requires `curl` (preinstalled on macOS/Linux) and one of `python3`/`base64`/`openssl` for base64 decoding (try in that order — at least one is always available).

Run in a single shell call (avoid relying on exported variables persisting across tool calls).

## Common preamble — API key, sanitized filename, JSON-escape helper

```bash
# Prompt user if env var is not set
if [ -z "$WELLAPI_API_KEY" ]; then
  read -r -p "Enter WELLAPI_API_KEY: " WELLAPI_API_KEY
fi
API_KEY="$WELLAPI_API_KEY"
[ -z "$API_KEY" ] && { echo "Error: WELLAPI_API_KEY not provided." >&2; exit 2; }

# Map FORMAT → extension
ext_for_format() {
  case "${1,,}" in
    jpeg|jpg) printf .jpg ;;
    webp)     printf .webp ;;
    *)        printf .png ;;
  esac
}

# CRITICAL: sanitize any filename used in shell
sanitize_name() {
  local raw="$1" fallback="$2"
  local clean
  clean=$(echo "$raw" | tr -cd 'A-Za-z0-9._-')
  if [ -z "$clean" ]; then clean="$fallback"; fi
  if [[ ! "$clean" =~ \.(png|jpg|jpeg|webp)$ ]]; then clean="$clean.png"; fi
  printf '%s' "$clean"
}

# Robust JSON string escape (python3 if available, else minimal sed)
json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$1" 2>/dev/null \
    || printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
}

# Decode first b64_json from a JSON response into a file.
decode_to_file() {
  local json="$1" out="$2"
  if command -v python3 >/dev/null 2>&1; then
    printf '%s' "$json" | python3 -c '
import json, sys, base64
d = json.load(sys.stdin)
if "data" not in d or not d["data"]:
    sys.stderr.write("No image data: %r\n" % d); sys.exit(1)
b64 = d["data"][0]["b64_json"]
sys.stdout.buffer.write(base64.b64decode(b64))
' > "$out"
    return $?
  fi
  local b64
  b64=$(printf '%s' "$json" | sed -n 's/.*"b64_json"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
  [ -z "$b64" ] && { echo "Error: no b64_json. Response: $json" >&2; return 1; }
  if command -v base64 >/dev/null 2>&1; then
    printf '%s' "$b64" | base64 -d > "$out" 2>/dev/null \
      || printf '%s' "$b64" | base64 -D > "$out" 2>/dev/null
    [ -s "$out" ] && return 0
  fi
  if command -v openssl >/dev/null 2>&1; then
    printf '%s' "$b64" | openssl base64 -d -A > "$out"
    return $?
  fi
  echo "Error: no base64 decoder available (need python3, base64, or openssl)" >&2
  return 1
}
```

## Text-to-image — `/images/generations`

Body: `application/json`. Required: `model`, `prompt` (≤1000 chars), `n` (1–10).

```bash
MODEL="gpt-image-2"
PROMPT="大海"           # ≤ 1000 chars
SIZE="1024x1024"        # 1024x1024 | 1536x1024 | 1024x1536 | 2048x2048 | 2048x1152 | 3840x2160 | 2160x3840 | auto
QUALITY="low"           # low | medium | high | auto
FORMAT="jpeg"           # png | jpeg | webp
N=1                     # 1..10

EXT=$(ext_for_format "$FORMAT")
OUT_FILE=$(sanitize_name "wellapi-$(date +%Y%m%d-%H%M%S)$EXT" "wellapi-$(date +%s).png")

PROMPT_JSON=$(json_escape "$PROMPT")

RESP=$(curl -sS -X POST "https://wellapi.ai/v1/images/generations" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<WELL_END
{"model":"$MODEL","prompt":$PROMPT_JSON,"n":$N,"size":"$SIZE","quality":"$QUALITY","format":"$FORMAT"}
WELL_END
)

if ! decode_to_file "$RESP" "$OUT_FILE"; then
  echo "Error: decode failed. Raw (truncated): ${RESP:0:500}" >&2
  exit 1
fi

FULL_PATH="$(cd "$(dirname "$OUT_FILE")" && pwd)/$(basename "$OUT_FILE")"
echo "MEDIA:$FULL_PATH"
```

> For `n > 1`: parse `data[*].b64_json` (use python3) and write each to `wellapi-<ts>-1.<ext>`, `-2.<ext>`, … with one `MEDIA:` line per file.

## Image edit (image-to-image) — `/images/edits`

Body: `multipart/form-data`. `image` is **required** (repeatable, up to **16 files, total ≤ 50MB**).
Optional: `mask` (PNG ≤ 4MB, same WxH as image), `background` (`opaque`/`auto`/`transparent`), `moderation` (`low`/`auto`), `n`/`size`/`quality`/`format`.

```bash
MODEL="gpt-image-2"      # also: gpt-image-1, gpt-image-1-all, gpt-image-2-all, flux-kontext-pro, flux-kontext-max
PROMPT="将他们合并在一个图片里面"
SIZE="1024x1536"
QUALITY="auto"
FORMAT="png"
N=1
BACKGROUND=""            # opaque | auto | transparent (optional)
MODERATION=""            # low | auto (optional)

INPUT_IMAGES=( "./例子.png" "./场景2.png" )   # up to 16, total ≤ 50MB
MASK=""                                       # optional PNG, ≤ 4MB

# Validate inputs
[ "${#INPUT_IMAGES[@]}" -gt 16 ] && { echo "Error: >16 images." >&2; exit 2; }
TOTAL=0
for p in "${INPUT_IMAGES[@]}"; do
  [ -f "$p" ] || { echo "Error: image not found: $p" >&2; exit 2; }
  SZ=$(wc -c <"$p" | tr -d ' ')
  TOTAL=$((TOTAL + SZ))
done
[ "$TOTAL" -gt 52428800 ] && { echo "Error: total > 50MB ($TOTAL bytes)." >&2; exit 2; }

if [ -n "$MASK" ]; then
  [ -f "$MASK" ] || { echo "Error: mask not found: $MASK" >&2; exit 2; }
  MASK_SZ=$(wc -c <"$MASK" | tr -d ' ')
  [ "$MASK_SZ" -gt 4194304 ] && { echo "Error: mask > 4MB." >&2; exit 2; }
fi

EXT=$(ext_for_format "$FORMAT")
OUT_FILE=$(sanitize_name "wellapi-$(date +%Y%m%d-%H%M%S)$EXT" "wellapi-edit-$(date +%s).png")

# Build curl form args
CURL_ARGS=(-sS -X POST "https://wellapi.ai/v1/images/edits"
  -H "Authorization: Bearer $API_KEY"
  -F "model=$MODEL"
  -F "prompt=$PROMPT"
  -F "n=$N"
  -F "size=$SIZE"
  -F "quality=$QUALITY"
  -F "format=$FORMAT")

[ -n "$BACKGROUND" ] && CURL_ARGS+=(-F "background=$BACKGROUND")
[ -n "$MODERATION" ] && CURL_ARGS+=(-F "moderation=$MODERATION")

for p in "${INPUT_IMAGES[@]}"; do
  CURL_ARGS+=(-F "image=@${p}")
done
[ -n "$MASK" ] && CURL_ARGS+=(-F "mask=@${MASK}")

RESP=$(curl "${CURL_ARGS[@]}")

if ! decode_to_file "$RESP" "$OUT_FILE"; then
  echo "Error: decode failed. Raw (truncated): ${RESP:0:500}" >&2
  exit 1
fi

FULL_PATH="$(cd "$(dirname "$OUT_FILE")" && pwd)/$(basename "$OUT_FILE")"
echo "MEDIA:$FULL_PATH"
```

## Notes

- **Synchronous** — no polling.
- `data[i].b64_json` is the full image bytes, base64-encoded. Decode and save.
- For `n > 1`, iterate `data[*]` and emit one `MEDIA:` line per file (`-1`, `-2`, … suffixes).
- Always print `MEDIA:<absolute_path>` so OpenClaw auto-attaches the result.
- Size strict rules: multiples of 16, max side 3840, ratio ≤ 3:1, total pixels in [655360, 8294400].
