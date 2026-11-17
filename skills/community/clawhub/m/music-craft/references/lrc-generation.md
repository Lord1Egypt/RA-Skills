# LRC Generation

Recipe for producing synced-lyrics (`.lrc`) files for any vocal track the
skill generates, whether the source was ACE-Step local, a cloud
path, or any other vocal-capable backend. Load this when the user asks for
karaoke output, music-video subtitles, or any karaoke / subtitle / accessibility
captioning use case for a generated track.

## When To Load

Load this reference when the request includes any of:

- "karaoke", "synced lyrics", "LRC", "subtitle file", "subtitles for the
  music video"
- a vocal track already generated (or about to be generated) and the user
  wants a separate `.lrc` companion file
- structured lyrics (`[Verse]`, `[Chorus]`, …) that need to be mapped onto
  actual vocal onset times

Do **not** load this for:

- plain lyrics output with no timing (use a writing skill or the lyrics
  workflow in `references/structure-tags.md`)
- subtitle files for narration / TTS (those use `mmx speech synthesize
  --subtitles` and a different timing contract — out of scope for music)
- instrumental tracks (no lyrics to align; skip the workflow)

## Cross-References

- **Lyrics section tags and ASR cleanup:** [`references/structure-tags.md`](structure-tags.md), [`references/lyrics-cleanup.md`](lyrics-cleanup.md)
- **Backend selection (vocal vs. instrumental):** [`references/other-backends.md`](other-backends.md), [`references/acestep-generation.md`](acestep-generation.md)
- **Verification scripts already in the skill:** [`scripts/verify_lyrics_alignment.py`](../scripts/verify_lyrics_alignment.py) (semantic delivery check), [`scripts/lint_lyrics.py`](../scripts/lint_lyrics.py) (preflight)
- **Validator (canonical):** [`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py)
- **Unit tests for the validator:** [`../../tests/unit/test_lrc_format.py`](../../tests/unit/test_lrc_format.py)
- **Roadmap item:** `music-craft_ROADMAP.md` § v1.2.0 item 18 (LRC generation for karaoke/subtitle support)

## 1. What is LRC

LRC is a plain-text, line-oriented lyrics format that pairs each lyric line
with a `mm:ss.xx` timestamp. Files use the `.lrc` extension, are encoded as
UTF-8, and are read by every mainstream karaoke player (MiniLyrics, Kanto,
Vanilla Lyrics, AIMP, foobar2000) plus most music players' lyrics pane
(Spotify-style display, Apple Music lyrics, etc.).

### History

The format was created by **Kuo-Chang Chao** ("Creator") in the late 1990s
as a companion file for a Winamp karaoke plugin. It was never standardized
through a formal body, but a de-facto convention emerged in the early 2000s
and is what every modern LRC player expects today. The format is sometimes
called **LRC lyrics**, **LRC file**, or just **"lyrics file"** in casual
usage.

### Use cases

| Use case | Why LRC works |
| --- | --- |
| **Karaoke display** | Each timestamp drives the next-line highlight; the player scrolls and highlights synchronously. |
| **Music video subtitles** | Hard-burn or soft-sub subtitle rendering for YouTube, TikTok, IG Reels, Shorts. |
| **Accessibility captions** | Same format as karaoke; readable by screen-reader software that supports timed lyrics. |
| **Music player lyrics pane** | Spotify / Apple Music / web players that import `.lrc` files alongside the audio. |
| **Sync debugging** | Diff the LRC timeline against a known-good track to find alignment drift after a generation tweak. |

### What LRC is **not**

- Not a video subtitle format. LRC cannot carry position or styling; for
  styled video subtitles use SRT, VTT, or ASS.
- Not a karaoke **score** format. LRC carries timing, not MIDI/notes.
- Not a closed-format. The spec is informal; players are lenient about
  ordering and metadata, strict about timestamps and UTF-8.

## 2. LRC Format Spec

### Metadata header

Metadata lines sit at the top of the file, each on its own line, in the form
`[key:value]`:

| Key | Meaning | Required? | Example |
| --- | --- | --- | --- |
| `ar` | Artist | Recommended | `[ar:Cold Mountain]` |
| `ti` | Title | Recommended (warn if missing) | `[ti:Ride On]` |
| `al` | Album | Optional | `[al:Jengi Sessions]` |
| `by` | LRC creator (who made the file) | Optional | `[by:music-craft]` |
| `length` | Total audio length in `mm:ss.xx` | Optional | `[length:03:12.50]` |
| `offset` | Global timestamp offset in ms (+/-) | Optional | `[offset:200]` |

Rules:

- Header lines must come **before** any timestamped lyric line.
- The validator ([`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py))
  recognizes the six keys above and emits a **warning** for missing `ti`
  and `ar`. Other keys are silently ignored.
