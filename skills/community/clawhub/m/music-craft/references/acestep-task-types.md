# ACE-Step Task Types Reference

Per-task reference for the five ACE-Step 1.5 **audio-conditioned** task types:
`cover`, `repaint`, `extract`, `lego`, and `complete`. Use this when the
request requires anything beyond plain text-to-music generation. Load
[`acestep-generation.md`](acestep-generation.md) first for the base
3-step workflow (submit, poll, collect), quality tiers, and the
`task_type` table.

## Audio-Conditioned Generation (umbrella category)

Every task below conditions on an input audio file. They differ in **what
the model is asked to produce** from that audio:

| `task_type` | What it does | Output count | Model support |
| --- | --- | --- | --- |
| `cover` | Re-style a song while following its melody and structure | 1 | BASE + SFT + TURBO |
| `repaint` | Regenerate only a time window, keep the rest of the audio | 1 | BASE + SFT + TURBO |
| `extract` | Stem separation (vocals / drums / bass / etc.) | 1–2 | **BASE only** |
| `lego` | Add a new instrument layer on top of existing audio | 2+ | **BASE only** |
| `complete` | Fill out a partial track with mixed accompaniment (e.g. Vocal2BGM) | 1 | **BASE only** |

> **BASE-only warning** — `extract`, `lego`, and `complete` are only
> supported by `acestep-v15-base` and `acestep-v15-xl-base`. They
> silently fail or refuse on `*turbo` and `*sft` checkpoints. The
> BASE model is research-grade in this skill's stack as of 2026-07;
> smoke-test on your hardware before promising production reliability.

## Model support matrix (verified upstream)

| DiT Model | Pre-Train | SFT | RL | CFG | Steps | Cover | Repaint | Extract | Lego | Complete |
| --- | :---: | :---: | :--: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `acestep-v15-base` | ✅ | ❌ | ❌ | ✅ | 50 | ✅ | ✅ | ✅ | ✅ | ✅ |
| `acestep-v15-sft` | ✅ | ✅ | ❌ | ✅ | 50 | ✅ | ✅ | ❌ | ❌ | ❌ |
| `acestep-v15-turbo` | ✅ | ✅ | ❌ | ❌ | 8 | ✅ | ✅ | ❌ | ❌ | ❌ |
| `acestep-v15-xl-base` | ✅ | ❌ | ❌ | ✅ | 50 | ✅ | ✅ | ✅ | ✅ | ✅ |
| `acestep-v15-xl-sft` | ✅ | ✅ | ❌ | ✅ | 50 | ✅ | ✅ | ❌ | ❌ | ❌ |
| `acestep-v15-xl-turbo` | ✅ | ✅ | ❌ | ❌ | 8 | ✅ | ✅ | ❌ | ❌ | ❌ |

> Source: `ACE-Step-1.5/README.md` § Model Zoo (DiT Models / XL DiT
> Models) plus the base `GenerationParams.task_type` enum in
> `acestep/inference.py`.

## Switching to a BASE-only model

BASE-only tasks fail with turbo/SFT. Before submitting an `extract`,
`lego`, or `complete` request, switch the loaded DiT:

```bash
# Switch to BASE (download acestep-v15-base first if not on disk)
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-base", "lm_model": "acestep-5Hz-lm-1.7B"}'

# Switch back to standard (turbo) after the task
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-turbo", "lm_model": "acestep-5Hz-lm-1.7B"}'
```

**XL-BASE path** (≥20 GB VRAM recommended):

```bash
python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-xl-base", "lm_model": "acestep-5Hz-lm-1.7B"}'
```

> Switching models reloads the DiT weights (~10–90 s cold start). Do
> not batch BASE-only and turbo/SFT tasks in the same minute.

## Uploading source audio (all tasks)

The API **rejects absolute file paths** in JSON (`{"detail":"absolute audio
file paths are not allowed"}`). Upload via multipart form-data:

| Field name | When |
| --- | --- |
| `src_audio` | cover, repaint, extract, lego, complete — the audio the model edits / conditions on |
| `reference_audio` / `ref_audio` | style-transfer reference (global timbre / mix feel, NOT melody) |

Send all other parameters as form fields:

```bash
python3 scripts/acestep_request.py release_task \
  --form 'task_type=<TASK>' \
  --form-file src_audio=/path/to/source.wav \
  --form '<other_field>=<value>'
```

