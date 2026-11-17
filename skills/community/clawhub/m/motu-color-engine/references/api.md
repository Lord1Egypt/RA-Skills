# MotuArt Color Engine — API reference

Base URL: `$MCE_API_BASE` (default `https://mce.motu.art`).
Auth: create a key at `https://mce.motu.art/account` (English: `/en/account`), then send
`X-API-Key: $MCE_API_KEY` (or `Authorization: Bearer $MCE_API_KEY`) on private and
processing endpoints. `/v1/health` and public Headshots discovery endpoints do not need
a key. The full key is displayed once; store it securely and rotate or revoke it from
the account page if exposed.

Scopes:
- `catalog:read` — styles, crop specs and approved outfits.
- `portrait:process` — process, smooth and mask.
- `id-photo:process` — crop, id-pack, id-check, optimize and print-sheet.
- `outfit:process` — standalone outfit replacement. Also required in addition to
  `id-photo:process` or `portrait:process` when those requests include `outfit_id`.
- `headshot:process` — private AI Headshots projects, reference preparation,
  generation, candidates, post-processing, and exports. See `headshots-api.md`.

Successful processing calls consume account credits; catalog requests do not. A `402`
response uses `detail.code="insufficient_credits"` and includes `required`, `available`,
and whether the request included outfit replacement.

## GET /v1/health
Liveness/version. No key required.

## GET /v1/styles
Returns `{ styles: [{id, name, kind, name_zh, ...}], composite_separator, bases, flavours }`.
`kind` is `base` or `flavour`. Combine as `<flavour><composite_separator><base>`
(default separator `@`), e.g. `kodak_gold@motu_korean_id`.

## POST /v1/process  (multipart/form-data)
Grade an image. Fields:
- `file` (required) — image upload (JPG/PNG/WebP, ≤ ~15 MB).
- `style` — style id (default `motu_korean_id`).
- `strength` — look intensity, default `1.0` (0–~1.5).
- `smooth_strength` — optional M15 pro skin smoothing, `0`–`1`. Omitted/`0` leaves skin
  texture untouched (default). Softens pores/blemishes only; never reshapes the face.
- `smooth_texture_retain` — optional, `0`–`1` (default `0.35`), how much natural
  texture to keep on top of the smoothing. Only used when `smooth_strength` > 0.
- `portrait_lighting_style` — optional M17 light-sculpting preset:
  `natural_dimension`, `soft_luminous`, or `studio_definition`. Omit it and all
  `portrait_lighting_*` fields to keep the existing grading output unchanged.
- `portrait_lighting_strength` — optional `0`–`1`; omitted uses the selected preset's
  calibrated strength. Supplying this without a style uses `natural_dimension`.
- `portrait_lighting_face_light_balance`, `portrait_lighting_subject_separation`,
  `portrait_lighting_local_contrast`, `portrait_lighting_skin_protection`, and
  `portrait_lighting_highlight_protection` — optional advanced overrides, each `0`–`1`.
- `output_format` — `png` (default) | `jpeg` | `webp`.
- `quality` — 1–100 for lossy formats (default 90).
- `max_long_edge` — cap working long edge (default 1024; server ceiling applies).
- `mask` — `true` to also return a mask inline (base64).
- `mask_kind` — mask type when `mask=true` (see below).
- `crop_spec` — optional M16 purpose crop spec id (see `GET /v1/crop/specs`). When set,
  the graded output is additionally cropped to that spec (grade + crop in one call).
  Omitted — full graded frame, uncropped.
- `pad_color` — optional `#RRGGBB` padding when the source lacks the spec's required
  margin; only used with `crop_spec`. Omitted — edge-replicate padding (the default).
- `bg_color` — optional background replacement (换底), only used with `crop_spec`: a
  palette name the spec allows (e.g. `white`/`blue`/`red`), `default` for the spec's
  standard color, or an explicit `#RRGGBB`. Omitted — original background kept.

Response JSON:
```
{ "trace_id", "style_id", "image_base64", "content_type",
  "processing_time_ms", "quality": { "skin_delta_e_to_target", "warnings" },
  "report_url", "compare_base64",
  "mask_base64", "mask_kind", "mask_content_type" }   // mask_* only when mask=true
```
Decode `image_base64` to bytes to get the graded image. `skin_delta_e_to_target`
is the skin ΔE to the target skin (lower = closer).
When portrait lighting is enabled, `GET report_url` includes a `portrait_lighting`
metrics object describing the applied preset, strength, EV guard, and before/after
subject-separation measurements.

