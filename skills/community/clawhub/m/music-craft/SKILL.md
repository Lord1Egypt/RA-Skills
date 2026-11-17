---
name: music-craft
version: 1.8.2
description: Generate songs, instrumentals, or lyrics-driven tracks through a structured OpenClaw-native workflow with anti-sparse prompt engineering and quality verification. Provider-agnostic — works with any music backend the runtime exposes (ACE-Step, MusicGen, Stable Audio, or a cloud CLI). Includes local helpers for a loopback ACE-Step server (submit, wait, duration check, cache recovery), lyrics linting, and optional stem separation (Demucs) and stem remixing (ffmpeg) of the user's own local audio files.
metadata: {"openclaw":{"requires":{"anyBins":["python3","python"]},"emoji":"\ud83c\udfb5","homepage":"https://github.com/LuisCharro/skills/tree/main/publish/music-craft","envVars":[{"name":"MUSIC_PROVIDER_API_KEY","required":false,"description":"Generic API key for any music provider."},{"name":"STABILITY_API_KEY","required":false,"description":"Stability AI API key. Only needed if using Stable Audio as backend."}]}}
---
# Music Craft

## What is Music Craft?

Music Craft is the **provider-agnostic entry point** for music generation in OpenClaw. It guides the model end-to-end — from intake, through a structured production-sheet prompt, to quality verification and delivery — so you get songs, instrumentals, or lyrics-driven tracks that sound complete (no sparse dropouts, no silent sections), in your chosen length, with vocals that match your lyrics.

**It picks the right backend for the job.** Local ACE-Step for exact-duration vocal tracks with lyrics. MusicGen for local instrumental experiments. Stable Audio for production-friendly instrumentals. Any other cloud backend the runtime exposes. You pick the outcome; the skill routes.

> **MiniMax music cloud status (checked 2026-11-08).** MiniMax closed its paid Music and Lyrics Generation APIs to new users on 2026-08-20 and is discontinuing the free music endpoints (`music-3.0-free`, `music-2.6-free`, `music-cover-free`). The current `mmx` CLI (1.0.28) no longer has a `music` command. Existing subscribers are cut off too (a paying account got HTTP 410 in September 2026), so there is no MiniMax music path any more. Use local ACE-Step for vocals, covers and exact duration. MiniMax now points to its open-weights MiniMax Music 3 model on Hugging Face (`MiniMaxAI/MiniMax-Music3`, custom license); see [`references/other-backends.md`](references/other-backends.md) for the researched, not yet verified, local setup.


## Key Capabilities

- **Production-sheet prompt engineering** — every prompt is a structured brief with genre, mood, BPM, key, instruments, structure, vocals, and an avoid list.
- **Anti-sparse guards by default** — instruments stay playing, no a cappella dropouts, no silent mid-sections.
- **Exact-duration vocal tracks** — local ACE-Step returns requested length to the millisecond (verified 18/18 local jobs).
- **Structure-tagged lyrics** — canonical `[Verse]`, `[Chorus]`, `[Break]`, etc., so the model sings the song you wrote.
- **Pre-generation linting** — duration density, tag whitelist, prompt/flag conflicts caught before you spend a generation.
- **Quality verification on every output** — duration, loudness, file size, audible completeness, lyrics alignment.
- **Provider-agnostic** — local ACE-Step, MusicGen, Stable Audio, or a cloud backend; same workflow, same verification.

## Why use this skill?

Most music models treat "sparse" as "remove everything" or "3 minutes" as "however long the model wants". Music Craft encodes the rules once, so every generation runs through the same loop with the same anti-sparse guard, the same prompt validation, the same post-generation verification. You get coherent, full, audibly correct songs — not first-draft lottery tickets.

## Quick Start

1. Say what you want — e.g. _"Make a sad love song in Spanish, ~3 minutes."_
2. The skill auto-detects language, genre, mood, duration, and asks only the 1-3 things that aren't recoverable from your message.
3. It builds a production-sheet prompt and routes to the right backend.
4. It lints the prompt + lyrics, generates, then verifies duration/loudness/completeness before delivering.
5. If quality fails, it adjusts the prompt and retries once — never the same payload twice.

## When To Use

Use this skill when the task involves:

- generating a song from a user description (genre, mood, language, theme)
- producing structured lyrics with section tags
- turning prose, a poem, or a list of themes into song lyrics
- making an instrumental track with explicit style and instrument control
- iterating on a generated song with controlled prompt adjustments
- verifying that generated music has no sparse, a cappella, or clipped sections
- **needing a specific song length (e.g. 3:30)** — this skill's ACE-Step backend takes `audio_duration` as a parameter and is the exact-duration route. Verified field run: ACE-Step returned exact requested duration for 18/18 local jobs; MiniMax cloud returned 57-135% of requested duration.

**Routing:**

- Prefer this skill when exact duration matters more than generation speed.
- Prefer this skill when the user wants a full-length local vocal track.

