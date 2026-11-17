---
name: ocas-imagine
description: 'Art-direction engine for text-to-image generation. Separates Style from Content to keep aesthetic identity consistent across an image series. Use when generating, rendering, or illustrating images (especially across a series), capturing the style of a reference image for reuse, or producing an image in a named/saved style. Not for captioning, image analysis for decisions (use ocas-look), or photo editing.'
license: MIT
source: https://github.com/<agent-handle>/imagine
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "1.1.0"
  hermes:
    category: creative
    tags:
    - image-generation
    - art-direction
    - text-to-image
    - creative
triggers:
- generate image
- text to image
- ai art
- image generation
- illustrate
---

# Imagine

Imagine is an art-direction engine that treats image generation as a two-part process: **Style Prompting** and **Content Prompting**. Decoupling aesthetic DNA from subject matter lets a series of images share one visual identity while their content varies. This separation exists because style and content have different reuse patterns — style is stable across many images while content changes per request.

## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- Create a series of images with a consistent visual identity (comics, storyboards, concept art).
- Translate a specific artistic style from a reference image into a reusable Style Prompt.
- Generate images using the current active text-to-image mode exposed by Hermes.
- Art-direct an LLM to produce a prompt that is style-pure (no content bleed).

## When NOT to Use

- Analyzing user-provided images to drive downstream decisions → use `ocas-look`
- General web research on aesthetics or art history → use `ocas-sift`
- Editing or post-processing existing images → use an image editor
- Image captioning or description → use `ocas-look`

## RULE — Read the Skill End-to-End Before Any Generation Run

Before ANY imagine run — especially the first after a gap in usage — read this SKILL.md and `references/api_reference.md` in full. Never reconstruct the methodology from memory of past runs and never guess the generation path: the skill documents the exact working procedure (current-model routing + GenTube browser bridge). If you catch yourself hand-rolling a substitute (hand-coded SVGs, a separate model, ad-hoc scripts), STOP — that is the signature of not having read the skill; fix the blocker instead. (Confirmed 2026-09-19: a banner run skipped the full read, hand-coded SVGs for ~50 turns, then found the documented path.)

## Responsibility Boundary

**Imagine does:** style library management, style extraction from reference images, art-directed prompt synthesis, image generation through the current active conversation model when that model is text-to-image capable, and journaling of every generation and extraction run.

**Imagine does not:** analyze user-provided images to drive downstream decisions (that is `ocas-look`), perform general web research on aesthetics (that is `ocas-sift`), edit/post-process existing images, call the separate `image_generate` tool, or bypass the active model by calling Pollinations/Pollination/FAL/direct provider endpoints.

Adjacent responsibility: `ocas-look` consumes images as decision inputs; Imagine produces images as creative output. If a request is "look at this image and do X with the info," route to Look; if it is "make an image that looks like this," route to Imagine.

## Optional Skill Cooperation

Imagine functions standalone. When present it may cooperate with:

- **ocas-sift** — research on a referenced artist, movement, or visual vocabulary before extraction.
- **ocas-weave** — resolving references to known people (portrait subjects) for identity context.

Imagine never depends on these skills and must run normally if they are absent.

## Journal Outputs

- **Action Journal** — emitted by `imagine.generate` and `imagine.style.save` (external HTTP side effect or persistent state write).
- **Observation Journal** — emitted by `imagine.extract` and `imagine.library.list` (analysis or read-only enumeration, no side effects).

Every run produces exactly one journal file. See `references/journal.md` for the record schema.

## Core Methodology

See `references/style_prompt_guide.md` for the full Style-Content separation methodology, the five standard style sections, and the overspecification rule.

## Operational Flows

### Flow 1: Image Generation (existing style)

Use when the user wants an image in a known or predefined style.

**Checklist:**
- [ ] Style selected from default_styles.md or styles.jsonl
- [ ] Content Prompt describes only what is in the scene (no style/color/lighting keywords)
- [ ] Final prompt = Style Prompt + Content Prompt (style first)
- [ ] API call executed successfully
- [ ] Action Journal record written with final prompt + image URL