> **Path caveat:** the file must exist on the server's filesystem or be
> uploaded through the multipart `src_audio` field. A path on the
> client's machine is never accepted.

## Polling and output collection (all tasks)

Same 3-step pattern as text2music:

1. Submit via `/release_task` (returns `task_id`).
2. Poll `/query_result` with `{"task_ids": ["..."]}`. Treat empty `data`
   as "still running" — see `acestep-generation.md` Polling caveat.
3. Collect from `${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/` once
   `status: 1` (success) appears. Cache-file detection (rather than
   `/query_result`) is the reliable completion signal under load.

Use [`scripts/wait_for_acestep.py`](../scripts/wait_for_acestep.py)
when available — it reconciles polling with cache-file detection.

## LM behavior per task type

| `task_type` | LM (`thinking`) | Why |
| --- | --- | --- |
| `text2music` | runs if `thinking=true` | default flow |
| `cover` | **skipped** | caption + lyrics come directly from the user; LM rewriting can fight the source |
| `repaint` | **skipped** | same reason as cover |
| `extract` | **skipped** | upstream note: LM-generated captions can cause DiT to reconstruct input instead of extracting stems |
| `lego` | runs if `thinking=true` | uses LM planning for the new layer |
| `complete` | runs if `thinking=true` | uses LM planning for the accompaniment |

**Implication:** for `cover`/`repaint`/`extract`, the `caption` and
`lyrics` fields you submit are used **verbatim**. Write them well.
`thinking: true` is silently ignored.

---

## 1. Cover

**Purpose:** Re-style a song while following its melody and structure.
Generate "in the style of X" renditions of an existing song. Local,
melody-aware alternative to cloud cover services.

### Inputs

- `src_audio` — the song you want to restyle (multipart upload, not a
  path). Format: any of `wav`, `mp3`, `flac`, `opus`, `aac`.
- `caption` — the style you want (genre + instruments + vocal character
  - mood + production). Use the same detailed multi-dimensional format
  as text2music (see `acestep-generation.md` Prompt format).
- `lyrics` — optional; defaults to empty (instrumental cover) or what
  the model infers.
- `audio_cover_strength` — how strictly to follow the source melody
  (see Parameters).
- Metas (`bpm`, `key_scale`, `time_signature`, `vocal_language`) — set
  explicitly for tighter control.

### Outputs

- **1 file** at `${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/`,
  duration auto-locked to the source length (`audio_duration` is
  ignored).

### Use cases

- Genre-jump covers (rock → synthwave, acoustic → orchestral).
- A/B a melody in different keys or tempos without re-recording.
- Local cover generation when the user wants a private / offline
  workflow.

### Parameters

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `task_type` | string | — | Must be `"cover"`. |
| `src_audio` | file | required | Multipart upload. |
| `caption` | string | required | Style description. Detailed, multi-dimensional. |
| `lyrics` | string | empty | If set, model sings this against the source melody. |
| `audio_cover_strength` | float | `1.0` | 0.0–1.0. Lower = bigger restyle. See table below. |
| `bpm` | int | none | Recommended: read source BPM first and set it explicitly. |
| `key_scale` | string | `""` | E.g. `"D major"`, `"A minor"`. |
| `time_signature` | string | `""` | E.g. `"4/4"`. |
| `vocal_language` | string | `"unknown"` | Set explicitly; LM is skipped. |
| `audio_format` | string | `"flac"` | Lossless for cover work — lossy MP3 round-trip degrades melody. |

**`audio_cover_strength` heuristic (verified in `acestep-generation.md`):**

| Value | Behavior |
| --- | --- |
| `0.2`–`0.4` | Strong genre jump (rock → synthwave). Most free interpretation. |
| `0.5`–`0.7` | Balanced — keeps the melody, allows noticeable style change. |
| `0.8`–`0.9` | Subtle restyle. Closer to source timbre. |
| `1.0` | Closest possible to source. |

### Example command

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task \
  --print-task-id \
  --form task_type=cover \
  --form-file src_audio=/path/to/source/rock_track.wav \
  --form audio_cover_strength=0.35 \
  --form 'prompt=dreamy 80s synthwave, warm analog synths, gated-reverb drums, arpeggiated bass, neon night-drive mood' \
  --form bpm=129 \
  --form 'key_scale=D major' \
  --form audio_format=wav)

