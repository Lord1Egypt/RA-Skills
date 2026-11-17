#!/usr/bin/env bash
# Replace clothing with a server-approved outfit via POST /v1/outfit.
# Usage: outfit.sh <input-image> <output.png> <outfit-id> [long-edge]
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: outfit.sh <input-image> <output.png> <outfit-id> [long-edge]}"
OUT="${2:?usage: outfit.sh <input-image> <output.png> <outfit-id> [long-edge]}"
OUTFIT="${3:?usage: outfit.sh <input-image> <output.png> <outfit-id> [long-edge]}"
LONG_EDGE="${4:-1536}"
[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

RESP="$(mktemp)"
trap 'rm -f "$RESP"' EXIT
args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/outfit"
  -F "file=@$IN" -F "outfit_id=$OUTFIT" -F "long_edge=$LONG_EDGE")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")
curl "${args[@]}" > "$RESP"
python3 - "$RESP" "$OUT" <<'PYCODE'
import base64, json, pathlib, sys
body = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
if body.get("detail"):
    raise SystemExit("outfit failed: %s" % body["detail"])
data = body.get("image_base64")
if not data:
    raise SystemExit("outfit failed: response has no image")
out = pathlib.Path(sys.argv[2])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(base64.b64decode(data))
print("saved %s  outfit=%s  task=%s" % (out, body.get("outfit_id"), body.get("task_id")))
PYCODE
