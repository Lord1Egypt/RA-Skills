#!/bin/bash
# Log a learning entry (failure, correction, version rule, etc.)
# Usage: bash log_learning.sh --category <category> --what <description> --fix <solution> [--context <context>] [--importance <0-1>] [--tags <tag1,tag2>]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

# Parse arguments
CATEGORY=""
WHAT=""
FIX=""
CONTEXT=""
IMPORTANCE="0.7"
TAGS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --category) CATEGORY="$2"; shift 2;;
    --what) WHAT="$2"; shift 2;;
    --fix) FIX="$2"; shift 2;;
    --context) CONTEXT="$2"; shift 2;;
    --importance) IMPORTANCE="$2"; shift 2;;
    --tags) TAGS="$2"; shift 2;;
    *) echo "Unknown: $1"; shift;;
  esac
done

if [ -z "$CATEGORY" ] || [ -z "$WHAT" ] || [ -z "$FIX" ]; then
  echo "Usage: bash log_learning.sh --category <category> --what <description> --fix <solution>"
  exit 1
fi

DATE=$(date +%Y-%m-%d)
ID="learn-$(date +%s)-$(echo "$WHAT" | md5sum | cut -c1-6)"

# Secure temp file
DOC_FILE=$(mktemp /tmp/learn-doc.XXXXXX)
chmod 600 "$DOC_FILE"
cleanup() { rm -f "$DOC_FILE"; }
trap cleanup EXIT

python3 - "$ID" "$CATEGORY" "$WHAT" "$FIX" "$CONTEXT" "$IMPORTANCE" "$TAGS" "$DATE" "$MEILI_HOST" "$MEILI_KEY" "$DOC_FILE" << 'PYEOF'
import json, sys, subprocess

args = {
    "id": sys.argv[1],
    "category": sys.argv[2],
    "what_happened": sys.argv[3],
    "fix": sys.argv[4],
    "context": sys.argv[5] if len(sys.argv) > 5 else "",
    "importance": float(sys.argv[6]) if len(sys.argv) > 6 else 0.7,
    "tags": [t.strip() for t in sys.argv[7].split(",") if t.strip()] if len(sys.argv) > 7 else [],
    "date": sys.argv[8] if len(sys.argv) > 8 else "",
    "source": "manual_log"
}
args["tags"].append("category/" + args["category"])
args["tags"].append("date/" + args["date"])

ms_host = sys.argv[9]
ms_key = sys.argv[10]
doc_file = sys.argv[11]

# Check for duplicates
sr = subprocess.run([
    "curl", "-s", f"{ms_host}/indexes/learnings/search",
    "-H", f"Authorization: Bearer {ms_key}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps({"q": args["what_happened"][:50], "limit": 3})
], capture_output=True, text=True)

try:
    for hit in json.loads(sr.stdout).get("hits", []):
        if hit.get("what_happened", "").lower() == args["what_happened"].lower():
            print(f"Duplicate found, skipping.")
            sys.exit(0)
except:
    pass

with open(doc_file, "w") as f:
    json.dump([args], f)

r = subprocess.run([
    "curl", "-s", "-X", "POST",
    f"{ms_host}/indexes/learnings/documents",
    "-H", f"Authorization: Bearer {ms_key}",
    "-H", "Content-Type: application/json",
    "-d", f"@{doc_file}"
], capture_output=True, text=True)

try:
    status = json.loads(r.stdout).get("status", "?")
except:
    status = "?"
print(f"Logged: [{args['category']}] {args['what_happened'][:60]}... ({status})")
PYEOF
