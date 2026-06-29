#!/bin/bash
# Search past learnings before acting to avoid repeating mistakes
# Usage: bash search_learnings.sh "query" [limit] [category]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

QUERY="${1}"
LIMIT="${2:-5}"
FILTER_cat="${3:-}"

if [ -z "$QUERY" ]; then
  echo '{"error":"Usage: search_learnings.sh <query> [limit] [category]"}' >&2
  exit 1
fi

# Secure tmp file for query payload
QUERY_FILE=$(mktemp /tmp/learn-search.XXXXXX)
chmod 600 "$QUERY_FILE"
cleanup() { rm -f "$QUERY_FILE"; }
trap cleanup EXIT

python3 - "$QUERY" "$LIMIT" "$FILTER_cat" "$MEILI_HOST" "$MEILI_KEY" "$QUERY_FILE" << 'PYEOF'
import json, subprocess, sys

query = sys.argv[1]
limit = int(sys.argv[2])
filter_cat = sys.argv[3]
ms_host = sys.argv[4]
ms_key = sys.argv[5]
query_file = sys.argv[6]

payload = {
    "q": query,
    "limit": limit,
    "attributesToRetrieve": ["id", "what_happened", "fix", "context", "category", "importance", "date", "tags"],
}
if filter_cat:
    payload["filter"] = f"category = {filter_cat}"

with open(query_file, "w") as f:
    json.dump(payload, f)

result = subprocess.run([
    "curl", "-s",
    f"{ms_host}/indexes/learnings/search",
    "-H", f"Authorization: Bearer {ms_key}",
    "-H", "Content-Type: application/json",
    "-d", f"@{query_file}"
], capture_output=True, text=True)

try:
    data = json.loads(result.stdout)
    output = {
        "query": query,
        "total_found": data.get("estimatedTotalHits", 0),
        "results": data.get("hits", [])
    }
    print(json.dumps(output, indent=2))
except:
    print(json.dumps({"query": query, "error": "search failed"}))
PYEOF