# Poll until ready
python3 scripts/wait_for_acestep.py "$TASK_ID" --expected-seconds <audio_duration>
```

### Limitations

- **Source-length cap.** A full ~5-minute cover hits the default
  600 s server timeout on 12 GB-class hardware. Trim the source with
  `ffmpeg -ss <start> -t 60 -i in.wav out.wav` for short experiments,
  or raise `ACESTEP_GENERATION_TIMEOUT=3600`.
- **Melody capture is approximate.** Sparse, mid/slow-tempo songs work
  best; dense / fast / percussive sources tend to lose melodic detail.
  Expect variation, not an exact pitch-perfect copy.
- **LM is skipped.** Your caption and lyrics are used verbatim — a weak
  caption degrades results more than on text2music.
- **No style-transfer / mashup support.** Two-song mashups are not
  available in this skill; say so.
- **No cancel endpoint.** Lint the request before submitting; cancel
  is not available mid-job.

### Quality tips

- **Always request lossless output** (`audio_format=wav` or `flac`)
  when iterating on style — MP3 round-trip hides melody artifacts.
- **Trim the source** to a section with clear melodic content for
  faster, more reliable covers. Cover the full song only on the
  final pass.
- **Set explicit BPM / key.** LM is skipped, so the model cannot infer
  from your prompt.
- **Generate a small batch** (`batch_size: 2–4`) and pick the best —
  cover quality varies more across seeds than text2music.
- **Validate with `tests/analyzers/task_validator.py`:**

  ```bash
  python3 tests/analyzers/task_validator.py cover \
      /path/to/source.wav /path/to/cover_output.wav --json
  ```

  Confirms output duration matches source within ±0.5 s.

### Routing gate

Use ACE-Step cover only when the user explicitly accepts a local,
slower, experimental workflow. There is no fast cloud cover path any more
(MiniMax music generation is no longer available).

---

## 2. Repaint

**Purpose:** Regenerate only a time window of an existing audio file,
keep the rest untouched. Fix a bad section without throwing away the
whole track.

### Inputs

- `src_audio` — the audio you want to patch (multipart upload).
- `repainting_start`, `repainting_end` — seconds, define the window
  to regenerate. `repainting_end: -1` means "until end of audio".
- `caption` — describes the new content for that window only.
- `lyrics` — optional; if set, replaces lyrics in the window.
- `repaint_mode` — `conservative` / `balanced` / `aggressive`.
- `repaint_strength` — float 0–1 (balanced mode only); higher = stick
  closer to source.

### Outputs

- **1 file** at the cache dir, **same total duration as the source**.
  Only the `[start, end)` window is regenerated; everything outside
  the window is preserved.

### Use cases

- Fix a mispronounced word in `[Chorus]` of an otherwise good track.
- Replace a weak bridge with a stronger arrangement.
- Add a section transition (e.g. change Verse → Pre-Chorus feel at
  `30 s`).
- "Continue writing" — extend the end of a track by repainting the
  last 10–30 s.

### Parameters

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `task_type` | string | — | Must be `"repaint"`. |
| `src_audio` | file | required | Multipart upload. |
| `repainting_start` | float | `0.0` | Seconds. |
| `repainting_end` | float | `-1` | Seconds. `-1` = end of file. |
| `caption` | string | required | Content for the repainted window. |
| `lyrics` | string | empty | Lyrics inside the window only. |
| `repaint_mode` | string | `"balanced"` | `conservative` (safer, sticks close to source) / `balanced` (default) / `aggressive` (more freedom). |
| `repaint_strength` | float | `0.5` | 0.0–1.0; only used in `balanced` mode. Higher = closer to source. |
| `chunk_mask_mode` | string | `"auto"` | `"explicit"` = hard 0/1 mask from range; `"auto"` = model decides per chunk. |
| `repaint_latent_crossfade_frames` | int | `10` | Latent-level blend width at boundaries (~0.4 s). |
| `repaint_wav_crossfade_sec` | float | `0.0` | Waveform splice crossfade in seconds; `0` = hard cut. |
| `audio_format` | string | `"flac"` | Lossless strongly recommended — lossy boundaries are audible. |
| `bpm` / `key_scale` / etc. | — | — | Set explicitly to anchor the new window. |

### Example command

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task \
  --print-task-id \
  --form task_type=repaint \
  --form-file src_audio=/path/to/source/track_with_bad_chorus.wav \
  --form repainting_start=72.0 \
  --form repainting_end=104.0 \
  --form repaint_mode=balanced \
  --form repaint_strength=0.6 \
  --form 'prompt=anthemic chorus, soaring female vocal, full band, big drums' \
  --form 'lyrics=[Chorus]\nWe rise together\nInto the light' \
  --form audio_format=wav)
```

