#!/usr/bin/env bash
# Gather git commits between two refs and output as JSON
# Usage: gather_commits.sh <from_ref> <to_ref>
# Output: JSON array of commit objects

set -euo pipefail

FROM_REF="${1:?Usage: gather_commits.sh <from_ref> <to_ref>}"
TO_REF="${2:-HEAD}"

# Verify we're in a git repo
git rev-parse --git-dir >/dev/null 2>&1 || {
  echo '{"error": "Not a git repository"}'
  exit 1
}

# Verify refs exist
git rev-parse "$FROM_REF" >/dev/null 2>&1 || {
  echo "{\"error\": \"Ref not found: $FROM_REF\"}"
  exit 1
}
git rev-parse "$TO_REF" >/dev/null 2>&1 || {
  echo "{\"error\": \"Ref not found: $TO_REF\"}"
  exit 1
}

# Separator that won't appear in commit messages
SEP="---COMMIT_SEP---"
FIELD_SEP="---FIELD_SEP---"

# Get commit count
COMMIT_COUNT=$(git rev-list "$FROM_REF".."$TO_REF" | wc -l | tr -d ' ')

# Get unique author count
AUTHOR_COUNT=$(git log "$FROM_REF".."$TO_REF" --format="%ae" | sort -u | wc -l | tr -d ' ')

# Get commits as structured data and convert to JSON with Python
git log "$FROM_REF".."$TO_REF" \
  --format="${SEP}%H${FIELD_SEP}%an${FIELD_SEP}%ae${FIELD_SEP}%aI${FIELD_SEP}%s${FIELD_SEP}%b" \
  | python3 -c "
import sys, json

content = sys.stdin.read()
SEP = '---COMMIT_SEP---'
FIELD_SEP = '---FIELD_SEP---'

commits = []
for block in content.split(SEP):
    block = block.strip()
    if not block:
        continue
    parts = block.split(FIELD_SEP)
    if len(parts) < 5:
        continue
    commits.append({
        'hash': parts[0].strip(),
        'author': parts[1].strip(),
        'email': parts[2].strip(),
        'date': parts[3].strip(),
        'subject': parts[4].strip(),
        'body': parts[5].strip() if len(parts) > 5 else ''
    })

result = {
    'from_ref': '$FROM_REF',
    'to_ref': '$TO_REF',
    'commit_count': $COMMIT_COUNT,
    'author_count': $AUTHOR_COUNT,
    'commits': commits
}

print(json.dumps(result, indent=2))
"
