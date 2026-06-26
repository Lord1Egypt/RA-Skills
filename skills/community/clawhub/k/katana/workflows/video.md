## Video Generation Workflow

**Load this file when the user requests video generation.**

---

### ⚠️ Video Poll Timeout

The video API has a **6000-second (100-minute) server-side timeout**. Video jobs may legitimately run for extended periods. The standard 10-minute poll guard from SKILL.md is too aggressive for video — use a **100-minute guard** for video requests instead.

Typical video returns: < 800 seconds. The 6000s deadline is a worst-case limit.

---

## Model Selection

Check `{baseDir}/models.md` for full catalogue with pricing, durations, and capabilities.

For model aliases and selection, see `{baseDir}/models.md`. Top picks: `seedance-2-0-fast` (default), `ltx-2-3` (ltx).

If the user specifies an exact model ID, pass it through directly.

### Cost Warning

Video can be expensive. Always mention estimated cost before generating. See `{baseDir}/models.md` for full pricing.

---

Before submitting, present a pre-submission summary and wait for user confirmation (see `{baseDir}/SKILL.md` for the mandatory protocol). Include model, cost, duration, aspect ratio, exact prompt, and any reference images.

---

## Workflow

Follow the general workflow defined in `{baseDir}/SKILL.md` (pre-submission → payload → submit → poll → deliver). Video-specific notes:

- Include duration, aspect ratio, and any reference images in the pre-submission summary
- Video can be expensive — always highlight estimated cost
- **Poll timeout:** Video API timeout is 6000s (100 min). Use 100-minute guard for video polling, not the 10-minute image/text guard.

---

## Video Parameters

- `duration_seconds`: must match a value in the model's `video_lengths_and_costs`. Common: `5`, `10`, `15`.
- `aspect_ratio`: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. Default `16:9`. Check `models.md` for per-model support.
- `video_image_data.first_frame_image_url`: first frame image (URL or data URL).
- `video_image_data.mid_frame_image_url`: mid-frame image (some models).
- `video_image_data.last_frame_image_url`: last frame (some models).
- `video_image_data.reference_image_urls`: reference images (some models).
- `video_image_data.audio_input_urls`: audio references (some models).
- `video_image_data.video_list`: array of video input clips for V2V models (each object requires `url`; optional `start`/`ends` second offsets with `video_offset_allowed` rule).
- `reference_assets`: typed asset references (alternative to video_image_data). Image kinds (`style_reference`, `reference_image`, `image`) and audio kinds (`audio`, `source_audio`, `reference_audio`, `audio_reference`).

### Top-Level Compatibility Aliases

The API accepts several top-level aliases that map to `video_image_data` fields. The `video_image_data` forms are preferred for new integrations:

- Top-level `image_url`, `input_image_url`, `input_image`, `input_image_b64` → alias for `video_image_data.first_frame_image_url`
- Top-level `reference_image_urls` → alias for `video_image_data.reference_image_urls`

### Aspect Ratio: `auto`

`aspect_ratio: "auto"` uses the first frame dimensions, then the first reference image. Defaults to `1:1` if neither exists.

### Audio File Limits

Per-model audio file limit via `maximum_reference_audio_files`. There is a global cap of 4 audio files. Check `models.md` for per-model limits.

### Custom Rules (varies by model — check `models.md`)

Full glossary of named custom rules:

| Rule | Description |
|------|-------------|
| `audio_15s_max` | Combined audio limited to 15s |
| `audio_drives_duration` | Video duration follows audio duration |
| `audio_ff_only` | Audio only with first-frame conditioning |
| `audio_needs_reference_image` | Audio requires reference image |
| `audio_or_fflf_exclusive` | Audio cannot combine with frame inputs |
| `lf_needs_ff` | Last frame requires first frame |
| `reference_ff_only` | References may combine with first frame only |
| `reference_is_voice_timbre` | Audio interpreted as voice timbre when refs present |
| `reference_no_ff_or_lf` | References cannot combine with frame inputs |
| `video_required` | Model requires video input via `video_image_data.video_list` |
| `video_offset_allowed` | Accepts `start`/`ends` second offsets in `video_list` objects |
| `input_video_drives_length` | Input video determines output length; listed duration is max input and fixed cost |

