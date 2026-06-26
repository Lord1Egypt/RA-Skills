---
name: hitem3d
description: Generate production-grade 3D models from images with the Hitem3D API. Use when the user wants to turn product shots, concept art, character images, portraits, or multi-view image sets into downloadable 3D assets; create printable STL files; export AR-ready GLB/USDZ; batch-convert folders of images; check Hitem3D balance/credits; or wait for and download finished task results. Supports intent-based mode selection, cost-aware defaults, multi-view vs batch routing, portrait/bust generation, quality/format control, and end-to-end submit→wait→download workflows.
metadata: {"openclaw":{"emoji":"🧊","homepage":"https://hitem3d.ai","requires":{"bins":["curl","python3","base64"],"env":["HITEM3D_AK","HITEM3D_SK"]},"primaryEnv":"HITEM3D_AK"}}
---

# Hitem3D

Use this skill to turn images into downloadable 3D models via `scripts/hitem3d.sh`.

## Use the script

Resolve all relative paths against this skill directory.

- Script: `scripts/hitem3d.sh`
- API reference: `references/api.md`
- Product guide / positioning: `references/product-guide.md`
- ClawHub-style description: `references/clawhub-description.md`
- Release checklist: `references/release-checklist.md`
- Live validation notes: `references/live-validation.md`

If the user asks for a normal one-off generation, prefer the full pipeline:
1. submit task
2. wait for completion
3. download result
4. report output path, format, model, and estimated credit cost

Do not leave the user with only a task ID unless they explicitly want async handling.

## Operator standard

Act like a production 3D operator, not a thin API wrapper.

- Infer likely intent from the request instead of asking obvious questions.
- Distinguish single-image, portrait, multi-view, and batch every time.
- Prefer finishing the workflow over handing back raw JSON.
- Surface cost, output path, format, and caveats in plain language.
- Stop early on ambiguous expensive jobs, invalid inputs, or unsafe assumptions.
- Never echo secrets, bearer tokens, or raw Authorization headers.

## Required setup

## Runtime requirements

- Binaries: `curl`, `python3`, `base64`
- Required env vars: `HITEM3D_AK`, `HITEM3D_SK`
- Optional env var: `HITEM3D_TOKEN`

The user must provide credentials through environment variables:

```bash
export HITEM3D_AK="your_access_key"
export HITEM3D_SK="your_secret_key"
```

If credentials are missing, stop and tell the user exactly which variables are not set.

## Default operating policy

When the user says “turn this image into 3D” without more detail, use these defaults:

- model: `hitem3dv2.0`
- request type: `3` (geometry + texture)
- resolution: `1536`
- format: `2` (GLB)
- face count: unset

Why: this is the best general-purpose quality/output tradeoff.

## Choose the right mode

### Single-image general object
Use when the input is one product shot, concept image, illustration, object render, furniture photo, toy, packaging, or other non-portrait asset.

Default command pattern:

```bash
scripts/hitem3d.sh run input.png
```

### Portrait / bust generation
Use portrait models when the user explicitly wants a person, face, bust, avatar head, or half-body likeness.

Preferred defaults:
- model: `scene-portraitv2.1`
- resolution: `1536pro`
- format: GLB unless user asks otherwise

Command pattern:

```bash
scripts/hitem3d.sh run face.jpg --model scene-portraitv2.1 --resolution 1536pro
```

### 3D printing
If the user mentions 3D printing, printer, slicer, or STL, prefer:
- format: `3` (STL)
- request type: `1` for mesh-only when texture is irrelevant
- optionally set higher face count for smoother geometry

Command pattern:

```bash
scripts/hitem3d.sh run object.png --format 3 --type 1 --face 500000
```

### AR / Apple preview
If the user mentions Apple AR, Quick Look, Vision Pro, AR preview, or iPhone preview, prefer format `5` (USDZ).

### Fast / cheap draft
If the user wants a rough draft, cheap test, or low-cost preview, prefer:
- model: `hitem3dv1.5`
- resolution: `512`
- type: `1` or `3` depending on whether texture matters

### Multi-view reconstruction
Use multi-view when the user provides 2-4 images of the same subject from different angles.

Use:
- `generate-multi` or `run-multi`
- pass a bitmap describing which views are present

Bitmap order is:
- front
- back
- left
- right

Examples:
- front + left = `1010`
- front + back + left + right = `1111`
- front + right = `1001`

Do not use multi-view mode for unrelated images.

### Batch processing
Use batch mode only when the user wants to process many separate images independently. Do not confuse batch with multi-view.

Batch means:
- one task per image
- submit all
- wait/download each
- return a concise summary of successes/failures and output paths

## Cost policy

Before batch jobs or obviously expensive jobs, tell the user the expected cost and ask for confirmation.

