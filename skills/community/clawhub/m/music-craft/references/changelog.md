# Changelog

Release history for music-craft. Operating guidance lives in the topic
references; this file is history only.
# v1.8.2

- `extract_stems.py`: the download check now looks for every checkpoint the
  chosen Demucs model needs (read from Demucs' own model lists), so unrelated
  or partial caches no longer count; fails closed if the lists cannot be read.
- `remix_stems.py`: no longer overwrites an existing output unless
  `--overwrite`; paths can never be read as ffmpeg options; explicit
  `shell=False`.
- Consent and privacy: no automatic switch to another cloud provider; Stable
  Audio section says what is sent and asks first; memory-derived web searches
  use generic terms and need the user's OK; unsupported-language recovery and
  lyric language follow the user's choice; capped retries.
- New "Tool Scope" section in SKILL.md.

# v1.8.1

- `acestep_request.py` and `wait_for_acestep.py` now ignore proxy settings and
  refuse HTTP redirects, so a reply can never send a request off the loopback
  host. Smoke test added.
- `extract_stems.py` refuses to let Demucs download model weights unless
  `--allow-model-download` is passed, and documents the download and cache.
- MPS memory-cap troubleshooting rows now ask for the user's OK first.
- LRC example no longer writes a fake `00:00` timestamp for unaligned lines;
  it stops and lists them instead.
- WSL troubleshooting no longer suggests `nohup`.

# v1.8.0

- New `scripts/acestep_request.py`: standard-library helper that sends one
  JSON or multipart request to a loopback ACE-Step server. All reference
  examples now use it instead of raw `curl` calls.
- `scripts/wait_for_acestep.py`: `--expected-seconds` / `--tolerance` reject
  short in-progress intermediates (measured with `ffprobe` when installed);
  `--scan-only` recovers a finished take from the cache when the client hung
  or died; `--api-url` must be loopback. Smoke test added.
- `references/wait-and-collect.md`: long-job recovery table and decision
  (submit once, check the cache before resubmitting, VAE-decode hang, MPS
  crash, server timeout) and a tail-splice recipe for takes that fade out.
- MiniMax: music generation no longer works even for paying accounts (HTTP
  410); all MiniMax routing removed. Added research notes for the
  open-weights MiniMax Music 3 (MLX route, sizes, license), marked not
  verified.
- Safety: the WSL guide now installs `uv` with `pipx install uv` instead of a
  piped remote installer; added a
  memory warning and user consent before `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0`;
  description now names the local helpers and optional stem separation;
  SKILL.md lists what each helper reads, writes and contacts.
- Corrected the claim that conda always provides `xformers` on macOS.

# v1.7.0

- MiniMax music cloud marked as legacy: MiniMax closed its paid Music and
  Lyrics APIs to new users on 2026-08-20, is discontinuing the free music
  models, and `mmx` 1.0.28 no longer has a `music` command.
- Routing now defaults to local ACE-Step for covers and source-audio
  restyles; `music-craft-minimax` is suggested only for accounts that still
  have MiniMax music access. Removed "fast cloud cover" promises.
- Noted MiniMax's open-weights MiniMax Music 3 (Hugging Face) as
  not yet supported or verified by this skill.
- Removed links to a maintainer-local install guide that pointed outside the
  bundle; install guidance now points at the bundled references.
- No script, env var, or binary changes.

# v1.6.0

- Reordered `SKILL.md` for discoverability: added hero sections
  ("What is Music Craft?", "Key Capabilities", "Why use this skill?",
  "Quick Start") at the top of the body. Capabilities are now the
  first thing a visitor reads, before the licensing section.
- Moved the licensing and commercial-use gate to the end of `SKILL.md`
  (preserving all legal content verbatim); data / consent sits just
  above it.
- Updated the frontmatter `description:` to anchor-keyword pack
  (Generate, songs, instrumentals, lyrics-driven tracks, anti-sparse,
  OpenClaw-native, Provider-agnostic, ACE-Step, MusicGen, Stable Audio,
  mmx) for clearer ClawHub routing.
- No behaviour, no env vars, no bins — pure content reordering and
  versioning.



# v1.5.1

- Added a licensing and commercial-use gate for local models and provider
  backends.
- Marked MusicGen as non-commercial because its model weights are CC-BY-NC
  4.0, while keeping ACE-Step's current MIT/commercial-ready status subject
  to checkpoint verification.
- Clarified that each operator must accept backend terms and use their own
  provider credentials.

## v1.5.0

v1.5.0 is a **breaking change** that aligns the base skill with
`music-craft-minimax` v1.5.0: both skills are now audio-only.

**Changed:**
- "When to redirect to music-craft-minimax" no longer mentions
  "audio download from YouTube, JioSaavn, or other URL"
- Audio input must be a local file path; URLs are not accepted
- Image free-tool flow removed (album art / OCR / face / VLM are gone)
- `references/input-workflows.md` deletes Input Type 4 (YouTube URL)
  and Input Type 8 (image)
- `references/free-tool-inputs.md` deletes the `image` tool section
  and the YouTube/JioSaavn download rows
- `references/quality-and-revision.md` deletes the LRCLib "Web Lyrics
  Lookup" subsection

**Companion private skill:**
- `publish/music-source-fetch/` is a new unpublished skill that holds
  the YouTube/JioSaavn/mx3.ch/LRCLib download code Luis uses personally.
  It is never `clawhub publish`-ed.
