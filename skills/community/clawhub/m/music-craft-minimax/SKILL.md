---
name: music-craft-minimax
version: 1.5.0
description: Advanced music generation for OpenClaw, using the MiniMax Music 2.6 token plan. Use for cover and style transfer, two-song mashup, lyrics generation API, emotion-driven prompt engineering, and fine control via the `mmx` CLI. Extends `music-craft` with MiniMax-specific features.
metadata: '{"openclaw":{"requires":{"env":["MINIMAX_API_KEY"],"bins":["python3","ffmpeg","mmx"]},"primaryEnv":"MINIMAX_API_KEY","emoji":"\ud83c\udfb6","homepage":"https://github.com/LuisCharro/skills/tree/main/publish/music-craft-minimax","envVars":[{"name":"MINIMAX_API_KEY","required":true,"description":"API key for the MiniMax Music 2.6 token plan. Required for cover, mashup, lyrics generation, and mmx flag control."}]}}'
---

# Music Craft — MiniMax

**Cloud duration is approximate.** Verified field run (2026-06-12): 18/18
cloud jobs saved an MP3, but output length ranged from 57-135% of requested
duration (12 truncated, 3 close, 3 extended). Use `music-craft` with local
ACE-Step when exact duration matters; use this skill when speed, MiniMax cover
workflows, lyrics API, emotion analysis, or `mmx` flag control matter more.

This is the **power-user upgrade** of [`music-craft`](../music-craft/). It does everything that skill does, plus the features that require the MiniMax Music 2.6 token plan:

- **Cover and style transfer** from a reference audio file (preserves melody)
- **Two-song mashup** (Song A's content and emotion + Song B's style)
- **Lyrics generation** via the MiniMax API endpoint (with edit mode for iteration)
- **Emotion analysis** on input audio to drive prompt construction (vocal speed, intensity curve, pitch bends)
- **Fine control** over generation parameters (BPM, key, structure, avoid list as separate flags via `mmx`)

For everything else (standard song generation, instrumentation, anti-sparse prompt engineering, structure tags, user preference flow), this skill uses the same workflow as `music-craft`. Read that skill first to understand the base, then come back here for the MiniMax-specific extensions.

## Data, Consent, and Local Side Effects

This skill is allowed to process music media, but it should not surprise the user:

- **Cloud generation:** prompts, lyrics, reference audio, and cover/mashup inputs may be sent to MiniMax through `mmx` or MiniMax API calls. Confirm consent before sending sensitive, private, or third-party-owned audio.
- **Local files only:** audio input must be a local file path. URLs are not accepted in v1.5.0+; use the private `music-source-fetch` skill to fetch audio by title first.
- **Lyrics:** Whisper transcription of the local audio file is the only lyrics source in this skill. LRCLib web lookup moved to `music-source-fetch`.
- **Local outputs:** analysis JSON, lyrics, prompts, temporary media, and generated audio are written to user-selected paths or temporary directories.
- **Overwrites:** helper scripts refuse to replace existing user-visible outputs unless the operator passes an explicit `--overwrite` flag.

There is no image, face, OCR, or VLM pipeline in this skill. Album art, video frames, and similar visual inputs are not analyzed.

## Required MiniMax Workflow

> **Operator rules for MiniMax generations:**
> - Run MiniMax generations sequentially, not in parallel.
> - Do not assume the CLI will honor a requested output path — pass `--out` to `mmx` and verify the file exists after each run.
> - Treat requested duration as a target, not a guarantee. Verified range: 57-135% of requested duration.
> - If `mmx` exits with SIGTERM/SIGKILL after saving, verify the file before rerunning; file existence is the source of truth.
> - Before running multi-output MiniMax generations, load [`references/minimax-generation-caveats.md`](references/minimax-generation-caveats.md).

For every cover, style-transfer, mashup, or precision `mmx` generation, follow this checklist in order:

1. **Analyze source audio** with `scripts/analysis_orchestrator.py` when audio is available.
2. **Build M1 + M2 prompts** from the analysis: M1 is the primary style, M2 is a strong contrast style.
3. **Lint both prompts and lyrics** with `scripts/lint_music_request.py` before generation. Use `--lyrics-file` when lyrics exist so invalid tags and duration density are caught. Stop on blockers.
4. **Generate with retry** via `scripts/generate_with_retry.py --output-path <final.mp3> -- music generate ... --out <final.mp3>` or `-- music cover ... --out <final.mp3>`. `--output-path` does not replace `mmx --out`.
5. **Verify outputs**: duration, LUFS/peak, file size, audible completeness, and lyrics alignment. When lyrics matter, listen or transcribe and use `scripts/verify_lyrics_alignment.py` before delivery.
6. **Finalize delivery copy** with `scripts/finalize_track.sh input.mp3 output.mp3` when the user wants production-ready loudness.
7. **Deliver both versions** with a short analysis summary and any caveats.

