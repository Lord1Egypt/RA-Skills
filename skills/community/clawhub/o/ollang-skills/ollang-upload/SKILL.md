---
name: ollang-upload
description: Upload files to Ollang API. Supports direct file uploads (video, audio, documents, spreadsheets) and VTT subtitle file uploads. Use when the user wants to upload a file to Ollang or add a project.
---

# Ollang File Upload

Upload files to the Ollang platform via the integration API.

## Authentication

All requests require the `X-Api-Key` header. The API key is read from the `OLLANG_API_KEY` environment variable. If not set, instruct the user to run: `export OLLANG_API_KEY=<your-api-key>` (get it from https://lab.ollang.com).

## Direct File Upload

**POST** `https://api-integration.ollang.com/integration/upload/direct`

Uploads video, audio, document, or spreadsheet files and creates a project.

### Request (multipart/form-data)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | File to upload (video, audio, document, spreadsheet) |
| `name` | string | Yes | Descriptive name for the uploaded content |
| `sourceLanguage` | string | Yes | Source language code (e.g., `en`, `es`, `fr`) |
| `notes` | array | No | Instruction objects with `details` and optional `timeStamp` (e.g., `[{"details": "Ignore subtitles for 30s", "timeStamp": "02:15:30"}]`) |
| `folderId` | string | No | Destination folder ID (defaults to "API Uploads") |

### Response (201)
```json
{ "projectId": "string" }
```

### Example (curl)
```bash
curl -X POST https://api-integration.ollang.com/integration/upload/direct \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -F "file=@/path/to/video.mp4" \
  -F "name=My Video" \
  -F "sourceLanguage=en" \
  -F "folderId=OPTIONAL_FOLDER_ID"
```

---

## Upload VTT File

**POST** `https://api-integration.ollang.com/integration/upload/vtt`

Associates a VTT subtitle file with an existing project.

### Request (multipart/form-data)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | VTT file (max 1GB) |
| `projectId` | string | Yes | Target project ID |
| `name` | string | Yes | Name for the document |
| `sourceLanguage` | string | No | Source language code |

### Response (201)
```json
{ "projectId": "string" }
```

### Example (curl)
```bash
curl -X POST https://api-integration.ollang.com/integration/upload/vtt \
  -H "X-Api-Key: $OLLANG_API_KEY" \
  -F "file=@/path/to/subtitles.vtt" \
  -F "projectId=PROJECT_ID" \
  -F "name=My Subtitles" \
  -F "sourceLanguage=en"
```

## Behavior

1. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
2. Determine if uploading a new file (direct upload) or attaching a VTT to existing project
3. For direct uploads: require `file`, `name`, `sourceLanguage`; optionally `folderId`
4. For VTT uploads: require `file`, `projectId`, `name`
5. Execute the upload and return the `projectId`
6. Note: save the `projectId` — it's needed to create orders

## Error Codes
- `400` - Invalid parameters or unsupported file format
- `401` - Invalid or missing API key
- `413` - File too large
