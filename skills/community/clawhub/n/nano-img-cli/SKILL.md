---
name: nano-img-cli
description: Drives the local nano-img Gemini image CLI for image generation, model selection, saved defaults, reference-image workflows, and output sizing or format conversion. Use when the user wants to generate images with nano-img or nano-image, inspect config or refs, set the default model or save directory, manage ~/.nano-img files, or get command-specific help for this CLI.
metadata:
  author: nano-cli-img
  version: 0.1.0
---

# Nano Img CLI

## When To Use

Use this skill when the task is specifically about the local `nano-img` or `nano-image` CLI in this repository or its home-directory defaults under `~/.nano-img`.

Package naming note:

- npm package: `nanobana`
- installed commands: `nano-img`, `nano-image`

Typical triggers:

- "generate an image with nano-img"
- "set the nano-img model"
- "save images to a default folder"
- "use the refs from ~/.nano-img/assets"
- "show what nano-img supports"
- "fix or inspect nano-img config"

Do not use this skill for general Gemini API design discussions that are not tied to this CLI.

## Execution Mode

Prefer the installed binaries when available:

- `nano-img`
- `nano-image`

If you are working inside this repo and do not want to depend on a global link, use:

- `npm run dev -- <command>`
- `npm run nano-img -- <command>`

## Core Workflow

1. Start by checking the exact command surface instead of assuming flags.
   Use `nano-img help` for global help or `nano-img <command> --help` for command help.
2. If the task is generation, inspect saved defaults first when they matter.
   Run `nano-img config --json`.
3. If the task depends on a saved model or output directory, prefer the dedicated commands over editing config by hand:
   - `nano-img model ...`
   - `nano-img save-dir ...`
4. If the task depends on reusable prompts or style, use the home-directory files:
   - `~/.nano-img/INSTRUCTION.md`
   - `~/.nano-img/STYLE.md`
   - `~/.nano-image/STYLE.md`
5. If the task uses default reference images, inspect `~/.nano-img/assets` and verify with `nano-img refs --json`.
6. After changing behavior, validate with one concrete CLI command and capture the resulting output path or config state.

## Generate Images

For generation details and command recipes, read `references/command-reference.md`.

Key rules:

- Use `generate` explicitly unless the user clearly wants the shorthand prompt form.
- Respect saved defaults from `~/.nano-img/config.json`.
- If the user passes `--save-to` or `--output`, that overrides the saved default output directory.
- Width-only or height-only requests preserve aspect ratio during local resize.
- Width plus height forces the final image to the exact requested dimensions.
- Format defaults to `png`; `jpg`, `jpeg`, and `webp` are supported through local conversion.

## Configure Defaults

For persistent settings and file layout, read `references/defaults-and-files.md`.

Prefer command-driven config changes:

- Save model: `nano-img model <name>`
- Pick model interactively: `nano-img models`
- Save default output dir: `nano-img save-dir --set "<path>"`
- Clear saved output dir: `nano-img save-dir --clear-save-dir`

Avoid editing `~/.nano-img/config.json` directly unless the user explicitly asks for a manual file edit.

## Troubleshooting

Read `references/troubleshooting.md` when:

- generation fails
- models do not list
- the picker or config looks wrong
- output paths or refs are not being used

## Validation

After making changes or guiding usage:

- run one obvious command that should succeed
- use `--json` when you need machine-readable confirmation
- report the exact saved model, output directory, or generated file path when relevant
