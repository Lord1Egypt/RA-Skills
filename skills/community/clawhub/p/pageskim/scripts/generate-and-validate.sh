#!/usr/bin/env bash
# Generate PageSkim siblings for a built site and validate every pair.
# Usage: generate-and-validate.sh <output-dir> [base-url]
set -euo pipefail

OUT_DIR="${1:?usage: generate-and-validate.sh <output-dir> [base-url]}"
BASE_URL="${2:-}"

ARGS=(generate "$OUT_DIR" --json --split --site-index)
if [[ -n "$BASE_URL" ]]; then
  ARGS+=(--base-url "$BASE_URL")
fi

npx --yes pageskim "${ARGS[@]}"

STATUS=0
while IFS= read -r -d '' page; do
  sibling="${page%.*}.llm.md"
  if [[ -f "$sibling" ]]; then
    if ! npx --yes pageskim validate "$page" "$sibling"; then
      echo "INVALID: $page" >&2
      STATUS=1
    fi
  fi
done < <(find "$OUT_DIR" -name '*.html' ! -name '*.llm.*' -print0)

exit "$STATUS"
