#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="${ROOT}/examples/improved/manuscript.md"
OUT_DIR="${ROOT}/build/improved"
PDF_DIR="${OUT_DIR}/pdf_check"
PAGES_DIR="${PDF_DIR}/pages"

mkdir -p "${PAGES_DIR}"

pandoc "${SRC}" -o "${OUT_DIR}/improved-manuscript.docx"
unzip -t "${OUT_DIR}/improved-manuscript.docx" >/tmp/improved-docx-unzip.log
tail -5 /tmp/improved-docx-unzip.log

soffice --headless --convert-to pdf --outdir "${PDF_DIR}" "${OUT_DIR}/improved-manuscript.docx"
pdfinfo "${PDF_DIR}/improved-manuscript.pdf" | rg 'Pages|Page size|File size'

rm -f "${PAGES_DIR}"/page-*.png
pdftoppm -png -r 130 "${PDF_DIR}/improved-manuscript.pdf" "${PAGES_DIR}/page"
ls -lh "${PAGES_DIR}"
