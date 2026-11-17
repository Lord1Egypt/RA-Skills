#!/usr/bin/env bash
# Open a deck in iA Presenter and capture the screen so an agent can inspect the
# rendered thumbnails. Requires macOS and Screen Recording permission for the terminal.
# Usage: preview_deck.sh DECK.iapresenter [OUT.png] [WAIT_SECONDS]
set -euo pipefail
DECK="${1:?usage: preview_deck.sh DECK.iapresenter [OUT.png] [WAIT_SECONDS]}"
OUT="${2:-preview.png}"
WAIT="${3:-6}"
[ -e "$DECK" ] || { echo "error: $DECK not found" >&2; exit 1; }
open -a "iA Presenter" "$DECK"
sleep "$WAIT"
osascript -e 'tell application "iA Presenter" to activate' >/dev/null 2>&1 || true
sleep 1
if screencapture -x "$OUT"; then
  echo "captured $OUT"
  echo "tip: make sure the Thumbnails sidebar is visible (View → Show Thumbnails) – it shows every slide rendered."
else
  echo "screencapture failed – grant Screen Recording to your terminal (System Settings → Privacy & Security) and, in sandboxed agents, run outside the sandbox." >&2
  exit 1
fi
