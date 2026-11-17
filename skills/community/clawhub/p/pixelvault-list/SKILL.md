---
name: pixelvault-list
description: List recently uploaded images on PixelVault with their CDN URLs. Use when the user asks to "see my uploads", "find that image URL", "what images have I hosted", "list my PixelVault images", or needs the link to a previously uploaded image.
args:
  - name: options
    description: Optional flags like --json for full metadata or --per-page 50 for more results
    required: false
---

# PixelVault List

List uploaded images and their CDN URLs.

## Prerequisites

The `pixelvault` CLI must be installed and configured. If not, tell the user to run `/pixelvault-setup`.

## Steps

1. **List images**:

```bash
# Default: 20 most recent, one URL per line
pixelvault list

# With full metadata
pixelvault list --json

# Pagination
pixelvault list --page 2 --per-page 50
```

2. **Report** — Show the URLs (or metadata if `--json` was used) to the user.

## Output

- Default: one CDN URL per line to stdout
- `--json`: full response with id, url, mime_type, size, filename, folder, created_at, and pagination metadata