1. **Select Style:** retrieve a style definition from `references/default_styles.md` or a previously saved Style Prompt in `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
2. **Expand Content:** turn the user's subject request into a detailed Content Prompt.
   - *Constraint:* describe what is in the scene, never how it looks (no colors, no style keywords, no lighting direction).
3. **Synthesis:** concatenate Style + Content into the final API call.
4. **Execute:** submit the synthesized prompt to the current active conversation model when it is text-to-image capable. Do not call the separate `image_generate` tool. Do not call Pollinations/Pollination, FAL, or any direct provider endpoint unless <operator> explicitly asks for that backend.
5. **Journal:** write an Action Journal record with the final synthesized prompt and the resulting image URL.

**I/O Example:**
- Input: `imagine.generate --style noir --content "a detective standing under a streetlight at night"`
- Output: `{"status": "ok", "image": "<active-mode image URL or file path>", "journal_id": "2026-06-27_abc123"}`

**Concise art-direction output schema:** Art-direction output is formatted as structured JSON containing prompt text, style weights, and negative prompts:

```json
{
  "prompt": "<Style Prompt + Content Prompt concatenated, style first>",
  "style_slug": "noir",
  "style_weights": {"mood": 0.8, "composition": 0.7, "color": 0.9, "texture": 0.6},
  "negative_prompt": "blurry, low quality, distorted, watermark",
  "content_summary": "a detective standing under a streetlight at night"
}
```

Rules: `style_weights` are normalized 0.0–1.0 relative weights per standard style section; `negative_prompt` carries the style library's default exclusions unless overridden; `prompt` is always the executable style+content concatenation (per Flow 1 step 3). Use this schema for any art-direction output consumed programmatically.

### Flow 2: Style Extraction (image → style)

Use when the user provides an image and wants to capture its soul for future use.

**Checklist:**
- [ ] Reference image loaded (path or URL)
- [ ] Multi-modal analysis completed
- [ ] Style extracted in exhaustive detail (no object/content names)
- [ ] Organized into five standard sections
- [ ] Style Test image generated and verified (no content bleed)
- [ ] Style Prompt saved to styles.jsonl
- [ ] Observation Journal record written

1. **Visual Analysis:** use a multi-modal LLM (via `vision_analyze` or equivalent) to analyze the reference image.
2. **Exhaustive Extraction:** apply the extraction prompt in `references/style_prompt_guide.md`.
   - *Requirement:* describe the style in exhaustive detail without naming any object or content.
3. **Semantic Organization:** organize the raw description into the five standard sections:
   - Perspective & Composition
   - Lighting & Shadow
   - Color Palette
   - Brushwork & Technique
   - Image Framing & Balance
4. **Verification:** generate a Style Test image of an unrelated, simple subject to confirm the prompt is robust and free of content bleed.
5. **Save:** append the resulting Style Prompt to `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
6. **Journal:** write an Observation Journal record for the extraction.

**I/O Example:**
- Input: `imagine.extract --image https://example.com/ref-photo.jpg`
- Output: `{"status": "ok", "style_name": "extracted-noir", "style_prompt": "...", "test_image_url": "...", "journal_id": "2026-06-27_def456"}`

## Commands

- `imagine.generate --style <name|prompt> --content <description>` — generate an image in a specific style.
- `imagine.extract --image <path|url>` — analyze an image and produce a structured Style Prompt.
- `imagine.library.list` — list all available predefined and saved styles.
- `imagine.style.save --name <name> --prompt <prompt>` — save a new custom style to the library.
- `imagine.journal` — read the most recent run record (final prompt + resulting image URL).

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every generation/extraction run writes an evidence record to `{agent_root}/commons/data/ocas-imagine/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: Not applicable — on-demand only.
- **Degraded mode**: When the current active conversation model cannot emit image attachments through the current surface, logs `degraded: current_model_t2i_unavailable` and returns the interface error without using fallback backends.
- **Log compaction**: Evidence and history logs older than 30 days compacted. Last 7 days retained.

## Storage Layout

```
{agent_root}/commons/data/ocas-imagine/
  config.json        # ConfigBase fields + Imagine defaults
  styles.jsonl       # Custom user-created style prompts (append-only)
  history.jsonl      # Append-only log of generation prompts and results
  intents.jsonl      # Append-only log of user intents per run
  evidence.jsonl     # Append-only evidence records (recovery contract)
{agent_root}/commons/journals/ocas-imagine/
  YYYY-MM-DD/
    {run_id}.json    # One journal file per run
