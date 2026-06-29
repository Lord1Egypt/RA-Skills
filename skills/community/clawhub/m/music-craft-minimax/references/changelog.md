# Changelog

Release history for music-craft-minimax. Operating guidance lives in the
topic references; this file is history only.

## v1.5.0

v1.5.0 is a **breaking change** that isolates all internet-download code
into the new private `music-source-fetch` skill and removes the album-art
/ face / OCR / VLM image pipeline entirely. The published skill is now
audio-only and accepts only local file paths.

**Removed (moved to `publish/music-source-fetch/`):**
- `scripts/download_youtube.py`, `scripts/download_mx3.py`,
  `scripts/fetch_lyrics_web.py`, `scripts/audio_sources.py`
- `analysis_orchestrator.py` flags: `--youtube`, `--audio-url`,
  `--lyrics-source {web,auto}`
- LRCLib web lyrics lookup; Whisper on the local file is the only lyrics
  source

**Deleted entirely (no replacement):**
- `scripts/analyze_image.py`, `scripts/extract_video_features.py`
- `analysis_orchestrator.py` flags: `--image`, `--video`, `--vlm`,
  `--ocr`, `--faces`
- Album-art color palette, face detection, OCR, VLM captioning flows

**Changed:**
- `check_environment.py` no longer recommends `yt-dlp`; drops `cv2`/`PIL`
  from optional imports
- `lint_music_request.py` URL detection now emits a `url_not_accepted`
  warning and routes to `needs_clarification`; only local file paths
  route to `minimax_cover`
- SKILL.md "Audio Source Fallback Order" replaced with "Audio Source
  (Local Only)"
- `cover-workflow.md` and `mashup-workflow.md` add explicit cloud
  transmission consent paragraphs (audit SQP-2)
- `examples.md` neutralises hardcoded language/locale defaults (audit SQP-3)
- README narrows the auto-load trigger (audit SQP-1)
- Frontmatter `metadata.openclaw.requires.bins` drops `yt-dlp`

**Audit findings resolved by this release:**
- SDI-2 (image OCR/face/VLM pipeline)
- SDI-2 (LRCLib lyrics retrieval copyright exposure)
- SDI-2 (VLM captioning external transmission)
- SQP-2 (LRCLib lookup consent)
- SQP-2 (YouTube/JioSaavn/mx3 download copyright exposure)
- AST4 (`mmx vision describe` subprocess)
- AST4 (VLM keyframe captioning subprocess)
- SQP-3 (hardcoded English/Spanish/Portuguese defaults in examples)
- SQP-1 (auto-load trigger too broad)
- Partial: SQP-2 (cover/mashup cloud transmission — sharpened consent text)

**Audit findings NOT resolved (intentional — core MiniMax cloud feature):**
- E1 (`api.minimax.io` external transmission)
- AST4 (`generate_with_retry.py` subprocess for `mmx`)
- SQP-2 (MiniMax cover preprocess cloud transmission — core feature)

## v1.4.1

v1.4.1 adds lyrics safety checks from field feedback without changing the
overall routing model.

**Scripts and validation:**
- New `scripts/lint_lyrics.py` in both music skills validates section tags
  against the canonical whitelist and estimates lyric pacing from syllables,
  BPM, and target duration.
- `scripts/lint_music_request.py` accepts `--lyrics-file`, surfaces invalid
  lyrics tags as blockers, reports a duration-density estimate, and no longer
  treats a plain prompt mention of "lyrics" as user-provided lyrics.
- New `scripts/verify_lyrics_alignment.py` compares expected lyrics with a
  transcript so semantic lyric mismatch can be caught after generation.
- `scripts/generate_with_retry.py` now rejects `--output-path` for `mmx music
  generate`/`cover` unless the underlying `mmx` command also includes `--out`.

**Documentation:**
- Both skills now document the lyrics tag whitelist, pre-generation lyrics
  linting, post-generation lyrics alignment checks, and the `--out`/`--output-path`
  contract.

## v1.4.0

v1.4.0 packages the arranger-helper expansion and the public-doc cleanup into
the next published release.