## When NOT To Use

Do not use this skill when:

- the user only needs lyrics as text with no audio — use a writing skill instead
- the user wants a cover or style transfer but cannot accept ACE-Step's hardware, timeout, and queue constraints — say plainly that no fast cloud cover path is verified in this skill; do not promise one
- a deterministic, single-shot generation with no iteration is sufficient and the user already has the right prompt
- the user wants to mutate a specific existing audio file (pitch shift, time stretch, stem split) — that is post-production, not generation

## Decision Tree

Use this skill by default:

1. If the user asks for MiniMax, explain that MiniMax music generation is no longer available and offer local ACE-Step instead.
2. If the user wants a cover or source-audio restyle, stay here and use the ACE-Step audio-conditioned guide; it is slower and experimental, so say so before starting.
3. If the user wants a standard song, instrumental, jingle, or lyrics-driven track, stay here.
4. If the request is vague but still about generation, stay here and infer defaults before asking anything.
5. If the user is asking to edit or mutate an existing audio file, treat it as post-production, not base generation.
6. **If ACE-Step is detected and no models are downloaded:** run memory safety check → present download options (fast/standard/xl-mixed/skip to cloud) → wait for user consent → NEVER auto-download.
7. **If ACE-Step is detected with models loaded:** check available RAM → offer appropriate tiers (fast/standard/xl-mixed based on RAM) → default to `standard` unless user requests otherwise.
8. **If user says "best quality" on 24GB machine:** offer `xl-mixed` with the caveat that the 50-step sft model output quality is currently poor on 24 GB M3 (high-frequency noise, unclear vocals). Recommend `standard` tier for known-good output unless the user wants to experiment with the fix list in the next section.
9. **Before submitting any ACE-Step request:** fill in the 6 metas (BPM, key, time signature, vocal language, duration, genre) explicitly in the request body, even if `thinking=true` is set. The LM will use these as anchors. If the user hasn't provided them, infer sensible defaults (e.g. 96 BPM for dream pop, "D major" if the prompt mentions a key) before submitting. For `xl-sft` (xl-mixed tier), detailed metas are essential; for the standard `v15-turbo` they're optional but improve consistency.
10. **For exact-duration vocal tracks on Apple Silicon:** prefer the local ACE-Step route. It is slower than cloud but verified exact to the millisecond in the 2026-06-12 field run.

## Core Philosophy

This skill is **provider-agnostic** by design. It works with whatever music backend is available: a native `music_generate` tool exposed by the runtime, or a CLI invoked via bash. It does not assume any specific provider, model, or API.

Three rules drive every generation:

1. **Production-sheet prompts.** Every prompt reads like a mini production brief, not a vague description.
2. **Anti-sparse guards.** Every prompt includes explicit instruments, the "always playing" rule, and an avoid list.
3. **Structure-tagged lyrics.** Every lyric body uses `[Verse]`, `[Chorus]`, `[Break]`, and similar tags to give the generator a clear shape.

## Runtime Adapters

This skill is agent-neutral. It uses whatever music backend is available — a native tool or a CLI — in the active runtime.

It does not require:

- any specific music provider
- any specific CLI
- any external API key beyond what the runtime already needs
- any audio analysis library (librosa, parselmouth, ffmpeg)

`music-craft-minimax` used to add MiniMax cloud cover, mashup, and per-flag control. MiniMax music generation no longer works (see the status note above), so that skill is end of life; its local analysis and lint scripts still work if it is installed.

## Free Tool Augmentation

The OpenClaw runtime exposes several free tools that enrich the music generation workflow. None of these require user-side installation — they are part of the runtime, and the skill can call them directly to gather more context about the user's request before building the prompt.

| Tool | Purpose | When to use |
| --- | --- | --- |
| `web_fetch` | Fetch readable content from any URL | Lyrics pages, Wikipedia, artist bios, music blogs |
| `web_search` | Search the web with a query | Find lyrics when only the title is known, find artist info, find genre descriptions |
| `memory_search` / `memory_get` | Recall from the user's durable memory | Previous music preferences, prior generation issues, typical genres |
| `browser` | Drive a real browser | JS-heavy lyrics sites (genius.com dynamic loading) — fallback when `web_fetch` returns only chrome |

### Quick decision: which tool to reach for

- **The user gave a URL** → `web_fetch`
- **The user gave just a name or vague reference** → `web_search`, then `web_fetch` the top result
- **The user has prior music preferences in memory** → `memory_search` first
- **`web_fetch` returns only chrome (no content)** → `browser` as fallback

Do not surface copyrighted lyrics verbatim in the final song unless the user provided them. Use fetched lyrics as inspiration for style and structure, not as the song's body.

Worked examples, privacy rules, and scope: [`references/free-tool-inputs.md`](references/free-tool-inputs.md).

## Pre-Flight Check

