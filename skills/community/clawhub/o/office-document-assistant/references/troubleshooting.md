# Troubleshooting

Use this guide when extraction is weak, empty, or fails.

## Quick dependency checks

Preferred quick check:

```bash
python3 {skill_dir}/scripts/check_deps.py
```

Manual checks if needed:

### Python packages

```bash
python3 - <<'PY'
import importlib
mods = ["pypdf", "docx", "openpyxl", "pptx"]
for m in mods:
    try:
        importlib.import_module(m)
        print(f"OK {m}")
    except Exception as e:
        print(f"MISS {m}: {e}")
PY
```

### System tools

```bash
command -v pdftoppm || true
command -v tesseract || true
command -v libreoffice || true
command -v antiword || true
command -v catdoc || true
```

### Tesseract languages

```bash
tesseract --list-langs
```

Look for:
- `chi_sim`
- `eng`

## Common issues

### 1. PDF returns little or no text
Likely causes:
- scanned PDF without embedded text
- missing `pdftoppm`
- missing `tesseract`
- missing OCR language packs

What to do:
- install `poppler-utils`
- install `tesseract-ocr`
- install `tesseract-ocr-chi-sim` for Chinese PDFs
- rerun extraction

### 2. Chinese OCR quality is poor
Likely causes:
- `chi_sim` missing
- low-quality scan
- rotated pages
- low contrast or tiny text

What to do:
- verify `chi_sim` appears in `tesseract --list-langs`
- warn the user that OCR quality may be limited by scan quality

### 3. Legacy `.doc` file fails
Likely causes:
- missing `antiword`
- missing `catdoc`
- missing `libreoffice`

What to do:
- install `antiword`
- install `catdoc`
- install `libreoffice`
- rerun extraction

### 4. Legacy `.xls` or `.ppt` file fails
Likely cause:
- missing `libreoffice`

What to do:
- install `libreoffice`
- rerun extraction

### 5. Extracted tables look messy
This is expected for text-first extraction.
The script is intended to expose content, not fully reconstruct styling or merged-cell semantics.
Explain the table in words instead of pretending the layout is exact.

### 6. Output is truncated
The script supports `--max-chars`.
If the result is cut off, rerun with a larger limit when needed.

## Practical guidance for replies

When extraction succeeds but is imperfect:
- say what was extracted directly
- say what parts may be noisy or OCR-derived
- avoid overclaiming certainty

When extraction fails:
- name the missing dependency or likely cause clearly
- suggest the smallest next step
- do not hallucinate document contents
