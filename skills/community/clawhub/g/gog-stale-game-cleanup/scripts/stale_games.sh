#!/usr/bin/env bash
set -euo pipefail

# GOG Stale Game Cleanup
# Finds installed GOG games not played in 30+ days, emails a report,
# and adds each game to Apple Reminders "Gaming" list.

STALE_DAYS="${STALE_DAYS:-30}"
GOG_LIBRARY="${GOG_LIBRARY:-}"
EMAIL_TO="${EMAIL_TO:-}"
EMAIL_ACCOUNT="${EMAIL_ACCOUNT:-personal}"
REMINDERS_LIST="${REMINDERS_LIST:-Gaming}"
DRY_RUN="${DRY_RUN:-false}"

if [[ -z "$GOG_LIBRARY" ]]; then
  echo "ERROR: GOG_LIBRARY path not set" >&2; exit 1
fi
if [[ -z "$EMAIL_TO" ]]; then
  echo "ERROR: EMAIL_TO not set" >&2; exit 1
fi

CUTOFF=$(date -d "-${STALE_DAYS} days" +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -v-${STALE_DAYS}d +%Y-%m-%dT%H:%M:%S 2>/dev/null)
if [[ -z "$CUTOFF" ]]; then
  echo "ERROR: Could not compute cutoff date" >&2; exit 1
fi

# Extract stale installed games via python (jq may not be available)
STALE_JSON=$(python3 -c "
import json, sys
from datetime import datetime, timezone

with open('$GOG_LIBRARY') as f:
    lib = json.load(f)

cutoff = datetime.fromisoformat('$CUTOFF').replace(tzinfo=None)
stale = []
for g in lib.get('games', []):
    if not g.get('installed'):
        continue
    lp = g.get('last_played')
    if lp is None:
        stale.append(g)
        continue
    try:
        dt = datetime.fromisoformat(lp).replace(tzinfo=None)
    except Exception:
        stale.append(g)
        continue
    if dt < cutoff:
        stale.append(g)

print(json.dumps(stale))
")

COUNT=$(echo "$STALE_JSON" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

if [[ "$COUNT" -eq 0 ]]; then
  echo "No stale games found. All installed games played within ${STALE_DAYS} days."
  exit 0
fi

echo "Found ${COUNT} stale game(s):"

# Build email body
EMAIL_BODY=$(echo "$STALE_JSON" | python3 -c "
import json, sys
from datetime import datetime

stale = json.load(sys.stdin)
lines = ['GOG Stale Game Report', '=' * 40, '']
lines.append('The following installed games have not been played in ${STALE_DAYS}+ days:')
lines.append('')
for i, g in enumerate(stale, 1):
    lp = g.get('last_played', 'Never')
    name = g.get('name', 'Unknown')
    path = g.get('install_path', 'N/A')
    lines.append(f'{i}. {name}')
    lines.append(f'   Last played: {lp}')
    lines.append(f'   Install path: {path}')
    lines.append('')
lines.append(f'Total: {len(stale)} game(s)')
print('\n'.join(lines))
")

echo "$EMAIL_BODY"
echo ""

# Add to Apple Reminders
if [[ "$DRY_RUN" != "true" ]]; then
  echo "$STALE_JSON" | python3 -c "
import json, sys, subprocess

stale = json.load(sys.stdin)
for g in stale:
    name = g.get('name', 'Unknown')
    title = f'Consider uninstalling: {name}'
    try:
        subprocess.run(['remindctl', 'add', '--title', title, '--list', '$REMINDERS_LIST'], check=True)
        print(f'  ✓ Reminder added: {title}')
    except Exception as e:
        print(f'  ✗ Failed to add reminder for {name}: {e}', file=sys.stderr)
"

  # Send email via himalaya
  echo "$EMAIL_BODY" | himalaya message send --account "$EMAIL_ACCOUNT" --to "$EMAIL_TO" --subject "GOG Stale Game Report — ${COUNT} game(s) to review"
  echo "✓ Email sent to $EMAIL_TO"
else
  echo "[DRY RUN] Would add ${COUNT} reminders and send email."
fi