Before starting the workflow loop, verify the runtime can do the work. This
skill has **zero external dependencies** — the only requirement is a music
generation backend (native tool or CLI). Before the first generation in a
session, run the full pre-flight protocol (including the Required check) in
[`references/setup-and-preflight.md`](references/setup-and-preflight.md).

Non-negotiable rules that always apply:

- Never install anything without explicit user consent (Dependency Consent
  Protocol). Show the exact command and its rough size/impact before asking.
- Detect the platform first (POSIX vs PowerShell vs cmd) and use matching
  command syntax for everything that follows.
- Ask hardware/setup questions once per session, then remember the answers.
- When a required dependency is missing, ask the user — do not silently
  degrade or skip.

### Covers, mashups, and MiniMax requests

MiniMax music generation is no longer available, so there is no skill to redirect to. For a cover or source-audio restyle, stay in this skill and load [`references/acestep-generation.md`](references/acestep-generation.md). ACE-Step cover/repaint is local, melody-aware, and queue-bound; tell the user it is slower and experimental. Two-song mashups and MiniMax emotion analysis are not available; say so instead of faking them.

**Audio source:** the user must provide a local audio file path. URLs are not accepted in either music skill in v1.5.0+; if the user wants to fetch audio by title from the internet, point them at the private `music-source-fetch` skill (not published on ClawHub).

## Local Models

Three local music models are supported by this skill. **License must be named and accepted before any model is downloaded** — the skill never auto-downloads (inherited hard rule from `setup-and-preflight.md`). License decides whether the output is fit for monetized channels, paid work, or advertising; pick the model that matches the distribution intent before installing.

| Model | License | Size | Commercial? | Purpose | Install guide |
| --- | --- | ---: | --- | --- | --- |
| **ACE-Step** (`acestep-v15-xl-base-diffusers`) | MIT | ~11 GB | ✅ Yes | Vocals + lyrics, local, exact-duration | [`§ 1`][acestep-install] |
| **MusicGen** (`facebook/musicgen-large`) | CC-BY-NC 4.0 | ~3.3 GB | ❌ No | Instrumental only, non-commercial | [`§ 2`][musicgen-install] |
| **Stable Audio Open** (`stabilityai/stable-audio-open-1.0`) | Stability AI Community | ~1.2 GB | ⚠️ Only if revenue < $1M/yr | Instrumental only, commercial-OK under cap | [`§ 3`][stable-audio-install] |

Hardware floor: Apple Silicon MPS gives 5–10× speed-up (CPU works but ~15 min / 30 s). NVIDIA CUDA is the reference. Apple Silicon requires `ACESTEP_LM_BACKEND=mlx`; on macOS, XL DiTs need `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`, which removes PyTorch's MPS memory cap: explain the system-wide memory risk and get the user's OK before using it (details in [`references/mps-bf16-acceleration.md`](references/mps-bf16-acceleration.md)). Memory probe protocol and per-model ML-budget rules: [`references/setup-and-preflight.md`](references/setup-and-preflight.md).

Full installation protocol (detection, environment setup, verify commands, license notes): [`references/setup-and-preflight.md`](references/setup-and-preflight.md).

[acestep-install]: references/acestep-generation.md
[musicgen-install]: references/setup-and-preflight.md
[stable-audio-install]: references/other-backends.md

## Backend Generation

Select the backend from the need, then load only that backend's reference:

| Need | Backend | Reference |
| --- | --- | --- |
| Vocals + lyrics, local, best local quality | ACE-Step 1.5 | [`references/acestep-generation.md`](references/acestep-generation.md) |
| Instrumental, local, no API key, non-commercial | MusicGen | [`references/other-backends.md`](references/other-backends.md) |
| Simple cloud generation (API key, no local model) | Stable Audio REST or another cloud backend the runtime exposes | [`references/other-backends.md`](references/other-backends.md) |
| Local source-audio cover/repaint, experimental | ACE-Step 1.5 | [`references/acestep-generation.md`](references/acestep-generation.md) |
| Instrumental via REST API | Stable Audio | [`references/other-backends.md`](references/other-backends.md) |
| Anything else the runtime exposes | Generic CLI | [`references/other-backends.md`](references/other-backends.md) |

Rules that always apply regardless of backend:

- Validate the prompt against the backend's format before generating
  (MusicGen wants 1–2 natural-language sentences; ACE-Step wants a detailed
  multi-dimensional caption; see the backend reference).
- Never retry an identical failing payload; change prompt, parameters, or
  backend between attempts.
- Verify the output file (duration, loudness, completeness) before delivery.

## ACE-Step Operational Caveats

Load [`references/acestep-generation.md`](references/acestep-generation.md)
and the focused local references before submitting a local ACE-Step job:

- The ACE-Step API server processes one job at a time; queue multiple versions
  sequentially and collect each output before submitting the next.
- `GET /v1/stats` exposes only top-level queue state. For long jobs, tail the
  server log (`/tmp/acestep-api.log`) for DiT/VAE progress.
