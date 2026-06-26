#!/usr/bin/env bash
# Vote on Aavegotchi Snapshot proposals via Bankr signature

set -euo pipefail

usage() {
  cat <<USAGE
Usage: $0 [--dry-run] <proposal-id> <choice>

Examples:
  Single-choice: $0 0xabc123... 2
  Weighted:      $0 0xabc123... '{"2": 2238}'
  Dry run:       $0 --dry-run 0xabc123... 2
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

DRY_RUN=0
POSITIONAL=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [ "${#POSITIONAL[@]}" -lt 2 ]; then
  usage
  exit 1
fi

PROPOSAL_ID="$(normalize_proposal_id "${POSITIONAL[0]}")"
CHOICE_RAW="${POSITIONAL[1]}"

require_tools
load_config
API_KEY="$(resolve_bankr_api_key)"

TMP_TYPED="$(mktemp /tmp/vote-typed-XXXXXX.json)"
TMP_PAYLOAD="$(mktemp /tmp/vote-payload-XXXXXX.json)"
cleanup() {
  rm -f "$TMP_TYPED" "$TMP_PAYLOAD"
}
trap cleanup EXIT

echo "🗳️  AAVEGOTCHI DAO VOTING"
echo "========================"
echo
printf "👤 Wallet: %s\n" "$WALLET"
printf "📋 Proposal: %s\n" "$PROPOSAL_ID"
printf "✅ Choice: %s\n" "$CHOICE_RAW"
echo

echo "🔍 Fetching proposal details..."
P_QUERY='query($id:String!){ proposal(id: $id) { id title type choices state } }'
P_VARS="$(jq -n --arg id "$PROPOSAL_ID" '{id:$id}')"
PROPOSAL_DATA="$(snapshot_query "$P_QUERY" "$P_VARS")"

if snapshot_has_errors "$PROPOSAL_DATA"; then
  echo "❌ Snapshot proposal query error"
  echo "$PROPOSAL_DATA" | jq '.errors'
  exit 1
fi

if [ "$(echo "$PROPOSAL_DATA" | jq -r '.data.proposal.id // empty')" = "" ]; then
  echo "❌ Proposal not found: $PROPOSAL_ID"
  exit 1
fi

TITLE="$(echo "$PROPOSAL_DATA" | jq -r '.data.proposal.title')"
TYPE="$(echo "$PROPOSAL_DATA" | jq -r '.data.proposal.type')"
STATE="$(echo "$PROPOSAL_DATA" | jq -r '.data.proposal.state')"
CHOICE_COUNT="$(echo "$PROPOSAL_DATA" | jq -r '.data.proposal.choices | length')"

echo "📝 Title: $TITLE"
echo "🎯 Type: $TYPE"
echo "⚡ State: $STATE"
echo

echo "📊 Available choices:"
echo "$PROPOSAL_DATA" | jq -r '.data.proposal.choices[]' | nl

if [ "$STATE" != "active" ]; then
  echo
  echo "⚠️  Proposal is not active (state: $STATE); sequencer may reject this vote."
fi

echo
echo "💪 Checking voting power..."
VP_QUERY='query($voter:String!, $space:String!, $proposal:String!){ vp(voter: $voter, space: $space, proposal: $proposal) { vp vp_by_strategy } }'
VP_VARS="$(jq -n --arg voter "$WALLET" --arg space "$SPACE" --arg proposal "$PROPOSAL_ID" '{voter:$voter,space:$space,proposal:$proposal}')"
VP_DATA="$(snapshot_query "$VP_QUERY" "$VP_VARS")"

if snapshot_has_errors "$VP_DATA"; then
  echo "❌ Snapshot VP query error"
  echo "$VP_DATA" | jq '.errors'
  exit 1
fi

VP="$(echo "$VP_DATA" | jq -r '.data.vp.vp // 0')"
VP_BY_STRATEGY="$(echo "$VP_DATA" | jq -c '.data.vp.vp_by_strategy // []')"
echo "   Total VP: $VP"
echo "   Breakdown: $VP_BY_STRATEGY"

if [ "$VP" = "0" ] || [ "$VP" = "null" ]; then
  echo "❌ You have 0 voting power on this proposal"
  exit 1
fi

CHOICE_TYPE="uint32"
CHOICE_VALUE="$CHOICE_RAW"

if [ "$TYPE" = "weighted" ]; then
  CHOICE_TYPE="string"

  if [[ "$CHOICE_RAW" =~ ^\{.*\}$ ]]; then
    echo "$CHOICE_RAW" | jq -e --argjson max "$CHOICE_COUNT" '
      type == "object" and
      (keys | length > 0) and
      all(keys[]; test("^[0-9]+$") and ((tonumber >= 1) and (tonumber <= $max))) and
      all(.[]; (type == "number") and (. >= 0))
    ' >/dev/null 2>&1 || err "Invalid weighted JSON choice (keys must be 1..$CHOICE_COUNT, values numeric >= 0)"
    CHOICE_VALUE="$(echo "$CHOICE_RAW" | jq -c '.')"
  elif [[ "$CHOICE_RAW" =~ ^[0-9]+$ ]]; then
    [ "$CHOICE_RAW" -ge 1 ] && [ "$CHOICE_RAW" -le "$CHOICE_COUNT" ] || err "Choice out of range (1..$CHOICE_COUNT)"
    VP_FLOOR="$(printf '%.0f' "$VP")"
    CHOICE_VALUE="$(jq -n --arg key "$CHOICE_RAW" --argjson vp "$VP_FLOOR" '{($key):$vp}' | jq -c '.')"
    echo "💡 Converted weighted choice: $CHOICE_VALUE"
  else
    err "Weighted voting requires numeric choice or JSON object"
  fi
else
  [[ "$CHOICE_RAW" =~ ^[0-9]+$ ]] || err "Single-choice voting requires numeric choice"
  [ "$CHOICE_RAW" -ge 1 ] && [ "$CHOICE_RAW" -le "$CHOICE_COUNT" ] || err "Choice out of range (1..$CHOICE_COUNT)"
  CHOICE_VALUE="$CHOICE_RAW"
fi

TIMESTAMP="$(date +%s)"

if [ "$CHOICE_TYPE" = "string" ]; then
  jq -n \
    --arg from "$WALLET" \
    --arg space "$SPACE" \
    --arg proposal "$PROPOSAL_ID" \
    --arg choice "$CHOICE_VALUE" \
    --arg app "openclaw" \
    --arg metadata "{}" \
    --argjson timestamp "$TIMESTAMP" \
    '{
      types: {
        Vote: [
          {name:"from",type:"address"},
          {name:"space",type:"string"},
          {name:"timestamp",type:"uint64"},
          {name:"proposal",type:"bytes32"},
          {name:"choice",type:"string"},
          {name:"reason",type:"string"},
          {name:"app",type:"string"},
          {name:"metadata",type:"string"}
        ]
      },
      domain: {name:"snapshot",version:"0.1.4"},
      primaryType:"Vote",
      message: {from:$from,space:$space,timestamp:$timestamp,proposal:$proposal,choice:$choice,reason:"",app:$app,metadata:$metadata}
    }' > "$TMP_TYPED"
