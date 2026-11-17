---
name: pixr-cli
description: Drives the local pixr image CLI (Gemini, OpenAI-compatible, OpenRouter, fal) for generation, editing, variations, model selection, saved defaults, profile-based defaults, reference-image workflows, and output sizing or format conversion. Use when the user wants to generate or edit images with pixr, inspect config, refs, or profiles, set the default model or save directory, manage ~/.pixr files, or get command-specific help for this CLI.
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

Do not use this skill for general image-API design discussions that are not tied to this CLI.

## Providers And Models (Never Assume Either)

pixr works with `gemini` (default), `openai` (any OpenAI-compatible API), `openrouter`, and `fal`. There is no built-in model and no hardcoded capability list: the user chooses the provider and model for each task, and everything about a model comes live from the provider.

1. Pick the provider with `--provider`, `--base-url`, and `--api-key-env <ENV_VAR_NAME>` (or a profile / `commands.<name>` in config). Check `pixr config --json` for what is resolved and whether a key is loaded.
2. Find models: `pixr models --provider <p> --search "<text>" [--category image-to-image] --json`.
3. Check what a model supports before using it: `pixr models --info <model> --provider <p>` (parameters, input image limit, native mask field). Gemini and OpenAI-compatible APIs publish nothing; then requests are sent as asked.
4. Pass provider parameters with `--param name=value` (JSON values; `@file.png` becomes an image data URL). Do not invent parameter names; use the ones `--info` lists.
5. Never choose a model for the user because a task "needs" one (for example background removal or upscaling). Search the catalog, show the options, and use the one the user picks.

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
- Use `vary` for one or more variations of an existing image.
- Use `edit <image> --mask <mask.png>` to change only part of an image (white = change, black = keep, same size as the input). Make masks with `pixr mask <image> --rect x,y,w,h` (or `--ellipse`). Outpaint with `pixr extend <image> --pad ...`, which also writes the mask of the new area.
- `edit` works with any image-to-image model; the prompt is optional for models that take none.
- Local tools that need no provider or key: `pixr info`, `resize`, `crop`, `extend`, `mask`, `grid` (`grid` puts several candidates in one sheet to compare).
- For automation: `--json`, `--no-stdin`, and errors arrive as JSON on stderr with exit code 1 (2 for usage errors).
- `-w` plus `-h` stretches an image of a different shape (pixr warns); use one of them to keep the shape.
- Respect saved defaults from `~/.pixr/config.json`.
- If the user passes `--save-to` or `--output`, that overrides the saved default output directory.
- Width-only or height-only requests preserve aspect ratio during local resize.
- Width plus height forces the final image to the exact requested dimensions.
- Format defaults to `png`; `jpg`, `jpeg`, and `webp` are supported through local conversion.

### Generate Workflow (Simple and Direct)

When generating from scratch:

1. Write one clear prompt for the full scene.
2. Run `pixr generate "<prompt>"` (or `pixr gen "<prompt>"`).
3. Check the output image.
4. If changes are needed, do not keep stretching a single prompt forever.
5. Either:
   - regenerate with a clearer prompt, or
   - switch to iterative `pixr edit` passes for controlled refinements.

### Edit Workflow (Layered, Never One-Shot)

For edits, use a Photoshop-style layer mindset.

Mandatory rules:

- Never try to do the whole edit in one prompt.
- Break the task into the smallest possible edit layers.
- Run one edit layer at a time.
- Inspect the resulting image after every layer.
- Continue from the latest good output image as the next input.
- If a layer result is off, fix only that layer in the next pass.

Recommended layer order (smallest changes first):

1. Cleanup or artifact fixes.
2. Subject geometry and proportions.
3. Main object details.
4. Background elements.
5. Lighting and shadows.
6. Color grading and style polish.
7. Final upscale/resize/format conversion.

Per-layer loop:

1. Define one micro-goal (single visual change).
2. Run one `pixr edit` command focused only on that micro-goal.
3. Review the output image.
4. Accept and move forward, or retry that same layer with a tighter instruction.

Example iterative sequence:

1. `pixr edit --input in.png --prompt "Remove small background clutter only; keep subject unchanged."`
2. Check output.
3. `pixr edit --input step1.png --prompt "Adjust face proportions slightly; keep lighting and colors unchanged."`
4. Check output.
5. `pixr edit --input step2.png --prompt "Add warm rim light on subject; do not alter composition."`
6. Check output and continue.

Prefer precise constraints in edit prompts:

- "only"
- "keep unchanged"
- "do not alter composition"
- "preserve identity"
- "preserve camera angle"

## Configure Defaults

For persistent settings and file layout, read `references/defaults-and-files.md`.

Prefer command-driven config changes:

- Save model: `pixr model <name>` (list real names first with `pixr models`)
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
