#!/usr/bin/env bash
set -euo pipefail

# Example: Find a lead by email, tag them, set score field, and trigger a flow.
# Requires: MANYCHAT_API_KEY set in environment.

CLI="/Users/danielfoch/manychat-cli/manychat_cli.py"
EMAIL="${1:-lead@example.com}"

FIND_JSON="$($CLI find-system --field-name email --field-value "$EMAIL")"
SUB_ID="$(echo "$FIND_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); data=d.get("result",{}).get("data",[]); print(data[0]["id"] if data else "")')"

if [[ -z "$SUB_ID" ]]; then
  echo "No subscriber found for $EMAIL"
  exit 0
fi

$CLI tag-add --subscriber-id "$SUB_ID" --tag-name "AI Qualified Lead" >/dev/null
$CLI field-set --subscriber-id "$SUB_ID" --field-name "lead_score" --value 85 >/dev/null
$CLI flow-send --subscriber-id "$SUB_ID" --flow-ns "qualified_lead_followup" --pretty
