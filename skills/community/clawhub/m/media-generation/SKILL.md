---
name: media-generation
description: Generate images, edit existing images, create short videos, run inpainting/outpainting and object-focused edits, use reference images as provider inputs, batch related media jobs from a manifest, and fetch returned media from URLs/HTML/JSON/data URLs/base64. Use when working on AI image generation, AI image editing, mask-based inpainting, outpainting, reference-image workflows, short AI video generation, product-shot variations, or reusable media-production pipelines.
---

# Media Generation

Handle image generation, image editing, and short video generation through one workflow: choose the right modality, pass caller intent through to the provider, save outputs under `tmp/images/` or `tmp/videos/`, and prefer the bundled helpers over ad-hoc one-off API calls.

## Workflow decision

- If the user wants a brand-new still image, use an image-generation model.
- If the user supplies an image or wants a specific existing image changed, use an image-edit workflow.
- If the user wants motion / a clip / a short video, use a video-generation model.
- If the request includes one or more reference images, use the helper that supports reference-image transport.

## Standard workflow

1. Determine whether the task is image generation, image editing, or video generation.
2. Clarify only when required to execute the request correctly.
3. Prefer `scripts/generate_image.py` for still-image generation.
4. Prefer `scripts/edit_image.py` for direct image edits.
5. Prefer `scripts/mask_inpaint.py` for localized edits with masks or generated regions.
6. Prefer `scripts/outpaint_image.py` for canvas expansion / outpainting.
7. Prefer `scripts/reference_media.py` when reference images need to be passed through.
8. Prefer `scripts/generate_video.py` for video generation, especially when the provider may return async job payloads.
9. Prefer `scripts/generate_batch_media.py` for repeatable batch jobs, templated variations, or auditable manifests.
10. Prefer `scripts/object_select_edit.py` for simple object-vs-background edits on transparent assets or clean backdrops.
11. If the provider returns a URL, path, HTML snippet, markdown snippet, `data:` URL, or `b64_json`, use `scripts/fetch_generated_media.py`.
12. Save outputs under:
    - images → `tmp/images/`
    - videos → `tmp/videos/`
13. If the user wants files sent in chat, prefer sending the local downloaded file.
14. Keep the original remote reference as fallback when local retrieval fails.

## Prompt handling

Default to **prompt pass-through**.

- Pass the caller's prompt through unchanged.
- Use optional request fields only when the caller provides them.
- Keep prompt semantics under caller control.

Use the scripts mainly as functional helpers:
- normalize arguments
- map fields to provider-specific JSON
- upload files
- poll async jobs
- download returned media
- save outputs under `tmp/images/` or `tmp/videos/`

## Delivery rules

- Save generated or edited images in `tmp/images/`.
- Save generated videos in `tmp/videos/`.
- Never scatter generated files in the workspace root.
- If message delivery blocks remote URLs, download locally first and then send the local file.
- If a remote file cannot be fetched locally but the raw link may still help, provide the original link clearly.

## Helper quick guide

Use the smallest helper that matches the request:

- `scripts/generate_image.py` → direct still-image generation
- `scripts/edit_image.py` → direct full-image edits
- `scripts/mask_inpaint.py` → localized edits with an explicit or generated mask
- `scripts/outpaint_image.py` → canvas expansion before an edit call
- `scripts/reference_media.py` → reference-image transport and delegation
- `scripts/generate_consistent_media.py` → backward-compatible wrapper only
- `scripts/generate_batch_media.py` → repeatable manifest-driven batches
- `scripts/object_select_edit.py` → simple object-vs-background edits on transparent or clean-backdrop assets
- `scripts/generate_video.py` → direct video generation and async polling
- `scripts/fetch_generated_media.py` → normalize returned media refs into local files

Use `references/model-capabilities.md` when deciding which helper fits the modality, transport, or return shape.
Use `references/reference-image-workflow.md` for reference-image transport details.
Use `references/batch-workflows.md` for manifest structure and batch execution behavior.

Minimal examples:

