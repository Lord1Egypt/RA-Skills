#!/usr/bin/env bash
# List available styles via GET /v1/styles.
# Usage: styles.sh
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"

args=(-sS -A "motu-mce-skill/1.0" "$BASE/v1/styles")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

curl "${args[@]}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.stderr.write("styles failed: non-JSON response from server\n")
    sys.exit(1)
styles = d.get("styles")
if styles is None:
    sys.stderr.write("styles failed: %s\n" % d.get("detail", d))
    sys.exit(1)
for s in styles:
    print("%-28s %-8s %s" % (s.get("id",""), s.get("kind",""),
                             s.get("name_zh") or s.get("name") or ""))
sep = d.get("composite_separator", "@")
print("\n# Combine a flavour with a base as  <flavour>%s<base>" % sep)
'
