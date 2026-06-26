# Hybrid Mode + OCR

## When to enable hybrid
- Complex tables
- Scanned PDFs
- Multi-language OCR
- Image/chart descriptions

## Start backend
Standard:
opendataloader-pdf-hybrid --port 5002

Forced OCR:
opendataloader-pdf-hybrid --port 5002 --force-ocr

Multi-language OCR:
opendataloader-pdf-hybrid --port 5002 --force-ocr --ocr-lang "es,en"

Image description:
opendataloader-pdf-hybrid --port 5002 --enrich-picture-description

## Use backend from client
Auto mode (triage):
opendataloader-pdf --hybrid docling-fast file1.pdf file2.pdf ./folder/ -o ./output -f json,markdown

With timeout and fallback:
opendataloader-pdf --hybrid docling-fast --hybrid-timeout 120000 --hybrid-fallback file1.pdf ./folder/ -o ./output -f json

## Critical rule
If --enrich-picture-description is used on the backend, the client must use --hybrid-mode full.

Example:
opendataloader-pdf --hybrid docling-fast --hybrid-mode full file1.pdf ./folder/ -o ./output -f json,markdown
