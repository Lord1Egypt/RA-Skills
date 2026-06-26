#!/usr/bin/env bash
# seasonal-campaign.sh — find when "수능 도시락" peaks. Pipe to jq to sort.
# Use the resulting peak month to schedule next year's campaign.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$here/../scripts/search.sh" \
  --start 2023-09-01 --end 2024-01-31 --time-unit month \
  --group "수능도시락:수능 도시락,수능도시락,도시락 추천" \
| jq -s 'sort_by(-.ratio) | .[0:3]'
