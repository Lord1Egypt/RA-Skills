#!/usr/bin/env bash
# pdf-extract.sh — Universal PDF text extraction with OCR fallback
# Usage: pdf-extract.sh <pdf-file> [--ocr-only] [--text-only] [--lang chi_sim+eng] [--dpi 300] [--output /path/to/output.txt]
#
# Strategy:
#   1. Try pdftotext (fast, high quality for text-layer PDFs)
#   2. If text extraction yields too little content, fall back to OCR
#   3. OCR: pdftoppm → tesseract (per-page, merged output)
#
# Exit codes:
#   0 = success
#   1 = missing input file
#   2 = missing required tools
#   3 = extraction failed

set -euo pipefail

# --- Defaults ---
OCR_ONLY=false
TEXT_ONLY=false
LANG="chi_sim+eng"
DPI=300
OUTPUT=""
AUTO_INSTALL=false
MIN_CHARS_PER_PAGE=50  # threshold: if avg chars/page < this, text layer is "empty"

# --- Allowed tesseract language codes (validation allowlist) ---
ALLOWED_LANGS="afr amh ara asm aze aze_cyrl bel ben bod bos bre bul cat ceb ces chi_sim chi_tra chr cos cym dan deu div dzo eng enm epo est eus fao fas fil fin fra frk frm fry gla gle glg grc guj hat hbs heb hin hrv hun hye iku ind isl ita ita_old jav jpn kan kat kat_old kaz khm kir kmr kor lao lat lav lit ltz mal mar mkd mlt mon mri msa mya nep nld nor oci ori osd pan pol por pus que ron rus san sin slk slv snd spa spa_old sqi srp srp_latn sun swa swe syr tam tat tel tgk tha tir ton tur uig ukr urd uzb uzb_cyrl vie yid yor"

# --- Parse args ---
PDF_FILE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ocr-only)  OCR_ONLY=true; shift ;;
    --auto-install) AUTO_INSTALL=true; shift ;;
    --text-only) TEXT_ONLY=true; shift ;;
    --lang)      LANG="$2"; shift 2 ;;
    --dpi)       DPI="$2"; shift 2 ;;
    --output|-o) OUTPUT="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: pdf-extract.sh <pdf-file> [--ocr-only] [--text-only] [--lang chi_sim+eng] [--dpi 300] [--output file.txt]"
      exit 0
      ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *)  PDF_FILE="$1"; shift ;;
  esac
done

if [[ -z "$PDF_FILE" ]]; then
  echo "Error: No PDF file specified" >&2
  exit 1
fi

if [[ ! -f "$PDF_FILE" ]]; then
  echo "Error: File not found: $PDF_FILE" >&2
  exit 1
fi

# --- Helper: output to file or stdout ---
output_text() {
  if [[ -n "$OUTPUT" ]]; then
    cat > "$OUTPUT"
    echo "[pdf-extract] Output written to: $OUTPUT" >&2
  else
    cat
  fi
}

# --- Helper: check tool availability ---
check_tool() {
  if ! command -v "$1" &>/dev/null; then
    return 1
  fi
  return 0
}

# --- Helper: validate language codes ---
validate_lang() {
  IFS='+' read -ra LANGS <<< "$1"
  for l in "${LANGS[@]}"; do
    # Only allow alphanumeric + underscore (strict tesseract lang code format)
    if ! [[ "$l" =~ ^[a-z]{2,3}(_[a-z]+)?$ ]]; then
      echo "[pdf-extract] Error: Invalid language code: '$l'. Must match pattern: [a-z]{2,3}(_[a-z]+)?" >&2
      exit 1
    fi
    if ! echo " $ALLOWED_LANGS " | grep -q " $l "; then
      echo "[pdf-extract] Error: Unsupported language code: '$l'. Use --lang with valid tesseract codes (e.g., chi_sim+eng)." >&2
      exit 1
    fi
  done
}

# --- Helper: install missing tools ---
install_tools() {
  local need_poppler=false
  local need_tesseract=false

  if ! check_tool pdftotext || ! check_tool pdftoppm || ! check_tool pdfinfo; then
    need_poppler=true
  fi
  if ! check_tool tesseract; then
    need_tesseract=true
  fi

  if $need_poppler || $need_tesseract; then
    if ! $AUTO_INSTALL; then
      echo "[pdf-extract] Error: Missing required tools." >&2
      if $need_poppler; then echo "  - poppler-utils (provides pdftotext, pdftoppm, pdfinfo)" >&2; fi
      if $need_tesseract; then echo "  - tesseract-ocr + language packs" >&2; fi
      echo "" >&2
      echo "Install manually:" >&2
      echo "  apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-chi-sim" >&2
      echo "" >&2
      echo "Or re-run with --auto-install to install automatically." >&2
      exit 2
    fi

    echo "[pdf-extract] Auto-installing missing tools..." >&2
    # Build validated package list
    local lang_pkgs=()
    IFS='+' read -ra LANGS <<< "$LANG"
    for l in "${LANGS[@]}"; do
      lang_pkgs+=("tesseract-ocr-$l")
    done

    if check_tool apt-get; then
      apt-get update -qq 2>/dev/null
      if $need_poppler; then
        apt-get install -y -qq poppler-utils 2>/dev/null
      fi
      if $need_tesseract; then
        apt-get install -y -qq tesseract-ocr "${lang_pkgs[@]}" 2>/dev/null
      fi
    elif check_tool yum; then
      if $need_poppler; then yum install -y -q poppler-utils 2>/dev/null; fi
      if $need_tesseract; then yum install -y -q tesseract "${lang_pkgs[@]}" 2>/dev/null; fi
    elif check_tool brew; then
      if $need_poppler; then brew install poppler 2>/dev/null; fi
      if $need_tesseract; then brew install tesseract tesseract-lang 2>/dev/null; fi
    else
      echo "[pdf-extract] Error: Cannot auto-install tools. Please install poppler-utils and tesseract-ocr manually." >&2
      exit 2
    fi
  fi
}

