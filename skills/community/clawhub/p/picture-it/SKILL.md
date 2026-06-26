---
name: picture-it
description: Generate and edit images from the CLI using picture-it. Use this skill whenever the user asks to create, edit, or manipulate images — blog headers, social cards, hero images, product comparisons, YouTube thumbnails, movie posters, magazine covers, Instagram edits, background removal, or any visual content. Also trigger when the user mentions picture-it by name, wants to composite images, apply color grading, add text to images, remove or replace backgrounds, crop/resize photos, or needs any kind of image generation or photo editing from the terminal. This skill covers multi-pass AI image editing workflows that chain composable operations together.
compatibility: Requires Node.js 18+ and picture-it CLI (npm package). FAL_KEY environment variable needed for AI operations. Network access to fal.ai for image generation/editing.
license: MIT
metadata:
  author: geongeorge
  version: "0.2.1"
  homepage: https://github.com/geongeorge/picture-it
  source: https://github.com/geongeorge/picture-it
  package: https://www.npmjs.com/package/picture-it
  openclaw:
    primaryEnv: FAL_KEY
    requires:
      env:
        - FAL_KEY
      bins:
        - node
        - picture-it
      config:
        - ~/.picture-it/config.json
    install:
      - kind: npm
        package: picture-it
        bins:
          - picture-it
    data-transmission: User images are uploaded to fal.ai for AI processing. See https://fal.ai/privacy for retention policy.
---

# picture-it

Photoshop for AI agents. Composable image operations from the CLI.

Source: https://github.com/geongeorge/picture-it | npm: https://www.npmjs.com/package/picture-it

## Prerequisites

picture-it must be installed and configured. Requires Node.js 18+.

```bash
# Install (pick one)
npm install -g picture-it
pnpm add -g picture-it
bun install -g picture-it

# Setup
picture-it download-fonts
```

### Credentials

The FAL API key is required for AI operations (generate, edit, remove-bg, upscale). Set it via environment variable or the CLI:

```bash
# Option 1: Environment variable (preferred — use platform-managed secrets)
export FAL_KEY=your-key-here

# Option 2: CLI config (stored in ~/.picture-it/config.json with 0600 permissions)
picture-it auth --fal <fal-api-key>
```

NEVER paste API keys into chat. Always use environment variables or the CLI auth command. Get a FAL key from https://fal.ai.

Note: User images are uploaded to fal.ai for AI processing when using generate, edit, remove-bg, or upscale commands. Local-only commands (crop, grade, grain, vignette, text, compose, template, info) do not transmit data.

## Core Concept

Every command takes an image in and outputs an image. Chain them to build anything. The agent calling picture-it IS the planner — there is no AI planner inside the tool.

## Before You Generate Anything — Think First

Image generation costs real money ($0.03–$0.15 per FAL call). A 4-pass workflow is $0.10+. Don't burn budget on a vague idea — spend time planning before running any commands.

### Step 1: Understand the purpose

Before touching picture-it, get full clarity on what the user wants. Ask yourself:

- **What is this image for?** (blog header, Instagram ad, YouTube thumbnail, product comparison, poster)
- **Who is the audience?** (developers, consumers, enterprise buyers)
- **What should someone FEEL when they see it?** (excitement, trust, urgency, curiosity)
- **What's the one message?** Every good image communicates exactly one thing.
- **Where will it be displayed?** This determines size, text sizing, and composition rules.

If any of these are unclear, ask the user before proceeding. A 30-second question saves $0.15 in wasted generation.

### Step 2: Plan the composition

Think through at least 3 different approaches before picking one. Consider:

- **Can this be done without FAL?** Templates and Satori compose are free. A solid gradient + good typography is often enough.
- **What's the minimum number of FAL calls?** Each call costs money. Plan the fewest passes that achieve the goal.
- **Which technique fits?** Text-behind-subject for thumbnails, remove-bg + compose for product photos, multi-pass for cinematic scenes.

Present your top 2-3 ideas to the user briefly — one sentence each — and let them pick before generating. Example:

