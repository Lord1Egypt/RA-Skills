---
name: artifact-gallery
description: Use when an agent generates local files/folders and must return mobile-accessible OCC/Tailscale viewer links instead of filesystem paths.
version: 1.0.0
author: OCC Hermit
license: MIT
metadata:
  hermes:
    tags: [artifacts, gallery, mobile, tailscale, generated-work]
    related_skills: []
---

# Artifact Gallery

## Overview

OCC Artifact Gallery turns generated local outputs on a VPS/headless server into stable HTTPS links that users can open from Telegram, WhatsApp, Discord, or a browser.

Use this for images, PDFs, HTML, Markdown, JSON, audio, video, reports, screenshots, and generated folders. Do not give users only `/home/...` paths when they are on mobile.

## Canonical URLs

- Gallery UI: `https://n2-pro.tail1c2e65.ts.net/artifacts`
- Artifact viewer: `https://n2-pro.tail1c2e65.ts.net/artifacts/a/{artifact_id}`
- API: `http://127.0.0.1:8080/api/artifacts-gallery`

## CLI

Register a generated file:

```bash
/home/shadoprizm/occ/venv/bin/python /home/shadoprizm/occ/scripts/artifact_gallery_tool.py register \
  --path /home/shadoprizm/occ/brain/infographic-studio/active/INFOG-6311545c/infographic-v1.png \
  --title "OCC Infographic dogfood output" \
  --source-system occ \
  --source-agent concierge \
  --tags infographic dogfood
```

List recent artifacts:

```bash
/home/shadoprizm/occ/venv/bin/python /home/shadoprizm/occ/scripts/artifact_gallery_tool.py list --limit 20
```

Get links:

```bash
/home/shadoprizm/occ/venv/bin/python /home/shadoprizm/occ/scripts/artifact_gallery_tool.py links art_xxxxx
```

## Agent response contract

When replying over mobile/chat channels, include:

- brief summary
- `viewer_url`
- optional `download_url`
- artifact type/size

Example:

```text
Done — generated the report.

View:
https://n2-pro.tail1c2e65.ts.net/artifacts/a/art_xxxxx

Download:
https://n2-pro.tail1c2e65.ts.net/api/artifacts-gallery/art_xxxxx/download
```

## Safety

The gallery only serves allowlisted roots and refuses credential/dot/secret-like paths. If registration fails, do not bypass it by inventing a URL; fix the path/root or report the failure.
