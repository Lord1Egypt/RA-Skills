#!/bin/bash
# Sitemap generator — reads doc list from docs.json (local or GitHub)
# Usage: sitemap.sh [--version <tag>] [--json]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

JSON=false
[[ "${OPENCLAW_SAGE_OUTPUT}" == "json" ]] && JSON=true

parse_version_flag "$@"
set -- "${REMAINING_ARGS[@]}"
for arg in "$@"; do
  [ "$arg" = "--json" ] && JSON=true
done

REF="$VERSION"
[ "$VERSION" = "latest" ] && REF="main"
DOCS_JSON_CACHE="${VERSION_CACHE_DIR}/docs.json"

# Ensure docs.json is cached
if ! is_cache_fresh "$DOCS_JSON_CACHE" "$DOC_TTL"; then
  if [[ "$SOURCE" == local:* ]]; then
    local_path="${SOURCE#local:}"
    cp "${local_path}/docs.json" "$DOCS_JSON_CACHE" 2>/dev/null || {
      echo "Error: docs.json not found at ${local_path}/docs.json" >&2
      exit 1
    }
  else
    if check_online; then
      src_url="$(resolve_source_raw "docs.json" "$REF")"
      curl -sf --max-time 10 "$src_url" -o "$DOCS_JSON_CACHE" 2>/dev/null
    else
      echo "Offline: cannot reach GitHub" >&2
      [ -f "$DOCS_JSON_CACHE" ] && echo "Using stale cached docs.json." >&2
    fi
  fi
fi

if [ ! -f "$DOCS_JSON_CACHE" ]; then
  echo "Error: docs.json not available. Run build-index.sh fetch first." >&2
  exit 1
fi

_PYEOF_COLLECT='
import sys, json
from collections import defaultdict

with open(sys.argv[1]) as f:
    data = json.load(f)

def collect_pages(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from collect_pages(item)
    elif isinstance(node, dict):
        if "pages" in node:
            yield from collect_pages(node["pages"])
        else:
            for v in node.values():
                yield from collect_pages(v)

categories = defaultdict(list)
for path in collect_pages(data.get("navigation", {})):
    if "/" not in path:
        continue
    cat = path.split("/")[0]
    if cat:
        categories[cat].append(path)
'

if $JSON; then
  if ! command -v python3 &>/dev/null; then
    echo '{"error": "python3 required for --json output"}' >&2
    exit 1
  fi
  python3 - "$DOCS_JSON_CACHE" <<PYEOF
$_PYEOF_COLLECT
result = [{"category": cat, "paths": sorted(paths)}
          for cat, paths in sorted(categories.items())]
print(json.dumps(result, indent=2))
PYEOF
else
  python3 - "$DOCS_JSON_CACHE" <<PYEOF
$_PYEOF_COLLECT
for cat in sorted(categories):
    print(f"📁 /{cat}/")
    for path in sorted(categories[cat]):
        print(f"  - {path}")
    print()
PYEOF
fi
