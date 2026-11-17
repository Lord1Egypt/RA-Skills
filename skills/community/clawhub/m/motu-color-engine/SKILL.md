---
name: motu-color-engine
description: AI portrait grading, skin-tone correction, identity-preserving smoothing, mask export, approved clothing replacement, professional AI Headshots generation, and ID/passport/headshot/avatar production through the MotuArt Color Engine HTTP API. Use for retouching portraits, normalizing skin tone, exporting mattes, replacing clothing, preparing identity references and generating professional headshot candidates, cropping to ID/passport/visa specs, replacing ID-photo backgrounds, checking compliance, optimizing uploads, or creating print sheets. Triggers include portrait grading, skin tone, retouch, skin mask, outfit replacement, AI headshots, professional headshot, business portrait, corporate portrait, LinkedIn photo, ID photo, passport photo, visa photo, background swap, print sheet, 调色, 肤色, 磨皮, 蒙版, 人像调色, AI形象照, 职业形象照, 商务形象照, 企业头像, 换装, 证件照, 裁剪, 换底, 合规检查, 排版, 一寸, 二寸.
---

# Motu Color Engine

Use Motu Color Engine to process portrait images through the hosted HTTP API. Prefer the bundled scripts in `scripts/` over hand-written `curl` calls unless the user explicitly needs raw API details.

The engine preserves identity. Do not describe it as slimming, reshaping, face swapping, or changing facial structure. Skin smoothing only softens pores and blemishes inside detected skin regions. Cropping repositions and pads to a spec; it never stretches or compresses the face.

## Setup

- Require `curl` and `python3`.
- Read `MCE_API_BASE` from the environment; default is `https://mce.motu.art`.
- Read `MCE_API_KEY` from the environment; send it only as `X-API-Key`.
- If the key is missing, direct the user to `https://mce.motu.art/account` (English: `/en/account`) to sign in by email and create one. Ask them to export it securely in their own environment; do not ask them to paste the full key into chat.
- Never hard-code, print, log, commit, or expose API keys in browser/client code. The full key is shown once and can be rotated or revoked from the account page.
- Request only the scopes needed: `catalog:read` for portrait/ID discovery, `portrait:process` for grading/smoothing/masks, `id-photo:process` for ID-photo workflows, `outfit:process` for outfit replacement, and `headshot:process` for private AI Headshots projects and generation. An ID package with an outfit needs both `id-photo:process` and `outfit:process`.
- Processing calls consume account credits; catalog discovery does not. Surface `402 insufficient_credits` instead of retrying.
- Check service health with `curl -sS "${MCE_API_BASE:-https://mce.motu.art}/v1/health"` when diagnosing connectivity.

## Choose The Workflow

- Use `scripts/grade.sh` when the user wants color grading, skin-tone correction, a film/commercial look, or grading plus optional crop.
- Use `scripts/smooth.sh` when the user wants smoothing only with no color or white-balance change.
- Use `scripts/portrait-lighting.sh` when the user wants visibly more dimensional portrait lighting, a brighter facial plane, readable dark clothing, or a focused background without changing identity or geometry.
- Use `scripts/mask.sh` when the user wants a skin, valid-skin, face, or person mask/matte.
- Use `scripts/crop.sh` when the user wants crop-only ID/passport/visa/headshot/avatar output, optionally with a solid background color.
- Use `scripts/outfit.sh` when the user wants clothing replacement only. The outfit id must come from the approved catalog; never accept or invent a custom prompt or outfit id.
- Use `scripts/outfits.sh` before clothing replacement to discover currently enabled outfit ids. Do not infer an id from a garment name.
- Use `scripts/id-pack.sh` when the user wants a complete ID/passport photo delivery package: one graded/smoothed master, multiple specs, upload-ready files, compliance report, and optional print sheets.
- Use `scripts/id-check.sh` when the user wants to validate an ID photo against a spec or understand compliance warnings.
- Use `scripts/optimize.sh` when the user needs a website/upload-ready file with format, pixel size, DPI, or maximum KB constraints.
- Use `scripts/print-sheet.sh` when the user wants cropped ID photos laid out on photo paper for printing.
- Use `scripts/headshots.sh` when the user wants AI-generated professional, business, corporate, LinkedIn, or studio headshots. Keep reference preparation, confirmation, generation, candidate download, post-processing, and export as explicit stages; do not turn them into one automatic operation.
- Use the Headshots person-reference library when the user wants to reuse a previously confirmed person. Distinguish starting a new project from applying that person to an existing project, and never delete existing projects when removing a library entry.
- Use `scripts/styles.sh` to discover live style ids. Read `references/styles.md` only when the user needs style-selection guidance or offline context.
- Use `scripts/crop-specs.sh` to discover live crop specs. Read `references/crop-specs.md` only when choosing specs or background palettes without live discovery.
- Read `references/api.md` for endpoint parameters, response fields, headers, limits, and error codes.
- Read `references/headshots-api.md` before operating the AI Headshots workflow or when the user needs its raw API details.

