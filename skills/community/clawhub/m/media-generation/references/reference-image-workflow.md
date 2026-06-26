# Reference-Image Workflow

Use this reference for reference-image transport behavior and provider compatibility.

## Purpose

Pass one or more reference images through to a provider without changing caller prompt text.

## Helper

Primary helper:
- `scripts/reference_media.py`

Backward-compatible wrapper:
- `scripts/generate_consistent_media.py`

This helper:
- accepts one or more `--reference-image` inputs
- in image mode, can encode them as data URLs
- in image mode, can attach them under a configurable JSON field
- can delegate execution to `generate_image.py` or `generate_video.py`
- in image mode, can retry without provider-json reference payloads when transport mode is `auto`

## Core arguments

- `--reference-image` repeatable reference image path
- `--reference-key` JSON field name for encoded reference images in image mode
- `--transport auto|none|provider-json` for image-mode provider-json handling; video mode ignores it
- `--mode image|video`

## Transport modes

### `provider-json`
- Encode reference images
- Attach them in request JSON under `reference_key`
- Use when provider schema accepts encoded reference-image fields
- Applies to image mode only

### `auto`
- In image mode, try provider-json transport first
- In image mode, if that request fails, retry without provider-json references
- In video mode, skip provider-json reference transport and use `input_reference` directly

### `none`
- In image mode, do not attach provider-json reference payloads
- In video mode, behavior is unchanged because video already uses multipart `input_reference`
- Still allow the delegated script to receive a direct `--input-reference` argument when applicable

## Video path behavior

When `--mode video` and at least one reference image is present:
- the first reference image is passed to `generate_video.py` via `--input-reference`
- `generate_video.py` uploads that file as multipart/form-data
- the delegated video request uses only the `input_reference` file field

## Common compatibility issues

Check these first:
- image mode provider rejects large encoded payloads
- image mode provider expects a different reference-image field name
- provider accepts direct image fields but not `reference_images`
- video mode expects multipart file upload, not JSON data URLs
- provider accepts video image input only in one specific field

## Data handling notes

- Reference images are read from local paths.
- In image mode, encoded payloads may be written to a temporary JSON file when the inline JSON would be too large.
- In video mode, the first reference image is uploaded directly as a multipart file field.
- Temporary JSON files are deleted after execution.
