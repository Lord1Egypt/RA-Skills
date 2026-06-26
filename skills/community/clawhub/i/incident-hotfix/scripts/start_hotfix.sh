#!/usr/bin/env bash
set -euo pipefail

ID=""
BASE="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id) ID="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "Usage: $0 --id INC-1234 [--base main]"
  exit 1
fi

SLUG=$(echo "$ID" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9-')
BRANCH="hotfix/${SLUG}"

mkdir -p "docs/incidents/${ID}/evidence"

cat > "docs/incidents/${ID}/TIMELINE.md" <<EOF
# ${ID} Timeline

- Detected:
- Impact:
- Mitigation started:
- Fixed in commit:
- Verified at:
EOF

cat > "docs/incidents/${ID}/ROLLBACK.md" <<EOF
# ${ID} Rollback Plan

- Trigger conditions:
- Rollback command:
- Data considerations:
- Verification steps:
EOF

cat > "docs/incidents/${ID}/ACTIONS.md" <<EOF
# ${ID} Corrective Actions

Use references/action-template.md from incident-hotfix skill.
EOF

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git fetch --all --prune || true
  git checkout "$BASE"
  git pull --ff-only || true
  git checkout -b "$BRANCH"
fi

echo "Initialized ${ID} on branch ${BRANCH}"