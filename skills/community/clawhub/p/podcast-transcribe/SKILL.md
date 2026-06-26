---
name: transcribe
description: "For transcript or subtitle requests involving podcast URLs, public audio URLs/files, or raw transcript cleanup. Generates audio + SRT + TXT artifacts and can optionally clean transcripts with episode-page context."
allowed-tools: Bash(curl:*), Bash(podcast-helper:*), Bash(npx podcast-helper:*), Bash(pnpm dlx podcast-helper:*), Bash(node dist/cli.js:*), Bash(pnpm run build:*)
metadata:
  version: "1.4.1"
  tags: [podcast, transcription, audio, subtitles, asr, cleanup]
---

# Transcribe with podcast-helper

Generate transcript artifacts from a podcast episode, audio file, or raw transcript, with an optional cleanup pass that uses episode-page context.

## Default Workflow

1. Choose a dedicated output directory such as `./out/<episode-slug>/`.
2. Run `npx podcast-helper transcribe <input> --output-dir <dir> --json`.
3. Add `--progress jsonl` only when machine-readable progress is needed.
4. Report the generated artifact paths for audio, `.srt`, and `.txt`.
5. Ask whether the user wants cleanup. Do not run cleanup implicitly.

If you are already inside this repository and `dist/cli.js` exists, `node dist/cli.js ...` is acceptable. Do not default to repository-local build steps outside this repository.
If you are inside this repository and `dist/cli.js` is missing, run `pnpm run build` before using the repo-local entry point.

## Gotchas

- Prefer no-install entry points first: `npx`, then `pnpm dlx`, then a globally installed `podcast-helper`.
- Let the CLI auto-select the engine unless the user explicitly requests a backend or needs offline Apple Silicon transcription.
- Spotify URLs are unsupported because the audio is DRM-protected. Ask for an RSS-backed episode page, Apple Podcasts link, or direct audio URL instead.
- YouTube inputs require `yt-dlp`.
- Generic episode pages sometimes hide audio metadata. If source resolution fails, download the audio separately and rerun with the file path.
- Hosted transcription failures usually come from a missing or wrong provider API key.
- Local `mlx-whisper` runs require `ffmpeg`, `python3`, and a working runtime from `podcast-helper setup mlx-whisper`.
- Keep the raw transcript untouched. Cleanup should write a sibling `*.cleaned.txt`.

## Command Forms

Default:

```bash
npx podcast-helper transcribe <input> --output-dir ./out/<slug> --json
```

Fallbacks:

- `pnpm dlx podcast-helper transcribe <input> --output-dir ./out/<slug> --json`
- `podcast-helper transcribe <input> --output-dir ./out/<slug> --json`
- `node dist/cli.js transcribe <input> --output-dir ./out/<slug> --json` only inside this repository

For offline Apple Silicon:

```bash
npx podcast-helper transcribe <input> --engine mlx-whisper --output-dir ./out/<slug> --json
```

## Cleanup Branch

Only enter cleanup when the user asks for it or already has a raw transcript.

1. Fetch episode context with `curl https://r.jina.ai/<podcast-url>`.
2. Use the page as reference context for obvious ASR repairs, especially names and proper nouns.
3. Do not summarize, invent missing content, or overwrite the raw transcript.
4. Write a sibling `*.cleaned.txt` file.

If no episode URL is available, clean conservatively and explicitly say that external episode context was not used.

## References

- Read `references/inputs-and-engines.md` for supported inputs, engine selection, and dependency notes.
- Read `references/output-contract.md` for the JSON success and failure envelopes and progress handling.
- Read `references/cleanup.md` for detailed cleanup rules and conservative editing guidance.
- Read `references/verification.md` for smoke-test inputs and verification steps.
- Read `references/setup.md` when installing this skill into Claude Code, OpenClaw, or other agents.