### Limitations

- **Window size.** Operates best on 3–90 s windows. Very short windows
  (<3 s) may not give the model enough context; very long windows
  (>90 s) start to drift from the source.
- **Boundary artifacts.** Even with `repaint_wav_crossfade_sec: 0.2`,
  edges between preserved and regenerated audio are audible if the
  source and the new content disagree on tempo/key. Sample-rate and
  bit-depth must match (default 48 kHz / float32).
- **Same total duration as source.** The repaint does not extend or
  shorten the track — only replaces content inside the window.
- **LM is skipped.** Caption is used verbatim. A vague caption gives
  a vague repaint.
- **No cancel.** Repaints on long sources (>3 min) take several
  minutes; verify the window before submitting.
- **Single-worker queue.** A failed repaint blocks subsequent jobs
  until the timeout fires.

### Quality tips

- **Pick the window from a structural analysis.** Use
  `references/structure-tags.md` to identify `[Verse]` / `[Chorus]` /
  `[Bridge]` boundaries, then target a single section.
- **Start with `repaint_mode=balanced` + `repaint_strength=0.6`**.
  Move to `aggressive` if the result is too similar to the source.
- **Match metas to the source.** Set `bpm` and `key_scale` to the
  detected values; mismatched keys make the boundary click.
- **Keep the window ≤ 60 s** for the first attempt. Smaller windows
  are faster, safer, and easier to validate.
- **Validate with `tests/analyzers/task_validator.py`:**

  ```bash
  python3 tests/analyzers/task_validator.py repaint \
      /path/to/source.wav /path/to/repainted.wav --json
  ```

  Output duration must match source within ±0.5 s.

---

## 3. Extract (**BASE-only**)

**Purpose:** Stem separation — extract a specific instrument or vocal
track from a mixed audio file. Local alternative to Demucs/Spleeter,
but experimental.

### Inputs

- `src_audio` — the mixed audio (multipart upload).
- `instruction` — must specify which track to extract. Auto-generated
  from `task_type` if omitted. Common forms:
  - `"Extract the vocals track from the audio:"`
  - `"Extract the drums track from the audio:"`
  - `"Extract the bass track from the audio:"`

### Outputs

- **1 file** (the extracted stem) at the cache dir, **same duration as
  the source**. The model writes the requested stem; it does NOT also
  write the residual (use `complete` or Demucs for residual
  extraction).

### Use cases

- Quick vocals / drums / bass isolation from a finished mix.
- Pre-process for `lego` (extract vocals → lego new drums on top).
- Local stem analysis when Demucs is not installed or too slow.

### Supported tracks (12 instrument families)

From `acestep/constants.py` § `TRACK_NAMES`:

`vocals`, `backing_vocals`, `drums`, `bass`, `guitar`, `keyboard`,
`percussion`, `strings`, `synth`, `fx`, `brass`, `woodwinds`.

### Parameters

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `task_type` | string | — | Must be `"extract"`. |
| `src_audio` | file | required | Multipart upload. |
| `instruction` | string | auto | `"Extract the {TRACK_NAME} track from the audio:"`. Pick one of the 12 names. |
| `audio_format` | string | `"flac"` | Lossless recommended. |
| `inference_steps` | int | `8` | BASE supports 32–64. Higher = cleaner separation but slower. |
| `guidance_scale` | float | `7.0` | BASE only. |
| `shift` | float | `3.0` | BASE only. Try `1.0` or `5.0` if defaults feel off. |
| `thinking` | bool | true | **Skipped** for extract (per upstream). Do not expect CoT planning. |

