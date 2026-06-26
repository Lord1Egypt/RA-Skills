#!/usr/bin/env bash
# detect-stale-config.sh <profile>
#
# Parse gateway status / plugins list output looking for warnings of the form:
#   "plugins.entries.<id>: plugin disabled (...) but config is present"
#
# Output one STALE line per detected stale entry:
#   STALE plugins.entries.<id>
#
# Exit: 0 always (advisory). If nothing detected, output is empty.

set -uo pipefail

PROFILE="${1:-}"
if [ -z "$PROFILE" ]; then
  echo "usage: detect-stale-config.sh <profile>" >&2
  exit 2
fi

# Collect warning text from the places that emit it.
TEXT=""
TEXT="$TEXT$(openclaw --profile "$PROFILE" gateway status 2>&1 || true)
"
TEXT="$TEXT$(openclaw --profile "$PROFILE" plugins list 2>&1 || true)
"

# Extract plugins.entries.<id> from "disabled ... but config is present"
# blocks. The CLI wraps warnings across multiple lines inside box-drawing
# characters, so we collapse whitespace and box-art before matching.
# Pass via env var (not stdin) so the heredoc carries the Python program.
PUM_RAW_TEXT="$TEXT" python3 <<'PY'
import os, re
raw = os.environ.get("PUM_RAW_TEXT", "")
flat = re.sub(r"[\u2500-\u257F|\u2502\u2503\u250F\u2513\u2517\u251B\u2520\u2528\u2530\u2538\u2541\u2548\u2562\u256C]", " ", raw)
flat = re.sub(r"\s+", " ", flat)
seen = set()
for m in re.finditer(r"plugins\.entries\.([a-zA-Z0-9._@/-]+)[^a-zA-Z0-9]+plugin\s+disabled[^.]*?but\s+config\s+is\s+present", flat, re.IGNORECASE):
    key = m.group(1)
    if key not in seen:
        seen.add(key)
        print(f"STALE plugins.entries.{key}")
PY
