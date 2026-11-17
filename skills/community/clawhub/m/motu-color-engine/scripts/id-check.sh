#!/usr/bin/env bash
# Check an ID photo against a crop spec via POST /v1/id-check.
# Usage: id-check.sh <input> [spec-id] [report-json]
#   input       source portrait or already-cropped ID photo
#   spec-id     crop spec id (default: passport_cn)
#   report-json optional crop/.mce report JSON; when provided, input is treated as the already-cropped image
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: id-check.sh <input> [spec-id] [report-json]}"
SPEC="${2:-passport_cn}"
REPORT="${3:-}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }
args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/id-check"
  -F "file=@$IN"
  -F "spec=$SPEC")
[ -n "$REPORT" ] && args+=(-F "report_json=$(cat "$REPORT")")
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

curl "${args[@]}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.stderr.write("id-check failed: non-JSON response from server\n")
    sys.exit(1)
if "ok" not in d:
    sys.stderr.write("id-check failed: %s\n" % d.get("detail", d))
    sys.exit(1)
print("status=%s ok=%s" % (d.get("status"), d.get("ok")))
for name, check in (d.get("checks") or {}).items():
    print("  %-16s %s value=%s expected=%s" % (name, "ok" if check.get("ok") else "fail", check.get("value"), check.get("expected")))
for w in d.get("warnings") or []:
    print("  [warn] %s" % w)
for e in d.get("errors") or []:
    print("  [error] %s" % e)
sys.exit(0 if d.get("ok") else 1)
'
