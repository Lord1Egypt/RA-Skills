#!/bin/bash
# Distill learnings into LEARNINGS.md
# Usage: bash distill_learnings.sh [--apply] [--dry-run]
#
# Default is dry-run. Use --apply to actually write.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

DRY_RUN=true
for arg in "$@"; do
  case $arg in
    --apply) DRY_RUN=false ;;
    --dry-run) DRY_RUN=true ;;
  esac
done

echo "=== Distilling Learnings ==="
if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Use --apply to write to LEARNINGS.md"
fi

# Secure tmp file for query
QUERY_FILE=$(mktemp /tmp/learn-distill.XXXXXX)
chmod 600 "$QUERY_FILE"
cleanup() { rm -f "$QUERY_FILE"; }
trap cleanup EXIT

python3 - "$SKILL_DIR" "$MEILI_HOST" "$MEILI_KEY" "$DRY_RUN" "$QUERY_FILE" << 'PYEOF'
import json, subprocess, sys, os
from datetime import datetime

skill_dir = sys.argv[1]
ms_host = sys.argv[2]
ms_key = sys.argv[3]
dry_run = sys.argv[4] == "true"
query_file = sys.argv[5]

learnings_file = f"{skill_dir}/LEARNINGS.md"

# Fetch all learnings
payload = {"q": "", "limit": 1000, "attributesToRetrieve": ["id", "what_happened", "fix", "context", "category", "importance", "date", "tags"]}
with open(query_file, "w") as f:
    json.dump(payload, f)

result = subprocess.run([
    "curl", "-s", f"{ms_host}/indexes/learnings/search",
    "-H", f"Authorization: Bearer {ms_key}",
    "-H", "Content-Type: application/json",
    "-d", f"@{query_file}"
], capture_output=True, text=True)

try:
    data = json.loads(result.stdout)
    hits = data.get("hits", [])
except:
    hits = []

print(f"Total learnings: {len(hits)}")

if not hits:
    print("No learnings to distill.")
    sys.exit(0)

# Group by category
by_cat = {}
for h in hits:
    cat = h.get("category", "unknown")
    by_cat.setdefault(cat, []).append(h)

# Stats
print("\nBy category:")
for cat, items in sorted(by_cat.items()):
    print(f"  {cat}: {len(items)}")

high = [h for h in hits if h.get("importance", 0) >= 0.7]
print(f"\nHigh importance (>=0.7): {len(high)}")

if dry_run:
    print(f"\n[DRY RUN] Would write {len(high)} learnings to LEARNINGS.md")
    print("Run with --apply to write.")
    sys.exit(0)

# Generate LEARNINGS.md
lines = ["# Learnings\n"]
lines.append(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
lines.append(f"Total entries: {len(hits)}\n\n")

lines.append("## By Category\n")
for cat, items in sorted(by_cat.items()):
    lines.append(f"### {cat.replace('_', ' ').title()}\n")
    for item in sorted(items, key=lambda x: x.get("importance", 0), reverse=True):
        lines.append(f"- **{item.get('what_happened', '')}**")
        if item.get("fix"):
            lines.append(f"  - Fix: {item['fix']}")
        if item.get("context"):
            lines.append(f"  - Context: {item['context']}")
        lines.append(f"  - Importance: {item.get('importance', '?')} | Date: {item.get('date', '?')}\n")

with open(learnings_file, "w") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(high)} learnings to LEARNINGS.md")
PYEOF

echo "=== Done ==="
