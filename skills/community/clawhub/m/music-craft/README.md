# Music Craft

Generate songs, instrumentals, and lyrics-driven tracks through a disciplined OpenClaw-native workflow.

Current release: v1.5.0.

This skill is **provider-agnostic**. It works with any music backend the OpenClaw runtime exposes via the `music_generate` tool — no special CLI, API, or library required.

## Data and consent

Depending on the chosen backend, prompts, lyrics, reference URLs, or generated/derived music instructions may be sent to a cloud provider. Local backends may download models and write temporary/generated audio files on the user's machine. Ask before installing/downloading large dependencies, uploading user-owned media, or overwriting existing outputs.

## Platform support

This base workflow is effectively OS-neutral: it should work on macOS, Linux, and Windows as long as the active OpenClaw runtime exposes the `music_generate` tool. Platform differences only matter if the runtime provider itself needs local setup.

## What it does

- Translates your request into a production-sheet prompt with anti-sparse guards
- Structures your lyrics (or auto-generated lyrics) with whitelisted section tags
- Calls the runtime's `music_generate` tool
- Verifies duration, loudness, structure, lyrics alignment, and audible quality before delivery
- Documents prompt-length, lyrics-transcription, direct ACE-Step submission, wait-and-collect, and post-generation finalization safeguards

## When to use

Use this skill for any music generation task that does not require:

- cover or style transfer from a reference audio file
- emotion analysis or two-song mashup
- separate `--avoid`, `--bpm`, `--key`, or `--structure` flags

For those, see [`music-craft-minimax`](../music-craft-minimax/) (requires MiniMax Token Plan). Audio input must be a local file path. URLs are not accepted in v1.5.0+; if you want to fetch audio by title from the internet, use the private `music-source-fetch` skill first (not published on ClawHub).

If the request is a standard song, instrumental, jingle, or lyrics-driven track, stay here and infer defaults first.

For exact-duration vocal tracks, prefer the local ACE-Step path documented in
[`references/acestep-generation.md`](references/acestep-generation.md). The
2026-06-12 field run verified 18/18 local ACE-Step jobs at exact requested
duration; MiniMax cloud is faster but approximate.

## Quickstart

This skill should load automatically when the task is clearly music generation. Typical flows:

> "Make an upbeat summer pop song in English, ~3 minutes, with original lyrics about road trips."

> "Here's a poem I wrote. Turn it into a rock ballad with male vocals in Spanish."

> "I need a 30-second lofi jingle for a YouTube intro, no vocals."

The skill reads, auto-detects what it can, asks at most 1–3 targeted questions for the ambiguous parts, then generates.

## Workflow loop

1. Clarify the goal and source material
2. Analyze source audio if available, or accept user-provided analysis
3. Build a production-sheet prompt
4. Select the backend based on vocals, lyrics, length, local/cloud preference, speed, and hardware
5. Validate prompt length, structure, conflicts, and expected duration
6. Generate
7. Verify duration, loudness/peak, file size, audible quality, lyrics alignment, and structure
8. Deliver with a short analysis summary, or iterate with a targeted prompt adjustment

## Reference

For full details, see [`SKILL.md`](SKILL.md).

For practical routing examples, see [`references/examples.md`](references/examples.md).
