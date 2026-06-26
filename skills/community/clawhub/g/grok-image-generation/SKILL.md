---
name: grok-image-generation
description: Generate new images and edit existing images with xAI Grok Imagine from a local OpenClaw workspace. Use when the user wants Grok/xAI as the image source for prompt-based image generation, batch variations, reference-image edits, style transfer, cleanup, background replacement, product art, poster concepts, or reusable local automation around xAI image APIs.
---

# Grok Image Generation

Use the local scripts in this skill when the user specifically wants **Grok/xAI** for image generation or editing.

## Quick workflow

1. Confirm `XAI_API_KEY` exists in the local environment.
2. For new images, run `scripts/grok_imagine.py generate ...`.
3. For edits or variations from source images, run `scripts/grok_imagine.py edit ...` with one to three `--image` or `--image-url` inputs.
4. Save outputs under a task-specific folder when the user names a destination; otherwise use the default `output/grok-images/`.
5. If prompts are weak or generic, read `references/prompt-templates.md` and improve them before generating.

## Commands

Run from the skill directory or give absolute paths.

### Generate

```powershell
py -3 scripts\grok_imagine.py generate "A retro sci-fi poster with a giant moon" --aspect-ratio 2:3 --resolution 2k --n 1
```

### Batch variations

```powershell
py -3 scripts\grok_imagine.py generate "A clean premium mockup of a horror-movie T-shirt design" --n 4 --aspect-ratio 1:1
```

### Edit one source image

```powershell
py -3 scripts\grok_imagine.py edit "Turn this into a vintage pulp-poster illustration" --image C:\path\to\source.png --resolution 2k
```

### Combine multiple references

```powershell
py -3 scripts\grok_imagine.py edit "Place the subject from image one into the lighting and palette of image two" --image C:\path\subject.png --image C:\path\style.png
```

## Prompting rules

- State what must be preserved before what must change.
- For products and mockups, prioritize subject accuracy and readability.
- For T-shirt art, ask for strong silhouette, high contrast, and print-friendly detail.
- For batches, request meaningful variation in composition, angle, and lighting.
- For edits, keep the instruction narrow unless the user wants radical transformation.

Read `references/prompt-templates.md` when you need a starting prompt pattern.

## Editing and variations

Treat **variation** in three ways depending on the job:

- Same prompt, multiple fresh outputs -> use `generate` with `--n > 1`
- Same image, changed style or cleanup -> use `edit` with one source image
- Composite / transfer / merge references -> use `edit` with two or three source images

## Failure handling

- If xAI returns `403` mentioning credits, licenses, or permissions, stop and tell the user billing/access is the blocker.
- If returned image URLs are temporary, download them immediately; the script already does this.
- If xAI changes payload shape, update `scripts/grok_imagine.py` using `references/api-reference.md` plus the latest xAI docs.

## Resources

- `scripts/grok_imagine.py` - local generator/editor wrapper for xAI
- `references/prompt-templates.md` - reusable prompt skeletons
- `references/api-reference.md` - current endpoint assumptions and payload shapes
