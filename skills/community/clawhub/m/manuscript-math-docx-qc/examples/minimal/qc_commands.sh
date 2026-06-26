#!/usr/bin/env bash
set -euo pipefail

mkdir -p build/pdf_check/pages

pandoc examples/minimal/manuscript.md -o build/minimal-manuscript.docx
unzip -t build/minimal-manuscript.docx >/tmp/minimal-docx-unzip.log
tail -5 /tmp/minimal-docx-unzip.log

soffice --headless --convert-to pdf --outdir build/pdf_check build/minimal-manuscript.docx
pdfinfo build/pdf_check/minimal-manuscript.pdf | rg 'Pages|Page size|File size'

pdftoppm -png -r 130 build/pdf_check/minimal-manuscript.pdf build/pdf_check/pages/page
ls -lh build/pdf_check/pages
