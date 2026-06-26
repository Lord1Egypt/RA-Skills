#!/usr/bin/env bash
# List active Aavegotchi DAO proposals on Snapshot

set -euo pipefail

usage() {
  cat <<USAGE
Usage: ./scripts/list-proposals.sh

Lists active proposals in configured Snapshot space and prints
wallet voting power per proposal.
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 0 ]; then
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_tools
load_config

echo "🗳️  AAVEGOTCHI DAO ACTIVE PROPOSALS"
echo "==================================="
echo

QUERY='query($space:String!){ proposals(first: 20, skip: 0, where: {space_in: [$space], state: "active"}, orderBy: "created", orderDirection: desc) { id title end state choices type } }'
VARS="$(jq -n --arg space "$SPACE" '{space:$space}')"
PROPOSALS="$(snapshot_query "$QUERY" "$VARS")"

if snapshot_has_errors "$PROPOSALS"; then
  echo "❌ Snapshot query error"
  echo "$PROPOSALS" | jq '.errors'
  exit 1
fi

COUNT="$(echo "$PROPOSALS" | jq '.data.proposals | length')"
if [ "$COUNT" = "0" ]; then
  echo "📭 No active proposals found"
  echo
  echo "🔗 Check: https://snapshot.org/#/$SPACE"
  exit 0
fi

echo "📊 Found $COUNT active proposal(s)"
echo

echo "$PROPOSALS" | jq -r '.data.proposals[] | @base64' | while read -r p64; do
  proposal="$(printf '%s' "$p64" | base64 -d)"
  ID="$(echo "$proposal" | jq -r '.id')"
  TITLE="$(echo "$proposal" | jq -r '.title')"
  TYPE="$(echo "$proposal" | jq -r '.type')"
  END="$(echo "$proposal" | jq -r '.end')"
  CHOICES="$(echo "$proposal" | jq -r '.choices | length')"

  END_DATE="$(format_utc "$END")"

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📋 $TITLE"
  echo
  echo "   ID: $ID"
  echo "   Type: $TYPE"
  echo "   Choices: $CHOICES"
  echo "   Ends: $END_DATE"
  echo

  VP_QUERY='query($voter:String!, $space:String!, $proposal:String!){ vp(voter: $voter, space: $space, proposal: $proposal) { vp } }'
  VP_VARS="$(jq -n --arg voter "$WALLET" --arg space "$SPACE" --arg proposal "$ID" '{voter:$voter,space:$space,proposal:$proposal}')"
  VP_DATA="$(snapshot_query "$VP_QUERY" "$VP_VARS")"

  if snapshot_has_errors "$VP_DATA"; then
    echo "   ⚠️  Could not fetch VP"
  else
    VP="$(echo "$VP_DATA" | jq -r '.data.vp.vp // 0')"
    if [ "$VP" != "0" ] && [ "$VP" != "null" ]; then
      printf "   💪 Your VP: %.2f\n" "$VP"
    else
      echo "   ⚠️  Your VP: 0 (cannot vote)"
    fi
  fi

  echo "   🔗 https://snapshot.org/#/$SPACE/proposal/$ID"
  echo
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "💡 To vote, use: ./scripts/vote.sh <proposal-id> <choice>"
