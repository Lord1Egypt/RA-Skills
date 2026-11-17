#!/usr/bin/env bash
# refresh-snapshot.sh — regenerate models-snapshot.json from the live API.
#
# models-snapshot.json is the offline fallback ofox-image.sh checks --model
# against when GET /v1/models can't be reached. It goes stale as Ofox adds
# models, so refresh it whenever you touch this skill.
#
# Needs no API key (the models endpoint is public). Run:
#   bash references/refresh-snapshot.sh
#
# Regenerating this file is a BEHAVIOUR change, not a data update: it moves
# what the script accepts offline and what it quotes offline. Diff the result
# against the previous copy and say in the changelog what moved — ids,
# supported_endpoints, and especially pricing.output_image, naming the
# direction. The 2026-09-15 refresh is the worked example: 11 of 16 models
# gained /v1/images/edits (without which `edit` refuses them offline), two
# models appeared, the qwen ids moved from bailian/* to qwen/* (old ids kept
# as aliases), and microsoft/mai-image-2.5-flash's output_image dropped
# 0.000026 -> 0.0000195, i.e. the old copy over-quoted it offline by 33%.

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_BASE="${OFOX_API_BASE_URL:-https://api.ofox.ai/v1}"
OUT="$SCRIPT_DIR/models-snapshot.json"

for bin in curl jq; do
  command -v "$bin" >/dev/null || { echo "ERROR: $bin is required." >&2; exit 2; }
done

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

curl -fsS --max-time 20 "$API_BASE/models" -o "$tmp"
jq -e '(.data | length) > 0' "$tmp" >/dev/null

# Keep an entry if it serves EITHER image endpoint. Selecting on generations
# alone would silently drop a model that only edits, and the offline path would
# then tell the caller it "is not in the Ofox model list" — a confident wrong
# answer about a model the API serves.
#
# pricing keeps prompt/image alongside output_image because both cost paths
# read them: image_cost_for multiplies input tokens by prompt, and edit_cost_for
# prices the uploaded picture at the separate `image` rate. Without them the
# offline cost line is silently absent rather than approximate.
jq --arg date "$(date -u +%Y-%m-%d)" '{
  _snapshot_note: "Offline fallback only. ofox-image.sh fetches the live list from GET /v1/models (public, no API key) and only reads this file when that fetch fails. Regenerate with: references/refresh-snapshot.sh",
  _snapshot_date: $date,
  object: "list",
  data: [ .data[]
    | select((.supported_endpoints // []) | any(. == "/v1/images/generations" or . == "/v1/images/edits"))
    | {id, is_deprecated, expiration_date, aliases,
       pricing: {prompt: .pricing.prompt,
                 image: .pricing.image,
                 output_image: .pricing.output_image},
       supported_endpoints}
  ]
}' "$tmp" > "$OUT"

printf 'wrote %s (%s image models, %s bytes)\n' \
  "$OUT" "$(jq '.data | length' "$OUT")" "$(wc -c < "$OUT" | tr -d ' ')"