- The cache directory accumulates generated files. Clean old files deliberately;
  never assume the API cleans them for you.
- There is no cancel endpoint. Lint prompt, lyrics, duration, and metas before
  submitting a long job.
- `thinking: true` is the quality default and may produce two cache files for a
  single request; collect and label both when they exist.
- For source-audio cover/repaint, use multipart upload and the `wait_for_acestep.py`
  helper when available. The local API can return empty `/query_result` data
  while work is still running, so cache-file detection is part of the workflow.
- For audio-conditioned tasks beyond cover/repaint (`extract`, `lego`, `complete`),
  the BASE-only DiT is required — load [`references/acestep-task-types.md`](references/acestep-task-types.md)
  before submitting. For XL (4B) DiT checkpoints (`xl-base`, `xl-sft`, `xl-turbo`,
  `xl-mixed`), the `num_inference_steps=50` (Diffusers path) / `inference_steps=50` (REST path) and `shift=3.0`
  footguns apply — load [`references/acestep-xl-models.md`](references/acestep-xl-models.md) before
  touching XL.

Copy-pasteable local commands and collection workflow:
[`references/local-ace-step-curl-template.md`](references/local-ace-step-curl-template.md)
and [`references/wait-and-collect.md`](references/wait-and-collect.md).

## Operating Rules

### 1. Read and auto-detect

Before asking anything, infer language, genre, mood, duration, and theme from the user's message. Default duration is about 3 minutes; only ask if the user is explicit about length.

Full auto-detect cheat sheet and edge cases: [`references/user-preference-flow.md`](references/user-preference-flow.md) and [`references/input-workflows.md`](references/input-workflows.md).

### First response defaults

Use these deterministic first responses before asking follow-up questions:

- **Standard song request** -> infer language, genre, mood, and duration; ask only for the missing lyric source, voice, or reference if it is not already implied.
- **User-provided lyrics** -> keep the lyrics intact, add section tags, and ask only for any missing voice or length detail.
- **Instrumental or jingle** -> set instrumental mode immediately; ask for duration only if the length is still unclear.
- **Vague style reference** -> use the reference as a style cue, infer the closest genre family, and ask only for lyrics source or voice if those are not recoverable from context.
- **Image or URL input enrichment** -> fetch or analyze the input first, turn the result into style cues, then ask only for anything that still cannot be inferred.

### 2. Analyze source material when available

If the user provides source audio or an analysis file, extract the reusable facts before writing the prompt. If there is no source material, continue with the request text and inferred defaults.

Full analysis options, tool choices, and the decision tree: [`references/input-workflows.md`](references/input-workflows.md).

#### Vocal confirmation gate

If source analysis returns `language=unknown`, suggests instrumental, or does not clearly confirm vocals, ask one targeted question before prompt construction:

> Is this instrumental, or does it have vocals? If vocals, what language, and should I use provided lyrics or extract them?

#### Target-length confirmation gate

If source audio exists and the user did not explicitly set the output length, confirm one of: same as source, standard 3:00, standard 3:30, or a specific length.

### 3. Ask only the ambiguous parts

After auto-detect, ask 1–3 questions max. Do not ask about language, genre, mood, or duration if the request already makes them obvious.

Question patterns and worked examples: [`references/user-preference-flow.md`](references/user-preference-flow.md).

### 4. Translate to a production-sheet prompt

The prompt you pass to `music_generate` is not a restatement of the user's words. It is a structured brief with ten required slots: genre/subgenre, mood, voice, instruments, anti-sparse instruction, BPM/key, structure, dynamics, production quality, and avoid list.

Full formula, slot-by-slot guide, and worked examples: [`references/prompt-formula.md`](references/prompt-formula.md).

### 5. Validate the prompt

Before generating, validate prompt length, structure, duration, lyrics tags, and backend-specific conflicts. Run `scripts/lint_lyrics.py <lyrics.txt> --bpm <bpm> --target-seconds <seconds>` for any provided/generated lyrics before spending a generation. If `music-craft-minimax` is installed, its `scripts/lint_music_request.py` is the canonical guard for mmx prompt size, missing fields, and conflicts.

Per-backend byte limits, length-reduction techniques, and lint rules: [`references/prompt-formula.md`](references/prompt-formula.md).

### 6. Structure the lyrics

If the user provides lyrics, add canonical section tags (`[Verse]`, `[Chorus]`, and so on) without altering the words. If the skill writes the lyrics, structure them from the start. Do not invent descriptive bracket tags such as `[Guitar Solo - distorted]` or `[Lyrics]`; bracket text can be sung by the model. ASR-extracted lyrics are unverified — cross-check and clean them before building the prompt.

Full tag reference, Whisper verification rules, transcript cleanup, and emotion-specific lyrics patterns: [`references/structure-tags.md`](references/structure-tags.md) and [`references/lyrics-cleanup.md`](references/lyrics-cleanup.md).

### 7. Generate and verify raw output

