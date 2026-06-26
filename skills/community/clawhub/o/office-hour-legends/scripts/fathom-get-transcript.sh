#!/usr/bin/env bash
# Fetch a single Fathom meeting with full transcript by recording ID.
# Usage: fathom-get-transcript.sh <recording_id>
# Requires: FATHOM_API_KEY environment variable
#
# The Fathom API doesn't have a single-meeting endpoint, so we fetch with
# include_transcript=true and filter client-side by recording_id.

set -euo pipefail

RECORDING_ID="${1:?Usage: fathom-get-transcript.sh <recording_id>}"
API_KEY="${FATHOM_API_KEY:?Missing FATHOM_API_KEY environment variable}"

# Fetch recent meetings with transcripts and filter for the requested one
curl -sS "https://api.fathom.ai/external/v1/meetings?limit=100&include_summary=true&include_transcript=true" \
  -H "X-Api-Key: ${API_KEY}" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
target = int('${RECORDING_ID}')
for item in data.get('items', []):
    if item.get('recording_id') == target:
        print(json.dumps(item, indent=2))
        sys.exit(0)
print(json.dumps({'error': 'Meeting not found', 'recording_id': target}))
sys.exit(1)
"
