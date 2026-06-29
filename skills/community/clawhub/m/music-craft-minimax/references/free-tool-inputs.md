# Free Tool Inputs (MiniMax Layer)

The OpenClaw runtime provides several free tools for input enrichment. The basics (`web_fetch`, `web_search`, `memory`, `browser`) are documented in [`music-craft` → references/free-tool-inputs.md](../../music-craft/references/free-tool-inputs.md). This file covers the **MiniMax layer**: how the free tools compose with MiniMax-specific features (`mmx` CLI, `lyrics_generation` API, cover workflow, emotion analysis, mashup).

## v1.5.0 changes

- **No URL downloads**: YouTube, JioSaavn, mx3.ch audio downloads moved
  to the private `music-source-fetch` skill. To analyze a track from a
  URL, fetch it locally first with that skill, then pass the local path.
- **No image pipeline**: album-art color palette, OCR, face detection,
  VLM captioning, and `--vlm`/`--ocr`/`--faces` orchestrator flags are
  gone. The skill is audio-only.
- **No LRCLib lyrics**: Whisper on the local file is the only lyrics
  source. For LRCLib-quality lyrics of a known mainstream track, use
  `music-source-fetch`.

## Routing and Failure Prevention

Before you analyze anything, classify the request:

- **Text-only style reference**: song name, artist, era, or genre cue with no source audio. Use web search / fetch for style context, not audio analysis.
- **Reference audio (local file)**: actual audio path that should be analyzed before prompt construction. URLs are not accepted in v1.5.0+ — fetch with `music-source-fetch` first.
- **Cover**: preserve melody and decide whether the lyrics stay original, get translated, or get rewritten.
- **Style transfer**: use the reference as style input and keep the output original.
- **Mashup**: decide which source is Song A, which is Song B, and which one contributes content versus style.
- **Emotion prompt**: convert analysis into prompt language only after the target emotional arc is clear.

The [`../scripts/lint_music_request.py`](../scripts/lint_music_request.py) helper emits one of these routes:

| Route | When |
|---|---|
| `base_prompt` | Standard generation, no MiniMax-specific feature needed. |
| `minimax_cover` | Melody-preserving cover from a local audio file. |
| `minimax_mashup` | Two-song mashup (A + B, both identified, both as local files in v1.5.0+). |
| `minimax_style_transfer` | Style transfer that does not preserve the source melody. |
| `minimax_emotion_prompt` | Emotion analysis, or precision `mmx` flag usage. |
| `needs_clarification` | At least one blocker is unresolved; ask the user first. |

### Text-Only Versus Real Audio

The linter distinguishes between a text-only style reference and a real audio source. The route changes accordingly:

**Text-only style reference (route `base_prompt`):**

```bash
# User says: "Make a song like Daft Punk"
python3 scripts/lint_music_request.py --text "Make a synthwave song in the style of Daft Punk."
# -> route: base_prompt, request_type: text_reference
# -> references: "style reference", no audio to analyze
```

In this case, do not try to run `analyze_vocal_emotion.py` on anything. Use `web_search` or `web_fetch` to gather style context (instruments, era, production cues), and build the prompt from that text. The linter returns `references: "style reference"` and no `references_missing` blocker.

**Reference audio file (route `minimax_cover` or `minimax_mashup`):**

```bash
# User says: "Make a reggaeton cover from /tmp/song.mp3"
python3 scripts/lint_music_request.py --text "Make a reggaeton cover from /tmp/song.mp3 with new English lyrics"
# -> route: minimax_cover, request_type: cover
# -> references: "local audio source"
```

In this case, run the analysis orchestrator on the local file. URLs in the request string (YouTube, JioSaavn, mx3.ch) now trigger a soft `url_not_accepted` warning — the operator should fetch the file with `music-source-fetch` and re-run with the local path.

**Both signals together (route `minimax_mashup`):**

```bash
# User says: "Mash up Song A (local file) and Song B (named) into pop"
python3 scripts/lint_music_request.py --text "Mash up /tmp/song_a.mp3 and 'Blinding Lights' into a pop track."
# -> route: minimax_mashup, request_type: mashup
# -> references: "local audio source", no "unclear Song A vs Song B" blocker
```

The linter only emits `minimax_mashup` when both Song A and Song B are clearly identified. A request like "Make a mashup" without naming both sources routes to `needs_clarification` with the "unclear Song A vs Song B assignment" blocker.

