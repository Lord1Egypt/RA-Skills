#!/usr/bin/env bash
# List server-approved clothing styles via GET /v1/outfits.
# Usage: outfits.sh
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"

args=(-sS -A "motu-mce-skill/1.0" "$BASE/v1/outfits")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

curl "${args[@]}" | python3 -c '
import json, sys
try:
    body = json.load(sys.stdin)
except Exception:
    sys.stderr.write("outfits failed: non-JSON response from server\n")
    sys.exit(1)
items = body.get("outfits")
if items is None:
    sys.stderr.write("outfits failed: %s\n" % body.get("detail", body))
    sys.exit(1)
available = [item for item in items if item.get("available")]
if not available:
    print("# No approved outfits are currently available.")
    sys.exit(0)
print("# Use one of these ids with scripts/outfit.sh or scripts/id-pack.sh")
for item in sorted(available, key=lambda value: (value.get("category", ""), value.get("order", 0), value.get("id", ""))):
    print("%-8s %-32s %s" % (
        item.get("category", "unisex"), item.get("id", ""),
        item.get("name_zh") or item.get("name") or item.get("description") or "",
    ))
'
