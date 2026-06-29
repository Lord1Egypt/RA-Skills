#!/usr/bin/env bash
# grill-scan.sh - mechanical floor for the grill pass.
# Flags AI-slop vocabulary, empty hedges, em dashes, and the rhythmic "That is X." tic.
# This is a FLOOR, not the check: voice, fact-sourcing, and right-number checks are
# judgment calls a grep cannot make. Read the prose by eye after running this.
#
# Usage: grill-scan.sh <file> [<file> ...]

set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: grill-scan.sh <file> [<file> ...]" >&2
  exit 2
fi

# AI-tell vocabulary and filler. Word-boundary, case-insensitive.
SLOP='\b(delve|delves|delving|leverage|leverages|leveraging|robust|seamless|seamlessly|journey|realm|tapestry|testament|elevate|elevates|underscore|underscores|boasts|bustling|treasure trove|game-changer|game changer|paradigm|synergy|cutting-edge|state-of-the-art|unlock|unlocks|unleash|harness the power)\b'

# Empty hedges and throat-clearing.
HEDGE='(in today'\''s world|it'\''s worth noting|its worth noting|needless to say|at the end of the day|when it comes to|navigate the complexities|dive in|dive into|let'\''s unpack|in conclusion|that being said|it is important to note|first and foremost)'

# Unsourced authority claims a skeptic will demand a citation for.
AUTHORITY='(studies show|research shows|it'\''s well known|it is well known|everyone knows|experts agree|as we all know)'

status=0

for f in "$@"; do
  [ -f "$f" ] || { echo "skip (not a file): $f" >&2; continue; }
  hits=0

  scan() { # label, pattern
    local label="$1" pat="$2" out
    out=$(grep -niE "$pat" "$f" || true)
    if [ -n "$out" ]; then
      echo "### $label"
      echo "$out"
      echo
      hits=$((hits + $(printf '%s\n' "$out" | grep -c . )))
    fi
  }

  echo "==================== $f ===================="
  scan "AI-slop vocabulary" "$SLOP"
  scan "Empty hedges / filler" "$HEDGE"
  scan "Unsourced authority claims" "$AUTHORITY"

  # Em dashes (house style forbids them).
  out=$(grep -nF '—' "$f" || true)
  if [ -n "$out" ]; then echo "### Em dashes (—)"; echo "$out"; echo; hits=$((hits + $(printf '%s\n' "$out" | grep -c .))); fi

  # The rhythmic "That is X." / "That's X." motivational tic at sentence start.
  out=$(grep -nE '(^|[.!?]"?[[:space:]])(That is|That'\''s|This is) [A-Za-z].{0,40}\.' "$f" || true)
  if [ -n "$out" ]; then echo "### Possible rhythmic tic (That is X. / This is X.)"; echo "$out"; echo; hits=$((hits + $(printf '%s\n' "$out" | grep -c .))); fi

  # Unresolved fact markers still in the draft.
  out=$(grep -nE '\[CONFIRM' "$f" || true)
  if [ -n "$out" ]; then echo "### Unresolved [CONFIRM] markers (resolve or cut before publish)"; echo "$out"; echo; hits=$((hits + $(printf '%s\n' "$out" | grep -c .))); fi

  if [ "$hits" -eq 0 ]; then
    echo "clean: no mechanical flags. Now read by eye for voice, sourcing, and right-number checks."
  else
    echo ">> $hits mechanical flag(s). Each is a candidate, not a verdict; judge in context."
    status=1
  fi
  echo
done

exit $status
