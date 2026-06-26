---
name: ppt-audio-to-video
description: Convert narration audio plus slide decks into a narrated video. Use when the user has an audio-only `mp4/m4a/mp3/wav` and a `ppt/pptx/pdf` deck, and needs slide images, transcript extraction, slide timing planning, or final `mp4` rendering with `whisper-cpp` and `ffmpeg`.
---

# PPT Audio To Video

Use this skill when the source video has narration audio but no usable slide visuals, and the final deliverable should be a slide-based lecture video.

Resolve bundled scripts relative to this skill directory. If the runtime has already opened this `SKILL.md`, prefer paths like `scripts/extract_slide_outline.py` and `scripts/render_from_timing_csv.py` instead of machine-specific absolute paths.

## Core workflow

1. Inventory inputs.
   - Confirm which of these exist: audio-only `mp4/m4a/mp3/wav`, `ppt/pptx`, `pdf`, and any pre-rendered slide images.
   - Prefer an existing `pdf` or image directory for rendering. Treat `pptx` as the source of slide text and as a fallback for export.

2. Prepare tools.
   - Required for deterministic steps: `ffmpeg`, `ffprobe`, `pdftoppm`.
   - Required for transcription: `whisper-cli` from `whisper-cpp` plus a multilingual model such as `ggml-small.bin`.
   - If only `pptx` exists and no `pdf/images` exist, prefer `Keynote` or `PowerPoint` export on macOS. Use `soffice` only as fallback because profile or rendering issues are common.

3. Produce slide images.
   - If `pdf` exists, render it to images:
     ```bash
     pdftoppm -png -r 200 "$PDF" "$OUTDIR/slide"
     ```
   - If only `pptx` exists, export to `pdf` or slide images with `Keynote` or `PowerPoint`, then continue from `pdf`.
   - Keep slide filenames ordered and stable, such as `slide-01.png`, `slide-02.png`, ...

4. Extract slide text.
   - Run:
     ```bash
     python3 scripts/extract_slide_outline.py \
       --pptx "$PPTX" \
       --out "$WORKDIR/slide_outline.csv"
     ```
   - Use the output to identify slide titles, distinctive keywords, and section changes.

5. Extract clean audio for ASR.
   - For audio-only `mp4`, extract mono `wav`:
     ```bash
     ffmpeg -y -i "$AUDIO_MP4" -ar 16000 -ac 1 -c:a pcm_s16le "$WORKDIR/audio.wav"
     ```
   - If the source is already `wav/mp3/m4a`, convert to the same mono `wav` form if needed.

6. Transcribe with `whisper-cli`.
   - Example:
     ```bash
     whisper-cli -ng \
       -m "$MODEL" \
       -f "$WORKDIR/audio.wav" \
       -l zh \
       -ocsv -osrt -of "$WORKDIR/transcript"
     ```
   - Prefer `transcript.csv` for downstream parsing. `transcript.srt` is useful for manual review.
   - If GPU allocation fails on macOS, retry with `-ng` to force CPU mode.

7. Build `slide_timings.csv`.
   - Do not average slide durations unless the user explicitly asks for it.
   - Read the transcript and slide outline together, then create a monotonic timing plan by topic changes, section boundaries, and unique keywords.
   - Use this schema:
     ```csv
     slide,start_sec,end_sec,duration_sec,reason
     1,0.000,15.000,15.000,opening title and agenda
     2,15.000,100.000,85.000,architecture overview starts here
     ```
   - Keep slide numbers sequential and ensure `duration_sec = end_sec - start_sec`.
   - Validate that the last `end_sec` matches the audio duration or is within a small tolerance.

8. Render the final video.
   - Run:
     ```bash
     python3 scripts/render_from_timing_csv.py \
       --images "$SLIDE_IMAGES_DIR" \
       --timings "$WORKDIR/slide_timings.csv" \
       --audio "$WORKDIR/audio.wav" \
       --output "$OUT_VIDEO"
     ```
   - The script generates an `ffconcat` file, validates timing continuity, and calls `ffmpeg` to encode the final `mp4`.

9. Verify and iterate.
   - Check output duration with `ffprobe`.
   - If a slide cuts too early or too late, edit only the affected rows in `slide_timings.csv` and rerun the render script.
   - Keep the transcript, outline, and timing CSV as reproducible working files.

## Heuristics for timing alignment

- Use section-divider slides briefly. These slides usually hold for 5-20 seconds.
- Use the first segment that clearly switches topic as the next slide start.
- Prefer exact topic transitions over title-word matching. ASR often distorts proper nouns and product names.
- Let the model infer timings, but keep the render step deterministic through `slide_timings.csv`.
- When confidence is low, produce a first-cut video and tell the user which slide boundaries likely need review.

## Common commands

Install dependencies on macOS if missing:
```bash
brew install ffmpeg poppler whisper-cpp
```

Typical multilingual model download:
```bash
mkdir -p .models
curl -L 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin' -o .models/ggml-small.bin
```

## Bundled scripts

- `scripts/extract_slide_outline.py`
  Extract slide text from `pptx` into CSV or JSON for timing analysis.
- `scripts/render_from_timing_csv.py`
  Validate a timing CSV, generate an `ffconcat`, and render the final video with `ffmpeg`.
