#!/usr/bin/env bash
# List available portrait crop specs via GET /v1/crop/specs.
# Usage: crop-specs.sh
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"

args=(-sS -A "motu-mce-skill/1.0" "$BASE/v1/crop/specs")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

curl "${args[@]}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.stderr.write("crop-specs failed: non-JSON response from server\n")
    sys.exit(1)
specs = d.get("specs")
if specs is None:
    sys.stderr.write("crop-specs failed: %s\n" % d.get("detail", d))
    sys.exit(1)
by_cat = {}
for s in specs:
    by_cat.setdefault(s.get("category", "other"), []).append(s)
for cat in ("id_photo", "portrait", "avatar"):
    items = by_cat.get(cat)
    if not items:
        continue
    print("# %s" % cat)
    for s in items:
        bg = ",".join(sorted(s.get("bg_colors") or {})) or "-"
        print("%-16s %-22s %4dx%-4dpx  bg=%s" % (
            s.get("id", ""), s.get("name_zh") or s.get("name") or "",
            s.get("width_px", 0), s.get("height_px", 0), bg))
    print()
print("# Pass a spec id as crop-spec to scripts/crop.sh or scripts/grade.sh.")
'
