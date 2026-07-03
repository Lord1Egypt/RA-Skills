---
name: hiapi-video-prompt-generator
description: Turn a brief, link, or research topic into a controlled, source-grounded video prompt that runs on HiAPI Seedance 2.0 or HappyHorse 1.0. Use when a user asks to direct, plan, or storyboard a video before generation.
metadata:
  short-description: Direct controlled video prompts for HiAPI Seedance 2.0 and HappyHorse 1.0
---

# HiAPI Video Prompt Generator

Before using this skill, run the update check once per session (it skips silently when offline; set `HIAPI_SKIP_UPDATE_CHECK=1` to disable):

```bash
node scripts/check-update.mjs
```

If it reports a required update, run the printed install command before continuing. If it reports an available update, tell the user and continue.

Use this skill when the user has a video idea, a product link, a research topic, or a brief, and needs a **strong, executable video prompt** before calling a video model.

This skill does not generate video. It produces a structured prompt that the user can paste into:

- `hiapi-seedance-2-0-video-skill` — high-quality text-to-video and image-to-video.
- `hiapi-happyhorse-1-0-video-skill` — lightweight text-to-video drafts.

The output is built so each fact, command, and UI label survives the trip to the model.

## When To Use This Skill

Use this skill when any of these are true:

- The user describes a video they want, but the brief is one or two sentences.
- The user gives a URL, GitHub repo, or document and asks for "a video about this".
- The user wants a product demo, teaching short, social short, explainer, or pitch.
- The user has a draft prompt that is vague, generic, or missing screen text and motion.

Skip this skill and route directly to the model skill when the user already has a final prompt and only wants to generate.

## Defaults

- **Duration**: `5` seconds. Never default to `30` — HiAPI's video models do not run that length.
- **Aspect**: `16:9` for horizontal demos and explainers, `9:16` for social shorts and vertical product teasers.
- **Scene count**: at micro-cut granularity (Seedance 2.0) — 4 blocks at `5` s, 5 at `8` s, 6 at `10` s, and up to 8 blocks at `15` s. At macro-beat granularity (HappyHorse 1.0) — 2 beats at `3` s, 3 beats at `5` s, 4 beats at `8` s, 5 beats at `10` s, 6 beats at `15` s. Either way the Output Contract still returns one block per scene.
- **Resolution**: Seedance 2.0 defaults to `720p`, downgrades to `480p` for fast drafts. HappyHorse 1.0 defaults to `1080p`, downgrades to `720p` when speed or cost matters; do not output `480p` for HappyHorse.
- **Language**: Match the user's language. Keep product names, commands, and UI labels in their original casing.

The supported parameter sets are **model-specific**. This skill must pick a target first, then constrain duration and aspect to that target's list.

### Seedance 2.0 (`hiapi-seedance-2-0-video`)

- **Durations** (seconds): any integer from `4` to `15`.
- **Resolutions**: `480p`, `720p`, `1080p`.
- **Ratios** (flag `--ratio`): `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `adaptive`.
- **Media modes**: text-to-video; first-frame image-to-video; first+last-frame image-to-video; multimodal references.
- **Mutual exclusion**: do not mix first/last-frame fields with `reference_image_urls`, `reference_video_urls`, or `reference_audio_urls`.
- **Reference limits**: reference images plus first/last frames <= 9 images; reference videos <= 3, each 2-15 s and total <= 15 s; reference audio <= 3, each 2-15 s and total <= 15 s.

### HappyHorse 1.0 (`hiapi-happyhorse-1-0-video`)

- **Durations** (seconds): any integer from `3` to `15`.
- **Resolutions**: `720p`, `1080p`.
- **Sizes** (flag `--size`, not `--ratio`): `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. No `21:9`.
- **Seed**: optional integer `0` to `2147483647`; include only when the user asks for reproducibility.
- **Input**: text-to-video only. No image input.

## Workflow

1. **Read the request.** Classify it: product demo, teaching short, social short, explainer, pitch, historical, or visual concept.
2. **Pick the target model.** Default to `hiapi-seedance-2-0-video` for image-to-video, cinematic feel, or anything over `5` seconds. Use `hiapi-happyhorse-1-0-video` for a fast text-to-video draft.
3. **Gather sources.** Use materials the user supplied first. If they are insufficient, research:
   - Official product site, docs, GitHub repo, release notes.
   - Primary sources for the topic (papers, organization sites, official archives).
   - Reputable English-language background coverage if needed.
   - Avoid sources the user did not ask for if they would dilute or contradict the brief.
