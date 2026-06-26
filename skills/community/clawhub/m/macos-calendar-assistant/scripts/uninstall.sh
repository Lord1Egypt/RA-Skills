#!/bin/zsh
set -euo pipefail

TMPCRON=$(mktemp /tmp/mca_cron_remove_XXXXXX)
trap 'rm -f "$TMPCRON"' EXIT

( crontab -l 2>/dev/null || true ) | sed '/calendar_clean_notify.sh/d' > "$TMPCRON"
crontab "$TMPCRON"

echo "Removed calendar_clean_notify.sh cron job."