## Grade Portraits

```bash
scripts/grade.sh <input-image> <output-image> [style-id] [strength] [smooth-strength] [smooth-texture-retain] [crop-spec] [bg-color] [pad-color] [lighting-style] [lighting-strength]
```

- Omit `style-id` for the default skin base, or choose a style from `scripts/styles.sh`.
- Use `strength` for look intensity; default is `1.0`, `0` disables the look, and values up to about `1.5` are stronger.
- Pass `smooth-strength` from `0` to `1` only when the user asks for softened pores or blemishes. Omit it, or pass `0`, to preserve natural texture.
- Use `smooth-texture-retain` from `0` to `1` to keep natural texture over smoothing; default is `0.35`.
- Pass `crop-spec` when the same output should be graded and cropped in one API call.
- Pass `bg-color` only with `crop-spec`; use an allowed palette name such as `white`, `blue`, or `red`, `default`, or explicit `#RRGGBB`.
- Pass `pad-color` only with `crop-spec` when a specific padding color is needed; otherwise let the API edge-replicate.
- Pass `lighting-style` only when the same output should also receive portrait light sculpting; choose `natural_dimension`, `soft_luminous`, or `studio_definition`. Omit it to preserve the existing grading result.
- Use `lighting-strength` from `0` to `1` to override that preset's calibrated strength.
- Report `skin_dE` from script output when summarizing quality; lower means closer skin color to the target.

For a folder, run the script once per image. Keep batch loops serial unless the user asks for parallelism and accepts API/load implications.

## Smooth Skin Only

```bash
scripts/smooth.sh <input-image> <output.png> [strength] [texture-retain]
```

- Use this for pore/blemish softening without style, color, or white-balance changes.
- Default `strength` is `0.6`.
- Default `texture-retain` is `0.35`; raise it to preserve more natural texture.

## Sculpt Portrait Lighting

```bash
scripts/portrait-lighting.sh <input-image> <output.png> [style] [strength]
```

- Styles are `natural_dimension` (default), `soft_luminous`, and `studio_definition`.
- Omit `strength` to use the calibrated default for the selected style; otherwise use `0`–`1`.
- `soft_luminous` prioritizes a luminous face and open dark midtones; `natural_dimension` balances face, wardrobe and background; `studio_definition` adds the strongest background focus and local definition.
- The operation reshapes luminance relationships only. It never moves facial features, changes face/body geometry, or regenerates image content.
- Use it independently after another editor, or as an explicit post-process after the user selects a Headshots candidate once that integration is available.

## Export Masks

```bash
scripts/mask.sh <input-image> <output.png> [mask-kind]
```

- Use `skin` by default.
- Other mask kinds are `valid_skin`, `face`, and `person`.
- Output is an 8-bit grayscale PNG aligned to the input.

## Crop ID Or Portrait Photos

```bash
scripts/crop.sh <input-image> <output-image> [spec-id] [bg-color] [pad-color]
```