Surface blockers before analysis:

- no source file (or only a URL — fetch with `music-source-fetch` first)
- unclear Song A / Song B assignment
- missing target style
- missing lyrics decision
- conflicting cover/style-transfer intent (asking for both "cover" and "style transfer" in the same request)

After analysis and prompt construction, lint the prompt and `mmx` flags together:

- compare the prompt's BPM against `--bpm`
- compare the prompt's key against `--key`
- compare the prompt's structure line against `--structure`
- compare the prompt's duration against the expected length
- compare the prompt's vocal mode against `--vocals`
- compare the prompt's language against `--language`
- compare the prompt's avoid language against `--avoid`
- flag conflicts early instead of letting the generator guess

When conflicts appear, the linter's `retry_guidance` field lists one hint per conflict so the operator can fix prompt + flags together before re-running.

## Compositions with MiniMax Tools

### `web_fetch` + `lyrics_generation`

Fetch a user's draft from a URL, run it through the lyrics API's edit mode for cleanup, then generate.

```bash
# Step 1: Fetch the draft
DRAFT=$(web_fetch(url="https://example.com/user-draft.txt", extractMode="text"))

# Step 2: Edit via MiniMax lyrics API
EDITED=$(curl -s -X POST https://api.minimax.io/v1/lyrics_generation \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg lyrics "$DRAFT" '{
    mode: "edit",
    prompt: "Clean up grammar, add section tags ([Verse], [Chorus], [Break]), keep the user voice",
    lyrics: $lyrics
  }')")

# Step 3: Extract the cleaned lyrics
LYRICS_BODY=$(echo "$EDITED" | jq -r '.lyrics')

# Step 4: Generate with the edited lyrics
mmx music generate \
  --prompt "..." \
  --lyrics "$LYRICS_BODY" \
  --model music-2.6 \
  --out /tmp/song.mp3
```

**Use case:** the user has a draft in a Google Doc, GitHub gist, or any URL. Fetch it, polish it, generate.

### `web_fetch` + cover workflow (translated lyrics)

Fetch the original song's lyrics, translate them via LLM, use in a cover with the new style.

```bash
# Step 1: Fetch original lyrics
ORIGINAL=$(web_fetch(url="https://genius.com/Edith-piaf-non-je-ne-regrette-rien-lyrics"))

# Step 2: LLM translates to the target language (in the LLM's response)
TRANSLATED="[Verse]
No, nada de nada
No, no lamento nada

[Chorus]
Ni el bien que me hicieron
Ni el mal, todo me da igual..."

# Step 3: Use the cover workflow with translated lyrics
python3 scripts/generate_with_retry.py \
  --output-path /tmp/piaf_reggaeton.mp3 \
  -- \
  music cover \
  --prompt "Reggaeton, dembow rhythm, 808 sub-bass, synth pads, passionate Spanish vocal" \
  --audio-file /tmp/piaf_original.mp3 \
  --lyrics "$TRANSLATED" \
  --model music-cover \
  --out /tmp/piaf_reggaeton.mp3
```

**Use case:** the user wants a cover with the original melody but lyrics in their language.

### `web_search` + cover workflow (style reference)

Find covers of a song in the target style, use their characteristics as inspiration.

```bash
# Step 1: Find existing covers
web_search(query="Bohemian Rhapsody bossa nova cover", count=5)

# Step 2: For each interesting result, fetch the page
# (YouTube watch pages are JS-rendered; the search-result page itself usually
# has the description and metadata you need)
web_fetch(url="https://www.google.com/search?q=Bohemian+Rhapsody+bossa+nova+cover")

# Step 3: Extract a style description from the metadata
# (LLM infers: bossa nova, nylon guitar, soft vocal, ~120 BPM)

# Step 4: Apply the inferred style to a cover
python3 scripts/generate_with_retry.py \
  --output-path /tmp/bossa_cover.mp3 \
  -- \
  music cover \
  --prompt "<style description as inferred by the LLM from the search results, including language and vocal style as confirmed with the user>" \
  --audio-file /tmp/original_song.mp3 \
  --lyrics "..." \
  --model music-cover \
  --out /tmp/bossa_cover.mp3
```

**Use case:** the user wants a cover in a style where existing covers are a good reference. Confirm the inferred language and vocal style with the user before locking the prompt (audit SQP-3).

