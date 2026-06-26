---
name: objectremover-video-object-ops
description: Remove or extract objects from videos with AI. Supports watermark/distraction removal, subject extraction with transparent background, natural-language object selection, upload-or-URL input, and end-to-end processing from input to downloadable result.
tags:
  - ai-video-editing
  - object-removal
  - object-extraction
  - watermark-removal
  - natural-language-selection
  - capcut-premiere-davinci
  - openclaw-ready
---

# ObjectRemover Video Object Ops

## Use This First

- **Single install for users:** this one skill is enough from upload to final result, including troubleshooting.
- Best for common ObjectRemover jobs: remove watermarks/distracting objects, or extract a subject for reuse in CapCut/Premiere/DaVinci.
- Supports both **chat-like natural language selection** and API-style automated processing.

## Authentication Model

This skill supports multiple authentication modes depending on deployment policy:

- Browser / guest flow:
  - No manual credential setup in most hosted deployments.
- API automation flow:
  - May use bearer-style authentication if enabled by host configuration.

- This bundle is instruction-only and does not require local install-time secret files.
- Any credential prompt and storage are controlled by the host platform.

## Service Contract

- Backend: `https://apiobjectremover.tokenlens.ai`

## Processing Flow

1. Prepare asset (upload file, URL-imported asset, or existing asset id).
2. `POST /api/processing/calculate-cost` (optional).
3. `POST /api/processing/generate-mask`
4. `POST /api/processing/start-task`
5. `GET /api/processing/task/:taskId` until terminal state.
6. Read `outputUrl` / UI when completed.

## Required Request Rules

- If using guest identity, include the guest session header on processing endpoints.
- If using authenticated API mode, use the credential mechanism provided by the host platform.
- Route processing calls to the backend domain.

## Fallback Rules

- No credits: low-trial when allowed, else checkout / top-up.
- 401 on guest flow: issue guest session first, retry with `x-guest-session-id`.
- 401 on authenticated API mode: verify credential validity and backend routing.

## When Something Breaks

- Use **[reference.md](reference.md)** troubleshooting for auth mismatch, polling stalls, and output retrieval issues.

## Additional Resources

- Full endpoint contracts and troubleshooting: [reference.md](reference.md)
