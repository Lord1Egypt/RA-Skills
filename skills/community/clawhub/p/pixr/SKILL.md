---
name: pixr-cli
description: Drives the local pixr Gemini image CLI for generation, editing, variations, model selection, saved defaults, profile-based defaults, reference-image workflows, and output sizing or format conversion. Use when the user wants to generate or edit images with pixr, inspect config, refs, or profiles, set the default model or save directory, manage ~/.pixr files, or get command-specific help for this CLI.
metadata:
  author: pixr
  version: 0.1.0
---

# Pixr CLI

## When To Use

Use this skill when the task is specifically about the local `pixr` CLI in this repository or its home-directory defaults under `~/.pixr`.

Typical triggers:

- "generate an image with pixr"
- "edit an image with pixr"
- "create variations with pixr"
- "set the pixr model"
- "save images to a default folder"
- "use the refs from ~/.pixr/assets"
- "init a pixr profile"
- "make a profile use a different model or save dir"
- "show the pixr profile layout"
- "show what pixr supports"
- "fix or inspect pixr config"

Do not use this skill for general Gemini API design discussions that are not tied to this CLI.

## Execution Mode

Prefer the installed binary when available:

- `pixr`

If you are working inside this repo and do not want to depend on a global link, use:

- `npm run dev -- <command>`
- `npm run pixr -- <command>`

## Core Workflow

1. Start by checking the exact command surface instead of assuming flags.
   Use `pixr help` for global help or `pixr <command> --help` for command help.
2. If the task is generation, inspect saved defaults first when they matter.
   Run `pixr config --json`.
3. If the task depends on profile-specific defaults, inspect or scaffold them first:
   - `pixr profile list`
   - `pixr profile show <name>`
   - `pixr profile init <name>`
   - `pixr config --profile <name> --json`
4. If the task depends on a saved model or output directory, prefer the dedicated commands over editing config by hand:
   - `pixr model ...`
   - `pixr save-dir ...`
5. If the task depends on reusable prompts or style, use the home-directory files:
   - `~/.pixr/INSTRUCTION.md`
   - `~/.pixr/STYLE.md`
   - `~/.pixr/prompts/<command>.md`
   - `~/.nano-image/STYLE.md`
6. If the task uses default reference images, inspect `~/.pixr/assets` or `~/.pixr/profiles/<name>/assets` and verify with `pixr refs --json`.
   Remember that pixr keeps only the latest three default asset images by modified time.
7. After changing behavior, validate with one concrete CLI command and capture the resulting output path or config state.

## Image Workflows

For generation details and command recipes, read `references/command-reference.md`.

Key rules:

- Use `generate` or `gen` for prompt-only creation.
- Use `edit` for text-guided changes to an existing image.
- Use `vary` for one or more Gemini-generated variations of an existing image.
- Respect saved defaults from `~/.pixr/config.json`.
- If the user passes `--save-to` or `--output`, that overrides the saved default output directory.
- Width-only or height-only requests preserve aspect ratio during local resize.
- Width plus height forces the final image to the exact requested dimensions.
- Format defaults to `png`; `jpg`, `jpeg`, and `webp` are supported through local conversion.

## Configure Defaults

For persistent settings and file layout, read `references/defaults-and-files.md`.

Prefer command-driven config changes:

- Save model: `pixr model <name>`
- Pick model interactively: `pixr models`
- Save default output dir: `pixr save-dir --set "<path>"`
- Clear saved output dir: `pixr save-dir --clear-save-dir`
- Save profile defaults: `pixr profile init <name> --model ... --save-dir ...`
- Use interactive profile setup: `pixr profile init <name>`

Avoid editing `~/.pixr/config.json` directly unless the user explicitly asks for a manual file edit.

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
