# Troubleshooting

## No Browser Found

If the script reports no local browser:

- verify Chrome, Chromium, Edge, or Brave is installed
- if not, allow the script to install Playwright Chromium

## Playwright Import Failed

If Playwright is missing:

- the exporter will try to install the Python package automatically
- if that fails, install manually:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

## Remote Images Missing

Possible causes:

- broken source URLs
- blocked external network
- image host rate limiting

The exporter waits for document fonts and image completion, but it cannot fix invalid URLs.

## JPG Looks Soft

Use PNG first for validation.

Switch to JPG only when:

- upload size matters more than sharpness, or
- the target platform compresses PNG heavily anyway

## Table Overflow

This skill preserves tables faithfully. If a source table is too wide for a phone:

- expect narrow columns and wrapped text
- if the user wants more aggressive redesign, this is no longer faithful conversion and should be treated as a different task
