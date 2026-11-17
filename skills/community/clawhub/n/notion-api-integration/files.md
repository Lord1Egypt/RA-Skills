# Files, Images, and Attachments

Two ways a file can live in Notion: hosted by Notion (uploaded), or referenced by URL (external). They fail in opposite directions, and choosing wrong is discovered months later.

Recorded 2026-07. Upload endpoints and size ceilings are the most movable part of this API; verify the limits before designing a bulk migration around them.

## Hosted vs External

| | Notion-hosted (upload) | External URL |
|---|---|---|
| Where the bytes live | Notion's storage, counted against the workspace | Your host |
| The URL Notion returns | **Signed and expires in about an hour** | Exactly the URL you gave |
| Survives you | Yes | Only while your host serves it |
| Right for | User-facing documents, anything that must outlive your infrastructure | Assets you already serve, images with a stable CDN URL |

**The single most damaging habit in this area is storing the URL Notion returned.** It is a short-lived credential in URL form: it 403s within the hour, and it is a secret while it lives. Store the block or page id and refetch when you need the bytes (`memory-template.md`, Secrets).

## Attaching an External File

```json
{"Attachments": {"files": [
  {"name": "spec.pdf", "type": "external", "external": {"url": "https://cdn.example.com/spec.pdf"}}
]}}
```

```json
{"type": "image", "image": {"type": "external", "external": {"url": "https://cdn.example.com/diagram.png"}}}
```

- The URL must be publicly reachable — Notion fetches it and does not carry your auth headers. A signed S3 URL works until it expires, and then the block shows a broken image with no error anywhere.
- Writing a `files` property replaces the whole array (`properties.md`).

## Uploading a File

The flow, in three steps:

1. **Create** a file upload object (`POST /v1/file_uploads`), declaring the filename and content type. The response carries the upload id and where to send the bytes.
2. **Send** the bytes (`POST /v1/file_uploads/{id}/send`) as multipart form data. Files above the single-part ceiling are sent as numbered parts and then completed.
3. **Attach** by referencing the upload id where a file goes — a `files` property value or a `file`/`image`/`pdf` block — using the file-upload reference shape rather than an external URL.

Constraints worth knowing before you start:

- Single-part upload up to 20 MB; larger files go multi-part.
- The workspace plan caps per-file size, and free plans cap it far lower than paid ones — a migration that works on your workspace can fail on the client's.
- An upload object that is never attached expires. Attach in the same job.
- Each upload is at least two requests plus the attach — a 500-file migration is ≥1,500 requests, ≈8 minutes at 3 req/s before retries (`bulk.md`).

## Downloading a File

- Read the block or property; take the URL from `file.url`; fetch it **immediately**.
- The fetch itself does not carry the Notion auth header — the signature is in the URL. Sending your token there leaks it into someone's access log.
- Expired URL → 403. Re-retrieve the object for a fresh one; there is no refresh endpoint.
- For an export, download as you walk the tree rather than collecting URLs and fetching later. A list of URLs gathered over a 40-minute export is a list of 403s (`blocks.md`).

## Migrating Files From Another Tool

1. Enumerate the source records and their file URLs.
2. For each, download from the source, upload to Notion, attach, and record the pair in `mappings/<source>-to-notion.md` — the external record id and the resulting Notion page id, not the file URL.
3. Checkpoint per file. Re-running must skip anything already attached, which means checking the target property before uploading, not after.
4. Failures cluster on size limits and content types. Record the failing ids in the run's failure list rather than aborting the job.

**When a file migration runs**, write its counts, duration, last processed key and per-file failures to `~/Clawic/data/notion-api-integration/runs/<year>.md`, and the id pairs to `mappings/<source>-to-notion.md`, appending as you go. Never write a file URL into either.