Some models require image input (e.g. `seedance-pro`, `hailuo-2-minimax`, `kling-2-0`). Check `models.md` for per-model rules.

### Video-to-Video (V2V)

V2V models (e.g. `gemini-omni-v2v`) accept video input via `video_image_data.video_list`. Each object requires `url` (HTTPS video URL). Optional `start` and `ends` offsets in seconds (requires `video_offset_allowed` rule).

The input video clip drives the output length and billing tier (`input_video_drives_length`). The listed duration is the maximum accepted input and the fixed cost.

---



## Audio Output

Most modern video models generate audio alongside the video by default. The model interprets the prompt content for sound design — it doesn't just add ambient noise, but generates contextually appropriate audio (speech, music, environmental sounds, effects) based on what's described in the prompt and depicted in the visual content.

### Which models generate audio

**Audio output enabled (✓):** `seedance-2-0`, `seedance-2-0-480p`, `seedance-2-0-fast`, `ltx-2-3`, `gemini-omni`, `gemini-omni-v2v`, `happy-horse-1-0-1080p`, `happy-horse-1-0-720p`, `wan-2-7-1080p`, `wan-2-7-720p`, `kling-3-0-kling30pro`, `kling-o3-4k`, `kling-3-0-kling30`, `veo3-1`, `veo3-1-fast`, `veo3-1-lite`, `wan-2-5`

**Audio output silent (✗):** `seedance-pro`, `hailuo-2-minimax`, `kling-2-1-kling21`, `kling-2-1-kling21loop`, `seedance-lite`, `seedance-lite-loop`, `kling-2-0`, `kling-1-6`

See `{baseDir}/models.md` for the full table with the Audio Out column.

### Audio input vs audio output

Audio **input** (via `video_image_data.audio_input_urls`) and audio **output** are independent capabilities:
- Some models accept audio references for voice/sound conditioning **and** generate audio output (e.g. `seedance-2-0`)
- Some models generate audio output but don't accept audio references (e.g. `veo3-1`, `kling-3-0-kling30pro`)
- Legacy models may do neither

When a model supports both, the audio reference serves as a style/timbre guide — the model still generates new audio content interpreted from the prompt, not a copy of the reference.

### Suppressing audio

Currently there is no API parameter to disable audio output on models that generate it. If silent video is required, post-process with ffmpeg to strip the audio track:

```bash
ffmpeg -i input.mp4 -c:v copy -an silent_output.mp4
```

---

## Delivery

Follow the delivery pattern defined in `{baseDir}/SKILL.md`. Deliver the generated video to the user with: model name, duration, resolution, credits, dollar cost, description, and the full-res URL.

**Thumbnail preview:** `responses[].output_assets[].thumbnail_silent_video_mp4_url` may be present for video outputs — a short/silent lightweight MP4 preview suited to galleries and hover previews. Returned as blank string when unavailable. This is NOT the full video — always use `original_data_url` for delivery.

## Video Continuation

To chain video clips together:

1. Extract `final_frame_image_url` from the completed poll response (blank string when unavailable)
2. Use it as `video_image_data.first_frame_image_url` in the next video request
3. Stitch the resulting clips with ffmpeg (see `{baseDir}/workflows/post-process.md`)

This enables multi-shot video generation by using the last frame of one clip as the starting frame of the next.

---

## Pre-Submission Confirmation (MANDATORY)

If the user asks to edit, join, trim, crop, add text, add effects, convert format, or otherwise post-process a generated video, load `{baseDir}/workflows/post-process.md`.

---

## Error Handling

Follow the error handling protocol defined in `{baseDir}/SKILL.md`.

---

*Part of the Katana skill. See SKILL.md for routing, general configuration, and llms.txt freshness checks.*