Call the detected backend with the production-sheet prompt and structured lyrics. Use the backend-specific generation command from the backend's reference file (routed via the **Backend Generation** table). Adapt the prompt format to the backend (e.g., MusicGen needs prompt + lyrics combined into one text block; mmx accepts them separately). After the tool returns, verify that audio is non-empty, has no sparse or a cappella drops, lyrics alignment is plausible, and structure matches the plan. When lyrics matter, listen or transcribe before delivery; `scripts/verify_lyrics_alignment.py` can compare expected lyrics against a transcript.

Backend commands and output verification details: backend reference files via the **Backend Generation** table above; quality checks: [`references/quality-and-revision.md`](references/quality-and-revision.md).

### 8. Finalize delivery copy

Normalize loudness with `ffmpeg loudnorm` (target -16 LUFS, -1 dBTP true peak), then verify duration, loudness, file size, and absence of silence drops or artifacts.

Loudnorm command, verify checklist, and request-fit checks: [`references/quality-and-revision.md`](references/quality-and-revision.md).

### 9. Iterate, do not retry the same payload

Identify the failure mode, adjust the prompt or lyrics to target it, and try once with a different seed if available. After 2 failed retries, ask the user to clarify or accept the best attempt. Never retry the same prompt plus lyrics combination twice in a row.

Iteration loop, adjustment recipes, and retry patterns: [`references/error-handling.md`](references/error-handling.md).

## Request Intake

Collect the required fields before generating: language, genre/subgenre, mood,
theme, vocal mode, lyric source, duration, structure, references, output location.
Ask the output location once, then reuse it for the whole session.
Build a confidence map for what was auto-detected vs assumed, and confirm
only the low-confidence slots with the user.

Full checklists, confidence-map examples, language-consistency checks,
ambiguous-phrase routing, and the per-song output layout and slug rules:
[`references/request-intake.md`](references/request-intake.md).

## Anti-Sparse Rules (Critical)

The single most common failure mode of music generators: interpreting "sparse", "quiet", or "minimal" as "remove all instruments and vocals".

### Always include in the prompt

1. **List every instrument by name.** Example: `accordion, upright bass, orchestral strings, piano, light percussion`.
2. **The always-playing rule.** `ALL instruments ALWAYS playing throughout, NEVER a cappella or silent`.
3. **The avoid list.** `AVOID sparse minimal arrangements, AVOID a cappella sections`.
4. **Explicit treatment of quiet sections.** `quiet sections: reduced to accordion and bass only, still fully played`.

### Never use alone

- `sparse arrangement`
- `minimal instrumentation`
- `stripped back`
- `a cappella section`
- `quiet with no instruments`

If the user asks for any of these, translate them into the explicit-instrument form.

### Ground every mood word

Every mood, energy, or emotion word in the prompt must be tied to at least one concrete production detail. A mood word with no grounding will be ignored — the model defaults to a "neutral pleasant" register.

| Mood word | Required grounding (pick at least one) |
| --- | --- |
| `sad` | minor key, slow BPM, breathy vocal, sparse chord pattern, low strings |
| `energetic` | fast BPM, driving drums, sharp synth hits, strong rhythm guitar |
| `romantic` | warm strings, soft vocal register, sustained pads, slow harmonic rhythm |
| `dark` | minor key, low register, distorted bass, low-pass mix, breathy vocal |
| `dreamy` | reverb-heavy mix, soft attack, layered pads, sustained vocal |
| `aggressive` | distorted guitars, fast BPM, shouted vocal, heavy drums |
| `triumphant` | major key, building dynamic, brass hits, declarative vocal |
| `intimate` | close-mic vocal, low dynamic range, soft attack, single voice |

If a mood word cannot be grounded, drop it. A grounded prompt with five moods beats an ungrounded prompt with fifteen. For the full emotion quick reference (21 emotions with prompt + lyrics + arrangement templates), see [`references/prompt-formula.md`](references/prompt-formula.md).

## Rate Limits

Respect backend rate limits; on a limit error, wait at least 60 seconds and reduce request rate rather than hammering. Details and per-backend behavior: [`references/quality-and-revision.md`](references/quality-and-revision.md).

## Quality Verification Checklist

Verification has two levels. **Technical generation success** means the file exists, is non-empty, and has audible content. **User-fit confirmed** means the output actually fits the user's intent (genre, language, length, structure, lyrics alignment). Always check both.

Before delivering a generated song to the user, walk this list mentally. If 3 or more items fail, the prompt needs adjustment and a regeneration. If 1–2 fail, you can either accept the result and warn the user, or make a targeted fix and regenerate.