### `memory` + emotion analysis

If the user has prior music preferences in memory, combine with deep audio analysis of a reference track.

```bash
# Step 1: Recall preferences
memory_search(query="music preferences")

# Step 2: Run emotion analysis on a reference the user liked
python3 scripts/analyze_vocal_emotion.py /tmp/liked_song.wav --output /tmp/emotion.json

# Step 3: Build a prompt that combines the emotion with the user's preferred style
python3 scripts/emotion_to_prompt.py \
  --emotion /tmp/emotion.json \
  --style '{"target_style": "user_preferred_genre_from_memory", ...}' \
  --output /tmp/combined_prompt.json

# Step 4: Generate
mmx music generate \
  --prompt "$(jq -r .final_prompt /tmp/combined_prompt.json)" \
  --lyrics "..." \
  --model music-2.6 \
  --out /tmp/personalized_song.mp3
```

**Use case:** the user has a track they liked, and the skill can build a new track that matches both the emotional arc of the reference and the user's typical preferences.

### `web_search` + mashup workflow (Song B style)

For a mashup where Song B is identified by name (no audio available), use web search to gather more info.

```bash
# Step 1: Find information about Song B
web_search(query="\"Song B Name\" style instruments era production", count=5)
web_fetch(url="https://en.wikipedia.org/wiki/Song_B_artist")

# Step 2: Extract BPM, instruments, era, vocal style
# (LLM summarizes from the fetched content)

# Step 3: Build the mashup prompt
PROMPT="Style: $(extracted_style), $(extracted_bpm) BPM, $(extracted_instruments), $(extracted_mood)"

# Step 4: Generate via cover workflow (preserves Song A's melody)
python3 scripts/generate_with_retry.py \
  --output-path /tmp/mashup.mp3 \
  -- \
  music cover \
  --prompt "$PROMPT" \
  --audio-file /tmp/song_a.mp3 \
  --lyrics "..." \
  --model music-cover \
  --out /tmp/mashup.mp3
```

**Use case:** the user names a Song B without providing the audio, and the skill needs to infer the style for the mashup.

## Decision Table: Free Tool + MiniMax Feature

| MiniMax feature | Best free tool combo |
|---|---|
| Standard generation (lyrics unknown) | `web_search` for theme → `lyrics_generation` to draft |
| Standard generation (lyrics known) | `web_fetch` lyrics URL or take user paste |
| Cover with original lyrics | `web_fetch` lyrics from original source |
| Cover with translated lyrics | `web_fetch` original → LLM translate → cover with translated |
| Cover with style reference | `web_search` for existing covers in target style |
| Mashup (both audio) | `scripts/analyze_vocal_emotion.py` on Song A + `analyze_two_songs.py` |
| Mashup (Song A audio, Song B by name) | `web_search` for Song B info + emotion analysis on A |
| Lyrics draft | `lyrics_generation` `write_full_song` mode |
| Lyrics iteration | `lyrics_generation` `edit` mode with specific instructions |
| Iterating on a result | `memory_get` for prior feedback → adjust next prompt |
| Style exploration | `web_search` for "[genre] characteristics" → `web_fetch` Wikipedia |
| Indian/regional music (Bollywood, South Indian) | Fetch metadata with `web_fetch` (Wikipedia, JioSaavn page); download audio with the private `music-source-fetch` skill |

## Privacy and Ethics (MiniMax Layer)

- **Web content may influence the lyrics optimizer in unexpected ways.** If the user wants fully isolated generation (no web influence), skip the free tools and use LLM knowledge only.
- **`mmx` has no "do not use web content" flag.** If isolation is required, run the LLM knowledge step first, then pass the output to `mmx` — no intermediate web calls.
- **Translated lyrics attribution**: when using `web_fetch` to get original lyrics, attribute the original writer in any user-facing documentation. The skill should not paste copyrighted lyrics verbatim into the final song without permission.
- **Memory is private.** The skill should not surface personal details from `memory_*` in error messages, generated songs, or logs.

## When Free Tools Are Not Enough in MiniMax

Some MiniMax features require actual audio analysis (not just metadata):

- **Emotion analysis** (intensity curve, vocal speed) — needs the analysis scripts in `scripts/`
- **Two-song comparison** — needs both audio files
- **Cover feature ID** — needs the audio URL or file (not just metadata)
- **`mmx` cover workflow** — needs `audio` or `audio-file` flag with actual audio