Preserve the anti-sparse guard in prompts: fully arranged, instruments keep playing, no a cappella dropouts unless explicitly requested.

## Reliability Caveats

Load [`references/minimax-generation-caveats.md`](references/minimax-generation-caveats.md)
before any multi-output, long-duration, or quota-sensitive cloud run.

- `--length` is a hint, not a contract. Cloud output can undershoot or overshoot
  the request; local ACE-Step is the exact-duration fallback.
- A shell SIGTERM/SIGKILL after save can still be a successful generation. Check
  file existence, file size, and `ffprobe` duration before retrying.
- Keep standard cloud generation prompts under about 500 characters when
  possible. Put detailed production sheets in the local ACE-Step route.
- Treat `--references` as optional and potentially flaky. Inline concise
  references in the prompt when reliability matters.
- Expected cloud output is MP3, stereo, 44.1 kHz, about 256 kbps. There are no
  documented flags for FLAC, 48 kHz, or bitrate selection.
- There is no documented MiniMax batch API or preview/draft mode. For repeated
  covers, use `scripts/batch_cover.py` so runs remain sequential and verified.
- Quota usage may not be visible from the CLI. Check the MiniMax dashboard when
  planning large batches.

Short cloud prompt recipes: [`references/short-prompt-recipes.md`](references/short-prompt-recipes.md).

## Routing and Blocker Checks

Classify the request before analysis or generation:

- **Text-only style reference** means the user gave a song name, artist, era, or genre cue without source audio. Treat it as style inference, not cover analysis.
- **Reference audio** means the user provided a local file that should be analyzed. URLs are not accepted; ask for a local file path.
- **Cover** preserves melody and usually needs a source file plus a target style decision.
- **Style transfer** uses a reference track or analyzed audio as style input, then changes the production direction.
- **Mashup** needs Song A and Song B, plus a decision about which one contributes content and which one contributes style.
- **Emotion prompt** means the user wants analysis turned into descriptive prompt language, not a full cover.

The [`scripts/lint_music_request.py`](scripts/lint_music_request.py) helper emits one of these routes:

| Route | When |
|---|---|
| `base_prompt` | Standard generation, no MiniMax-specific feature needed. |
| `minimax_cover` | Melody-preserving cover from a local audio file. |
| `minimax_mashup` | Two-song mashup (A + B, both identified). |
| `minimax_style_transfer` | Style transfer that does not preserve the source melody. |
| `minimax_emotion_prompt` | Emotion analysis, or precision `mmx` flag usage. |
| `needs_clarification` | At least one blocker is unresolved; ask the user first. |

Surface blockers before analysis:

- no local source file (URLs are not accepted)
- unclear which track is Song A versus Song B
- missing target style
- missing lyrics decision, such as original, translated, rewritten, or instrumental
- conflicting cover/style-transfer intent: the user asked for both "cover" (preserve melody) and "style transfer" (reproduce style) at once. These are mutually exclusive. Ask the user to pick one.

After you have prompt text and `mmx` flags, lint them together before generation:

- compare prompt BPM with `--bpm`
- compare prompt key with `--key`
- compare prompt structure line with `--structure`
- compare prompt duration with `--duration` (or implicit length expectation)
- compare prompt vocal mode with `--vocals`
- compare prompt language with `--language`
- compare prompt avoid language with `--avoid`
- stop when the prompt says one thing and the flags say another
- warn when prompt text exceeds 1800 UTF-8 bytes
- stop when prompt text exceeds 2000 UTF-8 bytes (observed API rejection at 2079 bytes)

If the user only has a text reference, route to the free-tool path in `references/free-tool-inputs.md` first. If the user has audio, analyze first and only then build the prompt. The linter returns a `retry_guidance` array with one hint per conflict so the operator can re-align prompt and flags on the next attempt.

## When To Use

Use this skill when the task involves:

