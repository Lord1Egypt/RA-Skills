---
name: r2-proxy
description: "Upload and manage files through Polsia's Cloudflare R2 proxy with authenticated API requests."
---

# R2 Proxy - File Storage

Upload and manage files using Polsia's R2 storage proxy. Files are stored in Cloudflare R2 with automatic CDN delivery.

## Base URL

https://polsia.com/api/proxy/r2

## Authentication

All requests require the POLSIA_API_KEY header. Use Authorization: Bearer process.env.POLSIA_API_KEY

## Upload a File

Endpoint: POST /upload, Content-Type: multipart/form-data

Use node-fetch (not native fetch) for uploads. Use form-data package and pass formData.getHeaders() to avoid missing boundary errors.

## Response Format

Returns: success, file.id, file.key, file.url, file.filename, file.mime_type, file.size, file.created_at

## Allowed File Types

Images: jpeg, png, gif, webp. Videos: mp4, webm, mov. Audio: mp3, wav, ogg. Documents: pdf, docx, xlsx, txt, csv.

## Size Limits

Images: 20MB, Videos: 1GB, Audio: 500MB, Documents: 50MB.
