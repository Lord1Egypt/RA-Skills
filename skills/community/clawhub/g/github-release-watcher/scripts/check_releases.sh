#!/bin/bash
# check_releases.sh — Check GitHub repos for new releases
# Usage: check_releases.sh [config_file]
# Config: one repo per line (owner/repo), # for comments

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG="${1:-$SCRIPT_DIR/repos.txt}"
STATE_FILE="${STATE_FILE:-$SCRIPT_DIR/.last_seen.json}"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found: $CONFIG"
  echo "Create repos.txt with one owner/repo per line"
  exit 1
fi

# Initialize state file if missing
[ -f "$STATE_FILE" ] || echo '{}' > "$STATE_FILE"

NEW_RELEASES=()

while IFS= read -r repo || [ -n "$repo" ]; do
  # Skip comments and blank lines
  [[ "$repo" =~ ^#|^$ ]] && continue
  repo=$(echo "$repo" | tr -d '[:space:]')
  
  # Get latest release
  latest=$(gh api "repos/$repo/releases/latest" --jq '.tag_name + "|" + .name + "|" + .published_at + "|" + (.body | split("\n") | first)' 2>/dev/null) || continue
  
  tag=$(echo "$latest" | cut -d'|' -f1)
  name=$(echo "$latest" | cut -d'|' -f2)
  date=$(echo "$latest" | cut -d'|' -f3)
  summary=$(echo "$latest" | cut -d'|' -f4-)
  
  # Check if we've seen this tag
  last_seen=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('$repo',''))" 2>/dev/null)
  
  if [ "$tag" != "$last_seen" ]; then
    NEW_RELEASES+=("🆕 **$repo** → $tag ($name)\n   📅 $date\n   $summary")
    # Update state
    python3 -c "
import json
with open('$STATE_FILE','r') as f: d=json.load(f)
d['$repo']='$tag'
with open('$STATE_FILE','w') as f: json.dump(d,f,indent=2)
"
  fi
done < "$CONFIG"

if [ ${#NEW_RELEASES[@]} -eq 0 ]; then
  echo "✅ No new releases detected."
else
  echo "🔔 New releases found:"
  echo ""
  for r in "${NEW_RELEASES[@]}"; do
    echo -e "$r"
    echo ""
  done
fi