else
  jq -n \
    --arg from "$WALLET" \
    --arg space "$SPACE" \
    --arg proposal "$PROPOSAL_ID" \
    --arg app "openclaw" \
    --arg metadata "{}" \
    --argjson timestamp "$TIMESTAMP" \
    --argjson choice "$CHOICE_VALUE" \
    '{
      types: {
        Vote: [
          {name:"from",type:"address"},
          {name:"space",type:"string"},
          {name:"timestamp",type:"uint64"},
          {name:"proposal",type:"bytes32"},
          {name:"choice",type:"uint32"},
          {name:"reason",type:"string"},
          {name:"app",type:"string"},
          {name:"metadata",type:"string"}
        ]
      },
      domain: {name:"snapshot",version:"0.1.4"},
      primaryType:"Vote",
      message: {from:$from,space:$space,timestamp:$timestamp,proposal:$proposal,choice:$choice,reason:"",app:$app,metadata:$metadata}
    }' > "$TMP_TYPED"
fi

echo
echo "📝 Typed data prepared"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "--- DRY RUN ---"
  cat "$TMP_TYPED" | jq '.'
  exit 0
fi

echo "📝 Signing vote with Bankr..."
SIGN_PAYLOAD="$(jq -n --slurpfile typed "$TMP_TYPED" '{signatureType:"eth_signTypedData_v4",typedData:$typed[0]}')"

SIGN_RESPONSE="$(curl -sS -X POST "https://api.bankr.bot/agent/sign" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$SIGN_PAYLOAD")"

SIGNATURE="$(echo "$SIGN_RESPONSE" | jq -r '.signature // empty')"

if [ -z "$SIGNATURE" ]; then
  echo "❌ Failed to get signature from Bankr"
  echo "$SIGN_RESPONSE" | jq '.'
  exit 1
fi

echo "✅ Signature obtained"

echo "📤 Submitting vote to Snapshot..."

jq -n \
  --arg address "$WALLET" \
  --arg sig "$SIGNATURE" \
  --slurpfile data "$TMP_TYPED" \
  '{address:$address,sig:$sig,data:$data[0]}' > "$TMP_PAYLOAD"

VOTE_RESPONSE="$(curl -sS -X POST "$SEQUENCER" -H "Content-Type: application/json" -d @"$TMP_PAYLOAD")"

echo "📬 Response:"
echo "$VOTE_RESPONSE" | jq '.'

if echo "$VOTE_RESPONSE" | jq -e '.id' >/dev/null 2>&1; then
  VOTE_ID="$(echo "$VOTE_RESPONSE" | jq -r '.id')"
  IPFS="$(echo "$VOTE_RESPONSE" | jq -r '.ipfs // empty')"
  echo
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ VOTE SUCCESSFUL"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📋 Vote ID: $VOTE_ID"
  if [ -n "$IPFS" ]; then
    echo "📦 IPFS: $IPFS"
  fi
  echo "🔗 View: https://snapshot.org/#/$SPACE/proposal/$PROPOSAL_ID"
else
  ERROR="$(echo "$VOTE_RESPONSE" | jq -r '.error_description // .error // "Unknown error"')"
  echo "❌ Vote failed: $ERROR"
  exit 1
fi
