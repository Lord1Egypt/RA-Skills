#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--dry-run] [gotchi-id]

Send interact([gotchi-id]) through Bankr on Base.
If gotchi-id is omitted, uses the first configured gotchi ID.
USAGE
}

DRY_RUN=0
POSITIONAL=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [ "$#" -gt 0 ]; do
        POSITIONAL+=("$1")
        shift
      done
      break
      ;;
    -*)
      echo "ERROR: Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      POSITIONAL+=("$1")
      ;;
  esac
  shift
done

if [ "${#POSITIONAL[@]}" -gt 1 ]; then
  echo "ERROR: Too many arguments" >&2
  usage >&2
  exit 1
fi

require_tx_tools
load_config

GOTCHI_ID="${POSITIONAL[0]:-$(default_gotchi_id)}"
if ! is_uint "$GOTCHI_ID"; then
  err "Invalid gotchi ID: $GOTCHI_ID"
fi

CALLDATA="$(encode_interact_calldata "$GOTCHI_ID")"
DESCRIPTION="Pet Aavegotchi #$GOTCHI_ID"

if [ "$DRY_RUN" -eq 1 ]; then
  jq -n \
    --arg to "$CONTRACT_ADDRESS" \
    --arg chainId "$CHAIN_ID" \
    --arg data "$CALLDATA" \
    --arg gotchi "$GOTCHI_ID" \
    '{mode:"dry-run",action:"pet-single",gotchiId:$gotchi,transaction:{to:$to,chainId:($chainId|tonumber),value:"0",data:$data}}'
  exit 0
fi

echo "Petting gotchi #$GOTCHI_ID via Bankr..."
RESPONSE="$(submit_bankr_tx "$CONTRACT_ADDRESS" "$CALLDATA" "$DESCRIPTION")"

if bankr_is_success "$RESPONSE"; then
  TX_HASH="$(bankr_tx_hash "$RESPONSE")"
  echo "OK: gotchi #$GOTCHI_ID petted"
  if [ -n "$TX_HASH" ]; then
    echo "tx=$TX_HASH"
    echo "url=https://basescan.org/tx/$TX_HASH"
  fi
  exit 0
fi

echo "ERROR: $(bankr_error "$RESPONSE")" >&2
printf '%s\n' "$RESPONSE" | jq '.' >&2 || true
exit 1
