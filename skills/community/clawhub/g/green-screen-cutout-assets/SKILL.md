---
name: green-screen-cutout-assets
description: Generate green-screen raster subject assets with an image model and convert them into transparent PNGs with robust chroma-key cutout. Use when Codex needs pet stickers, character sprites, eggs, props, icons, collectibles, UI decorations, or other foreground image assets that must sit over app backgrounds without blocking them; includes green-screen prompt guidance, batch cutout scripting, QA reports, and contact sheets.
---

# Green Screen Cutout Assets

Use this skill for foreground bitmap assets that need transparent backgrounds. Typical targets: pets, eggs, NPCs, stickers, props, collectibles, hand-drawn UI decorations, and app/game sprites.

Do not use this skill for full scene backgrounds, photos that should remain rectangular, native SVG/vector icons, or layout-only UI work.

## Workflow

1. Decide the asset type and final size.
   - Character/pet/sticker: square, 512x512 or 1024x1024 source.
   - Egg/prop/icon: square source with generous padding.
   - Scene/background: do not use this cutout workflow; generate a normal opaque image.
2. Generate source art on a green-screen background.
   - If the system `imagegen` skill/tool is available, use it for the raster generation.
   - If no image generation tool is available, provide prompts and ask the user to generate/upload the source images.
3. Save source images under a predictable folder such as:
   - `public/assets/source-green-screen/<name>-source.png`
   - `public/assets/source-green-screen/eggs/<name>-egg-source.png`
   - or another repo-specific source folder.
4. Run `scripts/chroma_key_cutout.py` from this skill.
5. Inspect the JSON report and contact sheet before integrating assets.
6. Register final transparent PNGs in the project asset registry/manifest if one exists.

## Prompt Rules

Always ask for a plain green-screen background, but never assume the model will use exact `#00ff00`. Keep the subject isolated and avoid shadows touching the image edges.

Core prompt clause:

```text
plain solid chroma green background for cutout, isolated full body centered with generous padding, no shadow touching edges, no text, no watermark
```

Warm hand-drawn journal style clause:

```text
warm hand-drawn journal sticker style, cozy mobile app asset, soft paper texture, pastel warm colors, no hard outline
```

Avoid clause:

```text
Do not use green inside the subject unless specifically requested. Do not crop ears, tail, paws, feet, hair, fur, props, or transparent-safe edges.
```

For detailed prompt templates, read `references/prompt-cookbook.md`.

## Cutout Script

Script path:

```powershell
python C:\Users\19540\.codex\skills\green-screen-cutout-assets\scripts\chroma_key_cutout.py --help
```

Batch example:

```powershell
python C:\Users\19540\.codex\skills\green-screen-cutout-assets\scripts\chroma_key_cutout.py `
  --input-dir public/assets/source-green-screen `
  --out-dir public/assets `
  --report public/assets/cutout-report.json `
  --contact-sheet public/assets/cutout-contact-sheet.png
```

Single image example:

```powershell
python C:\Users\19540\.codex\skills\green-screen-cutout-assets\scripts\chroma_key_cutout.py `
  --input .\source.png `
  --out .\transparent.png
```

Useful options:

- `--category pets|eggs|generic|auto`: force output folder category when batch-processing.
- `--padding 24`: crop to subject alpha while retaining transparent padding.
- `--feather 1.2`: soften the alpha edge.
- `--edge-contract 1`: remove an extra pixel of green screen if source has stubborn fringes.
- `--fail-on-warning`: exit nonzero if any item has QA warnings.

The script installs `pillow` and `numpy` if missing. It estimates the key color from image borders, removes only edge-connected green regions, feathers alpha, despills green fringes, crops to content, writes a report, and builds a contact sheet on a checkerboard/matte preview.

## QA Rules

Treat a cutout as usable only when:

- report has no `processing_failed`, `corners_not_transparent`, `low_transparent_area`, `low_subject_area`, or `cropped_subject_too_small` warnings;
- contact sheet shows no visible green halo;
- ears/tail/hair/fur/paws/props are not eroded;
- transparent corners are actually transparent;
- any intentional green subject details were preserved.

If QA fails, try in this order:

1. Regenerate with stronger prompt: `no green accessories, no green reflections, no shadow touching edges, generous padding`.
2. Re-run cutout with `--edge-contract 1` for stubborn exterior fringe.
3. Lower `--feather` if fine details are being washed out.
4. Manually inspect whether internal green details are intentional before changing thresholds.

## Integration Checklist

- Store source green-screen PNGs separately from final transparent PNGs.
- Keep final asset filenames stable, e.g. `wolf.png`, not `wolf-candidate-2.png`.
- Delete rejected candidates unless the user asks to keep them.
- Update asset registries/manifests with source path, output path, prompt, cutout report values, and status.
- Run the project checks requested by the repo, usually `npm run lint` and `npm run build` for web apps.