## POST /v1/mask  (multipart/form-data)
Segmentation only (decode + parse; **skips grading/render/score** — faster). Fields:
- `file` (required).
- `mask_kind` — `skin` (default) | `valid_skin` | `face` | `person`.
- `max_long_edge` — optional.

Returns the mask as a raw **grayscale PNG** (`Content-Type: image/png`), with header
`X-MCE-Mask-Kind`. Save the response body directly.

## POST /v1/smooth  (multipart/form-data)
Standalone M15 pro skin smoothing — runs decode + parse + smoothing + render only,
**skipping the entire color-grading stack**. Softens pores/blemishes on the detected
skin region; never reshapes the face or changes color. Fields:
- `file` (required).
- `strength` — smoothing amount, default `0.6`.
- `texture_retain` — how much natural texture to keep, default `0.35`.
- `radius_frac` — optional blur radius override (fraction of face size).
- `output_format` — `png` (default) | `jpeg` | `webp`.
- `quality` — 1–100 for lossy formats (default 90).

Returns the smoothed image as a raw payload (default `image/png`), like `/v1/mask`.

## POST /v1/portrait-lighting  (multipart/form-data)
Standalone deterministic portrait light sculpting. Runs decode + human parse + M17 +
render only, preserving identity, geometry, image content, and the existing light
direction. Fields:

- `file` (required).
- `style` — `natural_dimension` (default), `soft_luminous`, or `studio_definition`.
- `strength` — optional `0`–`1`; omitted uses the selected style's calibrated default.
- `face_light_balance`, `subject_separation`, `local_contrast`, `skin_protection`,
  `highlight_protection` — optional advanced overrides, each `0`–`1`.
- `max_long_edge` — optional working-resolution cap.
- `output_format` — `png` (default), `jpeg`, or `webp`.
- `quality` — 1–100 for lossy formats.

Returns the processed image as a raw payload. `X-MCE-Trace-Id` identifies the request;
`X-MCE-Lighting-Info` contains the applied style, strength, maximum EV adjustment,
subject-separation measurements, and warnings.

Local CLI equivalent:

```bash
mce run --input portrait.jpg --output lit.png --portrait-lighting-only \
  --lighting-style natural_dimension --lighting-strength 0.70
```

## GET /v1/crop/specs
List the available purpose-crop specs (证件照/形象照/头像 standards). Returns
`{ specs: [{id, name, name_zh, category, width_px, height_px, width_mm, height_mm,
dpi, head_ratio, bg_colors, default_bg, description_zh}] }`.
- `category` — `id_photo` | `portrait` | `avatar`.
- `width_mm`/`height_mm`/`dpi` — physical print size; `null` for portrait/avatar specs
  (pixel-only, no print standard).
- `bg_colors` — `{name: "#RRGGBB"}` palette the spec allows for background
  replacement; `{}` when the spec does not standardize a background (most
  portrait/avatar specs). `default_bg` is the palette name applied when a caller
  requests `bg_color="default"`.
- See `references/crop-specs.md` for a curated overview of the shipped specs.

## POST /v1/crop  (multipart/form-data)
Standalone M16 purpose-crop. Runs decode + face/head geometry + crop **only** — no
human parsing, no color grading (use `/v1/process` with `crop_spec` to grade and crop
together). Fields:
- `file` (required) — image upload (JPG/PNG/WebP, ≤ ~15 MB).
- `spec` — crop spec id (default `one_inch`); see `GET /v1/crop/specs`.
- `pad_color` — optional `#RRGGBB` padding when the source lacks the spec's required
  margin. Omitted — edge-replicate padding.
- `bg_color` — optional background replacement (换底): a palette name the spec
  allows, `default` for the spec's standard color, or an explicit `#RRGGBB`. Omitted —
  original background kept.
- `max_long_edge` — optional working-resolution cap; `0`/omitted means **full source
  resolution** (crop quality is bounded by source resolution, not a latency budget —
  unlike `/v1/process`, which defaults to 1024).
- `output_format` — `png` (default) | `jpeg` | `webp`.
- `quality` — 1–100 for lossy formats (default 90).

