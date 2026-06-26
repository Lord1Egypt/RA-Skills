# Troubleshooting: KaTeX → PNG

## Symptom: formulas look broken / weird

Most common cause: **KaTeX CSS or fonts** were not loaded.

### Correct setup

- KaTeX renders HTML
- You must load `katex.min.css`
- You must load KaTeX fonts (woff/ttf) via relative `fonts/...` URLs

### What to do

- Do NOT inline the CSS as a string if it contains `url(fonts/...)`
- Link the CSS as a local file:
  - `<link rel="stylesheet" href="file:///.../katex.min.css">`
  - then relative `fonts/` resolve next to the CSS file

### Headless Brave flags

This skill uses headless Brave and allows local file access:
- `--allow-file-access-from-files`

If running as root, Chromium requires:
- `--no-sandbox`
- `--disable-setuid-sandbox`

## Symptom: "Running as root without --no-sandbox is not supported"

Add:
- `--no-sandbox`
- `--disable-setuid-sandbox`