- Default `spec-id` is `one_inch`.
- Use `scripts/crop-specs.sh` to list supported specs and allowed background colors.
- Use `bg-color` only when the spec declares a background palette, mostly ID-photo specs.
- Use `pad-color` only when a source image lacks required margins and the user wants a specific fill.
- Surface crop warnings from script output, especially warnings about margins, resolution, or background limitations.
- Use `grade.sh` with crop arguments when the user wants grading and crop in one output.

## Make ID Photo Packages

```bash
scripts/id-pack.sh <input-image> <output-dir> [specs] [style-id] [smooth-strength] [bg-color] [upload] [print-sheet] [outfit-id] [outfit-long-edge]
```

- Use this for passport/visa/ID-photo deliverables rather than calling `grade.sh` once per spec. The API generates one graded/smoothed master first, then crops multiple specs from that master so colour and retouching stay consistent.
- `specs` is comma-separated, e.g. `passport_cn,one_inch,us_visa`; default is `passport_cn`. School/enrollment specs include `shanghai_compulsory_education_cn`, `college_graduation_image_cn`, and `national_k12_student_status_cn`.
- Default style is `motu_business_neutral`; pass `smooth-strength` from `0` to `1` only when the user asks for smoothing.
- `bg-color` defaults to `default`, which applies each spec's standard background palette. Use `white`, `blue`, `light_blue`, `red`, or `#RRGGBB` when the user asks and the spec allows it.
- `upload` defaults to `true`, writing upload-optimized JPG files using the spec's `upload` rules from `crop_specs.json`.
- `print-sheet` is optional, e.g. `6x4` or `a4`; when specs have different sizes, separate sheets may be generated.
- `outfit-id` is optional. When present, it must be an id returned by `scripts/outfits.sh`; omitted keeps the original clothing.
- `outfit-long-edge` controls the upstream outfit result size, defaults to 1536, and is bounded by the service to 512–2048px.
- Output folder contains `master.png`, `single/`, `upload/`, `print/`, and `report.json`. Surface compliance status and warnings from the report.
- When the user requests a supported outfit, pass its approved catalog id. Outfit replacement runs before the corrected master is generated, so all crop specs share the same clothing result.

## Replace Clothing Only

Discover the approved catalog first:

```bash
scripts/outfits.sh
```

Select only an id returned by that command, then replace clothing:

```bash
scripts/outfit.sh <input-image> <output.png> <approved-outfit-id> [long-edge]
```

- Only use ids returned by `GET /v1/outfits`; the API maps each approved id to its controlled generation prompt and rejects custom prompts or arbitrary ids.
- The catalog groups styles as `male`, `female`, `kids`, or `unisex`; use the category and localized name/description to help select a suitable style.
- If the requested clothing is absent, explain that only catalog styles are available; do not substitute a custom prompt, URL, or upload.
- The service protects the detected facial oval with the face mask and calls the configured Motu asynchronous workflow.
- Default output long edge is 1536px; the service bounds requests to 512–2048px.
- Clothing generation must preserve the face and identity. Report upstream failures or timeouts instead of silently returning the original image.

## Create AI Headshots

Use one work directory for the whole staged workflow. The script stores non-secret ids,
responses, and configuration in `headshots.json`; it never stores `MCE_API_KEY`.

Discover current options:

```bash
scripts/headshots.sh catalog [locale]
```

List reusable confirmed people:

```bash
scripts/headshots.sh people [limit]
```

Prepare a graded, optionally smoothed, purpose-cropped identity reference:

```bash
scripts/headshots.sh prepare <input-image> <work-dir> \
  [--scene ID] [--garment male|female] [--skin-base ID] [--smoothing 0..1] \
  [--crop-spec ID] [--crop-anchor auto|center|manual] \
  [--crop-rect X,Y,W,H] [--rotation DEG]
```

- Inspect `source-check.json` and `reference-preview.png` before continuing.
- Surface ineligible reasons and warnings. Do not submit generation for an ineligible source.
- `skin-base` performs colour/skin-tone preparation; `smoothing=0` preserves natural texture.
- Use an automatic crop unless the user provides a complete normalized manual rectangle.
- Never confirm the reference without the user approving the preview.

After approval, freeze that preview as the identity reference:

```bash
scripts/headshots.sh confirm <work-dir>
```

