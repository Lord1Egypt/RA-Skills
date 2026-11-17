---
name: pixelvault-upload
description: Upload image files to PixelVault and get a public CDN URL back. Use when the user says "screenshot this and host it", "upload this image", "host this mockup", "give me a URL for this diagram", "attach this screenshot to the PR/issue", or when you generate, render, or save an image (screenshot, diagram, chart, build artifact) that needs a shareable link. Ideal for embedding images in GitHub PRs, issues, and comments.
args:
  - name: files
    description: File path(s) or glob pattern to upload (e.g. screenshot.png, ./images/*.jpg)
    required: true
  - name: folder
    description: Optional folder to organize images in
    required: false
---

# PixelVault Upload

Upload image files to PixelVault and return CDN URLs.

## Prerequisites

The `pixelvault` CLI must be installed and configured. If the command is not found, install it:

```bash
npm install -g pixelvault-cli
```

If no API key is configured, tell the user to run `/pixelvault-setup` first or set `PIXELVAULT_API_KEY` in their environment.

## Steps

1. **Check CLI availability** — Run `which pixelvault` to confirm the CLI is installed.

2. **Check auth** — Run `pixelvault whoami --json` to verify an API key is configured. If it fails, stop and tell the user to run `/pixelvault-setup` or set `PIXELVAULT_API_KEY`.

3. **Upload** — Run the upload command:

```bash
# Single file
pixelvault upload $ARGUMENTS

# With folder
pixelvault upload <file> --folder <folder>

# Multiple files (shell glob)
pixelvault upload *.png --folder screenshots
```

4. **Report** — The CLI prints one CDN URL per line to stdout. Report these URLs back to the user. Each URL is permanent and globally cached.

## Output Contract

- The CLI prints **only URLs** to stdout (one per line)
- Human-readable messages go to stderr
- Use `--json` if you need metadata (id, mime_type, size, filename)

## Error Handling

| Error | Action |
|-------|--------|
| `command not found: pixelvault` | Tell user to `npm install -g pixelvault-cli` |
| `No API key configured` | Tell user to run `/pixelvault-setup` or set `PIXELVAULT_API_KEY` |
| `401 Unauthorized` | API key is invalid — tell user to run `pixelvault login` |
| `413 Payload Too Large` | File exceeds plan limit (5 MB free, 50 MB paid) |
| `415 Unsupported Media Type` | File is not a supported image format |

## Examples

```bash
# Upload a screenshot, get the URL
pixelvault upload screenshot.png
# → https://img.pixelvault.dev/proj_abc/img_xyz.png

# Upload with JSON metadata
pixelvault upload diagram.svg --json
# → { "id": "img_xyz", "url": "https://...", "size": 12400, ... }

# Bulk upload
pixelvault upload ./assets/*.png --folder assets
```