1. **Audio is non-empty and plays.** Sample the first 5 seconds and the midpoint. If the file is empty or silent, regenerate.
2. **No sparse or a cappella drops.** Check the midpoint specifically — sparse drops are most common in quiet sections.
3. **No clipped vocals or distortion.** Listen for sudden loudness spikes or harshness.
4. **Lyrics alignment is plausible.** If the user provided lyrics, the output should hit the key phrases recognizably.
5. **Structure matches the plan.** If you asked for intro-verse-chorus-verse-chorus-bridge-chorus-outro, the song should have 7–8 distinct sections.
6. **Genre and mood are recognisable.** A "French chanson ballad" should sound like French chanson, not generic acoustic.
7. **Language is correct.** If the user asked for Spanish, the vocals should be in Spanish, not accented English.
8. **Energy arc is coherent.** The song should build, peak, and resolve. If it stays at the same energy for 3 minutes, the prompt was likely too vague.

For the request-fit checklist and revision patterns, see [`references/quality-and-revision.md`](references/quality-and-revision.md).

## Revision Prompts

When the output is close but not right, do not regenerate from scratch. Keep 80% of the original prompt. Add a single `REVISION:` block at the end that targets the specific failure.

Worked examples and the full retry recipe library: [`references/quality-and-revision.md`](references/quality-and-revision.md).

## Lyrics Optimizer Behavior

When `music_generate` is called **without explicit lyrics** and the request implies a vocal track (not instrumental), the runtime may auto-generate lyrics from the prompt.

Per-provider behavior, the web lyrics lookup option, and handling user surprise at AI-written lyrics: [`references/quality-and-revision.md`](references/quality-and-revision.md).

## User Preference Flow

The skill does not start with a questionnaire. It starts by reading and inferring.

| User says... | Skill does... |
| --- | --- |
| "Make a sad love song in Spanish" | Auto-detect: ES, romantic, ~3 min. Ask: lyrics source and vocal register. |
| "Instrumental lofi for studying" | Auto-detect: lofi, no vocals, ~3 min. Ask: nothing. Generate. |
| "Here are the lyrics, make it pop" | Auto-detect: pop, user-lyrics. Ask: tempo and energy preference. |
| "Something that sounds like Rosalía" | Auto-detect: modern Latin pop, female vocal. Ask: lyrics source and theme. |
| "I don't know, surprise me" | Pick a coherent default (for example upbeat indie pop, EN, ~3 min, auto-lyrics) and confirm with the user before generating. |

For the full decision table and edge cases, see [`references/user-preference-flow.md`](references/user-preference-flow.md).

## Output File Layout

One subfolder per song under the user's chosen output root; analysis JSON,
prompt file, and versioned audio files (`A_`, `B_`, `C_`, `M1_`/`M2_`,
`N1_`/`N2_`, `v2_`/`v3_` prefixes) live together in that subfolder. Slug and version rules: [`references/request-intake.md`](references/request-intake.md).

If the runtime needs a `MEDIA:` delivery path, use a path without spaces or
copy the final file into a workspace media folder first. Keep the archival copy
in the per-song output folder.

## Reference Map

