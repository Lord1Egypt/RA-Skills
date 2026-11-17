#!/usr/bin/env bash
# Compatibility wrapper: the CLI owns durable keys, pacing and retry recovery.
# Usage: oag-submit-batch.sh BATCH_FILE.json [IDS_OUT.txt] [JOURNAL.json]
# Requires an updated oag-client installation and jq. Keep the journal on restart.
set -euo pipefail

batch_file="${1:?usage: oag-submit-batch.sh BATCH_FILE.json [IDS_OUT.txt] [JOURNAL.json]}"
ids_out="${2:-submitted-ids.txt}"
journal="${3:-${ids_out}.journal.json}"
command -v oag >/dev/null || { echo "Install or upgrade oag-client first; see references/cli.md." >&2; exit 2; }
if [ -s "$ids_out" ] && [ ! -f "$journal" ]; then
  echo "Existing IDs have no journal. Reconcile the previous batch before submitting again." >&2
  exit 2
fi
if [ "$ids_out" -ef "$batch_file" ] || [ "$ids_out" = "$journal" ] || [ "$ids_out" -ef "$journal" ]; then
  echo "The IDs output must differ from the batch and journal paths." >&2
  exit 2
fi
umask 077
result="$(mktemp)"
ids_tmp="$(mktemp "${ids_out}.XXXXXX")"
trap 'rm -f "$result" "$ids_tmp"' EXIT
code=0
oag submit "$batch_file" --journal "$journal" --output json \
  --timeout "${OAG_SUBMIT_TIMEOUT:-300}" >"$result" || code=$?
# Configuration errors and cancellation may produce no JSON. Preserve old IDs.
if jq -e '.version == 1 and (.records | type == "array")' "$result" >/dev/null 2>&1; then
  if [ "$ids_out" -ef "$journal" ]; then
    echo "The IDs output must differ from the journal path." >&2
    exit 2
  fi
  jq -r '.records[] | select(.state == "created") | .id' "$result" >"$ids_tmp"
  mv "$ids_tmp" "$ids_out"
  cat "$result"
  echo "Confirmed IDs written to $ids_out. Resume with the same journal: $journal" >&2
elif [ "$code" -eq 0 ]; then
  echo "CLI returned no valid result; preserving existing IDs." >&2
  code=2
fi
exit "$code"