These are documented in [`references/emotion-analysis.md`](emotion-analysis.md), [`references/mashup-workflow.md`](mashup-workflow.md), and [`references/cover-workflow.md`](cover-workflow.md).

## Optional Pip Packages for Advanced Analysis

The advanced audio analysis features described in [`advanced-audio-analysis.md`](advanced-audio-analysis.md) require optional pip packages beyond the base runtime. All are **optional** — the skill works without them, but the advanced features will not be available. (v1.5.0+: the image- and video-pipeline packages are gone — see the v1.5.0 changes section at the top of this file.)

| Package | Install command | What it provides | Size / License | Required? |
|---|---|---|---|---|
| **pyloudnorm** | `pip install pyloudnorm` | LUFS integrated loudness measurement and LRA (loudness range) per [EBU R128](https://tech.ebu.ch/loudness) | ~50 KB / MIT | Optional |
| **autochord** | `pip install autochord` | Automatic chord symbol recognition (CNN/RNN-based) | ~200 MB with model / Apache-2 | Optional, fragile with current Keras/H5 stacks unless pinned |
| **allin1** | `pip install allin1` | Neural song structure segmentation (intro/verse/chorus/bridge/outro) | ~500 MB with model / Apache-2 | Optional, problematic on macOS arm64 via `madmom` |
| **transformers** | `pip install transformers torch` | CLAP zero-shot audio classification for genre/mood/instrument/era | ~2 GB with model / Apache-2 | Optional |
| **openai-whisper** | `pip install openai-whisper` | Lyrics extraction from audio with timestamps | ~75 MB–3 GB (model-dependent) / MIT | Optional |

### Installation

```bash
# Install all optional analysis packages at once
pip install pyloudnorm transformers torch openai-whisper

# Or install individually as needed
pip install pyloudnorm                                    # LUFS/LRA only
pip install autochord                                     # chord detection; verify Keras/H5 compatibility first
pip install allin1                                        # structure segmentation; experimental on macOS arm64
pip install transformers torch                            # CLAP classification
pip install openai-whisper                                # lyrics extraction
```

### Pre-flight check

To verify which optional packages are available at runtime:

```python
import importlib

packages = {
    'pyloudnorm': 'pyloudnorm',
    'autochord': 'autochord',
    'allin1': 'allin1',
    'transformers': 'transformers',
    'openai-whisper': 'whisper',
}

for name, module_name in packages.items():
    try:
        importlib.import_module(module_name)
        print(f"{name}: installed")
    except ImportError:
        print(f"{name}: NOT installed (optional)")
```

If a package is not installed, the skill falls back to the base analysis and omits the corresponding feature from the prompt. No error is raised.

### What each package adds to the prompt

| Package | Prompt dimension added |
|---|---|
| `pyloudnorm` | `dynamics: "quiet/dynamic (LRA X LUFS)"` |
| `autochord` | `harmony: "chord progression I-V-vi-IV in A major"` |
| `allin1` | `structure: accurate segment timing for --structure flag` |
| `transformers` | `genre_tags: ["indie", "melancholic"], mood_tags: ["nostalgic"]` |
| `openai-whisper` | `lyrics: "auto-extracted from audio"` |

### Notes

- `transformers` is the largest install (~2 GB with PyTorch). Install it only if zero-shot classification is needed.
- `allin1` and `autochord` both download pre-trained model weights on first use. The first call may be slow, and both should be verified before use on a new machine.
- `pyloudnorm` is pure Python with no native dependencies — lightweight and fast.

Quick optional dependency checks:

```bash
python3 - <<'PY'
import importlib
checks = ["pyloudnorm", "transformers", "whisper"]
for name in checks:
    try:
        importlib.import_module(name)
        print(f"{name}: installed")
    except ImportError:
        print(f"{name}: missing")
PY
```

### New Analysis Scripts (v0.3.0, v1.5.0 audio-only)

The following audio-only scripts are detected at runtime. Image- and video-pipeline scripts (`analyze_image.py`, `extract_video_features.py`) were removed in v1.5.0.

| Script | Input | What it adds to the prompt |
|---|---|---|
| `scripts/extract_lyrics_whisper.py` | Audio file | Auto-extracted lyrics with `[Verse]` / `[Chorus]` tags (Whisper ASR) |
| `scripts/extract_stems.py` | Audio file (opt-in via `--use-demucs`) | Demucs source separation (vocals/drums/bass/other). Vocal-stem analysis is dramatically cleaner. |
| `scripts/per_stem_analysis.py` | `stems.json` from Demucs | Lightweight per-stem triage for masking, dominant layers, and non-musician recommendations. |
| `scripts/batch_cover.py` | Audio file + JSON prompt list | Sequential cover variants through `generate_with_retry.py`; use `--dry-run` first. |
| `scripts/hybrid_remix.py` | `stems.json` + validated transformed stem | Experimental preview remix; stem-only MiniMax cover is gated behind explicit smoke-test consent. |
| `scripts/track_beats.py` | Audio file | **beat_this** (ISMIR 2024 SOTA) — beat + downbeat positions, BPM with confidence, time signature estimate |
| `scripts/extract_melody.py` | Audio file | **Spotify Basic Pitch** (ICASSP 2022) — polyphonic AMT → MIDI; MIDI-confirmed key + scale modes + interval pattern |
| `scripts/compute_audio_embedding.py` | Audio file | **MERT v1-330M** — 1024-dim music-domain SSL embedding; cosine similarity for "vibe" matching |
| `scripts/classify_instruments.py` | Audio file | **MIT AST** (AudioSet 527-class) — fine-grained instrument / genre tagging (rock, grunge, punk, etc.) |

All scripts follow the same pattern: missing package → script outputs
`{"error": "install with pip install X", ...}` and exits cleanly.

For a unified entry point that dispatches based on input type, use `scripts/analysis_orchestrator.py`:

```bash
# Two audios (mashup) — gets key + BPM compatibility + vocal emotion on Song A
python3 scripts/analysis_orchestrator.py --audio /tmp/a.wav --audio /tmp/b.wav

# Opt-in: Demucs vocal-stem analysis (cleaner pitch/HNR/silence)
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --use-demucs

# Opt-in: Whisper lyrics extraction (tiny ~25s, base ~1min)
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --lyrics --lyrics-model base

# Skip advanced analyses for faster run (beat_this, Basic Pitch, MERT, AST)
python3 scripts/analysis_orchestrator.py --audio /tmp/song.wav --no-advanced
```

## Rate Limits and Cost

| Free tool | Cost | Notes |
|---|---|---|
| `web_fetch` | Free per call | Subject to site rate limits |
| `web_search` | Free per query | May have per-minute limits |
| `memory_*` | Free | Only useful if memory is populated |
| `browser` | Slowest, most expensive | Use as last resort |
| `lyrics_generation` API | Counts against Token Plan | See Token Plan section in SKILL.md |
| `mmx` generation | Counts against Token Plan | See Token Plan section |
| Cover workflow | Counts against Token Plan | Two-step uses 2 calls |

For a single user request, expect 1–5 free tool calls + 1–3 MiniMax API calls. For a complex mashup, may go up to 5–10 free + 5–8 MiniMax.

If a free tool call fails:
- Wait 30 seconds, retry once
- Fall back to a different free tool (e.g., `web_search` instead of `web_fetch`)
- If all free tools fail, ask the user to paste the content directly

If a MiniMax call fails:
- See [`references/error-handling.md`](error-handling.md) for the full error table

## Quick Recap of Free Tools

| Tool | Purpose |
|---|---|
| `web_fetch` | Fetch URL content (lyrics pages, artist Wikipedia pages, genre references) |
| `web_search` | Find lyrics, artist info, genre descriptions |
| `memory_search` / `memory_get` | Recall user's prior music preferences |
| `browser` | JS-heavy site fallback (last resort) |

## MiniMax Compositions (High-Value Combos)

- **`web_fetch` + `lyrics_generation`**: fetch the user's draft from a URL, run it through edit mode for cleanup, generate.
- **`web_search` + cover workflow**: find covers in the target style, extract their characteristics, apply to the user's track.
- **`memory` + emotion analysis**: combine the user's prior preferences with deep audio analysis of a reference track.
- **`web_fetch` + Indian/regional music metadata**: JioSaavn (`jiosaavn.com`) and Wikipedia are good sources for Bollywood, Hindi, Tamil, Telugu, Malayalam, Bengali, and other Indian language music. Fetch the page for metadata (artist, era, instruments), then download the audio with the private `music-source-fetch` skill for analysis.
