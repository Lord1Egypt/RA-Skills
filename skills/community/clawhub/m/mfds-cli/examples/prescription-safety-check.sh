#!/usr/bin/env bash
# Given a list of drug names (one per line on stdin or as args), flag DUR
# interaction warnings, pregnancy contraindications, and elderly cautions.
#
# Usage:
#   echo -e "와파린\n아스피린" | examples/prescription-safety-check.sh
#   examples/prescription-safety-check.sh "와파린" "아스피린"
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI="$ROOT/bin/mfds-cli"

drugs=()
if [[ "$#" -gt 0 ]]; then
  drugs=("$@")
else
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    drugs+=("$line")
  done
fi

for drug in "${drugs[@]}"; do
  for kind in interaction pregnancy elderly; do
    out="$($CLI dur --type "$kind" --name "$drug" --rows 5 --format jsonl 2>/dev/null || true)"
    if [[ -n "$out" ]]; then
      printf '%s\n' "$out" | while IFS= read -r line; do
        echo "[$kind] $drug → $line"
      done
    fi
  done
done