- generating a cover of an existing song with a different style (chanson version of a rock track, reggaeton version of a pop hit, and so on). Source must be a local file.
- style transfer from a local audio file to a target genre
- two-song mashup where Song A's lyrics and emotional arc are kept, but Song B's style is applied
- emotion analysis on input audio to extract intensity curves, vocal speed, pitch bends, and emotion classifications
- generating lyrics in a specific language and theme via the MiniMax `lyrics_generation` API
- editing existing lyrics to match a target style or emotional arc (MiniMax `lyrics_generation` edit mode)
- using `mmx` CLI directly for fine control over `--avoid`, `--bpm`, `--key`, `--structure`, `--vocals`, `--instruments` as separate flags
- accessing MiniMax's `music-cover` or `music-cover-free` models for melody preservation

## Request Intake (adapted for MiniMax features)

After the Routing and Blocker Checks classify the request, run this 2-pass intake to extract the full set of fields the user cares about. Label each field's confidence: **clear** (user said it), **inferred** (sensible default), **missing** (need to ask), or **conflicting** (user said two incompatible things — pause to resolve).

### Fields checklist (MiniMax-specific)

| # | Field | What to look for | MiniMax-specific notes |
|---|---|---|---|
| 1 | Route | Cover / style transfer / mashup / standard / emotion prompt | From the Routing and Blocker Checks section. Determines which MiniMax features to use. |
| 2 | Source audio | Local file path | Required for cover, mashup, style transfer. For standard, optional (text-only style reference is also fine). |
| 3 | Song A identity | Name, artist, audio | For mashup: needed. For cover: this is the source. |
| 4 | Song B identity | Name, artist, audio | For mashup only. |
| 5 | Target style | Genre / mood / reference | The destination of the cover or style transfer. If user says "like Rosalía", that's clear. If user says "something good", that's missing. |
| 6 | Lyrics decision | Original / translated / new / instrumental | For cover, default to original (translated if user requests it). For standard, default to new (or user-provided). |
| 7 | Vocal mode | Solo / duet / choir / instrumental | Drives `--vocals` and `--language` flags. |
| 8 | Language | BCP-47 code (en, fr, es, etc.) | For lyrics language AND vocal language. |
| 9 | Duration | Approximate length (jingle ~30s, standard ~3min, epic ~6min) | `--length` is a hint in milliseconds, not a guarantee. Length is still driven mainly by lyrics + structure. |
| 10 | BPM, key, structure | Exact values if user wants `--bpm`/`--key`/`--structure` | Optional. If provided, the prompt AND flags must agree (lint them). |
| 11 | Emotion arc | For emotion-prompt workflows: which emotions to emphasize | Drives the analysis-to-prompt translation. |
| 12 | **Output location** | Where the audio and analysis files go | Same as the base skill — per-song subfolder in `~/Music mix/<project>/<song-slug>/`. |

Confidence map example: [`references/examples.md`](references/examples.md).

If any field is **missing** or **conflicting**, that's a question to ask. The `Ambiguity Questions` section below has specific patterns for each route. If everything is **clear** or **inferred**, the request is ready to translate.

## User Preference Flow (message patterns → action)

The skill does not start with a questionnaire. It starts by reading and inferring from the user's natural-language request.

| User says... | Skill does... |
|---|---|
| "Haz un cover de X en Y" | Route: `minimax_cover`. Ask: local source audio file path, target language for lyrics, vocal register. |
| "Make this song sound like Rosalía" | Route: `minimax_style_transfer`. Ask: source audio, which album/era of Rosalía. |
| "I have audio of A, mash with B, keep A's melody" | Route: `minimax_mashup`. Ask: A vs B confirmation, source audio for A, B can be name or audio. |
| "Analyze the emotion curve of this track" | Route: `minimax_emotion_prompt` (analysis-only). Run `analysis_orchestrator.py --audio` first, then read the JSON. |
| "I want the lyrics to be about X, in French, melancholic" | Route: `base_prompt` (standard). Use the lyrics API to generate, then pass to `mmx music generate --lyrics-file`. Ask: target BPM/key/structure or derive from analysis. |
| "Recreate the song but in 90 BPM D minor" | Route: `base_prompt` with `mmx` flags. Lint prompt vs flags before generation. Verify BPM/key consistency. |
| "I don't know, surprise me" | Pick a coherent default (e.g. upbeat indie pop, EN, ~3min, auto-lyrics, standard generation) and confirm with the user before generating. |
| "Same song again but as a reggaeton version" | Route: `minimax_cover` with the existing song as source. Use the same project/song subfolder, suffix the MP3 (`M1_original.mp3` + `M2_reggaeton.mp3`). |

This table is the **abstract** of `references/user-preference-flow.md` (which lives in the base skill). If you want a more detailed case, defer to the base skill's table and combine with this skill's route mapping.

## Output File Layout (Per-Song Subfolders)

