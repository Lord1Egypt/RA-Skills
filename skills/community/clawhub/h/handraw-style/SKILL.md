---
name: handraw-style
description: "261 hand-drawn style prompt catalog with numbered system — supports GPT Image, Midjourney, and other AI image generators"
version: 1.0.0
author: yang0 | Weekly Discovery
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [image-generation, prompt-engineering, art-style, drawing]
---

# Handraw Style Prompter

261 numbered hand-drawn style presets with bilingual (Chinese/English) prompts. Memorize one number to generate consistent art styles.

## Source

- GitHub: https://github.com/yang0/handraw-style
- Stars: ~973 (2026-09)
- License: MIT

## Trigger Conditions

- Need to generate images in specific art styles but don't know how to describe them
- Want to maintain visual consistency across multiple images
- Looking to explore different hand-drawn art styles
- Creating unified visual assets for social media, blogs, or videos

## Core Feature: Numbered Style System

```
Style 001: Sketchy Pencil
Style 002: Watercolor Wash
Style 003: Ink Dot Work
...
Style 261: Glitch Art
```

Just remember a number — no need to memorize style names.

## Usage

### For GPT Image
```
Prompt: "[Description], [handraw style #042]"
Example: "A cat sitting on a windowsill, handraw style #042"
```

### For Midjourney
```
Prompt: "[Description] --style raw --ar 16:9 [handraw style #128]"
```

### Batch Generation
Generate multiple images with same style number for consistent visual identity.

## Pitfalls

- **Not a tool** — this is a prompt reference, not an executable
- **Style numbering** — numbers are arbitrary; refer to the catalog for exact meanings
- **Platform differences** — style rendering varies between GPT Image, Midjourney, Stable Diffusion
- **Chinese prompts** — bilingual prompts available; use English for wider compatibility

## Verification

Test with a simple prompt:
```
"A sunset over mountains, handraw style #007"
```
Check that output matches the expected artistic style.

## References

- GitHub: https://github.com/yang0/handraw-style
- Full style catalog: See repository README