> "Here are a few directions:
> 1. Dramatic product shot — generate a dark stage, edit to place your logo as a glowing 3D object ($0.07)
> 2. Clean comparison — remove-bg from both products, compose on gradient with text ($0.01)
> 3. Text-behind-subject — generate an action scene, edit to weave the title behind the subject ($0.07)
>
> Which direction, or a mix?"

### Step 3: Plan the pipeline

Before running the first command, write out the full pipeline:

```
1. generate (flux-dev $0.03) — dark stage scene
2. edit (seedream $0.04) — place logo into scene
3. compose (free) — add text overlay
4. grade + vignette (free) — post-process
Total: ~$0.07
```

This avoids discovering mid-way that you need a different approach and wasting the earlier calls.

## Commands Quick Reference

| Command | What it does | Needs FAL? |
|---|---|---|
| `generate` | Create image from text prompt | Yes |
| `edit` | Edit image(s) with AI | Yes |
| `remove-bg` | Remove background | Yes |
| `replace-bg` | Remove bg + generate new one | Yes |
| `crop` | Resize/crop to exact dimensions | No |
| `grade` | Apply color grading | No |
| `grain` | Add film grain | No |
| `vignette` | Add edge darkening | No |
| `text` | Render text onto image (Satori) | No |
| `compose` | Overlay images/text/shapes from JSON | No |
| `template` | Built-in templates (no AI) | No |
| `info` | Analyze image dimensions/colors | No |

## Model Selection

Choose the right model for the job — don't overspend.

**Generation (no input images):**
- `flux-schnell` ($0.003) — Default. Fast, good quality. Use for backgrounds and base scenes.
- `flux-dev` ($0.03) — Better quality. Use for hero images, portraits, detailed scenes where quality matters.

**Editing (with input images):**
- `seedream` ($0.04) — Default. Good for compositing multiple images, placing objects in scenes, adding text. Handles up to 10 inputs.
- `banana2` ($0.08) — Better image preservation. Use when you need the input image to stay more faithful, or >10 inputs.
- `banana-pro` ($0.15) — Best quality, best text rendering. Use for premium work, complex edits, character consistency.

**Background removal:**
- `bria` (default) — Best edge quality, clean cutouts
- `birefnet` — Good general purpose
- `pixelcut` — Alternative
- `rembg` — Cheapest

## How to Write Good Prompts

This is the difference between mediocre and professional output. Read `references/prompt-library.md` for a full library of tested prompts you can copy and adapt. Key rules:

**For generation:** Be specific about lighting ("dramatic side lighting from upper right"), camera ("shot on Canon R5 70-200mm f2.8"), and atmosphere ("dust particles visible in the light beam"). Vague prompts produce generic results.

**For text-behind-subject:** The key phrase is: *"Add '[TEXT]' in large bold [color] letters BEHIND the [subject] — the [subject's] body overlaps and partially covers the letters."* Without "BEHIND" and the occlusion instruction, the text floats on top.

**For edits:** Always end with *"Keep everything else exactly the same"* and list what to preserve. Without this, the AI changes things you didn't want changed.

**For background replacement:** Use realistic, specific locations ("modern upscale mall entrance during daytime, natural warm daylight"). Over-dramatic backgrounds ("city at night with neon reflections") look obviously fake.

## Typography

**For big titles and hero text:** Use the FAL model via `edit` — it handles large text well and integrates it into the scene naturally. No font size math needed, just say "very large bold" in the prompt.

**For precise small text** (credits, URLs, badges, coverlines): Use `compose` or `text` with Satori. This is where font sizing matters — images display much smaller on phones. Quick rule: on a 1080px Instagram image, nothing under 36px is readable. Run `picture-it download-fonts` first if fonts aren't installed.

**Hierarchy:** Max 3 text sizes per image. Brand name should be larger than tagline.

**Font pairing:** Serif + sans-serif works best. For FAL model text, just describe the style in the prompt. For Satori, 3 fonts are bundled — drop more `.ttf` files into `~/.picture-it/fonts/`. Run `picture-it download-fonts` if fonts aren't installed. See `references/composition-guide.md` for pairing suggestions.

## Composition Techniques

Read `references/composition-guide.md` for detailed multi-pass workflows, product photography, magazine covers, and overlay composition.

## Common Workflows

### Simple: Generate an image

