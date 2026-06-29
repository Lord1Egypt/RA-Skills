---
name: okfile
description: "Uploads and publishes files or static site folders to OkFile, with direct links, preview URLs, and multipart support. Use when the user asks to upload, publish, or share files or folders."
version: 1.2.3
license: Apache-2.0
---
# OkFile Skill
Official site: `https://www.okfile.com/`

## Overview
OkFile is an agent-first file upload and publish service.
Use this skill when an agent needs to:
- upload images, videos, PDFs, or common files
- fast-path small files with `POST /api/upload/quick` when the file is within the advertised quick-upload limit
- upload a static site folder and publish it to a per-site subdomain
- rely on automatic shared top-level directory stripping for folder-based site uploads
- expose a directory listing when a site has no root `index.html`
- return a direct file URL via `url`
- return a preview or playback URL via `playUrl`
- return a published site URL via `siteUrl` or `entryUrl`
- publish files anonymously or with a user API key
- handle large files with multipart upload and retry missing parts only
- drive repeatable upload or publish workflows from the bundled Python CLI
## When To Use
Choose this skill when the user asks to:
- upload or publish a file
- generate a public file link
- generate an image, video, or PDF preview link
- publish a folder as a static website
- publish a folder that may not contain root `index.html`
- batch-process multiple files
- upload large files with resumable multipart flow
- use a Python CLI for upload, publish, status, or config operations
## Quick Start
### Discover Capabilities First
1. `GET /api/upload/config`
2. read `quickUploadMaxSize`, `multipartThreshold`, and `partSize`
3. choose `POST /api/upload/quick` for small files, or `prepare -> PUT -> complete` for normal and large uploads
### Small File Fast Path
1. `POST /api/upload/quick` with `multipart/form-data`
2. receive the same final response shape as `POST /api/upload/complete`
### Standard File Flow
1. `POST /api/upload/prepare`
2. `PUT uploadUrl` or each `parts[].uploadUrl`
3. `POST /api/upload/complete`
### Static Site Flow
1. `POST /api/site/prepare`
2. upload each file through the normal file upload flow
3. `POST /api/site/complete`