Must confirm before proceeding when either is true:
- batch job with more than 5 images
- likely cost exceeds 100 credits total
- the request implies repeated retries, alternative variants, or multiple output formats that would multiply spend

For one-off standard jobs, confirmation is not required unless the user has asked to be cost-cautious.

Reference pricing in `references/api.md`.

Practical heuristics:
- cheapest draft: `hitem3dv1.5` + `512` + mesh-only = 5 credits
- default general result: `hitem3dv2.0` + `1536` + textured = 50 credits
- premium portrait / 1536pro textured = about 70 credits

When estimating cost, say whether the number is per task or total batch cost.

## Output policy

Prefer saving downloads into a user-relevant folder under the current workspace unless the user provides a destination.

Suggested defaults:
- one-off tasks: `./output/hitem3d/`
- batch tasks: `./output/hitem3d/<batch-name>/`

When reporting completion, include:
- task ID
- final status
- saved file path
- output format
- model used
- resolution
- estimated credit cost

If the API returns a preview/cover URL, include it when useful.

## Common commands

### Check balance
```bash
scripts/hitem3d.sh balance
```

### Submit only
```bash
scripts/hitem3d.sh generate photo.png
```

### Full one-shot pipeline
```bash
scripts/hitem3d.sh run photo.png
```

For long jobs, explicitly raise the timeout instead of assuming 10 minutes is enough:

```bash
scripts/hitem3d.sh run photo.png --timeout-seconds 3600 --poll-seconds 8
```

### Full one-shot pipeline with custom options
```bash
scripts/hitem3d.sh run photo.png --model hitem3dv1.5 --resolution 1024 --format 3 --type 1 --download-dir ./output/hitem3d/
```

### Multi-view submit
```bash
scripts/hitem3d.sh generate-multi front.png left.png --views 1010
```

### Multi-view full pipeline
```bash
scripts/hitem3d.sh run-multi front.png back.png left.png right.png --views 1111 --model hitem3dv2.0 --download-dir ./output/hitem3d/multi/
```

### Long-running jobs
If a job is likely to take a while, set explicit polling and timeout values:

```bash
scripts/hitem3d.sh run-multi front.png left.png --views 1010 --timeout-seconds 3600 --poll-seconds 8
```

### Wait for an existing task and download
```bash
scripts/hitem3d.sh wait <task_id> --download ./output/hitem3d/
```

For slow tasks:

```bash
scripts/hitem3d.sh wait <task_id> --download ./output/hitem3d/ --timeout-seconds 3600 --poll-seconds 8
```

### Batch folder processing
```bash
scripts/hitem3d.sh batch ./images --glob '*.png' --download-dir ./output/hitem3d/batch/
```

## Decision rules

If the user does not specify format:
- use GLB by default
- use STL for 3D printing intent
- use USDZ for Apple AR intent

If the user does not specify model:
- use `scene-portraitv2.1` for portraits
- otherwise use `hitem3dv2.0`

If the user does not specify resolution:
- use `1536` for general work
- use `1536pro` for portrait premium output
- use `512` for cheap drafts

If the user says “highest quality”:
- general object: `hitem3dv2.0` + `1536`
- portrait: `scene-portraitv2.1` + `1536pro`
- mention expected credit usage before running

## Failure handling

### Missing credentials
Stop and ask the user to set `HITEM3D_AK` and `HITEM3D_SK`.

### Bad input images
Reject unsupported formats and files larger than 20MB before calling the API.

### Auth failure
Tell the user credentials are invalid or expired. Do not keep retrying.

### Generation failure
If API error is `50010001`, tell the user the image likely could not be parsed and credits should be refunded automatically.

### Token expiry
The script auto-fetches tokens. Retry once if a token-related request fails.

### URL expiry
If the returned download URL has expired, re-query task status to fetch a fresh URL before declaring failure.

### Multi-view mismatch
If the user labels images as multi-view but the set is missing the front view, warn that Hitem3D expects the front view and that results may fail or degrade.

## Security rules

- Never print or store AK/SK in user-visible output.
- Treat callback URLs as advanced usage; do not invent or auto-fill webhooks.
- Do not claim full production validation unless live API runs have been completed with real credentials.
- If credentials are unavailable, say the skill is design-validated but not fully live-validated.

### Download URL expiry
If the result URL expired, re-query task status to obtain a fresh result URL if available, then download again.

### Unsupported combination
Reject obviously bad combos before calling the API, especially:
- request type `2` with `hitem3dv2.0`
- multi-view without a valid 4-bit view bitmap
- face count outside 100000-2000000

## Notes for good judgment

- A user saying “folder of 30 product renders” means batch, not multi-view.
- A user sending front/back/left/right of the same object means multi-view, not batch.
- For printing intent, geometry matters more than texture.
- For showcase/demo intent, textured GLB is usually the right default.
- Prefer completing the full task over dumping raw API responses.
- Keep user-visible replies concise and outcome-focused.
