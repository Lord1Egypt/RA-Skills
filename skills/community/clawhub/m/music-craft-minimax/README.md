# Music Craft — MiniMax

Advanced music generation for OpenClaw, using the MiniMax Music 2.6 token plan.

Current release: v1.5.0.

This is the **power-user upgrade** of [`music-craft`](../music-craft/). It does everything that skill does, plus the features that require MiniMax:

- Cover and style transfer (preserves melody)
- Two-song mashup (content + style)
- Lyrics generation API
- Emotion-driven prompt engineering
- Fine control via `mmx` CLI (BPM, key, structure, avoid list as separate flags)
- Production helpers: prompt/lyrics linting, retry wrapper, MP3 defaults, lyrics-alignment verification, and loudness finalization

Cloud generation is for speed and MiniMax-native workflows, not exact duration.
The 2026-06-12 field run saved 18/18 cloud outputs, but durations ranged from
57-135% of requested length. Use [`music-craft`](../music-craft/) with local
ACE-Step when exact duration matters.

## Data and consent

This skill may send prompts, lyrics, reference audio, and cover/mashup inputs to MiniMax when the user chooses cloud generation. Audio input must be a **local file path** — URLs are not accepted in v1.5.0+. Use the private `music-source-fetch` skill to fetch audio by title first. There is no image, face, OCR, or VLM pipeline.

## When to use

Use this skill when the task involves:

- cover or style transfer from a local reference audio file (URLs not accepted; use `music-source-fetch` to fetch by title)
- two-song mashup
- lyrics generation via the MiniMax API
- emotion analysis on input audio
- fine parameter control via `mmx` CLI
- fast standard cloud iterations where approximate duration is acceptable

Stay in [`music-craft`](../music-craft/) when the user only needs standard song generation, a text-only style reference without melody preservation, or provider-agnostic prompting. Use MiniMax when the request uses a local reference audio file, needs cover/mashup, lyrics API iteration, emotion-driven prompting, or exact `mmx` flags.

## First Response

- **Cover from local audio**: default to the one-step cover path; ask only if the user wants translated lyrics, edited ASR lyrics, or new lyrics.
- **Style transfer only**: do not use cover unless the melody must survive. Use standard generation plus `mmx` flags when exact BPM/key/structure matter.
- **Two-song mashup**: anchor on Song A. If Song A has audio, use the cover two-step path; if Song B is only named, ask for a short style description.
- **Lyrics API**: use `write_full_song` for blank-page generation and `edit` for revisions.
- **Emotion analysis to prompt**: analyze first, then convert to prompt; ask only for the output type and target language if missing.
- **Exact `mmx` control**: let flags win for BPM, key, structure, and avoid lists.

If the user provides a URL, do not attempt to download it. Tell them this skill accepts only local files, and suggest the private `music-source-fetch` skill if they want auto-download by title.

## Requirements

- `MINIMAX_API_KEY` environment variable (from your MiniMax Token Plan)
- `mmx` CLI (recommended for fine control)
- `ffmpeg` and `librosa` / `parselmouth` (recommended for emotion analysis and cover preprocessing)
- `python3` (required for the analysis scripts)

## Platform support

This workflow is intended to work best on macOS and Linux, where `python3`, `ffmpeg`, and the optional audio/ML packages are easiest to install and run. Windows should be treated as a partial-support target: the concepts still apply, but command examples may need PowerShell equivalents, paths may need adjustment, and some optional audio dependencies may require extra porting or manual setup.

See the **Pre-Flight Check** in [`SKILL.md`](SKILL.md) for the full list and the platform-aware install commands.

Run `python3 scripts/check_environment.py` and `python3 scripts/smoke_test.py` on macOS/Linux. On Windows PowerShell, use `python scripts/check_environment.py` or `py -3 scripts/check_environment.py`, and the same interpreter form for `scripts/smoke_test.py`.

For generated files, verify by file existence and duration, not exit code alone:
`scripts/verify_cloud_output.sh output.mp3 --expected-duration 180`.
For `mmx` generation through the retry wrapper, always pass `--out` inside the
`mmx` command; `--output-path` is only the wrapper's preservation/verification
destination.

## Quickstart

The skill is auto-loaded only when the request explicitly asks for: cover or style transfer from a local audio file, two-song mashup, lyrics generation via the MiniMax API, emotion-curve analysis on input audio, or direct `mmx` flag control. Generic music generation requests stay in `music-craft`. Addresses audit SQP-1.

> "Take this Beyoncé track and turn it into a reggaeton version."

> "I want a mashup of 'Bohemian Rhapsody' style + 'La Vie en Rose' lyrics."

> "Generate lyrics in French about lost love, melancholic, 80s chanson style."

> "Analyze the emotion curve of this audio file and write a prompt that captures the arc."

The skill runs the extended pre-flight, detects input type, asks 1–3 questions for the ambiguous parts, and generates.

## Relationship to the base skill

This skill extends [`music-craft`](../music-craft/). Read that skill first to understand the shared concepts (Pre-Flight, anti-sparse, prompt formula, structure tags, user preference flow). The MiniMax-specific additions live here:

- `mmx` CLI quick reference
- Cover workflow (one-step, two-step)
- Lyrics generation API
- Mashup workflow
- Emotion analysis

## Reference

For full details, see [`SKILL.md`](SKILL.md).

For practical routing examples, see [`references/examples.md`](references/examples.md).
