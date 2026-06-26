# Setup

## API key

1. Obtain an API key at `https://nowatermark.info/api-keys`.
2. Configure `NOWATERMARK_API_KEY` before using the skill.

Preferred OpenClaw config:

```json
{
  "skills": {
    "entries": {
      "image-watermark-remover": {
        "enabled": true,
        "env": {
          "NOWATERMARK_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Shell examples:

- POSIX: `export NOWATERMARK_API_KEY="your_api_key_here"`
- PowerShell: `$env:NOWATERMARK_API_KEY="your_api_key_here"`

## Input rules

- Provide one direct public image URL.
- Supported formats: `jpg`, `jpeg`, `png`, `webp`, `heic`, `avif`, `bmp`, `tiff`.
- Prefer files at or under 10 MB.
- Avoid local file paths, browser page URLs, and expiring signed URLs.

## Commands

macOS / Linux:

```bash
python3 scripts/remove_watermark.py --file-url https://example.com/input.png
```

Windows PowerShell:

```powershell
python scripts/remove_watermark.py --file-url https://example.com/input.png
```

Resume an existing job:

```bash
python3 scripts/remove_watermark.py --request-id req_xxx
```
