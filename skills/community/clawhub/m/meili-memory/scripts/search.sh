#!/bin/bash
# Tiered memory search with tag-based query understanding
# Usage: bash search.sh "query" [limit] [tier]
# Tiers: core, working, archive, all (default: all)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

QUERY="${1}"
LIMIT="${2:-5}"
FILTER_TIER="${3:-all}"

if [ -z "$QUERY" ]; then
  echo '{"error":"Usage: search.sh <query> [limit] [tier]"}' >&2
  exit 1
fi

# Secure temp file helper
tmpfile() {
  local f
  f=$(mktemp /tmp/meili-search.XXXXXX)
  chmod 600 "$f"
  echo "$f"
}

cleanup_files=()
cleanup() {
  for f in "${cleanup_files[@]}"; do
    rm -f "$f" 2>/dev/null
  done
}
trap cleanup EXIT

if [ "$FILTER_TIER" = "all" ]; then
  TIERS="core working archive"
else
  TIERS="$FILTER_TIER"
fi

QUERY_FILE=$(tmpfile)
cleanup_files+=("$QUERY_FILE")

python3 - "$QUERY" "$LIMIT" "$TIERS" "$MEILI_HOST" "$MEILI_KEY" "$QUERY_FILE" << 'PYEOF'
import json, subprocess, sys, os

query = sys.argv[1]
limit = int(sys.argv[2])
tiers = sys.argv[3].split()
ms_host = sys.argv[4]
ms_key = sys.argv[5]
query_file = sys.argv[6]

# Query understanding: map natural language patterns to tag filters.
# Each entry: (list_of_patterns, list_of_tag_filters)
# Patterns are matched case-insensitive. Multiple patterns in an entry
# are OR'd together; multiple entries are OR'd together.
QUERY_RULES = [
    # Finance / debts
    (["debt", "owe", "loan", "liabilit", "payment"],
     ["finance/debts", "finance"]),
    # Projects / repos
    (["project", "repo", "repository", "application"],
     ["project"]),
    # Identity / personal
    (["identity", "profile", "personal"],
     ["identity"]),
    # Finance / budget
    (["finance", "budget", "expense", "income", "savings", "net worth", "asset"],
     ["finance/debts", "finance"]),
    # Work / development
    (["work", "career", "job", "internship", "coding", "development", "programming"],
     ["work/development"]),
    # Schedules
    (["schedule", "cron", "daily", "weekly", "reminder", "calendar"],
     ["schedule"]),
    # Skills / plugins
    (["skill", "plugin", "installed", "extension"],
     ["skills"]),
    # Infrastructure
    (["server", "openclaw", "gateway", "meilisearch", "systemd", "linux", "hosting"],
     ["infrastructure/meilisearch", "infrastructure/openclaw"]),
    # Auth / credentials
    (["auth", "login", "token", "credential", "password", "oauth", "api key"],
     ["auth/github", "auth/google"]),
]

query_lower = query.lower()
detected_filters = []
for patterns, tags in QUERY_RULES:
    for pattern in patterns:
        if pattern in query_lower:
            for tag in tags:
                if tag not in detected_filters:
                    detected_filters.append(tag)
            break

all_results = []
seen_ids = set()

for tier in tiers:
    payload = {
        "q": query,
        "limit": limit * 2,
        "attributesToRetrieve": ["id", "text", "source", "file", "category", "importance", "date", "tags", "tier"],
        "attributesToHighlight": ["text"],
        "highlightPreTag": "**",
        "highlightPostTag": "**"
    }

    # Add tag filters if we detected known categories
    if detected_filters:
        payload["filter"] = " OR ".join(f'tags = "{t}"' for t in detected_filters)

    with open(query_file, "w") as f:
        json.dump(payload, f)
    os.chmod(query_file, 0o600)

    result = subprocess.run([
        "curl", "-s",
        f"{ms_host}/indexes/{tier}/search",
        "-H", f"Authorization: Bearer {ms_key}",
        "-H", "Content-Type: application/json",
        "-d", f"@{query_file}"
    ], capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
        hits = data.get("hits", [])
        for h in hits:
            if h["id"] not in seen_ids:
                seen_ids.add(h["id"])
                h["_tier"] = tier
                all_results.append(h)
    except:
        pass

# If tag-filtered search returned nothing, fall back to plain full-text search
if not all_results and detected_filters:
    for tier in tiers:
        payload = {
            "q": query,
            "limit": limit,
            "attributesToRetrieve": ["id", "text", "source", "file", "category", "importance", "date", "tags", "tier"],
            "attributesToHighlight": ["text"],
            "highlightPreTag": "**",
            "highlightPostTag": "**"
        }
        with open(query_file, "w") as f:
            json.dump(payload, f)

        result = subprocess.run([
            "curl", "-s",
            f"{ms_host}/indexes/{tier}/search",
            "-H", f"Authorization: Bearer {ms_key}",
            "-H", "Content-Type: application/json",
            "-d", f"@{query_file}"
        ], capture_output=True, text=True)

        try:
            data = json.loads(result.stdout)
            hits = data.get("hits", [])
            for h in hits:
                if h["id"] not in seen_ids:
                    seen_ids.add(h["id"])
                    h["_tier"] = tier
                    all_results.append(h)
        except:
            pass

tier_order = {"core": 0, "working": 1, "archive": 2}
all_results.sort(key=lambda x: (tier_order.get(x.get("_tier", "archive"), 2), -x.get("importance", 0)))

output = {
    "query": query,
    "matched_filters": detected_filters,
    "tiers_searched": tiers,
    "total_found": len(all_results),
    "results": all_results[:limit]
}
print(json.dumps(output, indent=2))
PYEOF