```

Config follows `ConfigBase` from `spec-ocas-shared-schemas.md`. All paths use the `{agent_root}/commons/` root per `spec-ocas-storage-conventions.md`.

## Implementation Details

See `references/api_reference.md` for the current-model execution contract and failure handling.

## Background Tasks

Imagine has no operational background tasks. The universal `imagine:update` self-update cron is standard and is not enumerated here.

## Self-Update

See `references/self-update-imagine.md`.

## Visibility

Public.

## Gotchas

- **Content bleed invalidates a Style Prompt** — If a Style Prompt references specific objects, people, or scene content, it will produce inconsistent results across subjects. Always verify with a Style Test image of an unrelated, simple subject before saving.
- **On-demand only — no background tasks** — Imagine has no scheduled cron jobs or heartbeat tasks. It runs purely on invocation. A generation failure won't be retried automatically.
- **Style-content concatenation order matters** — The final API prompt must be Style Prompt first, then Content Prompt. Reversing the order causes the model to prioritize subject over aesthetics.
- **Current-model failures are terminal** — When the active conversation model cannot emit image bytes/attachments through the current surface, there is no built-in retry in the skill itself. Log degraded mode and report the interface problem. Do not route around it via `image_generate`, Pollinations/Pollination, FAL, or direct provider calls.
- **Validation triple is mandatory** — Every generation must produce entries in `history.jsonl`, a journal file, AND `evidence.jsonl`. A generation missing any of these is considered invalid per the OKR data_integrity target.
- **Skipping the full read is the #1 failure mode** — Every usage regression traces to not reading SKILL.md + `references/api_reference.md` end-to-end before generating. Read first, generate second. Hand-coded SVG substitutes for image generation are prohibited when the documented path is available.

## Error Handling

| Failure | Handling |
|---|---|
| Current model image path unavailable (interface/tooling error) | Log `degraded: current_model_t2i_unavailable` to evidence.jsonl, return the interface error to the user, and do not use fallback backends |
| vision_analyze fails on reference image | Retry once with explicit prompt asking for visual style description; if still failing, report error to user with image format requirements |
| styles.jsonl is corrupted or unreadable | Initialize fresh styles.jsonl with only built-in defaults from `references/default_styles.md`; log corruption event to evidence.jsonl |
| Content Prompt accidentally contains style keywords | Halt generation, report content bleed to user, request pure content description |
| Style Test image shows content bleed | Do NOT save the Style Prompt; report extraction failure, suggest providing a cleaner reference image |
| Journal write fails (permissions/disk) | Log failure to stderr, still return generation result to user, flag evidence record with `journal_write_failed: true` |
| Invalid image path or URL in extract command | Return error with accepted formats: local file path, http(s) URL; do not attempt download of unsupported schemes |

## Support File Map

| File | When to read |
|---|---|
| `references/style_prompt_guide.md` | During Flow 2 step 2 — when extracting style from a reference image |
| `references/default_styles.md` | During Flow 1 step 1 — before picking a style, to browse available presets |
| `references/soma.md` | When user requests or you identify a soft luminous gradient aesthetic |
| `references/noir.md` | When user requests or you identify a flat silhouette + low sun aesthetic |
| `references/hiro.md` | When user requests or you identify a woodblock print aesthetic |
| `references/comic.md` | When user requests or you identify an ink linework + warm ground aesthetic |
| `references/candy.md` | When user requests or you identify a plein-air + opaque color field aesthetic |
| `references/vaporware.md` | When user requests or you identify a retro consumer electronics aesthetic |
| `references/api_reference.md` | When executing generation; contains the current-model routing contract |
| `references/journal.md` | Before writing any journal file; contains the record schema |

## Validation Rules

- Every generation writes to both `history.jsonl` and a journal file. A generation with no journal is invalid.
- Style Prompts must not reference specific objects, people, or scene content.
- Content Prompts must not reference colors, lighting, materials, or style keywords already covered by the selected Style Prompt.
- All filesystem writes stay within `{agent_root}/commons/data/ocas-imagine/` and `{agent_root}/commons/journals/ocas-imagine/`.

## OKRs

- **schedule_adherence**: 100% — on-demand only; every invocation completes or reports error within timeout. Measured via evidence.jsonl timestamps.
- **data_integrity**: 100% — every run produces valid history.jsonl + journal + evidence.jsonl records. A run missing any record is invalid.