- [`references/setup-and-preflight.md`](references/setup-and-preflight.md) — pre-flight protocol: dependency consent, platform detection, user and hardware setup, required/optional dependencies, install details
- [`references/windows-wsl-setup.md`](references/windows-wsl-setup.md) — Windows/WSL setup: certificate/proxy handling, WSL distro setup for local generation
- [`references/acestep-generation.md`](references/acestep-generation.md) — complete ACE-Step 1.5 guide: API workflow, full-song generation, quality tiers and memory-safe selection, audio-conditioned generation (cover, repaint, reference audio)
- [`references/local-ace-step-curl-template.md`](references/local-ace-step-curl-template.md) — JSON-safe `/release_task` submission template for direct ACE-Step submission
- [`references/wait-and-collect.md`](references/wait-and-collect.md) — M1 -> wait -> collect -> M2 local sequencing, log watching, cache collection, and duration verification
- [`references/lyrics-cleanup.md`](references/lyrics-cleanup.md) — cleanup recipe for Whisper/ASR transcripts, canonical section tags, `info.txt`, and `lyrics_whisper_medium.json`
- [`references/other-backends.md`](references/other-backends.md) — MusicGen, Stable Audio, generic CLI backends, and the MiniMax Music 3 local notes
- [`references/request-intake.md`](references/request-intake.md) — full intake protocol and per-song output layout (slugs, version prefixes)
- [`references/prompt-formula.md`](references/prompt-formula.md) — full production-sheet formula, worked examples across genres, prompt lint, and the emotion quick reference
- [`references/structure-tags.md`](references/structure-tags.md) — all section tags with rules, effects, and timing hints
- [`references/user-preference-flow.md`](references/user-preference-flow.md) — the auto-detect plus ask decision table and edge cases
- [`references/examples.md`](references/examples.md) — five worked examples (Spanish pop, English instrumental jingle, user-provided lyrics, image-inspired track, text-only style reference) with intake → prompt → verification for each
- [`references/style-categories.md`](references/style-categories.md) — 10 style categories with default instruments, BPM range, and mood
- [`references/input-workflows.md`](references/input-workflows.md) — 10 input types (description, user-lyrics, audio file, YouTube audio, song name, lyrics URL, YouTube metadata, JioSaavn metadata, image, genre/cultural), plus the signal-extraction rubric and confidence levels
- [`references/quality-and-revision.md`](references/quality-and-revision.md) — rate limits, request-fit checklist, revision prompts, delivery copy, lyrics-optimizer behavior
- [`references/error-handling.md`](references/error-handling.md) — error table, retry recipes (wrong language, weak chorus, sparse, vocals in instrumental, missing genre, too generic), and recovery patterns
- [`references/free-tool-inputs.md`](references/free-tool-inputs.md) — web_fetch, web_search, image, and memory tools for enriching inputs without scripts
- [`music-craft-minimax/scripts/lint_music_request.py`](../music-craft-minimax/scripts/lint_music_request.py) — optional standard-library helper for routing, blockers, missing fields, prompt, and `mmx` flag linting. Run it before generating to catch missing required slots, conflicting language signals, and vague mood words without grounding.
- [`scripts/lint_lyrics.py`](scripts/lint_lyrics.py) — standard-library lyrics preflight for section-tag whitelist checks and syllable/BPM duration estimates.
- [`scripts/verify_lyrics_alignment.py`](scripts/verify_lyrics_alignment.py) — standard-library post-generation transcript-vs-lyrics overlap check for semantic delivery.
- [`scripts/acestep_request.py`](scripts/acestep_request.py) — standard-library helper that sends one JSON or multipart request to a loopback ACE-Step server (`health`, `release_task`, `query_result`, `v1/init`).
- [`scripts/wait_for_acestep.py`](scripts/wait_for_acestep.py) — standard-library helper for ACE-Step task polling plus cache-file completion detection; `--expected-seconds` rejects short intermediates and `--scan-only` recovers a finished take from the cache.
- [`scripts/extract_stems.py`](scripts/extract_stems.py) — optional Demucs wrapper that writes normalized stem paths and `stems.json` for local arranger experiments.
- [`scripts/remix_stems.py`](scripts/remix_stems.py) — preview-quality `ffmpeg amix` helper for recombining validated stems.
- [`scripts/smoke_test.py`](scripts/smoke_test.py) — pure-Python smoke tests for local helper behavior.
- For emotion-driven generation (vocal speed, intensity, pitch bends, emotion recipes, iteration loop), see the quick reference in [`references/prompt-formula.md`](references/prompt-formula.md) under "Mood" and the full shared emotion recipes in [`music-craft-minimax/references/emotion-delivery.md`](../music-craft-minimax/references/emotion-delivery.md)
- [`references/acestep-task-types.md`](references/acestep-task-types.md) — per-task reference for the five ACE-Step audio-conditioned tasks (`cover`, `repaint`, `extract`, `lego`, `complete`): inputs, outputs, parameters, BASE-only footguns, and a routing tree
- [`references/acestep-xl-models.md`](references/acestep-xl-models.md) — XL (4B) DiT family: `xl-base` vs `xl-mixed` deployment shapes, hardware floor (≥12 GB VRAM, 24 GB M3 reference, 32 GB+ for `xl-mixed`), the two silent-regression footguns (`num_inference_steps=50` MUST be explicit, `shift=3.0` default), and an XL-vs-standard decision tree
- [`references/mps-bf16-acceleration.md`](references/mps-bf16-acceleration.md) — honest Apple Silicon (MPS) reference: which env vars actually work (`PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`, `ACESTEP_LM_BACKEND=mlx`), and the verifiable fact that ACE-Step currently forces fp32 on MPS (no bf16 escape valve — `ACESTEP_USE_BF16` is NOT consumed)
- [`references/lrc-generation.md`](references/lrc-generation.md) — backend-neutral LRC (synced lyrics) workflow: WhisperX/Whisper transcription → lyrics alignment → LRC format → validator
- [`references/audition-rubric.md`](references/audition-rubric.md) — 5-dimension quality scoring (Musicality, Production, Prompt Adherence, Vocal, Technical) for accept/revise/regenerate/reject decisions
- [`references/acestep-shift-schedule.md`](references/acestep-shift-schedule.md) — full `shift` parameter taxonomy (shift=1.0 turbo, shift=3.0 base/sft, continuous shift) with tier-to-shift mapping table and decision tree
- [`references/audio-format-selection.md`](references/audio-format-selection.md) — when to use wav vs flac vs mp3 vs ogg
- [`references/advanced-diffusion-controls.md`](references/advanced-diffusion-controls.md) — `guidance_scale`, `infer_method`, `scheduler`, and `eta` parameter reference

## Tool Scope

What this skill needs from the agent runtime, and nothing more:

