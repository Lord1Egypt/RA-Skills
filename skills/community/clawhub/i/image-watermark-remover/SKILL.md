---
name: image watermark remover
slug: image-watermark-remover
version: 1.0.0
description: Remove image watermarks with the Nowatermark.info API, request polling, request_id resume, and public image URL validation.
homepage: https://nowatermark.info
metadata: {"openclaw":{"homepage":"https://nowatermark.info","requires":{"env":["NOWATERMARK_API_KEY"]},"primaryEnv":"NOWATERMARK_API_KEY"}}
---

# Image Watermark Remover

Remove watermarks from public image URLs through the Nowatermark.info API.

## When to Use

Use this skill when the user wants to remove a watermark from an image they are authorized to edit, resume an existing `request_id`, or check the status of a prior cleanup job.

## Quick Reference

| Topic | File |
|-------|------|
| API key setup, input rules, and commands | `setup.md` |
| Endpoints, payloads, responses, and error codes | `references/api.md` |
| Submit-and-poll helper script | `scripts/remove_watermark.py` |

## External Endpoints

| Method | Endpoint | Purpose | Data sent |
|--------|----------|---------|-----------|
| `POST` | `https://nowatermark.info/api/image/remove-watermark` | Submit watermark-removal job | `file_url` |
| `POST` | `https://nowatermark.info/api/jobs/query` | Query job status | `request_id` |

## Data Storage

Do not create, download, or overwrite local files unless the user asks first.
Ask the user before saving API responses or downloading the cleaned image.

## Security & Privacy

- Ask the user to confirm they are allowed to edit the image when ownership or permission is unclear.
- Tell the user that the public image URL is sent to `nowatermark.info` for processing.
- Request the API key through environment or skill settings; do not expose `NOWATERMARK_API_KEY` in logs or replies.
- Prefer public image URLs over local file handling to minimize local data movement.

## Core Rules

1. If ownership or permission is unclear, ask the user to confirm they are allowed to edit the image before sending requests.
2. Verify `NOWATERMARK_API_KEY` is available before sending requests.
3. Require a direct public image URL; reject local paths, page URLs, and expiring signed URLs.
4. Prefer `scripts/remove_watermark.py` for submit-plus-poll workflows.
5. Poll every 3-5 seconds until `completed` or `failed`, then return the final `url` or the failure details.
6. Reuse a supplied `request_id` for status checks instead of creating a duplicate job.