### Example command

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task \
  --print-task-id \
  --form task_type=extract \
  --form-file src_audio=/path/to/source/full_mix.wav \
  --form 'instruction=Extract the vocals track from the audio:' \
  --form audio_format=wav \
  --form inference_steps=32)
```

### Limitations

- **BASE-only.** Fails on `*turbo` and `*sft` checkpoints. Switch
  models first (see "Switching to a BASE-only model" above).
- **No residual output.** You get one stem per request. To get
  "vocals + accompaniment", submit two extracts (one for vocals, one
  for the rest via `instrumental`-style instruction) or use Demucs.
- **LM is skipped.** Do not pass `caption`/`lyrics` — extract uses
  `instruction` only. Upstream note: LM-generated captions can cause
  DiT to reconstruct input audio instead of extracting stems.
- **Lower quality than Demucs** in published benchmarks. For
  production-quality stem separation, prefer `scripts/extract_stems.py`
  (Demucs wrapper) which writes a `stems.json` with normalized
  paths.
- **Output can leak source audio** when the chosen stem does not
  exist (e.g. asking for "saxophone" on a track with no sax). Treat
  unexpected content as a failure signal, not a success.
- **No cancel.** Long sources take minutes; check the duration
  before submitting.

### Quality tips

- **Start with vocals.** Vocals separation is the most reliably
  trained task; drums and bass are next. Fx / woodwinds are the
  weakest.
- **Match source sample rate.** Default 48 kHz; resample with ffmpeg
  if your source is 44.1 kHz.
- **For full stems**, use the Demucs helper path in
  `acestep-generation.md` (`scripts/extract_stems.py`) and skip
  ACE-Step extract entirely.
- **Validate with `tests/analyzers/task_validator.py`:**

  ```bash
  python3 tests/analyzers/task_validator.py extract \
      /path/to/source.wav /path/to/vocals.wav /path/to/instrumental.wav --json
  ```

  Confirms both stems are within ±0.5 s of the source duration.

### Routing gate

ACE-Step extract is **experimental**. For arranger workflows, prefer
the Demucs path documented in `acestep-generation.md`. Use ACE-Step
extract only when Demucs is not available and the user accepts a
research-grade result.

---

## 4. Lego (**BASE-only**)

**Purpose:** Add a new instrument layer on top of existing audio. Feed
in a backing track, ask for "the guitar track based on the audio
context", and the model renders a matching guitar layer that fits
rhythm, harmony, and timbre.

### Inputs

- `src_audio` — the existing audio (multipart upload). The "context"
  the model layers against.
- `instruction` — must specify which track to add. Forms:
  - `"Generate the vocals track based on the audio context:"`
  - `"Generate the drums track based on the audio context:"`
  - `"Generate the guitar track based on the audio context:"`
- `caption` — style description for the new layer.
- `repainting_start` / `repainting_end` — optional. Defines where in
  the source the new layer plays. Default: full length. If you set a
  window, the layer only renders there.

### Outputs

- **2+ files** at the cache dir:
  1. The **new layer** (e.g. `vocals.wav`) — only the added instrument.
  2. (Optional / depending on mode) A **combined mix** of source + new
     layer.

  Exact file count is implementation-dependent — always check the
  cache dir for new files, not just `/query_result`.

### Use cases

- Layer a guitar part on top of an existing drum + bass recording.
- Add backing vocals to a lead-vocal-only take.
- Build a multi-track composition iteratively (one instrument per
  request).
- Create a Stem2Track conversion: take a stem from `extract`, add a
  new layer via `lego`.

### Supported tracks (12)

Same as `extract`: `vocals`, `backing_vocals`, `drums`, `bass`,
`guitar`, `keyboard`, `percussion`, `strings`, `synth`, `fx`, `brass`,
`woodwinds`.

### Parameters

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `task_type` | string | — | Must be `"lego"`. |
| `src_audio` | file | required | The audio to layer against. |
| `instruction` | string | auto | `"Generate the {TRACK_NAME} track based on the audio context:"`. |
| `caption` | string | empty | Style description for the new layer. |
| `lyrics` | string | empty | If the new layer is vocals. |
| `repainting_start` | float | `0.0` | Optional window start (seconds). |
| `repainting_end` | float | `-1` | Optional window end; `-1` = end. |
| `global_caption` | string | empty | Song-level caption for "SFT-stems lego" mode (when using SFT-stems). |
| `inference_steps` | int | `8` | BASE supports 32–64. |
| `guidance_scale` | float | `7.0` | BASE only. |
| `shift` | float | `3.0` | BASE only. |
| `thinking` | bool | true | **Runs** for lego (unlike cover/repaint/extract). LM helps plan the new layer. |

### Example command

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task \
  --print-task-id \
  --form task_type=lego \
  --form-file src_audio=/path/to/source/drums_and_bass.wav \
  --form 'instruction=Generate the guitar track based on the audio context:' \
  --form 'prompt=clean electric guitar, bluesy lead, mid-gain, expressive bends' \
  --form audio_format=wav \
  --form inference_steps=32)
```