**Workflow and routing:**
- Base skill now documents the local ACE-Step arranger helper path more clearly:
  `wait_for_acestep.py`, `extract_stems.py`, and `remix_stems.py`
- MiniMax docs now distinguish fast cloud cover from the slower local ACE-Step
  cover/repaint path without mixing maintainer-specific environment notes

**Scripts and validation:**
- New `batch_cover.py` for sequential MiniMax cover batches through
  `generate_with_retry.py`
- New `per_stem_analysis.py` for lightweight arranger triage from `stems.json`
- New `hybrid_remix.py` for gated experimental remix planning with source-stem
  validation at plan-build time
- Expanded `scripts/smoke_test.py` to cover dry-run batch output and hybrid stem
  validation gates

**Documentation hygiene:**
- Removed maintainer/private machine details from published references
- Replaced user-specific example paths and placeholders with generic examples
- Generalized Windows/WSL notes away from personal managed-network context

## v1.3.0

v1.3.0 folds the 2026-06-12 9-song field run feedback into the public
operator workflow.

**Documentation:**
- Cloud duration caveat strengthened with verified results: 18/18 files saved,
  but duration ranged from 57-135% of requested length (12 truncated, 3 close,
  3 extended)
- New [`references/short-prompt-recipes.md`](short-prompt-recipes.md) gives
  short cloud prompt patterns under about 500 characters
