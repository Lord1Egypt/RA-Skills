#!/bin/bash
# Stirling-PDF helper script
# Usage: ./stirling-pdf.sh <command> [files...]
# Requires: STIRLING_API_KEY env var

BASE_URL="${STIRLING_API_URL:-http://192.168.31.158:3998}"
API_KEY="${STIRLING_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "Error: STIRLING_API_KEY not set"
  exit 1
fi

CMD="${1:-}"
shift

auth_header() {
  echo "-H X-API-KEY: $API_KEY"
}

case "$CMD" in
  ocr)
    lang="${1:-chi_sim+eng}"
    curl -s -X POST "$BASE_URL/api/v1/misc/ocr-pdf" \
      $(auth_header) \
      -F "fileInput=@${2?}" \
      -F "languages=$lang" \
      -o "${2%.pdf}_ocr.pdf"
    echo "Saved: ${2%.pdf}_ocr.pdf"
    ;;

  merge)
    files=("$@")
    if [ ${#files[@]} -lt 2 ]; then
      echo "Need at least 2 files to merge"
      exit 1
    fi
    cmd="curl -s -X POST $BASE_URL/api/v1/general/merge-pdfs $(auth_header)"
    for f in "${files[@]}"; do
      cmd="$cmd -F fileInput[]=@$f"
    done
    cmd="$cmd -F sortType=orderProvided -o merged.pdf"
    eval "$cmd"
    echo "Saved: merged.pdf"
    ;;

  compress)
    level="${2:-standard}"
    curl -s -X POST "$BASE_URL/api/v1/misc/compress-pdf" \
      $(auth_header) \
      -F "fileInput=@${1?}" \
      -F "compressionLevel=$level" \
      -o "${1%.pdf}_compressed.pdf"
    echo "Saved: ${1%.pdf}_compressed.pdf"
    ;;

  remove-blanks)
    curl -s -X POST "$BASE_URL/api/v1/misc/remove-blanks" \
      $(auth_header) \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}_noBlanks.zip"
    echo "Saved: ${1%.pdf}_noBlanks.zip"
    ;;

  health)
    curl -s "$BASE_URL/api/v1/info/health" $(auth_header)
    ;;

  *)
    echo "Usage: stirling-pdf.sh <command> [args...]"
    echo "Commands: ocr, merge, compress, remove-blanks, health"
    ;;
esac