### Limitations

- **BASE-only.** Fails on turbo/SFT. Switch first.
- **LM is required for best results.** Unlike cover/repaint/extract,
  lego uses LM planning — keep `thinking=true` and a non-empty
  `caption`.
- **New layer matches source rhythm/feel, not exact pitches.** Expect
  a complementary part, not a transposed copy.
- **File count varies.** Always inspect the cache dir after a lego
  job; do not assume a specific output filename pattern.
- **Cannot replace existing tracks.** Lego adds; it does not
  re-record. To change a track that's already in the mix, use
  `extract` first, then `lego` the replacement.
- **No cancel.** Long sources (5+ min) take a long time; trim the
  source to the section you actually need layered.
- **Stereo image is approximate.** The new layer lands roughly in
  the right place but does not preserve precise panning.

### Quality tips

- **Provide a strong context track.** A clean drums+bass mix gives
  better lego results than a busy full mix — the model has clearer
  rhythmic anchors.
- **Match BPM / key explicitly.** Unlike cover/repaint, lego runs LM,
  but explicit metas still anchor the new layer to the source's
  tempo / tonality.
- **Use `repainting_start` / `repainting_end` for sections.** A
  guitar solo from 60 s to 90 s is much easier to validate than a
  full-length layer.
- **Iterate.** Lego is a "first draft" task — expect to layer
  multiple times (vocals → guitar → keys) and combine with
  `scripts/remix_stems.py`.
- **Validate with `tests/analyzers/task_validator.py`:**

  ```bash
  python3 tests/analyzers/task_validator.py lego \
      /path/to/source.wav /path/to/original.wav /path/to/new_layer.wav --json
  ```

  Source duration and original duration must match; new layer
  duration may differ if a window was used (warning, not error).

---

## 5. Complete (**BASE-only**)

**Purpose:** Fill out a partial track with a full mixed accompaniment
("Vocal2BGM" pattern). Feed in a single vocal take; the model
generates a complete backing track (drums + bass + keys + etc.) that
matches rhythm, harmony, and style.

### Inputs

- `src_audio` — the partial / a-cappella track (multipart upload).
- `instruction` — must specify which tracks to add. Forms:
  - `"Complete the input track with drums, bass, guitar:"`
  - `"Complete the input track with drums, bass, guitar, keyboard:"`
  - `"Complete the input track with piano, strings:"`
- `caption` — style description for the accompaniment.

### Outputs

- **1 file** at the cache dir — a mix of the source (preserved) plus
  the generated accompaniment. **Output duration is typically ≥ 1.5×
  source duration** (the model often extends intros/outros).

### Use cases

- Turn a vocal-only phone recording into a demo with drums + bass +
  keys.
- Add a backing track to a melodic sketch (piano/vocal) for a fuller
  arrangement.
- Reverse-Vocal2BGM: feed a stripped instrumental and ask for vocal-
  like top-line.

### Parameters

| Parameter | Type | Default | Notes |
| --- | --- | --- | --- |
| `task_type` | string | — | Must be `"complete"`. |
| `src_audio` | file | required | Partial / a-cappella track. |
| `instruction` | string | auto | `"Complete the input track with {TRACK_CLASSES}:"`. Comma-separated track list from the 12 supported families. |
| `caption` | string | empty | Style description for the accompaniment. |
| `lyrics` | string | empty | Optional; if the source is vocal, the model can align. |
| `inference_steps` | int | `8` | BASE supports 32–64. |
| `guidance_scale` | float | `7.0` | BASE only. |
| `shift` | float | `3.0` | BASE only. |
| `thinking` | bool | true | **Runs** for complete (LM plans the accompaniment arrangement). |