Static site behavior:
- if every uploaded path is under one shared top-level folder, OkFile strips that folder and treats its contents as the site root
- if root `index.html` exists, the site root renders that page
- if root `index.html` does not exist, the site root renders a directory listing with file name, size, and upload time
- images and videos open inline from that listing
- other files should use download links
### Minimal Prepare Request
```bash
curl -X POST "https://www.okfile.com/api/upload/prepare" \
  -H "Content-Type: application/json" \
  --data '{"filename":"photo.jpg","size":12345,"contentType":"image/jpeg","preferredPartSize":5242880}'
```
### Minimal Quick Upload Request
```bash
curl -X POST "https://www.okfile.com/api/upload/quick" \
  -F "file=@photo.jpg"
```
### Minimal Complete Request
```bash
curl -X POST "https://www.okfile.com/api/upload/complete" \
  -H "Content-Type: application/json" \
  --data '{"id":"a3k7m92x"}'
```
### Status Check
```bash
curl "https://www.okfile.com/api/upload/status/a3k7m92x"
```
### Python CLI Examples
```bash
okfile upload photo.jpg
okfile upload photo.jpg --max-downloads 10
okfile upload photo.jpg --expires-at 2026-12-31T23:59:59Z
okfile publish ./my-site/
okfile publish ./my-site/ --expires-at 2026-12-31T23:59:59Z
okfile status a3k7m92x
okfile status a3k7m92x --verbose
okfile config --key okf_xxxxx
okfile config --clear-origin
okfile --version
```
### Python CLI Install
Prefer installing the latest published PyPI package:
```bash
py -3 -m pip install okfile
okfile --version
```
If you need a pinned install for reproducibility:
```bash
py -3 -m pip install okfile==1.2.3
```
Upgrade an existing install:
```bash
py -3 -m pip install --upgrade okfile
```
If you need a direct static artifact instead of PyPI, install the wheel from OkFile:
```bash
py -3 -m pip install "https://www.okfile.com/downloads/okfile-1.2.3-py3-none-any.whl"
```
Debugging tips:
```bash
okfile upload photo.jpg --origin https://www.okfile.com --verbose
okfile status invalid_id --verbose
```
### Key Rules
- use `GET /api/upload/config` to discover the current quick-upload and multipart thresholds instead of hardcoding them
- prefer `POST /api/upload/quick` for small files when `size <= quickUploadMaxSize`
- `apiKey` is optional and is only sent to `prepare`
- `--max-downloads` and `--expires-at` are supported by the CLI for file uploads; `--expires-at` is also supported for site publish
- `okfile config --clear-origin` removes the stored default origin and falls back to `https://www.okfile.com`
- `--verbose` prints traceback details for debugging request or parsing failures
- `complete` only needs `id`
- if `complete` returns `missingParts`, re-upload only those parts
- prefer returning `url`; return `playUrl` when preview matters
## Authentication Modes
### Anonymous
Use anonymous mode for direct publishing without login.
- no account required
- rate-limited by IP
- good for lightweight or temporary tasks
### API Key
Use API key mode for controlled, long-term, or team-managed usage.
Flow:
1. `POST /api/auth/request-link`
2. open the email verification link
3. create an API key in `/account`
4. include `apiKey` in `POST /api/upload/prepare`
## Endpoints
### `GET /api/upload/config`
Response example:
```json
{
  "success": true,
  "maxSize": 524288000,
  "quickUploadMaxSize": 5242880,
  "multipartThreshold": 26214400,
  "partSize": 10485760
}
```
Notes:
- use this endpoint before uploads when the client needs dynamic limits
- `quickUploadMaxSize` indicates when `/api/upload/quick` can be used
### `POST /api/upload/prepare`
Request body:
```json
{
  "filename": "photo.jpg",
  "size": 12345,
  "contentType": "image/jpeg",
  "preferredPartSize": 5242880,
  "apiKey": "okf_..."
}
```
Notes:
- `preferredPartSize` is optional
- current supported range is `5MB` to `100MB`
- response may be `single` or `multipart`
- `expiresIn` refers to the signed `uploadUrl` or `parts[].uploadUrl` lifetime only; it does not describe a separate Worker-side upload-session TTL
- if `complete` says the upload session was not found, first verify that you are using the exact same `id` returned by that specific `prepare` call
Single upload response example:
```json
{
  "success": true,
  "id": "a3k7m92x",
  "mode": "single",
  "uploadUrl": "https://upload.example.com/...",
  "expiresIn": 3600,
  "method": "PUT",
  "url": "https://www.okfile.com/i/a3k7m92x",
  "playUrl": "https://www.okfile.com/i/a3k7m92x?play=1",
  "type": "image"
}
```
Multipart response example:
```json
{
  "success": true,
  "id": "a3k7m92x",
  "mode": "multipart",
  "uploadId": "3c4d...",
  "partSize": 5242880,
  "totalParts": 33,
  "parts": [
    { "partNumber": 1, "uploadUrl": "https://..." }
  ],
  "url": "https://www.okfile.com/i/a3k7m92x",
  "playUrl": "https://www.okfile.com/i/a3k7m92x?play=1",
  "type": "video"
}
```
### `POST /api/upload/quick`
Request:
- send `multipart/form-data`
- include the file in the `file` field
- optional fields such as `expiresAt` and `maxDownloads` follow the normal upload semantics
Success response example:
```json
{
  "success": true,
  "id": "a3k7m92x",
  "url": "https://www.okfile.com/i/a3k7m92x",
  "downloadUrl": "https://www.okfile.com/d/a3k7m92x",
  "playUrl": "https://www.okfile.com/i/a3k7m92x?play=1",
  "type": "image"
}
```
Notes:
- intended for small files only
- the response shape matches the final `complete` response so clients can reuse downstream logic
### `PUT uploadUrl` or `parts[].uploadUrl`
- upload the file body directly to the signed URL
- single mode usually needs one `PUT`
- multipart mode needs one `PUT` per part
- set `Content-Length` explicitly
### `POST /api/upload/complete`
Request body:
```json
{
  "id": "a3k7m92x"
}
```
Success response example:
```json
{
  "success": true,
  "id": "a3k7m92x",
  "url": "https://www.okfile.com/i/a3k7m92x",
  "playUrl": "https://www.okfile.com/i/a3k7m92x?play=1",
  "type": "image"
}
```
Incomplete multipart response example:
```json
{
  "success": false,
  "error": "Missing parts",
  "uploadedParts": 45,
  "totalParts": 50,
  "missingParts": [4, 12, 28, 44, 49]
}
```
### `GET /api/upload/status/{id}`
Response example:
```json
{
  "id": "a3k7m92x",
  "status": "uploading",
  "progress": "45/50",
  "uploadedParts": 45,
  "totalParts": 50,
  "bytesReceived": 471859200
}
```
### `POST /api/site/prepare`
Request body:
```json
{
  "siteName": "docs-site",
  "files": [
    { "path": "docs/getting-started.md", "size": 1200, "contentType": "text/markdown; charset=utf-8" },
    { "path": "assets/app.css", "size": 3200, "contentType": "text/css; charset=utf-8" },
    { "path": "images/logo.png", "size": 4200, "contentType": "image/png" }
  ]
}
```
Notes:
- omit `entryPath` entirely when the uploaded folder has no root `index.html`
- do not generate or upload a synthetic `index.html` just to mimic a directory listing
- when root `index.html` is absent, OkFile generates the directory listing automatically
- use site-relative paths such as `assets/app.css`, not local absolute paths
- nested subdirectories are supported, for example `docs/getting-started.md` or `images/icons/logo.svg`
- `siteToken` is bound to one specific `site/prepare` response and should be passed to the matching `site/complete`; do not mix tokens across runs
Success response example:
```json
{
  "success": true,
  "siteId": "st_ab12cd34",
  "siteToken": "token",
  "siteHostname": "st-ab12cd34.ok26.org",
  "siteUrl": "https://st-ab12cd34.ok26.org/",
  "entryUrl": "https://st-ab12cd34.ok26.org/",
  "uploadStrategy": "reuse-file-upload-api"
}
```
### `POST /api/site/complete`
Request body:
```json
{
  "siteId": "st_ab12cd34",
  "siteToken": "token",
  "files": [
    { "relativePath": "docs/getting-started.md", "fileId": "f1a2b3c4" },
    { "relativePath": "assets/app.css", "fileId": "d4e5f6g7" },
    { "relativePath": "images/logo.png", "fileId": "h7i8j9k0" }
  ]
}
```
Success response example:
```json
{
  "success": true,
  "siteId": "st_ab12cd34",
  "siteHostname": "st-ab12cd34.ok26.org",
  "siteUrl": "https://st-ab12cd34.ok26.org/",
  "entryUrl": "https://st-ab12cd34.ok26.org/",
  "entryPath": "index.html"
}
```
## Output Strategy
Prefer returning:
- `url` for direct consumption, download, embedding, or API use
- `playUrl` for image preview, video playback, or PDF viewing
- `siteUrl` for the root of a published static site
- `entryUrl` for the preferred HTML entry page, or the same value as `siteUrl` when the site uses directory listing
For video or PDF, returning both is usually best.
## Python CLI
Use the CLI when the user wants a local command-line workflow instead of raw HTTP requests.