# --- Get page count ---
get_page_count() {
  pdfinfo "$PDF_FILE" 2>/dev/null | grep -i "^Pages:" | awk '{print $2}'
}

# --- Strategy 1: pdftotext extraction ---
extract_text_layer() {
  local text
  text=$(pdftotext "$PDF_FILE" - 2>/dev/null)
  echo "$text"
}

# --- Strategy 2: OCR extraction ---
extract_ocr() {
  local tmpdir
  tmpdir=$(mktemp -d "/tmp/pdf-extract-XXXXXX")
  trap "rm -rf '$tmpdir'" EXIT

  local pages
  pages=$(get_page_count)
  echo "[pdf-extract] OCR: Converting $pages pages to images (DPI=$DPI)..." >&2
  pdftoppm "$PDF_FILE" "$tmpdir/page" -png -r "$DPI" 2>/dev/null

  echo "[pdf-extract] OCR: Running tesseract (lang=$LANG)..." >&2
  local result=""
  local count=0
  for img in "$tmpdir"/page-*.png; do
    [[ -f "$img" ]] || continue
    count=$((count + 1))
    local page_text
    page_text=$(tesseract "$img" stdout -l "$LANG" --psm 6 2>/dev/null || true)
    if [[ -n "$page_text" ]]; then
      result+="--- Page $count ---"$'\n'"$page_text"$'\n\n'
    fi
    # Progress indicator
    if (( count % 5 == 0 )); then
      echo "[pdf-extract] OCR: Processed $count/$pages pages..." >&2
    fi
  done

  echo "[pdf-extract] OCR: Completed $count pages" >&2
  echo "$result"
}

# --- Evaluate text quality ---
is_text_sufficient() {
  local text="$1"
  local pages="$2"

  if [[ -z "$text" ]]; then
    return 1
  fi

  local char_count=${#text}
  # Strip whitespace-only content
  local stripped
  stripped=$(echo "$text" | tr -d '[:space:]')
  local real_chars=${#stripped}

  if [[ "$pages" -eq 0 ]]; then
    pages=1
  fi

  local avg_chars_per_page=$((real_chars / pages))

  if (( avg_chars_per_page < MIN_CHARS_PER_PAGE )); then
    echo "[pdf-extract] Text layer too sparse: ${avg_chars_per_page} chars/page (threshold: ${MIN_CHARS_PER_PAGE})" >&2
    return 1
  fi

  echo "[pdf-extract] Text layer OK: ${avg_chars_per_page} chars/page across ${pages} pages" >&2
  return 0
}

# --- Main ---
validate_lang "$LANG"
install_tools

# Verify critical tools
if ! check_tool pdftotext || ! check_tool pdfinfo; then
  echo "Error: poppler-utils not available" >&2
  exit 2
fi

pages=$(get_page_count)
echo "[pdf-extract] Processing: $(basename "$PDF_FILE") ($pages pages)" >&2

# Check PDF producer for early OCR hint
producer=$(pdfinfo "$PDF_FILE" 2>/dev/null | grep -i "^Producer:" | sed 's/^Producer:\s*//')
is_scan=false
if echo "$producer" | grep -qi "image.conversion\|scan\|canon\|xerox\|fujitsu"; then
  echo "[pdf-extract] Detected scan/image-based PDF (Producer: $producer)" >&2
  is_scan=true
fi

if $OCR_ONLY; then
  echo "[pdf-extract] Mode: OCR only" >&2
  if ! check_tool tesseract; then
    echo "Error: tesseract not available for OCR" >&2
    exit 2
  fi
  extract_ocr | output_text
  exit 0
fi

if $TEXT_ONLY; then
  echo "[pdf-extract] Mode: Text only (no OCR fallback)" >&2
  extract_text_layer | output_text
  exit 0
fi

# Auto mode: try text first, OCR fallback
if $is_scan; then
  echo "[pdf-extract] Skipping text extraction for scan PDF, going straight to OCR" >&2
  if ! check_tool tesseract; then
    install_tools
  fi
  extract_ocr | output_text
  exit 0
fi

echo "[pdf-extract] Trying text extraction..." >&2
text_result=$(extract_text_layer)

if is_text_sufficient "$text_result" "$pages"; then
  echo "[pdf-extract] Success: Text layer extraction" >&2
  echo "$text_result" | output_text
  exit 0
fi

echo "[pdf-extract] Text layer insufficient, falling back to OCR..." >&2
if ! check_tool tesseract; then
  install_tools
fi

if ! check_tool tesseract; then
  echo "[pdf-extract] Warning: tesseract unavailable, returning sparse text result" >&2
  echo "$text_result" | output_text
  exit 0
fi

ocr_result=$(extract_ocr)
# Use whichever result has more content
text_len=${#text_result}
ocr_len=${#ocr_result}

if (( ocr_len > text_len )); then
  echo "[pdf-extract] Using OCR result (${ocr_len} chars vs text ${text_len} chars)" >&2
  echo "$ocr_result" | output_text
else
  echo "[pdf-extract] Using text result (${text_len} chars vs OCR ${ocr_len} chars)" >&2
  echo "$text_result" | output_text
fi

exit 0
