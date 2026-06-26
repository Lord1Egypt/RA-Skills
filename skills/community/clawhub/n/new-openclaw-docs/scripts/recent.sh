#!/bin/bash
# Show recently updated/cached docs

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

DAYS=${1:-7}

echo "📅 Docs cached in the last $DAYS days"
echo ""

if [[ ! -d "$OPENCLAW_DOCS_CACHE_DIR" ]] || [[ -z "$(ls "$OPENCLAW_DOCS_CACHE_DIR"/*.md 2>/dev/null)" ]]; then
  echo "⚠️  No cached docs found."
  exit 0
fi

now=$(date +%s)
count=0

echo "Path                                      Age (hours)  Modified"
echo "--------------------------------------------------------------------"

for file in "$OPENCLAW_DOCS_CACHE_DIR"/*.md; do
  [[ ! -f "$file" ]] && continue
  
  # Calculate age in hours and days
  file_time=$(stat -c %Y "$file")
  age_secs=$((now - file_time))
  age_hours=$((age_secs / 3600))
  age_days=$((age_secs / 86400))
  
  # Check if within DAYS
  if [[ $age_days -le $DAYS ]]; then
    # Extract human-readable path
    doc_path="${file##*/}"
    doc_path="${doc_path%.md}"
    doc_path="${doc_path//_//}"
    
    # Format timestamp
    modified=$(date -d @"$file_time" '+%Y-%m-%d %H:%M')
    
    # Print as table
    printf "%-40s %3dh (%dd)   %s\n" "$doc_path" "$age_hours" "$age_days" "$modified"
    ((count++))
  fi
done

echo ""
if [[ $count -eq 0 ]]; then
  echo "No docs cached in the last $DAYS days"
else
  echo "✓ $count doc(s) found"
fi