- **Read files:** the user's own lyrics, prompts, and local audio files they point to; the bundled references and scripts.
- **Write files:** generated audio, prompts, lyrics, `.lrc` and `stems.json` files, only in the output folder the user chose. Never overwrite an existing file without the user's OK.
- **Run commands:** the bundled Python helpers, `ffmpeg`/`ffprobe` for verification and mixing, and the user's local ACE-Step server. No package installs, model downloads, or environment changes without the user's explicit OK.
- **Network:** the user's local ACE-Step server on the loopback interface; a cloud music provider only after the user agrees to send the prompt (and lyrics) there; web search only with generic terms and the user's OK.

## Data, Consent, and Local Side Effects

This skill may use local or cloud music backends depending on what the user asks for and what is installed. Keep the workflow user-visible:

- **Cloud backends:** prompts, lyrics, reference URLs, and generated/derived music instructions may be sent to the selected provider.
- **Local backends:** model downloads, local analysis, temporary files, and generated audio may be written on the user's machine.
- **Reference material:** fetched webpages and lyrics pages are used only to enrich the music prompt unless the user explicitly chooses an audio/cover workflow.
- **Output files:** ask where to save generated files and avoid overwriting user-visible outputs without explicit confirmation.

Before uploading user-owned or third-party media to a cloud backend, state what will be sent and why, then wait for confirmation if the user has not already clearly requested that cloud workflow.

**Bundled helpers and what they touch** (all optional, run only when the workflow calls for them):

| Helper | Reads | Writes | Network | External programs |
| --- | --- | --- | --- | --- |
| `scripts/acestep_request.py` | the JSON body or local audio file you pass | nothing | loopback ACE-Step server only (`127.0.0.1`, `localhost`, `::1`); no proxies, no redirects | none |
| `scripts/wait_for_acestep.py` | ACE-Step cache directory | nothing | loopback ACE-Step server only; no proxies, no redirects | `ffprobe`, when installed, to measure duration |
| `scripts/lint_lyrics.py`, `scripts/verify_lyrics_alignment.py` | text files you pass | nothing | none | none |
| `scripts/extract_stems.py` | a local audio file you pass | stem files and `stems.json` in the output folder you choose | none, unless `--allow-model-download` lets Demucs fetch its weights on first use (ask first) | `demucs`, on demand |
| `scripts/remix_stems.py` | stem files listed in `stems.json` | one remixed file you name | none | `ffmpeg`, on demand |

`ffmpeg`/`ffprobe` and `demucs` are optional and are not required to install the skill; the helpers report clearly when they are missing. Stem separation is for the user's own local audio (post-production on files they provide), not for fetching or extracting third-party content.

## Licensing and commercial-use gate

The published skill bundle is MIT-0 under ClawHub's publishing rules: it may
be used, modified, and redistributed commercially without attribution. That
license applies to these skill instructions and bundled helper code; it does
not grant a license to any third-party model, software package, input audio,
lyrics, voice, or generated output. Every operator must install the selected
backend under its own applicable terms and keep the required notices. Terms
and model cards can change, so check them before commercial release.

- **ACE-Step 1.5 local:** the project and published model card currently state
  an MIT license and commercial-ready use. Verify the exact model checkpoint
  and its current license before shipping a commercial track.
- **MusicGen local:** the code is MIT, but the MusicGen model weights are
  CC-BY-NC 4.0. Do not use MusicGen-generated audio for commercial work,
  monetized channels, client deliverables, paid products, or advertising.
- **Provider-agnostic/runtime backends:** do not assume commercial rights.
  Identify the actual provider, model, account/product tier, and output terms
  before generating for commercial use. If these are unknown, stop and ask.
- **Inputs:** the user must own or have permission for uploaded/reference
  audio, lyrics, samples, and voices. A model license does not legalize a
  copyrighted cover, lyric transcription, or unauthorized voice.

Generated audio may also lack copyright protection or exclusivity under the
law of the user's jurisdiction. Commercial permission from a provider is not
the same as a guarantee of exclusive copyright or zero similarity risk.

Treat music generation as a small, controlled iteration loop, not a single "press button, get song" call.

The required generation loop is:

1. Clarify goal and source material.
2. Analyze source audio if available, or accept user-provided analysis.
3. Build a production-sheet prompt with genre, mood, BPM, key, instruments, structure, vocals/lyrics, and constraints.
4. Select backend based on need: exact-duration vocals/lyrics -> ACE-Step; local melody-aware cover/repaint experiments -> ACE-Step if hardware and time budget allow; instrumental/local -> Stable Audio 3 or MusicGen; fast cloud cover, mashup, or MiniMax-specific flags -> `music-craft-minimax` / mmx.
5. Validate prompt length, structure, backend-specific conflicts, and expected duration.
6. Generate with the selected backend.
7. Verify duration, loudness/peak, file size, audible completeness, lyrics alignment, and structure.
8. Deliver files with a short analysis summary and caveats. If quality fails, adjust the prompt and retry; do not retry the same payload twice.

For deep prompt engineering, lyrics structure, and the full user-preference decision table, see the linked references at the end.

