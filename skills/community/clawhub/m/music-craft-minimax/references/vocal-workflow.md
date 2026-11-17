# Vocal Workflow (MiniMax)

End-to-end reference for **vocal** music generation through `mmx music
generate` on MiniMax Token Plan Plus: pre-flight, prompt and lyrics
preparation, generation, post-processing (loudness + format + metadata),
validation (audio quality + LRC sync + vocal intelligibility), and
delivery. Consolidates the **Gate 5 learnings** from the youtube-studio
vocal pilot programme ([2026-07-29-vocal-music-foundation-plan.md][vocal-plan])
into one place so the agent can run a vocal workflow without re-reading
the engine docs.

> **Before running any multi-output or quota-sensitive vocal run, load**
> [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
> for sequential-run rules, output-file verification, and duration
> caveats. **Before any cloud generation, also load**
> [`references/setup-and-preflight.md`](setup-and-preflight.md)
> and [`references/quota-checking.md`](quota-checking.md).

[vocal-plan]: https://github.com/LuisCharro/youtube-studio/blob/main/docs/superpowers/plans/deprecated/2026-07-29-vocal-music-foundation-plan.md

## Scope and prerequisites

- **Skill:** `music-craft-minimax` (this is the MiniMax-only upgrade of
  [`music-craft`](../../music-craft/)).
- **Operator rules:** one generation at a time (no parallel calls from the
  same session); `--out` is mandatory; `--length` is a hint, not a contract.
- **Token Plan Plus scope (`mmx` CLI, verified against `mmx` 1.0.16):**
  covers `mmx music` (generate + cover), `mmx speech` (synthesize +
  voices), and `mmx image` (generate). **NO video** — `mmx video generate`
  is blocked on Plus by a 3-hour rolling rate limit (Hailuo video lives on
  Max/Ultra). This skill uses `mmx music` only; `mmx speech` / `mmx
  image` are reference-only and stay in `youtube-studio` or a future
  `voice-craft-minimax` skill.
- **Music model on Plus (mmx-supported, 2026-07-30):** `music-2.6`
  (default, paid), `music-2.6-free` (lower RPM), `music-2.5+` and
  `music-2.5` (legacy), `music-cover` / `music-cover-free` (cover).
  `music-3.0` is the latest API model but is **not yet exposed** by the
  `mmx` CLI — do not pass `--model music-3.0` today.
- **Required env / binaries:** `MINIMAX_API_KEY`, `python3` ≥ 3.9,
  `ffmpeg`, `mmx`. Optional but recommended for the validation stage:
  `numpy`, `soundfile`, `pyloudnorm` (LUFS), `mutagen` (metadata),
  Whisper (`faster-whisper` preferred for lyrics re-transcription).
- **Skill scripts reused below:** `scripts/check_environment.py`,
  `scripts/lint_music_request.py`, `scripts/lint_lyrics.py`,
  `scripts/generate_with_retry.py`, `scripts/verify_lyrics_alignment.py`,
  `scripts/finalize_track.sh`, plus the test analyzers in
  `../../tests/analyzers/` (`audio_quality.py`, `lrc_validator.py`,
  `metadata_checker.py`).
- **Cross-references to load alongside this doc:**
  [`mmx-flags-reference.md`](mmx-flags-reference.md) (full flag table),
  [`lyrics-generation.md`](lyrics-generation.md) (the `lyrics_generation`
  API), [`emotion-analysis.md`](emotion-analysis.md) (when the user
  supplies source audio), and [`mmx-recipe-pattern.md`](mmx-recipe-pattern.md)
  / [`quota-checking.md`](quota-checking.md) for the wrapper pattern and
  quota preflight.

## Gate 5 learnings (youtube-studio, distilled)

The 2026-07-29 vocal music foundation plan shipped Gates 0-4 (request
contract, MiniMax command shape, ACE-Step runner payload, capabilities).
Gate 5 is the human-gated pilot phase — the real cloud vocal attempts
that surface what the engine docs do not say. The lessons relevant to
this skill's vocal workflow:

1. **MiniMax vocal quality is good but not perfect.** Vocal intelligibility
   depends more on **lyric density** (6-10 syllables/line, ~25-40 words for a
   30 s pilot) and **prompt composition** than on inference-time knobs.
   `music-2.6` lands near -16 LUFS / -1 dBTP naturally; further loudness
   work goes to a separate normalized copy, not to the diffusion
   parameters ([ace-step-vocal-research-local-2026-07-30.md][local-research] § 4,
   [ace-step-vocal-research-web-2026-07-30.md][web-research] § A.5).

[local-research]: https://github.com/LuisCharro/youtube-studio/blob/main/docs/research/ace-step-vocal-research-local-2026-07-30.md
[web-research]: https://github.com/LuisCharro/youtube-studio/blob/main/docs/research/ace-step-vocal-research-web-2026-07-30.md

1. **Pre-processing matters more than people expect.**
   - **Vocal isolation (Demucs) on the source** helps when the source
     audio is dirty and you want clean vocal-stem features for prompt
     building; do **not** feed Demucs-isolated vocals into Whisper for
     lyrics — it measurably worsens transcription WER
     ([orchestrator-quickstart.md](orchestrator-quickstart.md)).
   - **Lyrics cleanup** before generation beats prompt-level fixes after.
     Drop unwhitelisted bracket tags, normalize repeated `Section N` /
     `Verse 3` labels from Whisper, and trim repeated lines.
   - **Prompt engineering for vocals** is a one-line addition to the
     10-slot production-sheet prompt: a "vocal-forward mix direction"
     plus "lead vocal timbre / register / diction" descriptor.

2. **Post-processing helps when done at matched loudness.**
   - Cloud outputs land around -8 to -12 LUFS but true peaks near 0 dBFS;
     normalizing for **delivery** (separate copy) is correct; chasing
     peaks at diffusion time is wrong.
   - Streaming-friendly targets are `-16 LUFS / -1 dBTP / LRA 11` — this
     is the value `scripts/finalize_track.sh` already uses and what
     `ffmpeg loudnorm` should emit.
   - Format conversion (mp3 192 kbps for delivery; wav 48 kHz for archive
     / downstream DSP) is best done **after** loudness normalization.

3. **Quota management is the real ceiling.** MiniMax Token Plan Plus
   advertises 120 RPM, but the **5-hour rolling session quota** is what
   actually throttles. Vocal runs are slightly more expensive than
   instrumental (lyrics pipeline + ASR on cover) but they are **still
   included in the subscription** — no per-attempt billing on Plus. The
   live check is `mmx quota show --output json`; the recipe layer is
   `mmx_quota_show()` (see [`mmx-recipe-pattern.md`](mmx-recipe-pattern.md)
   and [`quota-checking.md`](quota-checking.md) § Live quota check).

4. **Human audition is mandatory for vocal selection.**
   `requested_lyrics_sha256` proves the **requested** lyrics text, not
   what the model actually sang. Treat the hash as a receipt for the
   request, not as proof of fidelity
   ([MUSIC-CAPABILITIES.md][music-cap] § 12 Vocal capabilities Gate 2).

[music-cap]: https://github.com/LuisCharro/youtube-studio/blob/main/docs/capabilities/MUSIC-CAPABILITIES.md

1. **Gate 5 quality checklist (human gates):**
   intelligibility, vocal presence, choir cleanliness, truncation,
   artifacts, loudness. The skill encodes each as an automated check
   below where possible (LUFS, peak, silence ratio, clipping) and
   explicitly flags the rest as "listen by ear" steps in the validation
   stage.

## Workflow overview

```
┌────────────────────────────────────────────────────────────────────┐
│ Stage 1 — PRE-FLIGHT                                              │
│  - mmx quota show --output json   (5h session headroom)            │
│  - check_environment.py           (deps + key + binaries)          │
│  - classify the request           (cover / standard / mashup)       │
│  - prepare prompt + lyrics        (lint both before generation)     │
│  - build argv                     (vocal command shape; see § 3)   │
├────────────────────────────────────────────────────────────────────┤
│ Stage 2 — GENERATION                                              │
│  - mmx music generate             (--lyrics --vocals --language;   │
│                                    no --instrumental)               │
│  - generate_with_retry.py         (timeout 600; 3 transient        │
│                                    retries; signal-recover)         │
│  - mmx_recipe pattern (optional)  (MMXReceipt, dry, check_quota)   │
├────────────────────────────────────────────────────────────────────┤
│ Stage 3 — POST-PROCESSING                                         │
│  - ffmpeg loudnorm                (delivery: -16 LUFS / -1 dBTP)   │
│  - format conversion              (mp3 192 kbps delivery; wav      │
│                                    48 kHz archive)                  │
│  - metadata embedding             (title, artist, album, ISRC,      │
│                                    lyrics + LRC sidecar)            │
├────────────────────────────────────────────────────────────────────┤
│ Stage 4 — VALIDATION                                              │
│  - audio_quality.py               (LUFS, peak, SNR, clipping)      │
│  - lrc_validator.py               (header + timestamps + order)     │
│  - verify_lyrics_alignment.py     (ASR vs requested lyrics)        │
│  - human listen                   (intelligibility + choir +        │
│                                    truncation — cannot automate)    │
├────────────────────────────────────────────────────────────────────┤
│ Stage 5 — DELIVERY                                                │
│  - per-song subfolder             (~/Music mix/<project>/<slug>/)   │
│  - archive copy                   (wav 48 kHz)                      │
│  - delivery copy                  (mp3 192 kbps loudnorm)           │
│  - receipts + LRC + metadata      (sidecars for downstream tooling)│
└────────────────────────────────────────────────────────────────────┘
```

Each stage is detailed below. The end-to-end script that ties them
together lives in [§ End-to-end example](#end-to-end-example).

---

## Stage 1 — Pre-flight

### 1.1 Quota check

A vocal `mmx music generate` call is roughly **1 Plus unit** on Plus;
`mmx music cover` is ~1 (one-step) or ~2 (two-step). The 5-hour pool
(~4,500 M2.7-equivalent calls) is the real ceiling, not RPM.

```bash
# Live human-readable quota snapshot
mmx quota show

# Machine-readable for scripts / preflight
mmx quota show --output json
```

If `current_interval_status` is `0` (exhausted) or `1` (warning), **wait**
until the rolling 5-hour window refills or drop down to a low-priority
mode. See [`quota-checking.md`](quota-checking.md) § Live quota check
for the JSON shape and the wait-vs-batch decision tree.

### 1.2 Environment check

```bash
python3 scripts/check_environment.py
```

Required for the vocal workflow:

| Check | Why it matters for vocals |
| --- | --- |
| `MINIMAX_API_KEY` | Token Plan Plus auth |
| `mmx` on `PATH` | `mmx music generate --lyrics --vocals --language` |
| `python3` ≥ 3.9 | Lint scripts, post-processing helpers, analyzers |
| `ffmpeg` on `PATH` | Loudness normalization + format conversion |
| `pyloudnorm`, `soundfile`, `numpy` | LUFS + audio quality analysis |
| `mutagen` | mp3 metadata embedding (optional but recommended) |
| `faster-whisper` (or `whisper`) | Lyrics re-transcription for verification |

Missing optional packages turn some validation checks into warnings
instead of hard failures — see [`audio_quality.py`](../../tests/analyzers/audio_quality.py)
for the threshold table.

### 1.3 Classify the request

Match the user's request to a route via `scripts/lint_music_request.py`:

| Route | When |
| --- | --- |
| `base_prompt` | New song, no source audio, vocal mode. |
| `minimax_cover` | Local source audio + change style, **preserve melody**. |
| `minimax_style_transfer` | Local source audio + change style, **do not** preserve melody. |
| `minimax_mashup` | Two songs (A + B) combined — content from A, style from B. |
| `minimax_emotion_prompt` | Source-audio emotion analysis feeds the prompt. |
| `needs_clarification` | Blockers — ask before generating. |

The vocal command shape applies to all five routes; only the prompt
content and (for cover/mashup) the source-audio upload changes.

### 1.4 Lyrics preparation

Lyrics are the single most failure-prone input. Run **all three** before
generating:

1. **`scripts/lint_lyrics.py`** — whitelist the structure tags, check
   syllable / BPM density, flag repeated sections and orphan brackets.
2. **`scripts/lint_music_request.py --lyrics-file`** — runs the lyrics
   lint plus the prompt-vs-flag conflict checks.
3. **Read the lyrics by hand.** Final acceptance is human; do not let a
   clean lint pass substitute for "does this actually sing well?".

**Lyric density rule (intelligibility):** aim for **6-10 syllables per
line** and **25-40 words for a 30 s pilot**. Faster lines than that get
dropped consonants; slower lines get verbose delivery. The same rule
applies to longer songs — scale the words up, not the per-line density.

**Whisper re-transcription (optional, for sanity):** if the lyrics came
from `extract_lyrics_whisper.py`, run Whisper on the **full mix**
(not on Demucs-isolated vocals) and sanity-check the language, length,
and look for hallucinations. Default model is `medium`; `large-v2` is
better on sung / multilingual audio and `small` is risky.

### 1.5 Prompt + flag composition (vocal command shape)

The exact command shape for a vocal `mmx music generate` call
([MUSIC-CAPABILITIES.md][music-cap] § 12 Gate 2):

```bash
mmx music generate \
  --prompt "<production-sheet prompt, max 2000 UTF-8 bytes>" \
  --lyrics-file "<path/to/lyrics.txt, max 3500 chars>" \
  --vocals "<vocal description>" \
  --language "<en | es | fr | it | pt>" \
  --genre "<genre>" \
  --mood "<mood>" \
  --instruments "<instruments>" \
  --bpm <int> \
  --key "<key>" \
  --structure "<structure tags>" \
  --avoid "<avoid list>" \
  --model music-2.6 \
  --out "<final.mp3>" \
  --timeout 600
```

Key invariants — enforced by the lint script:

- **Vocal command shape:** `--lyrics` (or `--lyrics-file`), `--vocals`,
  `--language`. **Omit `--instrumental`.** Including `--instrumental`
  and `--lyrics` together is the most common silent-broken case.
- **Prompt ≤ 2,000 UTF-8 bytes** (`lint_music_request.py` warns at
  1,800; errors at 2,000; observed API rejection at 2,079).
- **Lyrics ≤ 3,500 characters.**
- **Language is the v1 allowlist** `en, es, fr, it, pt` — this matches
  the `LANGUAGE_PATTERNS` table in `scripts/lint_music_request.py:28-34`
  and the youtube-studio Gate 0 #3 decision. **Do not pass `--language zh`
  or `--language ja`**; the engine will accept the flag but produce
  noticeably worse vocal delivery.
- **Vocal mode is `lead` or `choir`.** `lead-choir` is dropped from v1
  because both MiniMax and ACE-Step treat mode as a caption suffix —
  not an API control. If the user says "lead with choir", map it to
  `--vocals "clear lead vocal with warm backing choir"` and treat the
  choir as best-effort caption-driven cue. Linter emits a soft warning
  on bare `lead-choir` token in the prompt.
- **Anti-sparse guard.** Always include explicit instruments and the
  `ALL instruments ALWAYS playing` block. MiniMax interprets "sparse",
  "minimal", "intimate" aggressively — see
  [`references/error-handling.md`](error-handling.md#anti-sparse-minimax-specific-deep-dive).

---

## Stage 2 — Generation

### 2.1 Direct `mmx` invocation (simple path)

```bash
mmx music generate \
  --prompt "Indie pop, 96 BPM, warm electric guitar, fingerpicked acoustic,
melodic bass, steady brushed drums, intimate female lead vocal in English,
vocal-forward mix, restrained reverb, wide chorus" \
  --lyrics-file /tmp/lyrics.txt \
  --vocals "clear lead vocal, breathy verses, brighter choruses" \
  --language en \
  --genre "indie pop" \
  --mood "warm nostalgic" \
  --instruments "electric guitar, acoustic guitar, bass, brushed drums, piano" \
  --bpm 96 \
  --key "G major" \
  --structure "intro-verse-pre_chorus-chorus-verse-pre_chorus-chorus-bridge-chorus-outro" \
  --avoid "a cappella, sparse, minimal, electronic sounds, clipping" \
  --model music-2.6 \
  --out /tmp/vocal_pilot.mp3 \
  --timeout 600
```

**Verify after every run:**

```bash
test -f /tmp/vocal_pilot.mp3 || {
  echo "ERROR: output not found at /tmp/vocal_pilot.mp3" >&2
  exit 1
}
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels \
        -show_entries format=duration,bit_rate \
        -of default=nw=1 /tmp/vocal_pilot.mp3
```

If the file exists and `ffprobe` returns a positive duration, the
generation succeeded even if the CLI exited non-zero
(see [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
§ Output-file handling).

### 2.2 Skill wrapper — `generate_with_retry.py` (recommended)

The skill wrapper adds transient retry (3 attempts, exponential backoff
5s → 15s → 45s), `--timeout 600` by default, isolated `run_dir`, output
move, and duration warning when actual < expected × 0.7:

```bash
python3 scripts/generate_with_retry.py \
  --output-path ~/Music\ mix/<project>/<song-slug>/M1_vocal_pilot.mp3 \
  -- music generate \
    --prompt "..." --lyrics-file /tmp/lyrics.txt --vocals "..." \
    --language en --model music-2.6 \
    --out ~/Music\ mix/<project>/<song-slug>/M1_vocal_pilot.mp3
```

The wrapper's `--output-path` and `mmx --out` are **both required** —
the wrapper preserves the file at `--output-path` and verifies it
post-call; `mmx --out` is the CLI's destination. See
[`minimax-generation-caveats.md`](minimax-generation-caveats.md) for the
signals-after-save detection (`SIGNAL_AFTER_SAVE_CODES = {-15, -9, 137, 143}`).

### 2.3 `mmx_recipe` pattern (typed receipts + dry-run)

For batch or CI-driven runs where you want a structured receipt and a
preview without invoking the CLI, follow the
[`mmx_recipe` pattern](mmx-recipe-pattern.md). The reference
implementation lives at
`~/youtube-studio/tools/mmx_recipe.py` (read-only). This skill does
**not** ship a parallel `mmx_recipe.py`; the planned refactor
([roadmap v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md)) folds the
typed-receipt shape and `--dry` flag into `generate_with_retry.py`.

Quick example showing the shape (sketch only — does not run):

```python
from dataclasses import dataclass
from pathlib import Path
import subprocess, time

@dataclass(frozen=True)
class MMXReceipt:
    argv: tuple[str, ...]
    output_path: Path | None
    returncode: int
    elapsed_s: float
    stdout: str
    stderr: str
    quota: dict | None = None
    dry: bool = False

def mmx_music_generate(*, prompt, lyrics_file, vocals, language,
                       out_path, model="music-2.6",
                       dry=False, check_quota=False):
    argv = ("mmx", "music", "generate",
            "--prompt", prompt,
            "--lyrics-file", lyrics_file,
            "--vocals", vocals,
            "--language", language,
            "--model", model,
            "--out", str(out_path))
    if dry:
        return MMXReceipt(argv=argv, output_path=out_path,
                           returncode=-1, elapsed_s=0.0,
                           stdout="", stderr="", dry=True)
    quota = (json.loads(subprocess.check_output(
        ("mmx", "quota", "show", "--output", "json"), text=True))
        if check_quota else None)
    t0 = time.monotonic()
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    return MMXReceipt(argv=argv, output_path=out_path,
                       returncode=proc.returncode,
                       elapsed_s=time.monotonic() - t0,
                       stdout=proc.stdout, stderr=proc.stderr,
                       quota=quota)
```

Use `dry=True` for `--dry-run` preflights and `check_quota=True` to
attach the live `mmx quota show` snapshot to the receipt so the
audit log knows what was on hand when the call fired.

---

## Stage 3 — Post-processing

### 3.1 Loudness normalization (delivery copy)

Cloud vocal outputs land around -8 to -12 LUFS with peaks near 0 dBFS.
The streaming target is `-16 LUFS / -1 dBTP / LRA 11`. Use the existing
helper:

```bash
# Default path (refuses to overwrite existing output)
scripts/finalize_track.sh <input.mp3> <output.mp3>

# Overwrite if needed
scripts/finalize_track.sh --overwrite <input.mp3> <output.mp3>
```

The helper runs:

```bash
ffmpeg -y -i input.mp3 -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k output.mp3
```

**Why a separate copy, not in-place gain.** MiniMax output already has
a high crest factor (peaks near full scale, RMS 15-16 dB below). Pushing
peak gain to chase loudness overshoots integrated LUFS. Match loudness
**after** the fact on the delivery copy and keep the raw original for
audition and debugging.

### 3.2 Format conversion

| Use case | Format | Command |
| --- | --- | --- |
| Delivery (music apps, podcast hosts) | mp3 192 kbps stereo, 44.1 kHz | `ffmpeg -i input.mp3 -codec:a libmp3lame -b:a 192k -ar 44100 delivery.mp3` |
| Archive (lossless, downstream DSP) | wav 48 kHz 24-bit stereo | `ffmpeg -i input.mp3 -codec:a pcm_s24le -ar 48000 -ac 2 archive.wav` |
| Mastering engineer / label | flac 48 kHz | `ffmpeg -i input.mp3 -codec:a flac -ar 48000 archive.flac` |
| Re-transcription / Whisper | mp3 128 kbps (smaller, ASR doesn't need hi-fi) | `ffmpeg -i input.mp3 -codec:a libmp3lame -b:a 128k asr.mp3` |

The skill's existing `finalize_track.sh` already emits 48 kHz MP3 — that
is good for delivery but **lossy**; pair it with a separate wav/flac
archive copy when the user wants to remaster.

### 3.3 Metadata embedding

For mp3 files, use `mutagen` (or `ffmpeg -metadata`):

```python
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, USLT, SYLT

audio = MP3("delivery.mp3", ID3=ID3)
audio.add_tags()
audio.tags.add(TIT2(encoding=3, text=["Vocal Pilot — Indie Pop"]))
audio.tags.add(TPE1(encoding=3, text=["Operator"]))
audio.tags.add(TALB(encoding=3, text=["Vocal Pilot EP"]))
audio.tags.add(TDRC(encoding=3, text=["2026"]))
audio.tags.add(TCON(encoding=3, text=["Indie Pop"]))
audio.save()
```

For **synced lyrics (LRC + ID3 SYLT)**, embed both:

```python
from mutagen.id3 import SYLT, USLT

# Unsynchronized lyrics
audio.tags.add(USLT(encoding=3, lang="eng", desc="",
                    text=open("lyrics.txt").read()))

# Synchronized lyrics (LRC timestamps in milliseconds)
lrc = open("song.lrc").read()
pairs = []
for line in lrc.splitlines():
    m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", line)
    if m:
        ms = int(m.group(1)) * 60_000 + int(float(m.group(2)) * 1000)
        pairs.append((ms, m.group(3).strip()))
audio.tags.add(SYLT(encoding=3, lang="eng", format=2, type=1,
                    desc="", text=pairs))
audio.save()
```

For mp4 / m4a, use `mutagen.mp4.MP4` with `©lyr` (unsynced) and skip
the synced variant.

### 3.4 LRC sidecar

A plain-text `song.lrc` next to the audio is the simplest sync format.
Header format:

```text
[ar:Vocal Pilot Artist]
[ti:Vocal Pilot — Indie Pop]
[al:Vocal Pilot EP]
[length:03:24.50]
[offset:0]

[00:08.12]First sung line
[00:13.40]Second sung line
[00:21.05][Chorus]
[00:21.05]Chorus line one
```

Validate with `../../tests/analyzers/lrc_validator.py` (see [Stage 4](#stage-4--validation)).

---

## Stage 4 — Validation

### 4.1 Audio quality analyzer

```bash
python3 ../../tests/analyzers/audio_quality.py \
    ~/Music\ mix/<project>/<song-slug>/M1_vocal_pilot_finalized.mp3 --json
```

The analyzer (in [`../../tests/analyzers/audio_quality.py`](../../tests/analyzers/audio_quality.py))
measures and reports:

| Metric | Target for vocal delivery | Source |
| --- | --- | --- |
| `duration_s` | matches requested length ± 25% | `minimax-generation-caveats.md` |
| `sample_rate_hz` | ≥ 44,100 | cloud default 44,100; finalize bumps to 48,000 |
| `channels` | 2 (stereo) | required for streaming |
| `peak_dbfs` | ≤ -1.0 (post-loudnorm) | streaming true-peak target |
| `rms_dbfs` | -16 to -10 | correlates with integrated LUFS |
| `lufs` | -16.0 ± 1.0 | streaming target |
| `silence_ratio` | < 0.30 | high ratio → anti-sparse guard failed |
| `clipping_ratio` | < 0.001 | > 0.1% → over-limited / clipped input |
| `snr_db` | > 20.0 | < 20 dB → noisy source or bad prompt |

Exit codes: `0` = pass, `1` = one or more thresholds violated,
`2` = could not analyze file.

### 4.2 LRC validator

```bash
python3 ../../tests/analyzers/lrc_validator.py \
    ~/Music\ mix/<project>/<song-slug>/M1_vocal_pilot.lrc --json
```

Checks:

- Header format `[ar:artist]`, `[ti:title]`, `[al:album]`, `[length:duration]`.
- Timestamps in `[mm:ss.xx]` or `[mm:ss.xxx]` format.
- Chronological ordering (timestamps must be non-decreasing).
- Empty lyrics lines emit a warning (not an error).
- File is UTF-8.

Exit codes: `0` = valid, `1` = invalid, `2` = could not parse.

### 4.3 Metadata checker

```bash
python3 ../../tests/analyzers/metadata_checker.py \
    ~/Music\ mix/<project>/<song-slug>/M1_vocal_pilot_finalized.mp3 --json
```

Checks:

- File format (`mp3`, `wav`, `flac`, `ogg`, `m4a`, `aac`).
- Duration, sample rate, bit depth (wav), bitrate (mp3), channels.
- Encoding (signed PCM, float, etc.) for wav.

### 4.4 Lyrics alignment (semantic verification)

```bash
python3 scripts/verify_lyrics_alignment.py \
    --expected /tmp/lyrics.txt \
    --transcript /tmp/whisper_transcript.txt \
    --output /tmp/lyrics_alignment_report.json
```

The script strips structure tags and stopwords, then computes word-set
overlap. **High overlap** ≠ model sang the lyrics correctly — it just
means the right words are in the audio somewhere. Use the report as a
go / no-go gate, then **listen by ear** for the final acceptance.

### 4.5 Vocal intelligibility — human listen gate

Automated checks cannot reliably judge whether the lead vocal is
intelligible (cues: consonant clarity, breath-vs-pressed delivery,
choir balance, sibilance harshness, chorus lift, truncation artifacts).
The Gate 5 acceptance rubric (from the youtube-studio vocal plan):

| Check | Pass criterion | Tool |
| --- | --- | --- |
| **Intelligibility** | Lyrics are recognizable at the chorus without subtitles | ear |
| **Vocal presence** | Lead sits above the bed at the verse (not buried) | ear + LUFS comparison |
| **Choir cleanliness** | Backing vocals do not clash with lead | ear (if `mode=choir`) |
| **Truncation** | No clipped final word / fade-out cut mid-syllable | ear + `audio_quality.silence_ratio` |
| **Artifacts** | No clicks, pops, distortion in first 10 s | ear + `audio_quality.clipping_ratio` |
| **Loudness** | Comfortable at 0.5-1.0 system gain; not jarring | ear + `audio_quality.lufs` |

If **any** check fails, follow the iteration loop in the troubleshooting
section below — do not retry with the same seed and prompt.

---

## Stage 5 — Delivery

### 5.1 Per-song subfolder layout

The skill convention (from `SKILL.md` Output File Layout):

```
~/Music mix/<project>/<song-slug>/
├── M1_<song-slug>.mp3              # raw cloud output (archive)
├── M1_<song-slug>_finalized.mp3    # delivery copy (loudnorm)
├── M1_<song-slug>_archive.wav      # lossless archive
├── M1_<song-slug>.lrc              # synced lyrics sidecar
├── <song-slug>_analysis.json       # analysis orchestrator output
├── <song-slug>_lyrics.txt          # exact lyrics passed to mmx
├── <song-slug>_<style>_prompt.txt  # exact prompt text
├── M1_<song-slug>_receipt.json     # MMXReceipt (if mmx_recipe used)
└── M1_<song-slug>_validation.json  # audio_quality + lrc + alignment report
```

### 5.2 Archive

The raw cloud MP3 and the wav archive stay as the "source of truth" for
re-mastering. If the user wants to re-issue a louder version, a
different master, or a different LRC timing, regenerate from these.

### 5.3 Delivery

Hand the user the `*_finalized.mp3` and the `*.lrc` sidecar (and the
embed version of the LRC inside the mp3 ID3 SYLT frame). Mention:

- Actual duration vs requested (cloud duration is a target, not a
  guarantee — see [`minimax-generation-caveats.md`](minimax-generation-caveats.md)).
- Any caveats from the validation report.
- Any human-listen issues that survived into the final mix (so the
  reviewer knows what to listen for).

### 5.4 Receipts

If you used the `mmx_recipe` pattern with `check_quota=True`, the
receipt carries the live quota snapshot. Save this alongside the audio
so audits can replay "what quota was on hand when this was generated?"
later. Otherwise, capture the key fields by hand:

```json
{
  "argv": ["mmx", "music", "generate", "..."],
  "output_path": "M1_vocal_pilot.mp3",
  "returncode": 0,
  "elapsed_s": 47.2,
  "model": "music-2.6",
  "lyrics_sha256": "<requested_lyrics_sha256>",
  "quota": {
    "current_interval_status": 3,
    "remaining_5h_units": 4102
  },
  "validation": {
    "lufs": -15.9,
    "peak_dbfs": -1.2,
    "snr_db": 32.1,
    "alignment_overlap": 0.86,
    "human_intelligibility": "pass",
    "notes": "..."
  }
}
```

---

## Pre-processing techniques

### P.1 Vocal isolation (Demucs)

For source-audio analysis only — do **not** feed Demucs-isolated vocals
into Whisper ([orchestrator-quickstart.md](orchestrator-quickstart.md)
guidance). Use Demucs for **timbre/pitch feature extraction**:

```bash
python3 scripts/extract_stems.py /tmp/source.wav --out-dir /tmp/stems/
python3 scripts/per_stem_analysis.py /tmp/stems/stems.json \
    --output /tmp/stems/per_stem_report.json
```

The `htdemucs` model is the standard 4-stem option (vocals / drums /
bass / other). `htdemucs_ft` has non-commercial weight licensing —
gated. `htdemucs_6s` adds guitar / piano but with quality caveats.

### P.2 Prompt engineering for vocals

The vocal addition to the 10-slot production-sheet prompt is a
**vocal-forward mix direction** plus a **lead-vocal timbre / register /
diction** descriptor. Example of an effective vocal prompt slot:

```text
clear lead vocal in <language>, <gender> <register> voice,
crisp consonants and clear diction, intimate vocal-forward studio mix,
restrained reverb, no clipping, no harsh sibilance
```

Two-line "compact sentence" form (matches the ACE-Step card's example
and works well on MiniMax too):

```text
Uplifting synth-pop with punchy drums, warm analog bass and bright guitars;
warm female soprano lead in English, crisp consonants and clear diction,
intimate vocal-forward studio mix, restrained reverb, wide chorus.
```

What to **avoid** in the vocal slot:

- "Sparse", "minimal", "intimate" without an explicit instrument list.
- "Powerful" or "epic" alone (the model interprets as compressed and
  clipped).
- Negative descriptions ("not harsh", "no clipping") without a positive
  alternative ("warm", "rounded", "soft attack").
- Language names that are not in the v1 allowlist (`zh`, `ja`, etc.).

### P.3 Lyrics cleanup

Common fixes before generation:

| Issue | Fix |
| --- | --- |
| Repeated `Section N` from Whisper segmentation | Collapse to canonical `[Verse]`, `[Chorus]`, etc. |
| Unwhitelisted bracket tags (`[Spoken Word]`, `[Ad-lib]`) | Either whitelist the tag or remove the bracket — non-whitelisted tags get sung |
| Lyrics too long (> 3,500 chars) | Trim to verse + pre-chorus + chorus + bridge + outro; remove double choruses |
| Lines too dense (> 12 syllables) | Split into two lines or drop words |
| Language detection surprise (Whisper hallucinates German for English singing) | Re-transcribe with `large-v2`; sanity-check language |

### P.4 Lyric density rule (intelligibility)

The S5/S6 finding from the youtube-studio web vocal research:

- **6-10 syllables per line.** Faster lines drop consonants; slower lines
  sound verbose.
- **25-40 words for a 30 s pilot.** Scale up proportionally for longer
  songs; do not change per-line density.
- **One singable phrase per line.** Avoid prose-like long lines; reduce
  syllables when notes must be held.
- Deliberate vowel elongation requests held notes but reduces
  literal-text fidelity — use sparingly and only for clear effect.

### P.5 Vocal mode tag

If the request includes "lead with choir" or "backing choir":

- Map to `--vocals "clear lead vocal with warm backing choir"` (caption
  cue).
- Do not promise discrete choir control — MiniMax treats mode as a
  caption suffix, not an API flag.
- Linter emits a soft warning on bare `lead-choir` token in the prompt.
- Acceptance is by ear; treat choir quality as best-effort until the
  Gate 5 pilot is human-auditioned.

---

## Post-processing techniques (deep-dive)

### P.6 Loudness target table

| Target | Use case | `loudnorm` values |
| --- | --- | --- |
| -16 LUFS / -1 dBTP / LRA 11 | Spotify, Apple Music, podcast | `I=-16:TP=-1:LRA=11` |
| -14 LUFS / -1 dBTP / LRA 11 | YouTube music | `I=-14:TP=-1:LRA=11` |
| -23 LUFS / -2 dBTP | EBU R128 broadcast | `I=-23:TP=-2:LRA=11` |
| -16 LUFS / -1.5 dBTP / LRA 11 | youtube-studio delivery (recommended for mixed bed) | `I=-16:TP=-1.5:LRA=11` |

The skill's `finalize_track.sh` is hard-coded to `-16 LUFS / -1 dBTP /
LRA 11` (the most common streaming target). If the user wants a
different target, run `ffmpeg loudnorm` directly with the values above.

### P.7 Format comparison

| Format | Lossless? | Best for |
| --- | --- | --- |
| mp3 192 kbps | ❌ | Streaming delivery, podcast hosting, music apps |
| mp3 256 kbps | ❌ | Higher-quality streaming; close to transparent at 256+ for most material |
| mp3 320 kbps | ❌ | "Transparent" mp3; very close to CD quality |
| wav 48 kHz 24-bit | ✅ | Mastering engineer, archive, downstream DSP |
| wav 44.1 kHz 16-bit | ✅ | CD master |
| flac 48 kHz | ✅ | Archive with smaller file size than wav |
| m4a / AAC 256 kbps | ❌ | Apple ecosystem delivery (lossy but better than mp3 at the same bitrate) |

The cloud default is **mp3 ~256 kbps stereo 44.1 kHz**. `finalize_track.sh`
bumps to 48 kHz. For lossless archive, transcode with `ffmpeg -i input.mp3 -codec:a pcm_s24le -ar 48000 archive.wav`
after the loudnorm pass.

### P.8 Metadata embedding recipes

Common tag fields by format:

| Field | mp3 (ID3v2.4) | flac (Vorbis) | m4a (iTunes) |
| --- | --- | --- | --- |
| Title | `TIT2` | `TITLE` | `©nam` |
| Artist | `TPE1` | `ARTIST` | `©ART` |
| Album | `TALB` | `ALBUM` | `©alb` |
| Year | `TDRC` | `DATE` | `©day` |
| Genre | `TCON` | `GENRE` | `©gen` |
| Track number | `TRCK` | `TRACKNUMBER` | `trkn` |
| Lyrics (unsynced) | `USLT` | `LYRICS` | `©lyr` |
| Lyrics (synced) | `SYLT` | (custom) | (custom) |
| Cover art | `APIC` | `METADATA_BLOCK_PICTURE` | `covr` |

`mutagen` abstracts the per-format differences; the snippet in
[§ 3.3 Metadata embedding](#33-metadata-embedding) is the canonical
mp3 starting point.

---

## Validation details

### V.1 What `audio_quality.py` actually measures

```
- duration_s: float (librosa.get_duration or sf.info)
- sample_rate_hz: int
- channels: int
- peak_dbfs: float (max |sample|)
- rms_dbfs: float (20*log10(sqrt(mean(x**2))))
- lufs: float | None (pyloudnorm.Meter; None if pyloudnorm missing)
- silence_ratio: float (fraction of samples below -50 dBFS)
- clipping_ratio: float (fraction of samples at 0 dBFS)
- snr_db: float (estimated; not a calibrated measurement)
```

`SNR` is **estimated** by comparing the signal RMS to the silent
windows; it is not a calibrated measurement and should not be cited as
proof of source quality.

### V.2 What `lrc_validator.py` actually checks

- Header lines `[key:value]` for `ar`, `ti`, `al`, `by`, `length`,
  `offset`.
- Timestamp format `[mm:ss.xx]` or `[mm:ss.xxx]`.
- Chronological ordering.
- Empty lyrics lines emit a warning.
- UTF-8 encoding.

It does **not** check whether the LRC matches the audio; that requires
either a synced re-transcription or a human listen.

### V.3 What `metadata_checker.py` actually checks

- File extension → expected format.
- Format-specific minimums:
  - mp3: 16-48 kHz sample rate, 64-320 kbps bitrate.
  - wav: 16-192 kHz sample rate, 16/24/32-bit depth, signed PCM or float.
  - flac: 16-192 kHz, 16/24-bit.
- Channels ≥ 1.
- Duration in plausible range.

### V.4 The Gate 5 acceptance gates

These come straight from the youtube-studio vocal plan and cannot be
fully automated:

| Gate | What it means | How to evaluate |
| --- | --- | --- |
| Intelligibility | Lyrics recognizable without subtitles | Listen at chorus |
| Vocal presence | Lead sits above the bed | Listen at verse; LUFS comparison |
| Choir cleanliness | Backing vocals do not clash | Listen with mode=choir flag |
| Truncation | No clipped final word | Listen to last 10 s; check `silence_ratio` |
| Artifacts | No clicks, pops, distortion | Listen first 10 s; check `clipping_ratio` |
| Loudness | Comfortable at 0.5-1.0 system gain | Listen at mix gain; check `lufs` |

If any gate fails, do not retry with the same seed and prompt — adjust
prompt or lyrics (see [Troubleshooting](#troubleshooting)).

---

## Integration with `mmx_recipe`

The `mmx_recipe` pattern lives at
[`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) (reference
implementation at `~/youtube-studio/tools/mmx_recipe.py`). For vocal
work, the pattern adds three things on top of the skill's existing
wrapper:

1. **Typed `MMXReceipt`.** Every call returns a frozen dataclass with
   `argv`, `output_path`, `returncode`, `elapsed_seconds`, `stdout`,
   `stderr`, `quota` (snapshot when `check_quota=True`), and `dry`. Use
   this in batch scripts to attach receipts to per-song sidecars.
2. **`dry=True`.** Builds the argv and returns a receipt **without**
   invoking `subprocess`. Use this for `--dry-run` preflights and CI.
3. **`check_quota=True`.** Calls `mmx quota show --output json` **before**
   the spend and attaches the snapshot to the receipt. Audit logs can
   then replay "what quota was on hand when this fired?".

The skill's `scripts/generate_with_retry.py` is the planned refactor
target ([roadmap v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md)) to
gain these without losing its existing operational guarantees (transient
retry, `--timeout 600`, signal recovery, file move). Until that
lands, write a small operator script that calls `mmx` directly with
`subprocess.run` and bakes in `MMXReceipt` + `check_quota=True`.

A minimal vocal-batch orchestrator (sketch):

```python
import json, subprocess, time
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(frozen=True)
class MMXReceipt:
    argv: tuple[str, ...]
    output_path: Path
    returncode: int
    elapsed_s: float
    stdout: str
    stderr: str
    quota: dict | None = None
    dry: bool = False

def mmx_music_generate_vocal(
    *, prompt, lyrics_file, vocals, language, out_path,
    model="music-2.6", bpm=96, key="G major",
    dry=False, check_quota=False,
):
    argv = ("mmx", "music", "generate",
            "--prompt", prompt,
            "--lyrics-file", lyrics_file,
            "--vocals", vocals,
            "--language", language,
            "--bpm", str(bpm),
            "--key", key,
            "--model", model,
            "--out", str(out_path))
    if dry:
        return MMXReceipt(argv=argv, output_path=out_path,
                           returncode=-1, elapsed_s=0.0,
                           stdout="", stderr="", dry=True)
    quota = None
    if check_quota:
        try:
            quota = json.loads(subprocess.check_output(
                ("mmx", "quota", "show", "--output", "json"), text=True))
        except Exception as e:
            quota = {"error": str(e)}
    t0 = time.monotonic()
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    return MMXReceipt(argv=argv, output_path=out_path,
                       returncode=proc.returncode,
                       elapsed_s=time.monotonic() - t0,
                       stdout=proc.stdout, stderr=proc.stderr,
                       quota=quota)


# In a batch loop
for song in songs:
    out = Path(f"~/Music mix/{song.project}/{song.slug}/M1_{song.slug}.mp3").expanduser()
    receipt = mmx_music_generate_vocal(
        prompt=song.prompt, lyrics_file=song.lyrics_file,
        vocals=song.vocals, language=song.language, out_path=out,
        check_quota=True,
    )
    sidecar = out.with_suffix(".receipt.json")
    sidecar.write_text(json.dumps(asdict(receipt), indent=2, default=str))
    if receipt.returncode != 0 or not out.exists():
        print(f"FAIL {song.slug}: rc={receipt.returncode}")
        print(receipt.stderr.strip()[:500])
        continue
    print(f"OK   {song.slug}: {receipt.elapsed_s:.1f}s")
```

Use the receipt to gate downstream steps: if `quota["remaining_5h_units"]`
drops below a threshold (e.g. 200), the orchestrator short-circuits the
rest of the batch and reports "quota low — pause until refill". This is
the quota-aware batch the youtube-studio engine uses as a first-class
gate.

---

## End-to-end example

A complete vocal workflow for "Vocal Pilot — Indie Pop":

```bash
#!/usr/bin/env bash
set -euo pipefail

# 0. Setup
PROJECT="demo-project"
SLUG="vocal-pilot"
SONG_DIR="$HOME/Music mix/$PROJECT/$SLUG"
mkdir -p "$SONG_DIR"

# 1. Pre-flight
python3 scripts/check_environment.py
mmx quota show --output json

# 2. Prepare lyrics (6-10 syllables/line, with structure tags)
cat > /tmp/vocal_pilot_lyrics.txt <<'EOF'
[Intro]

[Verse]
City lights are calling out my name tonight
Walking shadows under neon sign
Every street a memory of your face
Every corner hides a piece of you

[Pre Chorus]
And I don't know why I keep returning
To the place where we first met

[Chorus]
We were golden in the morning light
We were burning through the summer night
We were something that I'll never find
We were golden, you and I

[Verse]
Empty coffee cups and laughter in the rain
Photographs that time can never take away

[Pre Chorus]
And I don't know why I keep returning
To the place where we first met

[Chorus]
We were golden in the morning light
We were burning through the summer night
We were something that I'll never find
We were golden, you and I

[Bridge]
Time keeps moving but the feeling stays
Like a song that's stuck inside my head

[Outro]
We were golden...
EOF

# 3. Lint prompt + lyrics together
PROMPT='Indie pop, 96 BPM, warm electric guitar, fingerpicked acoustic,
melodic bass, steady brushed drums, intimate female lead vocal in English,
vocal-forward mix, restrained reverb, wide chorus.
ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent,
no sparse arrangements.'
python3 scripts/lint_music_request.py \
    --prompt "$PROMPT" \
    --lyrics-file /tmp/vocal_pilot_lyrics.txt \
    --flags-json '{"bpm":96,"key":"G major","structure":"intro-verse-pre_chorus-chorus-verse-pre_chorus-chorus-bridge-chorus-outro","vocals":"clear lead vocal, breathy verses, brighter choruses","language":"en","avoid":"a cappella, sparse, minimal, electronic sounds, clipping"}' \
    --output /tmp/lint_report.json

# Inspect the lint report — proceed only if no blockers
cat /tmp/lint_report.json

# 4. Generation (sequential; verify file after)
python3 scripts/generate_with_retry.py \
    --output-path "$SONG_DIR/M1_${SLUG}.mp3" \
    -- music generate \
      --prompt "$PROMPT" \
      --lyrics-file /tmp/vocal_pilot_lyrics.txt \
      --vocals "clear lead vocal, breathy verses, brighter choruses" \
      --language en \
      --genre "indie pop" \
      --mood "warm nostalgic" \
      --instruments "electric guitar, acoustic guitar, bass, brushed drums, piano" \
      --bpm 96 \
      --key "G major" \
      --structure "intro-verse-pre_chorus-chorus-verse-pre_chorus-chorus-bridge-chorus-outro" \
      --avoid "a cappella, sparse, minimal, electronic sounds, clipping" \
      --model music-2.6 \
      --out "$SONG_DIR/M1_${SLUG}.mp3"

# 5. Post-processing — finalize for delivery, archive lossless
python3 scripts/finalize_track.sh "$SONG_DIR/M1_${SLUG}.mp3" "$SONG_DIR/M1_${SLUG}_finalized.mp3"
ffmpeg -y -i "$SONG_DIR/M1_${SLUG}.mp3" \
       -codec:a pcm_s24le -ar 48000 -ac 2 \
       "$SONG_DIR/M1_${SLUG}_archive.wav"

# 6. Validation
python3 ../../tests/analyzers/audio_quality.py "$SONG_DIR/M1_${SLUG}_finalized.mp3" --json > "$SONG_DIR/M1_${SLUG}_validation.json"
python3 ../../tests/analyzers/metadata_checker.py "$SONG_DIR/M1_${SLUG}_finalized.mp3" --json >> "$SONG_DIR/M1_${SLUG}_validation.json"

# 7. LRC sidecar (manual — Whisper sync)
cat > "$SONG_DIR/M1_${SLUG}.lrc" <<'EOF'
[ar:Vocal Pilot Artist]
[ti:Vocal Pilot — Indie Pop]
[al:Vocal Pilot EP]
[length:03:24.50]
[offset:0]

[00:08.12]City lights are calling out my name tonight
[00:13.40]Walking shadows under neon sign
...
EOF
python3 ../../tests/analyzers/lrc_validator.py "$SONG_DIR/M1_${SLUG}.lrc" --json >> "$SONG_DIR/M1_${SLUG}_validation.json"

# 8. Lyrics alignment (Whisper re-transcription)
python3 scripts/verify_lyrics_alignment.py \
    --expected /tmp/vocal_pilot_lyrics.txt \
    --transcript "$SONG_DIR/M1_${SLUG}_whisper.txt" \
    --output "$SONG_DIR/M1_${SLUG}_alignment.json"

# 9. Human listen gate (intelligibility, vocal presence, choir, loudness, artifacts, truncation)
echo "MANUAL: listen at $SONG_DIR/M1_${SLUG}_finalized.mp3 — pass all Gate 5 gates?"

# 10. Delivery
echo "Deliver: $SONG_DIR/M1_${SLUG}_finalized.mp3 + $SONG_DIR/M1_${SLUG}.lrc"
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| **Vocal is unintelligible** | Lyrics too dense (> 12 syllables/line) or too fast (> 40 words for 30 s) | Trim lyrics to 6-10 syllables/line; reduce word count; drop a section |
| **Vocal buried under bed** | Prompt missing "vocal-forward mix direction" or "lead vocal timbre" descriptor | Add `intimate vocal-forward studio mix` and a specific vocal descriptor; reduce bed instruments in `--avoid` |
| **Sparse / a cappella sections** | Anti-sparse guard not applied | Add `ALL instruments ALWAYS playing throughout, NEVER go a cappella or silent`; add explicit instruments in `--instruments` |
| **Output duration is wrong** | `--length` is a hint; lyrics length + structure drive duration more | Trim lyrics to ~120 words for ~3 min; add `[Break]` tags; or switch to ACE-Step for exact duration |
| **Output peaks clip / harsh** | Cloud output is high crest; pushing gain makes it worse | Match loudness via `finalize_track.sh`; do not chase peaks at diffusion time |
| **Wrong language vocal** | `--language` not set or set to a non-allowlist code | Set `--language en\|es\|fr\|it\|pt`; check `LANGUAGE_PATTERNS` table in `lint_music_request.py:28-34` |
| **No choir audible** | `mode=choir` is caption-only, not a discrete API control | Verify prompt includes the choir descriptor; treat as best-effort |
| **Truncation mid-syllable** | Output ends abruptly on a held note | Add `[Outro]` + `[Break]` tags near the end; trim lyrics to fit |
| **`requested_lyrics_sha256` mismatch** | Receipt hash refers to a different lyrics file | Pass `--lyrics-file` with the exact same path used for the lint; do not edit between lint and generate |
| **HTTP 400 / 2079-byte prompt rejection** | Prompt over the 2,000-byte limit | Linter warns at 1,800; errors at 2,000; observed API rejection at 2,079 — trim to under 2,000 |
| **HTTP 429 / quota exhaustion** | 5h session exhausted | Wait for the rolling window to refill; check `mmx quota show`; reduce concurrency |
| **`SIGTERM`/`SIGKILL` after file save** | mmx exit signal post-save (known operational quirk) | Verify file exists + size > 100 KB + `ffprobe` positive duration before retrying — file existence is the source of truth |
| **Vocal artifacts in first 10 s** | Cold-start silence or clicky attack | Add `soft intro, fade-in arrangement, no clicks` to prompt; or generate M2 contrast variant |
| **Chorus quieter than verse** | No energy/dynamic contrast in prompt | Add `intimate restrained verse, progressively building, wide dynamic contrast, full hook-forward chorus; clean vocal-forward mix, restrained reverb, no clipping` |

### Iteration loop

If a Gate 5 gate fails:

1. **Do not retry the same seed and prompt.** That wastes quota and
   produces the same result.
2. **Pick one adjustment** at a time so you know what worked:
   - Adjust the prompt (vocal-forward mix, energy contrast, diction).
   - Adjust the lyrics (density, structure, syllable count).
   - Adjust the flags (BPM, key, structure, instruments).
3. **Re-lint** prompt and lyrics with `lint_music_request.py`.
4. **Regenerate** with a new attempt id (sequential, not parallel).
5. **Re-validate** with the analyzer pipeline.
6. **Re-listen** — confirm the new variant passes the failed gate.
7. If **two** consecutive attempts fail the same gate, escalate to
   the user with the symptom + diagnostics. Do not burn quota on a
   third blind retry.

### When to give up and switch backends

- **Vocal quality does not improve after 3 attempts.** Switch to a
  local ACE-Step vocal route if the user wants the exact-duration,
  free path; cloud is the right tool when iteration speed and cover
  workflows matter more.
- **Quota is exhausted and the user needs the song today.** Switch to
  ACE-Step (local) — exact duration, free, no quota cost.
- **The user needs a guaranteed full-length 3:00+ song.** Switch to
  ACE-Step — MiniMax vocal cloud produces 60-180 s reliably; longer is
  not guaranteed.

---

## Cross-references

- [`references/mmx-flags-reference.md`](mmx-flags-reference.md) — full
  flag table including `--lyrics`, `--vocals`, `--language`, `--avoid`,
  `--structure`, `--bpm`, `--key`.
- [`references/lyrics-generation.md`](lyrics-generation.md) — the
  `lyrics_generation` API (`write_full_song` + `edit` modes).
- [`references/cover-workflow.md`](cover-workflow.md) — one-step and
  two-step cover workflow with vocal flag set.
- [`references/mashup-workflow.md`](mashup-workflow.md) — two-song
  mashup, which uses the vocal command shape when the user wants
  sung content for Song A.
- [`references/emotion-analysis.md`](emotion-analysis.md) — emotion
  analysis on input audio (timbre, intensity, vocal effort) to drive
  vocal-forward prompt composition.
- [`references/emotion-delivery.md`](emotion-delivery.md) — 21 emotion
  recipes for the OUTPUT.
- [`references/error-handling.md`](error-handling.md) — MiniMax-specific
  error table (lyrics too long, prompt too long, cover errors,
  anti-sparse failures).
- [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
  — sequential runs, output-file handling, duration is a target.
- [`references/setup-and-preflight.md`](setup-and-preflight.md) —
  extended pre-flight for the vocal workflow.
- [`references/quota-checking.md`](quota-checking.md) — Token Plan Plus
  quota mechanics and `mmx quota show` integration.
- [`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) — the
  `mmx_recipe` wrapper pattern (`MMXReceipt`, `dry`, `check_quota`).
- [`references/short-prompt-recipes.md`](short-prompt-recipes.md) —
  compact prompt recipes (under 500 chars) for fast cloud iteration.
- [`references/orchestrator-quickstart.md`](orchestrator-quickstart.md)
  — per-input orchestrator commands, Demucs-on-full-mix-not-vocals
  rule, Whisper `large-v2` for sung audio.
- [`references/free-tool-inputs.md`](free-tool-inputs.md) — MiniMax
  layer: free-tool routing, blocker checks, prompt/flag conflict lint
  before analysis.
- [`../../music-craft/SKILL.md`](../../music-craft/SKILL.md) — base skill
  with the anti-sparse guard and the prompt formula this vocal
  workflow extends.
- [`scripts/check_environment.py`](../scripts/check_environment.py) —
  preflight diagnostic (planned v1.1.5 item 18: extend with
  `mmx quota show --output json`).
- [`scripts/lint_music_request.py`](../scripts/lint_music_request.py) —
  prompt + flag conflict linter; enforces `LANGUAGE_PATTERNS` allowlist
  and prompt-byte limit.
- [`scripts/lint_lyrics.py`](../scripts/lint_lyrics.py) — lyrics tag
  whitelist + syllable/BPM density check.
- [`scripts/generate_with_retry.py`](../scripts/generate_with_retry.py)
  — transient retry wrapper; planned v1.1.5 item 17: refactor to add
  `MMXReceipt`-shaped return and `--dry` flag.
- [`scripts/verify_lyrics_alignment.py`](../scripts/verify_lyrics_alignment.py)
  — semantic overlap between expected lyrics and post-gen transcript.
- [`scripts/finalize_track.sh`](../scripts/finalize_track.sh) —
  loudnorm to `-16 LUFS / -1 dBTP / LRA 11` + 48 kHz resample.
- [`scripts/extract_stems.py`](../scripts/extract_stems.py) — Demucs
  source separation (for timbre / pitch analysis of an isolated vocal).
- [`../../tests/analyzers/audio_quality.py`](../../tests/analyzers/audio_quality.py)
  — duration / LUFS / peak / RMS / silence / clipping / SNR analyzer.
- [`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py)
  — LRC header + timestamp + ordering + UTF-8 validator.
- [`../../tests/analyzers/metadata_checker.py`](../../tests/analyzers/metadata_checker.py)
  — format-specific metadata validator.
- [`../../music-craft-minimax_ROADMAP.md`](../../music-craft-minimax_ROADMAP.md)
  — v1.1.5 items 17-22 (refactor `generate_with_retry.py` to typed
  receipt, surface `mmx quota show` via `check_environment.py`,
  document vocal flag set, language allowlist, mode allowlist, lyrics
  provenance vs audit). v1.1.6 item 23 (Music 3.0 migration when mmx
  supports it; **out of scope for this vocal workflow today**).
- [`~/youtube-studio/docs/capabilities/MUSIC-CAPABILITIES.md`][music-cap]
  § 12 Vocal capabilities — engine single source of truth for vocal
  generation contract (Gate 2 wired).
- [`~/youtube-studio/docs/superpowers/plans/deprecated/2026-07-29-vocal-music-foundation-plan.md`][vocal-plan]
  — Gates 0-4 contract decisions; Gate 5 human-gated pilots; cost-model
  clarification (Token Plan Plus, no per-attempt vocal billing).
- [`~/youtube-studio/docs/research/ace-step-vocal-research-local-2026-07-30.md`][local-research]
  — local-evidence report on vocal generation parameters (lyric density
  rule, runner pass-through, loudness/peak dynamics).
- [`~/youtube-studio/docs/research/ace-step-vocal-research-web-2026-07-30.md`][web-research]
  — web-research synthesis (CFG/shift/APG artifact levers, expectation
  setting on XL base).
- [`~/youtube-studio/tools/mmx_recipe.py`](https://github.com/LuisCharro/youtube-studio/blob/main/tools/mmx_recipe.py)
  — canonical `MMXReceipt` + `dry` + `check_quota` reference
  implementation.
