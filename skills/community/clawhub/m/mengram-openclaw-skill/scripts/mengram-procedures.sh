#!/usr/bin/env bash
# SECURITY MANIFEST:
# Environment variables accessed: MENGRAM_API_KEY (only)
# External endpoints called: https://mengram.io/v1/procedures, https://mengram.io/v1/procedures/*/history (only)
# Local files read: none
# Local files written: none
set -euo pipefail

MENGRAM_BASE_URL="${MENGRAM_BASE_URL:-https://mengram.io}"
API_KEY="${MENGRAM_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: MENGRAM_API_KEY not set. Get your free key at https://mengram.io"
  exit 1
fi

PROC_ID="${1:-}"

if [ -n "$PROC_ID" ]; then
  # Show specific procedure with version history
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X GET "${MENGRAM_BASE_URL}/v1/procedures/${PROC_ID}/history" \
    -H "Authorization: Bearer ${API_KEY}")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" -ne 200 ]; then
    echo "ERROR: Mengram API returned HTTP ${HTTP_CODE}"
    echo "$BODY"
    exit 1
  fi

  python3 -c "
import json, sys

try:
    data = json.loads(sys.argv[1])
except json.JSONDecodeError:
    print('No data.')
    sys.exit(0)

versions = data.get('versions', [])
evolution = data.get('evolution_log', [])

for v in versions:
    current = ' (CURRENT)' if v.get('is_current') else ''
    print(f'=== v{v.get(\"version\", 1)}{current} ===')
    print(f'Name: {v.get(\"name\", \"\")}')
    print(f'Trigger: {v.get(\"trigger_condition\", \"\")}')
    steps = v.get('steps', [])
    for s in steps:
        print(f'  {s.get(\"step\", \"\")}. {s.get(\"action\", \"\")} — {s.get(\"detail\", \"\")}')
    print(f'Success: {v.get(\"success_count\", 0)}, Fail: {v.get(\"fail_count\", 0)}')
    print()

if evolution:
    print('=== EVOLUTION LOG ===')
    for ev in evolution:
        change = ev.get('change_type', '')
        vb = ev.get('version_before', '?')
        va = ev.get('version_after', '?')
        diff = ev.get('diff', {})
        reason = diff.get('reason', '')
        added = diff.get('added', [])
        print(f'v{vb} -> v{va}: {change}')
        if added:
            for a in added:
                print(f'  + {a}')
        if reason:
            print(f'  Reason: {reason}')
" "$BODY"
else
  # List all procedures
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X GET "${MENGRAM_BASE_URL}/v1/procedures" \
    -H "Authorization: Bearer ${API_KEY}")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" -ne 200 ]; then
    echo "ERROR: Mengram API returned HTTP ${HTTP_CODE}"
    echo "$BODY"
    exit 1
  fi

  python3 -c "
import json, sys

try:
    data = json.loads(sys.argv[1])
except json.JSONDecodeError:
    print('No procedures found.')
    sys.exit(0)

procs = data.get('procedures', [])
if not procs:
    print('No procedures yet. Procedures are auto-created from conversations.')
    sys.exit(0)

print(f'PROCEDURES ({len(procs)}):')
print()
for p in procs:
    name = p.get('name', '')
    version = p.get('version', 1)
    steps = p.get('steps', [])
    success = p.get('success_count', 0)
    fail = p.get('fail_count', 0)
    pid = p.get('id', '')
    steps_str = ' -> '.join(s.get('action', '') for s in steps[:10])
    v_tag = f' v{version}' if version > 1 else ''
    print(f'- {name}{v_tag} [{pid[:8]}]')
    print(f'  Steps: {steps_str}')
    print(f'  Success: {success}, Fail: {fail}')
    print()
" "$BODY"
fi
