#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
n=$(ls "$HERE/policies"/pol-*.txt 2>/dev/null | wc -l)
echo "policies=$n"
python3 - "$HERE/config/policy.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("manifest entries=%d min_expected=%d" % (len(d.get("policies") or []), d.get("min_expected", 0)))
PY
