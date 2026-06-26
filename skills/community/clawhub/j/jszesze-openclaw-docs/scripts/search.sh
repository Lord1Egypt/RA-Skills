#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash ./scripts/search.sh <keyword or regex>"
  exit 1
fi

query="$*"
extract_doc_tsv | awk -F '\t' -v q="$query" 'BEGIN{IGNORECASE=1} $1 ~ q || $2 ~ q {printf "- %s\n  %s\n", $1, $2; found=1} END{if (!found) exit 2}'
