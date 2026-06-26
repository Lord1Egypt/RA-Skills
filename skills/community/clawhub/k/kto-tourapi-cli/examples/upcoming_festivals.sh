#!/usr/bin/env bash
# Emit a tab-separated calendar of festivals starting in the next 30 days,
# nationwide. Pipe into a sheet or a calendar generator.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$here/../scripts"

START=$(date -u +%Y%m%d)
# macOS BSD date vs GNU date — try both shapes for "+30 days".
END=$(date -u -v+30d +%Y%m%d 2>/dev/null || date -u -d "+30 days" +%Y%m%d)

bash "$S/festival.sh" --start "$START" --end "$END" --num 100 \
  | jq -r '[.eventstartdate, .eventenddate, .title, .addr1, .tel] | @tsv'
