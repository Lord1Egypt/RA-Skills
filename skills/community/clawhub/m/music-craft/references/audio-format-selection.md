# Audio Format Selection

Reference for ACE-Step 1.5 output container/codec choice and `ffmpeg`
delivery paths. Load only for generated-audio output: audio file format, audio quality vs.
size trade-off, streaming masters, or ACE-Step `audio_format` / `output_format`.
Not for non-audio file formats.

> **Status:** Tier 3 reference. Backed by `ACE-Step-1.5/docs/en/INFERENCE.md`
> § GenerationConfig Parameters and `docs/en/API.md` § `/v1/audio`.

## TL;DR

- ACE-Step 1.5 exposes **six output codecs**: `wav`, `wav32` (32-bit float),
  `flac` (lossless, default since v1.5), `mp3`, `opus`, `aac`.
- **No native `ogg` codec** — encode from a `flac` master via
  `ffmpeg -c:a libvorbis`.
- `audio_format` lives in **`GenerationConfig`** (not `GenerationParams`);
  in REST it is the `"audio_format"` field on `/release_task`.
- **Rule of thumb:** `flac` / `wav` for intermediate masters; `mp3` or
  `opus` for the user-facing delivery copy after loudnorm.

## 1. Supported formats

| Format | Type | Bit depth / rate | Size (3:30 stereo) | When to use |
| --- | --- | --- | --- | --- |
| `wav` | Uncompressed PCM | 16-bit / 48 kHz | ~40 MB | Editing, stems, archival |
| `wav32` | 32-bit float WAV | 32-bit float / 48 kHz | ~80 MB | Mastering chain / DAW handoff |
| `flac` | Lossless | 16-24-bit / 48 kHz | ~18-22 MB | Default master (fastest save, lossless) |
| `mp3` | Lossy | CBR 192-320 kbit/s | ~5-8 MB | Delivery copy, ubiquitous |
| `opus` | Lossy (modern) | 128-192 kbit/s | ~3-5 MB | Streaming, web embed, low-bandwidth |
| `aac` | Lossy (Apple) | 192-256 kbit/s | ~5-8 MB | Apple ecosystem delivery (m4a) |

> ACE-Step renders internally at **48 kHz stereo**; the codec inherits
> that rate. Re-encoding lossy → lossy compounds artifacts — treat
> `mp3` / `opus` / `aac` as **terminal formats**.

## 2. Decision tree

```text
Where will this file end up?
│
├── Stems / editing / DAW round-trip / archival master
│   └── wav (or wav32 if you need 32-bit float headroom)
│
├── Intermediate master → loudnorm → delivery copy
│   └── flac  ← upstream default
│
├── User-facing delivery copy (small)
│   ├── Apple ecosystem ──→ aac (m4a)
│   ├── Web / streaming  ──→ opus
│   └── Cross-platform   ──→ mp3 @ 192 kbps
│
└── User asked for a specific format (ogg / vorbis / wav / flac / mp3)
    └── Honor literally; convert with ffmpeg if needed
```

## 3. ACE-Step `audio_format` parameter

```python
from acestep.inference import GenerationParams, GenerationConfig, generate_music
config = GenerationConfig(batch_size=2, audio_format="flac")  # default
result = generate_music(dit_handler, llm_handler, params, config, save_dir="/out")
```

REST example:

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json '{
    "prompt": "upbeat indie pop, jangly guitars, four-on-the-floor kick, warm vocals",
    "audio_duration": 210,
    "thinking": true,
    "audio_format": "flac"
  }')
```

**Valid values:** `flac` (default), `mp3`, `opus`, `aac`, `wav`, `wav32`.
Output lands in
`${ACE_STEP_PATH}/.cache/acestep/tmp/api_audio/` per
[`acestep-generation.md`](acestep-generation.md) § "Cache caveat".

> **`output_format` is not an ACE-Step parameter name.** If a different
> tool uses that name, it is an alias for `audio_format`.

## 4. Post-processing with ffmpeg

```bash
# 4.1  Loudness-normalize the master (target streaming loudness)
ffmpeg -i master.flac \
  -af loudnorm=I=-16:TP=-1:LRA=11 -ar 48k -c:a flac master_norm.flac

# 4.2  mp3  (CBR 192 kbps — cross-platform safe default)
ffmpeg -i master_norm.flac -c:a libmp3lame -b:a 192k delivery.mp3

# 4.3  opus (web embed / streaming — better quality per byte than mp3)
ffmpeg -i master_norm.flac -c:a libopus -b:a 160k delivery.opus

# 4.4  aac  (Apple / m4a container)
ffmpeg -i master_norm.flac -c:a aac -b:a 192k delivery.m4a

# 4.5  ogg  (not exposed by ACE-Step — rewrap from flac)
ffmpeg -i master_norm.flac -c:a libvorbis -q:a 6 delivery.ogg

# 4.6  wav16 (DAW that insists on 16-bit)
ffmpeg -i master.flac -c:a pcm_s16le -ar 48000 master_16.wav

# 4.7  Verify loudness after re-encode
ffmpeg -i delivery.mp3 -af ebur128=framelog=verbose -f null - 2>&1 | grep "I:"
# Expect integrated loudness near -16 LUFS
```

`audio_quality.py` accepts any of these container/codec combinations
(decodes via the same ffmpeg path) — see
[`audition-rubric.md`](audition-rubric.md) § 5.

## 5. Footguns

1. **Re-encoding lossy → lossy compounds artifacts.** Encode `mp3` once
   from `flac`; do not chain `flac → mp3 → aac → opus`.
2. **`wav32` is two× the size of `wav`**; both are lossless. Reach for
   `wav32` only when a DAW mastering chain needs 32-bit float headroom.
3. **`opus` is not universally supported** on older Apple devices
   without a codec pack — validate on the target device before shipping.
4. **`audio_format` is in `GenerationConfig`, not `GenerationParams`.**
   The local REST API still accepts it in `/release_task` JSON, but the
   SDK split is intentional: format is a batch-level setting.
5. **Default is `flac`, not `mp3`.** v1.5 changed it from `mp3` to
   `flac` for faster save; older docs may show the old default.
6. **`ogg` requires external `ffmpeg`.** No `audio_format="ogg"` value
   exists by design (ACE-Step prefers modern codecs).

## 6. Sources

- `ACE-Step-1.5/docs/en/INFERENCE.md` § GenerationConfig Parameters —
  `audio_format` field, valid values, v1.5 default.
- `ACE-Step-1.5/docs/en/API.md` § `/v1/audio` — REST output format.
- `ACE-Step-1.5/docs/en/INFERENCE.md` § Best Practices — quality vs. speed
  format recommendations.

## 7. See also

- [`quality-and-revision.md`](quality-and-revision.md) § Delivery Copy —
  loudnorm command + verify checklist.
- [`acestep-generation.md`](acestep-generation.md) — baseline generation
  workflow, where the format option lives.
- [`acestep-xl-models.md`](acestep-xl-models.md) — XL DiT footguns that
  interact with format choice (always `wav` or `flac` for XL work).
