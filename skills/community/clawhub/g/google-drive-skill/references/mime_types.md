# Google Drive MIME Types Reference

## Google Workspace Types

| Resource | MIME Type |
|----------|-----------|
| Folder | `application/vnd.google-apps.folder` |
| Google Docs | `application/vnd.google-apps.document` |
| Google Sheets | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Google Forms | `application/vnd.google-apps.form` |
| Google Drawings | `application/vnd.google-apps.drawing` |
| Google Maps | `application/vnd.google-apps.map` |
| Google Sites | `application/vnd.google-apps.site` |
| Google Apps Script | `application/vnd.google-apps.script` |
| Shortcut | `application/vnd.google-apps.shortcut` |

**Note:** Google Workspace files (Docs, Sheets, etc.) cannot be downloaded directly with `get_media`. Export them first:

```python
# Export Google Doc as PDF
request = drive.files().export_media(
    fileId=file_id,
    mimeType="application/pdf"
)
```

## Common Binary / Text Types

| Content | MIME Type |
|---------|-----------|
| PDF | `application/pdf` |
| ZIP | `application/zip` |
| Plain text | `text/plain` |
| HTML | `text/html` |
| Markdown | `text/markdown` |
| CSV | `text/csv` |
| JSON | `application/json` |
| XML | `application/xml` |
| JavaScript | `text/javascript` |
| Python | `text/x-python` |

## Image Types

| Format | MIME Type |
|--------|-----------|
| PNG | `image/png` |
| JPEG | `image/jpeg` |
| GIF | `image/gif` |
| WebP | `image/webp` |
| SVG | `image/svg+xml` |
| TIFF | `image/tiff` |
| BMP | `image/bmp` |
| ICO | `image/x-icon` |

## Audio / Video Types

| Format | MIME Type |
|--------|-----------|
| MP4 | `video/mp4` |
| WebM | `video/webm` |
| AVI | `video/x-msvideo` |
| MP3 | `audio/mpeg` |
| WAV | `audio/wav` |
| OGG | `audio/ogg` |

## Office / Document Types

| Format | MIME Type |
|--------|-----------|
| DOCX | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| XLSX | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| PPTX | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| ODT | `application/vnd.oasis.opendocument.text` |
| ODS | `application/vnd.oasis.opendocument.spreadsheet` |

## Auto-detection in Python

```python
import mimetypes

mime_type, _ = mimetypes.guess_type("report.pdf")
# mime_type = "application/pdf"

mime_type, _ = mimetypes.guess_type("unknown.xyz")
# mime_type = None  → fall back to "application/octet-stream"
```
