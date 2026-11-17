---
name: produce-voiceover-teaching-video
description: Turn a supplied narration audio file plus an article, notes, screenshots, images, or source videos into a fact-checked faceless vertical teaching video, synchronized captions, cover, publish copy, hashtags, and pinned comment. Use when a user provides a cloned or recorded MP3/WAV and wants a multi-agent edit with privacy-scoped local job state, adjustable speech rate, semantic media placement, original-video interludes, mobile-safe text, modern transitions, final QC, and social publishing assets.
---

# Voiceover Teaching Video Factory

Act as the director of a seven-worker production line. Treat the supplied narration as sensitive source material and the prepared narration duration as the timeline authority. Do not clone a voice, upload source media, or publish the finished video unless the user explicitly requests that separate action.

## Required setup

Require `ffmpeg`, `ffprobe`, Python 3.10+, and a video renderer capable of deterministic 9:16 output. Prefer HyperFrames when installed; otherwise use the existing renderer in the repository or an FFmpeg composition. Use local Whisper only when no transcript or reliable timing exists.

Read these references before execution:

- `references/workflow.md` for the seven roles and wave schedule.
- `references/contracts.md` for stage artifacts and handoff fields.
- `references/performance.md` for `fast`, `balanced`, and `quality` modes.
- `references/publishing.md` before creating the cover or social copy.

## Capability boundary

- Read only the Skill's own files and inputs explicitly supplied for the job. Copy user media into the selected job directory and keep all derivatives there.
- Write only inside the selected job directory and the user-selected delivery directory. Reject any implicit request to scan unrelated folders.
- Limit shell execution to `ffmpeg`, `ffprobe`, Python, the selected renderer, and bundled scripts required by this workflow.
- Do not enumerate environment variables, credential stores, browser sessions, cookies, or unrelated repositories.
- Normal local production requires no network access. Fetch a user-provided article URL or publish to a named destination only when the user explicitly requests that action and scopes the destination.
- Never run registry-maintenance, package-publishing, installation, or self-modification commands as part of a video job.

## Initialize the job

Create a new job directory outside the skill folder. Never write user media into the skill directory.

```bash
python scripts/jobctl.py init \
  --job-dir <job-dir> \
  --article <article-or-notes> \
  --audio <voiceover.mp3-or-wav> \
  --images <image-1> <image-2> \
  --videos <video-1> <video-2> \
  --mode fast \
  --speech-rate 1.15 \
  --source-video-speed 1.0
```

Use `--speech-rate 1.2` only when the user explicitly requests 1.2x. If the user gives a target duration instead, run `scripts/prepare_voiceover.py --target-minutes <min>-<max>` and reject an automatically calculated rate outside `0.85-1.35`; ask the user whether the script or duration should change.

## Run seven workers

Use subagents when the host supports them. Give each worker only the artifact paths listed in `references/workflow.md`, never the full conversation. Run independent roles in parallel; otherwise run the same roles sequentially without changing their contracts.

1. Intake and rights worker
2. Timing and captions worker
3. Editorial distillation worker
4. Teaching storyboard worker
5. Visual preparation worker
6. Composition and finishing worker
7. QC and publishing worker

Every worker must write a compact JSON report with `status: pass|needs-human|fail`. A failure returns only to the worker that owns the defective artifact. Do not rerun completed upstream roles unless their input hash changed.

## Editing contract

- Prepare the speech rate once, before transcription and alignment. Preserve pitch with FFmpeg `atempo`; never speed the final mixed video as a shortcut.
- Preserve conversational cadence. Detect silence before retiming, shorten only outlier pauses of roughly 0.85 seconds or longer to about 0.30-0.40 seconds, and keep normal phrase boundaries intact. Do not cut inside English names, numbers, or source-video boundaries.
- Prefer the FFmpeg Rubber Band filter with formant preservation when available; fall back to `atempo`. Align captions after pause cleanup and retiming.
- Keep the voice understandable. Default to `1.0x`; recommend `1.1-1.2x` for concise explainers and require explicit approval above `1.25x`.
- Honor an explicit speech rate exactly. For a requested `1.15x`, retime narration, captions, and narration-led visuals together while keeping embedded source videos at `1.0x` unless the user separately changes their speed.
- Map every visual to the sentence it explains. Do not distribute article images evenly or use a screenshot merely because it is available.
- Treat a source video with meaningful audio as a standalone interlude by default. Pause narration and narration captions, play the source video at natural speed with only its original audio, then resume narration at the exact next word and matching visual beat.
- Never mix cloned narration over a source-video interlude. Use muted source footage under narration only when the user explicitly requests B-roll treatment or the clip has no meaningful audio.
- Default to 1080x1920, 30 fps, H.264 High, yuv420p, and AAC 48 kHz for delivery.
- Keep captions and critical labels inside conservative mobile safe bounds. Remove source-account branding, unrelated headers, and engagement prompts when the user requests it.
- Keep every frame visually occupied. Use a meaningful poster frame or designed fallback while media initializes; do not leave blank opening, transition, or ending frames.
- Use restrained modern transitions. A card flip, vertical card exchange, or depth slide may bridge major sections; use simple cuts inside procedural steps.
- Do not invent claims. Verify names, numbers, dates, and quoted statements against the frozen local source.
- Use only licensed source images, fonts, music, sound effects, and authorized voice recordings.
- Add a voiced ending CTA only from authorized audio: a supplied CTA take, a verified phrase already present in the approved recording, or newly generated speech after explicit authorization. Otherwise use a text-only CTA.

## Fast production loop

1. Prepare the narration and timing artifacts.
2. Build the storyboard and visual manifest before authoring the composition.
3. Render a low-cost proxy defined by the selected mode.
4. Inspect the first frame, every configured sample interval, every transition boundary, and the last frame. Run automated overflow, black-frame, decode, and loudness checks.
5. Inspect the start, midpoint, end, and both boundaries of every source-video interlude. Confirm original audio is present and narration/captions are absent during playback.
6. Repair only affected scenes or render chunks. Reuse unchanged chunks by cache key.
7. Render the full-resolution final once after the proxy gate passes.
8. Create `cover.png` and `publish-copy.json`, then run `scripts/validate_delivery.py`.

Never perform a second full render for a copy-only or outro-only change when a local scene/chunk replacement is possible.
Keep one canonical `08-delivery/final.mp4`. For revisions, build and fully decode a temporary master, then atomically replace the canonical file. Do not create `v2`, `final-final`, or other duplicate deliveries unless the user asks for versions.

## Delivery gate

Deliver only when all of the following exist and validation passes:

- `08-delivery/final.mp4`
- `08-delivery/cover.png`
- `08-delivery/publish-copy.json`
- `07-qc/qc-report.json`

The final response must report the absolute output paths, duration, speech rate, resolution, frame rate, loudness result, mode, and any rights items that still need human confirmation.
When source videos are present, also report their count, playback speed, original-audio policy, and confirmation that narration pauses and resumes.

## Bundled scripts

- `scripts/jobctl.py`: initialize jobs, hash inputs, track stages, and validate handoffs.
- `scripts/prepare_voiceover.py`: apply pitch-preserving speed changes and write audio metadata.
- `scripts/render_cover.py`: render an exact-text 9:16 technology-style cover without model-generated text.
- `scripts/validate_delivery.py`: probe the final MP4, cover, publish copy, and QC report.