```bash
python3 skills/media-generation/scripts/generate_image.py \
  --prompt 'person' \
  --size '1024x1024' \
  --out-dir 'tmp/images' \
  --prefix 'generated'

python3 skills/media-generation/scripts/edit_image.py \
  --image 'tmp/images/source.jpg' \
  --prompt 'replace the background' \
  --out-dir 'tmp/images' \
  --prefix 'edited'

python3 skills/media-generation/scripts/mask_inpaint.py \
  --image 'tmp/images/source.jpg' \
  --x 120 --y 80 --width 220 --height 180 \
  --prompt 'replace the masked area' \
  --out-dir 'tmp/images' \
  --prefix 'mask-result'

python3 skills/media-generation/scripts/outpaint_image.py \
  --image 'tmp/images/source.jpg' \
  --left 512 --right 512 --top 128 --bottom 128 \
  --mode blur \
  --prompt 'extend outward' \
  --out-dir 'tmp/images' \
  --prefix 'outpaint-result'

python3 skills/media-generation/scripts/reference_media.py \
  --mode image \
  --reference-image 'tmp/images/reference.png' \
  --prompt 'character' \
  --size '1024x1024' \
  --out-dir 'tmp/images' \
  --prefix 'reference-output'

python3 skills/media-generation/scripts/generate_batch_media.py \
  --manifest 'tmp/images/media-batch.jsonl' \
  --vars-json '{"subject":"item"}' \
  --summary-out 'tmp/images/media-batch-summary.json' \
  --continue-on-error \
  --print-json

python3 skills/media-generation/scripts/object_select_edit.py \
  --image 'tmp/images/product.png' \
  --selection-mode alpha \
  --edit-target background \
  --prompt 'replace the background' \
  --out-dir 'tmp/images' \
  --prefix 'product-bg-edit'

python3 skills/media-generation/scripts/generate_video.py \
  --prompt 'motion clip' \
  --size '720x1280' \
  --seconds 6 \
  --out-dir 'tmp/videos' \
  --prefix 'generated-video'
```

## Quick compatibility checklist

Before blaming the skill, check these first:
- config exists and is valid JSON
- `config.models.providers.<provider>` exists
- the selected provider has both `baseUrl` and `apiKey`
- the chosen endpoint actually exists on that provider
- the chosen model name is valid for that endpoint
- any provider-specific fields passed through `--extra-json` or `--extra-json-file` match that provider's schema

Defaults used by the bundled scripts:
- config path: `~/.openclaw/openclaw.json` or `$OPENCLAW_CONFIG`
- default provider: `$OPENCLAW_MEDIA_PROVIDER`, otherwise the first provider found in config
- default model names: placeholders unless overridden by env vars or `--model`
  - image → `$OPENCLAW_MEDIA_IMAGE_MODEL` or `image-model`
  - edit → `$OPENCLAW_MEDIA_EDIT_MODEL` or `image-edit-model`
  - video → `$OPENCLAW_MEDIA_VIDEO_MODEL` or `video-model`
- output root: `tmp/` or `$MEDIA_GENERATION_OUTPUT_ROOT`
- output paths are resolved relative to the current working directory unless you pass an absolute `--out-dir`

## Quick troubleshooting

Common failure patterns:
- **`provider not found`** → pass `--provider` explicitly or set `$OPENCLAW_MEDIA_PROVIDER`
- **placeholder model warning (`image-model` / `image-edit-model` / `video-model`)** → pass `--model` explicitly or set the matching `$OPENCLAW_MEDIA_*_MODEL` env var
- **`config not found` / invalid JSON** → pass `--config` explicitly or fix the OpenClaw config file
- **HTTP 404** → check `--endpoint` and video polling paths
- **HTTP 400** → check model name and provider-specific payload fields in `--extra-json` / `--extra-json-file`
- **HTTP 401/403** → check the provider `apiKey`
- **request failed before HTTP response** → check base URL, proxy/TLS, or network reachability
- **video accepted then failed later** → check request payload, provider logs, or switch provider/model

Use `--print-json` when debugging so the response body, resolved endpoint, and failure hints stay visible.

## References

Read these selectively:

- helper selection, modality fit, transport notes, return-shape handling → `references/model-capabilities.md`
- reference-image transport rules and compatibility notes → `references/reference-image-workflow.md`
- manifest format, templating, and batch execution behavior → `references/batch-workflows.md`

Primary helpers:

- image generation → `scripts/generate_image.py`
- image edit → `scripts/edit_image.py`
- mask inpaint → `scripts/mask_inpaint.py`
- outpaint → `scripts/outpaint_image.py`
- reference-image transport → `scripts/reference_media.py`
- backward-compatible wrapper → `scripts/generate_consistent_media.py`
- video generation → `scripts/generate_video.py`
- batch generation → `scripts/generate_batch_media.py`
- object-select edit → `scripts/object_select_edit.py`
- object mask prep → `scripts/prepare_object_mask.py`
- shared request utility → `scripts/media_request_common.py`
- smoke tests → `scripts/smoke_test.py`
- media retrieval → `scripts/fetch_generated_media.py`
