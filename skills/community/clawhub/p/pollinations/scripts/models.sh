#!/bin/bash
# Pollinations Model Listing (single source: GET /v1/models)
# Usage: ./models.sh [text|image|video|audio|vision|embedding|3d|all] [--free] [--json]
# Prints: id  [aliases]  free|paid. Use an id or any alias as --model.

set -e

TYPE="all"; FREE_ONLY=0; AS_JSON=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) TYPE="$2"; shift 2 ;;
    --free) FREE_ONLY=1; shift ;;
    --json) AS_JSON=1; shift ;;
    text|image|video|audio|vision|embedding|3d|all) TYPE="$1"; shift ;;
    *) echo "Usage: models.sh [text|image|video|audio|vision|embedding|3d|all] [--free] [--json]"; exit 1 ;;
  esac
done

DATA=$(curl -s --max-time 30 ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
  "https://gen.pollinations.ai/v1/models")
if ! echo "$DATA" | jq -e '(.data // .) | length > 0' >/dev/null 2>&1; then
  echo "Error: could not fetch models from gen.pollinations.ai/v1/models"; exit 1
fi

# vision = text models that accept image input
FILTER='(.data // .)[]'
case "$TYPE" in
  all) ;;
  vision) FILTER="$FILTER | select(.category==\"text\" and (.input_modalities|index(\"image\")))" ;;
  *) FILTER="$FILTER | select(.category==\"$TYPE\")" ;;
esac
[[ $FREE_ONLY -eq 1 ]] && FILTER="$FILTER | select(.paid_only|not)"

if [[ $AS_JSON -eq 1 ]]; then
  echo "$DATA" | jq "[${FILTER}]"
else
  echo "$DATA" | jq -r "$FILTER | \"\(.category)\t\(.id)\t[\(.aliases|join(\",\"))]\t\(if .paid_only then \"paid\" else \"free\" end)\"" | sort
fi