4. **Extract visualizable facts.** See `references/source-extraction.md`. Pull names, commands, UI labels, numbers, differentiators, visual hooks, and what the product should never claim.
5. **Pick a pattern.** See `references/prompt-patterns.md`. Adapt the pattern to the chosen duration and aspect ratio.
6. **Write the prompt** following the Output Contract below. Each fact, command, and UI label must show up either on screen, in narration, or in a labeled visual cue.
7. **Verify the constraints.** Confirm the duration is in the chosen target's allowed list (Seedance: any integer from `4` to `15`; HappyHorse: any integer from `3` to `15`). Confirm the aspect value matches the right flag for that target (`--ratio` for Seedance, `--size` for HappyHorse) and is in its allowed list. For Seedance, choose exactly one media mode: first-frame, first+last-frame, or multimodal references. Confirm reference image/video/audio limits before writing a handoff command. Confirm screen text is short enough to render. Confirm nothing in the prompt fabricates a feature.
8. **Hand off.** See `references/hiapi-handoff.md`. Show the user the exact `node scripts/...` command for the chosen HiAPI skill so they can run it next.

## Output Contract

Return all of the following sections, in this order, in the user's language. Keep section headers in the user's language too.

1. **Video Type** — one of: product demo, teaching short, social short, explainer, pitch, historical, visual concept.
2. **Target Model** — `hiapi-seedance-2-0-video` or `hiapi-happyhorse-1-0-video`, with one reason.
3. **Duration And Aspect** — pick from the chosen target's allowed list above. Seedance: any integer from `4` to `15` seconds and one of `16:9|9:16|1:1|4:3|3:4|21:9|adaptive`. HappyHorse: any integer from `3` to `15` seconds and one of `16:9|9:16|1:1|4:3|3:4`. State which flag the target uses (`--ratio` for Seedance, `--size` for HappyHorse).
4. **Core Objective** — one sentence: what the viewer should remember at the end.
5. **Source Extraction Summary** — five to ten bullet facts, each tagged `[source]` if pulled from a real source, or `[creative assumption]` if invented for staging. Never tag a guess as a source.
6. **Narrative Through-Line** — one sentence: the story arc from frame one to the last frame.
7. **Scene Prompts** — one block per scene. Each block has:
   - `Time` (e.g. `0.0s–1.2s`)
   - `Visual` — what is on screen
   - `On-Screen Text` — exact strings, in quotes, short enough for the duration
   - `Action / Camera` — one dominant motion and one secondary ambient motion
   - `Narration` — one short line, or `(none)`
   - `Transition` — to the next scene
8. **Required Screen Text** — a deduplicated list of every quoted on-screen string. Preserve command syntax and tag text exactly.
9. **Motion And Camera Control** — list the dominant motions (typing, click, zoom, pan, dolly, reveal). Avoid particle effects unless the brief is artistic.
10. **Style Requirements** — color, lighting, typography, density, mood. One paragraph.
11. **Negative Constraints** — what the model must not show. Always include: no fabricated features, no logos the brief did not authorize, no on-screen text outside Required Screen Text.
12. **Final Copy-Ready Prompt** — a compact block suitable for `--prompt`. It MUST keep the scene order with short time cues (e.g. `[0–1.2s]`), every Required Screen Text string verbatim, the dominant motions, and at least one Negative Constraint. A flat description that drops these cues is wrong.
13. **Handoff Command** — the exact `node scripts/...` command for the chosen HiAPI skill, with duration, resolution, media mode, and the right ratio flag (`--ratio` for Seedance, `--size` for HappyHorse) pre-filled. Prefix with the working directory the user must `cd` into first (the installed target skill directory).

## Quality Bar

A strong output is **directed**, not described. It tells the model what appears, what moves, what is typed, what is heard, what is grounded in the source, and what must not appear. If a fact in the Source Extraction Summary does not show up either on screen, in narration, or as a labeled visual cue, drop the fact or add a scene.

Do not fabricate facts. Product names, metrics, commands, UI labels, version numbers, testimonials, and feature claims must come from the brief or a cited source. Only **staging choices** — camera, layout, lighting, generic visual treatment, transition copy — may be tagged `[creative assumption]` when no source pins them. A missing fact is a question for the user, not a license to invent.

## Routing And Adjacent Skills

- For a **still image starting frame** before image-to-video, route to [awesome-gpt-image-2-prompts](https://github.com/HiAPIAI/awesome-gpt-image-2-prompts) for image prompts, then [hiapi-gpt-image-2-skill](https://github.com/HiAPIAI/hiapi-gpt-image-2-skill) to render it.
- For a **library of proven video prompts** to anchor on, see [awesome-seedance-2-0-prompts](https://github.com/HiAPIAI/awesome-seedance-2-0-prompts).
- For **broader model discovery**, see [hiapi-skills](https://github.com/HiAPIAI/hiapi-skills) or the Remote MCP at `https://mcp.hiapi.ai/mcp`.

## Examples

```text
$hiapi-video-prompt-generator Turn https://github.com/HiAPIAI/hiapi-skills into a 5-second product intro.
```

```text
$hiapi-video-prompt-generator Make a 9:16 social short about why agent skills beat one-shot prompts.
```

```text
$hiapi-video-prompt-generator Plan an 8-second image-to-video starting from outputs/product.png, soft camera, studio lighting.
```

## Important Links

- HiAPI Seedance 2.0 video skill: https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
- HiAPI HappyHorse 1.0 video skill: https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- HiAPI docs: https://docs.hiapi.ai
