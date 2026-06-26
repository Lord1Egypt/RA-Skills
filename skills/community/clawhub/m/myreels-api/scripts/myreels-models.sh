#!/usr/bin/env bash
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

usage() {
  cat <<'EOF'
Usage:
  myreels-models.sh [--tag <tag>] [--model <model_name>] [--summary] [--raw]
  myreels-models.sh -h | --help

Description:
  Load live model metadata from /api/v1/models/api.

Options:
  --tag <tag>          Filter models by tag, for example t2i, i2v, t2v
  --model <name>       Return a single model by exact modelName
  --summary            Return a compact view for selection
  --raw                Return the raw API payload instead of filtered items

Returns:
  Default:
    .data.items array, optionally filtered
  --model:
    single model object
  --summary:
    compact objects with modelName, tags, cost, estimatedTime, and input keys
  --raw:
    raw API response body
EOF
}

source "$(dirname "$0")/_common.sh"

tag=""
model_name=""
summary=false
raw=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag)
      [[ $# -ge 2 ]] || { echo "Error: --tag requires a value" >&2; exit 2; }
      tag="$2"
      shift 2
      ;;
    --model)
      [[ $# -ge 2 ]] || { echo "Error: --model requires a value" >&2; exit 2; }
      model_name="$2"
      shift 2
      ;;
    --summary)
      summary=true
      shift
      ;;
    --raw)
      raw=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

payload=$(myreels_get_optional_auth "/api/v1/models/api")
myreels_require_api_ok "$payload" "Load models failed" || exit 1

if [[ "$raw" == "true" ]]; then
  echo "$payload" | jq '.'
  exit 0
fi

items=$(echo "$payload" | jq '.data.items // []')

if [[ -n "$tag" ]]; then
  items=$(echo "$items" | jq --arg tag "$tag" '
    map(
      select(
        if (.tags | type) == "array" then
          any(.tags[]?; . == $tag)
        elif (.tags | type) == "string" then
          .tags == $tag
        else
          false
        end
      )
    )
  ')
fi

if [[ -n "$model_name" ]]; then
  item=$(echo "$items" | jq --arg model "$model_name" '
    map(select(.modelName == $model)) | if length > 0 then .[0] else empty end
  ')
  if [[ -z "$item" ]]; then
    echo "Error: model not found: $model_name" >&2
    exit 1
  fi
  items="$item"
fi

if [[ "$summary" == "true" ]]; then
  items=$(echo "$items" | jq '
    def summarize:
      {
        modelName,
        name,
        tags,
        estimatedCost,
        estimatedTime: (.displayConfig.estimatedTime // null),
        description,
        inputs: (
          .userInputSchema
          | if type == "object" then (keys | sort) else [] end
        )
      };

    if type == "array" then map(summarize) else summarize end
  ')
fi

echo "$items" | jq '.'