### Example command

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task \
  --print-task-id \
  --form task_type=complete \
  --form-file src_audio=/path/to/source/vocal_only_take.wav \
  --form 'instruction=Complete the input track with drums, bass, guitar, keyboard:' \
  --form 'prompt=indie folk, acoustic drums, upright bass, fingerstyle guitar, soft piano' \
  --form 'lyrics=[Verse]\nwalking through the morning light\nnothing feels the same' \
  --form audio_format=wav \
  --form inference_steps=32)
```

### Limitations

- **BASE-only.** Fails on turbo/SFT.
- **Extends the source.** The model often adds intro/outro pads to
  smooth the entry and exit. If you need the exact source length,
  trim the output with ffmpeg after the job completes.
- **Single accompaniment shape.** The model picks one arrangement;
  re-running with different seeds gives different arrangements.
  There is no control over individual instrument layers here — use
  `lego` after `complete` for that.
- **LM is required for best results.** Keep `thinking=true` and
  write a specific `caption`.
- **Vocal-source alignment depends on quality.** A noisy / roomy
  phone vocal gives weaker alignment than a clean studio take.
- **No cancel.** Long sources take minutes; trim the source to the
  section you actually need filled.
- **Output style is global, not sectional.** The whole
  accompaniment uses one style; per-section variation requires
  multiple `repaint` passes after `complete`.

### Quality tips

- **Source vocal quality matters.** A clean, pitched vocal gives
  better accompaniment than a noisy phone recording. Noise removal
  with ffmpeg before the request is worth it.
- **Be specific in `instruction`.** `"drums, bass, guitar"` gives a
  standard trio; `"drums, bass, guitar, keyboard, strings"` gives
  a fuller arrangement. Empty / vague instructions give vague
  results.
- **Set BPM / key from the source.** Detect first (use the librosa
  pipeline or ACE-Step's audio-understanding mode) and pass
  explicitly — the model anchors the accompaniment to those.
- **Generate 2–4 variations** (`batch_size: 2–4`) and pick the best.
  Arrangement quality varies more across seeds than across caption
  changes.
- **Validate with `tests/analyzers/task_validator.py`:**

  ```bash
  python3 tests/analyzers/task_validator.py complete \
      /path/to/partial.wav /path/to/completed.wav --json
  ```

  Output duration must be ≥ source duration; warns if < 1.5×.

---

## Cross-task operational notes

### Server timeouts

Default `ACESTEP_GENERATION_TIMEOUT=600` (10 min). BASE tasks on long
sources routinely exceed this. **Set `ACESTEP_GENERATION_TIMEOUT=3600`
(1 h)** whenever you intend to run BASE-only tasks:

```bash
ACESTEP_GENERATION_TIMEOUT=3600 \
ACESTEP_CONFIG_PATH=acestep-v15-base \
ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B \
uv run acestep-api --port 8001
```

### Memory budgets (24 GB M3 reference)

| Task | Model | Approx peak RAM | Wall time per 60 s audio |
| --- | --- | --- | --- |
| cover | turbo | ~11 GB | ~3–5 min |
| cover | xl-sft | ~25–30 GB | ~10–15 min |
| repaint | turbo | ~11 GB | ~3–5 min |
| repaint | xl-sft | ~25–30 GB | ~10–15 min |
| extract | base | ~10 GB | ~3–6 min |
| extract | xl-base | ~25–30 GB | ~15–25 min |
| lego | base | ~10 GB | ~3–6 min |
| lego | xl-base | ~25–30 GB | ~15–25 min |
| complete | base | ~10 GB | ~3–6 min |
| complete | xl-base | ~25–30 GB | ~15–25 min |

See `acestep-generation.md` § Quality Tiers for the full
memory-probe protocol.

### Smoke-test before production

Per item 13e of `music-craft_ROADMAP.md`: **do not promise production
reliability for `extract`, `lego`, or `complete` until smoke tests
land on this machine.** Minimum smoke test for each:

1. Download the BASE model (or XL-BASE if RAM allows):

   ```bash
   uv run acestep-download --model acestep-v15-base
   ```

2. Switch the loaded DiT:

   ```bash
   python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-base"}'
   ```

3. Run a 30-second task (extract a vocal, lego a guitar on a 30 s
   backing, complete a 30 s vocal) and validate with
   `tests/analyzers/task_validator.py`.
4. Only after that passes on your hardware, accept user requests.

### Output naming and caching

All outputs land under
`${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/` with auto-generated
filenames. There is no per-task subdirectory — sort by `task_id` and
collection time:

```bash
# After a task completes
find "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  -type f -newer /tmp/last_marker -name '*.wav' -o -name '*.flac' -o -name '*.mp3'
```

Cache accumulation is the same caveat as text2music — see
`acestep-generation.md` Cache caveat. Review before deleting.

### Validation helper

`tests/analyzers/task_validator.py` accepts task type + file paths
and validates output shape per task:

| Task | Required files | Checks |
| --- | --- | --- |
| `cover` | 2 (source, cover) | output duration ≈ source |
| `repaint` | 2 (source, repainted) | output duration ≈ source |
| `extract` | 3 (source, vocal, instrumental) | both stems ≈ source duration |
| `lego` | 3 (source, original, new_layer) | original ≈ source; new_layer may be shorter |
| `complete` | 2 (partial, completed) | completed ≥ partial; warns if < 1.5× |

```bash
python3 tests/analyzers/task_validator.py <task> <files...> --json
```

Exits 0 = valid, 1 = invalid, 2 = error (missing deps / wrong arg count).
Use `--json` for machine-readable output; omit for human summary.

### Common errors

| Symptom | Cause | Fix |
| --- | --- | --- |
| `task_type` rejected | wrong task for current DiT | switch to BASE for extract/lego/complete |
| Output is a reconstruction of input | extract with bad `instruction` or LM-coaxed caption | drop `caption`/`lyrics`; verify `instruction` is exact |
| Window boundary click | repaint with mismatched key/tempo | match source metas; raise `repaint_wav_crossfade_sec` |
| Server timeout fired mid-job | default 600 s on long source | set `ACESTEP_GENERATION_TIMEOUT=3600` |
| Output duration wrong | turbo steps used with BASE | BASE tasks need `inference_steps` ≥ 32 |
| Empty `/query_result` while running | known server quirk | use cache-file detection, not just `/query_result` |
| `absolute audio file paths are not allowed` | JSON body with file path | use multipart `-F "src_audio=@/path"` |

### Routing decision tree

When the request involves source audio:

| Request shape | Recommended path |
| --- | --- |
| Re-style a song while keeping the melody | ACE-Step `cover` (this skill) |
| Fix a bad section of an existing track | ACE-Step `repaint` (this skill) |
| Two-song mashup or emotion-driven style transfer | Not available (MiniMax music generation was discontinued) |
| Stem separation (vocals / drums / bass) | Demucs via `scripts/extract_stems.py` (faster, higher quality) — ACE-Step `extract` only if Demucs unavailable |
| Add an instrument layer to a backing track | ACE-Step `lego` (this skill) |
| Add full backing to a vocal-only take | ACE-Step `complete` (this skill) — Vocal2BGM |
| Generate from a prompt with no source audio | text2music (see `acestep-generation.md`) |

---

## See also

- [`acestep-generation.md`](acestep-generation.md) — base 3-step workflow,
  quality tiers, full prompt/parameter table, MP3/FLAC cache details.
- [`setup-and-preflight.md`](setup-and-preflight.md) — dependency consent,
  platform detection, ML budget probe.
- [`wait-and-collect.md`](wait-and-collect.md) — M1 → wait → collect → M2
  sequencing pattern.
- [`local-ace-step-curl-template.md`](local-ace-step-curl-template.md) —
  JSON-safe `/release_task` template.
- [`structure-tags.md`](structure-tags.md) — section tag vocabulary for
  picking repaint windows.
- [`../../tests/analyzers/task_validator.py`](../../tests/analyzers/task_validator.py)
  — output-shape validator for all five task types.
- ACE-Step upstream:
  [`README.md`](../../../../ACE-Step-1.5/README.md) § Model Zoo,
  [`docs/en/INFERENCE.md`](../../../../ACE-Step-1.5/docs/en/INFERENCE.md)
  § Task Types,
  [`docs/en/Tutorial.md`](../../../../ACE-Step-1.5/docs/en/Tutorial.md)
  § "Base Model Advanced Audio Control Tasks".