**MiniMax-specific additions** (drop these into the per-song subfolder alongside the base items):

| File | Source | Notes |
|---|---|---|
| `<song-slug>_analysis.json` | `analysis_orchestrator.py --output` | MiniMax-specific analysis results (emotion, BPM, key, segments) |
| `<song-slug>_lyrics.txt` | `mmx music generate --lyrics-file` | Optional if user provided lyrics inline |
| `<song-slug>_<style>_prompt.txt` | The exact text passed to `--prompt` | For reproducibility |

The LLM should aim for the base skill's layout by default. The MiniMax-specific files are added on top when MiniMax features are used (cover workflow, mashup, analysis, etc.).

If the runtime needs a `MEDIA:` delivery path, use a path without spaces or
copy the final file into a workspace media folder first. Keep the archival copy
in the per-song output folder.

## Quick Start with the Orchestrator

One entry point for all input analysis:

```bash
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav
```

It routes local audio files and two-song pairs to the right extractors.
URLs, video, and images are no longer supported as input to this skill.
Full per-input commands, extraction guidance, and the per-song output
layout:
[`references/orchestrator-quickstart.md`](references/orchestrator-quickstart.md).

## When NOT To Use

Do not use this skill when:

- the user only needs standard song generation without cover, mashup, or analysis — use `music-craft` instead (lighter, no MiniMax dependency)
- the runtime does not expose a `music_generate` tool and there is no `MINIMAX_API_KEY` configured — both skills need the runtime
- the user wants deterministic, single-shot generation with no iteration — overkill
- the user wants to mutate a specific existing audio file (pitch shift, time stretch, stem split) — that is post-production, not generation
- the user is not on a MiniMax Token Plan — the advanced features (cover, mmx per-flag control, lyrics API, emotion-driven prompts) require the plan
- the user needs a reliable full-length 3:00+ song with exact duration — prefer `music-craft` with ACE-Step instead; MiniMax is the right tool when speed, convenience, cover workflows, mashups, or mmx flag control matter more than exact output length

## Decision Tree

Use the base skill unless one of these MiniMax-specific needs is present:

- melody-preserving cover or style transfer from a local audio file
- two-song mashup
- lyrics API preview/edit flow
- emotion analysis that feeds the prompt
- exact `mmx` control for BPM, key, structure, or avoid lists

If the user wants a new song that only borrows a style, stay in `music-craft` unless they also need exact flag control or lyrics API iteration.

If the user provides a URL, do not attempt to download it. Tell them this skill accepts only local files, and suggest `music-source-fetch` if they need to fetch audio by title.

## Audio Source (Local Only)

The source for cover, mashup, or style transfer must be a local audio file
path. URL inputs trigger a soft warning and the agent asks for a local
file. If you have a URL, fetch it locally first with the private
`music-source-fetch` skill.

## First Response Defaults

Use these defaults on the first pass:

- **Cover from a local audio file**: start with the one-step cover path. Switch to two-step only if the user wants translated lyrics, edited ASR lyrics, or custom lyrics.
- **Style transfer only**: do not use cover unless melody preservation matters. Use standard generation plus `mmx` flags if exact BPM/key/structure matter.
- **Two-song mashup**: anchor on Song A. If Song A has audio, default to the cover two-step workflow; if Song B is only named, ask for a short style description or fetch more context if free tools are available.
- **Lyrics API generation or edit**: use `write_full_song` for blank-page generation and `edit` for revisions.
- **Emotion-analysis-to-prompt**: run analysis first, then convert to a prompt; only ask whether the output should be cover, mashup, or standard generation, plus the target language if missing.
- **Exact BPM/key/structure control**: make `mmx` flags the source of truth and keep the prompt descriptive but non-conflicting.

## Ambiguity Questions

Ask at most 1-3 questions. Separate blockers from quality tweaks:

- Required blockers first: local source file, which song is A vs B, whether lyrics already exist, whether the output must preserve melody.
- Optional quality after blockers: target language, target style, BPM, key, structure, instruments, vocal color, avoid list.

Use these exact patterns when clarification is needed:

- **Cover**: "Which source should I use?" "Do you want the original lyrics, translated lyrics, or new lyrics?" "Any target style, or should I derive it from the source?"
- **Mashup**: "Which song is A and which is B?" "Do you have audio for Song B, or only the name?" "Should the lyrics stay the same or be rewritten?"
- **Lyrics API**: "Write from scratch or edit existing lyrics?" "What language should I target?" "Any hard structure requirements?"
- **Emotion prompt**: "Do you want cover, mashup, or standard generation?" "What language should the output use?" "Should I prioritize tenderness, energy, or structure?"
- **mmx precision**: "Which values are mandatory: BPM, key, structure, or avoid list?" "Any instruments or vocals that must stay in or stay out?"