Recommended commands:
```bash
okfile upload photo.jpg
okfile publish ./my-site/
okfile status a3k7m92x
okfile config --key okf_xxxxx
okfile config --clear-origin
okfile --version
```

Recommended install path:
```bash
py -3 -m pip install okfile
```

Pinned install example:
```bash
py -3 -m pip install okfile==1.2.3
```

Use the CLI when:
- the user wants a copy-pasteable install command
- the user prefers local commands over direct API calls
- the workflow needs repeatable upload or publish commands on Windows
## Supported Types
- images: `JPG`, `JPEG`, `PNG`, `GIF`, `WebP`, `BMP`, `SVG`
- videos: `MP4`, `WebM`, `MOV`, `AVI`, `MKV`
- documents: `PDF`
- other common files are handled as generic files
## Limits
- max file size: `500MB`
- quick-upload path: currently advertised by `GET /api/upload/config`, typically `<= 5MB`
- files above threshold automatically use multipart upload
- anonymous mode is IP rate-limited
- API key mode is controlled by backend quotas
- parallel uploads are supported, but concurrency should be controlled by the client
## Best Practices
- call `GET /api/upload/config` before automation runs that need dynamic thresholds
- use `quick` for small files and reserve `prepare -> PUT -> complete` for larger payloads
- always follow `prepare -> PUT -> complete`
- keep the `prepare` response values (`id`, and for site publishing also `siteId` + `siteToken`) from the same execution context until `complete` finishes
- set a normal `User-Agent` on `prepare` and `complete`
- set `Content-Length` on each `PUT`
- check every part upload for `2xx` status
- retry only `missingParts`, not the whole file
- prefer stable HTTP clients for large files and multipart flows
- include `index.html` at the site root when you want the subdomain homepage to render a page immediately
- if a site is intentionally file-browsing-only, leave root `index.html` out and use the generated listing page
- do not ask the agent to create a synthetic listing `index.html`; upload the real folder tree and let OkFile render the listing automatically
- preserve nested subdirectories exactly as uploaded; published sites support paths like `/docs/guide/` and `/assets/app.css`
## Useful URLs
- home: `https://www.okfile.com/en/`
- upload page: `https://www.okfile.com/en/upload/`
- account: `https://www.okfile.com/account`
- admin: `https://www.okfile.com/admin`
- PyPI package: `https://pypi.org/project/okfile/`
- CLI wheel: `https://www.okfile.com/downloads/okfile-1.2.3-py3-none-any.whl`
- repo CLI entry: `okfile_cli/__main__.py`