- The `length` value is informational; players do not use it for sync.
- `offset` is applied by some players as a global shift: positive values
  push every timestamp later, negative values pull them earlier. Use it
  to correct whole-file alignment without rewriting every line.

### Timestamps

Two timestamp formats are valid:

```text
[mm:ss.xx]      # centiseconds (2-digit fraction, 10 ms precision)
[mm:ss.xxx]     # milliseconds (3-digit fraction, 1 ms precision)
```

- `mm` is minutes (two or more digits; `mm` ≥ 2).
- `ss` is seconds (always two digits).
- `.xx` or `.xxx` is the fractional part — either 2 or 3 digits.
- Multiple timestamps per line are allowed: each one creates a separate
  lyric entry that shares the same text.

Examples:

```text
[00:12.50]First line of the verse
[00:20.10][00:25.40][00:31.80]Same chorus repeated
[01:30.250]Millisecond precision (WhisperX output)
```

### Section tags

Section tags (`[Verse]`, `[Chorus]`, `[Bridge]`, …) become **timestamped
lines with the tag as text**:

```text
[00:00.00][Intro]
[00:08.50][Verse]
[00:08.50]I walked alone beneath the rain
[00:14.20]Every window knew my pain
[00:20.10][Chorus]
[00:20.10]We ride on through the night
```

This is what karaoke players expect: the section tag appears as a
"meta-line" with its own timestamp and no lyric text. The first lyric
under the tag shares that same timestamp, which gives the player a
synchronization anchor for the section break.

For the full section-tag catalog and the canonical 8-section default, see
[`references/structure-tags.md`](structure-tags.md).

### Encoding

**UTF-8 only.** Latin-1 or any other encoding is rejected by the validator
(`File is not valid UTF-8`). Non-English lyrics (Spanish, French, Japanese,
Chinese, Korean, etc.) require UTF-8; do not use cp1252 or cp1256 even for
European accented characters.

### Format reference table

| Element | Pattern | Example | Notes |
| --- | --- | --- | --- |
| Metadata | `[key:value]` | `[ar:Cold Mountain]` | Header only, no timestamps |
| Timestamp (centisecond) | `[mm:ss.xx]` | `[00:12.50]` | 10 ms precision |
| Timestamp (millisecond) | `[mm:ss.xxx]` | `[01:30.250]` | 1 ms precision (WhisperX default) |
| Multi-timestamp line | `[ts1][ts2]text` | `[00:20.10][00:25.40]Chorus` | Same text, two lyric entries |
| Section tag | `[mm:ss.xx][Section]` | `[00:20.10][Chorus]` | First lyric under it shares the timestamp |
| Lyric line | `[mm:ss.xx]text` | `[00:08.50]I walked alone` | One lyric entry |
| Encoding | UTF-8 | — | Required; non-UTF-8 fails validation |

## 3. Generation Workflow

The path is **backend-neutral**: LRC can be generated for any vocal track,
regardless of whether the audio came from ACE-Step or another
vocal-capable backend. The only requirement is that you have
both the audio file and the lyrics that were sung (either user-provided
or ASR-extracted).

### Workflow

1. **Generate audio and keep the lyrics text** — any vocal backend (ACE-Step or another).
2. **Align lyrics to audio** — WhisperX (word-level) or Whisper (segment-level).
3. **Build LRC lines** — one timestamp per lyric line; section tags on their own timestamped lines.
4. **Validate** — `lrc_validator.py --json`.
5. **Deliver the `.lrc` file** — in the same folder as the audio.

### Step 1 — Generate audio and retain lyrics

Run the normal generation loop from `SKILL.md`. Save the lyrics that
were actually fed to the generator as `<slug>_lyrics.txt` (the skill's
default lyrics file naming) **alongside** the generated audio. The
LRC generator needs both inputs to align.