Confirmation automatically adds the approved person to the account library, deduplicated
by the confirmed reference image. To start a separate project from a saved person, or switch
the active person inside an existing project while preserving its history:

```bash
scripts/headshots.sh start-person <person-reference-id> <new-work-dir> [--scene ID]
scripts/headshots.sh use-person <existing-work-dir> <person-reference-id>
```

`use-person` appends a new immutable reference to the same project. Existing jobs, candidates,
favorites, and prior references remain available. Removing a person is a library-only soft delete:

```bash
scripts/headshots.sh remove-person <person-reference-id>
```

Submit a compatible generation plan without waiting for the asynchronous worker:

```bash
scripts/headshots.sh generate <work-dir> [--scene ID] [--batch-size 1|2|4] \
  [--style ID] [--pose ID] [--outfit ID] [--background ID] \
  [--ratio 1:1|4:5|3:4] [--framing auto|close_up|half_body|three_quarter]
```

- Let the recommendation endpoint fill omitted options and correct incompatible defaults.
- Use only ids returned by the live Headshots catalog. Never send custom generation prompts.
- Generation consumes credits per requested image. Surface `402` and do not retry unchanged.
- The command submits one job and returns; it does not hide asynchronous work behind a long synchronous call.

Check and download results explicitly:

```bash
scripts/headshots.sh status <work-dir>
scripts/headshots.sh download <work-dir>
```

Download after the job is `completed` or `partially_completed`. For a partial result, surface the
failure reason and download every ready candidate rather than discarding successful outputs.

Post-process a user-selected candidate and optionally export that render:

```bash
scripts/headshots.sh render <work-dir> --candidate ID-or-ordinal --style ID [--locale LOCALE]
scripts/headshots.sh light <work-dir> --candidate ID-or-ordinal [--style ID] [--strength 0..1] [--render]
scripts/headshots.sh export <work-dir> --candidate ID-or-ordinal [--render] \
  [--crop SPEC] [--format jpeg|png|webp] [--quality 70..100]
```

- Require an explicit candidate id or ordinal.
- `light` without `--render` creates an immutable lighting Render from the Candidate master. With `--render`, it uses the latest saved Render as its source, allowing an explicit grade → light chain without overwriting either version.
- Without `--render`, export the generated master candidate. With `--render`, use the latest explicit render saved in the work directory.
- Keep `project_id`, `reference_id`, `job_id`, and derivative ids so an interrupted workflow can resume.

## Check ID Photo Compliance

```bash
scripts/id-check.sh <input-image> [spec-id] [report-json]
```

- Without `report-json`, the input is treated as a source portrait: the API crop-checks it against the spec and reports practical compliance.
- With `report-json`, the input is treated as the already-cropped ID photo and the supplied crop metrics are checked.
- Report failures and warnings plainly; this is a practical QA check, not a government guarantee.

## Optimize Upload Files

```bash
scripts/optimize.sh <input-image> <output-image> [format] [max-kb] [quality] [resize] [dpi]
```

- Use for official website upload limits such as JPG under a maximum KB, exact pixel dimensions, or DPI metadata.
- `format` is `jpg`, `png`, or `webp`; `resize` is `WIDTHxHEIGHT`; lossy formats search quality down to the server default floor when `max-kb` is set.

## Make Print Sheets

```bash
scripts/print-sheet.sh <output-image> <paper> <input1> [input2 ...]
```

- Use after generating cropped ID photos when the user wants a printable sheet.
- `paper` supports common values such as `6x4`, `4x6`, `5x7`, and `a4`. Inputs on a single sheet must have the same pixel size; use `id-pack.sh` for automatic grouping by size.

## Constraints To Surface

- Upload limit is about 15 MB per image.
- Supported upload formats are JPG, PNG, and WebP.
- Portrait, crop, and ID-photo processing calls are synchronous. Headshots generation is asynchronous and must be polled by job id.
- Background replacement is limited to specs that declare `bg_colors`.
- If a script fails, read its HTTP status and error detail before deciding whether to retry, change arguments, or ask the user for configuration.