## Relationship to `music-craft`

This skill **extends** the base skill, it does not replace it. The shared concepts are:

| Concept | Where it lives |
|---|---|
| Pre-Flight Check (platform detection) | This skill (extended required list) |
| Anti-sparse rules (canonical text) | Base skill, referenced from here |
| Prompt formula (production sheet) | Base skill, referenced from here |
| Structure tags (14 tags) | Base skill, referenced from here |
| User preference flow (auto-detect + ask) | Base skill, referenced from here |
| Output file layout (per-song subfolders, slug rules, version prefix) | Base skill, referenced from here; MiniMax adds analysis.json and lyrics.txt |
| Rate limits (generic) | Base skill |
| Quality verification checklist | Base skill, extended here for MiniMax |
| Operating rules (6-step loop) | Base skill, summarized here with MiniMax-specific extensions |

The MiniMax-specific additions are:

| MiniMax concept | Where it lives |
|---|---|
| `mmx` CLI quick reference | This skill |
| `mmx` full flag reference | This skill, [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md) |
| Cover workflow (one-step, two-step) | This skill, [`references/cover-workflow.md`](references/cover-workflow.md) |
| Lyrics generation API | This skill, [`references/lyrics-generation.md`](references/lyrics-generation.md) |
| Mashup workflow (A + B) | This skill, [`references/mashup-workflow.md`](references/mashup-workflow.md) |
| Emotion analysis (vocal speed, intensity, pitch) | This skill, [`references/emotion-analysis.md`](references/emotion-analysis.md) |
| MiniMax-specific error handling | This skill, [`references/error-handling.md`](references/error-handling.md) |
| Audio analysis scripts | This skill, [`scripts/`](scripts/) |
| Free tool inputs (web, memory; image removed in v1.5.0) | Both skills — base layer in [`music-craft`](../music-craft/), MiniMax layer here in [`references/free-tool-inputs.md`](references/free-tool-inputs.md) |

## Pre-Flight Check

Run the extended pre-flight in
[`references/setup-and-preflight.md`](references/setup-and-preflight.md)
before the first generation or analysis. Never install anything without
explicit user consent; required: the `music_generate` tool, `MINIMAX_API_KEY`, `python3`, `mmx` —
if one is missing, ask, do not degrade silently.

## Free Tool Augmentation (Input Enrichment)