Returns the cropped image as a raw payload (default `image/png`, with the spec's DPI
embedded), like `/v1/mask`/`/v1/smooth`. The achieved geometry and any warnings are in
the `X-MCE-Crop-Info` response header (JSON), alongside `X-MCE-Trace-Id`.

## POST /v1/id-pack  (multipart/form-data)
Generate a complete ID-photo delivery package. The service creates one graded/smoothed
master, detects face/head geometry once, then crops multiple specs from that master.
Fields:
- `file` (required) — image upload.
- `specs` (required) — comma-separated crop spec ids, e.g. `passport_cn,one_inch`.
- `style` — style id (default `motu_korean_id`).
- `smooth_strength`, `smooth_texture_retain` — optional skin smoothing.
- `strength`, `output_space`, `max_long_edge` — same meaning as `/v1/process`.
- `bg_color` — `default` (recommended for ID photos), palette name, or `#RRGGBB`.
- `pad_color` — optional padding colour.
- `output_format` — `png` (default) | `jpeg` | `webp` for single-spec files.
- `quality` — output quality for lossy formats.
- `upload` — `true` to include upload-optimized files using spec `upload` rules.
- `print_sheet` — optional paper id such as `6x4`/`a4`; groups same-size photos.

Response JSON includes `trace_id`, `style_id`, `master_base64`, `items[]` with
`image_base64`, `crop_info`, `compliance`, optional `upload.image_base64`, optional
`print_sheets[].image_base64`, and the master quality report.

Optional outfit fields:
- `outfit_id` — approved id returned by `GET /v1/outfits`; omitted keeps the original clothing.
- `outfit_long_edge` — upstream generation long edge, bounded to 512–2048; default 1536.

## GET /v1/outfits
Returns the approved outfit catalog. Each item includes `id`, localized names and
descriptions, `category` (`male`/`female`/`kids`/`unisex`), `order`, `available`, and
optional `preview_url`. `available` mirrors the catalog's `enabled` switch. The
controlled `generation_prompt` used by the workflow is never exposed.

## POST /v1/outfit  (multipart/form-data)
Controlled standalone clothing replacement. Fields:
- `file` (required) — source JPG, PNG, or WebP.
- `outfit_id` (required) — approved catalog id. Custom prompts and arbitrary ids are rejected.
- `long_edge` — requested generation long edge, bounded to 512–2048; default 1536.

Response JSON contains `task_id`, `outfit_id`, `image_base64`, `content_type`,
`long_edge`, and `processing_time_ms`. MCE resolves the id to its controlled
`generation_prompt`, then submits the source, prompt, face mask, and long edge to the
configured asynchronous Motu workflow and polls it.

## POST /v1/id-check  (multipart/form-data)
Check an ID photo against a crop spec. Fields:
- `file` (required) — source portrait, or already-cropped ID photo when `report_json` is supplied.
- `spec` (required) — crop spec id.
- `report_json` — optional crop report containing `metrics.crop`; use this when checking an already-cropped output.
- `bg_color` — optional background for the temporary crop-check path (default `default`).

Response JSON: `{ ok, status, checks, warnings, errors }`. This is practical QA, not
a government acceptance guarantee.

## POST /v1/optimize  (multipart/form-data)
Export an upload-ready file. Fields:
- `file` (required).
- `output_format` — `jpg`/`jpeg` (default), `png`, or `webp`.
- `max_kb` — optional maximum file size in KB.
- `quality`, `min_quality` — lossy encoder quality range.
- `resize` — optional `WIDTHxHEIGHT`.
- `dpi` — optional DPI metadata.

Returns the optimized image as a raw payload. Metadata is in `X-MCE-Export-Info`.

## POST /v1/print-sheet  (multipart/form-data)
Layout one or more same-size ID photos on paper. Fields:
- `files` — one or more image uploads.
- `paper` — `6x4` (default), `4x6`, `5x7`, `7x5`, `a4`, or `WIDTHxHEIGHTin`.
- `dpi`, `margin_mm`, `gap_mm`, `cut_lines`, `output_format`.

Returns the print sheet as a raw image payload. Metadata is in `X-MCE-Print-Sheet-Info`.

## Errors
- `400` bad params / empty upload · `401` missing/invalid key ·
  `413` too large · `415` unsupported content-type · `422` processing/segmentation failed.
Error bodies are JSON `{ "detail": "..." }`.
