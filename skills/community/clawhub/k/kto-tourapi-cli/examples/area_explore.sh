#!/usr/bin/env bash
# Print the canonical KTO areaCode list (광역시도) and, for each, fetch its
# sigungu list. Useful as a one-shot reference dump before drilling deeper.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$here/../scripts"

bash "$S/area-code.sh" \
  | jq -c '{level:"area", code:.code, name:.name}'

bash "$S/area-code.sh" \
  | jq -r '.code' \
  | while read -r ac; do
      bash "$S/area-code.sh" --area-code "$ac" \
        | jq -c --arg parent "$ac" '{level:"sigungu", parent:$parent, code:.code, name:.name}'
    done