```bash
picture-it generate --prompt "dark cosmic background with nebula" --size 1200x630 -o bg.png
```

### Simple: Add text to an image

```bash
picture-it text -i bg.png --title "Hello World" --font "Space Grotesk" --color white --font-size 64 -o hero.png
```

### Medium: Blog header with AI background + text

```bash
picture-it generate --prompt "abstract dark tech background" --size 1200x630 -o bg.png
picture-it text -i bg.png --title "My Blog Post" --font "DM Serif Display" --font-size 72 -o header.png
picture-it grade -i header.png --name cinematic -o header-graded.png
```

### Medium: Edit a photo background

```bash
picture-it edit -i photo.jpg --prompt "replace background with modern hotel entrance, keep subject identical" --model banana-pro -o edited.jpg
```

### Advanced: Text behind subject (YouTube thumbnail style)

```bash
# 1. Generate a scene
picture-it generate --prompt "runner on mountain trail at golden hour" --model flux-dev --size 1280x720 -o runner.png

# 2. Use FAL edit to add text BEHIND the subject
picture-it edit -i runner.png --prompt "Add 'RUN FASTER' in large bold black letters BEHIND the runner — the runner's body overlaps the text" --model seedream -o thumbnail.png
```

### Advanced: Product comparison with real photos

```bash
# 1. Remove backgrounds from product photos
picture-it remove-bg -i product-a.png --model bria -o a-cutout.png
picture-it remove-bg -i product-b.png --model bria -o b-cutout.png

# 2. Generate a background
picture-it generate --prompt "split gradient, blue left to orange right" --size 1200x630 -o bg.png

# 3. Compose cutouts onto background with text
picture-it compose -i bg.png --overlays overlays.json -o comparison.png
```

### Advanced: Multi-pass cinematic composition

```bash
# 1. Generate base scene
picture-it generate --prompt "dark stage with green spotlight" --model flux-dev --size 2048x1080 -o stage.png

# 2. Edit scene to place objects
picture-it edit -i stage.png -i logo.png --prompt "Place Figure 2 as glowing 3D cube in the spotlight" --model seedream -o composed.png

# 3. Post-process
picture-it crop -i composed.png --size 1200x630 --position attention -o cropped.png
picture-it grade -i cropped.png --name cinematic -o graded.png
picture-it vignette -i graded.png --opacity 0.3 -o final.png
```

## Platform Presets

Use `--platform <name>` with `generate` or `crop`:

| Preset | Size |
|---|---|
| `blog-featured` | 1200x630 |
| `og-image` | 1200x630 |
| `youtube-thumbnail` | 1280x720 |
| `instagram-square` | 1080x1080 |
| `instagram-story` | 1080x1920 |
| `twitter-header` | 1500x500 |

## Output Behavior

- **stdout**: only the output file path
- **stderr**: progress logs
- **Exit 0** on success, **Exit 1** on failure

Read stdout to get the file path. This is how you chain commands.

## Gotchas

- Always use `--model bria` for `remove-bg` — the default birefnet leaves rectangular artifacts that cause ugly glow/shadow halos when compositing.
- The `glow` effect in compose mode blurs the entire rectangular buffer, not the shape. Avoid using glow on cutout images — use the background color/lighting to create the glow effect instead.
- The `shadow` effect has the same rectangular artifact issue. For cutout images on clean backgrounds, skip shadows entirely.
- When editing with FAL, the model may alter product details (logos, text, design elements). For product images where accuracy matters, use `remove-bg` + `compose` instead of `edit` to preserve the original exactly.
- SeedDream takes ~60 seconds per generation. Don't assume it failed if it's slow.
- For `edit` with banana-pro, don't pass `resolution` or `limit_generations` params — it auto-detects.
- Always `crop` to exact dimensions after FAL generation — FAL models output approximate sizes.
- Use `flux-dev` ($0.03) not `flux-schnell` ($0.003) when image quality matters (hero images, portraits). The quality difference is significant.
- Satori does NOT support: display:grid, transforms, animations, box-shadow, filters. Use flexbox only.
- When adding text behind a subject with `edit`, be very explicit in the prompt: "the text is BEHIND the subject — the subject's body overlaps and partially covers the letters."