The OpenClaw runtime exposes several free tools (web_fetch, web_search, memory, browser) that enrich the music generation workflow. The base layer is documented in [`music-craft` → Free Tool Augmentation](../music-craft/SKILL.md#free-tool-augmentation) and [`references/free-tool-inputs.md`](../music-craft/references/free-tool-inputs.md). This section shows how they compose with MiniMax-specific features.

> **v1.5.0+**: The `image` tool flow was removed (no album art / OCR / face / VLM analysis in this skill). The skill is audio-only. Web tools (`web_fetch`, `web_search`) are still available for metadata-only enrichment (artist info, genre descriptions) but never for downloading audio.

Free-tool routing, blocker checks, prompt/flag lint, and MiniMax combos: [`references/free-tool-inputs.md`](references/free-tool-inputs.md).

## Operating Rules

Same 6-step loop as `music-craft`, with MiniMax-specific extensions:

1. **Read and auto-detect** — same
2. **Ask only the ambiguous parts** — same, plus ask if the user wants cover / mashup / standard
3. **Translate to a production-sheet prompt** — same, but consider whether to use `mmx` flags (see [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md)) instead of packing everything into the prompt
4. **Structure the lyrics** — same, plus consider lyrics API for generation or edit (see [`references/lyrics-generation.md`](references/lyrics-generation.md))
5. **Generate and verify** — same, plus the `music-cover` model for melody preservation
6. **Iterate** — same, plus emotion analysis to inform the next prompt adjustment

For the full 6-step detail, see `music-craft` → Operating Rules.

## Song length (`--length` is a hint, not a guarantee)

`mmx music generate --length` accepts milliseconds as a **duration hint**. It is useful, but it is not precise. **Don't expect mmx to hit 3:30 exactly.** In the 2026-06-12 field run, cloud outputs ranged from 57-135% of requested duration. If you need precise length, ACE-Step is the right tool (it has `audio_duration`). If you want MiniMax's speed and the song length is flexible, mmx is fine.

Details: [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md).

## mmx CLI Quick Reference

The shape of a complete generation command:

```bash
mmx music generate \
  --prompt "<production-sheet prompt>" \
  --lyrics-file lyrics.txt \
  --model music-2.6 \
  --bpm 96 --key "D major" --structure "intro-verse-chorus-verse-chorus-bridge-chorus-outro" \
  --vocals "<vocal description>" --genre "<genre>" --mood "<mood>" --instruments "<instruments>" \
  --avoid "<what to avoid>" --out output.mp3
```

Full reference with all flags, examples, and model selection guidance: [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md).

## mmx Music Generation — verified patterns (June 2026)

Pattern A: full song with detailed prompt + 6 metadata flags (`--vocals`, `--genre`, `--mood`, `--instruments`, `--bpm`, `--key`) — production-grade output. Pattern B: crazy combo experiments (e.g. opera vocals over heavy metal), uses `scripts/generate_with_retry.py` wrapper.
Model selection guidance covers `music-2.6` vs `music-2.6-free` and when to use each; `--instrumental` and `--lyrics-optimizer` flags bypass the `--lyrics` requirement for BGM and auto-lyrics workflows.
Prompt length safety: prompts `>2000` UTF-8 bytes fail with `invalid params, prompt length not valid` — run `scripts/lint_music_request.py` before generation. Lyrics tag safety: run `scripts/lint_lyrics.py` or pass `--lyrics-file` to `lint_music_request.py`; non-whitelisted bracket tags may be sung. URL expiration: when using `--output-format url`, the returned URL has a 24h time limit — always use `--out` or download promptly.

For cloud reliability, keep standard `music generate` prompts under about 500
characters when possible. Inline reference artists in the prompt instead of
relying on `--references` for batch runs.

Details: [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md).

## Cover Workflow

Cover workflow preserves the original song's melody while applying a different style. Two paths exist: one-step (`scripts/generate_with_retry.py -- music cover ...`, MiniMax extracts lyrics via ASR and applies the new style) and two-step (preprocess to get a `cover_feature_id`, edit ASR lyrics, then generate — better when lyrics need correction or the user wants different lyrics in the new style).

Full workflow with payloads, error handling, and use cases: [`references/cover-workflow.md`](references/cover-workflow.md).

## Lyrics Generation

MiniMax has a dedicated `lyrics_generation` endpoint that produces structured lyrics (with `[Verse]`, `[Chorus]`, etc. tags) from a theme prompt. Two modes:

- `write_full_song` — create new lyrics from a theme
- `edit` — modify existing lyrics (e.g., make the chorus stronger, shift to a hopeful ending)

The output is structured lyrics that can be passed directly to `music_generate` or `mmx music generate`.

Full detail with API examples, parameters, and use cases: [`references/lyrics-generation.md`](references/lyrics-generation.md).

## Lyrics Source

Whisper transcription of the local audio file is the only lyrics source
in this skill. The LRCLib web lookup moved to the private
`music-source-fetch` skill in v1.5.0.

## Mashup Workflow

The signature MiniMax-specific feature: combine Song A (content + emotion) with Song B (style).

Workflow:

1. Get Song A (local audio file or song name)
2. Get Song B (local audio file or song name)
3. Run emotion analysis on Song A (if audio available) to extract the emotional arc
4. Build a prompt that applies Song B's style to Song A's content and emotion
5. Generate using the cover workflow (preserves melody) or standard generation (creative reimagining)

This is the most powerful feature in this skill. The output preserves what makes Song A recognizable (lyrics, melody, emotion) while applying Song B's production style.

Full detail with the emotion-to-prompt conversion and the two-song analysis script: [`references/mashup-workflow.md`](references/mashup-workflow.md) and [`references/emotion-analysis.md`](references/emotion-analysis.md).

## Emotion Analysis

Emotion analysis extracts per-section features from input audio (intensity, pitch, vocal effort, breathiness, spectral centroid, emotion classification, repetitive intensification, emotional shifts, vocal speed, pitch bends). The analysis outputs JSON that the `emotion_to_prompt.py` script converts into a ready-to-use production-sheet prompt. Run analysis first when audio is available; use the local-only path (assemble prompt from JSON without the cloud helper) when MiniMax API access is unavailable.

Full detail with detection cookbook, pipeline, scripts, local-only path, and the 25+ emotion set: [`references/emotion-analysis.md`](references/emotion-analysis.md). For emotion recipes in the OUTPUT, see [`references/emotion-delivery.md`](references/emotion-delivery.md).

## Analysis Quality (Summary Format, Confidence, Fallbacks)

Analysis scripts in `scripts/` produce different views (emotion, beats, melody, structure, instrumentation). The skill expects them to converge on a single compact summary so downstream code and humans can read the same shape regardless of which scripts ran.

### Compact Analysis Summary

Every analysis result should include a `summary` object with these keys:

| Key | Type | Meaning |
|---|---|---|
| `tempo` | string | BPM value with confidence, e.g. `120 BPM (confidence 0.92)` |
| `key` | string | Detected key, e.g. `E minor (confidence 0.71)` |
| `sections` | list | Section labels with timing, e.g. `[{"label": "verse", "start": 0.0, "end": 28.5}, ...]` |
| `instrumentation` | list | Detected instrument palette, e.g. `["electric guitar", "drums", "bass"]` |
| `vocal_traits` | dict | Breathiness, intensity, pitch range, e.g. `{"breathiness": "high", "intensity": "medium"}` |
| `energy_curve` | list | Per-section energy values, e.g. `[{"t": 0, "energy": 0.6}, ...]` |
| `hook_points` | list | Timestamps of detected hooks, e.g. `[12.4, 48.0]` |
| `mix_notes` | list | Short strings, e.g. `["vocal upfront", "wide stereo drums", "rolled-off highs"]` |

Scripts may add their own fields, but every script must return at least the keys above (use empty list / unknown string when a key has no data).

Confidence levels and fallback behavior for missing optional dependencies: [`references/advanced-audio-analysis.md`](references/advanced-audio-analysis.md).

For arranger-style triage, extract stems with `scripts/extract_stems.py`, then run
`scripts/per_stem_analysis.py <stems.json>`. Use full-mix Whisper for lyrics;
stems are for timbre, pitch, masking, and mix decisions. If the user asks to
change one instrument, `scripts/hybrid_remix.py` is experimental and requires a
validated transformed stem unless `--allow-stem-cover` is explicitly used for a
smoke test.

## Rate Limits (MiniMax-specific)

Hard limits: 120 RPM, 20 concurrent connections, output URLs expire in 24 hours, cover feature IDs expire in 24 hours. Under Token Plan 3.0 (June 2026+), the actual ceiling is credit-based: **the documented 120 RPM is the API limit, but the Token Plan 3.0 quota is what determines your real ceiling.**

Full detail, Token Plan 3.0 credit-pool mechanics, 429 recovery steps, and the usage-check command: [`references/error-handling.md`](references/error-handling.md#rate-limits-minimax-specific).

## Anti-Sparse (MiniMax-Specific Deep Dive)

The base anti-sparse rules live in [`../music-craft/SKILL.md`](../music-craft/SKILL.md). MiniMax adds a more severe failure mode: **MiniMax interprets "sparse" or "minimal" as "remove all instruments"**, even more aggressively than other providers — never use those words in a prompt without pairing them with an explicit instrument list.

Full deep-dive with observed failure modes, mitigation steps, and the canonical phrase blocklist: [`references/error-handling.md`](references/error-handling.md#anti-sparse-minimax-specific-deep-dive).

## Quality Verification Checklist

Same 8-point checklist as the base skill, plus 4 MiniMax-specific items:

9. **Cover preserves melody recognisably.** If the user said "make it sound like Song X", the new version should be recognisable as Song X's melody with Song Y's style.
10. **Emotion curve matches Song A** (for mashups). The dynamic arc of the output should follow the original's intensity, not flatten to a single energy.
11. **`--avoid` flags are respected.** If the user said "no electronic sounds", the output should not have synths.
12. **Per-flag control worked** (BPM, key, structure). If the user asked for 80 BPM in E minor, the output should be in that range, not "close enough".

## Output Verification (Covers, Mashups, Style Transfer)

After generation, run a post-generation check that is specific to the route. Every cover, mashup, and style-transfer output is verified against its route checklist before delivery.

Route checklists (cover / mashup / style transfer / emotion prompt), failure-signature table, and revision prompt templates: [`references/error-handling.md`](references/error-handling.md#output-verification-covers-mashups-style-transfer).

## Lyrics Optimizer Behavior

Same as the base skill — when `music_generate` is called without explicit lyrics, MiniMax auto-generates. With this skill, you can also call the `lyrics_generation` API directly to preview the lyrics before generation, or to iterate via the `edit` mode.

If the user wants specific words, the `lyrics_generation` API's `edit` mode lets you modify auto-generated lyrics to match the user's intent without regenerating the whole song.

## Reference Map

- [`references/setup-and-preflight.md`](references/setup-and-preflight.md) — extended pre-flight: platform notes, required/optional dependencies, ask-the-user pattern, local analysis memory
- [`references/mmx-flags-reference.md`](references/mmx-flags-reference.md) — full `mmx` CLI flag reference with worked examples
- [`references/examples.md`](references/examples.md) — practical MiniMax examples with routing, first questions, workflow shapes, and prompt/flag lint catches
- [`references/cover-workflow.md`](references/cover-workflow.md) — one-step and two-step cover workflow with payloads, error handling, use cases
- [`references/lyrics-generation.md`](references/lyrics-generation.md) — the `lyrics_generation` API endpoint, both modes, examples
- [`references/mashup-workflow.md`](references/mashup-workflow.md) — two-song mashup workflow, emotion-to-prompt conversion, decision tree
- [`references/emotion-analysis.md`](references/emotion-analysis.md) — 25+ emotion classifications + per-emotion detection cookbook + emotion combinations + the analysis pipeline
- [`references/emotion-delivery.md`](references/emotion-delivery.md) — 21 emotion recipes for the OUTPUT + iteration loop + common mistakes
- [`references/orchestrator-quickstart.md`](references/orchestrator-quickstart.md) — per-input orchestrator commands (audio, two-song pairs), extraction guidance, per-song output layout
- [`references/minimax-generation-caveats.md`](references/minimax-generation-caveats.md) — sequential-run rules, output-file verification, duration-is-a-target caveats, and delivery copy templates
- [`references/short-prompt-recipes.md`](references/short-prompt-recipes.md) — short prompt recipes for reliable cloud iterations under about 500 characters
- [`references/advanced-audio-analysis.md`](references/advanced-audio-analysis.md) — advanced free tools (Essentia, Demucs, Basic Pitch, Music21, CREPE) for deeper analysis when basic librosa/parselmouth is not enough
- [`references/error-handling.md`](references/error-handling.md) — MiniMax-specific error table, recovery patterns, anti-sparse failure recovery
- [`references/free-tool-inputs.md`](references/free-tool-inputs.md) — MiniMax layer: free-tool routing, blocker checks, and prompt/flag conflict lint before analysis
- [`scripts/check_environment.py`](scripts/check_environment.py) — lightweight preflight diagnostic for Python, env vars, CLI tools, and optional packages
- [`scripts/lint_music_request.py`](scripts/lint_music_request.py) — standard-library helper for routing, blocker, missing-field, prompt, lyrics-tag, duration-density, and `mmx` flag conflict checks
- [`scripts/lint_lyrics.py`](scripts/lint_lyrics.py) — standard-library lyrics preflight for section-tag whitelist checks and syllable/BPM duration estimates
- [`scripts/verify_lyrics_alignment.py`](scripts/verify_lyrics_alignment.py) — standard-library post-generation transcript-vs-lyrics overlap check for semantic delivery
- [`scripts/verify_cloud_output.sh`](scripts/verify_cloud_output.sh) — shell helper for file existence, size, MP3 probe, and expected-duration range checks after cloud generation
- [`scripts/batch_cover.py`](scripts/batch_cover.py) — sequential batch wrapper for repeated `music cover` prompts via `generate_with_retry.py`
- [`scripts/per_stem_analysis.py`](scripts/per_stem_analysis.py) — lightweight arranger triage from `extract_stems.py` `stems.json`
- [`scripts/hybrid_remix.py`](scripts/hybrid_remix.py) — experimental preview remix planner; stem-to-cover is gated behind explicit smoke-test consent
- [`scripts/smoke_test.py`](scripts/smoke_test.py) — standard-library smoke tests for pure helper behavior
- [`scripts/`](scripts/) — Python helpers for audio analysis (download, segment, analyze, convert emotion to prompt)
- [`music-source-fetch`](../music-source-fetch/) — private skill (NOT published) that holds the YouTube/JioSaavn/mx3.ch/LRCLib download code Luis uses to fetch source audio + lyrics by title
- [`music-craft`](../music-craft/) — base skill with shared concepts (Pre-Flight, anti-sparse, prompt formula, structure tags, Request Intake, User Preference Flow)
- [`music-craft` → references/free-tool-inputs.md](../music-craft/references/free-tool-inputs.md) — base layer for free tool inputs (web_fetch, web_search, image, memory)
- [`references/changelog.md`](references/changelog.md) — release history (v1.4.1, v1.4.0, v1.3.0, v1.1.0, v1.0.0, v0.3.0); operating guidance lives in the topic references
