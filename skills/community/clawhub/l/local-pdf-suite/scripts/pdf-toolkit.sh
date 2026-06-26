#!/bin/bash
# PDF Toolkit — Stirling-PDF CLI helper
# Usage: ./pdf-toolkit.sh <command> [files...]
# Env: STIRLING_API_KEY, STIRLING_BASE_URL (optional)

BASE_URL="${STIRLING_BASE_URL:-http://localhost:3998}"
API_KEY="${STIRLING_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "Error: STIRLING_API_KEY not set"
  exit 1
fi

auth() { echo "-H"; echo "X-API-KEY: $API_KEY"; }

do_curl() {
  curl -s -H "X-API-KEY: $API_KEY" "$@"
}

CMD="${1:-}"; shift

case "$CMD" in
  ocr)
    lang="${2:-chi_sim+eng}"
    do_curl -X POST "$BASE_URL/api/v1/misc/ocr-pdf" \
      -F "fileInput=@${1?}" \
      -F "languages=$lang" \
      -o "${1%.pdf}_ocr.pdf"
    echo "Saved: ${1%.pdf}_ocr.pdf"
    ;;

  merge)
    files=("$@")
    if [ ${#files[@]} -lt 2 ]; then echo "Need 2+ files"; exit 1; fi
    for f in "${files[@]}"; do
      cmd="$cmd -F fileInput[]=@$f"
    done
    do_curl -X POST "$BASE_URL/api/v1/general/merge-pdfs" \
      -F sortType=orderProvided $cmd \
      -o merged.pdf
    echo "Saved: merged.pdf"
    ;;

  compress)
    do_curl -X POST "$BASE_URL/api/v1/misc/compress-pdf" \
      -F "fileInput=@${1?}" \
      -F "compressionLevel=standard" \
      -o "${1%.pdf}_compressed.pdf"
    echo "Saved: ${1%.pdf}_compressed.pdf"
    ;;

  remove-blanks)
    do_curl -X POST "$BASE_URL/api/v1/misc/remove-blanks" \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}_noBlanks.zip"
    echo "Saved: ${1%.pdf}_noBlanks.zip"
    ;;

  to-word)
    do_curl -X POST "$BASE_URL/api/v1/convert/pdf/word" \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}.docx"
    echo "Saved: ${1%.pdf}.docx"
    ;;

  to-html)
    do_curl -X POST "$BASE_URL/api/v1/convert/pdf/html" \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}.html"
    echo "Saved: ${1%.pdf}.html"
    ;;

  to-md)
    do_curl -X POST "$BASE_URL/api/v1/convert/pdf/markdown" \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}.md"
    echo "Saved: ${1%.pdf}.md"
    ;;

  to-pdfa)
    do_curl -X POST "$BASE_URL/api/v1/convert/pdf/pdfa" \
      -F "fileInput=@${1?}" \
      -o "${1%.pdf}_archival.pdf"
    echo "Saved: ${1%.pdf}_archival.pdf"
    ;;

  img2pdf)
    do_curl -X POST "$BASE_URL/api/v1/convert/img/pdf" \
      -F "fileInput=@${1?}" \
      -F "colorType=color" \
      -F "fitOption=maintainAspectRatio" \
      -o "${1%.*}.pdf"
    echo "Saved: ${1%.*}.pdf"
    ;;

  encrypt)
    do_curl -X POST "$BASE_URL/api/v1/security/encrypt" \
      -F "fileInput=@${1?}" \
      -F "userPassword=${2?}" \
      -F "ownerPassword=${2?}" \
      -o "${1%.pdf}_encrypted.pdf"
    echo "Saved: ${1%.pdf}_encrypted.pdf"
    ;;

  decrypt)
    do_curl -X POST "$BASE_URL/api/v1/security/decrypt" \
      -F "fileInput=@${1?}" \
      -F "password=${2?}" \
      -o "${1%.pdf}_decrypted.pdf"
    echo "Saved: ${1%.pdf}_decrypted.pdf"
    ;;

  watermark)
    do_curl -X POST "$BASE_URL/api/v1/security/add-watermark" \
      -F "fileInput=@${1?}" \
      -F "watermarkType=text" \
      -F "watermarkText=${2:-WATERMARK}" \
      -F "fontSize=30" \
      -F "opacity=0.5" \
      -F "rotation=0" \
      -F "alphabet=roman" \
      -o "${1%.pdf}_watermarked.pdf"
    echo "Saved: ${1%.pdf}_watermarked.pdf"
    ;;

  rotate)
    do_curl -X POST "$BASE_URL/api/v1/general/rotate-pdf" \
      -F "fileInput=@${1?}" \
      -F "rotation=${2:-90}" \
      -o "${1%.pdf}_rotated.pdf"
    echo "Saved: ${1%.pdf}_rotated.pdf"
    ;;

  health)
    do_curl "$BASE_URL/api/v1/info/health"
    ;;

  *)
    echo "PDF Toolkit — usage:"
    echo "  ocr <file> [lang]       OCR (default: chi_sim+eng)"
    echo "  merge <f1> <f2> [...]   Combine PDFs"
    echo "  compress <file>          Reduce file size"
    echo "  remove-blanks <file>     Strip empty pages"
    echo "  to-word <file>          PDF → Word (.docx)"
    echo "  to-html <file>          PDF → HTML"
    echo "  to-md <file>            PDF → Markdown"
    echo "  to-pdfa <file>          PDF → PDF/A (archival)"
    echo "  img2pdf <file>          Image → PDF"
    echo "  encrypt <file> <pass>   Password protect"
    echo "  decrypt <file> <pass>   Remove password"
    echo "  watermark <file> <text>  Add text watermark"
    echo "  rotate <file> <deg>      Rotate (90/180/270)"
    echo "  health                  Check API status"
    ;;
esac