If the track was generated without lyrics (instrumental, or the user
didn't provide any), skip the rest of this reference — there is nothing
to align.

### Step 2 — Align lyrics to audio

Pick one of two alignment strategies:

| Strategy | Tool | Precision | When to use |
| --- | --- | --- | --- |
| **Word-level** (recommended) | [WhisperX](https://github.com/m-bain/whisperX) | ~20 ms | Default; supports forced alignment via wav2vec2 |
| **Segment-level** | Whisper `medium` or larger | ~200–500 ms | When WhisperX is unavailable or model size is a concern |

WhisperX is the recommended path because it pairs Whisper transcription
with **forced alignment** through a separate acoustic model (typically
`wav2vec2-base-960h` for English). That gives per-word timestamps tight
enough for karaoke display; vanilla Whisper only emits segment-level
timestamps and karaoke highlight drift becomes visible above ~300 ms.

For non-English audio, swap in a WhisperX-compatible alignment model
for that language. WhisperX supports multilingual alignment via
`torchaudio` and the `nlp/transformers`-hosted alignment models.

Example (WhisperX, Python):

```python
import whisperx

device = "cuda"        # "cpu" works but is ~10× slower; "mps" on Apple Silicon
audio_file = "out/Ride_On_M1_v1.mp3"

# 1. Transcribe
model = whisperx.load_model("medium", device)
audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=8)

# 2. Align (forced alignment per word)
align_model, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], align_model, metadata, audio, device
)

# 3. Emit word-level timestamps
for seg in result["segments"]:
    for word in seg["words"]:
        # word["start"], word["end"], word["word"], word["score"]
        ...
```

Example (faster-whisper, when GPU/CUDA is unavailable):

```python
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "out/Ride_On_M1_v1.mp3",
    word_timestamps=True,        # word-level via wav2vec2 alignment
    vad_filter=True,             # skip silent regions
)

for seg in segments:
    for w in seg.words:
        # w.start, w.end, w.word, w.probability
        ...
```

### Step 3 — Build LRC lines

Take the word-level timestamps and project them onto the original lyrics
structure. Two practical approaches:

**Approach A — one LRC line per lyrics line** (simpler, lower precision):

1. Distribute the total word duration for a lyric line evenly across its
   words.
2. Place each lyric line's timestamp at the **first word** of the line.
3. Section tags (`[Verse]`, `[Chorus]`, …) become their own lines
   timestamped to the same point as the first lyric that follows.

**Approach B — one LRC line per lyric line, anchored to first word start**
(recommended; matches karaoke players):

1. For each lyric line, find the word-level timestamp of the **first
   word**.
2. Use that timestamp as the lyric line's `[mm:ss.xx]` value.
3. For chorus repeats, look up the matching line in the next chorus
   segment and emit a second `[mm:ss.xx]` for the same text:
   `[00:20.10][01:08.50]We ride on through the night`.

Both approaches give ~50–100 ms alignment, which is the practical
ceiling for hand-distributed word timestamps. WhisperX itself is
~20 ms; the gap comes from mapping word-level data back to lyric lines.

### Step 4 — Validate

Run the validator on the produced `.lrc`:

```bash
python3 ../../tests/analyzers/lrc_validator.py out/Ride_On_M1_v1.lrc --json
```

Exit code `0` = valid; `1` = invalid; `2` = error. Use `--json` to
machine-parse the report and check `report["valid"]` in CI. See
[§ 6 Validation](#6-validation) for the full report shape.

### Step 5 — Deliver

Place the `.lrc` file alongside the audio with a matching stem:

```text
out/Ride_On_M1_v1.mp3
out/Ride_On_M1_v1.lrc
```

The matching stem is what most karaoke players look for by default.

## 4. Tools

### Comparison table

| Tool | Speed | Precision | Local? | Language coverage | Notes |
| --- | --- | --- | --- | --- | --- |
| **WhisperX** | Medium (GPU-accelerated) | ~20 ms word-level | Yes (Python) | 100+ via Whisper + wav2vec2 alignment | **Recommended.** Pairs Whisper with forced alignment. |
| **Whisper** (openai-whisper) | Slow on CPU | ~200–500 ms segment-level | Yes (Python) | 99 | Segment-only timestamps; karaoke drift visible above 300 ms. |
| **faster-whisper** | Fast (CTranslate2) | ~20 ms word-level | Yes (Python) | Same as Whisper | CTranslate2 backend; ~4× faster than vanilla Whisper on CPU. Good WhisperX substitute. |
| **whisper.cpp** | Fastest on CPU/Apple Silicon | ~50–100 ms segment-level | Yes (C++) | 99 | Best for CPU-only / Apple Silicon / edge. Word-level timestamps via `-ml` models. |

### WhisperX — recommended

- Repo: <https://github.com/m-bain/whisperX>
- Install: `pip install whisperx` (Python ≥ 3.9, PyTorch, `torchaudio`)
- Hardware: CUDA GPU strongly preferred; MPS and CPU work but are slower.
- Output: word-level JSON with `start`, `end`, `word`, `score` per token.

### Whisper (openai-whisper)

- Repo: <https://github.com/openai/whisper>
- Install: `pip install -U openai-whisper`
- Hardware: any (CPU works; CUDA ~10× faster).
- Output: segment-level JSON with `start`, `end`, `text` per segment.
- Model recommendation: **`medium`** for lyrics (default for this skill).
  Use `large-v2` for complex singing, noisy audio, or multilingual songs.
  Treat `small` as a fast draft only — see
  [`references/structure-tags.md`](structure-tags.md) § "Lyrics from ASR".

### faster-whisper

- Repo: <https://github.com/SYSTRAN/faster-whisper>
- Install: `pip install faster-whisper`
- Hardware: CPU-friendly (CTranslate2 quantized inference); CUDA also
  supported.
- Output: same shape as Whisper, with optional `word_timestamps=True`
  for word-level data via wav2vec2 alignment.

### whisper.cpp

- Repo: <https://github.com/ggerganov/whisper.cpp>
- Build: `git clone https://github.com/ggerganov/whisper.cpp && make`
- Hardware: best CPU/Apple Silicon option; Vulkan, OpenCL, CUDA backends
  available; Core ML support for Apple Neural Engine.
- Output: SRT, VTT, or plain segment text. Use `-ml 1` for the medium
  model and `--output-json` to get word-level timestamps.
- **Best fit** when you do not want to install PyTorch.

### Model size guidance

| Model | VRAM | Speed (3-min audio) | Lyrics quality |
| --- | --- | --- | --- |
| `tiny` | ~1 GB | ~10 s | poor — hallucination-prone |
| `base` | ~1 GB | ~20 s | weak |
| `small` | ~2 GB | ~40 s | draft-quality only |
| `medium` | ~5 GB | ~2 min | **recommended** for lyrics |
| `large-v2` / `large-v3` | ~10 GB | ~4 min | best for noisy / multilingual |

CPU-only users should default to **`medium` with `int8` quantization**
(via faster-whisper). Going larger than `medium` on CPU is rarely worth
the wall-time cost.

## 5. Backend-Specific Notes

### ACE-Step (local)

**Lyrics are input to the generator.** The user (or this skill) supplies
the lyrics text in the `lyrics` parameter of `/release_task`. The audio
that comes back is supposed to sing those lyrics. This means:

- You have the exact lyrics the model was given.
- You can run WhisperX on the output audio to get word-level timestamps.
- The forced alignment step is forgiving because the model is supposed
  to sing the same words — small ASR mismatches are easy to spot and
  correct manually.

Practical tip: if ACE-Step returns audio where the lyrics don't match
the input (model sang different words or skipped a line), the LRC will
also be wrong. Fix the prompt first, regenerate, then run the LRC
pipeline. Do not try to "fix" the LRC to match wrong audio.

### Stable Audio Open / Stable Audio 3

**Instrumental only.** No lyrics, no LRC. Skip this entire workflow.

If the user asks for "LRC for a Stable Audio track", the answer is:
"this track has no vocals, so no LRC file is generated." Do not produce
an LRC with empty timestamps.

### MusicGen

**Instrumental only** (CC-BY-NC 4.0 weights, no vocal training). Same as
Stable Audio — skip the workflow.

### Other vocal backends

Any future vocal-capable backend that accepts lyrics as input follows the
same pattern as ACE-Step: you know the lyrics, you run forced
alignment on the audio, you emit the LRC.

## 6. Validation

The canonical validator lives at
[`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py).
It is also exercised by the unit tests at
[`../../tests/unit/test_lrc_format.py`](../../tests/unit/test_lrc_format.py)
(8 test cases covering valid files, invalid timestamps, ordering,
multi-timestamp lines, missing files, encoding, missing metadata, and
millisecond precision).

### CLI usage

```bash
python3 ../../tests/analyzers/lrc_validator.py out/Ride_On_M1_v1.lrc
```

Human-readable report:

```text
=== LRC Validation Report ===
Path:       out/Ride_On_M1_v1.lrc
Valid:      True
Lines:      24
Metadata:
  [ar: Cold Mountain]
  [ti: Ride On]
  [al: Jengi Sessions]
  [length: 03:12.50]
```

JSON report (for CI / scripting):

```bash
python3 ../../tests/analyzers/lrc_validator.py out/Ride_On_M1_v1.lrc --json
```

```json
{
  "path": "out/Ride_On_M1_v1.lrc",
  "valid": true,
  "metadata": {
    "ar": "Cold Mountain",
    "ti": "Ride On",
    "al": "Jengi Sessions",
    "length": "03:12.50"
  },
  "lines": [
    {"timestamp_ms": 0, "text": "[Intro]"},
    {"timestamp_ms": 8500, "text": "[Verse]"},
    {"timestamp_ms": 8500, "text": "I walked alone beneath the rain"}
  ],
  "line_count": 24,
  "errors": [],
  "warnings": []
}
```

### Exit codes

| Code | Meaning |
| ---: | --- |
| `0` | Valid (or valid with warnings — only `errors` block success) |
| `1` | Invalid (errors present) |
| `2` | Error (file not found, encoding error, etc.) |

### Python usage

```python
from lrc_validator import parse_lrc
from pathlib import Path

report = parse_lrc(Path("out/Ride_On_M1_v1.lrc"))
if not report["valid"]:
    for err in report["errors"]:
        print(f"ERROR: {err}")
    raise SystemExit(1)
for warn in report["warnings"]:
    print(f"warn: {warn}")
print(f"OK — {report['line_count']} lines")
```

## 7. Common Issues

### Alignment drift

**Symptom:** The LRC timestamps look correct on paper but the highlighted
line in the karaoke player runs ahead of (or behind) the audio.

**Cause:** WhisperX segment-level timestamps accumulate error across a
long track. Even at ~20 ms word-level precision, a 3-minute song can
drift 200–500 ms by the end if the alignment model misses a phrase.

**Fixes:**

1. **Use word-level alignment, not segment-level.** WhisperX with
   `align_model` gives the tightest fit.
2. **VAD filter.** Enable `vad_filter=True` (faster-whisper) or
   WhisperX's built-in VAD so silent regions don't add spurious
   timestamps.
3. **Manual anchor.** For the most important chorus, hand-set its
   timestamp to the precise downbeat. Use a DAW or `ffprobe` waveform
   inspection to find the downbeat to ~10 ms.
4. **`offset` metadata.** If the whole file is uniformly off, set
   `[offset:+200]` (push later) or `[offset:-200]` (pull earlier)
   rather than rewriting every line.

### Missing words

**Symptom:** A lyric line is in the LRC but the actual sung audio says
something different (or nothing).

**Cause:** Forced alignment only matches words it can hear. If the
singer swallows a syllable, elongates a vowel, or skips a word, the
alignment model returns no timestamp for that word.

**Fixes:**

1. **Use a larger model** (`large-v2` instead of `medium`) for noisy
   or quiet vocals.
2. **Drop the lyric from the LRC.** If the singer genuinely skips a
   line, the LRC should not pretend they sang it. Mark the gap with
   `[mm:ss.xx][Inst]` instead of forcing a timestamp.
3. **Manual timestamp.** Use a DAW to find the actual onset and hand-
   write the line. This is the right answer for the chorus hook.

### Timing precision

**Symptom:** Player shows the highlight jumping rather than scrolling.

**Cause:** LRC `mm:ss.xx` only has 10 ms precision; the file uses
centisecond timestamps but the alignment data is millisecond-precise.

**Fix:** Use `mm:ss.xxx` (3-digit fraction) for tightest timing.
WhisperX output should be rounded to the nearest millisecond before
formatting:

```python
def to_lrc_ts(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = seconds - minutes * 60
    return f"[{minutes:02d}:{secs:06.3f}]"   # → [00:08.500]
```

The validator accepts both formats; players vary in which they prefer.

### Empty lyric text

**Symptom:** Validator emits a warning like `Line has no lyrics text:
[00:20.10]`.

**Cause:** A timestamped line with no lyrics text. Usually a section
tag that was emitted without the leading lyric line sharing its
timestamp.

**Fix:** Section tags **must** have a timestamp and may be followed by a
lyric line with the same timestamp:

```text
[00:20.10][Chorus]
[00:20.10]We ride on through the night
```

If the section is purely instrumental, the tag line alone is fine —
the warning is informational, not a blocker.

### Out-of-order timestamps

**Symptom:** Validator reports `Timestamp out of order at line N`.

**Cause:** Two adjacent lyric lines have timestamps that don't increase
chronologically. The validator sorts lines, so this only surfaces when
the **same** timestamp is reused on multiple non-multi-timestamp lines.

**Fix:** Use multi-timestamp syntax for repeated lines:

```text
[00:20.10][00:45.50]We ride on through the night
```

Not:

```text
[00:20.10]We ride on through the night
[00:45.50]We ride on through the night
```

(That is technically allowed by some players, but the validator will
flag it as ambiguous.)

### Non-UTF-8 file

**Symptom:** Validator reports `File is not valid UTF-8`.

**Cause:** File was saved as Latin-1, cp1252, cp1256, etc.

**Fix:** Re-save as UTF-8:

```bash
iconv -f latin1 -t utf-8 out/Ride_On_M1_v1.lrc > out/Ride_On_M1_v1.utf8.lrc
mv out/Ride_On_M1_v1.utf8.lrc out/Ride_On_M1_v1.lrc
```

## 8. End-to-End Example

Generate an ACE-Step vocal track, then produce and validate its LRC
companion file.

### Step 1 — Generate the audio

Run the normal generation loop. Save the lyrics next to the audio:

```text
out/Ride_On_M1_v1/
- Ride_On_M1_v1.mp3
- Ride_On_M1_v1_lyrics.txt
- Ride_On_M1_v1_prompt.txt
```

Where `_lyrics.txt` is:

```text
[Intro]

[Verse]
I walked alone beneath the rain
Every window knew my pain

[Chorus]
We ride on through the night

[Verse]
The streetlights bend and break
For every choice we make

[Chorus]
We ride on through the night

[Outro]
```

### Step 2 — Transcribe with WhisperX

```python
import whisperx
from pathlib import Path

audio_path = Path("out/Ride_On_M1_v1/Ride_On_M1_v1.mp3")
device = "cuda"   # or "mps" / "cpu"

model = whisperx.load_model("medium", device)
audio = whisperx.load_audio(str(audio_path))
result = model.transcribe(audio, batch_size=8)

align_model, metadata = whisperx.load_align_model(
    language_code=result["language"], device=device
)
result = whisperx.align(
    result["segments"], align_model, metadata, audio, device,
    return_char_alignments=False,
)

# Emit word-level timestamp CSV
with open("out/Ride_On_M1_v1/Ride_On_M1_v1_words.csv", "w") as fh:
    fh.write("start,end,word,score\n")
    for seg in result["segments"]:
        for w in seg["words"]:
            fh.write(f"{w['start']:.3f},{w['end']:.3f},{w['word']},{w['score']:.3f}\n")
```

### Step 3 — Build the LRC

Using Approach B from [§ 3 Step 3](#step-3--build-lrc-lines) — anchor each
lyric line to its first word's timestamp:

```python
from pathlib import Path

audio_stem = Path("out/Ride_On_M1_v1/Ride_On_M1_v1")
lyrics = (audio_stem.with_name(audio_stem.name + "_lyrics.txt")).read_text(
    encoding="utf-8"
)
words = [
    (float(line.split(",")[0]), line.split(",")[2])
    for line in (audio_stem.with_name(audio_stem.name + "_words.csv"))
        .read_text(encoding="utf-8").splitlines()[1:]
]

SECTION_TAGS = {
    "[Intro]", "[Verse]", "[Pre Chorus]", "[Chorus]",
    "[Bridge]", "[Outro]", "[Break]", "[Inst]", "[Solo]",
    "[Interlude]", "[Transition]", "[Post Chorus]", "[Hook]",
    "[Build Up]",
}

# Project lyric lines onto word-level timestamps (greedy, left-to-right).
word_idx = 0
out_lines = []
unaligned = []

def to_lrc_ts(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = seconds - minutes * 60
    return f"[{minutes:02d}:{secs:06.3f}]"

for raw in lyrics.splitlines():
    line = raw.strip()
    if not line:
        continue
    if line in SECTION_TAGS:
        # Section tag becomes its own timestamped line; the lyric line
        # that follows will share this timestamp.
        section_ts = words[min(word_idx, len(words) - 1)][0]
        out_lines.append((section_ts, line))
        continue
    # Lyric line — anchor to current word pointer
    if word_idx < len(words):
        ts = words[word_idx][0]
        out_lines.append((ts, line))
        # Advance word pointer by the number of word tokens in this line
        tokens = line.split()
        word_idx += len(tokens)
    else:
        # Out of alignment data: do not invent a timestamp. Stop and report
        # the unaligned lines so they can be re-aligned or timed by hand.
        unaligned.append(line)

if unaligned:
    raise SystemExit(f"{len(unaligned)} lyric line(s) have no alignment; re-align or time them manually: {unaligned[:3]}")

# Emit .lrc
lrc_path = audio_stem.with_suffix(".lrc")
with lrc_path.open("w", encoding="utf-8") as fh:
    fh.write(f"[ar:Cold Mountain]\n")
    fh.write(f"[ti:Ride On]\n")
    fh.write(f"[al:Jengi Sessions]\n")
    for ts, text in out_lines:
        fh.write(f"{to_lrc_ts(ts)}{text}\n")
```

### Step 4 — Validate

```bash
python3 ../../tests/analyzers/lrc_validator.py \
    out/Ride_On_M1_v1/Ride_On_M1_v1.lrc --json
```

Expected: `"valid": true`, `"line_count"` matching the number of lyric +
section lines, no errors. Warnings (e.g. "Missing `[length:]`") are
informational only.

### Step 5 — Deliver

The final layout:

```text
out/Ride_On_M1_v1/
- Ride_On_M1_v1.mp3
- Ride_On_M1_v1.lrc            (the LRC file)
- Ride_On_M1_v1_lyrics.txt     (original lyrics input)
- Ride_On_M1_v1_words.csv      (WhisperX intermediate, debug only)
- Ride_On_M1_v1_prompt.txt
```

Open the `.lrc` in any karaoke player (MiniLyrics, Kanto, Vanilla Lyrics,
AIMP) and confirm the highlight scrolls synchronously with the audio.
If it drifts, re-run alignment with `large-v2` or hand-anchor the chorus.

## Quick Reference

| Task | Command |
| --- | --- |
| Validate an LRC file | `python3 ../../tests/analyzers/lrc_validator.py path/to/song.lrc` |
| Validate as JSON | `python3 ../../tests/analyzers/lrc_validator.py path/to/song.lrc --json` |
| Convert non-UTF-8 to UTF-8 | `iconv -f latin1 -t utf-8 in.lrc > out.lrc` |
| Get audio duration | `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 file.mp3` |
| Inspect word-level timestamps | Open `*_words.csv` next to the audio in a spreadsheet |

## Limitations

- **Timestamp precision is bounded by the alignment model.** WhisperX is
  ~20 ms; vanilla Whisper is ~200–500 ms. Going tighter than the
  alignment model allows is fiction.
- **No styling.** LRC cannot carry font, color, position. For styled
  video subtitles use SRT, WebVTT, or ASS.
- **Section tags are not standardized.** Different players treat
  `[Intro]` slightly differently. Stick to the canonical tags listed
  in [`references/structure-tags.md`](structure-tags.md).
- **Instrumental sections need manual timestamps.** If the singer is
  silent, there is nothing to align; emit a section-tag line at the
  expected time or omit the line.
- **Lyrics provided to the generator may not match what was actually
  sung.** Verify with `scripts/verify_lyrics_alignment.py` before
  publishing an LRC; the validator only checks format, not accuracy.

## See Also

- [`references/structure-tags.md`](structure-tags.md) — section-tag catalog, default structure, ASR sanity checks
- [`references/lyrics-cleanup.md`](lyrics-cleanup.md) — cleanup recipe for ASR transcripts and section tags
- [`references/acestep-generation.md`](acestep-generation.md) — ACE-Step generation workflow
- [`references/other-backends.md`](other-backends.md) — MusicGen, Stable Audio, generic CLI backends, MiniMax Music 3 notes
- [`../../tests/analyzers/lrc_validator.py`](../../tests/analyzers/lrc_validator.py) — canonical LRC validator
- [`../../tests/unit/test_lrc_format.py`](../../tests/unit/test_lrc_format.py) — LRC validator unit tests