- [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
  now documents SIGTERM/SIGKILL-after-save recovery, MP3 output defaults,
  prompt budget guidance, `--references` flakiness, and local-vs-cloud duration
  comparison data

**Scripts:**
- `generate_with_retry.py` treats a fresh, probeable output file as a
  successful generation after a signal-style return code
- New `verify_cloud_output.sh` checks file existence, minimum size, MP3 format,
  and optional expected-duration range
- `check_environment.py` prints best-effort `mmx` path/version diagnostics

## v1.1.0

v1.1.0 combines the unpublished JioSaavn audio-source work with the later
workflow-hardening improvements into the next real ClawHub release after
v1.0.1.

**Documentation:**
- New [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md) documents sequential-run requirements, output-path verification, and duration-is-a-target behavior
- Vocal-confirm gate and target-length confirmation gate added to the base skill intake workflow
- Exact-duration routing clarified: `music-craft` with ACE-Step is the right tool when exact 3:00+ duration is required; MiniMax is the right tool when speed, cover workflows, or mmx flag control matter more

**Linter (lint_music_request.py):**
- New warning when a prompt requests >150 seconds with lyric-heavy density — advises that MiniMax often returns ~120–150s for those prompts and suggests ACE-Step as the exact-length alternative

**Wrapper script (generate_with_retry.py):**
- New `--output-path` flag moves the generated file to a caller-specified path after success (isolates each run from filename collisions)
- New `--expected-duration-seconds` flag emits a best-effort warning (via ffprobe when available) if output is materially shorter than expected
- Each invocation now uses an isolated temporary working directory so concurrent runs do not collide
- Retry backoff is capped to prevent unbounded delays

### Included scope: JioSaavn audio source additions

v1.1.0 adds **JioSaavn as the third official audio source**, completing the fallback chain for cover, mashup, and style-transfer workflows.

**Audio source fallback order:**

| Priority | Source | When to use |
|---|---|---|
| 1 | YouTube | Global music, well-known international tracks |
| 2 | **JioSaavn** | Bollywood, Hindi, Tamil, Telugu, Malayalam, Bengali, and other Indian regional music |
| 3 | mx3.ch | Niche or regional sources with direct audio links |
| 4 | Local file / alternate URL | When all cloud sources fail |

JioSaavn URLs (`jiosaavn.com`, `www.jio.com/jiosaavn`) are handled by `yt-dlp` directly — no special auth required. Before downloading, inform the user: "I'll download this from JioSaavn to analyze the audio."

The `--youtube` flag on `analysis_orchestrator.py` is reused for JioSaavn auto-detection; both YouTube and JioSaavn URLs are passed the same way.

## v1.0.0

v1.0.0 is the first stable release. It builds on the v0.x series (v0.3.0 / v0.4.0 dev line) with stronger preflight routing, wider prompt/flag consistency, and explicit post-generation verification:

**Preflight routing:**
- `lint_music_request.py` now emits one of six routes: `base_prompt`, `minimax_cover`, `minimax_mashup`, `minimax_style_transfer`, `minimax_emotion_prompt`, or `needs_clarification`
- New blockers: missing Song B, missing lyrics decision, and conflicting cover/style-transfer intent
- A `retry_guidance` array on every conflict so the operator can re-align prompt and flags

**Prompt and flag consistency:**
- Linter now detects conflicts in BPM, key, structure, duration, vocal mode, language, and avoid list
- The canonical `mmx` prompt schema is documented in `examples.md`

**Analysis quality:**
- All analysis scripts converge on a compact `summary` (tempo, key, sections, instrumentation, vocal traits, energy curve, hook points, mix notes)
- Confidence levels (clear, high, medium, low, inferred, missing) attached to every detection
- Missing optional dependencies fall back to a JSON error block instead of failing the whole workflow

**Output verification:**
- Post-generation verification checklists for covers, mashups, style transfer, and emotion prompts
- Eight failure signatures (copied too closely, lost melody, wrong tempo, wrong key, muddy mix, weak chorus, style mismatch, neutral vocals) with matching fixes
- Revision prompt templates that preserve source identity while fixing one specific dimension

**Tests and portability:**
- Smoke tests now cover all new linter routes, the new conflict types, and the stdlib-only import guarantee
- Windows is documented as partial support; scripts stay POSIX-safe, audio tools may need platform install

## v0.3.0

v0.3.0 builds on v0.2.0 with a substantially richer analysis pipeline:

**New analysis scripts (8):**
- `extract_stems.py` — Demucs source separation (vocal/drums/bass/other)
- `track_beats.py` — beat_this beat + downbeat tracking (ISMIR 2024 SOTA)
- `extract_melody.py` — Spotify Basic Pitch polyphonic AMT → MIDI + key/scale
- `compute_audio_embedding.py` — MERT v1-330M music embeddings (vibe similarity)
- `classify_instruments.py` — MIT AST 527-class AudioSet tagging
- `extract_video_features.py` — extended with camera motion + VLM captioning
- `analyze_image.py` — extended with OpenCLIP, OCR, face detection, VLM caption
- `analysis_orchestrator.py` — single entry point, --use-demucs, --vlm, --ocr flags

**New prompt slots (consumed in emotion_to_prompt.py):**
- `beat grid: 4/4 at 150 BPM (confidence 0.80)` from beat_this
- `melodic key from MIDI: E minor; interval motion: mostly leaps; modal character: pentatonic, blues` from Basic Pitch
- `AST-detected sound palette: rock music (0.16), punk rock (0.14), grunge (0.20)` from MIT AST
- `emotion signature from analysis: intense, passionate, dramatic, triumphant` (expanded to 25-emotion classifier)
- `vocal texture in verse: breathier / more intimate than average` (per-section aggregation)
- `tempo: tight, on-beat delivery` (from tempo_consistency)
- `tonal character: dark warm tone, rolled-off highs` (from brightness)
- `instruments detected: electronic / synthetic textures` (from instrument_hints)
- `natural dramatic pauses detected at: 2s (11.7s pause), 20s (3.3s pause)` (from Demucs vocal-stem)
- `style direction: ...` (from analyze_two_songs mashup_plan)

**Bug fixes:**
- parselmouth 0.4.x API (get_value_at_time / get_value_at_xy)
- ffmpeg 8.x image2 muxer workaround (per-frame extraction)
- pylette 5.1+ capital-P import + Pylette fallback
- open_clip 3.3 3-tuple return + get_tokenizer() for tokenizer
- demucs 4.x apply_model API

**Prompting wins (verified end-to-end with a source-audio test case):**
- Mix: 0 silence gaps, 35 pitch bends
- Vocal stem: 19 silence gaps, 49 pitch bends, 2.32 syll/sec
- BPM 150 (4/4) from beat_this, E minor (MIDI-confirmed G# minor)
- AST: "Rock music", "Punk rock", "Heavy metal", "Grunge" — matches the actual band
